from render_export.GraphRenderer import *
from render_export.Color import Color
from render_export.Aliases import *

m = 3

labels = [
  r"$A_{i-1}$",
  r"$A_i$",
  r"$A{i+1}$",
  r"$B_{j-1}$",
  r"$B_j$",
  r"$B_{j+1}$",
]

C_CON1 = Color.MAGENTA
C_CON2 = Color.GREEN
C_CENTER = Color.BLUE

render_edges = [
  RE((0,1), C_CON1),
  RE((4,5), C_CON1),
  RE((0,4), C_CON1),
  RE((1,5), C_CON1),
  
  RE((1,4), C_CENTER, width=2),

  RE((3,4), C_CON2),
  RE((1,2), C_CON2),
  RE((1,3), C_CON2),
  RE((2,4), C_CON2),
]


draw_channel_triangulation(m, render_edges, filename="HE_oberservation_flippable" , labels=labels, draw_border=False)