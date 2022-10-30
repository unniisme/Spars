import pygame
from utils.math_utils import *

## A barebone 3d renderer test

class Camera:

    def __init__(self, centre, focus = None, width = None, height = None, direction = None):
        self.centre = centre
        self.focus = focus
        self.direction = direction

class Mesh:

    def __init__(self, points, color):
        self.points = points
        self.color = color

    def IsomtericProjection(self):
        # For now assuming camera at origin facing (0,0,1)
        return [Vector2(x).asTuple() for x in self.points]

class Box:
    def __init__(self, semiwidth, centre, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.semiwidth = semiwidth
        self.centre = centre

        x = Vector3.SphericalConstructorDeg(1, alpha, beta)
        try:
            y = x.Cross(Vector3.X()).Normalized()
        except:
            y = Vector3.UP()
        z = Vector3.Cross(x, y)

        self.faces = []
        points = [(Vector3(centre) + semiwidth*(x+i*y+j*z)).asTuple() for i in [-1,1] for j in [1,-1]]
        self.faces.append(Mesh(points, (100,100,0)))
        points = [Vector3(centre) + semiwidth*(i*x+y+j*z) for i in [-1,1] for j in [1,-1]]
        self.faces.append(Mesh(points, (50,100,0)))
        points = [Vector3(centre) + semiwidth*(i*x+j*y+z) for i in [-1,1] for j in [1,-1]]
        self.faces.append(Mesh(points, (100,50,0)))

    def Update(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        centre = self.centre
        semiwidth = self.semiwidth

        x = Vector3.SphericalConstructorDeg(1, alpha, beta)
        try:
            y = x.Cross(Vector3.X()).Normalized()
        except:
            y = Vector3.UP()
        z = Vector3.Cross(x, y)

        self.faces = []
        points = [(Vector3(centre) + semiwidth*(x+i*y+j*z)).asTuple() for i in [-1,1] for j in [1,-1]]
        self.faces.append(Mesh(points, (100,100,0)))
        points = [Vector3(centre) + semiwidth*(i*x+y+j*z) for i in [-1,1] for j in [1,-1]]
        self.faces.append(Mesh(points, (50,100,0)))
        points = [Vector3(centre) + semiwidth*(i*x+j*y+z) for i in [-1,1] for j in [1,-1]]
        self.faces.append(Mesh(points, (100,50,0)))


screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
box = Box(30, (400,300,100), 45, 45)
turnrate = 0.4
running=True
while running:
    screen.fill((255,255,255))

    mouse_pos = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN: 
            if e.key == pygame.K_ESCAPE:
                running = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        box.Update(box.alpha+turnrate, box.beta)
    if pressed[pygame.K_DOWN]:
        box.Update(box.alpha-turnrate, box.beta) 
    if pressed[pygame.K_RIGHT]:
        box.Update(box.alpha, box.beta+turnrate)
    if pressed[pygame.K_LEFT]:
        box.Update(box.alpha, box.beta-turnrate) 

    for mesh in box.faces:
        pygame.draw.polygon(screen, mesh.color, mesh.IsomtericProjection())    

    pygame.display.flip()
    clock.tick(60)



