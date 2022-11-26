from ..Objects import GameObject2D, Transform2D
from ..utils.math_utils import *


# TODO: Lots of error catching
class Shape2D(GameObject2D):

    shapes = []  # Global list of shapes

    def __init__(self, transform:Transform2D):
        super().__init__(transform)
        Shape2D.shapes.append(self)
        ## NOTE: Rotation should be zero for now, else screws up

    def __del__(self):
        Shape2D.shapes.remove(self)

    def VectorsToWorldSpace(self, pts : list):
        return [self.ToWorldSpace(v).asTuple() for v in pts]

    # Queries
    # NOTE: All query functions return in world space
    def GetCorners(self) -> list:
        """
        Get corners of the shape in world space
        """
        pass

    def Contains(self, pt) -> bool:
        """
        Returns if the given point is inside this shape
        """
        pass

    def RayCastHit(self, pt, dir) -> bool:
        """
        Returns if a raycast from the given point in the given direction hits this object
        """
        pass

class Rectangle(Shape2D):

    def __init__(self, transform : Transform2D, breadth, height):
        super().__init__(transform)
        self.breadth = breadth
        self.height = height

    def __del__(self):
        super().__del__()
    
    # Queries

    def GetCorners(self):
        """
        Get corners of the rectangle transformed to world space
        """
        pts = [self.ToWorldSpace((i*self.breadth/2, j*self.height/2)).asTuple() for i in (1,-1) for j in (1,-1)]
        pts[0], pts[1] = pts[1], pts[0] # So that vertices are in the right order for polygon rendering
        return pts
    
    def Contains(self, pt) -> bool:
        """
        Check if a point is in the rectangle in world space.
        pt is assumed to be in world space
        """
        ptv = self.ToTransformSpace(pt) 
        return (-self.breadth/2) <= ptv[0] <= (self.breadth/2) and (-self.height/2) <= ptv[1] <= (self.height/2)

    def RayCastHit(self, pt, dir) -> bool:
        #Hmmm TODO: Figure this out
        pass


class Polygon(Shape2D):

    def __init__(self, transform : Transform2D, points : list):
        super().__init__(transform)
        self.points = points

    def __del__(self):
        super().__del__()

    # Internal queries

    def CountRayCast(self, rayStart, rayDir) -> int:
        """
        Returns the number of times a ray intersects the shape
        Returns in local space
        """

        edges = list(zip(self.points, self.points[1:])) + [(self.points[-1], self.points[0])]

        intersectionCount = 0
        for edge in edges:
            if RaySegmentIntersection(Vector2(rayStart), Vector2(rayDir), Vector2(edge[0]), Vector2(edge[1])):
                intersectionCount += 1

        return intersectionCount


    # Queries

    def GetCorners(self) -> list:
        return self.VectorsToWorldSpace(self.points)

    def Contains(self, pt) -> bool:
        rayStart = self.ToTransformSpace(pt)
        rayDir = Vector2.LEFT()

        return (self.CountRayCast(rayStart, rayDir)%2 == 1)

    def RayCastHit(self, rayStart, rayDir) -> bool:
        return (self.CountRayCast(rayStart, rayDir) > 0)

class Circle(Shape2D):

    def __init__(self, transform, radius):
        super().__init__(transform)

        self.radius = radius
        self.centre = (0,0) # Centre of transform

    def __del__(self):
        super().__del__()


    # Query functions

    def GetCorners(self, resolution = 1):
        """
        Returns 360/resolution points that approximate the circle
        Not recommended, as it is better directly draw a circle using pygame functions

        #NOTE : This is the only function that acutally uses degrees for angles I think
        """

        n = int(360/resolution)

        pts = [Vector2.PolarConstructorDeg(self.radius, i*resolution) for i in range(n)]
        return self.VectorsToWorldSpace(pts)

    def Contains(self, pt) -> bool:
        pt = self.ToTransformSpace(pt)
        return pt.magnitude <= self.radius

    def RayCastHit(self, pt, d) -> bool:
        d = Vector2(d)
        pt = self.ToTransformSpace(pt)
        mu = pt.Dot(d)/d.SqMagnitude()
        
        if mu<0:
            return False

        return self.Contains(pt + d*mu)




def RaySegmentIntersection(rayStart : Vector2, rayDir : Vector2, a : Vector2, b : Vector2) -> bool:
    """
    Check if ray (rayStart + mu*rayDir) instersects line segment (a-b) + gamma*b
    mu >= 0
    0 <= gamma <= 1 
    """
    d = rayDir.Normalized()

    # Parallel
    if d.Cross(a - b) == 0:
        return False

    mu = (b.Cross(a) + a.Cross(rayStart) + rayStart.Cross(b)) / d.Cross(a - b)
    gamma = d.Cross(rayStart-b) / d.Cross(a-b) 

    if not (mu >= 0 and 0 <= gamma <= 1):
        return False

    return True



