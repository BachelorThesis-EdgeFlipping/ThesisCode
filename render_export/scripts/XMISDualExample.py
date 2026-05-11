from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

n = 7

labels = [
  "$A$",
  "$B$",
  "$C$",
  "$D$",
  "$E$",
  "$F$",
  "$G$"
]

highlight_width = 12
highlight_color = Color.PURPLE
c_happy = Color.CUSTOM_GREEN

render_edges_source= [
  RE((0,3)),
  RE((0,4)),
  RE((1,3)),
  RE((4,6)),
]
render_edges_target= [
  RE((0,5)),
  RE((1,5)),
  RE((2,5)),
  RE((2,4)),
]


render_edges_path_1_0 = [
  RE((0,3), highlight_color=highlight_color, highlight_width=highlight_width),
  RE((0,4)),
  RE((1,3)),
  RE((4,6), highlight_color=highlight_color, highlight_width=highlight_width),
]
render_edges_path_1_1 = [
  RE((1,4)),
  RE((0,4), highlight_color=highlight_color, highlight_width=highlight_width),
  RE((1,3), highlight_color=highlight_color, highlight_width=highlight_width),
  RE((0,5), c_happy),
]
render_edges_path_1_2 = [
  RE((1,4), highlight_color=highlight_color, highlight_width=highlight_width),
  RE((1,5), c_happy),
  RE((2,4), c_happy),
  RE((0,5), c_happy),
]
render_edges_path_1_3 = [
  RE((2,5), c_happy),
  RE((1,5), c_happy),
  RE((2,4), c_happy),
  RE((0,5), c_happy),
]

render_edges_path_2_0 = [
  RE((0,5)),
  RE((1,5)),
  RE((2,5), highlight_color=highlight_color, highlight_width=highlight_width),
  RE((2,4)),
]
render_edges_path_2_1 = [
  RE((0,5)),
  RE((1,5),  highlight_color=highlight_color, highlight_width=highlight_width),
  RE((1,4)),
  RE((2,4),  highlight_color=highlight_color, highlight_width=highlight_width),
]
render_edges_path_2_2 = [
  RE((0,5),  highlight_color=highlight_color, highlight_width=highlight_width),
  RE((0,4),  c_happy),
  RE((1,4),  highlight_color=highlight_color, highlight_width=highlight_width),
  RE((1,3), c_happy),
]
render_edges_path_2_3 = [
  RE((4,6),  c_happy),
  RE((0,4),  c_happy),
  RE((0,3),  c_happy),
  RE((1,3), c_happy),
]



draw_polygon_triangulation(
  n,
  render_edges_source, 
  filename="MIS_maximality_symmetry_counterexample_source",
  title=r"$T_S$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  render_edges_target, 
  filename="MIS_maximality_symmetry_counterexample_target",
  title=r"$T_T$",
  labels=labels
)





draw_polygon_triangulation(
  n,
  render_edges_path_1_0, 
  filename="MIS_maximality_symmetry_counterexample_1_0",
  title=r"$T_O=T_S$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  render_edges_path_1_1, 
  filename="MIS_maximality_symmetry_counterexample_1_1",
  title=r"$T_1$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  render_edges_path_1_2, 
  filename="MIS_maximality_symmetry_counterexample_1_2",
  title=r"$T_2$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  render_edges_path_1_3, 
  filename="MIS_maximality_symmetry_counterexample_1_3",
  title=r"$T_3 = T_T$",
  labels=labels
)





draw_polygon_triangulation(
  n,
  render_edges_path_2_0, 
  filename="MIS_maximality_symmetry_counterexample_2_0",
  title=r"$T^{-1}_O=T_T$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  render_edges_path_2_1, 
  filename="MIS_maximality_symmetry_counterexample_2_1",
  title=r"$T^{-1}_1$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  render_edges_path_2_2, 
  filename="MIS_maximality_symmetry_counterexample_2_2",
  title=r"$T^{-1}_2$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  render_edges_path_2_3, 
  filename="MIS_maximality_symmetry_counterexample_2_3",
  title=r"$T^{-1}_3 = T_S$",
  labels=labels
)
