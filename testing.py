import time

from core.buffer import Buffer
from core.sequences import ANSISequences
from styles.cell import Cell
from styles.grid import Grid
from examples.useful import *
from core.table_config import ConsoleDisplayConf
from styles.table import Table
from core.alignment import Alignment
import pandas as pd
from core.pandas_table_config import PandasConf


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


def basic_table_normal_conf():
    clear_screen()

    conf = create_table_conf()

    table = Table(conf)

    # print(table.cells[0][0])
    table.write()
    table.update_cell(0, 2, ["cell"])
    table.update_index(2, ["indx"])
    # table.update_table_name(["tabs"])
    # table.update_column(1, ["cll"])

    print("\n" * 20)


def nested_table_normal_conf():
    clear_screen()

    parent_conf = create_table_conf()
    nested_conf = create_table_conf()

    nested_t = Table(nested_conf)
    parent_conf.data[0][1] = nested_t
    parent_table = Table(parent_conf)
    # parent_table.update_cell_home(0, 1)

    parent_table.update_nested_table_cell([(0, 1), (0, 2)], ["cell"])
    nested_t.update_cell(0, 1, ["df"])

    # print(table.cells[0][0])

    parent_table.write()

    print("\n" * 10)


def basic_table_pandas_conf():
    clear_screen()

    conf = create_pandas_table_conf()
    conf = conf.convert_pandas_conf_to_console_conf()
    table = Table(conf)

    table.write()
    # table.update_cell(0, 2, ["cell"])
    # table.update_index(2, ["indx"])
    # table.update_table_name(["tabs"])
    # table.update_column(1, ["cll"])

    print("\n" * 20)


def nested_table_pandas_conf():
    clear_screen()

    parent_conf = create_pandas_table_conf()
    parent_conf = parent_conf.convert_pandas_conf_to_console_conf()
    nested_conf = create_pandas_table_conf()
    nested_conf = nested_conf.convert_pandas_conf_to_console_conf()

    nested_table = Table(nested_conf)
    # parent_conf.index[0] = nested_table
    parent_conf.data[0][0] = nested_table
    parent_table = Table(parent_conf)

    parent_table.write()


    print("\n" * 20)


if __name__ == '__main__':
    # basic_table_normal_conf()
    # nested_table_normal_conf()
    # basic_table_pandas_conf()
    nested_table_pandas_conf()
