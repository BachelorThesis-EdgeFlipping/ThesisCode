
from pygame import Vector2


class RenderPos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __sub__(self, other) -> 'RenderPos':
        if isinstance(other, RenderPos):
            return RenderPos(self.x - other.x, self.y - other.y)
        return RenderPos(self.x - other, self.y - other)

    def __add__(self, other) -> 'RenderPos':
        if isinstance(other, RenderPos):
            return RenderPos(self.x + other.x, self.y + other.y)
        return RenderPos(self.x + other, self.y + other)
    
    def __mul__(self, other: int) -> 'RenderPos':
        return RenderPos(self.x * other, self.y * other)
    
    def __rmul__(self, other: int) -> 'RenderPos':
        return RenderPos(self.x * other, self.y * other)
    
    def tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
      
    @staticmethod
    def from_vector2(v: Vector2) -> 'RenderPos':
        return RenderPos(int(v.x), int(v.y))
    
    @staticmethod
    def square_from_int(x: int) -> 'RenderPos':
        return RenderPos(x, x)