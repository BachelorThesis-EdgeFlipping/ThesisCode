from dataclasses import dataclass
from dataclasses_json import dataclass_json

Edge = tuple[int, int]
Flip = tuple[Edge, Edge]

#################
# Import Models #
#################
class ImportModel:
  pass

@dataclass_json
@dataclass
class RegularPolygonTriangulation(ImportModel): 
  order: int #starting at 0 at the top center
  internal_edges: list[Edge]
  projection_size: int = 200

@dataclass_json
@dataclass
class PointSetTriangulation(ImportModel):
  vertices: list[tuple[int, int]]
  edges: list[Edge] #list of edges as tuples of vertex indices

@dataclass_json
@dataclass
class SequentialSolutionPolygon(ImportModel):
  order: int
  internal_source_edges: list[Edge]
  internal_target_edges: list[Edge]
  steps: list[Flip]