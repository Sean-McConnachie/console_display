from core.buffer import Buffer
from core.alignment import Alignment
from core.display_property import DisplayProperty



class Cell(DisplayProperty):
    style: Buffer

    __text: list[str]
    __auto_update: bool
    __alignment: Alignment

    def __init__(
            self,
            text: list[str],
            display_home: tuple[int, int] = None,
            style: Buffer = Buffer(),
            padding_style: Buffer = Buffer(),
            max_length: int = None,
            max_height: int = None,
            outer_padding: tuple[int, int, int, int] = None,
            alignment: Alignment = Alignment.LEFT,
            auto_update: bool = True
    ):
        if max_length is None:
            max_length = len(max(text, key=len))
        if max_height is None:
            max_height = len(text)

        self.__text = text
        self.style = style
        self.__alignment = alignment
        self.__auto_update = auto_update

        super().__init__(
            display_home=display_home,
            outer_padding=outer_padding,
            content_length=max_length,
            content_height=max_height,
            padding_buffer=padding_style
        )

    @property
    def alignment(self) -> Alignment:
        return self.__alignment

    @alignment.setter
    def alignment(self, val: Alignment):
        self.__alignment = val

    @property
    def text(self) -> list[str]:
        return self.__text

    @text.setter
    def text(self, text: list[str]):
        if len(max(text, key=len)) > self.content_length or len(text) > self.content_height:
            raise ValueError(f"Text is too long for cell. Text: {text} Max length: {self.content_length}")
        self.__text = text
        if self.__auto_update:
            self.write()

    def write(self):
        pos = self.get_write_position()
        self.style.write_config()

        for i in range(len(self.__text)):
            line = self.__text[i]
            match self.__alignment:
                case Alignment.LEFT:
                    line = line.ljust(self.content_length)
                case Alignment.RIGHT:
                    line = line.rjust(self.content_length)
                case Alignment.CENTER:
                    line = line.center(self.content_length)
            self.style.write_at(column=pos[0], line=pos[1] + i, text=line)

    def __str__(self):
        temp = f"Cell(text={self.__text}, display_home={self.display_home}, content_length={self.content_length}, content_height={self.content_height}"
        temp += ")"
        return temp