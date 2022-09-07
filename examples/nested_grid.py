import time

from .useful import clear_screen, get_grid_cells_in_columns, get_grid_cells_in_rows
from styles.grid import Grid


def nested_grid():
    # To create a nested grid:
    #     1) Create a parent and child grid
    #     2) Finalise the child grid
    #     3) Set the parent grid's cells to the child grid
    #     4) Call .update_grid_size() on the parent
    #     5) Finalise the parent grid
    #     6) Call .set_cell_homes() on the child
    #     7) Call .write() on the parent

    clear_screen()

    parent_grid = Grid(
        cells=get_grid_cells_in_columns(),
        display_home=(3, 2),
        in_rows=False,
        auto_finalise=True
    )

    nested_grid = Grid(
        cells=get_grid_cells_in_rows(),
        #outer_padding=(0, 4, 4, 0),
        display_home=None,
        in_rows=True
    )

    nested_grid.finalise = True
    parent_grid.cells[0][0] = nested_grid
    parent_grid.update_grid_size()
    parent_grid.finalise = True
    nested_grid.set_cell_homes()
    parent_grid.write()

    for i in range(1000):
        for r in range(3):
            for c in range(2):
                time.sleep(1)
                parent_grid.cells[0][0].cells[c][r].text = [str(i)]

    print("\n" * 10)
