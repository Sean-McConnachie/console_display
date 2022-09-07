# console_display
 
## Overview
 - This is a library for displaying text in tabular format in the console.
 - It allows text to be styled using ANSI escape codes.
 - When updating information for a cell, only that relevant cell is printed, not the entire screen.
 - Information can be displayed in a table:
   - Tables have column headers
   - Tables have index labels
   - Both labels and headers are optional - `T/T`, `T/F`, `F/T`, `F/F`
   - Tables can be nested within one another
   - Allow for easy addressing of cells, indexes and columns:
     - `my_table.update_cell(column=1, row=2, text=["new text"])`
     - `my_table.update_index(row=2, text=["new text"])`
     - `my_table.update_column(column=1, text=["new text"])`
   - Tables have borders (both outer and inner)
   - Tables can be created purely from creating `Cell` objects by passing a `ConsoleDisplayConf`
   - Or tables can be created from a Pandas `DataFrame` object by:
     - First creating a `PandasConf` object
     - Then converting that to a `ConsoleDisplayConf` object using the `.convert_pandas_conf_to_console_conf()` method
 - Grids are a relatively low level way of displaying information:
   - They do not create borders
   - They do not have index headers
   - They do not have column headers
   - Grids are inherited by `Table` to provide more useful functionality
 - Every display element inherits from `DisplayProperty`:
   - Outer padding
   - Outer padding style
   - Display home (set by user or inferred if in a table/grid)

### See `examples` for screenshots and how to use the library

