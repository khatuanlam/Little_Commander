import public as public

from Bullet import Bullet
from Rambo import Rambo

width = 1000
height = 700
idBullet = 0


class Game:

    def __init__(self, id):
        self.player0 = Rambo(0, 460)
        self.player1 = Rambo(886.5, 460)
        self.ready = False
        self.id = id
        self.moving_left = False
        self.moving_right = False
        self.moving_jump = False
        self.playerWin = -1
        self.players = [self.player0, self.player1]

    def update(self):
        for player in self.players:
            if player.left_jumping:
                player.left_jump()
            elif player.right_jumping:
                player.right_jump()
            elif player.jumping:
                player.jump()
            # Cập nhật độ cao khi đứng trên đá
            if player.on_step:
                player.y = 322
            # Cập nhật vị trí khi nhân vật rơi xuống đất
            if not player.fallDone:
                player.fall()

            if player.gunning:
                player.gunning_image()

            if player.hurting:
                player.hurting_image()

    def play(self, player, move):
        if move == "left_jump":
            self.moving_left = True
            self.moving_jump = True
        elif move == "right_jump":
            self.moving_right = True
            self.moving_jump = True
        elif move == "left":
            self.moving_left = True
        elif move == "right":
            self.moving_right = True
        elif move == "jump":
            self.moving_jump = True
        elif move == "un_left":
            self.moving_left = False
        elif move == "un_right":
            self.moving_right = False
        else:
            pass
        # Cập nhật hành động cho nhân vật của người chơi
        for i in range(0, len(self.players)):
            if player == i:
                self.players[i].update(
                    self.moving_left, self.moving_right, self.moving_jump)

        # Ok ghi nhận là nhảy rồi, sẽ xử lý ở player
        self.moving_jump = False
        if move == "left_jump":
            self.moving_left = False
        if move == "right_jump":
            self.moving_right = False

    def connected(self):
        return self.ready

    def createBullet(self, player):
        global idBullet
        if player == 0:
            current_player = self.player0
            current_player.gunning = True
        elif player == 1:
            current_player = self.player1
            current_player.gunning = True
        else:
            raise ValueError("Invalid player ID")

        if len(current_player.bullets) >= 2:
            return
        if current_player.left:
            toado_x = current_player.x
        else:
            toado_x = current_player.x + 114

        new_id = idBullet
        idBullet += 1
        new_bullet = Bullet(toado_x, current_player.y + 66,
                            current_player.left, new_id)
        current_player.bullets.append(new_bullet)
        print("Tong so dan cua player", player,
              "la", len(current_player.bullets))

    def capNhatDan(self):
        if len(self.player0.bullets) <= 0 and len(self.player1.bullets) <= 0:
            return
        for player in self.players:
            for bullet in player.bullets:
                bullet.update()
                if bullet.x > width - bullet.vel:
                    player.bullets.remove(bullet)
                if bullet.x < bullet.vel:
                    player.bullets.remove(bullet)

    def reset(self):
        global idBullet
        self.player0.reset()
        self.player1.reset()
        self.player0.x, self.player0.y = (0, 460)
        self.player1.x, self.player1.y = (886.5, 460)
        self.ready = False
        self.moving_left = False
        self.moving_right = False
        self.moving_jump = False
        self.players = [self.player0, self.player1]
        self.playerWin = -1
        idBullet = 0
