import os
import time
import pygame

from states.title import Title

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pykemon")
        self.GAME_W = 640
        self.GAME_H = 576
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 640, 576
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.actions = {
            'left': False,
            'right': False,
            'up': False,
            'down': False,
            'select': False,
            'back': False
        }
        self.BLACK = (0, 0, 0)
        self.RED = (248, 0, 0)
        self.GREEN = (0, 184, 0)
        self.BLUE = (32, 136, 248)
        self.YELLOW = (248, 168, 0)

        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.load_assets()
        self.load_states()
        self.SCALE = 4

    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_UP:
                    self.actions['up'] = True
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = True
                if event.key == pygame.K_LEFT:
                    self.actions['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.actions['right'] = True
                if event.key == pygame.K_RETURN:
                    self.actions['select'] = True
                if event.key == pygame.K_BACKSPACE:
                    self.actions['back'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.actions['up'] = False
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = False
                if event.key == pygame.K_LEFT:
                    self.actions['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.actions['right'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['select'] = False
                if event.key == pygame.K_BACKSPACE:
                    self.actions['back'] = False

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, colour, x, y):
        text_surface = self.font.render(text, False, colour)
        text_rect = text_surface.get_rect()
        text_rect = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.images_dir = os.path.join(self.assets_dir, "images")
        self.font_dir = os.path.join(self.assets_dir, "font")
        self.font = pygame.font.Font(os.path.join(self.font_dir, "pokemon_generation_1.ttf"), 32)

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()