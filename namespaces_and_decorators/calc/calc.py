import sys
import math
from typing import Any

PROMPT = '>>> '


def run_calc(context: dict[str, Any] | None = None) -> None:
    """Run interactive calculator session in specified namespace"""
    inp = sys.stdin
    out = sys.stdout

    out.write(PROMPT)
    out.flush()
    result = inp.readline().strip("\n")
    while len(result):
        out.write(str(eval(result, {'__builtins__': {}}, context)) + '\n')
        out.write(PROMPT)
        out.flush()
        result = inp.readline().strip("\n")
    out.write('\n')
    out.flush()


if __name__ == '__main__':
    context = {'math': math}
    run_calc(context)
