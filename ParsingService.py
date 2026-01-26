from abc import ABC, abstractmethod
from Globals import DATA_DIR
from data_structures.Triangulation import Triangulation
from Models import ImportModel, PolygonTriangulation 
import math
import os

class Parser(ABC):
  @staticmethod
  @abstractmethod
  def getJSONString(filename: str) -> str:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r') as f:
      json_str = f.read()
    return json_str
  
  @staticmethod
  @abstractmethod
  def parse(json_str: str):
    pass 

class TriangulationParser(Parser):
  @staticmethod
  def parse(filename: str) -> Triangulation:
    model = PolygonTriangulation.from_json(Parser.getJSONString(filename))
    tri = Triangulation()
    points = []
    radius = model.projection_size / 2
    center_x, center_y = radius, radius
    for i in range(model.order):
      angle = 2 * math.pi * i / model.order - math.pi / 2 #start at top (pi/2)
      x = center_x + radius * math.cos(angle)
      y = center_y + radius * math.sin(angle)
      points.append((x, y))
    #initialize polygon in triangulation
    tri.initialize_polygon(points)
    #insert internal edges
    for edge in model.internal_edges:
      tri.insert_edge(edge[0], edge[1])
    tri.sanity_check(model.order)
    return tri