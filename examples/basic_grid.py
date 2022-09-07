from .useful import clear_screen, get_grid_cells_in_columns


def basic_grid():
    clear_screen()

    parent_grid = Grid(
        cells=get_grid_cells_in_columns(),
        display_home=(1, 1),
        in_rows=False,
        auto_finalise=True
    )

    parent_grid.finalise = True
    parent_grid.write()
    print(10 * "\n")
