def red(text: str) -> str:
    return f'\033[91m{text}\033[0m'


def green(text: str) -> str:
    return f'\033[92m{text}\033[0m'


def yellow(text: str) -> str:
    return f'\x1b[33m{text}\033[0m'


def blue_back(text: str) -> str:
    return f'\x1b[44m{text}\033[0m'


def bold(text: str) -> str:
    return f'\x1b[1m{text}\033[0m'


def emphasize(text: str) -> str:
    return bold(blue_back(green(text)))

    # print("\x1b[1mBold Text\x1b[0m")
    # print("\x1b[3mItalic Text\x1b[0m")
    # print("\x1b[4mUnderlined Text\x1b[0m")
    # print("\x1b[9mStrikethrough Text\x1b[0m")

    # print("\x1b[31mRed Text\x1b[0m")
    # print("\x1b[32mGreen Text\x1b[0m")
    # print("\x1b[33mYellow Text\x1b[0m")
    # print("\x1b[34mBlue Text\x1b[0m")
    # print("\x1b[35mMagenta Text\x1b[0m")
    # print("\x1b[36mCyan Text\x1b[0m")
    # print("\x1b[37mWhite Text\x1b[0m")

    # print("\x1b[41mRed Background\x1b[0m")
    # print("\x1b[42mGreen Background\x1b[0m")
    # print("\x1b[43mYellow Background\x1b[0m")
    # print("\x1b[44mBlue Background\x1b[0m")
    # print("\x1b[45mMagenta Background\x1b[0m")
    # print("\x1b[46mCyan Background\x1b[0m")
    # print("\x1b[47mWhite Background\x1b[0m")
