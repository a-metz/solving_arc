# core entities
from .grid import Grid
from .argument import (
    ArgumentError,
    expect_scalar,
    extract_scalar,
    expect_tuple,
    extract_tuple,
    expect_same_shape,
)

# operations
from .logic import elementwise_equal_and, elementwise_equal_or, elementwise_xor
from .segmentation import extract_islands, extract_color_patches, extract_color_patch
from .color import switch_color, map_color
