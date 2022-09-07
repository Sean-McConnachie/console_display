from core.buffer import Buffer
from core.sequences import ANSISequences
from core.table_config import ConsoleDisplayConf
from core.pandas_table_config import PandasConf
from core.alignment import Alignment
from styles.cell import Cell

import pandas as pd


def clear_screen():
    buf = Buffer()
    buf.specials = ANSISequences.Erase.SCREEN
    buf.specials = ANSISequences.CommonPrivate.CURSOR_INVISIBLE
    buf.write_special()


def create_random_buffer():
    import random
    buf = Buffer()
    buf.foreground = random.randint(0, 255)
    buf.background = random.randint(0, 255)
    buf.graphics = random.choice([ANSISequences.Graphics.BOLD, ANSISequences.Graphics.ITALIC])
    return buf


def reset_buffer():
    buf = Buffer()
    buf.write_reset()


def get_grid_cells_in_rows() -> list[list[Cell]]:
    cells = [
        [
            Cell(text=["n0, 0"]),
            Cell(text=["n1, 0"]),
        ],
        [
            Cell(text=["n0, 1"]),
            Cell(text=["n1, 1"]),
        ],
        [
            Cell(text=["n0, 2"]),
            Cell(text=["n1, 2"]),
        ]
    ]
    return cells


def get_grid_cells_in_columns() -> list[list[Cell]]:
    cells = [
        [
            Cell(text=["0, 0"]),
            Cell(text=["0, 1"]),
            Cell(text=["0, 2"]),
        ],
        [
            Cell(text=["1, 0"]),
            Cell(text=["1, 1"]),
            Cell(text=["1, 2"]),
        ],
    ]
    return cells


def create_table_conf():
    table_name = Cell(text=["Table name"])

    index = [
        Cell(text=["Ind 0"]),
        Cell(text=["Ind 1"]),
        Cell(text=["Ind 2"]),
    ]

    columns = [
        Cell(text=["Col 0"]),
        Cell(text=["Col 1"]),
    ]

    outer_borders = [
        Cell(text=["═"], auto_update=False),
        # None,
        Cell(text=["║"], auto_update=False),
        Cell(text=["═"], auto_update=False),
        Cell(text=["║"], auto_update=False),
        Cell(text=["╬"], auto_update=False),
    ]

    inner_borders = [
        Cell(text=["━"], auto_update=False),
        # None,
        Cell(text=["┃"], auto_update=False),
        Cell(text=["╂"], auto_update=False),
    ]

    data = [
        [
            Cell(text=["0, 0"], alignment=Alignment.CENTER),
            Cell(text=["0, 1"], alignment=Alignment.CENTER),
            Cell(text=["0, 2"], alignment=Alignment.CENTER),
        ],
        [
            Cell(text=["1, 0"], alignment=Alignment.CENTER),
            Cell(text=["1, 1"], alignment=Alignment.CENTER),
            Cell(text=["1, 2"], alignment=Alignment.CENTER),
        ],
    ]

    conf = ConsoleDisplayConf(
        table_name=table_name,
        display_home=(1, 1),
        index=index,
        columns=columns,
        data=data,
        in_rows=False,
        outer_borders=outer_borders,
        inner_borders=inner_borders,
    )

    return conf


def create_pandas_table_conf():
    data_buf = Buffer()
    data_buf.foreground = 69

    index_buf = Buffer()
    index_buf.graphics = ANSISequences.Graphics.BOLD
    index_buf.graphics = ANSISequences.Graphics.ITALIC
    index_buf.foreground = 141

    column_buf = Buffer()
    column_buf.graphics = ANSISequences.Graphics.BOLD
    column_buf.foreground = 160

    df = pd.read_csv("examples/PizzaDeliveryTimes.csv")
    conf = PandasConf(
        display_home=(1, 1),
        dataframe=df,
        data_style=data_buf,
        index_style=index_buf,
        column_style=column_buf,
    )

    return conf
