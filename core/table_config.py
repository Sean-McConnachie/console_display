from core.buffer import Buffer
from styles.cell import Cell


class ConsoleDisplayConf:
    display_home: tuple[int, int]

    table_name: Cell
    index: list[Cell]
    columns: list[Cell]
    data: list[list[Cell]]
    in_rows: bool

    outer_padding_style: Buffer
    outer_padding: tuple[int, int, int, int]
    inner_borders: list[Cell | None]  # horizontal, vertical, corner
    outer_borders: list[Cell | None]  # top, right, bottom, left, corner

    def __init__(
            self,
            table_name: Cell = Cell(text=[""]),
            display_home: tuple[int, int] = (0, 0),
            index: list[Cell] = None,
            columns: list[Cell] = None,
            data: list[list[Cell]] = None,
            in_rows: bool = False,
            outer_padding_style: Buffer = Buffer(),
            outer_padding: tuple[int, int, int, int] = (0, 0, 0, 0),
            outer_borders: list[Cell, Cell, Cell, Cell, Cell] = None,
            inner_borders: list[Cell, Cell, Cell, Cell, Cell] = None
    ):
        self.table_name = table_name
        self.display_home = display_home

        self.index = index
        self.columns = columns
        self.data = data
        self.in_rows = in_rows


        self.outer_padding_style = outer_padding_style
        self.outer_padding = outer_padding
        if outer_borders is None:
            self.outer_borders = [None, None, None, None, None]
        else:
            self.outer_borders = outer_borders
        if inner_borders is None:
            self.inner_borders = [None, None, None]
        else:
            self.inner_borders = inner_borders


class PandasConf:
    ...
