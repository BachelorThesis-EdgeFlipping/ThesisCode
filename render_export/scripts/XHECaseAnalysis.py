from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

order = 12
C_HE = Color.BLUE
C_DADDY = Color.ORANGE
C_JUVENILE = Color.PURPLE

title_before = r"$T_i\ &\ T_{i+1}$"
title_after = r"$N(T_i)\ &\ N(T_{i+1})$"

info_box_before = InfoBox(
  items=[
    InfoBoxItem(r"$e$", C_HE, edge_style="dotted"),
    InfoBoxItem(r"$\varepsilon(f)$", C_DADDY),
    InfoBoxItem(r"$\phi(f)$", C_JUVENILE)
  ],
  loc="upper left",
  bbox_to_anchor=(-0.12, 1.12)
)
info_box_after = InfoBox(
  items=[
    InfoBoxItem(r"$e$", C_HE),
    InfoBoxItem(r"$e_\varepsilon$", C_DADDY),
    InfoBoxItem(r"$e_\phi$", C_JUVENILE),
  ],
  loc="upper left",
  bbox_to_anchor=(-0.12, 1.12)
)



# Case 1

labels_1 = [
  r"$A^e$", #0
  "", #1
  "", #2
  "", #3
  r"$B^{\gamma}$", #4
  "", #5
  "", #6
  r"$C^{\gamma}$", #7
  "", #8
  r"$D^{\gamma}$", #9
  "", #10
  r"$A^{\gamma}$", #11
]
render_edges_1_before = [
  RE((4,7)),
  RE((7,9)),
  RE((9,11)),
  RE((4,11)),
  RE((0,3), C_HE, edge_style="dotted"),
  RE((7,11), C_DADDY),
  RE((4,9), C_JUVENILE),
]
render_edges_1_after = [
  RE((4,7)),
  RE((7,9)),
  RE((9,11)),
  RE((4,11)),
  RE((0,3), C_HE),
  RE((7,11), C_DADDY),
  RE((4,9), C_JUVENILE),
]
color_vertices_1 = [
  CV(0, Color.BLUE)
]


#Case 2

labels_2 = [
  r"$A^{\gamma}$", #0
  "", #1
  "", #2
  r"$B^{\gamma}$", #3
  r"$A^e$", #4
  "", #5
  r"$C^{\gamma}$", #6
  "", #7
  "", #8
  r"$D^{\gamma}$", #9
  "", #10
  "", #11
]
render_edges_2_1_before = [
  RE((0,3)),
  RE((3,6)),
  RE((6,9)),
  RE((0,9)),
  RE((0,6), C_DADDY),
  RE((3,9), C_JUVENILE),
  RE((4,8), C_HE, edge_style="dotted"),
]
render_edges_2_1_after = [
  RE((0,3)),
  RE((3,4)),
  RE((4,9)),
  RE((0,9)),
  RE((0,4), C_DADDY),
  RE((3,9), C_JUVENILE),
  RE((4,8), C_HE),
]
render_edges_2_2_before = [
  RE((0,3)),
  RE((3,6)),
  RE((6,9)),
  RE((0,9)),
  RE((0,6), C_DADDY),
  RE((3,9), C_JUVENILE),
  RE((1,4), C_HE, edge_style="dotted"),
]
render_edges_2_2_after = [
  RE((0,4)),
  RE((4,6)),
  RE((6,9)),
  RE((0,9)),
  RE((0,6), C_DADDY),
  RE((4,9), C_JUVENILE),
  RE((1,4), C_HE),
]
color_vertices_2 = [
  CV(4, Color.BLUE)
]




# Case 3

labels_3 = [
  r"$A^{\gamma}$", #0
  "", #1
  r"$A^e$", #2
  "", #3
  r"$B^{\gamma}$", #4
  "", #5
  r"$C^{\gamma}$", #6
  "", #7
  "", #8
  r"$D^{\gamma}$", #9
  "", #10
  "", #11
]
render_edges_3_before = [
  RE((0,4)),
  RE((4,6)),
  RE((6,9)),
  RE((0,9)),
  RE((0,6), C_DADDY),
  RE((4,9), C_JUVENILE),
  RE((2,8), C_HE, edge_style="dotted"),
]
render_edges_3_after = [
  RE((0,2), bg_color=EDGE_COLOR, color=C_DADDY, edge_style="dashed"),
  RE((2,4), bg_color=EDGE_COLOR, color=C_JUVENILE, edge_style="dashed"),
  RE((4,6)),
  RE((2,6), bg_color=EDGE_COLOR, color=C_DADDY, edge_style="dashed"),
  RE((0,9)),
  RE((2,9), bg_color=EDGE_COLOR, color=C_JUVENILE, edge_style="dashed"),
  RE((2,8), C_HE),
]

