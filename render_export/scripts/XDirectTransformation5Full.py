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
  "$B_5$",
]

edge_highlight_width = 3

# ---- STEP 0 ----

render_edges_0_0 = [
  RE((0,6)),
  RE((0,7)),
  RE((0,8)),
  RE((0,9)),
  RE((1,9)),
  RE((2,9)),
  RE((3,9))
]
color_faces_0_0 = [
  CF((0,1,9), Color.L_0_1),
  CF((0,8,9), Color.L_0_1)
]
render_edges_0_1 = [
  RE((0,6)),
  RE((0,7)),
  RE((0,8)),
  RE((1,8), Color.L_0_0, width=edge_highlight_width),
  RE((1,9)),
  RE((2,9)),
  RE((3,9))
]

# ---- STEP 1 ----

render_edges_1_0 = [
  RE((0,6)),
  RE((0,7)),
  RE((0,8)),
  RE((1,8), Color.L_0_0),
  RE((1,9)),
  RE((2,9)),
  RE((3,9))
]
color_faces_1_0 = [
  CF((1,2,9), Color.L_1_1),
  CF((1,8,9), Color.L_1_1),

  CF((0,1,8), Color.L_1_2),
  CF((0,7,8), Color.L_1_2),
]
render_edges_1_1 = [
  RE((0,6)),
  RE((0,7)),
  RE((1,7), Color.L_1_0, width=edge_highlight_width),
  RE((1,8), Color.L_0_0),
  RE((2,8), Color.L_1_0, width=edge_highlight_width),
  RE((2,9)),
  RE((3,9))
]


# ---- STEP 2 ----

render_edges_2_0 = [
  RE((0,6)),
  RE((0,7)),
  RE((1,7), Color.L_1_0),
  RE((1,8), Color.L_0_0),
  RE((2,8), Color.L_1_0),
  RE((2,9)),
  RE((3,9))
]
color_faces_2_0 = [
  CF((0,1,7), Color.L_2_1),
  CF((0,6,7), Color.L_2_1),

  CF((1,2,8), Color.L_2_2),
  CF((1,7,8), Color.L_2_2),
  
  CF((2,3,9), Color.L_2_1),
  CF((2,8,9), Color.L_2_1),
]
render_edges_2_1 = [
  RE((0,6)),
  RE((1,6), Color.L_2_0, width=edge_highlight_width),
  RE((1,7), Color.L_1_0),
  RE((2,7), Color.L_2_0, width=edge_highlight_width),
  RE((2,8), Color.L_1_0),
  RE((3,8), Color.L_2_0, width=edge_highlight_width),
  RE((3,9))
]

# ---- STEP 3 ----

render_edges_3_0 = [
  RE((0,6)),
  RE((1,6), Color.L_2_0),
  RE((1,7), Color.L_1_0),
  RE((2,7), Color.L_2_0),
  RE((2,8), Color.L_1_0),
  RE((3,8), Color.L_2_0),
  RE((3,9))
]
color_faces_3_0 = [
  CF((0,1,6), Color.L_3_1),
  CF((0,5,6), Color.L_3_1),
  
  CF((1,2,7), Color.L_3_2),
  CF((1,6,7), Color.L_3_2),
  
  CF((2,3,8), Color.L_3_1),
  CF((2,7,8), Color.L_3_1),
 
  CF((3,4,9), Color.L_3_2),
  CF((3,8,9), Color.L_3_2),
]
render_edges_3_1 = [
  RE((1,5), Color.L_3_0, width=edge_highlight_width),
  RE((1,6), Color.L_2_0),
  RE((2,6), Color.L_3_0, width=edge_highlight_width),
  RE((2,7), Color.L_2_0),
  RE((3,7), Color.L_3_0, width=edge_highlight_width),
  RE((3,8), Color.L_2_0),
  RE((4,8), Color.L_3_0, width=edge_highlight_width)
]


# ---- STEP 4 ----

