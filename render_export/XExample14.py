from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

order = 4
extra_vertices = [
  XV((0,2), 0.5)
]
render_edges = [
  RE((0,4)),
  RE((1,4)),
  RE((2,4), c=C_HAPPY),
  RE((3,4))
]

draw_advanced_polygon_triangulation(order, extra_vertices, render_edges, filename="networkX_test2")
#exec: python -m 