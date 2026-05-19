from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

n = 12

labels = [
  "",
  "",
  "",
  "",
  "$A$", #4
  "$B$", #5
  "$C$", #6
  "",
  "",
  "",
  "",
  "",
]

h_width = 12
h_color = Color.MAGENTA
e_h_width = 2
e_width = 2
C_HAPPY = Color.BLUE
C_DEFENDER = Color.ORANGE
C_ATTACKER_P = Color.from_tuple((66, 171, 60)) #Color.GREEN
C_ATTACKER_F = Color.from_tuple((60, 151, 171)) #Color.CYAN

info_box_1 = InfoBox(
  items=[
    InfoBoxItem("defender", C_DEFENDER),
    InfoBoxItem("attacker (penetration)", C_ATTACKER_P),
    InfoBoxItem("attacker (flank)", C_ATTACKER_F),
  ],
  loc="upper left",
  bbox_to_anchor=(-0.5, 1.1)
)
info_box_2 = InfoBox(
  items=[
    InfoBoxItem("defender", C_DEFENDER),
    InfoBoxItem("p. attacker", C_ATTACKER_P),
    InfoBoxItem("f. attacker", C_ATTACKER_F),
    InfoBoxItem(r"included in $\sigma[i]$", h_color.make_transparent(int(255*0.2)) , width=6),

  ],
  loc="upper left",
  bbox_to_anchor=(-0.35, 1.08)
)

r_e_showcase_defender = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4)),
  RE((2,4)),
  RE((5,1), C_DEFENDER, e_h_width),
  RE((5,10), C_DEFENDER, e_h_width),
  RE((5,11), C_DEFENDER, e_h_width),
  RE((5,8), C_DEFENDER, e_h_width),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]

r_e_showcase_attacker = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4), C_ATTACKER_F, e_h_width),
  RE((2,4)),
  RE((5,1), C_DEFENDER, e_width),
  RE((5,10), C_DEFENDER, e_width),
  RE((5,11), C_DEFENDER, e_width),
  RE((5,8), C_DEFENDER, e_width),
  RE((6,8), C_ATTACKER_F, e_h_width),
  RE((8,10), C_ATTACKER_P, e_h_width),
  RE((1,11), C_ATTACKER_P, e_h_width),
  RE((0,5), C_ATTACKER_P, e_width, edge_style='dotted'),
  RE((9,5), C_ATTACKER_P,e_width, edge_style='dotted'),
  RE((2,5), C_ATTACKER_F, e_width,edge_style='dotted'),
  RE((7,5), C_ATTACKER_F, e_width,edge_style='dotted'),
]

r_e_case_uneven = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4), C_ATTACKER_F, e_width),
  RE((2,4)),
  RE((5,1), C_DEFENDER, e_width, highlight_width=h_width, highlight_color=h_color),
  RE((5,10), C_DEFENDER, e_width),
  RE((1,10), C_ATTACKER_P, e_width),
  RE((5,8), C_DEFENDER, e_width, highlight_width=h_width, highlight_color=h_color),
  RE((6,8), C_ATTACKER_F, e_width),
  RE((8,10), C_ATTACKER_P, e_width),
  RE((1,11)),
]
r_e_case_uneven_post = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4)),
  RE((2,4)),
  RE((4,10), C_ATTACKER_F, e_h_width),
  RE((5,10), C_DEFENDER, e_width),
  RE((1,10)),
  RE((6,10), C_ATTACKER_F, e_h_width),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]

r_e_case_two_one_flank = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((3,5), C_DEFENDER, e_width),
  RE((1,3), C_ATTACKER_P, e_width),
  RE((5,1), C_DEFENDER, e_width, highlight_width=h_width, highlight_color=h_color),
  RE((6,11)),
  RE((1,6), C_ATTACKER_F, e_width),
  RE((6,10)),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]

r_e_case_even_many = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4), C_ATTACKER_F, e_width, highlight_width=h_width, highlight_color=h_color),
  RE((2,4)),
  RE((5,1), C_DEFENDER, e_width),
  RE((5,10), C_DEFENDER, e_width),
  RE((5,11), C_DEFENDER, e_width, highlight_width=h_width, highlight_color=h_color),
  RE((5,8), C_DEFENDER, e_width, highlight_width=h_width, highlight_color=h_color),
  RE((6,8), C_ATTACKER_F, e_width),
  RE((8,10), C_ATTACKER_P, e_width),
  RE((1,11), C_ATTACKER_P, e_width),
]
r_e_case_even_many_post = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((2,5), C_DEFENDER, e_h_width),
  RE((2,4), C_ATTACKER_F, e_h_width),
  RE((5,1), C_DEFENDER, e_width),
  RE((5,10), C_DEFENDER, e_width),
  RE((1,10), C_ATTACKER_P, e_h_width),
  RE((6,10), C_ATTACKER_F, e_h_width),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]

r_e_case_two_two_flank = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4)),
  RE((1,3)),
  RE((5,11), C_DEFENDER, e_width),
  RE((4,11), C_ATTACKER_F, e_width, highlight_width=h_width, highlight_color=h_color),
  RE((5,10), C_DEFENDER, e_width, highlight_width=h_width, highlight_color=h_color),
  RE((6,10), C_ATTACKER_F, e_width),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]
r_e_case_two_two_flank_post = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4), C_ATTACKER_F, e_h_width, highlight_width=h_width, highlight_color=h_color),
  RE((1,3)),
  RE((5,11), C_DEFENDER, e_width, highlight_width=h_width, highlight_color=h_color),
  RE((1,5), C_DEFENDER, e_h_width),
  RE((6,11), C_ATTACKER_F, e_h_width),
  RE((6,10)),
  RE((6,8)),
  RE((8,10)),
  RE((1,11), C_ATTACKER_P, e_h_width),
]
r_e_case_two_two_flank_post_post = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((3,5), C_DEFENDER, e_h_width),
  RE((1,3), C_ATTACKER_P, e_h_width),
  RE((1,6), C_ATTACKER_F,  e_h_width),
  RE((1,5), C_DEFENDER, e_width),
  RE((6,11)),
  RE((6,10)),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]

draw_polygon_triangulation(
  n,
  r_e_showcase_defender, 
  filename="MIS_termination_defender_fan",
  title=r"$T^d$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_showcase_attacker, 
  filename="MIS_termination_attacker_edges",
  title=r"$T^d$",
  info_box=info_box_1,
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_uneven, 
  filename="MIS_termination_case_uneven",
  title=r"$T^d$",
  info_box=info_box_2,
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_uneven_post, 
  filename="MIS_termination_case_uneven_post",
  title=r"$T'^d$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_two_one_flank, 
  filename="MIS_termination_case_two_one_flank",
  title=r"$T^d$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_even_many, 
  filename="MIS_termination_case_even_many",
  title=r"$T^d$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_even_many_post, 
  filename="MIS_termination_case_even_many_post",
  title=r"$T'^d$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_two_two_flank, 
  filename="MIS_termination_case_two_two_flank",
  title=r"$T^d$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_two_two_flank_post, 
  filename="MIS_termination_case_two_two_flank_post",
  title=r"$T'^d$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_two_two_flank_post_post
, 
  filename="MIS_termination_case_two_two_flank_post_post",
  title=r"$T''^d$",
  labels=labels
)