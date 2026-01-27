import pygame
import copy
from pygame.math import Vector2
from frontend.Gobals import Color
from ParsingService import TriangulationParser
import data_structures.Triangulation
from frontend.renderers.Renderer import Renderer
from frontend.renderers.TriangulationRenderer import TriangulationRenderer
from data_structures.DualTree import DualTree
from frontend.renderers.DualTreeRenderer import DualTreeRenderer
from frontend.Gobals import DEFAULT_FONT
import sys


#TEMP CODE FOR TESTING
INPUT_FILE = f"{sys.argv[1]}.json" if len(sys.argv) > 1 else "test1.json"
tri = TriangulationParser.parse(INPUT_FILE)
tri_flip = copy.deepcopy(tri)
tri_flip.flip_edge(0,2)
tri_flip.sanity_check(len(tri_flip.vertices))
d_tree = DualTree(tri)
d_tree.sanity_check(tri)
d_tree_rotated = DualTree(tri)
d_tree_rotated.rotate_left_by_face_id(4)

pygame.init()

V_WIDTH, V_HEIGHT = 1280, 720
screen = pygame.display.set_mode((V_WIDTH, V_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Sequential Squishing")

#--Renderers--
renderers: list[Renderer] = []

renderers.append(TriangulationRenderer(
    content=tri,
    anchor=Vector2(50, 50),
    bounds=Vector2(300, 300),
    margin=Vector2(20, 20),
    fill=True
))
renderers.append(TriangulationRenderer(
    content=tri_flip,
    anchor=Vector2(50, 400),
    bounds=Vector2(300, 300),
    margin=Vector2(20, 20),
    fill=True
))
renderers.append(DualTreeRenderer(
    content=d_tree,
    anchor=Vector2(700, 50),
    bounds=Vector2(300, 300),
))
renderers.append(DualTreeRenderer(
    content=d_tree_rotated,
    anchor=Vector2(700, 400),
    bounds=Vector2(300, 300)
))

font = DEFAULT_FONT

clock = pygame.time.Clock()
running = True

while running:
  #INPUTS
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False

  #LOGIC

  #RENDER
  screen.fill(Color.WHITE.value)

  #--triangulation rendering--

  #--test renderer--
  for renderer in renderers:
    renderer.render(screen)

  pygame.display.flip() #update full display (double buffers swap)
  clock.tick(60)