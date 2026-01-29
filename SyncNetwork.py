from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from frontend.renderers.Renderer import Renderer

class Syncable(ABC):
  @abstractmethod
  def sync(self, face_id1: int, face_id2: int):
      pass

class SyncNetwork:
  def __init__(self):
    self.syncables: list[tuple[Syncable, 'Renderer']] = []

  def register(self, renderer: 'Renderer'):
    self.syncables.append((renderer.content, renderer))

  def sync_others(self, caller: Syncable, face_id1: int, face_id2: int):
    for syncable, renderer in self.syncables:
      if syncable != caller:
        syncable.sync(face_id1, face_id2)
        renderer.update_content()