import pygame
from pygame.math import Vector2
from typing import Tuple

from frontend.renderers.RenderPos import RenderPos

def vec2_to_tuple(v: Vector2) -> Tuple[int, int]:
    return (int(v.x), int(v.y))

def vec2_to_renderpos(v: Vector2) -> 'RenderPos':
    return RenderPos(int(v.x), int(v.y))