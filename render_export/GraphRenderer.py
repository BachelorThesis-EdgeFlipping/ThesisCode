from dataclasses import dataclass
from typing_extensions import Literal
import matplotlib.pyplot as plt
import networkx as nx
import math
from render_export.Color import Color
from render_export.Globals import DEFAULT_EXPORT_PATH

#####################
# Types and Aliases #
#####################
LINE_STYLE = Literal["solid", "dashed", "dotted"]

#####################
#  Default Config   #
#####################
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

# AX
AX_MARGIN = 0.15
# Vertex
VERTEX_COLOR = Color.BLACK
VERTEX_RADIUS = 30
VERTEX_WIDTH = 1
VERTEX_FILL_COLOR = Color.WHITE
# Edge
EDGE_COLOR = Color.BLACK
EDGE_WIDTH = 1
EDGE_HIGHLIGHT_WIDTH = 12
EDGE_HIGHLIGHT_ALPHA = 0.2
# Figure
FIGSIZE = (4, 4)
BACKGROUND_COLOR = Color.INVISIBLE
TITLE_BACKGROUND_COLOR = Color.LIGHT_GRAY
TITLE_FONT_FAMILY = "serif"
# Channel
CHANNEL_ARCH_FACTOR = 0.12
# Label
SHOW_LABELS = False
LABEL_COLOR = Color.BLACK
LABEL_FONT_SIZE = 12
LABEL_FONT_FAMILY = "serif"
LABEL_OFFSET = 0.2

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
  bg_color: Color
  bg_width: int
  def __init__(self, 
              edge, 
              color=EDGE_COLOR,
              width=EDGE_WIDTH,
              highlight_color=Color.INVISIBLE,
              highlight_width=EDGE_HIGHLIGHT_WIDTH,
              edge_style="solid",
              bg_color=Color.INVISIBLE,
              bg_width=EDGE_WIDTH,
              **kwargs):
    self.edge = edge
    self.color = kwargs.pop('c', color)
    self.width = kwargs.pop('w', width)
    self.highlight_color = kwargs.pop('hc', highlight_color)
    self.highlight_width = kwargs.pop('hw', highlight_width)
    self.edge_style = kwargs.pop('es', edge_style)
    self.bg_color = kwargs.pop('bgc', bg_color)
    self.bg_width = kwargs.pop('bgw', bg_width)

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

@dataclass
class ColorFace:
  vertices: tuple[int,int,int]
  color: Color

@dataclass
class ColorVertex:
  vertex: int
  color: Color

@dataclass
class EdgeLabel:
  edge: tuple[int, int]
  label: str
  color: Color = LABEL_COLOR
  bg_color: Color = Color.INVISIBLE
  offset: float = LABEL_OFFSET

@dataclass
class InfoBoxItem:
  label: str
  color: Color
  edge_style: LINE_STYLE = "solid"
  width: int = EDGE_WIDTH

@dataclass
class InfoBox:
  items: list[InfoBoxItem]
  loc: str = "best"
  title: str = None
  bbox_to_anchor: tuple[float, float] = None

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

def _channel_positions(n: int) -> dict[int, tuple[float, float]]:
  # Channel vertex positions: n top vertices, n bottom vertices
  pos = {}
  for i in range(n):
      x = -1.0 + (2.0 * i / (n - 1)) if n > 1 else 0.0
      top_arc = CHANNEL_ARCH_FACTOR * (x**2)        # U-shape (bend downwards / concave)
      bottom_arc = -CHANNEL_ARCH_FACTOR * (x**2)    # Cap-shape (bend upwards / convex)
      
      pos[i] = (x, 0.6 + top_arc)       # Top line
      pos[n + i] = (x, -0.6 + bottom_arc)   # Bottom line
  return pos

def _build_render_layers(G: nx.Graph, render_edges: list[RenderEdge]):
  #Separate graph edges into highlight and main drawing layers
  highlight_edges, highlight_colors, highlight_widths = [], [], []
  bg_edges, bg_colors, bg_widths = [], [], []
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
      #bg layer
      if r_edge.bg_color != Color.INVISIBLE:
        bg_edges.append((u,v))
        bg_colors.append(r_edge.bg_color)
        bg_widths.append(r_edge.bg_width)
      #main layer
      main_edges.append((u,v))
      main_colors.append(r_edge.color)
      main_widths.append(r_edge.width)
      main_styles.append(r_edge.edge_style)
  return (highlight_edges, highlight_colors, highlight_widths,
          bg_edges, bg_colors, bg_widths,
          main_edges, main_colors, main_widths, main_styles)

