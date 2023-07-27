from .parsing import parse, optimize
from .roller import DEFAULT_ROLLER
from .interpreter import Interpreter
from .stringifier import PlaintextStringifier
from .inliner import InlineError, Inliner, DEFAULT_INLINE_TABLE
from lark import UnexpectedCharacters
from .defaults import roll_func

interpreter = Interpreter()
stringifier = PlaintextStringifier()
inliner = Inliner(DEFAULT_INLINE_TABLE)


def main(*args, **kwargs):
    del args
    del kwargs

    roll = roll_func()

    while query := input("> "):
        try:
            for (string, result) in roll(query):
                if result is not None:
                    print(f"{string} = {result}")
                else:
                    # There was a binding, no need for equal sign
                    print(string)

        except InlineError as err:
            print(err)
        except UnexpectedCharacters as err:
            print(err)
        except BaseException as err:
            raise err


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
