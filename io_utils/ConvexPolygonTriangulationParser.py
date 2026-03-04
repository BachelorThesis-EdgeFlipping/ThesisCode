import math

from Models import RegularPolygonTriangulation
from data_structures.Triangulation import Triangulation
from .Parser import Parser

class ConvexPolygonTriangulationParser(Parser):
  @staticmethod
  def parse(filename: str) -> Triangulation:
    model = RegularPolygonTriangulation.from_json(Parser.getJSONString(filename))
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
    tri.initialize_regular_polygon(points)
    #insert internal edges
    for edge in model.internal_edges:
      tri.insert_edge(edge[0], edge[1])
    tri.sanity_check()
    return tri