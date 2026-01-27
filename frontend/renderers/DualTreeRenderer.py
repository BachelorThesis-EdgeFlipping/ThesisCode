from .Renderer import Renderer
from data_structures.DualTree import DualTree, Node
import pygame
from pygame.math import Vector2
from frontend.Gobals import Color, DEFAULT_FONT

class RenderNode: 
  def __init__(self, node: Node, position: Vector2):
    self.node = node
    self.position = position

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
    self._nodes_buffer = []
    self._post_init()

  def render(self, screen: pygame.Surface):
    super().render(screen)
    self._global_node_index = 0
    self._nodes_buffer = []
    self._render_node(self.content.root, 0, screen)

  def _render_node(self, node: Node, cur_depth: int, screen: pygame.Surface) -> tuple[int,int]:
    if node is None:
      return
    #recursion left
    left_pos =self._render_node(node.left, cur_depth + 1, screen)
    #compute position
    x = (self.content_size.x / (self._nodes_count + 1)) * (self._global_node_index + 1)
    y = (self.content_size.y / (self._max_depth + 2)) * (cur_depth + 1)
    pos = self._project_position(Vector2(x, y))
    #increment global index
    self._global_node_index += 1
    #recursion right
    right_pos = self._render_node(node.right, cur_depth + 1, screen)
    #render edges
    if left_pos:
      pygame.draw.line(screen, self.edge_color.value, pos, left_pos, self.edge_width)
    if right_pos:
      pygame.draw.line(screen, self.edge_color.value, pos, right_pos, self.edge_width)
    #render node
    pygame.draw.circle(screen, self.node_color.value, pos, self.node_radius)
    img = self.font.render(str(node.face.id), True, Color.WHITE.value)
    screen.blit(img, (pos[0] - img.get_width() // 2, pos[1] - img.get_height() // 2))
    return pos

  def _get_content_size(self) -> Vector2:
    return self.content_bounds
  
  def update_content(self, content: DualTree):
    super().update_content(content)
    self._nodes_count = self.content.node_count
    self._max_depth = self.content.depth
  
  def _project_position(self, pos):
    return super()._project_position(pos)