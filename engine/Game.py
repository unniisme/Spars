import pygame

class PyGameInstance:
    
    def __init__(self, breadth, height):
        """Initiate a pygame instance with an associated screen of given hight and breadth"""
        pygame.init()
        
        self.height = height
        self.breadth = breadth
        self.playing = False

        self.screen = pygame.display.set_mode([breadth, height])
        self.clock = pygame.time.Clock()

    def Start(self):
        """Set instance to running"""
        self.playing = True

    def Pause(self):
        self.playing = False

    def Stop(self):
        self.playing = False
        pygame.quit()

    def isPlaying(self) -> bool:
        """Check is instance is running"""
        return self.playing

    def initFrame(self):
        """Initialize a frame"""
        if not self.isPlaying():
            pygame.quit()
            raise RuntimeError("Illegal frame initialization")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.fill((255,255,255))
            
    def endFrame(self):
        """End a frame"""
        pygame.display.flip()
        self.clock.tick(60)

