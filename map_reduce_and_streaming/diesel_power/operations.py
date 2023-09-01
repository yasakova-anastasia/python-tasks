import functools
import heapq
import itertools
import operator
import re
import string
import typing as tp
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Generator, Sequence
from typing import Any, Optional

TRow = dict[str, tp.Any]
TRowsIterable = tp.Iterable[TRow]
TRowsGenerator = tp.Generator[TRow, None, None]


class Operation(ABC):
    @abstractmethod
    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        pass


class Read(Operation):
    def __init__(self, filename: str, parser: tp.Callable[[str], TRow]) -> None:
        self.filename = filename
        self.parser = parser

    def __call__(self, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        with open(self.filename) as f:
            for line in f:
                yield self.parser(line)


class ReadIterFactory(Operation):
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        for row in kwargs[self.name]():
            yield row


# Operations


class Mapper(ABC):
    """Base class for mappers"""
    @abstractmethod
    def __call__(self, row: TRow) -> TRowsGenerator:
        """
        :param row: one table row
        """
        pass


class Map(Operation):
    def __init__(self, mapper: Mapper) -> None:
        self.mapper = mapper

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        for row in rows:
            yield from self.mapper(row)


class Reducer(ABC):
    """Base class for reducers"""
    @abstractmethod
    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        """
        :param rows: table rows
        """
        pass


class Reduce(Operation):
    def __init__(self, reducer: Reducer, keys: tp.Sequence[str]) -> None:
        self.reducer = reducer
        self.keys = keys

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        for _, val in itertools.groupby(rows, operator.itemgetter(*self.keys)):
            yield from self.reducer(tuple(self.keys), val)


class Joiner(ABC):
    """Base class for joiners"""
    def __init__(self, suffix_a: str = '_1', suffix_b: str = '_2') -> None:
        self._a_suffix = suffix_a
        self._b_suffix = suffix_b

    def _join_rows(self, keys: Sequence[str], row_a: TRow, row_b: TRow) -> TRow:
        cols = (row_a.keys() & row_b.keys()) - set(keys)
        res: TRow = dict()
        for row, suff in zip((row_a, row_b), (self._a_suffix, self._b_suffix)):
            for col, val in row.items():
                key = col + suff if col in cols else col
                res[key] = val
        return res

    @abstractmethod
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        """
        :param keys: join keys
        :param rows_a: left table rows
        :param rows_b: right table rows
        """
        pass


class Join(Operation):
    def __init__(self, joiner: Joiner, keys: tp.Sequence[str]):
        self.keys = keys
        self.joiner = joiner

    def _row_selector(self, rows: TRowsIterable
                      ) -> Generator[tuple[Optional[tuple[Any, ...]], Optional[TRowsIterable]], None, None]:
        if self.keys:
            yield from itertools.groupby(rows, operator.itemgetter(*self.keys))
        else:
            yield tuple(), rows
        yield None, None

    def __call__(self, rows: TRowsIterable, *args: tp.Any, **kwargs: tp.Any) -> TRowsGenerator:
        f_grouper = self._row_selector(rows)
        s_grouper = self._row_selector(args[0])
        f_key, f_group = next(f_grouper)
        s_key, s_group = next(s_grouper)

        while f_key is not None and s_key is not None:
            if f_key < s_key:
                yield from self.joiner(self.keys, f_group or [], [])
                f_key, f_group = next(f_grouper)
                continue

            if f_key == s_key:
                yield from self.joiner(self.keys, f_group or [], s_group or [])
                f_key, f_group = next(f_grouper)
                s_key, s_group = next(s_grouper)
                continue

            if f_key > s_key:
                yield from self.joiner(self.keys, [], s_group or [])
                s_key, s_group = next(s_grouper)
                continue

        while f_key is not None:
            yield from self.joiner(self.keys, f_group or [], [])
            f_key, f_group = next(f_grouper)

        while s_key is not None:
            yield from self.joiner(self.keys, [], s_group or [])
            s_key, s_group = next(s_grouper)


# Dummy operators


class DummyMapper(Mapper):
    """Yield exactly the row passed"""
    def __call__(self, row: TRow) -> TRowsGenerator:
        yield row


class FirstReducer(Reducer):
    """Yield only first row from passed ones"""
    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        for row in rows:
            yield row


# Mappers


class FilterPunctuation(Mapper):
    """Left only non-punctuation symbols"""
    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    def __call__(self, row: TRow) -> TRowsGenerator:
        row[self.column] = "".join(list(filter(lambda x: x not in string.punctuation, row[self.column])))
        yield row


class LowerCase(Mapper):
    """Replace column value with value in lower case"""
    def __init__(self, column: str):
        """
        :param column: name of column to process
        """
        self.column = column

    @staticmethod
    def _lower_case(txt: str) -> str:
        return txt.lower()

    def __call__(self, row: TRow) -> TRowsGenerator:
        row[self.column] = self._lower_case(row[self.column])
        yield row


class Split(Mapper):
    """Split row on multiple rows by separator"""
    def __init__(self, column: str, separator: str | None = None) -> None:
        """
        :param column: name of column to split
        :param separator: string to separate by
        """
        self.column = column
        self.separator = separator

    @staticmethod
    def itersplit(text: str, sep: Optional[str]) -> Generator[str, None, None]:
        sep = sep or r"\s+"
        matches = re.finditer(r'\w+', text)
        for match in matches:
            yield match.group(0)

    def __call__(self, row: TRow) -> TRowsGenerator:
        for val in self.itersplit(row[self.column], self.separator):
            new = row.copy()
            new[self.column] = val
            yield new


class Product(Mapper):
    """Calculates product of multiple columns"""
    def __init__(self, columns: tp.Sequence[str], result_column: str = 'product') -> None:
        """
        :param columns: column names to product
        :param result_column: column name to save product in
        """
        self.columns = columns
        self.result_column = result_column

    def __call__(self, row: TRow) -> TRowsGenerator:
        prod = {col: row[col] for col in row.keys() & self.columns}
        res = row.copy()
        res[self.result_column] = functools.reduce(operator.mul, prod.values())
        yield res


class Filter(Mapper):
    """Remove records that don't satisfy some condition"""
    def __init__(self, condition: tp.Callable[[TRow], bool]) -> None:
        """
        :param condition: if condition is not true - remove record
        """
        self.condition = condition

    def __call__(self, row: TRow) -> TRowsGenerator:
        if self.condition(row):
            yield row


class Project(Mapper):
    """Leave only mentioned columns"""
    def __init__(self, columns: tp.Sequence[str]) -> None:
        """
        :param columns: names of columns
        """
        self.columns = columns

    def __call__(self, row: TRow) -> TRowsGenerator:
        yield {col: row[col] for col in self.columns}


# Reducers


class TopN(Reducer):
    """Calculate top N by value"""
    def __init__(self, column: str, n: int) -> None:
        """
        :param column: column name to get top by
        :param n: number of top values to extract
        """
        self.column_max = column
        self.n = n

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        yield from heapq.nlargest(self.n, rows, key=operator.itemgetter(self.column_max))


class TermFrequency(Reducer):
    """Calculate frequency of values in column"""
    def __init__(self, words_column: str, result_column: str = 'tf') -> None:
        """
        :param words_column: name for column with words
        :param result_column: name for result column
        """
        self.words_column = words_column
        self.result_column = result_column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        cnt: defaultdict[str, int] = defaultdict(int)
        last: TRow = dict()
        for row in rows:
            cnt[row[self.words_column]] += 1
            last = row
        tmp = {col: val for col, val in last.items() if col in group_key}
        words = sum(cnt.values())
        for col, val in cnt.items():
            row = tmp.copy()
            row[self.words_column] = col
            row[self.result_column] = val / words
            yield row


class Count(Reducer):
    """
    Count records by key
    Example for group_key=('a',) and column='d'
        {'a': 1, 'b': 5, 'c': 2}
        {'a': 1, 'b': 6, 'c': 1}
        =>
        {'a': 1, 'd': 2}
    """
    def __init__(self, column: str) -> None:
        """
        :param column: name for result column
        """
        self.column = column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        cnt: defaultdict[str, int] = defaultdict(int)
        vals: dict[str, Any] = dict()
        for row in rows:
            for key in group_key:
                cnt[key] += 1
                vals[key] = row[key]
        for key, value in cnt.items():
            yield {self.column: value, key: vals[key]}


class Sum(Reducer):
    """
    Sum values aggregated by key
    Example for key=('a',) and column='b'
        {'a': 1, 'b': 2, 'c': 4}
        {'a': 1, 'b': 3, 'c': 5}
        =>
        {'a': 1, 'b': 5}
    """
    def __init__(self, column: str) -> None:
        """
        :param column: name for sum column
        """
        self.column = column

    def __call__(self, group_key: tuple[str, ...], rows: TRowsIterable) -> TRowsGenerator:
        sums: defaultdict[str, int] = defaultdict(int)
        vals: dict[str, Any] = dict()
        for row in rows:
            for key in group_key:
                sums[key] += row[self.column]
                vals[key] = row[key]
        for key, value in sums.items():
            yield {self.column: value, key: vals[key]}


# Joiners


class InnerJoiner(Joiner):
    """Join with inner strategy"""
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        cache_b = list(rows_b)
        for a in rows_a:
            for b in cache_b:
                yield self._join_rows(keys, a, b)


class OuterJoiner(Joiner):
    """Join with outer strategy"""
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        cache_a = list(rows_a)
        cache_b = list(rows_b)

        if not cache_a:
            yield from cache_b

        if not cache_b:
            yield from cache_a

        for a in cache_a:
            for b in cache_b:
                yield self._join_rows(keys, a, b)


class LeftJoiner(Joiner):
    """Join with left strategy"""
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        cache_b = list(rows_b)

        if not cache_b:
            yield from rows_a

        for row_a in rows_a:
            for row_b in cache_b:
                yield self._join_rows(keys, row_a, row_b)


class RightJoiner(Joiner):
    """Join with right strategy"""
    def __call__(self, keys: tp.Sequence[str], rows_a: TRowsIterable, rows_b: TRowsIterable) -> TRowsGenerator:
        cache_a = list(rows_a)

        if not cache_a:
            yield from rows_b

        for row_b in rows_b:
            for row_a in cache_a:
                yield self._join_rows(keys, row_b, row_a)
