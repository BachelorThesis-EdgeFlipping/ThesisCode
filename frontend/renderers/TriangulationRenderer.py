from .Renderer import Interactable, Renderer
import pygame
from frontend.renderers.RenderPos import RenderPos
from pygame.math import Vector2
from data_structures.Triangulation import Triangulation, Vertex, Face
from frontend.Gobals import Color, DEFAULT_FONT

class RenderNode:
  def __init__(self, node: Vertex, position: Vector2):
    self.node: Vertex = node
    self.position: Vector2 = position #center possition

class RenderEdge:
  def __init__(self, from_pos: Vector2, to_pos: Vector2):
    self.from_pos = from_pos
    self.to_pos = to_pos

class RenderFace:
  def __init__(self, face: Face, centroid_position: Vector2):
    self.face: any = face
    self.position: Vector2 = centroid_position

class TriangulationRenderer(Renderer):

  #default styling settings
  VERTEX_RADIUS = 14
  VERTEX_COLOR = Color.BLUE
  EDGE_WIDTH = 2
  EDGE_COLOR = Color.LIGHT_BLUE
  FACE_COLOR = Color.CORAL
  FACE_BACKGROUND_COLOR = Color.LIGHT_YELLOW
  FACE_BACKGROUND_RADIUS = 10
  SHOW_VERTEX_IDS = True
  SHOW_FACE_IDS = True
  SHOW_FACE_BACKGROUND = True
  FONT = DEFAULT_FONT

  def __init__(self, 
              content: Triangulation, 
              title: str = "",
              vertex_radius: int = VERTEX_RADIUS,
              vertex_color: Color = VERTEX_COLOR,
              edge_width: int = EDGE_WIDTH,
              edge_color: Color = EDGE_COLOR,
              face_color: Color = FACE_COLOR,
              face_background_color: Color = FACE_BACKGROUND_COLOR,
              face_background_radius: int = FACE_BACKGROUND_RADIUS,
              show_vertex_ids: bool = SHOW_VERTEX_IDS,
              show_face_ids: bool = SHOW_FACE_IDS,
              show_face_background: bool = SHOW_FACE_BACKGROUND,
              font: pygame.font.Font = FONT,
              **kwargs):
    super().__init__(
      content,
      internal_content_padding = Vector2(vertex_radius, vertex_radius),
      title = "Triangulation" + (": " + title if title else ""),
      **kwargs)
    self.vertex_radius = vertex_radius
    self.vertex_color = vertex_color
    self.edge_width = edge_width
    self.edge_color = edge_color
    self.face_color = face_color
    self.face_background_color = face_background_color
    self.face_background_radius = face_background_radius
    self.show_vertex_ids = show_vertex_ids
    self.show_face_ids = show_face_ids
    self.show_face_background = show_face_background
    self.font = font
    #Render Cache
    self._render_nodes: list[RenderNode] = []
    self._render_edges: list[RenderEdge] = []
    self._render_faces: list[RenderFace] = []
    self._post_init()

  def _post_init(self):
    super()._post_init()
    self._calculate_triangulation()

  def _calculate_triangulation(self):
    self._render_nodes = []
    self._render_edges = []
    self._render_faces = []
    for vertex in self.content.vertices:
      render_node = RenderNode(vertex, vertex.pos_v2())
      self._render_nodes.append(render_node)
    for edge in self.content.half_edges:
      render_edge = RenderEdge(edge.origin.pos_v2(), edge.twin.origin.pos_v2())
      self._render_edges.append(render_edge)
    for face in self.content.faces:
      he_start = face.half_edge
      pts = []
      cur = he_start
      while True:
        pts.append(cur.origin.pos_v2())
        cur = cur.next
        if cur == he_start:
          break
      if(len(pts) != 3):
        continue
      centroid_x = sum(p[0] for p in pts) / len(pts)
      centroid_y = sum(p[1] for p in pts) / len(pts)
      centroid_pos = Vector2(centroid_x, centroid_y)
      render_face = RenderFace(face, centroid_pos)
      self._render_faces.append(render_face)

  def render(self, screen: pygame.Surface):
    super().render(screen)
    #render edges
    for edge in self._render_edges:
      projected_pos_origin: RenderPos = self._project_position(edge.from_pos)
      projected_pos_twin: RenderPos = self._project_position(edge.to_pos)
      pygame.draw.line(screen, self.edge_color.value, projected_pos_origin.tuple(), projected_pos_twin.tuple(), self.edge_width) 
    #render vertices
    for node in self._render_nodes:
      projected_pos_t: RenderPos = self._project_position(node.position)
      pygame.draw.circle(screen, self.vertex_color.value, projected_pos_t.tuple(), self.vertex_radius)
      if self.show_vertex_ids:
        img = self.font.render(str(node.node.id), True, Color.WHITE.value)
        screen.blit(img, (projected_pos_t.x - img.get_width() // 2, projected_pos_t.y - img.get_height() // 2))
    #render faces
    for face in self._render_faces:
      projected_centroid: RenderPos = self._project_position(face.position)
      if self.show_face_ids:
        if self.show_face_background:
          pygame.draw.circle(screen, self.face_background_color.value, projected_centroid.tuple(), self.face_background_radius)
        img = self.font.render(str(face.face.id), True, self.face_color.value)
        screen.blit(img, (projected_centroid.x - img.get_width() // 2, projected_centroid.y - img.get_height() // 2))

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
  
  def _project_position(self, pos: Vector2) -> RenderPos:
    #triangulation internal possible offset
    pos = pos + self.triangulation_projection_offset
    return super()._project_position(pos)
  
  def update_content(self):
    super().update_content()
    self._calculate_triangulation()

  def get_interables(self) -> list[Interactable[Vertex]]:
    interactables: list[Interactable[Vertex]] = []
    for render_node in self._render_nodes:
      pos: RenderPos = self._project_position(render_node.position) - RenderPos.square_from_int(self.vertex_radius)
      size: RenderPos = RenderPos.square_from_int(self.vertex_radius * 2)
      interactables.append(Interactable(render_node.node, pos, size))
    return interactables
    
    