from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

n = 6

labels = [
  "$A$",
  "$B$",
  "$C$",
  "$D$",
  "$E$",
  "$F$",
]

render_edges = [
  RE((0,2)),
  RE((2,5)),
  RE((3,5)),
  RE((1,5), Color.BLUE, edge_style="dotted"),
]



draw_polygon_triangulation(
  n,
  render_edges, 
  filename="MIS_no_happy_edges",
  labels=labels
)
