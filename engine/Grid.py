from .utils.math_utils import *

#data structures to represent a grid and its components

#A GridCell is what is in each cell of the grid. Only includes non-moving objects
class GridCell:
    """
    Constuctor for class GridCell
    Constructor(position, lable)
    Position is a tuple (or any iterable) that holds x and y coordinates
    label is anything that can be represented as a string, so that it can be printed 
    """

    def __init__(self, position : tuple, label = '0'):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.label = label
        self.objects = []

    def __str__(self):
        return (str(self.label) if len(self.objects) == 0 else self.objects[0].label[0])

    def GetPosition(self):
        """Returns position of the gridCell"""
        return self.position

    def GetLabel(self):
        """Returns the label of the gridCell"""
        return self.label

#Class that holds an array of gridcells as well as objects on this grid
class Grid:
    """
    Constructor for class Grid
    Constructor(height, breadth, gridCellConstructor)
    breadth is initialized to height if left empty
    gridCellConstructor is the constructor (usually class name) of the gridCell used in the grid
    """
    """
    Class for grid
    each cell in the grid is represented by a gridcell

    variables:
    height, breadth - Dimensions of the grid
    grid - an 2x2 array of gridCells
    objects - a list of objects that are present on the grid
    
    functions:
    GetCell(x,y) - return the gridCell at the given position
        note, `Grid[(x,y)]` works identically
    SetCell(x,y, newCell) - sets the cell at the given postion to newCell
        note, `Grid[(x,y)] = newCell` works identically
    inBound(x,y) - returns if the given position is in the grid
    CellInDirection(position, direction) - postion from the given postion in the given direction
        returns none if the successor position is outside the grid
    
    GridToString() - a debug function to print the grid and all objects in it
        note, print(Grid) does the same thing
    """

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, height : int, breadth : int =None, gridCellConstructor : 'function' = GridCell):
        if breadth == None:
            breadth = height
        
        self.height = height
        self.breadth = breadth
        self.objects = []        #Holds the list of objects in the grid
        self.grid = [ [ None for y in range( breadth ) ] for x in range( height ) ]
        self.objectGrid = None
        self.gridCellSet = set()
        self.objectSet = set()

        for j in range(height):
            for i in range(breadth):
                gridCell = gridCellConstructor((i, j))
                self.SetCell(i, j, gridCell)


    def InitObjectGrid(self):
        self.objectGrid = Grid(self.height, self.breadth, lambda null: None)
        for gameObject in self.objects:
            self.objectGrid[gameObject.position] = gameObject

    def NewObject(self, gameObject):
        """Function to be called when a new object is added to the grid"""
        self.objectGrid[gameObject.transform.position] = gameObject
        self.objects.append(gameObject)

    def DelObject(self, gameObject):
        """Function to be called when an object is removed from the grid"""
        self.objectGrid[gameObject.transform.position] = None
        self.objects.remove(gameObject)

    def MoveObject(self, positionFrom, positionTo):
        """Funcion to be called to update the position of an object in the grid"""
        self.objectGrid[positionTo], self.objectGrid[positionFrom] = self.objectGrid[positionFrom], None
              
    def GetCell(self, x, y):
        if not self.inBound(x,y):
            return GridError.out_of_bound()
        return self.grid[y][x]

    def SetCell(self, x, y, gridCell):
        if not self.inBound(x,y):
            return GridError.out_of_bound()
        self.grid[y][x] = gridCell
        return

    def __getitem__(self, position):
        if position == None:
            return None
        return self.GetCell(position[0], position[1])

    def __setitem__(self, position, gridCell):
        if position == None:
            return
        self.SetCell(position[0], position[1], gridCell)

    def __str__(self):
        return self.GridToString()

    def inBound(self, x, y):
        return 0<=x<self.breadth and 0<=y<self.height

    def CellInDirection(self, position : tuple, direction : float, distance = 1):
        """
        Returns the position of the cell that is at given direction from given position
        """
        VectorToCell = Vector2.PolarConstructorDeg(distance, direction)
        newCell = (Vector2(position[0], position[1]) + VectorToCell).IntClamp().asTuple()
        if not self.inBound(newCell[0], newCell[1]):
            return None
        return newCell

    def GridCellInDirection(self, position : tuple, direction : float, distance = 1):
        """
        Returns the gridCell in the given direction from given position
        """
        position = self.CellInDirection(position, direction, distance)
        if position == None:
            return None
        return self[position]

    def RayCastDir(self, position : tuple, direction : float, distance = -1, objectTypeMask : list = [], cellMask : list = [], distanceInGridCells : bool = False) -> 'RayCastData':
        """
        Casts a ray in the given direction. Returns a raycast datatype
        """
        if distance == -1: #effectively infinite distance
            distance = self.breadth+self.height

        hit = False
        castDistance = 0
        nextCell = position
        while not hit:
            nextCell = self.CellInDirection(nextCell, direction)
            if nextCell == None:
                return RayCastData()
                
            if castDistance > distance:
                break
            if distanceInGridCells:
                castDistance += 1
            else:
                castDistance = (Vector2(position) - Vector2(nextCell)).Magnitude()

            if self[nextCell].label in cellMask:
                return RayCastData(postion, nextCell, self[nextCell], castDistance)
            if type(self.objectGrid[nextCell]) in objectTypeMask:
                return RayCastData(postion, nextCell, self.objectGrid[nextCell], castDistance)
        
        return RayCastData()

    def RayCast(self, *args, **kwargs):
        """
        Wrapper function for raycasting
        Directional Raycasting:
        RayCast(position, direction, distance, objectTypeMask, cellLabelMask)
        
        Point to point raycasting:
        RayCast(position, endPosition, objectTypeMask, cellMask)
        """
        if type(args[1]) == float or type(args[1]) == int: #Directional raycasting
            return self.RayCastDir(*args, **kwargs)
        if type(args[1]) == tuple: #point to point raycasting
            position = args[0]
            dirVector = Vector2(args[1]) - Vector2(position)
            direction = Vector2.AngleDeg(dirVector)
            distance = dirVector.Magnitude()
            kwargs["distance"] = distance

            return self.RayCastDir(position, direction, **kwargs)
        
        raise TypeError("Unknown Input type")

            
        
    def GetObjectPositions(self):
        return [gameObject.transform.position.IntClamp().asTuple() for gameObject in self.objects]

    def GridToString(self, spacing = " "):
        string = ""
        transformPositions = self.GetObjectPositions()
        for j in range(self.height):
            for i in range(self.breadth):
                if (i,j) in transformPositions:
                    string += str(self.objects[transformPositions.index((i,j))]) + spacing
                else:
                    string += str(self[(i,j)]) + spacing
            string += '\n'
        return string

