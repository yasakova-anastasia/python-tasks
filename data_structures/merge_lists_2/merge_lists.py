import typing as tp
import heapq


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    heap: list[tp.Any] = []
    id = 0
    for i in seq:
        if len(i):
            id += 1
            heapq.heappush(heap, (i[0], id, (i, 0)))

    result: list[int] = []
    while len(heap):
        idx = heap[0][2][1]
        result.append(heap[0][2][0][idx])
        curr = heapq.heappop(heap)[2]

        if len(curr[0]) - 1 > idx:
            id += 1
            heapq.heappush(heap, (curr[0][idx + 1], id, (curr[0], idx + 1)))

    return result
