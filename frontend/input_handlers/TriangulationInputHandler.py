from data_structures.Triangulation import Vertex
from frontend.input_handlers.InputHandler import InputHandler
from frontend.renderers.DualTreeRenderer import DualTreeRenderer
import pygame
from collections import deque

class TriangulationInputHandler(InputHandler):

  def __init__(self, renderer: DualTreeRenderer, sync_network = None):
    super().__init__(renderer, sync_network)
    self.selected_nodes: Vertex = deque(maxlen=2)

  def handle_event(self, event: any):
    super().handle_event(event)
    if(event.type == pygame.MOUSEBUTTONDOWN):
      mouse_pos = event.pos
      for interactable in self.renderer.get_interables():
        rect = pygame.Rect(interactable.pos.tuple(), interactable.size.tuple()) 
        if rect.collidepoint(mouse_pos):
          self.selected_nodes.append(interactable.reference)
          print(f"Selected Node ID: {self.selected_nodes[-1].id}. Selected nodes: {self.selected_nodes}")
    if(event.type == pygame.KEYDOWN):
      if event.key == pygame.K_SPACE:
        if len(self.selected_nodes) == 2:
          n1: Vertex = self.selected_nodes.popleft()
          n2: Vertex = self.selected_nodes.popleft()
          face_id1, face_id2 = self.renderer.content.get_face_ids_adjacent_to_edge(n1.id, n2.id)
          self.renderer.content.flip_edge(n1.id, n2.id)
          self.renderer.update_content()
          self.sync_network.sync_others(self.renderer.content, face_id1, face_id2)

  def _on_unfocus(self):
    self.selected_nodes.clear()