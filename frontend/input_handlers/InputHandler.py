from abc import ABC, abstractmethod

import pygame

from frontend.renderers.Renderer import Renderer

class InputHandler(ABC):

  def __init__(self, renderer: Renderer):
    self.renderer = renderer

  @abstractmethod
  def handle_event(self, event: any):
    if(event.type == pygame.MOUSEBUTTONDOWN):
      if(not self.renderer.outline_rect.collidepoint(event.pos)):
        self._on_unfocus()
    pass

  @abstractmethod
  def _on_unfocus(self):
    pass