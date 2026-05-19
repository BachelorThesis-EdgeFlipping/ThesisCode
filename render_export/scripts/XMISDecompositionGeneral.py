from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

order = 5
extra_vertices = [
  XV((0,2), 0.5)
]

C_HAPPY = Color.BLUE

info_box = InfoBox(
  items=[
    InfoBoxItem("happy edge", C_HAPPY)
  ],
  loc="upper left",
  bbox_to_anchor=(-0.06, 1)
)

render_edges = [
  RE((0,5), C_HAPPY,  width=2),
]

draw_advanced_polygon_triangulation(order, extra_vertices, render_edges, info_box=info_box, filename="MIS_decomposition_general")