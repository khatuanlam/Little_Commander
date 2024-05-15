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

    def capNhat(self):
        if self.player0.left_jumping:
            self.player0.left_jump()
        elif self.player0.right_jumping:
            self.player0.right_jump()
        elif self.player0.jumping:
            self.player0.jump()

        if self.player1.left_jumping:
            self.player1.left_jump()
        elif self.player1.right_jumping:
            self.player1.right_jump()
        elif self.player1.jumping:
            self.player1.jump()

        # Nếu nằm trên step thì cập nhật vị trí cho nhân vật
        if self.player0.va_cham_da:
            self.player0.y = 322
        if self.player1.va_cham_da:
            self.player1.y = 322

        if not self.player0.fallDone:
            self.player0.fall()
        if not self.player1.fallDone:
            self.player1.fall()

        if self.player0.gunning:
            self.player0.gunning_image()
        if self.player1.gunning:
            self.player1.gunning_image()

        if self.player0.hurting:
            self.player0.hurting_image()
        if self.player1.hurting:
            self.player1.hurting_image()

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
            print("Da gan gunning la True")
        elif player == 1:
            current_player = self.player1
            current_player.gunning = True
            print("Da gan gunning la True")
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
        print("Id dan vua tao la: ", new_bullet.id)
        print("Toa do dan vua tao la: ", new_bullet.x, new_bullet.y)
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
        self.player0.x, self.player0.y = 0, 460
        self.player1.x, self.player1.y = 886.5, 460
        self.ready = False
        self.moving_left = False
        self.moving_right = False
        self.moving_jump = False
        self.players = list()
        self.players.append(self.player0)
        self.players.append(self.player1)
        self.playerWin = -1
        idBullet = 0
