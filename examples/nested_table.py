from examples.useful import clear_screen, create_table_conf
from styles.table import Table


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
