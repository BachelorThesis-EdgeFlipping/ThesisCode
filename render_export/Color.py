from enum import Enum

#Color scheme for graph renders
class Color(Enum):
  WHITE       = (255, 255, 255)
  BLACK       = (0, 0, 0)
  RED         = (255, 0, 0)
  GREEN       = (0, 255, 0)
  BLUE        = (43, 92, 227)
  YELLOW      = (255, 255, 0)
  CYAN        = (0, 255, 255)
  MAGENTA     = (255, 0, 255)
  ORANGE      = (255, 165, 0)
  PURPLE      = (128, 0, 128)
  GRAY        = (128, 128, 128)
  LIGHT_GRAY  = (200, 200, 200)
  LIGHT_LIGHT_GRAY = (235, 235, 235)
  DARK_GRAY   = (50, 50, 50)
  PINK        = (255, 192, 203)
  LIME        = (50, 205, 50)
  TEAL        = (0, 128, 128)
  NAVY        = (0, 0, 128)
  MAROON      = (128, 0, 0)
  OLIVE       = (128, 128, 0)
  CORAL       = (255, 127, 80)
  SALMON      = (250, 128, 114)
  GOLD        = (255, 215, 0)
  TURQUOISE   = (64, 224, 208)
  INDIGO      = (75, 0, 130)
  VIOLET      = (238, 130, 238)
  LAVENDER    = (230, 230, 250)
  MINT        = (152, 255, 152)
  PEACH       = (255, 218, 185)
  SKY_BLUE    = (135, 206, 235)
  #light variants
  LIGHT_RED     = (255, 102, 102)
  LIGHT_GREEN   = (144, 238, 144)
  LIGHT_BLUE    = (173, 216, 230)
  LIGHT_YELLOW  = (255, 255, 153)
  LIGHT_CYAN    = (224, 255, 255)
  LIGHT_MAGENTA = (255, 153, 255)
  LIGHT_ORANGE  = (255, 200, 128)
  LIGHT_PURPLE  = (200, 162, 200)
  LIGHT_PINK    = (255, 224, 230)
  LIGHT_TEAL    = (128, 204, 204)
  LIGHT_CORAL   = (255, 180, 150)
  LIGHT_SALMON  = (255, 180, 170)
  #extra
  INVISIBLE   = (0, 0, 0, 0) #fully transparent
  #full transformation

  L_0_0 = (255, 70, 70)
  L_0_1 = LIGHT_LIGHT_GRAY #(255, 225, 225)
  L_0_2 = LIGHT_LIGHT_GRAY #(255, 235, 235)

  L_1_0 = (255, 120, 40)
  L_1_1 = LIGHT_LIGHT_GRAY #(255, 230, 210)
  L_1_2 = LIGHT_LIGHT_GRAY #(255, 240, 225)

  L_2_0 = (255, 200, 40)
  L_2_1 = LIGHT_LIGHT_GRAY #(255, 240, 200)
  L_2_2 = LIGHT_LIGHT_GRAY #(255, 248, 220)

  L_3_0 = (60, 200, 90)
  L_3_1 = LIGHT_LIGHT_GRAY #(210, 240, 210)
  L_3_2 = LIGHT_LIGHT_GRAY #(225, 248, 225)

  L_4_0 = (60, 140, 255)
  L_4_1 = LIGHT_LIGHT_GRAY #(210, 230, 255)
  L_4_2 = LIGHT_LIGHT_GRAY #(225, 240, 255)

  L_5_0 = (140, 60, 255)
  L_5_1 = LIGHT_LIGHT_GRAY #(230, 210, 255)
  L_5_2 = LIGHT_LIGHT_GRAY #(240, 225, 255)

  L_6_0 = (255, 60, 170)
  L_6_1 = LIGHT_LIGHT_GRAY #(255, 210, 235)
  L_6_2 = LIGHT_LIGHT_GRAY #(255, 225, 240)

  def value_normalized(self):
    return tuple(value / 255 for value in self.value)
