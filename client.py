import pygame

import Bullet
from network import Network
from Step import Step

pygame.mixer.init()
pygame.font.init()

width = 1000
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


# Background Image
background = pygame.image.load(r'assets\Images\backgrounds\background.png')
background = pygame.transform.scale(background, (width, height))

step1 = Step(150, 400)
step2 = Step(600, 400)
# Sound
shoot_sound = pygame.mixer.Sound(r'assets\Sound\Shoot.mp3')
hit_sound = pygame.mixer.Sound(r'assets\Sound\Hit.mp3')
jump_sound = pygame.mixer.Sound(r'assets\Sound\Jump.mp3')
reload_amor = pygame.mixer.Sound(r'assets\Sound\Reload.mp3')

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

FPS = 60

# Draw fighter health


def draw_health(health, x, y):
    # Health Percent
    ratio = health/100
    pygame.draw.rect(win, WHITE, (x - 2, y - 2, 402, 32))
    pygame.draw.rect(win, RED, (x, y, 400, 30))
    pygame.draw.rect(win, GREEN, (x, y, 400 * ratio, 30))


def redrawWindow(win, game, p, n):
    win.fill((128, 128, 128))
    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() /
                 2, height / 2 - text.get_height() / 2))

    else:
        win.blit(background, (0, 0))
        win.blit(step1.step, (step1.x, step1.y))
        win.blit(step2.step, (step2.x, step2.y))

        draw_health(game.players[p].hp, 20, 20)
        draw_health(game.players[1 if p == 0 else 0].hp,
                    width - 400 - 20, 20)
        # Trạng thái hiện thị
        players_surface = []
        # Tọa độ của nhân vật
        players_rect = []

        for i, player in enumerate(game.players):
            if player.jumping:
                surface = pygame.image.load(str(player.img['jump']))
            elif player.gunning:
                surface = pygame.image.load(
                    str(player.gun_img[player.index_gun_img]))
            elif player.hurting:
                surface = pygame.image.load(
                    str(player.hurt_img[player.index_hurt_img]))
            else:
                surface = pygame.image.load(
                    str(player.img[player.index_img]))

            players_surface.append(surface)

            players_surface[i] = pygame.transform.scale(
                players_surface[i], (player.width, player.height))

            if player.left:
                players_surface[i] = pygame.transform.flip(
                    players_surface[i], True, False)
            # Lấy vị trí của nhân vật
            rect = players_surface[i].get_rect()
            players_rect.append(rect)
            players_rect[i].x = player.x
            players_rect[i].y = player.y
            win.blit(players_surface[i],
                     (player.x, player.y))
        if p == 0:
            if not game.players[p].va_cham_da and players_rect[p].x + 60.5 >= 150 and players_rect[p].x < 276.3 and players_rect[p].y < 304:
                print("va cham da")
                n.send("va_cham_da")
            elif game.players[p].va_cham_da and (players_rect[p].x + 60.5 < 150 or players_rect[p].x >= 276.3):
                print("het va cham da")
                n.send("het_va_cham_da")
        else:
            if not game.players[1].va_cham_da and players_rect[1].x + 60.5 >= 600 and players_rect[1].x < 726.3 and players_rect[1].y < 304:
                print("va cham da")
                n.send("va_cham_da")
            elif game.players[1].va_cham_da and (players_rect[1].x + 60.5 < 600 or players_rect[1].x >= 726.3):
                print("het va cham da")
                n.send("het_va_cham_da")

        drawBullet(game.players, players_rect, p, n)

    pygame.display.update()


def drawBullet(players, players_rect, p, n):
    for player in players:
        index_player = players.index(player)
        for bullet in player.bullets:
            bullet_surface = pygame.image.load(Bullet.Bullet.getImg())
            bullet_surface = pygame.transform.scale(
                bullet_surface, (bullet.width, bullet.height))
            if bullet.left:
                bullet_surface = pygame.transform.flip(
                    bullet_surface, True, False)
            bullet_rect = bullet_surface.get_rect()
            bullet_rect.x, bullet_rect.y = bullet.x, bullet.y
            win.blit(bullet_surface, (bullet.x, bullet.y))
            for player_rect in players_rect:
                if bullet_rect.colliderect(player_rect):
                    index_rect = players_rect.index(player_rect)
                    if index_rect != index_player and p == index_rect:
                        n.send("bi_ban_boi_dan_" + str(bullet.id))
                        hit_sound.play()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()

    player = int(n.getPost())
    print("You are player", player)

    while run:
        clock.tick(FPS)
        try:
            # print("Chuan bi game = n.send('get')")
            game = n.send("get")
            # print("Da game = n.send('get') xong")
        except:
            print("Couldn't get game")
            break
        if game.playerWin != -1:
            font = pygame.font.SysFont("comicsans", 60)
            win_text = font.render("You Win", 1, WHITE)
            lose_text = font.render("You Lose", 1, WHITE)
            if game.playerWin == player:
                win.blit(win_text, (100, 350))
            else:
                win.blit(lose_text, (100, 350))
            pygame.display.update()
            pygame.time.delay(4000)
            return

        action = ''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            action = "left"
        elif keys[pygame.K_RIGHT]:
            action = "right"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    action = "un_left"
                elif event.key == pygame.K_RIGHT:
                    action = "un_right"
                elif event.key == pygame.K_UP:
                    action = "un_jump"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if keys[pygame.K_LEFT]:
                        action = "left_jump"
                        jump_sound.play()
                        print("nhay sang trai")

                    elif keys[pygame.K_RIGHT]:
                        action = "right_jump"
                        jump_sound.play()
                        print("nhay sang phai")
                    else:
                        action = "jump"
                        jump_sound.play()
                if event.key == pygame.K_s:
                    action = "shoot"
                    current_player = game.players[player]
                    if len(current_player.bullets) < 2:
                        shoot_sound.play()
                    else:
                        reload_amor.play()
        if action != "" and game.connected():
            n.send(action)
        redrawWindow(win, game, player, n)


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        # Vẽ background
        win.blit(background, (0, 0))

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
