

def count_util(text: str, flags: str | None = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """
    lines = text.split("\n")
    # if lines[len(lines) - 1] == "":
    #     lines.pop()
    words = text.split()
    if (flags is None) or (len(flags) == 0):
        flags = "-mlLw"
    res = {}
    for s in flags:
        if "m" in s:
            res["chars"] = 0
        if "l" in s:
            res["lines"] = 0
        if "L" in s:
            res["longest_line"] = 0
        if "w" in s:
            res["words"] = 0
    for k in res.keys():
        if k == "chars":
            res[k] = len(text)
        if k == "lines":
            res[k] = len(lines) - 1
        if k == "longest_line":
            maxx = 0
            for line in lines:
                maxx = max(maxx, len(line))
            res[k] = maxx
        if k == "words":
            res[k] = len(words)
    return res
