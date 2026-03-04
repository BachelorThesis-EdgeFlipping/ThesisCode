import math

from Models import PointSetTriangulation
from data_structures.Triangulation import Triangulation
from .Parser import Parser

class PointSetTriangulationParser(Parser):
  @staticmethod
  def parse(filename: str) -> Triangulation:
    model = PointSetTriangulation.from_json(Parser.getJSONString(filename))
    tri = Triangulation()
    tri.initialize_from_edges(model.vertices, model.edges)
    tri.sanity_check()
    return tri