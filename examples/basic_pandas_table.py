from examples.useful import clear_screen, create_pandas_table_conf
from styles.table import Table


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
