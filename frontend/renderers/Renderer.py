from abc import ABC, abstractmethod
from pygame.math import Vector2
import pygame
from frontend.Gobals import Color

class Renderer(ABC):
  def __init__(self, 
              content: any,
              anchor: Vector2, 
              bounds: Vector2, 
              margin: Vector2 = Vector2(0,0),
              internal_content_padding = Vector2(0,0),
              fill: bool = False, 
              stretch: bool = True,
              outline: bool = True, 
              outline_color: Color = Color.BLACK,
              outline_width: int = 2):
    self.content = content
    self.anchor = anchor
    self.bounds = bounds
    self.fill = fill
    self.stretch = stretch
    self.content_anchor = anchor + margin + internal_content_padding
    self.content_bounds = self.bounds - margin * 2 - internal_content_padding * 2
    self.outline_rect = None
    self.outline_color = outline_color
    self.outline_width = outline_width
    if outline and outline_width > 0:
      self.outline_rect = pygame.Rect(anchor.x, anchor.y, bounds.x, bounds.y)
    
  def _post_init(self):
    self.content_size = self._get_content_size()
    self.content_scale = self._calculate_content_scale()


  @abstractmethod
  def render(self, screen: pygame.Surface):
    if self.outline_rect:
      pygame.draw.rect(screen, self.outline_color.value, self.outline_rect, self.outline_width)

  @abstractmethod
  def update_content(self, content: any):
    self.content = content
    self.content_size = self._get_content_size()
    self.content_scale = self._calculate_content_scale()

  @abstractmethod
  def _get_content_size(self) -> Vector2:
    pass

  def _calculate_content_scale(self) -> Vector2:
    content_scale: Vector2 = Vector2(1,1)
    dimensions = Vector2(self.content_bounds.x / self.content_size.x, self.content_bounds.y / self.content_size.y)
    if self.fill:
      if self.stretch:
        content_scale = dimensions
      else: 
        min_dimension = min(dimensions.x, dimensions.y)
        content_scale = Vector2(min_dimension, min_dimension)
    return content_scale
  
  @abstractmethod
  def _project_position(self, pos: Vector2) -> tuple[int,int]:
    #content scaling and anchoring
    pos = (pos.elementwise() * self.content_scale) + self.content_anchor
    #convert to tuple for pygame
    projected_pos_t = (int(pos.x), int(pos.y))
    return projected_pos_t