from enum import Enum
from pygame import font

font.init()
DEFAULT_FONT = font.SysFont(None, 24)

class Color(Enum):
  WHITE       = (255, 255, 255)
  BLACK       = (0, 0, 0)
  RED         = (255, 0, 0)
  GREEN       = (0, 255, 0)
  BLUE        = (0, 0, 255)
  YELLOW      = (255, 255, 0)
  CYAN        = (0, 255, 255)
  MAGENTA     = (255, 0, 255)
  ORANGE      = (255, 165, 0)
  PURPLE      = (128, 0, 128)
  GRAY        = (128, 128, 128)
  LIGHT_GRAY  = (200, 200, 200)
  DARK_GRAY   = (50, 50, 50)