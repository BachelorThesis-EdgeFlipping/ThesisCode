from dataclasses import dataclass
from typing_extensions import Literal
import matplotlib.pyplot as plt
import networkx as nx
import math
from render_export.Color import Color

#####################
# Types and Aliases #
#####################
LINE_STYLE = Literal["solid", "dashed", "dotted"]

#####################
#  Default Config   #
#####################
# Path
DEFAULT_EXPORT_PATH = "D:/BA/Obsidian/Bachelor Thesis/Data"
# Vertex
VERTEX_COLOR = Color.BLACK
VERTEX_RADIUS = 100
VERTEX_WIDTH = 2
VERTEX_FILL_COLOR = Color.WHITE
# Edge
EDGE_COLOR = Color.GRAY
EDGE_WIDTH = 2
EDGE_HIGHLIGHT_WIDTH = 12
EDGE_HIGHLIGHT_ALPHA = 0.2
# Figure
FIGSIZE = (4, 4)
BACKGROUND_COLOR = Color.INVISIBLE
# Label
SHOW_LABELS = False
LABEL_COLOR = Color.BLACK
LABEL_FONT_SIZE = 12

##################
# Data Classes   #
##################
@dataclass(init=False)
class RenderEdge:
  edge: tuple[int, int]
  color: Color 
  width: int
  highlight_color: Color 
  highlight_width: int 
  edge_style: LINE_STYLE
  def __init__(self, 
              edge, 
              color=EDGE_COLOR,
              width=EDGE_WIDTH,
              highlight_color=Color.INVISIBLE,
              highlight_width=EDGE_HIGHLIGHT_WIDTH,
              edge_style="solid",
              **kwargs):
    self.edge = edge
    self.color = kwargs.pop('c', color)
    self.width = kwargs.pop('w', width)
    self.highlight_color = kwargs.pop('hc', highlight_color)
    self.highlight_width = kwargs.pop('hw', highlight_width)
    self.edge_style = kwargs.pop('es', edge_style)

@dataclass
class ExtraVertex:
  #Placed at pct (0-1) along the line from edge[0] to edge[1]
  edge: tuple[int, int]
  pct: float
  label: int = -1  #assigned automatically

@dataclass
class FreeVertex:
  #Position in normalized coordinates (0-1)
  x: float
  y: float

##########################
# Internal Helpers       #
##########################
def _polygon_positions(order: int) -> dict[int, tuple[float, float]]:
  #Convex polygon vertex positions (0 = top, clockwise)
  pos = {}
  for i in range(order):
      angle = -math.pi / 2 + 2 * math.pi * i / order
      pos[i] = (math.cos(angle), -math.sin(angle))
  return pos

def _build_render_layers(G: nx.Graph, render_edges: list[RenderEdge]):
  #Separate graph edges into highlight and main drawing layers
  highlight_edges, highlight_colors, highlight_widths = [], [], []
  main_edges, main_colors, main_widths, main_styles = [], [], [], []
  for u, v in G.edges():
    r_edge = next((e for e in render_edges if e.edge == (u,v) or e.edge == (v,u)), None)
    if r_edge is None:
      main_edges.append((u,v))
      main_colors.append(EDGE_COLOR)
      main_widths.append(EDGE_WIDTH)
      main_styles.append("solid")
    else:
      #highlight layer
      if r_edge.highlight_color != Color.INVISIBLE:
        highlight_edges.append((u,v))
        highlight_colors.append(r_edge.highlight_color)
        highlight_widths.append(r_edge.highlight_width)
      #main layer
      main_edges.append((u,v))
      main_colors.append(r_edge.color)
      main_widths.append(r_edge.width)
      main_styles.append(r_edge.edge_style)
  return (highlight_edges, highlight_colors, highlight_widths,
          main_edges, main_colors, main_widths, main_styles)

def _draw_and_export(G: nx.Graph, pos: dict, render_edges: list[RenderEdge], filename: str):
  #Draw the graph and export as SVG
  hl_edges, hl_colors, hl_widths, m_edges, m_colors, m_widths, m_styles = _build_render_layers(G, render_edges)
  plt.figure(figsize=FIGSIZE, facecolor=BACKGROUND_COLOR.value)
  if hl_edges:
    nx.draw(G.edge_subgraph(hl_edges), pos,
        edge_color=[c.value for c in hl_colors],
        width=hl_widths,
        alpha=EDGE_HIGHLIGHT_ALPHA,
        node_size=0,
        with_labels=False)
  nx.draw(G.edge_subgraph(m_edges), pos,
      edge_color=[c.value for c in m_colors] ,
      width=m_widths,
      style=m_styles,
      node_size=0,
      with_labels=SHOW_LABELS)
  #Draw vertices as rings
  ax = plt.gca()
  xs = [pos[n][0] for n in G.nodes()]
  ys = [pos[n][1] for n in G.nodes()]
  ax.scatter(xs, ys, s=VERTEX_RADIUS, facecolors=VERTEX_FILL_COLOR.value, edgecolors=VERTEX_COLOR.value, linewidths=VERTEX_WIDTH, zorder=3)
  plt.axis('off')
  ax.set_aspect('equal', adjustable='datalim')
  export_path = f"{DEFAULT_EXPORT_PATH}/{filename}.svg"
  plt.savefig(export_path, format="svg", transparent=True, bbox_inches="tight")
  print(f"Exported figure to {export_path}.")
  plt.close()

#######################
# Rendering Interface #
#######################
def draw_polygon_triangulation(order: int, render_edges: list[RenderEdge], filename: str):
  #Triangulation of a convex polygon with diagonals
  G = nx.Graph()
  pos = _polygon_positions(order)
  G.add_nodes_from(range(order))
  border_edges = [(i, (i + 1) % order) for i in range(order)]
  G.add_edges_from(border_edges)
  G.add_edges_from([e.edge for e in render_edges])
  _draw_and_export(G, pos, render_edges, filename)

def draw_advanced_polygon_triangulation(order: int, extra_vertices: list[ExtraVertex], render_edges: list[RenderEdge], filename: str):
  #Polygon base with additional vertices placed along edges
  G = nx.Graph()
  pos = _polygon_positions(order)
  #Place extra vertices via linear interpolation
  next_label = order
  for ev in extra_vertices:
    u, v = ev.edge
    t = ev.pct
    x = pos[u][0] * (1 - t) + pos[v][0] * t
    y = pos[u][1] * (1 - t) + pos[v][1] * t
    ev.label = next_label
    pos[next_label] = (x, y)
    next_label += 1
  #Build graph
  G.add_nodes_from(pos.keys())
  border_edges = [(i, (i + 1) % order) for i in range(order)]
  G.add_edges_from(border_edges)
  G.add_edges_from([e.edge for e in render_edges])
  _draw_and_export(G, pos, render_edges, filename)

def draw_arbitrary_triangulation(vertices: list[FreeVertex], render_edges: list[RenderEdge], filename: str):
  #Fully free triangulation, all vertex positions and edges are manual
  #Vertex indices correspond to list order (0, 1, 2, ...)
  #No border edges are added automatically
  G = nx.Graph()
  pos = {}
  for i, v in enumerate(vertices):
      pos[i] = (v.x, 1.0 - v.y)
  G.add_nodes_from(pos.keys())
  G.add_edges_from([e.edge for e in render_edges])
  _draw_and_export(G, pos, render_edges, filename)