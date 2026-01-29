from abc import ABC, abstractmethod
from pygame.math import Vector2
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from SyncNetwork import Syncable
from frontend.Gobals import Color, DEFAULT_FONT
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable
from frontend.renderers.RenderPos import RenderPos


T = TypeVar('T', bound='Interactable')
@dataclass
class Interactable(Generic[T]):
  reference: T
  pos: RenderPos
  size: RenderPos
  

class Renderer(ABC):

  #default styling settings
  OUTLINE_COLOR = Color.BLACK
  OUTLINE_WIDTH = 2
  TITLE_FONT = DEFAULT_FONT
  TITLE_COLOR = Color.BLACK

  def __init__(self, 
              content: 'Syncable',
              anchor: Vector2, 
              bounds: Vector2, 
              title: str = "",
              title_font: pygame.font.Font = TITLE_FONT,
              title_color: Color = TITLE_COLOR,
              margin: Vector2 = Vector2(0,0),
              internal_content_padding = Vector2(0,0),
              fill: bool = False, 
              stretch: bool = True,
              outline: bool = True, 
              outline_color: Color = OUTLINE_COLOR,
              outline_width: int = OUTLINE_WIDTH):
    self.content: Syncable = content
    self.title = title
    self.title_font = title_font
    self.title_color = title_color
    self.anchor = anchor
    self.bounds = bounds
    self.fill = fill
    self.stretch = stretch
    self.content_anchor = anchor + margin + internal_content_padding
    self.content_bounds = self.bounds - margin * 2 - internal_content_padding * 2
    self.outline_rect = None
    self.outline_color = outline_color
    self.outline_width = outline_width
    self.outline_rect = pygame.Rect(anchor.x, anchor.y, bounds.x, bounds.y)
    
  def _post_init(self):
    self.content_size = self._get_content_size()
    self.content_scale = self._calculate_content_scale()


  @abstractmethod
  def render(self, screen: pygame.Surface):
    if self.outline_rect:
      pygame.draw.rect(screen, self.outline_color.value, self.outline_rect, self.outline_width)
    if self.title:
      title_surface = self.title_font.render(self.title, True, self.title_color.value)
      title_x = self.anchor.x + (self.bounds.x - title_surface.get_width()) // 2
      title_y = self.anchor.y - title_surface.get_height() - 5 #5 pixels padding
      screen.blit(title_surface, (title_x, title_y))


  @abstractmethod
  def update_content(self):
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
  def _project_position(self, pos: Vector2) -> RenderPos:
    #content scaling and anchoring
    pos = (pos.elementwise() * self.content_scale) + self.content_anchor
    #convert to tuple for pygame
    projected_pos_t: RenderPos = RenderPos.from_vector2(pos)
    return projected_pos_t
  
  @abstractmethod
  def get_interables(self) -> list[Interactable]:
    pass