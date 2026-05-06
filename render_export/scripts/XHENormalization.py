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

C_TYPE_0 = Color.BLUE
C_TYPE_1 = Color.GREEN
C_TYPE_2 = Color.TEAL

info_box_before = InfoBox(
  items=[
    InfoBoxItem("Type 0", C_TYPE_0, edge_style="dotted"),
    InfoBoxItem("Type 1", C_TYPE_1),
    InfoBoxItem(r"$\phi(f)$", C_TYPE_2)
  ],
  loc="upper left",
  bbox_to_anchor=(-0.12, 1.12)
)



render_edges_before = [
  RE((1,7), C_TYPE_1),
  RE((1,3), C_TYPE_2),
  RE((3,7), C_TYPE_2),
  RE((4,7), C_TYPE_2),
  RE((4,6), C_TYPE_1),
  RE((2,6), C_TYPE_0, edge_style="dotted"),
]

render_edges_after = [
  RE((1,7)),
  RE((2,7)),
  RE((2,6)),
  RE((2,4)),
  RE((4,6)),
  
]

color_vertices = [
  CV(2, Color.BLUE)
]


draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_before,
  color_vertices=color_vertices,
  title= "$T$",
  labels = labels,
  info_box=info_box_before,
  filename="HE_normalization_before")

draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_after,
  color_vertices=color_vertices,
  title= "$N(T)$",
  labels = labels,
  filename="HE_normalization_after")
#exec: python -m 
