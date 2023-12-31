from typing import Iterable, Sized, Any


class Range(Sized, Iterable[int]):
    """The range-like type, which represents an immutable sequence of numbers"""

    def __init__(self, *args: int) -> None:
        """
        :param args: either it's a single `stop` argument
            or sequence of `start, stop[, step]` arguments.
        If the `step` argument is omitted, it defaults to 1.
        If the `start` argument is omitted, it defaults to 0.
        If `step` is zero, ValueError is raised.
        """
        self.data = range(*args)
        self.args: Any = args
        if len(args) == 1:
            self.args = list([0, *args])
        elif len(args) == 2 or args[2] == 1:
            self.args = list(args)[:2]
        else:
            self.args = args

    def __iter__(self) -> 'Range.RangeIterator':  # type: ignore
        for val in self.data:
            yield val

    def __repr__(self) -> str:
        return "range(" + ','.join(map(str, self.args)) + ")"

    def __str__(self) -> str:
        return "range(" + ', '.join(map(str, self.args)) + ")"

    def __contains__(self, key: int) -> bool:
        return key in self.data

    def __getitem__(self, key: int) -> int:
        return self.data[key]

    def __len__(self) -> int:
        return len(self.data)
