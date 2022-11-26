from engine import *


root = Scene2D(Transform2D.Null("Root"))

game = PyGameInstance(800, 600)
camera = Camera2D(Transform2D.Null("Camera"), game.screen)

box = Rectangle(Transform2D((50,50), 0, "Box"), 20, 20)
poly = Polygon(Transform2D((200,200), 0, "Polygon"), [(-100,0), (-100, 100), (0,100), (100,0), (0,-100) ])
circ = Circle(Transform2D((400,400), 0, "Circle"), 100)
boxRend = ShapeRenderer2D(Transform2D.Null("Box Renderer"), box)
plyRend = ShapeRenderer2D(Transform2D.Null("Polygon Renderer"), poly)
circRend = ShapeRenderer2D(Transform2D.Null("Circle Renderer"), circ)


randomObj = GameObject2D(Transform2D((400,400), 0, "Dude"))
randomObj.AttachChild(circRend)



print(root.ToTreeString())
game.Start()

while game.isPlaying():

    game.initFrame()

    R = camera.ToTransformSpace(pygame.mouse.get_pos())

    boxRend.color = (0,200,0) if box.Contains(R) else (200,0,0)
    plyRend.color = (0,200,0) if poly.Contains(R) else (200,0,0)
    circRend.color = (0,200,0) if circ.Contains(R) else (200,0,0)

    root.doUpdate(0.1)


    if pygame.key.get_pressed()[pygame.K_LEFT]:
        randomObj.UpdatePosition((-2,0))
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        randomObj.UpdatePosition((2,0))
    if pygame.key.get_pressed()[pygame.K_UP]:
        randomObj.UpdatePosition((0,-2))
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        randomObj.UpdatePosition((0,2))
    
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        print(circ.transform.position)
    

    game.endFrame()
