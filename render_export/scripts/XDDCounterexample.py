from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

order = 8
render_edges_source = [
  RE((1,7)),
  RE((1,6)),
  RE((1,5)),
  RE((2,5)),
  RE((2,4))
]

render_edges_target = [
  RE((0,2)),
  RE((0,3)),
  RE((0,4)),
  RE((0,5)),
  RE((5,7))
]


draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_source,
  title= "$T_S$",
  filename="DD_counterexample_source")

draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_target,
  title= "$T_T$",
  filename="DD_counterexample_target")
#exec: python -m 
