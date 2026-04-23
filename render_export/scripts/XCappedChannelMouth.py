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

render_edges = [
  RE((2*n, 1)),
  RE((2*n, 2)),
  RE((2*n, 3)),
  RE((2*n, 4), Color.BLUE),
  RE((2*n, n+1)),
  RE((2*n, n+2), Color.ORANGE),

  RE((n-1, n+2)),
  RE((n-1, n+3)),
]

draw_capped_channel_triangulation(n, render_edges, filename="HE_mouth_edges", labels=labels)
