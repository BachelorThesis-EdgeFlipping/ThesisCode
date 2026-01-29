import pygame
import copy
from pygame.math import Vector2
from SyncNetwork import SyncNetwork
from frontend.Gobals import Color
from ParsingService import TriangulationParser
import data_structures.Triangulation
from frontend.input_handlers.TriangulationInputHandler import TriangulationInputHandler
from frontend.input_handlers.InputHandler import InputHandler
from frontend.renderers.Renderer import Renderer
from frontend.renderers.TriangulationRenderer import TriangulationRenderer
from data_structures.DualTree import DualTree
from frontend.renderers.DualTreeRenderer import DualTreeRenderer
from frontend.input_handlers.DualTreeInputHandler import DualTreeInputHandler
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
renderers: list[Renderer] = []
renderers.append(TriangulationRenderer(
    content=tri,
    anchor=Vector2(20, 50),
    bounds=Vector2(600, 600),
    margin=Vector2(20, 20),
    fill=True
))
renderers.append(DualTreeRenderer(
    content=d_tree,
    anchor=Vector2(640, 50),
    bounds=Vector2(600, 600),
    margin=Vector2(20, 20),
))

#--Sync Network--
sync_network = SyncNetwork()
sync_network.register(renderers[0])  # Triangulation
sync_network.register(renderers[1])  # DualTree

#--Input Handlers--
input_handlers: list[InputHandler] = []
input_handlers.append(TriangulationInputHandler(
    renderer=renderers[0],  # TriangulationRenderer for tri
    sync_network=sync_network
))
input_handlers.append(DualTreeInputHandler(
    renderer=renderers[1],  # DualTreeRenderer for d_tree
    sync_network=sync_network
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
    for handler in input_handlers:
      handler.handle_event(event)

  #RENDER
  screen.fill(Color.WHITE.value)
  for renderer in renderers:
    renderer.render(screen)

  pygame.display.flip() #update full display (double buffers swap)
  clock.tick(60)