from frontend.renderers.RenderPos import RenderPos
from .Renderer import Interactable, Renderer
from data_structures.DualTree import DualTree, Node
import pygame
from pygame.math import Vector2
from frontend.Gobals import Color, DEFAULT_FONT

class RenderNode: 
  def __init__(self, node: Node, position: Vector2):
    self.node: Node = node
    self.position: Vector2 = position #center possition
class RenderEdge:
  def __init__(self, from_node: RenderNode, to_node: RenderNode):
    self.from_node = from_node
    self.to_node = to_node

class DualTreeRenderer(Renderer):

  #default styling settings
  NODE_RADIUS = 16
  NODE_COLOR = Color.GRAY
  EDGE_WIDTH = 2
  EDGE_COLOR = Color.PURPLE
  FONT = DEFAULT_FONT

  def __init__(self, 
              content: DualTree, 
              node_radius: int = NODE_RADIUS,
              node_color: Color = NODE_COLOR,
              edge_width: int = EDGE_WIDTH,
              edge_color: Color = EDGE_COLOR,
              font: pygame.font.Font = FONT,
              **kwargs):
    kwargs['fill'] = True
    kwargs['stretch'] = True
    super().__init__(
      content,
      title = "Dual Tree",
      internal_content_padding = Vector2(node_radius, node_radius),
      **kwargs)
    self.node_radius = node_radius
    self.node_color = node_color
    self.edge_width = edge_width
    self.edge_color = edge_color
    self.font = font
    #rendering meta-data
    self._nodes_count = self.content.node_count
    self._max_depth = self.content.depth
    self._global_node_index = 0
    #Render Cache
    self._render_nodes: list[RenderNode] = []
    self._render_edges: list[RenderEdge] = []
    self._post_init()

  def _post_init(self):
    super()._post_init()
    self._calculate_dual_tree()

  def _calculate_dual_tree(self):
    self._global_node_index = 0
    self._render_nodes = []
    self._render_edges = []
    self._calculate_node(self.content.root, 0)

  def _calculate_node(self, node: Node, cur_depth: int) -> RenderNode:
    if node is None:
      return
    #recursion left
    left_render_node: RenderNode =self._calculate_node(node.left, cur_depth + 1)
    #compute position
    x = (self.content_size.x / (self._nodes_count + 1)) * (self._global_node_index + 1)
    y = (self.content_size.y / (self._max_depth + 1)) * cur_depth
    pos = Vector2(x, y)
    #increment global index
    self._global_node_index += 1
    #recursion right
    right_render_node: RenderNode = self._calculate_node(node.right, cur_depth + 1)
    #add render node
    render_node = RenderNode(node, pos)
    self._render_nodes.append(render_node)
    #add render edge
    if left_render_node:
      self._render_edges.append(RenderEdge(render_node, left_render_node))
    if right_render_node:
      self._render_edges.append(RenderEdge(render_node, right_render_node))
    return render_node

  def render(self, screen: pygame.Surface):
    super().render(screen)
    for edge in self._render_edges:
      from_pos: RenderPos = self._project_position(edge.from_node.position)
      to_pos: RenderPos = self._project_position(edge.to_node.position)
      pygame.draw.line(screen, self.edge_color.value, from_pos.tuple(), to_pos.tuple(), self.edge_width)
    for render_node in self._render_nodes:
      pos: RenderPos = self._project_position(render_node.position)
      pygame.draw.circle(screen, self.node_color.value, pos.tuple(), self.node_radius)
      img = self.font.render(str(render_node.node.face.id), True, Color.WHITE.value)
      screen.blit(img, (pos.x - img.get_width() // 2, pos.y - img.get_height() // 2))

  def _get_content_size(self) -> Vector2:
    return self.content_bounds
  
  def update_content(self):
    super().update_content()
    self._nodes_count = self.content.node_count
    self._max_depth = self.content.depth
    self._calculate_dual_tree()
  
  def _project_position(self, pos):
    return super()._project_position(pos)
  
  def get_interables(self) -> list[Interactable[Node]]:
    interactables: list[Interactable[Node]] = []
    for render_node in self._render_nodes:
      pos: RenderPos = self._project_position(render_node.position) - RenderPos.square_from_int(self.node_radius)
      size: RenderPos = RenderPos.square_from_int(self.node_radius * 2)
      interactables.append(Interactable(render_node.node, pos, size))
    return interactables