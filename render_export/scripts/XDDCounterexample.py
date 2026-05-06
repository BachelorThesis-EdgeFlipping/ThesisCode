from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

order = 8
labels = [
  "A", #0
  "B", #1
  "C", #2
  "D", #3
  "E", #4
  "F", #5
  "G", #6
  "H" #7
]
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
  labels = labels,
  filename="DD_counterexample_source")

draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_target,
  title= "$T_T$",
  labels = labels,
  filename="DD_counterexample_target")
#exec: python -m 
