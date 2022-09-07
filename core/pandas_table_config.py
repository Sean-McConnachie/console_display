import pandas as pd

from core.table_config import ConsoleDisplayConf
from core.buffer import Buffer
from styles.cell import Cell


class PandasConf:
    table_name: Cell

    display_home: tuple[int, int]

    dataframe: pd.DataFrame
    use_index: bool
    use_columns: bool

    column_style: Buffer
    index_style: Buffer
    data_style: Buffer
    outer_padding_style: Buffer

    outer_padding: tuple[int, int, int, int]
    inner_borders: list[Cell | None]  # horizontal, vertical, corner
    outer_borders: list[Cell | None]  # top, right, bottom, left, corner

    def __init__(
            self,
            dataframe: pd.DataFrame,
            table_name: Cell = Cell(text=[""]),
            use_index: bool = True,
            use_columns: bool = True,
            display_home: tuple[int, int] = (0, 0),

            column_style: Buffer = Buffer(),
            index_style: Buffer = Buffer(),
            data_style: Buffer = Buffer(),

            outer_padding_style: Buffer = Buffer(),
            outer_padding: tuple[int, int, int, int] = (0, 0, 0, 0),

            use_default_outer_border_style: bool = True,
            use_default_inner_border_style: bool = True,
            inner_borders: list[Cell | None] = None,  # horizontal, vertical, corner
            outer_borders: list[Cell | None] = None,  # top, right, bottom, left, corner
    ):
        self.table_name = table_name
        self.display_home = display_home

        self.dataframe = dataframe
        self.use_index = use_index
        self.use_columns = use_columns

        self.column_style = column_style
        self.index_style = index_style
        self.data_style = data_style

        self.outer_padding_style = outer_padding_style
        self.outer_padding = outer_padding

        if use_default_outer_border_style:
            outer_borders = [
                Cell(text=["═"], auto_update=False),
                Cell(text=["║"], auto_update=False),
                Cell(text=["═"], auto_update=False),
                Cell(text=["║"], auto_update=False),
                Cell(text=["╬"], auto_update=False),
            ]
        self.outer_borders = outer_borders

        if use_default_inner_border_style:
            inner_borders = [
                Cell(text=["━"], auto_update=False),
                Cell(text=["┃"], auto_update=False),
                Cell(text=["╂"], auto_update=False),
            ]
        self.inner_borders = inner_borders


    def convert_pandas_conf_to_console_conf(
            self,
            conf: "PandasConf" = None,
    ) -> ConsoleDisplayConf:
        if conf is None:
            conf = self

        if conf.use_index is True:
            index = []
            for ind in list(conf.dataframe.index.values):
                index.append(Cell(text=[str(ind)], style=conf.index_style))
        else:
            index = None

        if conf.use_columns is True:
            columns = []
            for col in list(conf.dataframe.columns.values):
                columns.append(Cell(text=[str(col)], style=conf.column_style))
        else:
            columns = None

        data = []
        for col in conf.dataframe.columns:
            column_cells = []
            for row in list(conf.dataframe[col].values):
                column_cells.append(Cell(text=[str(row)], style=conf.data_style))
            data.append(column_cells)

        conf = ConsoleDisplayConf(
            table_name=conf.table_name,
            display_home=conf.display_home,
            index=index,
            columns=columns,
            data=data,
            in_rows=False,
            outer_padding_style=conf.outer_padding_style,
            outer_padding=conf.outer_padding,
            outer_borders=conf.outer_borders,
            inner_borders=conf.inner_borders
        )
        return conf
