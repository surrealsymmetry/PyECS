import pygame

class Game:     # a singleton! this instance of pygame
    __instance = None

    def __init__(self, r):
        game_entity = r.e()
        pygame.init()
        self.view = pygame.display.set_mode((640, 480))

        bg = pygame.Surface(self.view.get_size())
        bg.fill((85, 82, 87))
        self.bg = bg.convert()
        e_bg = r.e()
        e_bg.grant(r.c("graphic", sprite=bg, bounds=bg.get_rect(), layer=-1))

        self.mainloop = True
        self.clock = pygame.time.Clock()
        self.c_timer = game_entity.grant(r.c("timer"))

    def run(self):
        while self.mainloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.mainloop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.mainloop = False
            self.view.blit(self.bg, (0,0))
            self.r.update()
            text = ":FPS: {0:.2f} Playtime: {1:.2f}".format(self.clock.get_fps(), self.c_timer.total)
            pygame.display.set_caption(text)
            pygame.display.flip()
        pygame.quit()
        print("Game played for {0:.2f} seconds".format(self.c_timer.total))