import pygame
from pygame.math import Vector2
from frontend.Gobals import Color
from ParsingService import TriangulationParser
import data_structures.Triangulation
from frontend.renderers.TriangulationRenderer import TriangulationRenderer
from data_structures.DualTree import DualTree
from frontend.renderers.DualTreeRenderer import DualTreeRenderer
from frontend.Gobals import DEFAULT_FONT
import sys


#TEMP CODE FOR TESTING
INPUT_FILE = f"{sys.argv[1]}.json" if len(sys.argv) > 1 else "test1.json"
tri = TriangulationParser.parse(INPUT_FILE)
d_tree = DualTree(tri)
d_tree.sanity_check(tri)

pygame.init()

V_WIDTH, V_HEIGHT = 1280, 720
screen = pygame.display.set_mode((V_WIDTH, V_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Sequential Squishing")

#--Renderers--
triangulation_renderer = TriangulationRenderer(
    content=tri,
    anchor=Vector2(50, 50),
    bounds=Vector2(600, 600),
    margin=Vector2(20, 20),
    fill=True
)
dualtree_renderer = DualTreeRenderer(
    content=d_tree,
    anchor=Vector2(700, 50),
    bounds=Vector2(400, 400),
)

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
  triangulation_renderer.render(screen)
  dualtree_renderer.render(screen)

  pygame.display.flip() #update full display (double buffers swap)
  clock.tick(60)