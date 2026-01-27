from .Renderer import Renderer
import pygame
from pygame.math import Vector2
from data_structures.Triangulation import Triangulation
from frontend.Gobals import Color, DEFAULT_FONT

class TriangulationRenderer(Renderer):

  #default styling settings
  VERTEX_RADIUS = 10
  VERTEX_COLOR = Color.BLUE
  EDGE_WIDTH = 2
  EDGE_COLOR = Color.PURPLE
  FACE_COLOR = Color.GRAY
  SHOW_VERTEX_IDS = True
  SHOW_FACE_IDS = True
  FONT = DEFAULT_FONT

  def __init__(self, 
              content: Triangulation, 
              vertex_radius: int = VERTEX_RADIUS,
              vertex_color: Color = VERTEX_COLOR,
              edge_width: int = EDGE_WIDTH,
              edge_color: Color = EDGE_COLOR,
              face_color: Color = FACE_COLOR,
              show_vertex_ids: bool = SHOW_VERTEX_IDS,
              show_face_ids: bool = SHOW_FACE_IDS,
              font: pygame.font.Font = FONT,
              **kwargs):
    super().__init__(
      content,
      internal_content_padding = Vector2(vertex_radius, vertex_radius),
      title = "Triangulation",
      **kwargs)
    self.vertex_radius = vertex_radius
    self.vertex_color = vertex_color
    self.edge_width = edge_width
    self.edge_color = edge_color
    self.face_color = face_color
    self.show_vertex_ids = show_vertex_ids
    self.show_face_ids = show_face_ids
    self.font = font
    self._post_init()

  def render(self, screen: pygame.Surface):
    super().render(screen)
    #render edges
    #NOTE: right now, render every edge twice (once for each HE)
    for edge in self.content.half_edges:
      projected_pos_origin = self._project_position(edge.origin.pos_v2())
      projected_pos_twin = self._project_position(edge.twin.origin.pos_v2())
      pygame.draw.line(screen, self.edge_color.value, projected_pos_origin, projected_pos_twin, self.edge_width) 
    #render vertices
    for vertex in self.content.vertices:
      projected_pos_t = self._project_position(vertex.pos_v2())
      pygame.draw.circle(screen, self.vertex_color.value, projected_pos_t, self.vertex_radius)
      img = self.font.render(str(vertex.id), True, Color.WHITE.value)
      screen.blit(img, (projected_pos_t[0] - img.get_width() // 2, projected_pos_t[1] - img.get_height() // 2))
    #render faces
    for face in self.content.faces:
      he_start = face.half_edge
      pts = []
      cur = he_start
      while True:
        pts.append(self._project_position(cur.origin.pos_v2()))
        cur = cur.next
        if cur == he_start:
          break
      if(len(pts) != 3):
        continue
      centroid_x = sum(p[0] for p in pts) / len(pts)
      centroid_y = sum(p[1] for p in pts) / len(pts)
      img = self.font.render(str(face.id), True, self.face_color.value)
      screen.blit(img, (centroid_x - img.get_width() // 2, centroid_y - img.get_height() // 2))

  def _get_content_size(self) -> Vector2:
    max_v2 = Vector2(0,0)
    min_v2 = Vector2(float('inf'), float('inf'))
    for vertex in self.content.vertices:
      v_pos = vertex.pos_v2()
      if v_pos.x > max_v2.x:
        max_v2.x = v_pos.x
      if v_pos.y > max_v2.y:
        max_v2.y = v_pos.y
      if v_pos.x < min_v2.x:
        min_v2.x = v_pos.x
      if v_pos.y < min_v2.y:
        min_v2.y = v_pos.y
    self.triangulation_projection_offset = Vector2(-min_v2.x, -min_v2.y)
    return max_v2 - min_v2
  
  def _project_position(self, pos: Vector2) -> tuple[int,int]:
    #triangulation internal possible offset
    pos = pos + self.triangulation_projection_offset
    return super()._project_position(pos)
  
  def update_content(self, content: Triangulation):
    super().update_content(content)