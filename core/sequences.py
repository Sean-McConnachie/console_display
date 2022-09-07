"""
This file contains most ANSI escape sequences.

It is used to make usage cases more readable.

Generally speaking, these escape sequences should not be used without the buffer.
"""


class ANSISequences:
    # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

    class Prefixes:
        # Prefixes
        CTRL: str = "^["
        HEX: str = "\x1b["
        UNICODE: str = "\u001b"
        OCTAL: str = "\033"

    class Basic:
        BELL: str = "\a"
        BACKSPACE: str = "\b"
        HORIZONTAL_TAB: str = "\t"
        NEWLINE: str = "\n"
        VERTICAL_TAB: str = "\v"
        FORM_FEED: str = "\f"
        CARRIAGE_RETURN: str = "\r"

    class Cursor:
        HOME: str = "H"
        TO: str = "{line};{column}f"
        NUM_UP: str = "{num}A"
        NUM_DOWN: str = "{num}B"
        NUM_RIGHT: str = "{num}C"
        NUM_LEFT: str = "{num}D"

    class Erase:
        SCREEN: str = "2J"
        LINE: str = "2K"
        LINE_TO_END: str = "0K"
        LINE_FROM_START: str = "1K"

    class Graphics:
        RESET: str = "0m"
        BOLD: str = "1m"
        DIM: str = "2m"
        ITALIC: str = "3m"
        UNDERLINE: str = "4m"
        BLINK: str = "5m"
        INVERSE: str = "7m"
        INVISIBLE: str = "8m"
        STRIKE: str = "9m"

    class Color:
        # https://user-images.githubusercontent.com/995050/47952855-ecb12480-df75-11e8-89d4-ac26c50e80b9.png
        COLOR = [i for i in range(256)]
        COLOR_FOREGROUND = "38;5;{color}m"
        COLOR_BACKGROUND = "48;5;{color}m"

    class CommonPrivate:
        CURSOR_INVISIBLE: str = "?25l"
        CURSOR_VISIBLE: str = "?25h"
        RESTORE: str = "?47l"
        SAVE: str = "?47h"
        EN_ALTERNATIVE_BUFFER: str = "?1049h"
        DIS_ALTERNATIVE_BUFFER: str = "?1049l"
