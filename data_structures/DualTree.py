from data_structures.Triangulation import Triangulation, Face, HalfEdge

class Node:
  def __init__(self, face: Face = None):
    self.face = face
    self.left = None
    self.right = None

class DualTree:
  def __init__(self, tri: Triangulation = None, root_edge: tuple[int, int] = (0,1)):
    #meta data for rendering
    self.node_count = 0
    self.depth = 0
    self._visited_faces: set[Face] = set()
    self.root_he = tri.find_edge_by_ids(root_edge[0], root_edge[1])
    self.root_face = self.root_he.face
    self.root = self._build_subtree(self.root_face, self.root_he, tri._outer_face, 0)

  def _build_subtree(self, current_face: Face, entry_edge: HalfEdge, outer_face: Face, cur_depth: int):
    if current_face in self._visited_faces:
      return None
    self._visited_faces.add(current_face)
    node = Node(current_face)
    self.node_count += 1
    self.depth = max(self.depth, cur_depth)
    left_candidate = entry_edge.next
    right_candidate = entry_edge.prev
    #right child
    right_face = right_candidate.twin.face
    if right_face == outer_face:
      node.right = None
    else:
      node.right = self._build_subtree(right_face, right_candidate.twin, outer_face, cur_depth + 1)
    #left child
    left_face = left_candidate.twin.face
    if left_face == outer_face:
      node.left = None
    else:
      node.left = self._build_subtree(left_face, left_candidate.twin, outer_face, cur_depth + 1)
    return node
  
  #########################
  #  Validation (AI-Code) #
  #########################
  def sanity_check(self, tri: Triangulation):
    # Node count should equal number of inner faces (order - 2)
    expected_node_count = len(tri.faces) - 1  # exclude outer face
    if self.node_count != expected_node_count:
      raise ValueError(f"Expected {expected_node_count} nodes, found {self.node_count}")
    # Root should exist
    if self.root is None:
      raise ValueError("Root node is None")
    # Root face should not be outer face
    if self.root_face == tri._outer_face:
      raise ValueError("Root face is the outer face")
    # Collect all nodes and faces via traversal
    visited_nodes: set[Node] = set()
    visited_faces: set[Face] = set()
    def traverse(node: Node, depth: int, max_depth: list[int]):
      if node is None:
        return
      # Check for cycles
      if node in visited_nodes:
        raise ValueError(f"Cycle detected: node with face {node.face.id} visited twice")
      visited_nodes.add(node)
      # Check node has a face
      if node.face is None:
        raise ValueError("Node has no face reference")
      # Check face not duplicated
      if node.face in visited_faces:
        raise ValueError(f"Face {node.face.id} appears in multiple nodes")
      visited_faces.add(node.face)
      # Check face is not outer face
      if node.face == tri._outer_face:
        raise ValueError(f"Node contains outer face (face {node.face.id})")
      # Track max depth
      max_depth[0] = max(max_depth[0], depth)
      # Recurse
      traverse(node.left, depth + 1, max_depth)
      traverse(node.right, depth + 1, max_depth)
    max_depth = [0]
    traverse(self.root, 0, max_depth)
    # Check all inner faces are covered
    inner_faces = {f for f in tri.faces if f != tri._outer_face}
    if visited_faces != inner_faces:
      missing = inner_faces - visited_faces
      extra = visited_faces - inner_faces
      if missing:
        raise ValueError(f"Missing faces in tree: {[f.id for f in missing]}")
      if extra:
        raise ValueError(f"Extra faces in tree: {[f.id for f in extra]}")
    # Check node count matches traversal
    if len(visited_nodes) != self.node_count:
      raise ValueError(f"Node count mismatch: stored {self.node_count}, traversed {len(visited_nodes)}")
    # Check depth
    if max_depth[0] != self.depth:
      raise ValueError(f"Depth mismatch: stored {self.depth}, computed {max_depth[0]}")