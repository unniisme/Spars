from .GridRenderer import GridRenderer
from ..Objects_2D.TileMap import GenerativeTileMap
from ..utils.math_utils import Vector2
import pygame


class GenerativeTileMapRenderer(GridRenderer):

    def __init__(self, tileMap : GenerativeTileMap, scale):

        super().__init__(tileMap, scale)

    def RenderCell(self, i, j, screen):
        scale = self.scale

        if self.grid[i,j]: 
            pygame.draw.rect(screen, self.grid.layerMap[0]["col"], pygame.Rect(i*scale, j*scale, scale, scale))
        else:
            return
        
        # Edges
        dirs = [0, 90, 180, 270]
        for d in dirs:
            newTile = self.grid.GridCellInDirection((i,j), d)
            if newTile == None:
                continue
                
            if not newTile:
                # only 1 layer here
                ptv = Vector2(self.CellCentre(i, j)) + Vector2.PolarConstructorDeg(scale/2, d)
                spanv = Vector2.PolarConstructorDeg(scale/2, d+90)
                backv = Vector2.PolarConstructorDeg(self.grid.layerMap[1]['thickness'], d+180)
                pts = [(ptv + spanv).asTuple(), (ptv - spanv).asTuple(), (ptv - spanv + backv).asTuple(), (ptv + spanv + backv).asTuple()]

                pygame.draw.polygon(screen, self.grid.layerMap[1]['col'], pts)

        # Corners
        dirs = [45, 135, -135, -45]
        for d in dirs:
            newTile = self.grid.GridCellInDirection((i,j), d)
            if newTile == None:
                continue
                
            if not newTile:
                # only 1 layer here
                ptv = Vector2(self.CellCentre(i, j)) + Vector2.PolarConstructorDeg(scale/2, d+45) + Vector2.PolarConstructorDeg(scale/2, d-45)
                dxv = -Vector2.PolarConstructorDeg(self.grid.layerMap[1]['thickness'], d+45)
                dyv = -Vector2.PolarConstructorDeg(self.grid.layerMap[1]['thickness'], d-45)
                pts = [(ptv + dxv).asTuple(), (ptv + dyv + dxv).asTuple(), (ptv + dyv).asTuple(), (ptv).asTuple()]

                pygame.draw.polygon(screen, self.grid.layerMap[1]['col'], pts)
        
