def get_fizz_buzz(n: int) -> list[int | str]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    result: tp.List[tp.Union[int, str]] = []
    for val in range(1, n + 1):
        if val % 15 == 0:
            result.append("FizzBuzz")
        elif val % 5 == 0:
            result.append("Buzz")
        elif val % 3 == 0:
            result.append("Fizz")
        else:
            result.append(val)
    return result
