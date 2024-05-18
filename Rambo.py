import os

import pygame

width = 1000
height = 700

pygame.init()


class Rambo:
    def __init__(self, x, y):
        super().__init__()
        self.img = self.get_img('Run')
        self.gun_img = self.get_img('Shot')
        self.hurt_img = self.get_img('Hurt')
        self.jump_img = r'assets\Images\character\Jump\jump.png'
        self.index_gun_img = 0
        self.index_img = 0
        self.index_hurt_img = 0
        self.left = False
        self.jumpCount = 10
        self.jump_vel = 3
        self.jumping = False
        self.left_jumping = False
        self.right_jumping = False
        self.x = x
        self.y = y
        self.width = 113.5
        self.height = 98
        self.vel = 5
        self.moving_left = False
        self.moving_right = False
        self.moving_jump = False
        self.bullets = []
        self.hp = 100
        self.on_step = False
        self.fallCount = 0
        self.fallDone = True
        self.gunning = False
        self.hurting = False

    def get_img(self, action):
        return {i: fr'assets\Images\character\{action}\{i}.png' for i in range(10)}

    def update(self, moving_left, moving_right, moving_jump):
        if moving_left and moving_jump:
            self.left_jumping = True
        elif moving_right and moving_jump:
            self.right_jumping = True
        elif moving_left:
            self.left = True
            self.x -= self.vel
            self.index_img -= 1
        elif moving_right:
            self.left = False
            self.x += self.vel
            self.index_img += 1
        elif moving_jump:
            self.jumping = True

        # Đổi index ảnh khi di chuyển để k bị hết ảnh
        if self.index_img < 0:
            self.index_img = 9
        if self.index_img > 9:
            self.index_img = 0

        # Giới hạn màn hình
        self.x = max(0, min(self.x, width - self.width))
        self.y = max(0, min(self.y, height - self.width - 125))

    def jump(self):
        if self.jumpCount >= -10:
            self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.25
            self.jumpCount -= 0.5
        else:
            self.jumping = False
            self.jumpCount = 10

    def fall(self):
        if self.fallCount >= -10:
            self.y -= (self.fallCount * abs(self.fallCount)) * 0.25
            self.fallCount -= 0.5
        else:
            self.fallDone = True
            self.fallCount = 0
        if self.y > height - self.width - 125:
            self.y = height - self.width - 125

    def left_jump(self):
        if self.jumpCount >= -10:
            if self.on_step and self.jumpCount <= 2:
                self.x -= 0
            else:
                self.x -= 3
            self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.25
            self.jumpCount -= 0.5
        else:
            self.left_jumping = False
            self.jumpCount = 10

    def right_jump(self):
        if self.jumpCount >= -10:
            if self.on_step and self.jumpCount <= 2:
                self.x += 0
            else:
                self.x += 3
            self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.25
            self.jumpCount -= 0.5
        else:
            self.right_jumping = False
            self.jumpCount = 10

    def gunning_image(self):
        self.index_gun_img += 1
        if self.index_gun_img > 9:
            self.index_gun_img = 0
            self.gunning = False

    def hurting_image(self):
        self.index_hurt_img += 1
        if self.index_hurt_img > 9:
            self.index_hurt_img = 0
            self.hurting = False

    def reset(self):
        self.index_img = 0
        self.left = False
        self.jumpCount = 10
        self.jump_vel = 3
        self.jumping = False
        self.left_jumping = False
        self.right_jumping = False
        self.width = 113.5
        self.height = 98
        self.vel = 5
        self.moving_left = False
        self.moving_right = False
        self.moving_jump = False
        self.bullets.clear()
        self.hp = 100
