from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

n = 12

labels = [
  "0",
  "1",
  "2",
  "3",
  "$A$", #4
  "$B$", #5
  "$C$", #6
  "7",
  "8",
  "9",
  "10",
  "11",
]

h_width = 10
h_color = Color.MAGENTA
e_width = 2
C_HAPPY = Color.BLUE
C_DEFENDER = Color.ORANGE
C_ATTACKER_P = Color.from_tuple((66, 171, 60)) #Color.GREEN
C_ATTACKER_F = Color.from_tuple((60, 151, 171)) #Color.CYAN

r_e_showcase_defender = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4)),
  RE((2,4)),
  RE((5,1), C_DEFENDER, e_width),
  RE((5,10), C_DEFENDER, e_width),
  RE((5,11), C_DEFENDER, e_width),
  RE((5,8), C_DEFENDER, e_width),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]

r_e_showcase_attacker = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4), C_ATTACKER_F, e_width),
  RE((2,4)),
  RE((5,1), C_DEFENDER),
  RE((5,10), C_DEFENDER),
  RE((5,11), C_DEFENDER),
  RE((5,8), C_DEFENDER),
  RE((6,8), C_ATTACKER_F, e_width),
  RE((8,10), C_ATTACKER_P, e_width),
  RE((1,11), C_ATTACKER_P, e_width),
  RE((0,5), C_ATTACKER_P, edge_style='dotted'),
  RE((9,5), C_ATTACKER_P, edge_style='dotted'),
  RE((2,5), C_ATTACKER_F, edge_style='dotted'),
  RE((7,5), C_ATTACKER_F, edge_style='dotted'),
]

r_e_case_uneven = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4), C_ATTACKER_F),
  RE((2,4)),
  RE((5,1), C_DEFENDER, highlight_width=h_width, highlight_color=h_color),
  RE((5,10), C_DEFENDER),
  RE((1,10), C_ATTACKER_P),
  RE((5,8), C_DEFENDER, highlight_width=h_width, highlight_color=h_color),
  RE((6,8), C_ATTACKER_F),
  RE((8,10), C_ATTACKER_P),
  RE((1,11)),
]
r_e_case_uneven_post = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4)),
  RE((2,4)),
  RE((4,10), C_ATTACKER_F, e_width),
  RE((5,10), C_DEFENDER),
  RE((1,10)),
  RE((6,10), C_ATTACKER_F, e_width),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]

r_e_case_two_one_flank = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((3,5), C_DEFENDER),
  RE((1,3), C_ATTACKER_P),
  RE((5,1), C_DEFENDER,  highlight_width=h_width, highlight_color=h_color),
  RE((6,11)),
  RE((1,6), C_ATTACKER_F),
  RE((6,10)),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]

r_e_case_even_many = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4), C_ATTACKER_F, highlight_width=h_width, highlight_color=h_color),
  RE((2,4)),
  RE((5,1), C_DEFENDER),
  RE((5,10), C_DEFENDER),
  RE((5,11), C_DEFENDER, highlight_width=h_width, highlight_color=h_color),
  RE((5,8), C_DEFENDER, highlight_width=h_width, highlight_color=h_color),
  RE((6,8), C_ATTACKER_F),
  RE((8,10), C_ATTACKER_P),
  RE((1,11), C_ATTACKER_P),
]
r_e_case_even_many_post = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((2,5), C_DEFENDER, e_width),
  RE((2,4), C_ATTACKER_F, e_width),
  RE((5,1), C_DEFENDER),
  RE((5,10), C_DEFENDER),
  RE((5,11), C_ATTACKER_P, e_width),
  RE((6,10), C_ATTACKER_F, e_width),
  RE((6,8)),
  RE((8,10)),
  RE((1,11)),
]

r_e_case_two_two_flank = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((1,4), C_ATTACKER_F, highlight_width=h_width, highlight_color=h_color),
  RE((1,3)),
  RE((5,11), C_DEFENDER,  highlight_width=h_width, highlight_color=h_color),
  RE((1,5), C_DEFENDER),
  RE((6,11), C_ATTACKER_F),
  RE((6,10)),
  RE((6,8)),
  RE((8,10)),
  RE((1,11), C_ATTACKER_P),
]
r_e_case_two_two_flank_post = [
  RE((4,6), C_HAPPY, edge_style='dashed'),
  RE((3,5), C_DEFENDER, e_width),
  RE((1,3), C_ATTACKER_P, e_width),
  RE((1,6), C_ATTACKER_F,  e_width),
  RE((1,5), C_DEFENDER),
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
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_uneven, 
  filename="MIS_termination_case_uneven",
  title=r"$T^d$",
  labels=labels
)
draw_polygon_triangulation(
  n,
  r_e_case_uneven_post, 
  filename="MIS_termination_case_uneven_post",
  title=r"$(T^d)'$",
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
  title=r"$(T^d)'$",
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
  title=r"$(T^d)'$",
  labels=labels
)