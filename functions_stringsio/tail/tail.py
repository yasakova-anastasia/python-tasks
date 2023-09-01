import typing as tp
from pathlib import Path
import os.path as osp
import sys


def tail(filename: Path, lines_amount: int = 10, output: tp.IO[bytes] | None = None) -> None:
    """
    :param filename: file to read lines from (the file can be very large)
    :param lines_amount: number of lines to read
    :param output: stream to write requested amount of last lines from file
                   (if nothing specified stdout will be used)
    """
    curr: tp.List[int] = []
    count = 0
    prev_pos = 0
    curr_pos = 0
    step = 0
    n = osp.getsize(filename)
    if n > 0:
        with open(filename, 'rb') as f:
            prev_pos = f.seek(0, 2)
            while (count < lines_amount and prev_pos > 0):
                if (-1) * (step - 1000) > n:
                    curr_pos = f.seek((step - prev_pos), 1)
                    b = bytearray(prev_pos)
                else:
                    curr_pos = f.seek(step - 1000, 1)
                    b = bytearray(1000)
                if prev_pos == curr_pos:
                    curr_pos = f.seek(prev_pos * (-1), 1)
                    b = bytearray(prev_pos)
                f.readinto(b)
                m = memoryview(b)
                list_bytes = list(m)
                if len(curr) == 0:
                    curr = list_bytes
                else:
                    curr = list_bytes + curr
                while curr.count(10) > lines_amount + 1:
                    i = curr.index(10)
                    curr = curr[i + 1:]
                if curr.count(10) == lines_amount + 1:
                    i = curr.index(10)
                    curr = curr[i + 1:]
                    break
                prev_pos = curr_pos
                if step == 0:
                    step = -1000
    out = sys.stdout.buffer
    if output is not None:
        out = output  # type: ignore
    out.write(bytes(curr))
