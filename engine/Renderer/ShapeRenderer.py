from ..Objects_2D.Shapes import *
from .Renderer import Renderer2D, Camera2D
from ..Objects import *
import pygame

class ShapeRenderer2D(Renderer2D):

    def __init__(self, transform:Transform2D, shape:Shape2D, color : tuple = (200,0,0), attachAsChild = True):
        super().__init__(transform) # Renderer transform is irrelevent
        self.shape = shape
        self.color = color

        if attachAsChild:
            self.AttachChild(shape)


    def Draw(self):
        camera = Renderer2D.FetchCamera()
        pygame.draw.polygon(camera.screen, self.color, camera.OffsetPoint(self.shape.GetCorners()))
        
