from ..Objects_2D.Shapes import *
from .Renderer import Renderer2D
from ..Objects import *
import pygame

class ShapeRenderer2D(Renderer2D):

    def __init__(self, transform:Transform2D, shape:Shape2D):
        super().__init__(transform)
        self.shape = shape

    def Draw(self, screen, color):
        pygame.draw.polygon(screen, color, self.VectorListToRenderer(self.shape.GetCorners()))
        
