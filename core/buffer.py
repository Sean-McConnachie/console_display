"""
The buffer class is used to write different styles of text to the screen in different places.

The buffer should be used to write text to the screen in different places.

The config needs to be set explicitly by using .write_config().

Example usage:
buf = Buffer(use_validator=True)
# Clear entire screen command
buf.set_special(ANSISequences.Erase.SCREEN)
# Set foreground color
buf.set_foreground(156)
buf.set_graphic(ANSISequences.Graphics.BOLD)
buf.set_graphic(ANSISequences.Graphics.ITALIC)

# Would print normal text
buf.write_text("hello")
buf.write_config()
# Would now print styled text
buf.write_text("hello")

# Now calls the clear command
buf.write_special()
"""


import sys

from core.sequences import ANSISequences


class Buffer:
    __specials: list[str]

    __prefix: str
    __graphics: list[str]
    __foreground: str | None  # 0 - 255
    __background: str | None  # 0 - 255
    __common_privates: list[str]

    __use_validator: bool

    def __init__(
            self,
            prefix: str = ANSISequences.Prefixes.HEX,
            use_validator: bool = False
    ):
        self.__use_validator = use_validator

        self.__prefix = self.__validate(prefix, ANSISequences.Prefixes)

        self.__specials = []
        self.__graphics = []
        self.__common_privates = []
        self.__foreground = None
        self.__background = None

    def write_reset(self):
        self.__write(ANSISequences.Graphics.RESET)

    def write_config(self):
        self.write_reset()

        for graphic in self.__graphics:
            self.__write(graphic)

        for common_private in self.__common_privates:
            self.__write(common_private)

        if self.__foreground is not None:
            self.__write(ANSISequences.Color.COLOR_FOREGROUND.format(color=self.__foreground))

        if self.__background is not None:
            self.__write(ANSISequences.Color.COLOR_BACKGROUND.format(color=self.__background))

    def write_special(self):
        for special in self.__specials:
            sys.stdout.write(self.__prefix)
            sys.stdout.write(special)

    @staticmethod
    def write_text(text: str):
        sys.stdout.write(text)
        sys.stdout.flush()

    def write_at(self, column: int, line: int, text: str):
        self.__write(ANSISequences.Cursor.TO.format(line=line, column=column))
        sys.stdout.flush()
        sys.stdout.write(text)
        sys.stdout.flush()

    # Specials
    @property
    def specials(self) -> list[str]:
        return self.__graphics

    @specials.setter
    def specials(self, specials: list[str] | str | None):
        if specials is None:
            self.__specials = []
            return
        if isinstance(specials, str):
            self.__specials.append(self.__validate(specials, ANSISequences.Graphics))
            return
        for special in specials:
            self.__specials.append(self.__validate(special, ANSISequences.Graphics))

    # Graphics
    @property
    def graphics(self) -> list[str]:
        return self.__graphics

    @graphics.setter
    def graphics(self, graphics: list[str] | str | None):
        if graphics is None:
            self.__graphics = []
            return
        if isinstance(graphics, str):
            self.__graphics.append(self.__validate(graphics, ANSISequences.Graphics))
            return
        for graphic in graphics:
            self.__graphics.append(self.__validate(graphic, ANSISequences.Graphics))

    # Common Private
    @property
    def common_privates(self) -> list[str]:
        return self.__common_privates

    @common_privates.setter
    def common_privates(self, common_privates: list[str] | str | None):
        if common_privates is None:
            self.__common_privates = []
            return
        if isinstance(common_privates, str):
            self.__common_privates.append(self.__validate(common_privates, ANSISequences.Graphics))
            return
        for common_private in common_privates:
            self.__common_privates.append(self.__validate(common_private, ANSISequences.Graphics))

    # Colo(u)rs
    @property
    def foreground(self):
        return self.__foreground

    @foreground.setter
    def foreground(self, color: str | int | None):
        if color is not None:
            if int(color) not in range(0, 256):
                raise ValueError("Invalid foreground color: " + str(color))
        self.__foreground = color

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, color: str | int | None):
        if color is not None:
            if int(color) not in range(0, 256):
                raise ValueError("Invalid background color: " + str(color))
        self.__background = color

    # Private methods
    def __validate(self, value: str, class_type: type) -> str:
        if self.__use_validator:
            if value in vars(class_type).values():
                return value
            raise ValueError(f"Invalid value: {value}. Not found in {class_type.__name__}")
        return value

    def __write(self, val: str):
        sys.stdout.write(self.__prefix)
        sys.stdout.write(val)

    def __str__(self):
        return f"Buffer(foreground={self.__foreground}, background={self.__background})"
