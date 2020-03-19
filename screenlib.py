import pygame

class Screen(object):
    def __init__(self):

        self.width = 224
        self.height = 256
        self.scaling_width = 3
        self.scaling_height = 2
        self.video = [0] * (self.width * self.height)

        pygame.init()
        self.window = pygame.display.set_mode((self.width * self.scaling_width, self.height * self.scaling_height))
        self.screen = pygame.Surface((self.width, self.height))

        self.clock = pygame.time.Clock()


    def ScreenDraw(self, core):
        
        counter = 0
        for x in core.list_memory[0x2400:0x4000]:
            for y in range(0, 8):
                if(x & (1 << y)):
                    self.video[counter] = 1
                else:
                    self.video[counter] = 0

                counter = counter + 1

        counter = 0
        for i in range(self.width):
            for j in reversed(range(self.height)):
                if(self.video[counter]):
                    self.screen.set_at((i, j), (255, 255, 255))
                counter = counter + 1

        self.window.blit(pygame.transform.scale(self.screen, self.window.get_rect().size), (0, 0))
        pygame.display.update()
