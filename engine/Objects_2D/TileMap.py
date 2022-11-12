from ..Grid import *
from ..Renderer.GridRenderer import GridRenderer

class Tile(GridCell):

    def __init__(self):
        # Abstraction right now
        pass


class Tilmap(Grid):
    
    def __init__(self, height, breadth):
        super().__init__(height, breadth, Tile)


class GenerativeTile(GridCell):

    def __init__(self, position, isTile = False):
        self.isTile = isTile

        super().__init__(position, int(isTile))

    def __bool__(self):
        return self.isTile

    def SetTile(self, val = True):
        self.isTile = val
        self.label = int(val)


class GenerativeTileMap(Grid):

    def __init__(self, breadth, height, layerMap : list):

        self.layerMap = layerMap

        super().__init__(height, breadth, GenerativeTile)
