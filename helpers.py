import secrets


def randint(start: int, stop: int, step: int = 1) -> int:
    return (secrets.randbelow(int((stop - start) / step)) * step) + start