def _calculate_label_positions(G: nx.Graph, pos: dict, border_edges: list[tuple[int, int]] = None) -> dict:
  label_pos = {}
  
  cx = sum(p[0] for p in pos.values()) / len(pos)
  cy = sum(p[1] for p in pos.values()) / len(pos)
  
  border_G = nx.Graph()
  if border_edges:
    border_G.add_edges_from(border_edges)
  else:
    border_G = G

  for node in G.nodes():
    neighbors = list(border_G.neighbors(node)) if node in border_G else []
    if not neighbors:
      neighbors = list(G.neighbors(node))
      
    if not neighbors:
      label_pos[node] = (pos[node][0], pos[node][1] + LABEL_OFFSET)
      continue
    
    vx, vy = 0.0, 0.0
    for nbr in neighbors:
      dx = pos[nbr][0] - pos[node][0]
      dy = pos[nbr][1] - pos[node][1]
      length = math.hypot(dx, dy)
      if length > 1e-5:
        vx += dx / length
        vy += dy / length
    
    length = math.hypot(vx, vy)
    if length < 1e-5:
      bx = pos[node][0] - cx
      by = pos[node][1] - cy
    else:
      bx, by = vx, vy
      
    # Ensure the vector points outwards away from the centroid
    out_x = pos[node][0] - cx
    out_y = pos[node][1] - cy
    if (bx * out_x + by * out_y) < 0:
      bx, by = -bx, -by
      
    length_b = math.hypot(bx, by)
    if length_b > 1e-5:
      bx /= length_b
      by /= length_b
    else:
      bx, by = 0, 1
      
    label_pos[node] = (pos[node][0] + bx * LABEL_OFFSET,
                       pos[node][1] + by * LABEL_OFFSET)
  return label_pos

