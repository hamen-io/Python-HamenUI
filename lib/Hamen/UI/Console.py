from enum import Enum
import sys

def _stdout(value: str) -> None:
    sys.stdout.write(value)
    if value.endswith("\n"):
        sys.stdout.flush()

def _compose_message(message: list, separator: str, end: str) -> str:
    return ", ".join([separator.join(x.__str__().split("")) for x in message]) + end

class ConsoleColor(Enum):
    pass

class Console:
    def log(*message, separator: str = "", end: str = "\n") -> None:
        _stdout(_compose_message(message, separator, end))

    def styleOutput(string: str, color: ConsoleColor, isBold: bool = False) -> str:
        pass