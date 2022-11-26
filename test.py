from engine import *

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


box = Rectangle(Transform2D((50,50), 0, "Box"), 20, 20)
poly = Polygon(Transform2D((200,200), 0, "Polygon"), [(-100,0), (-100, 100), (0,100), (100,0), (0,-100) ])
circ = Circle(Transform2D((400,400), 0, "Circle"), 100)
boxRend = ShapeRenderer2D(Transform2D.Null("Box Renderer"), box)
plyRend = ShapeRenderer2D(Transform2D.Null("Polygon Renderer"), poly)
circRend = ShapeRenderer2D(Transform2D.Null("Circle Renderer"), circ)

root = GameObject2D(Transform2D.Null("Root"))
root.AttachChild(boxRend)
root.AttachChild(plyRend)
root.AttachChild(circRend)

print(root.ToTreeString())

game = PyGameInstance(800, 600)
game.Start()

while game.isPlaying():

    game.initFrame()

    boxcol = (0,200,0) if box.Contains(pygame.mouse.get_pos()) else (200,0,0)
    polycol = (0,200,0) if poly.Contains(pygame.mouse.get_pos()) else (200,0,0)
    circcol = (0,200,0) if circ.Contains(pygame.mouse.get_pos()) else (200,0,0)

    boxRend.Draw(game.screen, boxcol)
    plyRend.Draw(game.screen, polycol)
    circRend.Draw(game.screen, circcol)

    game.endFrame()
