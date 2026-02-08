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
from data_structures.BinaryTree import BinaryTree
from frontend.renderers.BinaryTreeRenderer import BinaryTreeRenderer
from frontend.input_handlers.BinaryTreeInputHandler import BinaryTreeInputHandler
from frontend.Gobals import DEFAULT_FONT
import sys


SOURCE = f"{sys.argv[1]}.json"
TARGET = f"{sys.argv[2]}.json"
tri_s = TriangulationParser.parse(SOURCE)
d_tree_s = BinaryTree(tri_s)
d_tree_s.sanity_check(tri_s)
tri_t = TriangulationParser.parse(TARGET)
d_tree_t = BinaryTree(tri_t, (4,5))
d_tree_t.sanity_check(tri_t)

pygame.init()

V_WIDTH, V_HEIGHT = 1280, 720
screen = pygame.display.set_mode((V_WIDTH, V_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sequential Squishing")

#--Renderers--
PADDING = 20
CELL_SIZE = min((V_WIDTH - PADDING * 3) / 2, (V_HEIGHT - PADDING * 3) / 2)

renderers: list[Renderer] = []
# Source at top
renderers.append(TriangulationRenderer(
    content=tri_s,
    title=" [Source]",
    anchor=Vector2(PADDING, PADDING + 5),
    bounds=Vector2(CELL_SIZE, CELL_SIZE),
    margin=Vector2(20, 20),
    fill=True
))
renderers.append(BinaryTreeRenderer(
    content=d_tree_s,
    title=" [Source]",
    anchor=Vector2(PADDING * 2 + CELL_SIZE, PADDING + 5),
    bounds=Vector2(CELL_SIZE, CELL_SIZE),
    margin=Vector2(20, 20),
))
# Target at bottom
renderers.append(TriangulationRenderer(
    content=tri_t,
    title=" [Target]",
    anchor=Vector2(PADDING, PADDING * 2 + CELL_SIZE + 10),
    bounds=Vector2(CELL_SIZE, CELL_SIZE),
    margin=Vector2(20, 20),
    fill=True
))
renderers.append(BinaryTreeRenderer(
    content=d_tree_t,
    title=" [Target]",
    anchor=Vector2(PADDING * 2 + CELL_SIZE, PADDING * 2 + CELL_SIZE + 10),
    bounds=Vector2(CELL_SIZE, CELL_SIZE),
    margin=Vector2(20, 20),
))
#--Sync Network--
sync_network = SyncNetwork()
sync_network.register(renderers[0])  # Triangulation
sync_network.register(renderers[1])  # BinaryTree

#--Input Handlers--
input_handlers: list[InputHandler] = []
input_handlers.append(TriangulationInputHandler(
    renderer=renderers[0],  # TriangulationRenderer for tri
    sync_network=sync_network
))
input_handlers.append(BinaryTreeInputHandler(
    renderer=renderers[1],  # BinaryTreeRenderer for d_tree
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