from examples.useful import clear_screen, create_table_conf
from styles.table import Table


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
