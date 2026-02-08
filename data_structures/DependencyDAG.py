from typing import Dict,List,Set
from Models import Flip, SequentialSolutionPolygon

class Vertex:
  def __init__(self, id: Flip):
    self.id = id
    self.next: Set[Vertex] = set()


class DependencyDAG:
  vertices = []

  def __init__(self, input : SequentialSolutionPolygon):
    for flip in input.steps:
      