color_vertices_3 = [
  CV(2, Color.BLUE)
]




#Case 4

labels_4 = [
  r"$A^{\gamma}$/A^e$", #0
  "", #1
  "", #2
  r"$B^{\gamma}$", #3
  "", #4
  "", #5
  r"$C^{\gamma}$", #6
  "", #7
  "", #8
  r"$D^{\gamma}$", #9
  "", #10
  "", #11
]
render_edges_4_before = [
  RE((0,3)),
  RE((3,6)),
  RE((6,9)),
  RE((0,9)),
  RE((0,6), bg_color=C_DADDY, color=C_HE, edge_style="dotted"),
  RE((3,9), C_JUVENILE),
]
render_edges_4_after = [
  RE((0,3), bg_color=EDGE_COLOR, color=C_JUVENILE, edge_style="dashed"),
  RE((3,6)),
  RE((6,9)),
  RE((0,9), bg_color=EDGE_COLOR, color=C_JUVENILE, edge_style="dashed"),
  RE((0,6), bg_color=C_HE, color=C_DADDY, edge_style="dashed"),
]

color_vertices_4 = [
  CV(0, Color.BLUE)
]



# Case 5

labels_5 = [
  "", #0
  "", #1
  "", #2
  "", #3
  r"$B^{\gamma}/A^e$", #4
  "", #5
  "", #6
  r"$C^{\gamma}$", #7
  "", #8
  r"$D^{\gamma}$", #9
  "", #10
  r"$A^{\gamma}$", #11
]
render_edges_5_before = [
  RE((4,7)),
  RE((7,9)),
  RE((9,11)),
  RE((4,11), bg_color=EDGE_COLOR, color=C_HE, edge_style="dotted"),
  RE((7,11), C_DADDY),
  RE((4,9), C_JUVENILE),
]
render_edges_5_after = [
  RE((4,7)),
  RE((7,9)),
  RE((9,11)),
  RE((4,11), bg_color=EDGE_COLOR, color=C_HE, edge_style="dashed"),
  RE((7,11), C_DADDY),
  RE((4,9), C_JUVENILE),
]
color_vertices_5 = [
  CV(4, Color.BLUE)
]








draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_1_before,
  color_vertices=color_vertices_1,
  labels = labels_1,
  title= title_before,
  draw_border=False,
  info_box=info_box_before,
  filename="HE_case_analysis_1_before"
)
draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_1_after,
  color_vertices=color_vertices_1,
  labels = labels_1,
  title= title_after,
  draw_border=False,
  info_box=info_box_after,
  filename="HE_case_analysis_1_after"
)


draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_2_1_before,
  color_vertices=color_vertices_2,
  labels = labels_2,
  title= title_before,
  draw_border=False,
  info_box=info_box_before,
  filename="HE_case_analysis_2_1_before"
)
draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_2_1_after,
  color_vertices=color_vertices_2,
  labels = labels_2,
  title= title_after,
  draw_border=False,
  info_box=info_box_after,
  filename="HE_case_analysis_2_1_after"
)
draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_2_2_before,
  color_vertices=color_vertices_2,
  labels = labels_2,
  title= title_before,
  draw_border=False,
  info_box=info_box_before,
  filename="HE_case_analysis_2_2_before"
)
draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_2_2_after,
  color_vertices=color_vertices_2,
  labels = labels_2,
  title= title_after,
  draw_border=False,
  info_box=info_box_after,
  filename="HE_case_analysis_2_2_after"
)


draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_3_before,
  color_vertices=color_vertices_3,
  labels = labels_3,
  title= title_before,
  draw_border=False,
  info_box=info_box_before,
  filename="HE_case_analysis_3_before"
)
draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_3_after,
  color_vertices=color_vertices_3,
  labels = labels_3,
  title= title_after,
  draw_border=False,
  info_box=info_box_after,
  filename="HE_case_analysis_3_after"
)


draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_4_before,
  color_vertices=color_vertices_4,
  labels = labels_4,
  title= title_before,
  draw_border=False,
  info_box=info_box_before,
  filename="HE_case_analysis_4_before"
)
draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_4_after,
  color_vertices=color_vertices_4,
  labels = labels_4,
  title= title_after,
  draw_border=False,
  info_box=info_box_after,
  filename="HE_case_analysis_4_after"
)


draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_5_before,
  color_vertices=color_vertices_5,
  labels = labels_5,
  title= title_before,
  draw_border=False,
  info_box=info_box_before,
  filename="HE_case_analysis_5_before"
)
draw_polygon_triangulation(
  order=order,
  render_edges=render_edges_5_after,
  color_vertices=color_vertices_5,
  labels = labels_5,
  title= title_after,
  draw_border=False,
  info_box=info_box_after,
  filename="HE_case_analysis_5_after"
)