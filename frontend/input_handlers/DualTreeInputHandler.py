from data_structures.DualTree import Node, RotationDirection
from frontend.input_handlers.InputHandler import InputHandler
from frontend.renderers.DualTreeRenderer import DualTreeRenderer
import pygame

class DualTreeInputHandler(InputHandler):

  def __init__(self, renderer: DualTreeRenderer, sync_network = None):
    super().__init__(renderer, sync_network)
    self.selected_node: Node = None

  def handle_event(self, event: any):
    super().handle_event(event)
    if(event.type == pygame.MOUSEBUTTONDOWN):
      mouse_pos = event.pos
      for interactable in self.renderer.get_interables():
        rect = pygame.Rect(interactable.pos.tuple(), interactable.size.tuple())
        if rect.collidepoint(mouse_pos):
          self.selected_node = interactable.reference
          print(f"Selected Node ID: {self.selected_node.face.id}, Height: {self.selected_node.height}")
          break
    if(event.type == pygame.KEYDOWN):
      if event.key == pygame.K_LEFT:
        if self.selected_node is not None:
          face_id1, face_id2 = self.renderer.content.get_face_ids_from_rotation(self.selected_node, RotationDirection.LEFT)
          self.renderer.content.rotate(self.selected_node, RotationDirection.LEFT)
          self.renderer.update_content()
          self.sync_network.sync_others(self.renderer.content, face_id1, face_id2)
      if event.key == pygame.K_RIGHT:
        if self.selected_node is not None:
          face_id1, face_id2 = self.renderer.content.get_face_ids_from_rotation(self.selected_node, RotationDirection.RIGHT)
          self.renderer.content.rotate(self.selected_node, RotationDirection.RIGHT)
          self.renderer.update_content()
          self.sync_network.sync_others(self.renderer.content, face_id1, face_id2)

  def _on_unfocus(self):
    self.selected_node = None