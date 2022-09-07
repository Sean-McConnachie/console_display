import time

from core.buffer import Buffer
from core.sequences import ANSISequences
from styles.cell import Cell
from styles.grid import Grid
from examples.useful import *
from core.table_config import ConsoleDisplayConf
from styles.table import Table
from core.alignment import Alignment


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
        Cell(text=["║"], auto_update=False),
        Cell(text=["═"], auto_update=False),
        Cell(text=["║"], auto_update=False),
        Cell(text=["╬"], auto_update=False),
    ]

    inner_borders = [
        Cell(text=["╍"], auto_update=False),
        Cell(text=["╏"], auto_update=False),
        Cell(text=["╀"], auto_update=False),
    ]

    data = [
        [
            Cell(text=["0, 0"], outer_padding=(1, 1, 1, 1), alignment=Alignment.CENTER),
            Cell(text=["0, 1"], outer_padding=(1, 1, 1, 1), alignment=Alignment.CENTER),
            Cell(text=["0, 2"], outer_padding=(1, 1, 1, 1), alignment=Alignment.CENTER),
        ],
        [
            Cell(text=["1, 0"], outer_padding=(1, 1, 1, 1), alignment=Alignment.CENTER),
            Cell(text=["1, 1"], outer_padding=(1, 1, 1, 1), alignment=Alignment.CENTER),
            Cell(text=["1, 2"], outer_padding=(1, 1, 1, 1), alignment=Alignment.CENTER),
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


def basic_table():
    clear_screen()

    conf = create_table_conf()

    table = Table(conf)

    # print(table.cells[0][0])
    table.write()
    table.update_cell(0, 0, ["cell"])
    # table.update_index(0, ["indx"])

    print("\n" * 10)


def nested_table():
    clear_screen()

    parent_conf = create_table_conf()
    nested_conf = create_table_conf()

    nested_t = Table(nested_conf)
    parent_conf.data[0][1] = nested_t
    parent_table = Table(parent_conf)

    # print(table.cells[0][0])
    parent_table.write()

    print("\n" * 10)



if __name__ == '__main__':
    basic_table()
    # nested_table()
