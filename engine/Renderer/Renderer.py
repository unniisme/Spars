from ..Grid import *
from ..Objects import *
import pygame

class Camera2D(GameObject2D):

    def __init__(self, transform : Transform2D, screen):
        super().__init__(transform) # For now best kept and updated separately
        self.screen = screen
        GameObject.gameObjects[0].camera = self # Set global camera

    def OffsetPoint(self, pts):
        return [self.ToWorldSpace(pt).asTuple() for pt in pts]

    def SetTarget(self, target : GameObject2D):
        self.target = target
        self.selfOffset = self.transform.position - target.transform.position

    def Update(self, dt):
        if hasattr(self, 'target'):
            self.transform.position = self.target.transform.position + self.selfOffset
        # BUG: not working rn

        


class Renderer2D(GameObject2D):

    def __init__(self, transform : Transform):
        super().__init__(transform)

    def VectorListToRenderer(self, l : list):
        return list(map(Vector2.asTuple, map(self.ToWorldSpace, l)))

    def Draw(self):
        pass

    def FetchCamera():
        return GameObject.gameObjects[0].camera

    def Update(self, dt):
        self.Draw()



class GridRenderer(Renderer2D):

    def __init__(self, transform : Transform, grid : Grid, scale):
        """
        Scale is the length of a side of the grid in number of pygame screen pixels
        """
        self.grid = grid
        self.scale = scale

        super().__init__(transform)

    def Draw(self):
        camera = Renderer2D.FetchCamera()
        for i in range(self.grid.height):
            for j in range(self.grid.breadth):
                self.RenderCell(i, j, camera)

    def CellCentre(self, i, j):
        scale = self.scale
        return ((i*scale) + (scale/2) , (j*scale) + (scale/2))

    def RenderCell(self, i, j, camera):
        pass