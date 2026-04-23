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

render_edges_1 = [
  RE((0,n+1)),
  RE((0,n+2)),
  RE((0,n+3)),
  RE((0,n+4)),
  RE((1,n+4)),
  RE((2,n+4)),
  RE((3,n+4)),
  RE((4,n+4)),
]
color_faces_1 = [
  CF((0,1,n+4), Color.LIGHT_ORANGE),
  CF((0,n+3,n+4), Color.LIGHT_PURPLE)
]
color_vertices_1 = [
  CV(n+4, Color.LIGHT_ORANGE),
  CV(0, Color.LIGHT_PURPLE),
]


render_edges_2 = [
  RE((0,n+1)),
  RE((0,n+2)),
  RE((0,n+3)),
  RE((1,n+3)),
  RE((1,n+4)),
  RE((2,n+4)),
  RE((3,n+4)),
  RE((4,n+4)),
]
color_faces_2 = [
  CF((0,1,n+3), Color.LIGHT_ORANGE),
  CF((1,n+3,n+4), Color.LIGHT_PURPLE)
]
color_vertices_2 = [
  CV(n+3, Color.LIGHT_ORANGE),
  CV(1, Color.LIGHT_PURPLE),
]


draw_channel_triangulation(n, render_edges_1, filename="HE_progress_flip_1", color_faces=color_faces_1, color_vertices=color_vertices_1, labels=labels)
draw_channel_triangulation(n, render_edges_2, filename="HE_progress_flip_2", color_faces=color_faces_2, color_vertices=color_vertices_2, labels=labels)
#exec: python -m 
