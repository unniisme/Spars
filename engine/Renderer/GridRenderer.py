from ..Grid import *
from ..Objects import *
import pygame

class GridRenderer(GameObject):

    def __init__(self, grid : Grid, scale):
        """
        Scale is the length of a side of the grid in number of pygame screen pixels
        """
        self.grid = grid
        self.scale = scale

        super().__init__(Transform2D.Null())

    def Draw(self, screen):
        for i in range(self.grid.height):
            for j in range(self.grid.breadth):
                self.RenderCell(i, j, screen)

    def CellCentre(self, i, j):
        scale = self.scale
        return ((i*scale) + (scale/2) , (j*scale) + (scale/2))

    def RenderCell(self, i, j, screen):
        pass