from core.buffer import Buffer


class DisplayProperty:
    __content_home: tuple[int, int]  # relative
    __corners: tuple[tuple[str, str]]

    __total_length: int
    __total_height: int

    __has_been_finalised: bool

    # User defined properties
    __display_home: tuple[int, int]
    __outer_padding: tuple[int, int, int, int]  # top, right, bottom, left
    __content_length: int
    __content_height: int
    __padding_buffer: Buffer

    def __init__(
            self,
            display_home: tuple[int, int] = None,
            outer_padding: tuple[int, int, int, int] = None,
            content_length: int = None,
            content_height: int = None,
            padding_buffer: Buffer = None
    ):
        self.__display_home = display_home
        if outer_padding is None:
            self.__outer_padding = (0, 0, 0, 0)
        else:
            self.__outer_padding = outer_padding

        self.__content_length = content_length
        self.__content_height = content_height
        self.__padding_buffer = padding_buffer
        self.__has_been_finalised = False

    def get_write_position(self):
        if self.__display_home is None:
            raise ValueError("Display home has not been set.")
        return self.__display_home[0] + self.__content_home[0], self.__display_home[1] + self.__content_home[1]


    @property
    def padding_buffer(self) -> Buffer:
        return self.__padding_buffer

    @property
    def finalise(self) -> bool:
        return self.__has_been_finalised

    @finalise.setter
    def finalise(self, val: bool):
        if val is not True:
            raise ValueError("Finalise must be set to True.")

        if self.__has_been_finalised:
            raise RuntimeError("DisplayProperty has already been finalised.")

        if self.content_length is None or self.content_height is None or self.__outer_padding is None:
            raise ValueError("Content length or height or padding is not set.")

        has_padding = False
        for i in self.__outer_padding:
            if i > 0:
                has_padding = True
                break
        if has_padding and self.__padding_buffer is None:
            raise ValueError("Padding buffer is not set.")

        self.__total_length = self.content_length + self.__outer_padding[1] + self.__outer_padding[3]
        self.__total_height = self.content_height + self.__outer_padding[0] + self.__outer_padding[2]
        self.__content_home = (self.__outer_padding[3], self.__outer_padding[0])

        self.__has_been_finalised = True

    @property
    def display_home(self):
        return self.__display_home

    @display_home.setter
    def display_home(self, display_home: tuple[int, int]):
        self.__display_home = display_home

    @property
    def content_home(self):
        return self.__content_home

    @content_home.setter
    def content_home(self, content_home: tuple[int, int]):
        raise AttributeError("Cannot set content home. It is calculated automatically.")

    @property
    def corners(self):
        return self.__corners

    @corners.setter
    def corners(self, corners: tuple[tuple[str, str]]):
        raise AttributeError("Cannot set corners. It is calculated automatically.")

    @property
    def outer_padding(self):
        return self.__outer_padding

    @outer_padding.setter
    def outer_padding(self, outer_padding: tuple[int, int, int, int]):
        if self.__has_been_finalised:
            raise ValueError("Cannot change outer padding after finalising!")
        self.__outer_padding = outer_padding

    @property
    def total_length(self):
        return self.__total_length

    @total_length.setter
    def total_length(self, total_length: int):
        if self.__has_been_finalised:
            raise ValueError("Cannot change max length after finalising!")
        self.__total_length = total_length

    @property
    def total_height(self):
        return self.__total_height

    @total_height.setter
    def total_height(self, total_height: int):
        if self.__has_been_finalised:
            raise ValueError("Cannot change max height after finalising!")
        self.__total_height = total_height

    @total_length.setter
    def total_length(self, total_length: int):
        if self.__has_been_finalised:
            raise ValueError("Cannot change max length after finalising!")
        self.__total_length = total_length

    @property
    def content_length(self):
        return self.__content_length

    @content_length.setter
    def content_length(self, content_length: int):
        if self.__has_been_finalised:
            raise ValueError("Cannot change max height after finalising!")
        self.__content_length = content_length

    @property
    def content_height(self):
        return self.__content_height

    @content_height.setter
    def content_height(self, content_height: int):
        if self.__has_been_finalised:
            raise ValueError("Cannot change max height after finalising!")
        self.__content_height = content_height

    def write_padding(self):
        if self.__display_home is None:
            raise ValueError("Display home has not been set.")

        self.__padding_buffer.write_config()

        whitespace = " " * self.__total_length
        for l in range(self.__outer_padding[0]):  # Top
            self.__padding_buffer.write_at(
                column=self.__display_home[0],
                line=self.display_home[1] + l,
                text=whitespace
            )

        for l in range(self.__outer_padding[2]):
            self.__padding_buffer.write_at(
                column=self.__display_home[0],
                line=self.display_home[1] + l + self.__content_height + 1,
                text=whitespace
            )

        l_whitespace = " " * self.__outer_padding[3]
        r_whitespace = " " * self.__outer_padding[1]
        for l in range(self.__content_height):
            self.__padding_buffer.write_at(  # Left
                column=self.display_home[0],
                line=self.display_home[1] + l + self.__outer_padding[0],
                text=l_whitespace
            )
            self.__padding_buffer.write_at(  # Right
                column=self.display_home[0] + self.__content_length + self.__outer_padding[3],
                line=self.display_home[1] + l + self.__outer_padding[0],
                text=r_whitespace
            )

    def write(self):
        ...
