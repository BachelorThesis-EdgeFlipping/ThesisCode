from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

n = 12


C_HAPPY = Color.BLUE
he_width = 2

#maximaler spaghetti code xD
trans = 100
C_D1 = Color.L_0_0.make_transparent(trans)
C_D2 = Color.L_2_0.make_transparent(trans)
C_D3 = Color.L_6_0.make_transparent(trans) 
C_D4 = Color.from_tuple((170, 217, 0,trans)) #L5
C_D5 = Color.L_1_0.make_transparent(trans) 

info_box = InfoBox(
  items=[
    InfoBoxItem("happy edge", C_HAPPY)
  ],
  loc="upper left",
  bbox_to_anchor=(-0.06, 1)
)

r_e_source = [
  RE((1,3), C_HAPPY, he_width),
  RE((0,3)),
  RE((0,4)),
  RE((0,5)),
  RE((5,11), C_HAPPY, he_width),
  RE((6,11), C_HAPPY, he_width),
  RE((7,11)),
  RE((8,11), C_HAPPY, he_width),
  RE((9,11))
]
r_e_target = [
  RE((1,3), C_HAPPY, he_width),
  RE((1,11)),
  RE((3,11)),
  RE((3,5)),
  RE((5,11), C_HAPPY, he_width),
  RE((6,11), C_HAPPY, he_width),
  RE((6,8)),
  RE((8,11), C_HAPPY, he_width),
  RE((8,10))
]

color_faces_source = [
  CF((9,10,11), C_D1),
  CF((8,9,11), C_D1),

  CF((7,8,11), C_D2),
  CF((6,7,11), C_D2),

  CF((5,6,11), C_D3),

  CF((0,5,11), C_D4),
  CF((0,4,5), C_D4),
  CF((0,3,4), C_D4),
  CF((0,1,3), C_D4),

  CF((1,2,3), C_D5),
]
color_faces_target = [
  CF((9,10,8), C_D1),
  CF((8,10,11), C_D1),

  CF((7,8,6), C_D2),
  CF((6,8,11), C_D2),

  CF((5,6,11), C_D3),

  CF((0,1,11), C_D4),
  CF((1,3,11), C_D4),
  CF((3,5,11), C_D4),
  CF((3,4,5), C_D4),
  

  CF((1,2,3), C_D5),
]

edge_labels_decomp_source = [
  EL((1,2), "$T^d_{A,4}$", bg_color=C_D5),
  EL((0,11), "$T^d_{A,3}$", bg_color=C_D4),
  EL((5,6), "$T^d_{A,2}$", bg_color=C_D3),
  EL((7,8), "$T^d_{A,1}$", bg_color=C_D2),
  EL((9,10), "$T^d_{A,0}$", bg_color=C_D1)
]

edge_labels_decomp_target = [
  EL((1,2), "$T^d_{B,4}$", bg_color=C_D5),
  EL((0,11), "$T^d_{B,3}$", bg_color=C_D4),
  EL((5,6), "$T^d_{B,2}$", bg_color=C_D3),
  EL((7,8), "$T^d_{B,1}$", bg_color=C_D2),
  EL((9,10), "$T^d_{B,0}$", bg_color=C_D1)
]


draw_polygon_triangulation(
  n,
  r_e_source, 
  filename="MIS_decomposition_source_default",
  title=r"$T_A$",
  info_box=info_box,
)
draw_polygon_triangulation(
  n,
  r_e_target, 
  filename="MIS_decomposition_target_default",
  title=r"$T_B$",
)


draw_polygon_triangulation(
  n,
  r_e_source, 
  filename="MIS_decomposition_source_decomp",
  #title=r"$\mathcal{D}_{T_T}(T_i)$",
  color_faces=color_faces_source,
  edge_labels=edge_labels_decomp_source
)
draw_polygon_triangulation(
  n,
  r_e_target, 
  filename="MIS_decomposition_target_decomp",
  #title=r"$\mathcal{D}_{T_i}(T_T)$",
  color_faces=color_faces_target,
  edge_labels=edge_labels_decomp_target
)