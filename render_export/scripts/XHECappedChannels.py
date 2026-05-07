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
  "$B_1$", #5
  "$B_2$",
  "$B_3$",
  "$B_4$",
  "$B_5$",
  "O"     #10
]


render_edges_left_inclined = [
  RE((0,9)),
  RE((0,8)),
  RE((0,7)),
  RE((0,6)),
  RE((0,5)),
  RE((1,9)),
  RE((2,9)),
  RE((3,9)),
  RE((4,9)),

]

render_edges_canonical = [
  RE((1,10)),
  RE((2,10)),
  RE((3,10)),
  RE((4,10)),
  RE((6,10)),
  RE((7,10)),
  RE((8,10)),
  RE((9,10)),
]



draw_capped_channel_triangulation(n, render_edges_canonical, title=r"$CC_5^O$" ,filename="HE_canonical_channel", labels=labels)
draw_capped_channel_triangulation(n, render_edges_left_inclined, title=r"$CH_5^{L,O}$" ,filename="HE_capped_left_inclined", labels=labels)