def _draw_and_export(G: nx.Graph, pos: dict, render_edges: list[RenderEdge], color_faces: list[ColorFace], filename: str, labels: list[str] = None, border_edges: list[tuple[int, int]] = None, color_vertices: list[ColorVertex] = None, info_box: InfoBox = None, title: str = None, margin: float = AX_MARGIN, edge_labels: list[EdgeLabel] = None):
  labels_dict = {i: str(labels[i]) for i in range(min(len(labels), len(pos)))} if labels is not None else None
  
  #Draw the graph and export as SVG
  hl_edges, hl_colors, hl_widths, bg_edges, bg_colors, bg_widths, m_edges, m_colors, m_widths, m_styles = _build_render_layers(G, render_edges)
  plt.figure(figsize=FIGSIZE, facecolor=BACKGROUND_COLOR.value_normalized())
  
  if title:
    plt.title(title, loc='center', fontfamily=TITLE_FONT_FAMILY, bbox=dict(boxstyle="round,pad=0.3", facecolor=TITLE_BACKGROUND_COLOR.value_normalized(), edgecolor='none', alpha=0.5))
  if color_faces:
    ax = plt.gca()
    for cf in color_faces:
      if len(cf.vertices) == 3:
        triangle = plt.Polygon([pos[v] for v in cf.vertices], color=cf.color.value_normalized(), zorder=1)
        ax.add_patch(triangle)
  if hl_edges:
    hl_col = nx.draw_networkx_edges(G, pos,
        edgelist=hl_edges,
        edge_color=[c.value_normalized() for c in hl_colors],
        width=hl_widths,
        alpha=EDGE_HIGHLIGHT_ALPHA,
        node_size=0)
    if hl_col:
        if isinstance(hl_col, list):
            for c in hl_col:
                c.set_zorder(2)
        else:
            hl_col.set_zorder(2)

  if bg_edges:
    bg_col = nx.draw_networkx_edges(G, pos,
        edgelist=bg_edges,
        edge_color=[c.value_normalized() for c in bg_colors],
        width=bg_widths,
        style="solid",
        node_size=0)
    if bg_col:
        if isinstance(bg_col, list):
            for c in bg_col:
                c.set_zorder(2)
        else:
            bg_col.set_zorder(2)

  # Draw main edges without inline labels
  m_col = nx.draw_networkx_edges(G, pos,
      edgelist=m_edges,
      edge_color=[c.value_normalized() for c in m_colors],
      width=m_widths,
      style=m_styles,
      node_size=0)
  if m_col:
      if isinstance(m_col, list):
          for c in m_col:
              c.set_zorder(3)
      else:
          m_col.set_zorder(3)
  # Draw labels using calculated free space
  should_draw_labels = SHOW_LABELS if labels is None else True
  if should_draw_labels and labels_dict:
    label_pos = _calculate_label_positions(G, pos, border_edges)
    nx.draw_networkx_labels(G, label_pos,
        labels=labels_dict,
        font_size=LABEL_FONT_SIZE,
        font_family=LABEL_FONT_FAMILY,
        font_color=LABEL_COLOR.value_normalized())

  #Draw vertices as rings
  ax = plt.gca()
  xs = [pos[n][0] for n in G.nodes()]
  ys = [pos[n][1] for n in G.nodes()]
  
  vertex_facecolors = [VERTEX_FILL_COLOR.value_normalized() for _ in G.nodes()]
  if color_vertices:
    cv_dict = {cv.vertex: cv.color.value_normalized() for cv in color_vertices}
    for i, n in enumerate(G.nodes()):
      if n in cv_dict:
        vertex_facecolors[i] = cv_dict[n]

  ax.scatter(xs, ys, s=VERTEX_RADIUS, facecolors=vertex_facecolors, edgecolors=VERTEX_COLOR.value_normalized(), linewidths=VERTEX_WIDTH, zorder=3)
  plt.axis('off')
  
  # explicitly set axis limits independent of drawn lines to ensure consistent sizing across plots
  min_x, max_x = min(xs), max(xs)
  min_y, max_y = min(ys), max(ys)
  dx = max_x - min_x if max_x > min_x else 1.0
  dy = max_y - min_y if max_y > min_y else 1.0
  ax.set_xlim(min_x - margin * dx, max_x + margin * dx)
  ax.set_ylim(min_y - margin * dy, max_y + margin * dy)
  
  ax.set_aspect('equal', adjustable='box')
  
  if info_box:
    import matplotlib.lines as mlines
    legend_handles = []
    for item in info_box.items:
      handle = mlines.Line2D([], [], color=item.color.value_normalized(), 
                             linewidth=item.width, linestyle=item.edge_style, 
                             label=item.label)
      legend_handles.append(handle)
    
    legend_kwargs = {'loc': info_box.loc}
    if info_box.title is not None:
      legend_kwargs['title'] = info_box.title
    if info_box.bbox_to_anchor is not None:
      legend_kwargs['bbox_to_anchor'] = info_box.bbox_to_anchor
    ax.legend(handles=legend_handles, **legend_kwargs)

  if edge_labels:
    cx = sum(p[0] for p in pos.values()) / len(pos)
    cy = sum(p[1] for p in pos.values()) / len(pos)
    for el in edge_labels:
      u, v = el.edge
      if u not in pos or v not in pos:
        continue
      mx = (pos[u][0] + pos[v][0]) / 2.0
      my = (pos[u][1] + pos[v][1]) / 2.0
      
      out_x = mx - cx
      out_y = my - cy
      length = math.hypot(out_x, out_y)
      if length > 1e-5:
        out_x /= length
        out_y /= length
      else:
        out_x, out_y = 0, 1
      
      lx = mx + out_x * el.offset
      ly = my + out_y * el.offset
      
      bbox = None
      if el.bg_color != Color.INVISIBLE:
         bbox = dict(boxstyle="round,pad=0.2", facecolor=el.bg_color.value_normalized(), edgecolor='none')
         
      plt.text(lx, ly, el.label, color=el.color.value_normalized(), fontsize=LABEL_FONT_SIZE, fontfamily=LABEL_FONT_FAMILY, ha='center', va='center', bbox=bbox, zorder=5)

  # Remove from limits computation from graph print
  # print(f"{filename} limits: x={ax.get_xlim()} y={ax.get_ylim()}")
  export_path = f"{DEFAULT_EXPORT_PATH}/{filename}.svg"
  plt.savefig(export_path, format="svg", transparent=True, bbox_inches="tight")
  print(f"Exported figure to {export_path}.")
  plt.close()

# Rendering Interface #
#######################
def draw_channel_triangulation(n: int, render_edges: list[RenderEdge], filename: str, color_faces: list[ColorFace] = None, labels: list[str] = None, color_vertices: list[ColorVertex] = None, info_box: InfoBox = None, title: str = None, draw_border: bool = True, margin: float = AX_MARGIN, edge_labels: list[EdgeLabel] = None):
  # Channel triangulation with n vertices at the top and n at the bottom
  G = nx.Graph()
  pos = _channel_positions(n)
      
  G.add_nodes_from(pos.keys())
  
  border_edges = []
  if n > 1:
      # Top border 0 to n-1
      border_edges.extend([(i, i + 1) for i in range(n - 1)])
      # Bottom border n to 2n-1
      border_edges.extend([(n + i, n + i + 1) for i in range(n - 1)])
      # Side borders
      border_edges.append((0, n))
      border_edges.append((n - 1, 2 * n - 1))
      
  if draw_border:
    G.add_edges_from(border_edges)
  G.add_edges_from([e.edge for e in render_edges])
  _draw_and_export(G, pos, render_edges, color_faces, filename, labels=labels, border_edges=border_edges, color_vertices=color_vertices, info_box=info_box, title=title, margin=margin, edge_labels=edge_labels)

