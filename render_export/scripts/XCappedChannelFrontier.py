from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

n = 5

info_box = InfoBox(
  items=[
    InfoBoxItem(r"$A_{i'}B_{j'}$ (frontier edge)",Color.BLUE),
    InfoBoxItem(r"$A_{i''}B_{j''}$",Color.ORANGE),
  ],
  loc="upper left",
  bbox_to_anchor=(-0.48, 1.12)
)

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

render_edges = [
  RE((0,2*n-1)),
  RE((1,2*n-1)),
  RE((2,2*n-1)),
  RE((3,2*n-1)),

  RE((0,2*n-2), Color.ORANGE),
  RE((0,2*n-3), Color.BLUE),
  RE((2*n, n+1)),
  RE((2*n, n+2))
]


color_vertices_1 = [
  CV(0, Color.LIGHT_BLUE),
  CV(2*n-3, Color.LIGHT_BLUE),
  CV(0, Color.LIGHT_ORANGE),
  CV(2*n-2, Color.LIGHT_ORANGE),
]


draw_capped_channel_triangulation(n, render_edges, info_box=info_box, filename="HE_frontier_edge_1", title=r"$T \in CH^O_5$", labels=labels)
