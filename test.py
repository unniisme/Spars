from engine.Objects_2D.TileMap import GenerativeTileMap
from engine.Renderer.TileMapRenderer import GenerativeTileMapRenderer
from engine.Renderer.ShapeRenderer import ShapeRenderer2D
from engine.Objects_2D.Shapes import Shape2D, Rectangle
from engine.Game import PyGameInstance
from engine.Objects import Transform2D
import pygame
from engine.utils.math_utils import Vector2

gridFile = 'grid1'
    # Load grid from file
file = open(gridFile, 'r')    

rows,columns = map(int, file.readline().split())

grid = GenerativeTileMap(rows, columns, [{'col': (200,0,0)}, {'col': (10,10,10), 'thickness' : 10}])
for i in range(rows):
    for j,c in enumerate(file.readline().split()):
        if c != '0':
            grid[i,j].SetTile()

file.close()

rend = GenerativeTileMapRenderer(Transform2D.Null(), grid, int(1000/max(rows, columns)))
box = Rectangle(Transform2D((50,50,50), 0), 20, 20)
boxRend = ShapeRenderer2D(Transform2D.Null(), box)

print(grid)

game = PyGameInstance(rend.scale*columns, rend.scale*rows)
game.Start()

while game.isPlaying():

    game.initFrame()

    rend.Draw(game.screen)

    col = (0,200,0) if box.Contains(pygame.mouse.get_pos()) else (200,0,0)

    if box.Contains(pygame.mouse.get_pos()):
        print("Yes")

    boxRend.Draw(game.screen, col)

    if pygame.key.get_pressed()[pygame.K_LEFT]:
        rend.UpdatePosition(Vector2(-0.2,0))

    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        rend.UpdatePosition(Vector2(0.2,0))
    
    if pygame.key.get_pressed()[pygame.K_UP]:
        rend.UpdateRotation(0.02)

    if pygame.key.get_pressed()[pygame.K_DOWN]:
        rend.UpdateRotation(-0.02)

    game.endFrame()
