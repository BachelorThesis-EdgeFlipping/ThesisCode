from abc import ABC, abstractmethod

import pygame

import SyncNetwork
from frontend.renderers.Renderer import Renderer

class InputHandler(ABC):

  def __init__(self, renderer: Renderer, sync_network: 'SyncNetwork' = None):
    self.renderer = renderer
    self.sync_network = sync_network

  @abstractmethod
  def handle_event(self, event: any):
    if(event.type == pygame.MOUSEBUTTONDOWN):
      if(not self.renderer.outline_rect.collidepoint(event.pos)):
        self._on_unfocus()
    pass

  @abstractmethod
  def _on_unfocus(self):
    pass

  