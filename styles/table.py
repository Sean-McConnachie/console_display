"""
A Table inherits from Grid.

The grid is considered relatively low level (in the sense that there is no easy way to add borders, labels, etc...)

Therefore, the table will simply store maps to the correct rows and columns for the cells, and then add the borders,
labels, etc...
"""

from core.buffer import Buffer
from core.alignment import Alignment
from core.display_property import DisplayProperty

from styles.cell import Cell
from styles.grid import Grid

from core.table_config import ConsoleDisplayConf
from core.pandas_table_config import PandasConf


class Table(Grid):
    config: ConsoleDisplayConf | PandasConf

    __index_loc: list[tuple[int, int]]
    __columns_loc: list[tuple[int, int]]
    __data_loc: list[list[tuple[int, int]]]

    __outer_borders: list[list[list[tuple[int, int]]]]  # top, right, bottom, left, corner
    __inner_borders: list[list[list[tuple[int, int]]]]  # top, right, bottom, left, corner

    def __init__(
            self,
            config: ConsoleDisplayConf | PandasConf,
    ):
        if isinstance(config, PandasConf):
            raise ValueError("Please convert your PandasConf to a ConsoleDisplayConf before passing it to Table.\n\nTo do this use `your_config = your_config.convert_pandas_conf_to_console_conf()`")
        else:
            self.config = config

        if self.config.in_rows is True:
            self.config.data = Grid.transform_data(cells=self.config.data)

        all_cells = self.__generate_cells()

        #self.__print_all_cells(cells=self.config.data)

        super().__init__(
            display_home=self.config.display_home,
            cells=all_cells,
            in_rows=self.config.in_rows,
            auto_finalise=True,
            outer_padding=self.config.outer_padding,
            padding_style=self.config.outer_padding_style
        )

        for c, r in self.__grid_table_to_update_home:
            self.update_cell_home(c=c, r=r)

    @staticmethod
    def get_row(row: int, cells: list[list[Cell]]):
        return [col[row] for col in cells]

    @staticmethod
    def col_max_length(col: list[Cell]) -> int:
        return max([cell.total_length for cell in col])

    @staticmethod
    def row_max_height(row: list[Cell]) -> int:
        return max([cell.total_height for cell in row])

    def __print_all_cells(self, cells: list[list[Cell]]):

        for row in range(len(cells[0])):
            r = self.get_row(row=row, cells=cells)
            for cell in r:
                if cell is None:
                    print("[None]", end=" ")
                else:
                    print(cell.text, end="")
            print("")

    @staticmethod
    def __calculate_max_heights_lengths(cells: list[list[Cell]]) -> tuple[list[int], list[int], int, int]:
        num_rows = len(cells[0])
        num_cols = len(cells)
        column_heights = [0 for _ in range(num_rows)]
        row_lengths = [0 for _ in range(num_cols)]
        for col_i in range(len(cells)):
            col = cells[col_i]
            for row_i in range(len(col)):
                cell = col[row_i]
                if cell.total_height > column_heights[row_i]:
                    column_heights[row_i] = cell.total_height
                if cell.total_length > row_lengths[col_i]:
                    row_lengths[col_i] += cell.total_length
        return row_lengths, column_heights, sum(row_lengths), sum(column_heights)

    def __generate_cells(self) -> list[list[Cell]]:
        cells = self.config.data

        self.__grid_table_to_update_home = []
        self.__table_name_loc = None
        self.__index_loc = []
        self.__columns_loc = []
        self.__data_loc = [[None for _ in range(len(cells[0]))] for _ in range(len(cells))]

        # Add index and columns to cells
        data_offset = (0, 0)
        if self.config.index is not None and self.config.columns is not None:
            side_column = self.config.index
            side_column.insert(0, self.config.table_name)
            for i in range(len(self.config.columns)):
                cells[i].insert(0, self.config.columns[i])
            cells.insert(0, side_column)
            data_offset = (-1, -1)
        elif self.config.index is None and self.config.columns is not None:
            for i in range(len(self.config.columns)):
                cells[i].insert(0, self.config.columns[i])
            data_offset = (0, -1)
        elif self.config.columns is None and self.config.index is not None:
            cells.insert(0, self.config.index)
            data_offset = (-1, 0)

        # Finalise all cells
        for col_i in range(len(cells)):
            for row_i in range(len(cells[col_i])):
                if cells[col_i][row_i].finalise is False:
                    cells[col_i][row_i].finalise = True

        # Get max lengths and heights
        row_lengths, column_heights, total_length, total_height = self.__calculate_max_heights_lengths(cells=cells)

        # Move from top left to bottom right
        # Column first, then row
        # Have a current offset list[int, int] (basically a vector)

        # cells.insert(len(cells), [None for _ in range(len(cells[0]))])
        for c in range(len(cells) + 1):
            # Vertical rules
            cells.insert((c * 2), [None for _ in range(len(cells[c]))])

        for c in range(len(cells)):
            # Horizontal rules
            for r in range(len(cells[c])):
                cells[c].insert((r * 2), None)
            cells[c].insert(len(cells[c]), None)

        for c in range(len(cells)):
            for r in range(len(cells[c])):
                if isinstance(cells[c][r], Table) or isinstance(cells[c][r], Grid):
                    self.__grid_table_to_update_home.append((c, r))

                col = (c - 1) // 2
                row = (r - 1) // 2

                # Corners
                if c % 2 == 0 and r % 2 == 0:
                    if c == 0 or c == len(cells) - 1 or r == 0 or r == len(cells[c]) - 1:
                        # outer corner
                        temp = self.multiply_cell_height(cell=self.config.outer_borders[4], height=1)
                        cells[c][r] = temp
                    else:
                        # inner corner
                        temp = self.multiply_cell_height(cell=self.config.inner_borders[2], height=1)
                        cells[c][r] = temp
                # Vertical Borders
                elif c % 2 == 0 and r % 2 == 1:
                    if c == 0:
                        # outer border left
                        temp = self.multiply_cell_height(cell=self.config.outer_borders[3], height=column_heights[row])
                        cells[c][r] = temp
                    elif c == len(cells) - 1:
                        # outer border right
                        temp = self.multiply_cell_height(cell=self.config.outer_borders[1], height=column_heights[row])
                        cells[c][r] = temp
                    else:
                        # inner border
                        temp = self.multiply_cell_height(cell=self.config.inner_borders[1], height=column_heights[row])
                        cells[c][r] = temp
                # Horizontal Borders
                elif c % 2 == 1 and r % 2 == 0:
                    if r == 0:
                        # outer border top
                        temp = self.multiply_cell_width(cell=self.config.outer_borders[0], width=row_lengths[col])
                        cells[c][r] = temp
                    elif r == len(cells[c]) - 1:
                        # outer border bottom
                        temp = self.multiply_cell_width(cell=self.config.outer_borders[2], width=row_lengths[col])
                        cells[c][r] = temp
                    else:
                        # inner border
                        temp = self.multiply_cell_width(cell=self.config.inner_borders[0], width=row_lengths[col])
                        cells[c][r] = temp
                elif c < len(cells) and r < len(cells[c]):
                    # Data or index or table name or column
                    if self.config.index is not None and self.config.columns is not None and col == 0 and row == 0:  # Both col and ind set
                        self.__table_name_loc = c, r
                    elif self.config.index is not None and self.config.columns is not None and col == 0:  # Both col and ind set
                        self.__index_loc.append((c, r))
                    elif self.config.index is not None and self.config.columns is not None and row == 0:  # Both col and ind set
                        self.__columns_loc.append((c, r))
                    elif self.config.columns is not None and self.config.index is None and row == 0:  # Only col set
                        self.__columns_loc.append((c, r))
                    elif self.config.columns is None and self.config.index is not None and col == 0:  # Only ind set
                        self.__index_loc.append((c, r))
                    else:
                        # print(col + data_offset[0], row + data_offset[1])
                        self.__data_loc[col + data_offset[0]][row + data_offset[1]] = c, r


        # print(f"Table name loc: \t {self.__table_name_loc}")
        # print(f"Index loc: \t\t {self.__index_loc}")
        # print(f"Columns loc: \t\t {self.__columns_loc}")
        # print(f"Data loc: \t\t {self.__data_loc}")
        # print()
        # print()
        # exit()
        return cells

    @staticmethod
    def multiply_cell_height(cell: Cell, height: int) -> Cell:
        if cell is None:
            temp = [" " for _ in range(height)]
            temp = Cell(text=temp)
            temp.finalise = True
        else:
            temp = [cell.text[0] for _ in range(height)]
            temp = Cell(text=temp, style=cell.style, padding_style=cell.padding_buffer, outer_padding=cell.outer_padding, alignment=cell.alignment)
            temp.finalise = True
        return temp

    @staticmethod
    def multiply_cell_width(cell: Cell, width: int) -> Cell:
        if cell is None:
            temp = [" " * width]
            temp = Cell(text=temp)
            temp.finalise = True
        else:
            temp = [cell.text[0] * width]
            temp = Cell(text=temp, style=cell.style, padding_style=cell.padding_buffer, outer_padding=cell.outer_padding, alignment=cell.alignment)
            temp.finalise = True
        return temp

    def get_table_name_loc(self) -> tuple[int, int]:
        return self.__table_name_loc

    def get_index_loc(self) -> list[tuple[int, int]]:
        return self.__index_loc

    def get_columns_loc(self) -> list[tuple[int, int]]:
        return self.__columns_loc

    def get_data_loc(self) -> list[list[tuple[int, int]]]:
        return self.__data_loc

    def update_table_name(self, text: list[str]):
        if self.__table_name_loc is None:
            raise ValueError("This table does not have a table name. Please note you must have both an index and columns to have a table name.")
        self.cells[self.__table_name_loc[0]][self.__table_name_loc[1]].text = text

    def update_column(self, column: int, text: list[str]):
        if self.config.columns is None:
            raise ValueError("You have not set any columns for this table.")
        self.cells[self.__columns_loc[column][0]][self.__columns_loc[column][1]].text = text

    def update_index(self, row: int, text: list[str]):
        if self.config.index is None:
            raise ValueError("You have not set an index for this table.")
        self.cells[self.__index_loc[row][0]][self.__index_loc[row][1]].text = text

    def update_cell(self, column: int, row: int, text: list[str]):
        self.cells[self.__data_loc[column][row][0]][self.__data_loc[column][row][1]].text = text

    def update_nested_table_cell(
            self,
            nested_locs: list[tuple[int, int]],
            text: list[str]
    ):
        """
        Updates a cell in a nested table.

        nested_locs is a list of (col, row), where each item goes one level deeper into another nested table. The final
        item nested_locs is the location of the cell to be updated.

        Please note that instead of using this it is also possible to simply store the original instance of the nested
        table that was passed into the config and call .update_cell(...).

        :param nested_locs:
        :param text:
        :return:
        """
        if len(nested_locs) == 1:
            self.update_cell(column=nested_locs[0][0], row=nested_locs[0][1], text=text)
        else:
            self.cells[self.__data_loc[nested_locs[0][0]][nested_locs[0][1]][0]][self.__data_loc[nested_locs[0][0]][nested_locs[0][1]][1]].update_nested_table_cell(nested_locs=nested_locs[1:], text=text)

    def update_cell_home(self, c: int, r: int):
        self.cells[c][r].set_cell_homes()
