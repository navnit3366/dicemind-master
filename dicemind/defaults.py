from .parsing import parse, optimize
from .roller import DEFAULT_ROLLER
from .interpreter import Interpreter
from .stringifier import PlaintextStringifier
from .inliner import Inliner, DEFAULT_INLINE_TABLE

from typing import Tuple, Optional, Generator, Callable
from decimal import Decimal


def roll_func(
    interpreter=Interpreter(),
    stringifier=PlaintextStringifier(),
    inliner=Inliner(DEFAULT_INLINE_TABLE),
    roller=DEFAULT_ROLLER,
) -> Callable[
    [str], Generator[Tuple[str, Optional[Decimal]], None, None]
]:
    def curried(query: str):
        parsed = parse(query)
        inlined = inliner.transform(parsed)
        optimal = optimize(inlined)
        roller.roll(optimal)

        strings = stringifier.stringify(optimal)
        values = interpreter.evaluate(optimal)

        for (string, result) in zip(strings, values):
            yield string, result

    return curried
