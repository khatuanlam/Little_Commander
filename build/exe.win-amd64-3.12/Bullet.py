import os

import pygame


class Bullet:
    pygame.init()

    def __init__(self, x, y, left, id):
        super().__init__()
        self.id = id
        self.x = x
        self.y = y
        self.left = left
        self.width = 21.05
        self.height = 11.2
        self.vel = 8
        self.img = r'assets\Images\backgrounds\bullet.png'
        # self.img = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Img", "bullet.png")

    @staticmethod
    def getImg():
        return r'assets\Images\backgrounds\bullet.png'

    def update(self):
        if not self.left:
            self.x += self.vel
        else:
            self.x -= self.vel
