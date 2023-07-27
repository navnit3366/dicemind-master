from typing import Callable, NamedTuple, List
from lark import Visitor, Tree
from random import randint
from decimal import Decimal
from enum import IntFlag


class Dice(NamedTuple):
    amount: int
    power: int


class RolledValueFlag(IntFlag):
    CRIT = 1 << 0
    FAIL = 1 << 1
    DISCARDED = 1 << 2


class RolledValue:
    def __init__(self, value: Decimal, flags: RolledValueFlag = 0):
        self.value = value
        self.flags = flags


class Roller(Visitor):
    def __init__(self, roll_one: Callable[[Dice, Tree], List[Decimal]]):
        self.roll_one = roll_one

    def dice(self, expr):
        die = Dice(expr.meta.amount, expr.meta.power)
        expr.meta.rolls = [
            RolledValue(x) for x in self.roll_one(die, expr)
        ]

        # Apply roll flags
        for roll in expr.meta.rolls:
            flags = RolledValueFlag(0)

            if roll.value == die.power:
                flags |= RolledValueFlag.CRIT
            elif roll.value == 1:
                flags |= RolledValueFlag.FAIL

            roll.flags = flags

    def roll(self, tree: Tree):
        self.visit(tree)


DEFAULT_ROLLER = Roller(
    lambda d, _: [Decimal(randint(1, d.power)) for _ in range(d.amount)]
)
