# import time
#
# from core.buffer import Buffer
# from core.sequences import ANSISequences
# from styles.cell import Cell
# from styles.grid import Grid
# from examples.useful import *
# from core.table_config import ConsoleDisplayConf
# from styles.table import Table
# from core.alignment import Alignment
# import pandas as pd
# from core.pandas_table_config import PandasConf
#
#
# def clear_screen(col: int = None):
#     buf = Buffer()
#     buf.specials = ANSISequences.Erase.SCREEN
#     buf.specials = ANSISequences.CommonPrivate.CURSOR_INVISIBLE
#     buf.write_special()
#
#     if col is not None:
#         buf.background = col
#         buf.write_config()
#         whitespace = " " * 100
#         for _ in range(100):
#             buf.write_text(whitespace)
#
#
# def create_table_conf_with_colours():
#     bg_col = 236
#     outer_border_col = 25
#     inner_border_col = 112
#     inner_border_corner_col = 227
#     fg_col = 135
#
#     column_col = 12
#     index_col = 160
#     data_col = 120
#
#     table_name_buf = Buffer()
#     table_name_buf.graphics = ANSISequences.Graphics.BOLD
#     table_name_buf.foreground = fg_col
#     table_name_buf.background = bg_col
#
#     index_buf = Buffer()
#     index_buf.graphics = ANSISequences.Graphics.BOLD
#     index_buf.graphics = ANSISequences.Graphics.ITALIC
#     index_buf.foreground = index_col
#     index_buf.background = bg_col
#
#     column_buf = Buffer()
#     column_buf.graphics = ANSISequences.Graphics.BOLD
#     column_buf.foreground = column_col
#     column_buf.background = bg_col
#
#     data_buf = Buffer()
#     data_buf.foreground = data_col
#     data_buf.background = bg_col
#
#     outer_border_buffer = Buffer()
#     outer_border_buffer.background = bg_col
#     outer_border_buffer.foreground = outer_border_col
#
#     inner_border_buffer = Buffer()
#     inner_border_buffer.background = bg_col
#     outer_border_buffer.foreground = inner_border_col
#
#     inner_border_corner_buffer = Buffer()
#     inner_border_corner_buffer.background = bg_col
#     inner_border_corner_buffer.foreground = inner_border_corner_col
#
#     table_name = Cell(text=["Table name"], style=table_name_buf)
#
#     index = [
#         Cell(text=["Ind 0"], style=index_buf),
#         Cell(text=["Ind 1"], style=index_buf),
#         Cell(text=["Ind 2"], style=index_buf),
#     ]
#
#     columns = [
#         Cell(text=["Col 0"], style=column_buf),
#         Cell(text=["Col 1"], style=column_buf),
#     ]
#
#     outer_borders = [
#         Cell(text=["═"], style=outer_border_buffer, auto_update=False),
#         # None,
#         Cell(text=["║"], style=outer_border_buffer, auto_update=False),
#         Cell(text=["═"], style=outer_border_buffer, auto_update=False),
#         Cell(text=["║"], style=outer_border_buffer, auto_update=False),
#         Cell(text=["╬"], style=outer_border_buffer, auto_update=False),
#     ]
#
#     inner_borders = [
#         Cell(text=["━"], style=inner_border_buffer, auto_update=False),
#         # None,
#         Cell(text=["┃"], style=inner_border_buffer, auto_update=False),
#         Cell(text=["╂"], style=inner_border_corner_buffer, auto_update=False),
#     ]
#
#     data = [
#         [
#             Cell(text=["0, 0"], style=data_buf, alignment=Alignment.CENTER),
#             Cell(text=["0, 1"], style=data_buf, alignment=Alignment.CENTER),
#             Cell(text=["0, 2"], style=data_buf, alignment=Alignment.CENTER),
#         ],
#         [
#             Cell(text=["1, 0"], style=data_buf, alignment=Alignment.CENTER),
#             Cell(text=["1, 1"], style=data_buf, alignment=Alignment.CENTER),
#             Cell(text=["1, 2"], style=data_buf, alignment=Alignment.CENTER),
#         ],
#     ]
#
#     conf = ConsoleDisplayConf(
#         table_name=table_name,
#         display_home=(20, 20),
#         index=index,
#         columns=columns,
#         data=data,
#         in_rows=False,
#         outer_borders=outer_borders,
#         inner_borders=inner_borders,
#     )
#
#     return conf
#
#
# def create_pandas_table_conf():
#     data_buf = Buffer()
#     data_buf.foreground = 69
#
#     index_buf = Buffer()
#     index_buf.graphics = ANSISequences.Graphics.BOLD
#     index_buf.graphics = ANSISequences.Graphics.ITALIC
#     index_buf.foreground = 141
#
#     column_buf = Buffer()
#     column_buf.graphics = ANSISequences.Graphics.BOLD
#     column_buf.foreground = 160
#
#     df = pd.read_csv("examples/PizzaDeliveryTimes.csv")
#     conf = PandasConf(
#         display_home=(1, 1),
#         dataframe=df,
#         data_style=data_buf,
#         index_style=index_buf,
#         column_style=column_buf,
#     )
#     return conf
#
#
# def basic_table_normal_conf():
#     clear_screen(236)
#
#     conf = create_table_conf()
#
#     table = Table(conf)
#
#     # print(table.cells[0][0])
#     table.write()
#     table.update_cell(0, 2, ["cell"])
#     table.update_index(2, ["indx"])
#     # table.update_table_name(["tabs"])
#     # table.update_column(1, ["cll"])
#
#     print("\n" * 20)
#
#
# def nested_table_normal_conf():
#     clear_screen()
#
#     parent_conf = create_table_conf()
#     nested_conf = create_table_conf()
#
#     nested_t = Table(nested_conf)
#     parent_conf.data[0][1] = nested_t
#     parent_table = Table(parent_conf)
#     # parent_table.update_cell_home(0, 1)
#
#     parent_table.update_nested_table_cell([(0, 1), (0, 2)], ["cell"])
#     nested_t.update_cell(0, 1, ["df"])
#
#     # print(table.cells[0][0])
#
#     parent_table.write()
#
#     print("\n" * 10)
#
#
# def basic_table_pandas_conf():
#     clear_screen()
#
#     conf = create_pandas_table_conf()
#     conf = conf.convert_pandas_conf_to_console_conf()
#     table = Table(conf)
#
#     table.write()
#     # table.update_cell(0, 2, ["cell"])
#     # table.update_index(2, ["indx"])
#     # table.update_table_name(["tabs"])
#     # table.update_column(1, ["cll"])
#
#     print("\n" * 20)
#
#
# def nested_table_pandas_conf():
#     clear_screen()
#
#     parent_conf = create_pandas_table_conf()
#     parent_conf = parent_conf.convert_pandas_conf_to_console_conf()
#     nested_conf = create_pandas_table_conf()
#     nested_conf = nested_conf.convert_pandas_conf_to_console_conf()
#
#     nested_table = Table(nested_conf)
#     # parent_conf.index[0] = nested_table
#     parent_conf.data[0][0] = nested_table
#     parent_table = Table(parent_conf)
#
#     parent_table.write()
#
#
#     print("\n" * 20)
#
#
# if __name__ == '__main__':
#     basic_table_normal_conf()
#     # nested_table_normal_conf()
#     # basic_table_pandas_conf()
#     # nested_table_pandas_conf()