render_edges_4_0 = [
  RE((1,5), Color.L_3_0),
  RE((1,6), Color.L_2_0),
  RE((2,6), Color.L_3_0),
  RE((2,7), Color.L_2_0),
  RE((3,7), Color.L_3_0),
  RE((3,8), Color.L_2_0),
  RE((4,8), Color.L_3_0)
]
color_faces_4_0 = [
  CF((1,5,6), Color.L_4_1),
  CF((1,2,6), Color.L_4_1),

  CF((2,3,7), Color.L_4_2),
  CF((2,6,7), Color.L_4_2),

  CF((3,4,8), Color.L_4_1),
  CF((3,7,8), Color.L_4_1),
]
render_edges_4_1 = [
  RE((1,5), Color.L_3_0),
  RE((2,5), Color.L_4_0, width=edge_highlight_width),
  RE((2,6), Color.L_3_0),
  RE((3,6),Color.L_4_0, width=edge_highlight_width),
  RE((3,7), Color.L_3_0),
  RE((4,7),Color.L_4_0, width=edge_highlight_width),
  RE((4,8), Color.L_3_0)
]

# ---- STEP 5 ----

render_edges_5_0 = [
  RE((1,5), Color.L_3_0),
  RE((2,5), Color.L_4_0),
  RE((2,6), Color.L_3_0),
  RE((3,6),Color.L_4_0),
  RE((3,7), Color.L_3_0),
  RE((4,7),Color.L_4_0),
  RE((4,8), Color.L_3_0)
]
color_faces_5_0 = [
  CF((2,3,6), Color.L_5_1),
  CF((2,5,6), Color.L_5_1),

  CF((3,4,7), Color.L_5_2),
  CF((3,6,7), Color.L_5_2),
]
render_edges_5_1 = [
  RE((1,5), Color.L_3_0),
  RE((2,5), Color.L_4_0),
  RE((3,5), Color.L_5_0, width=edge_highlight_width),
  RE((3,6),Color.L_4_0),
  RE((4,6), Color.L_5_0, width=edge_highlight_width),
  RE((4,7),Color.L_4_0),
  RE((4,8), Color.L_3_0)
]

# ---- STEP 6 ----

render_edges_6_0 = [
  RE((1,5), Color.L_3_0),
  RE((2,5), Color.L_4_0),
  RE((3,5), Color.L_5_0),
  RE((3,6),Color.L_4_0),
  RE((4,6), Color.L_5_0),
  RE((4,7),Color.L_4_0),
  RE((4,8), Color.L_3_0)
]
color_faces_6_0 = [
  CF((3,4,6), Color.L_6_1),
  CF((3,5,6), Color.L_6_1),
]

# ---- STEP 7 ----

render_edges_7 = [
  RE((1,5), Color.L_3_0),
  RE((2,5), Color.L_4_0),
  RE((3,5), Color.L_5_0),
  RE((4,5),Color.L_6_0, width=edge_highlight_width),
  RE((4,6), Color.L_5_0),
  RE((4,7),Color.L_4_0),
  RE((4,8), Color.L_3_0)
]


draw_channel_triangulation(
  n,
  render_edges_0_0, 
  filename="HE_direct_transformation_full_0_0",
  color_faces=color_faces_0_0,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_0_1, 
  filename="HE_direct_transformation_full_0_1",
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_1_0, 
  filename="HE_direct_transformation_full_1_0",
  color_faces=color_faces_1_0,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_1_1, 
  filename="HE_direct_transformation_full_1_1",
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_2_0, 
  filename="HE_direct_transformation_full_2_0",
  color_faces=color_faces_2_0,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_2_1, 
  filename="HE_direct_transformation_full_2_1",
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_3_0, 
  filename="HE_direct_transformation_full_3_0",
  color_faces=color_faces_3_0,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_3_1, 
  filename="HE_direct_transformation_full_3_1",
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_4_0, 
  filename="HE_direct_transformation_full_4_0",
  color_faces=color_faces_4_0,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_4_1, 
  filename="HE_direct_transformation_full_4_1",
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_5_0, 
  filename="HE_direct_transformation_full_5_0",
  color_faces=color_faces_5_0,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_5_1, 
  filename="HE_direct_transformation_full_5_1",
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_6_0, 
  filename="HE_direct_transformation_full_6_0",
  color_faces=color_faces_6_0,
  labels=labels
)
draw_channel_triangulation(
  n,
  render_edges_7, 
  filename="HE_direct_transformation_full_7",
  labels=labels
)


#exec: python -m 