def draw_capped_channel_triangulation(n: int, render_edges: list[RenderEdge], filename: str, color_faces: list[ColorFace] = None, labels: list[str] = None, color_vertices: list[ColorVertex] = None, info_box: InfoBox = None, title: str = None, draw_border: bool = True, margin: float = AX_MARGIN, edge_labels: list[EdgeLabel] = None):
  # Capped channel triangulation with n vertices at the top and n at the bottom, plus a left cap vertex
  G = nx.Graph()
  pos = _channel_positions(n)
  
  cap_idx = 2 * n
  left_x = pos[0][0]
  mid_y = (pos[0][1] + pos[n][1]) / 2.0
  # Placing cap slightly to the left, but closer than before
  offset = 0.3
  pos[cap_idx] = (left_x - offset, mid_y)
      
  G.add_nodes_from(pos.keys())
  
  border_edges = []
  if n > 1:
      # Top border 0 to n-1
      border_edges.extend([(i, i + 1) for i in range(n - 1)])
      # Bottom border n to 2n-1
      border_edges.extend([(n + i, n + i + 1) for i in range(n - 1)])
      # Right Side border
      border_edges.append((n - 1, 2 * n - 1))
      
  # Left Cap borders
  border_edges.append((cap_idx, 0))
  border_edges.append((cap_idx, n))
      
  if draw_border:
    G.add_edges_from(border_edges)
  G.add_edges_from([e.edge for e in render_edges])
  _draw_and_export(G, pos, render_edges, color_faces, filename, labels=labels, border_edges=border_edges, color_vertices=color_vertices, info_box=info_box, title=title, margin=margin, edge_labels=edge_labels)

def draw_polygon_triangulation(order: int, render_edges: list[RenderEdge], filename: str, color_faces: list[ColorFace] = None, labels: list[str] = None, color_vertices: list[ColorVertex] = None, info_box: InfoBox = None, title: str = None, draw_border: bool = True, margin: float = AX_MARGIN, edge_labels: list[EdgeLabel] = None):
  #Triangulation of a convex polygon with diagonals
  G = nx.Graph()
  pos = _polygon_positions(order)
  G.add_nodes_from(range(order))
  border_edges = [(i, (i + 1) % order) for i in range(order)]
  if draw_border:
    G.add_edges_from(border_edges)
  G.add_edges_from([e.edge for e in render_edges])
  _draw_and_export(G, pos, render_edges, color_faces, filename, labels=labels, border_edges=border_edges, color_vertices=color_vertices, info_box=info_box, title=title, margin=margin, edge_labels=edge_labels)

def draw_advanced_polygon_triangulation(order: int, extra_vertices: list[ExtraVertex], render_edges: list[RenderEdge], filename: str, color_faces: list[ColorFace] = None, labels: list[str] = None, color_vertices: list[ColorVertex] = None, info_box: InfoBox = None, title: str = None, margin: float = AX_MARGIN, edge_labels: list[EdgeLabel] = None):
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
  _draw_and_export(G, pos, render_edges, color_faces, filename, labels=labels, border_edges=border_edges, color_vertices=color_vertices, info_box=info_box, title=title, margin=margin, edge_labels=edge_labels)

def draw_arbitrary_triangulation(vertices: list[FreeVertex], render_edges: list[RenderEdge], filename: str, color_faces: list[ColorFace] = None, labels: list[str] = None, color_vertices: list[ColorVertex] = None, info_box: InfoBox = None, title: str = None, edge_labels: list[EdgeLabel] = None):
  #Fully free triangulation, all vertex positions and edges are manual
  #Vertex indices correspond to list order (0, 1, 2, ...)
  #No border edges are added automatically
  G = nx.Graph()
  pos = {}
  for i, v in enumerate(vertices):
      pos[i] = (v.x, 1.0 - v.y)
  G.add_nodes_from(pos.keys())
  G.add_edges_from([e.edge for e in render_edges])
  _draw_and_export(G, pos, render_edges, color_faces, filename, labels=labels, color_vertices=color_vertices, info_box=info_box, title=title, edge_labels=edge_labels)