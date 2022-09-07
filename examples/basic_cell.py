import time

from styles.cell import Cell
from .useful import clear_screen, create_random_buffer, reset_buffer


def basic_cell_test():
    clear_screen()

    s1 = create_random_buffer()
    s2 = create_random_buffer()

    c = Cell(
        text=["hello", "line22222"],
        display_home=(3, 2),
        style=s1,
        padding_style=s2,
        outer_padding=(1, 2, 3, 4)
    )
    c.finalise = True
    c.write_padding()
    c.write()

    time.sleep(1)
    c.text = ["hello", "line2"]

    reset_buffer()

    print("\n" * 10)
    #print(c.display_home)
    print("\n" * 10)
