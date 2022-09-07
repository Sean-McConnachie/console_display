from core.buffer import Buffer
from core.sequences import ANSISequences
from styles.cell import Cell


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
