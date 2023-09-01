import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """
    lines = inp.read().split("\n")
    for line in lines:
        if line == '':
            continue
        items = line.split("\t")
        out.write(items[0][0:7] + '.' * (73 - len(items[-1])) + items[-1] + '\n')