#Directions are handled as angles in degree from positive x axis
class Direction:
    LEFT = 180
    UP = 90
    RIGHT = 0
    DOWN = 270


def BresenhamLine(start : tuple, end : tuple) -> list:
    """
    Function to draw the Bresenham Line between 2 points, yields all cells that a line between 2 cells pass through
    """ 
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    def xline(start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        yi = 1

        if dy<0:
            yi = -1
            dy = -dy


        D = (2*dy) - dx
        y = start[1]

        for x in range(start[0], end[0]):
            yield (x,y)
            if D>0:
                y = y+yi
                D = D + 2*(dy - dx)
            else:
                D = D + 2*dy

    outlist = []
    #slopes -1 to 0 to 1
    if dx >= abs(dy):
        outlist = list(xline(start, end))
        if len(outlist) == 0:
            return outlist
        outlist.pop(0)

    #slopes 1 to inf to -1
    if dy > abs(dx):
        for point in xline((start[1], start[0]), (end[1], end[0])):
            outlist.append((point[1], point[0]))
        outlist.pop(0)

    #slopes -1 to 0 to 1
    if -dx >= abs(dy):
        outlist = list(xline(end, start))
        if len(outlist) == 0:
            return outlist
        outlist.reverse()
        outlist.pop()

    #slopes 1 to inf to -1
    if -dy > abs(dx):
        for point in xline((end[1], end[0]), (start[1], start[0])):
            outlist.append((point[1], point[0]))
        outlist.reverse()
        outlist.pop()

    return outlist

def ManhattenDistance(cell1, cell2):
    return abs(cell1.x - cell2.x) + abs(cell1.y-cell2.y)
    
    

class GridError:
    
    def out_of_bound():
        raise IndexError

class RayCastData:
    """Holds the data pertaining to a raycast.
    
    Constructors:
    RayCastData() returns a miss instance
    RayCastData(rayPos, hitPos, object, depth) """

    def __init__(self, *args):
        if len(args) == 0: #Null constructor
            self.hit = False
            self.distance = 0
            self.object = None
            self.point = (0,0)
            self.depth = 0
            return
        if len(args) == 5:
            rayPos, hitPos, obj, depth, self.flags = args
        if len(args) == 4:
            rayPos, hitPos, obj, depth = args
        if len(args) == 3:
            rayPos, hitPos, obj = args
            depth = -1

        self.hit = True
        self.distance = (Vector2(hitPos) - Vector2(rayPos)).magnitude
        self.object = obj
        self.point = hitPos
        self.depth = depth

    def __str__(self):
        if not self.hit:
            return "Miss"
        else:
            return "Hit " + str(self.object)

    def __bool__(self):
        return self.hit