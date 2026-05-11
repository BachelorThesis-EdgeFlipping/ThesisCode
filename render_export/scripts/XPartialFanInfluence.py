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
  "O"
]

h_c_1 = Color.LIGHT_ORANGE
h_c_2 = Color.FAINT_LIGHT_GREEN


info_box = InfoBox(
  items=[
    InfoBoxItem("center edge", Color.BLUE),
    InfoBoxItem("right half", h_c_2, width=6),
    InfoBoxItem(r"$O$-fan \\ influence", h_c_1, width=6),
  ],
  loc="upper left",
  bbox_to_anchor=(-0.4, 1.12)
)

render_edges = [
  RE((1,10)),
  RE((6,10)),
  RE((7,10)),
  RE((1,7)),
  RE((2,7), Color.BLUE, width=3),
  RE((2,8)),
  RE((3,8)),
  RE((3,9))
]
color_faces = [
  #O-fan
  CF((0,1,10), h_c_1),
  CF((1,7,10), h_c_1),
  CF((6,7,10), h_c_1),
  CF((5,6,10), h_c_1),
  #untouched region
  CF((1,2,7), h_c_2),
  CF((2,7,8), h_c_2),
  CF((2,3,8), h_c_2),
  CF((3,8,9), h_c_2),
  CF((3,4,9), h_c_2),
]


draw_capped_channel_triangulation(
  n,
  render_edges, 
  filename="HE_partial_fan_influence",
  title=r"$T \in CH^O_5$",
  info_box=info_box,
  color_faces=color_faces,
  labels=labels
)

