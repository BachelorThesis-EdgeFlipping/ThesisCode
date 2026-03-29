
from pygame.math import Vector2
import math

from Models import Edge
from SyncNetwork import Syncable

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
    self.origin: Vertex = origin
    self.twin: 'HalfEdge' = None
    self.next: 'HalfEdge' = None
    self.prev: 'HalfEdge' = None
    self.face: Face = None #CCW

class Triangulation(Syncable):
  def __init__(self):
    self.center = ConnectionError
    self.vertices = []
    self.half_edges = []
    self.faces = []
    self._outer_face = None
    self._edge_set_cache: frozenset[Edge] | None = None

  def deep_copy(self) -> 'Triangulation':
    copy = Triangulation()
    for v in self.vertices:
      copy.vertices.append(Vertex(v.x, v.y, v.id))
    for f in self.faces:
      copy.faces.append(Face(f.id))
    he_map: dict[int, HalfEdge] = {}
    for he in self.half_edges:
      new_he = HalfEdge(copy.vertices[he.origin.id])
      new_he.face = copy.faces[he.face.id]
      he_map[id(he)] = new_he
      copy.half_edges.append(new_he)
    #link twin, next, prev
    for he in self.half_edges:
      new_he = he_map[id(he)]
      if he.twin is not None:
        new_he.twin = he_map[id(he.twin)]
      if he.next is not None:
        new_he.next = he_map[id(he.next)]
      if he.prev is not None:
        new_he.prev = he_map[id(he.prev)]
    #l ink vertex.half_edge
    for v in self.vertices:
      if v.half_edge is not None:
        copy.vertices[v.id].half_edge = he_map[id(v.half_edge)]
    #link face.half_edge
    for f in self.faces:
      if f.half_edge is not None:
        copy.faces[f.id].half_edge = he_map[id(f.half_edge)]
    #outer face
    if self._outer_face is not None:
      copy._outer_face = copy.faces[self._outer_face.id]
    return copy

  #return a set of undirected edges for hashing and equality checks
  def edge_set(self) -> frozenset[tuple[int, int]]:
    if self._edge_set_cache is None:
      edges = set()
      for he in self.half_edges:
        a, b = he.origin.id, he.twin.origin.id
        edges.add((min(a, b), max(a, b)))
      self._edge_set_cache = frozenset(edges)
    return self._edge_set_cache

  def count_shared_edges(self, other: 'Triangulation') -> int:
    self_edges = self.edge_set()
    other_edges = other.edge_set()
    if len(self_edges) > len(other_edges):
      self_edges, other_edges = other_edges, self_edges
    return sum(1 for edge in self_edges if edge in other_edges)

  @staticmethod
  def _orientation(ax: float, ay: float, bx: float, by: float, cx: float, cy: float) -> float:
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

  @staticmethod
  def _sign_float_safe(value: float) -> int:
    stupid_ass_float_safety_value = 1e-12
    if value > stupid_ass_float_safety_value:
      return 1
    if value < -stupid_ass_float_safety_value:
      return -1
    return 0

  @staticmethod
  def _segments_strictly_intersect(
    a1: Vertex,
    a2: Vertex,
    b1: Vertex,
    b2: Vertex
  ) -> bool:
    #shared endpoints = no geometric crossings
    if (
      a1.id == b1.id or a1.id == b2.id or
      a2.id == b1.id or a2.id == b2.id
    ):
      return False
    o1 = Triangulation._sign_float_safe(Triangulation._orientation(a1.x, a1.y, a2.x, a2.y, b1.x, b1.y))
    o2 = Triangulation._sign_float_safe(Triangulation._orientation(a1.x, a1.y, a2.x, a2.y, b2.x, b2.y))
    o3 = Triangulation._sign_float_safe(Triangulation._orientation(b1.x, b1.y, b2.x, b2.y, a1.x, a1.y))
    o4 = Triangulation._sign_float_safe(Triangulation._orientation(b1.x, b1.y, b2.x, b2.y, a2.x, a2.y))
    #strict intersection: excludes collinear/touching case
    return o1 * o2 < 0 and o3 * o4 < 0

  def count_geometric_crossings_with(self, other: 'Triangulation') -> int:
    crossings = 0
    self_edges = self.edge_set()
    other_edges = other.edge_set()
    for a_id, b_id in self_edges:
      a1 = self.vertices[a_id]
      a2 = self.vertices[b_id]
      for c_id, d_id in other_edges:
        b1 = other.vertices[c_id]
        b2 = other.vertices[d_id]
        if Triangulation._segments_strictly_intersect(a1, a2, b1, b2):
          crossings += 1
    return crossings

  def __hash__(self) -> int:
    return hash(self.edge_set())

  def __eq__(self, other: 'Triangulation') -> bool:
    return self.edge_set() == other.edge_set()

  #################
  #  API methods  #
  #################
  def insert_edge(self, v1_id: int, v2_id: int):
    he_start, he_end = self._find_he_in_common_face(v1_id, v2_id)
    self._split_face(he_start, he_end)
    self._edge_set_cache = None

  def initialize_regular_polygon(self, points:list[tuple[float,float]]):
    self._edge_set_cache = None
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

  def initialize_from_edges(self, points: list[tuple[int, int]], edges: list[tuple[int, int]]):
    self._edge_set_cache = None
    #create vertices
    for i, (x, y) in enumerate(points):
      self._create_vertex(x, y)
    #create he pairs for every edge
    outgoing: dict[int, list[HalfEdge]] = {v: [] for v in range(len(points))}
    for v1_id, v2_id in edges:
      v1 = self.vertices[v1_id]
      v2 = self.vertices[v2_id]
      he = HalfEdge(v1)
      twin = HalfEdge(v2)
      he.twin = twin
      twin.twin = he
      self.half_edges.append(he)
      self.half_edges.append(twin)
      outgoing[v1_id].append(he)
      outgoing[v2_id].append(twin)
    #sort outgoing he's CCW around each vertex and link prev and next
    for v_id, he_list in outgoing.items():
      origin = self.vertices[v_id]
      #sort by angle from vertex to the edges target
      def angle_to_target(he: HalfEdge) -> float:
        target = he.twin.origin
        return math.atan2(target.y - origin.y, target.x - origin.x)
      he_list.sort(key=angle_to_target)
      origin.half_edge = he_list[0]
      n = len(he_list)
      for i in range(n):
        #link CCW neighbors. arriving via e_{i+1}.twin, leave via e_i
        he_list[(i + 1) % n].twin.next = he_list[i]
        he_list[i].prev = he_list[(i + 1) % n].twin
    #discover faces
    visited = set()
    for he in self.half_edges:
      if id(he) in visited:
        continue
      face = self._create_face()
      face.half_edge = he
      curr = he
      signed_area = 0.0
      while True:
        curr.face = face
        visited.add(id(curr))
        if curr.origin.half_edge is None:
          curr.origin.half_edge = curr
        #shoelace contribution
        p1 = curr.origin
        p2 = curr.twin.origin
        signed_area += (p1.x * p2.y - p2.x * p1.y)
        curr = curr.next
        if curr == he:
          break
      #identify outer face by largest absolute signed area
      abs_area = abs(signed_area)
      if self._outer_face is None:
        self._outer_face = face
        self._outer_face_area = abs_area
      elif abs_area > self._outer_face_area:
        self._outer_face = face
        self._outer_face_area = abs_area
    #clean up temporary attribute
    if hasattr(self, '_outer_face_area'):
      del self._outer_face_area

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
  
  def _cross_product(self, v1: Vertex, v2: Vertex, v3: Vertex) -> float:
    #compute cross product of vectors (v1,v2) and (v1,v3)
    return (v2.x - v1.x) * (v3.y - v1.y) - (v2.y - v1.y) * (v3.x - v1.x)
  
  def is_flippable(self, v1_id: int, v2_id: int) -> bool:
    he = self.find_edge_by_ids(v1_id, v2_id)
    # check if internal edge (not connected to outer face)
    if he.face == self._outer_face or he.twin.face == self._outer_face:
      return False
    a = he.prev.origin
    b = he.origin
    c = he.next.origin
    d = he.twin.prev.origin
    #strict convex check: diagonals BC and AD must intersect
    #A and D must rest on strictly opposite sides of line BC
    if not self._opposite_sides(b, c, a, d):
      return False
    # B and C must rest on strictly opposite sides of line AD
    if not self._opposite_sides(a, d, b, c):
      return False
    return True
  
  def _opposite_sides(self, a: Vertex, b: Vertex, c: Vertex, d: Vertex) -> bool:
    #check if C and D are STRICTLY on opposite sides of AB
    #fails for quasi-quadrilateral cases where one of the points is collinear with AB
    cp1 = self._cross_product(a, b, c)
    cp2 = self._cross_product(a, b, d)
    return cp1 * cp2 < 0

  #return list of edges (not half-edges) that are flipable 
  def get_flippable_edges(self) -> list[Edge]:
    flippable = []
    seen = set()
    for he in self.half_edges:
      a, b = he.origin.id, he.twin.origin.id
      key = (min(a, b), max(a, b))
      if key in seen:
        continue
      seen.add(key)
      if self.is_flippable(a, b):
        flippable.append(key)
    return flippable

  #return all independent subsets of flippable edges (including non-maximal sets)
  def get_independent_flip_sets(self, ignore_edges: set[Edge] = None) -> list[list[Edge]]:
    flippable = self.get_flippable_edges()
    #filter out ignored edges
    if ignore_edges is not None and len(ignore_edges) > 0:
      ignored_edges_normalized: set[Edge] = set(map(lambda e: (min(e[0], e[1]), max(e[0], e[1])), ignore_edges))
      flippable = [e for e in flippable if e not in ignored_edges_normalized]
    if not flippable:
      return []
    #precompute face pairs for each flippable edge
    edge_faces: list[tuple[int, int]] = []
    for v1, v2 in flippable:
      he = self.find_edge_by_ids(v1, v2)
      edge_faces.append((he.face.id, he.twin.face.id))
    n = len(flippable)
    #enumerate all independent sets via backtracking
    results: list[list[Edge]] = []
    def backtrack(index: int, current: list[int], used_faces: set[int]):
      if current:
        results.append([flippable[i] for i in current])
      for k in range(index, n):
        f_a, f_b = edge_faces[k]
        if f_a not in used_faces and f_b not in used_faces:
          current.append(k)
          used_faces.add(f_a)
          used_faces.add(f_b)
          backtrack(k + 1, current, used_faces)
          current.pop()
          used_faces.discard(f_a)
          used_faces.discard(f_b)
    backtrack(0, [], set())
    results.sort(key=len, reverse=True)
    return results

  #expects a valid list of flips
  def flip_edges_simultaneous(self, flip_list: list[Edge]) -> bool:
    faces_involved = set()
    for v1_id, v2_id in flip_list:
      #verification phase (geometric validity)
      if not self.is_flippable(v1_id, v2_id):
        return False
      he = self.find_edge_by_ids(v1_id, v2_id)
      face1_id = he.face.id
      face2_id = he.twin.face.id
      #blocking condition (topological independence)
      if face1_id in faces_involved or face2_id in faces_involved:
        return False
      faces_involved.add(face1_id)
      faces_involved.add(face2_id)
    #execution phase
    for v1_id, v2_id in flip_list:
      self.flip_edge(v1_id, v2_id, pre_verified=True)
    return True

  def flip_edge(self, v1_id: int, v2_id: int, pre_verified: bool = False) -> bool:
    he = self.find_edge_by_ids(v1_id, v2_id)
    twin = he.twin
    if not pre_verified:
      if not self.is_flippable(v1_id, v2_id):
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
    self._edge_set_cache = None
    return True
  
  def _find_flip_candidate_by_face_ids(self, face1_id: int, face2_id: int) -> tuple[int,int]:
    face1 = self.faces[face1_id]
    face2 = self.faces[face2_id]
    shared_he = self._find_shared_he_between_faces(face1, face2)
    return (shared_he.origin.id, shared_he.twin.origin.id)

  def _find_shared_he_between_faces(self, face1: Face, face2: Face) -> HalfEdge:
    start_he = face1.half_edge
    cur = start_he
    max_iterations = len(self.half_edges) + 1
    count = 0
    while count < max_iterations:
      count += 1
      if cur.twin.face == face2:
        return cur
      cur = cur.next
      if cur == start_he:
        break
    raise ValueError(f"No shared half-edge found between faces {face1.id} and {face2.id}")
  
  def get_face_ids_adjacent_to_edge(self, v1_id: int, v2_id: int) -> tuple[int,int]:
    he = self.find_edge_by_ids(v1_id, v2_id)
    face1_id = he.face.id
    face2_id = he.twin.face.id
    return (face1_id, face2_id)

  #######################
  #   Syncable method   #
  #######################

  def sync(self, face_id1: int, face_id2: int):
    v1_id, v2_id = self._find_flip_candidate_by_face_ids(face_id1, face_id2)
    self.flip_edge(v1_id, v2_id)

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
  def sanity_check(self):
    V = len(self.vertices)
    if V < 3:
      raise ValueError(f"Expected at least 3 vertices, found {V}")
    # Half-edge count must be even (every edge has a twin)
    HE = len(self.half_edges)
    if HE % 2 != 0:
      raise ValueError(f"Half-edge count {HE} is not even")
    E = HE // 2
    F = len(self.faces)
    # Euler's formula for planar graphs: V - E + F = 2
    euler = V - E + F
    if euler != 2:
      raise ValueError(f"Euler's formula violated: V({V}) - E({E}) + F({F}) = {euler}, expected 2")
    # Check each face has correct edge count (3 for inner faces, any for outer)
    for face in self.faces:
      if face.half_edge is None:
        raise ValueError(f"Face {face.id} has no half-edge reference")
      count = 0
      start_he = face.half_edge
      cur = start_he
      max_iterations = HE + 1
      while count < max_iterations:
        count += 1
        cur = cur.next
        if cur == start_he:
          break
      else:
        raise ValueError(f"Face {face.id} has infinite loop in edge traversal")
      if face == self._outer_face:
        if count < 3:
          raise ValueError(f"Outer face should have at least 3 edges, has {count}")
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
    # No duplicate directed edges
    seen_edges = set()
    for he in self.half_edges:
      key = (he.origin.id, he.twin.origin.id)
      if key in seen_edges:
        raise ValueError(f"Duplicate directed edge {key}")
      seen_edges.add(key)
    # CCW orientation: all inner faces must have positive signed area
    for face in self.faces:
      if face == self._outer_face:
        continue
      he = face.half_edge
      a = he.origin
      b = he.next.origin
      c = he.next.next.origin
      cp = self._cross_product(a, b, c)
      if cp <= 0:
        raise ValueError(
          f"Face {face.id} has non-positive orientation (cross product = {cp}). "
          f"Vertices: {a.id}({a.x:.2f},{a.y:.2f}), {b.id}({b.x:.2f},{b.y:.2f}), {c.id}({c.x:.2f},{c.y:.2f})"
        )
    # Boundary edges must not be flippable
    for he in self.half_edges:
      if he.face == self._outer_face or he.twin.face == self._outer_face:
        v1_id = he.origin.id
        v2_id = he.twin.origin.id
        if self.is_flippable(v1_id, v2_id):
          raise ValueError(f"Boundary edge ({v1_id}, {v2_id}) incorrectly reported as flippable")
    # Flippable edges must form strictly convex quadrilaterals
    checked_edges = set()
    for he in self.half_edges:
      if he.face == self._outer_face or he.twin.face == self._outer_face:
        continue
      edge_key = frozenset((he.origin.id, he.twin.origin.id))
      if edge_key in checked_edges:
        continue
      checked_edges.add(edge_key)
      v1_id = he.origin.id
      v2_id = he.twin.origin.id
      if self.is_flippable(v1_id, v2_id):
        a = he.prev.origin
        b = he.origin
        c = he.next.origin
        d = he.twin.prev.origin
        # Verify the 4 vertices are distinct
        ids = {a.id, b.id, c.id, d.id}
        if len(ids) != 4:
          raise ValueError(
            f"Flippable edge ({v1_id}, {v2_id}) has non-distinct quadrilateral vertices: "
            f"{a.id}, {b.id}, {c.id}, {d.id}"
          )