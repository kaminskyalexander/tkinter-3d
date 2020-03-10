from game.geometry import intersection
from core.vector import Vector

a, b, c, d = 0, 0, 1, 0
point = Vector(1, 1, 0)
point2 = Vector(1, -1, 0)
print(intersection(a, b, c, d, *point, *point2))
