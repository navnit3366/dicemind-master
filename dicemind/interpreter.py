from lark.visitors import Interpreter as LarkInterpreter
from decimal import Decimal
from typing import Optional
from lark.tree import Tree


class Interpreter(LarkInterpreter):
    def add(self, tree) -> Decimal:
        return sum(self.visit_children(tree))

    def sub(self, tree) -> Decimal:
        first, second, *_ = self.visit_children(tree)
        return first - second

    def mul(self, tree) -> Decimal:
        first, second, *_ = self.visit_children(tree)
        return first * second

    def div(self, tree) -> Decimal:
        first, second, *_ = self.visit_children(tree)
        return first / second

    def neg(self, tree) -> Decimal:
        return -self.visit_children(tree)[0]

    def dice(self, tree) -> Decimal:
        return sum(x.value for x in tree.meta.rolls)

    def number(self, token) -> Decimal:
        return Decimal(token.children[0].value)

    def paren(self, tree) -> Decimal:
        value, *_ = self.visit_children(tree)
        return value

    def binding(self, *args) -> None:
        # Bindings are not evaluated
        return None

    def evaluate(self, tree: Tree) -> Optional[Decimal]:
        return self.visit(tree)
