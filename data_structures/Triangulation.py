
from pygame.math import Vector2

class Vertex: 
  def __init__(self, x, y, id):
    self.id: int = id
    self.x: float = x
    self.y: float = y
    self.half_edge: 'HalfEdge' = None
  def pos_t(self):
    return (self.x, self.y)
  def pos_v2(self):
    return Vector2(self.x, self.y)
    
class Face:
  def __init__(self, id: int):
    self.id = id
    self.half_edge: 'HalfEdge' = None
  
class HalfEdge:
  def __init__(self, origin: Vertex):
    self.origin = origin
    self.twin: 'HalfEdge' = None
    self.next: 'HalfEdge' = None
    self.prev: 'HalfEdge' = None
    self.face: Face = None #CCW

class Triangulation:
  def __init__(self):
    self.center = ConnectionError
    self.vertices = []
    self.half_edges = []
    self.faces = []
    self._outer_face = None
  #################
  #  API methods  #
  #################
  def insert_edge(self, v1_id: int, v2_id: int):
    he_start, he_end = self._find_he_in_common_face(v1_id, v2_id)
    self._split_face(he_start, he_end)

  def initialize_polygon(self, points:list[tuple[float,float]]):
    n = len(points)
    if n < 3:
      raise ValueError("At least 3 points are required to form a polygon convex hull")
    #create vertices
    for i, (x, y) in enumerate(points):
      self._create_vertex(x, y)
    #create faces (inner and outer)
    inner_face = self._create_face()
    outer_face = self._create_face()
    self._outer_face = outer_face
    #create ring of edges
    inner_edges = []
    outer_edges = []
    for i in range(n):
      u = self.vertices[i]
      v = self.vertices[(i + 1) % n]
      he_in = self._create_half_edge(u, inner_face)
      he_out = self._create_half_edge(v, outer_face)
      self._link_twins(he_in, he_out)
      inner_edges.append(he_in)
      outer_edges.append(he_out)
    #link next and prev
    for i in range(n):
      #Inner (CCW)
      inner_edges[i].next = inner_edges[(i + 1) % n]
      inner_edges[i].prev = inner_edges[(i - 1) % n]
      #Outer (CW)
      outer_edges[i].next = outer_edges[(i - 1) % n]
      outer_edges[i].prev = outer_edges[(i + 1) % n]

  @staticmethod
  def find_edge(v_from: Vertex, v_to: Vertex) -> HalfEdge:
    cur = v_from.half_edge
    start_edge = cur
    while True:
      if cur.twin.origin == v_to:
        return cur
      cur = cur.twin.next
      if cur == start_edge:
        break
    raise ValueError(f"No edge found from vertex {v_from.id} to vertex {v_to.id}")
  
  def find_edge_by_ids(self, v_from_id: int, v_to_id: int) -> HalfEdge:
    v_from = self.vertices[v_from_id]
    v_to = self.vertices[v_to_id]
    return Triangulation.find_edge(v_from, v_to)
  
  def flip_edge(self, v1_id: int, v2_id: int) -> bool:
    he = self.find_edge_by_ids(v1_id, v2_id)
    twin = he.twin
    if he.face == self._outer_face or twin.face == self._outer_face:
        return False
    # Store all neighbors before modification
    he_next = he.next
    he_prev = he.prev
    twin_next = twin.next
    twin_prev = twin.prev 
    # Store faces
    face1 = he.face
    face2 = twin.face
    # The 4 vertices: he goes from b→c, twin goes c→b
    # he's face has vertices: a (he_prev.origin), b (he.origin), c (he_next.origin)
    # twin's face has vertices: d (twin_prev.origin), c (twin.origin), b (twin_next.origin)
    a = he_prev.origin
    d = twin_prev.origin
    # Fix vertex half_edge references before changing origins
    if he.origin.half_edge == he:
        he.origin.half_edge = twin_next
    if twin.origin.half_edge == twin:
        twin.origin.half_edge = he_next
    # Rotate edge: he now goes a→d, twin goes d→a
    he.origin = a
    twin.origin = d
    # Update face assignments
    he.face = face2
    twin.face = face1
    twin_next.face = face1
    he_next.face = face2
    # he_prev stays in face1, twin_prev stays in face2
    # Relink face1: he_prev → twin_next → twin → he_prev
    he_prev.next = twin_next
    twin_next.prev = he_prev
    twin_next.next = twin
    twin.prev = twin_next
    twin.next = he_prev
    he_prev.prev = twin
    # Relink face2: he → twin_prev → he_next → he
    he.next = twin_prev
    twin_prev.prev = he
    twin_prev.next = he_next
    he_next.prev = twin_prev
    he_next.next = he
    he.prev = he_next
    # Update face half_edge references
    face1.half_edge = twin
    face2.half_edge = he
    return True

  #####################
  #  Factory methods  #
  #####################
  def _create_vertex(self, x, y):
    v = Vertex(x, y, len(self.vertices))
    self.vertices.append(v)
    return v
  
  def _create_face(self):
    f = Face(len(self.faces))
    self.faces.append(f)
    return f
  
  def _create_half_edge(self, origin: Vertex, face: Face):
    he = HalfEdge(origin)
    he.face = face
    #link vertex
    if origin.half_edge is None:
      origin.half_edge = he
    #link face
    if face.half_edge is None:
      face.half_edge = he
    self.half_edges.append(he)
    return he
  
  def _link_twins(self, he1: HalfEdge, he2: HalfEdge):
    he1.twin = he2
    he2.twin = he1

  def _find_he_in_common_face(self, v1_id: int, v2_id: int) -> HalfEdge:
    v1 = self.vertices[v1_id]
    v2 = self.vertices[v2_id]
    #get all HE starting in v1
    start_candidates = []
    cur = v1.half_edge
    if cur:
      start_edge = cur
      while True:
        start_candidates.append(cur)
        if cur.twin is None: break #shouln't happen in triangulation
        cur = cur.twin.next
        if cur == start_edge:
          break
    #get all HE starting in v2
    end_candidates = []
    cur = v2.half_edge
    if cur:
      start_edge = cur
      while True:
        end_candidates.append(cur)
        if cur.twin is None: break #shouln't happen in triangulation
        cur = cur.twin.next
        if cur == start_edge:
          break
    #find pair with same face
    for he_s in start_candidates:
      for he_e in end_candidates:
        if he_s.face == he_e.face and he_s.face != self._outer_face:
          return he_s, he_e
    raise ValueError(f"No common face found between vertices {v1_id} and {v2_id}")
  
  def _split_face(self, he_start: HalfEdge, he_end: HalfEdge):
    old_face = he_start.face
    new_face = self._create_face()
    new_he = self._create_half_edge(he_start.origin, old_face)
    new_twin = self._create_half_edge(he_end.origin, new_face)
    self._link_twins(new_he, new_twin)
    #neighbors
    he_start_prev = he_start.prev
    he_end_prev = he_end.prev
    #relink old face
    new_he.next = he_end
    new_he.prev = he_start_prev
    he_start_prev.next = new_he
    he_end.prev = new_he
    #link new face
    new_twin.next = he_start
    new_twin.prev = he_end_prev
    he_end_prev.next = new_twin
    he_start.prev = new_twin
    #update face references
    cur = new_twin
    while True:
      cur.face = new_face
      cur = cur.next
      if cur == new_twin:
        break
    #update half_edge reference
    old_face.half_edge = new_he

  #########################
  #  Validation (AI Code) #
  #########################
  def sanity_check(self, order: int):
    # Vertex count
    if len(self.vertices) != order:
      raise ValueError(f"Expected {order} vertices, found {len(self.vertices)}")
    # Face count: (order - 2) inner triangles + 1 outer face
    expected_face_count = order - 2 + 1
    if len(self.faces) != expected_face_count:
      raise ValueError(f"Expected {expected_face_count} faces, found {len(self.faces)}")
    # Half-edge count: 2*n boundary + 2*(n-3) internal = 4n - 6
    expected_edge_count = 4 * order - 6
    if len(self.half_edges) != expected_edge_count:
      raise ValueError(f"Expected {expected_edge_count} half-edges, found {len(self.half_edges)}")    
    # Check each face has correct edge count (3 for inner, order for outer)
    for face in self.faces:
      if face.half_edge is None:
        raise ValueError(f"Face {face.id} has no half-edge reference")
      count = 0
      start_he = face.half_edge
      cur = start_he
      max_iterations = len(self.half_edges) + 1
      while count < max_iterations:
        count += 1
        cur = cur.next
        if cur == start_he:
          break
      else:
        raise ValueError(f"Face {face.id} has infinite loop in edge traversal")
      if face == self._outer_face:
        if count != order:
          raise ValueError(f"Outer face should have {order} edges, has {count}")
      elif count != 3:
        raise ValueError(f"Face {face.id} does not have 3 edges, has {count} edges instead")
    # Check each vertex has at least one outgoing edge
    for vertex in self.vertices:
      if vertex.half_edge is None:
        raise ValueError(f"Vertex {vertex.id} has no outgoing half-edge")
    # Check edge twins
    for he in self.half_edges:
      if he.twin is None:
        raise ValueError(f"Half-edge from vertex {he.origin.id} has no twin")
      if he.twin.twin != he:
        raise ValueError(f"Half-edge from vertex {he.origin.id} twin linkage is broken")
      if he.origin == he.twin.origin:
        raise ValueError(f"Half-edge from vertex {he.origin.id} has the same origin as its twin")
      # Twin should start where this edge ends
      if he.twin.origin != he.next.origin:
        raise ValueError(f"Half-edge from vertex {he.origin.id}: twin origin doesn't match next origin")
    # Check next/prev consistency
    for he in self.half_edges:
      if he.next is None:
        raise ValueError(f"Half-edge from vertex {he.origin.id} has no next")
      if he.prev is None:
        raise ValueError(f"Half-edge from vertex {he.origin.id} has no prev")
      if he.next.prev != he:
        raise ValueError(f"Half-edge from vertex {he.origin.id}: next.prev != self")
      if he.prev.next != he:
        raise ValueError(f"Half-edge from vertex {he.origin.id}: prev.next != self")
    # Check face linkage consistency
    for he in self.half_edges:
      if he.face is None:
        raise ValueError(f"Half-edge from vertex {he.origin.id} has no face")
      if he.next.face != he.face:
        raise ValueError(f"Half-edge from vertex {he.origin.id}: next half-edge has different face")