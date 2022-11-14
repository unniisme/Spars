from .Renderer import GridRenderer
from ..Objects_2D.TileMap import GenerativeTileMap
from ..utils.math_utils import Vector2
import pygame


class GenerativeTileMapRenderer(GridRenderer):

    def __init__(self, transform, tileMap : GenerativeTileMap, scale):

        super().__init__(transform, tileMap, scale)

    def RenderCell(self, i, j, screen):
        scale = self.scale

        if self.grid[i,j]: 
            basev = Vector2(i,j)*scale
            dxv = Vector2(1,0)*scale
            dyv = Vector2(0,1)*scale
            pts = self.VectorListToRenderer([basev, basev+dxv, basev+dxv+dyv, basev+dyv])
            pygame.draw.polygon(screen, self.grid.layerMap[0]["col"], pts)
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
                #pts = [(ptv + spanv).asTuple(), (ptv - spanv).asTuple(), (ptv - spanv + backv).asTuple(), (ptv + spanv + backv).asTuple()]
                pts = self.VectorListToRenderer([(ptv + spanv), (ptv - spanv), (ptv - spanv + backv), (ptv + spanv + backv)])

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
                pts = self.VectorListToRenderer([(ptv + dxv), (ptv + dyv + dxv), (ptv + dyv), (ptv)])

                pygame.draw.polygon(screen, self.grid.layerMap[1]['col'], pts)
        
