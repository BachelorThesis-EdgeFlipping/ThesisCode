from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

n = 5

labels = [
  "$A_1$",
  "$A_2$",
  "$A_3$",
  "$A_4$",
  "$A_5$",
  "$B_1$",
  "$B_2$",
  "$B_3$",
  "$B_4$",
  "$B_5$"
]

center_edge_h_w = 2
center_edge_h_c = Color.BLUE
h_c_1 = Color.FAINT_LIGHT_PURPLE
h_c_2 = Color.FAINT_LIGHT_GREEN
render_edges_1 = [
  RE((0,6)),
  RE((0,7)),
  RE((0,8)),
  RE((0,9), width=center_edge_h_w, color=center_edge_h_c),
  RE((1,9)),
  RE((2,9)),
  RE((3,9))
]
color_faces_1_1 = [
  CF((0,5,6), h_c_1),
  CF((0,6,7), h_c_1),
  CF((0,7,8), h_c_1),
  CF((0,8,9), h_c_1),
  CF((0,1,9), h_c_1)
]
color_faces_1_2 = [
  CF((0,8,9), h_c_2),
  CF((0,1,9), h_c_2),
  CF((1,2,9), h_c_2),
  CF((2,3,9), h_c_2),
  CF((3,4,9), h_c_2),
]

render_edges_2 = [
  RE((1,5)),
  RE((2,5)),
  RE((3,5)),
  RE((3,6), width=center_edge_h_w, color=center_edge_h_c),
  RE((4,6)),
  RE((4,7)),
  RE((4,8))
]
color_faces_2_1 = [
  CF((0,1,5), h_c_1),
  CF((1,2,5), h_c_1),
  CF((2,3,5), h_c_1),
  CF((3,4,6), h_c_1),
  CF((3,5,6), h_c_1),
]
color_faces_2_2 = [
  CF((3,4,6), h_c_2),
  CF((3,5,6), h_c_2),
  CF((4,6,7), h_c_2),
  CF((4,7,8), h_c_2),
  CF((4,8,9), h_c_2),
]



draw_channel_triangulation(
  n,
  render_edges_1, 
  filename="HE_closed_halves_1_left",
  color_faces=color_faces_1_1,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_1, 
  filename="HE_closed_halves_1_right",
  color_faces=color_faces_1_2,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_2, 
  filename="HE_closed_halves_2_left",
  color_faces=color_faces_2_1,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_2, 
  filename="HE_closed_halves_2_right",
  color_faces=color_faces_2_2,
  labels=labels
)




#exec: python -m 
