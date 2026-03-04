from Models import Edge
from data_structures.Triangulation import Vertex
from frontend.input_handlers.InputHandler import InputHandler
from frontend.renderers.BinaryTreeRenderer import BinaryTreeRenderer
import pygame
from collections import deque

class TriangulationInputHandler(InputHandler):

  def __init__(self, renderer: BinaryTreeRenderer, sync_network = None):
    super().__init__(renderer, sync_network)
    self.selected_nodes: Vertex = deque(maxlen=2)
    self.flip_stash: list[Edge] = []
  
  def handle_event(self, event: any):
    super().handle_event(event)
    if(event.type == pygame.MOUSEBUTTONDOWN):
      mouse_pos = event.pos
      for interactable in self.renderer.get_interables():
        rect = pygame.Rect(interactable.pos.tuple(), interactable.size.tuple()) 
        if rect.collidepoint(mouse_pos) and interactable.reference not in self.selected_nodes:
          self.selected_nodes.append(interactable.reference)
          print(f"Selected Node ID: {self.selected_nodes[-1].id}. Selected nodes: {self.selected_nodes}")
    if(event.type == pygame.KEYDOWN):
      if event.key == pygame.K_w:
        if len(self.selected_nodes) == 2:
          n1: Vertex = self.selected_nodes.popleft()
          n2: Vertex = self.selected_nodes.popleft()
          self.flip_stash.append((n1.id, n2.id))
          print(f"Stashed edge for flip: ({n1.id},{n2.id}). Current stash: {self.flip_stash}")
      if event.key == pygame.K_s:
        self.flip_stash.clear()
        print("Cleared flip stash.")
      if event.key == pygame.K_SPACE:
        try:
          if not self.flip_stash:
            print("No edges stashed for flipping.")
            return
          # cache face ids for sync before flip
          face_ids = []
          for edge in self.flip_stash:
            face_id1, face_id2 = self.renderer.content.get_face_ids_adjacent_to_edge(edge[0], edge[1])
            face_ids.append((face_id1, face_id2))
          if not self.renderer.content.flip_edges_simultaneous(self.flip_stash):
            print(f"cant flip current flip stash. Stash: {self.flip_stash}")
          self.renderer.update_content()
          for (face_id1, face_id2) in face_ids:
            self.sync_network.sync_others(self.renderer.content, face_id1, face_id2)
        except Exception as e:
          print(f"[Warning] Edge flip failed: {e}")
        self.flip_stash.clear()

  def _on_unfocus(self):
    self.selected_nodes.clear()
    self.flip_stash.clear()