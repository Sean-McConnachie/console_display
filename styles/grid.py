from core.buffer import Buffer
from core.alignment import Alignment
from core.display_property import DisplayProperty

from styles.cell import Cell


class Grid(DisplayProperty):
    cells: list[list[Cell]]  # [col][row]

    __num_rows: int
    __num_cols: int

    __column_heights: list[int]
    __row_lengths: list[int]

    def __init__(
            self,
            cells: list[list[Cell]],
            display_home: tuple[int, int] = None,
            padding_style: Buffer = Buffer(),
            outer_padding: tuple[int, int, int, int] = None,
            in_rows: bool = False,
            auto_finalise: bool = True
    ):
        # Transform data if in wrong format
        if in_rows is True:
            cells = self.transform_data(cells=cells)
        temp = None
        # Validate that rows and columns are all equal length
        self.__num_rows = len(cells[0])
        self.__num_cols = len(cells)

        for col in cells:
            if len(col) != self.__num_rows:
                raise ValueError("All columns must be the same length")
        for rowi in range(self.__num_cols):
            row = [col[rowi] for col in cells]
            if len(row) != self.__num_cols:
                raise ValueError("All rows must be the same length")

        self.cells = cells
        if auto_finalise is True:
            self.__finalise_all_cells()

        # Calculate the size of the grid
        length, height = self.__calculate_grid_size()

        super().__init__(
            display_home=display_home,
            outer_padding=outer_padding,
            content_length=length,
            content_height=height,
            padding_buffer=padding_style
        )

        if display_home is not None:
            self.set_cell_homes()

    @staticmethod
    def transform_data(cells: list[list[Cell]]):
        temp = cells
        cells = [[None for _ in range(len(temp))] for _ in range(len(temp[0]))]
        for rowi in range(len(temp)):
            row = temp[rowi]
            for coli in range(len(row)):
                c = row[coli]
                cells[coli][rowi] = c
        return cells

    def update_grid_size(self):
        length, height = self.__calculate_grid_size()
        self.content_length = length
        self.content_height = height
        self.set_cell_homes()

    def set_cell_homes(self):
        # Set the homes of all cells
        vert_offset = 0
        hori_offset = 0
        for col_i in range(len(self.cells)):
            col = self.cells[col_i]
            for row_i in range(len(col)):
                self.cells[col_i][row_i].display_home = (
                    self.display_home[0] + self.outer_padding[3] + hori_offset,
                    self.display_home[1] + self.outer_padding[0] + vert_offset
                )
                vert_offset += self.__column_heights[row_i]
            vert_offset = 0
            hori_offset += self.__row_lengths[col_i]

    def __calculate_grid_size(self) -> tuple[int, int]:  # TODO: Check output is correct
        self.__column_heights = [0 for _ in range(self.__num_rows)]
        self.__row_lengths = [0 for _ in range(self.__num_cols)]
        for col_i in range(len(self.cells)):
            col = self.cells[col_i]
            for row_i in range(len(col)):
                cell = col[row_i]
                if cell.total_height > self.__column_heights[row_i]:
                    self.__column_heights[row_i] = cell.total_height
                if cell.total_length > self.__row_lengths[col_i]:
                    self.__row_lengths[col_i] += cell.total_length
        return sum(self.__row_lengths), sum(self.__column_heights)

    def __finalise_all_cells(self):
        for col in self.cells:
            for cell in col:
                if cell.finalise is False:
                    cell.finalise = True

    @property
    def alignment(self) -> Alignment:
        return self.__alignment

    @alignment.setter
    def alignment(self, val: Alignment):
        self.__alignment = val

    def write(self):
        for col_i in range(len(self.cells)):
            col = self.cells[col_i]
            for row_i in range(len(col)):
                # print(col_i, row_i)
                #cell = col[row_i]
                #print(cell, col_i, row_i)
                self.cells[col_i][row_i].write()
