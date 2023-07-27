from decimal import Decimal
from lark.visitors import Interpreter as LarkInterpreter
from .roller import RolledValueFlag, Roller


class PlaintextStringifier(LarkInterpreter):
    def add(self, tree) -> str:
        first, second, *_ = self.visit_children(tree)
        return f"{first} + {second}"

    def sub(self, tree) -> str:
        first, second, *_ = self.visit_children(tree)
        return f"{first} - {second}"

    def mul(self, tree) -> str:
        first, second, *_ = self.visit_children(tree)
        return f"{first} * {second}"

    def div(self, tree) -> str:
        first, second, *_ = self.visit_children(tree)
        return f"{first} / {second}"

    def neg(self, tree) -> str:
        return f"-{self.visit_children(tree)[0]}"

    def dice(self, tree) -> str:
        dice = f"{tree.meta.amount if tree.meta.amount > 1 else ''}d{tree.meta.power}"
        rolls = self.rolls(tree)
        return f"{dice} [ {rolls} ]"

    def rolls(self, tree) -> str:
        return ", ".join(
            [
                f"{x.value}!"
                if (
                    x.flags & RolledValueFlag.CRIT
                    or x.flags & RolledValueFlag.FAIL
                )
                else str(x.value)
                for x in tree.meta.rolls
            ]
        )

    def number(self, token) -> str:
        return token.children[0].value

    def paren(self, tree) -> str:
        value, *_ = self.visit_children(tree)
        return f"({value})"

    def binding(self, tree) -> str:
        varname, expr = self.visit_children(tree)
        return f"{varname} := {expr}"

    def var(self, tree) -> str:
        return tree.children[0].value

    def stringify(self, tree) -> str:
        return self.visit(tree)


class MarkdownStringifier(PlaintextStringifier):
    def rolls(self, tree) -> str:
        return ", ".join(
            [
                f"**{x.value}**"
                if (
                    x.flags & RolledValueFlag.CRIT
                    or x.flags & RolledValueFlag.FAIL
                )
                else str(x.value)
                for x in tree.meta.rolls
            ]
        )
