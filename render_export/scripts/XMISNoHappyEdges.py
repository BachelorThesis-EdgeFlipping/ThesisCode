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

render_edges_source = [
  RE((0,2)),
  RE((2,5)),
  RE((3,5)),
  RE((1,5), Color.BLUE, edge_style="dotted"),
]
render_edges_target = [
  RE((2,5)),
  RE((3,5)),
  RE((1,5)),
]



draw_polygon_triangulation(
  n,
  render_edges_source, 
  filename="MIS_no_happy_edges_source",
  title=r"$T_S$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  render_edges_target, 
  filename="MIS_no_happy_edges_target",
  title=r"$T_T$",
  labels=labels
)
