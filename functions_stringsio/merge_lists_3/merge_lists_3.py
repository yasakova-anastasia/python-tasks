import typing as tp
import heapq


def merge(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    flag = False
    heap: list[tp.Any] = []
    ident = 0
    for line in input_streams:
        if line != b'':
            bytes = line.read().split(b'\n')
            digits = [int(s.decode("utf-8")) for s in bytes if s != b'']
            if len(digits):
                heapq.heappush(heap, (digits[0], ident, (digits, 0)))
                ident += 1
    while len(heap) != 0:
        val = heap[0]
        heapq.heappop(heap)
        output_stream.write(str(val[0]).encode("utf-8") + b'\n')
        flag = True
        if val[2][1] + 1 < len(val[2][0]):
            new_index = val[2][1] + 1
            heapq.heappush(heap, (val[2][0][new_index], ident, (val[2][0], new_index)))
            ident += 1
    if not flag:
        output_stream.write(b'\n')
