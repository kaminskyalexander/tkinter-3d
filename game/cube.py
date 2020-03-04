from game.setup import *
from game.world import World
from game.polygon import Polygon

class Cube(World):

    def __init__(self, size = 1):
        polygons = [
            # Bottom
        	Polygon(
        		canvas,
        		Vector(-size, -size, -size),
        		Vector( size, -size, -size),
        		Vector( size, -size,  size),
        		Vector(-size, -size,  size),
        		fill = "#f0f"
        	),
        	# Front
        	Polygon(
        		canvas,
        		Vector(-size,  size, -size),
        		Vector(-size, -size, -size),
        		Vector( size, -size, -size),
        		Vector( size,  size, -size),
        		fill = "#f00"
        	),
        	# Left
        	Polygon(
        		canvas,
        		Vector(-size,  size, -size),
        		Vector(-size, -size, -size),
        		Vector(-size, -size,  size),
        		Vector(-size,  size,  size),
        		fill = "#ff0"
        	),
        	# Right
        	Polygon(
        		canvas,
        		Vector( size,  size, -size),
        		Vector( size, -size, -size),
        		Vector( size, -size,  size),
        		Vector( size,  size,  size),
        		fill = "#0f0"
        	),
        	# Back
        	Polygon(
        		canvas,
        		Vector(-size,  size,  size),
        		Vector(-size, -size,  size),
        		Vector( size, -size,  size),
        		Vector( size,  size,  size),
        		fill = "#0ff"
        	),
        	# Top
        	Polygon(
        		canvas,
        		Vector(-size,  size, -size),
        		Vector( size,  size, -size),
        		Vector( size,  size,  size),
        		Vector(-size,  size,  size),
        		fill = "#00f"
        	)
        ]
        super().__init__(*polygons)
