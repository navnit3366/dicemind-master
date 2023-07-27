from lark import Tree, Token, Transformer, Discard
from abc import ABC, abstractmethod
from typing import Optional, Dict


class InlineError(BaseException):
    def __init__(self, macro: str):
        self.macro = macro

    def __str__(self) -> str:
        return f"Couldn't inline macro `{self.macro}`"


class AbstractInlineTable(ABC):
    @abstractmethod
    def get(self, name: str) -> Optional[Tree]:
        ...

    @abstractmethod
    def put(self, name: str, tree: Tree):
        ...


class DictInlineTable(AbstractInlineTable):
    def __init__(self, dictionary: Dict[str, Tree]):
        self.table = dictionary

    def get(
        self, name: str, meta: Optional[object] = None
    ) -> Optional[Tree]:
        del meta
        if tree := self.table.get(name):
            return tree
        else:
            raise InlineError(name)

    def put(self, name: str, tree: Tree, meta: Optional[object] = None):
        del meta
        self.table[name] = tree


DEFAULT_INLINE_TABLE = DictInlineTable(
    {"one": Tree("number", [Token("NUMBER", "1")])}
)


class Inliner(Transformer):
    def __init__(self, inline_table: AbstractInlineTable):
        self.inline_table = inline_table

    def binding(self, children):
        varname, expr = children
        self.inline_table.put(varname.children[0].value, expr)
        raise Discard()

    def var(self, children):
        varname = children[0].value
        return Tree("paren", [self.inline_table.get(varname)])
