import string


def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    res = ''
    for i in message:
        if i in lower:
            res += lower[(lower.index(i) + n) % len(lower)]
        elif i in upper:
            res += upper[(upper.index(i) + n) % len(upper)]
        else:
            res += i
    return res
