def get_middle_value(a: int, b: int, c: int) -> int:
    """
    Takes three values and returns middle value.
    """
    if a <= b and b <= c or c <= b and b <= a:
        return b
    elif b <= a and a <= c or c <= a and a <= b:
        return a
    else:
        return c
