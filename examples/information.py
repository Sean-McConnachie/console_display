"""
This package was designed to be extremely customizable. This is why every displayable element has:
    - Outer padding (doesn't affect inner content) - (left, right, top, bottom)
    - Outer padding style
    - Each cell has a style/buffer (i.e. foreground, background, graphics)
    - Tables have outer borders that are all cells (left, right, top, bottom, corner)
    - Tables have inner borders that are all cells (left, right, top, bottom, corner)
    - Tables and grids can be nested within each other
    - Display homes are automatically set for any display element

Buffers represent the style of a cell. They are used to set the foreground, background, and graphics of a cell:
    - Foreground: The color of the text
    - Background: The color of the background
    - Graphics: The style of the text (bold, italic, underline, etc.)
    - Any other ANSI escape sequence can be added to a buffer
    - use_validator: If True, the buffer will validate the ANSI escape sequence before writing it to the terminal (recommended off)

Buffers have three different display lists:
    - Graphics: The graphics that are applied to the cell (called whenever a cell is written)
    - Specials: The special characters that are applied to the cell (called by the user)
    - Common private: The common private characters that are applied to the cell (called by the user)

These different lists allow for a single buffer to perform multiple different operations when the user likes.
"""
from core.buffer import Buffer
from core.sequences import ANSISequences


# Example of clearing the terminal screen
def clear_screen():
    buf = Buffer()
    buf.specials = ANSISequences.Erase.SCREEN
    buf.write_special()


# Example of creating a buffer with a style
def styled_buffer():
    buf = Buffer()
    buf.graphics = ANSISequences.Graphics.BOLD  # Bold text
    buf.foreground = 118  # Green foreground
    buf.background = 17  # Dark blue background
    buf.write_text("I'm boring!\n")  # This will not print styled text
    buf.write_config()  # Doesn't output anything, only applies the style to the buffer
    buf.write_text("Bring some happiness into my life!")  # This will print styled text


# See other examples on how to utilize cells, tables and grids.
