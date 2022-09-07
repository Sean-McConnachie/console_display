from examples.useful import clear_screen, create_pandas_table_conf
from styles.table import Table


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
