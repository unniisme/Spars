from ..Objects import GameObject, Transform

class Rectangle(GameObject):

    def __init__(self, transform : Transform = Transform(), breadth = 0, height = 0):
        super().__init__(transform)
        self.breadth = breadth
        self.height = height

    
    # Getters

    def GetCorners(self):
        return [(i*self.breadth/2, j*self.height/2) for i in range(1,-1) for j in range(1,-1)]