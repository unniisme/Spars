from engine.Objects_2D.TileMap import GenerativeTileMap
from engine.Renderer.TileMapRenderer import GenerativeTileMapRenderer
from engine.Game import PyGameInstance


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

rend = GenerativeTileMapRenderer(grid, int(1000/max(rows, columns)))

print(grid)

game = PyGameInstance(rend.scale*columns, rend.scale*rows)
game.Start()

while game.isPlaying():

    game.initFrame()

    rend.Draw(game.screen)

    game.endFrame()
