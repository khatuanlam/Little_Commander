import os

import pygame


class Step():
    def __init__(self, x, y):
        super().__init__()  # kế thừa từ pygame.sprite.Sprite
        self.x = x
        self.y = y
        self.width = 155.7
        self.height = 96.3
        self.vel = 3
        self.step = pygame.image.load(r'assets\Images\backgrounds\step.png')
        # self.step = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Img", "step.png"))
        self.step = pygame.transform.scale(
            self.step, (self.width, self.height))
        self.rect = self.step.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, moving_left, moving_right, moving_up, moving_down):
        # print("di duyen step")
        pass
