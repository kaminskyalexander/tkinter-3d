from game.geometry import getDotProduct, findNormal, intersection
from game.polygon import Polygon
from game.setup import time

class Node:
    def __init__(self, polygon):
        self.polygon = polygon
        self.front = None
        self.back = None

def buildSubtree(polygons):
    polygons = polygons[:]
    if polygons:
        rootPoly = polygons[0]
        polygons.remove(rootPoly)
        rootNode = Node(rootPoly)

        # Find normal vector of root polygon 
        normal = findNormal(*rootPoly.frame[:3])
        # Values for plane equation of root polygon
        a, b, c = normal
        d = -(rootPoly.frame[0].x * a + rootPoly.frame[0].y * b + rootPoly.frame[0].z * c)

        frontList = []
        backList = []
        for p in polygons:
            # Determines if each vertex is in front of or behind the root polygon
            sides = []
           # print(p.frame, p.properties)
            for vertex in p.frame:
                dp = getDotProduct(normal, (vertex - rootPoly.frame[0]))
                if dp > 0:
                    sides.append(1)
                elif dp < 0:
                    sides.append(0)
                else:
                    sides.append(None)
            
            print(sides)
            # In front
            if 1 in sides and not 0 in sides:
                frontList.append(p)

            # Behind
            elif 0 in sides and not 1 in sides:
                backList.append(p)

            # Intersecting
            else:
                toggle = 0
                splitPolygon = [[],[]]
                
                for i, vertex in enumerate(p.frame):
                    before = p.frame[i - 1]
                    # If the edge is not intersecting the plane
                    if sides[i] == sides[i - 1]:
                        splitPolygon[toggle].append(before)
                    else:
                        poi = intersection(a, b, c, d, *before, *vertex)
                        splitPolygon[toggle].append(before)
                        splitPolygon[toggle].append(poi)
                        toggle = 1 if not toggle else 0
                        splitPolygon[toggle].append(poi)
                backList.append( Polygon(p.canvas, *splitPolygon[0], debug = p.debug, **p.properties))
                frontList.append(Polygon(p.canvas, *splitPolygon[1], debug = p.debug, **p.properties))
        rootNode.front = buildSubtree(frontList)
        rootNode.back = buildSubtree(backList)
        return rootNode