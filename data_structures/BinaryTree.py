from SyncNetwork import Syncable
from data_structures.Triangulation import Triangulation, Face, HalfEdge
from enum import Enum

class RotationDirection(Enum):
  LEFT = 1
  RIGHT = 2

class Node:
  def __init__(self, face: Face = None, parent: 'Node' = None):
    self.face = face
    self.parent = parent
    self.left = None
    self.right = None
    self.height = 0

class BinaryTree(Syncable):
  def __init__(self, tri: Triangulation = None, root_edge: tuple[int, int] = (0,1)):
    #meta data for rendering
    self.node_count = 0
    self._visited_faces: set[Face] = set()
    self.root_he = tri.find_edge_by_ids(root_edge[0], root_edge[1])
    self.root_face = self.root_he.face
    self.root = self._build_subtree(None, self.root_face, self.root_he, tri._outer_face)

  @property
  def depth(self) -> int:
    return self.root.height if self.root else 0

  def _build_subtree(self, parent: Node, current_face: Face, entry_edge: HalfEdge, outer_face: Face):
    if current_face in self._visited_faces:
      return None
    self._visited_faces.add(current_face)
    node = Node(current_face, parent)
    self.node_count += 1
    left_candidate = entry_edge.next
    right_candidate = entry_edge.prev
    #right child
    right_face = right_candidate.twin.face
    if right_face == outer_face:
      node.right = None
    else:
      node.right = self._build_subtree(node, right_face, right_candidate.twin, outer_face)
    #left child
    left_face = left_candidate.twin.face
    if left_face == outer_face:
      node.left = None
    else:
      node.left = self._build_subtree(node, left_face, left_candidate.twin, outer_face)
    self._update_height(node)
    return node
  
  def _update_height(self, node: Node):
    if node is None:
      return
    left_height = node.left.height if node.left else -1
    right_height = node.right.height if node.right else -1
    node.height = 1 + max(left_height, right_height)
    self._update_height(node.parent)
  
  def rotate(self, node: Node, direction: RotationDirection):
    if direction == RotationDirection.LEFT:
      self._rotate_left(node)
    elif direction == RotationDirection.RIGHT:
      self._rotate_right(node)

  def _rotate_left(self, node: Node):
    if node is None or node.right is None:
      return
    new_root = node.right
    node.right = new_root.left
    if new_root.left: 
      new_root.left.parent = node
    new_root.left = node
    if node.parent is None:
      self.root = new_root
      new_root.parent = None
    else:
      if node.parent.left == node:
        node.parent.left = new_root
      else:
        node.parent.right = new_root
      new_root.parent = node.parent
    node.parent = new_root
    self._update_height(node)
  
  def _rotate_right(self, node: Node):
    if node is None or node.left is None:
      return
    old_left = node.left
    old_right = node.right
    old_left_left = old_left.left
    old_left_right = old_left.right
    node.left = old_left_left
    if old_left_left:
      old_left_left.parent = node
    old_left.left = old_left_right
    if old_left_right:
      old_left_right.parent = old_left
    old_left.right = old_right
    if old_right:
      old_right.parent = old_left
    node.right = old_left
    old_left.parent = node
    self._update_height(old_left)
    self._update_height(node)

  def rotate_left_by_face_id(self, face_id: int):
    node = self._get_node_by_face_id(face_id)
    self._rotate_left(node)

  def rotate_right_by_face_id(self, face_id: int):
    node = self._get_node_by_face_id(face_id)
    self._rotate_right(node)

  def _get_node_by_face_id(self, face_id: int) -> Node:
    def _traverse(node: Node) -> Node:
      if node is None:
        return None
      if node.face.id == face_id:
        return node
      left_result = _traverse(node.left)
      if left_result is not None:
        return left_result
      return _traverse(node.right)
    return _traverse(self.root)

  def find_rotation_candidate_by_face_ids(self, face_id1: int, face_id2: int) -> tuple[Node, RotationDirection]:
    node1 = self._get_node_by_face_id(face_id1)
    node2 = self._get_node_by_face_id(face_id2)
    if node1 is None or node2 is None:
      raise ValueError(f"One or both face IDs {face_id1}, {face_id2} not found in Binary Tree")
    if node1.right == node2:
      return (node1, RotationDirection.LEFT)
    elif node1.left == node2:
      return (node1, RotationDirection.RIGHT)
    elif node2.right == node1:
      return (node2, RotationDirection.LEFT)
    elif node2.left == node1:
      return (node2, RotationDirection.RIGHT)
    raise ValueError(f"Nodes with face IDs {face_id1} and {face_id2} are not adjacent in the Binary Tree")

  def get_face_ids_from_rotation(self, node: Node, direction: RotationDirection) -> tuple[int, int]:
    if direction == RotationDirection.LEFT:
      if node.right is None:
        raise ValueError("Cannot get face IDs for left rotation: right child is None")
      return (node.face.id, node.right.face.id)
    elif direction == RotationDirection.RIGHT:
      if node.left is None:
        raise ValueError("Cannot get face IDs for right rotation: left child is None")
      return (node.face.id, node.left.face.id)
    else:
      raise ValueError("Invalid rotation direction")

  #######################
  #   Syncable method   #
  #######################
  def sync(self, face_id1: int, face_id2: int):
    node, direction = self.find_rotation_candidate_by_face_ids(face_id1, face_id2)
    self.rotate(node, direction)

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
    traversal_depths = []
    def traverse(node: Node, depth: int):
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
      # Track depth
      traversal_depths.append(depth)
      # Recurse
      traverse(node.left, depth + 1)
      traverse(node.right, depth + 1)
    traverse(self.root, 0)
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
    # Check height consistency for all nodes
    def validate_heights(node: Node) -> int:
      if node is None:
        return -1
      left_height = validate_heights(node.left)
      right_height = validate_heights(node.right)
      expected_height = 1 + max(left_height, right_height)
      if node.height != expected_height:
        raise ValueError(f"Node {node.face.id} has incorrect height: expected {expected_height}, found {node.height}")
      return node.height
    validate_heights(self.root)
    # Check depth property matches root height
    if self.depth != (self.root.height if self.root else 0):
      raise ValueError(f"Depth property mismatch: root height is {self.root.height if self.root else 0}, property returns {self.depth}")
    # Check that tree edges correspond to triangulation adjacencies
    def check_adjacencies(node: Node):
      if node is None:
        return
      current_face = node.face
      # Get all adjacent faces in the triangulation
      adjacent_faces = set()
      he = current_face.half_edge
      start = he
      while True:
        if he.twin.face != tri._outer_face:
          adjacent_faces.add(he.twin.face)
        he = he.next
        if he == start:
          break
      # Check children are adjacent
      if node.left is not None:
        if node.left.face not in adjacent_faces:
          raise ValueError(f"Left child face {node.left.face.id} is not adjacent to face {current_face.id}")
      if node.right is not None:
        if node.right.face not in adjacent_faces:
          raise ValueError(f"Right child face {node.right.face.id} is not adjacent to face {current_face.id}")
      # Recurse
      check_adjacencies(node.left)
      check_adjacencies(node.right)
    
    check_adjacencies(self.root)