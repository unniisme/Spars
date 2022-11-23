from ..Objects import GameObject2D, Transform2D

class Shape2D(GameObject2D):
    def __init__(self, transform:Transform2D):
        super().__init__(transform)

    # Queries

    def GetCorners(self) -> list:
        pass

    def Contains(self, pt) -> bool:
        pass


class Rectangle(Shape2D):

    def __init__(self, transform : Transform2D, breadth, height):
        super().__init__(transform)
        self.breadth = breadth
        self.height = height
    
    # Queries

    def GetCorners(self):
        """
        Get corners of the rectangle transformed to world space
        """
        pts = [self.ToWorldSpace((i*self.breadth/2, j*self.height/2)).asTuple() for i in (1,-1) for j in (1,-1)]
        pts[0], pts[1] = pts[1], pts[0]
        return pts
    
    def Contains(self, pt) -> bool:
        """
        Check if a point is in the rectangle in world space.
        pt is assumed to be in world space
        """
        ptv = self.ToTransformSpace(pt)
        return (-self.breadth/2) <= ptv[0] <= (self.breadth/2) and (-self.height/2) <= ptv[1] <= (self.height/2)


