def red(text: str) -> str:
    return f'\033[91m{text}\033[0m'


def green(text: str) -> str:
    return f'\033[92m{text}\033[0m'


def yellow(text: str) -> str:
    return f'\x1b[33m{text}\033[0m'