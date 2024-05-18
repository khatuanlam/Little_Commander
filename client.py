import pygame

import Bullet
from network import Network
from Step import Step

pygame.mixer.init()
pygame.font.init()

width = 1000
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')


# Background Image
background = pygame.image.load(r'assets\Images\backgrounds\background.png')
background = pygame.transform.scale(background, (width, height))


# Sound
shoot_sound = pygame.mixer.Sound(r'assets\Sound\Shoot.mp3')
hit_sound = pygame.mixer.Sound(r'assets\Sound\Hit.mp3')
jump_sound = pygame.mixer.Sound(r'assets\Sound\Jump.mp3')
reload_amor = pygame.mixer.Sound(r'assets\Sound\Reload.mp3')
bg_sound = pygame.mixer.Sound(r'assets\Sound\bg_music.mp3')
count_sound = pygame.mixer.Sound(r'assets\Sound\countdown.mp3')
explo_sound = pygame.mixer.Sound(r'assets\Sound\explosion.mp3')

bg_sound.set_volume(0.5)
bg_sound.play(-1, 0, 5000)

count_sound.set_volume(0.2)

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

FPS = 60
# 2 bậc thềm
step1 = Step(150, 400)
step2 = Step(600, 400)
# Draw fighter health


def draw_health(health, x, y):
    # Health Percent
    ratio = health/100
    pygame.draw.rect(win, BLACK, (x - 2, y - 2, 402, 32))
    pygame.draw.rect(win, RED, (x, y, 400, 30))
    pygame.draw.rect(win, GREEN, (x, y, 400 * ratio, 30))


def redrawWindow(win, game, p, n):
    win.fill((128, 128, 128))
    if not (game.connected()):
        font = pygame.font.SysFont('comicsans', 80)
        text = font.render('Waiting for Player...', 1, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() /
                 2, height / 2 - text.get_height() / 2))

    else:
        win.blit(background, (0, 0))
        win.blit(step1.step, (step1.x, step1.y))
        win.blit(step2.step, (step2.x, step2.y))

        # Mảng chứa hình ảnh nhân vâtj
        players_surface = []
        # Tọa độ của nhân vật
        players_rect = []

        for i, player in enumerate(game.players):
            if player.jumping:
                surface = pygame.image.load(str(player.jump_img))
            elif player.gunning:
                surface = pygame.image.load(
                    str(player.gun_img[player.index_gun_img]))
            elif player.hurting:
                surface = pygame.image.load(
                    str(player.hurt_img[player.index_hurt_img]))
            else:
                # Vẽ nhân vật ở trạng thái Idle
                surface = pygame.image.load(
                    str(player.img[player.index_img]))

            players_surface.append(surface)

            players_surface[i] = pygame.transform.scale(
                players_surface[i], (player.width, player.height))

            if player.left:
                players_surface[i] = pygame.transform.flip(
                    players_surface[i], True, False)

            # Lấy vị trí của nhân vật để đặt cho hình vẽ
            rect = players_surface[i].get_rect()
            players_rect.append(rect)
            players_rect[i].x = player.x
            players_rect[i].y = player.y
            win.blit(players_surface[i],
                     (player.x, player.y))

         # Nhảy lên bậc

        if not game.players[p].on_step:
            if (players_rect[p].x + 60.5 >= step1.x and players_rect[p].x + 60.5 < 276.3) or (players_rect[p].x + 60.5 >= step2.x and players_rect[p].x + 60.5 < 726.3):
                if players_rect[p].y < 304:
                    n.send('on_step')
        else:
            if players_rect[p].x + 60.5 < step1.x or (players_rect[p].x >= 276.3 and players_rect[p].x + 60.5 < step2.x) or players_rect[p].x >= 726.3:
                n.send('not_on_step')

        draw_health(game.players[p].hp, 20, 20)
        draw_health(game.players[1 if p == 0 else 0].hp,
                    width - 400 - 20, 20)

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
                        n.send('get_shot' + str(bullet.id))
                        hit_sound.play()
                # 2 nhân vật va chạm
                if players_rect[0].colliderect(players_rect[1]):
                    n.send('attach')


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()

    player = int(n.getPost())
    print('You are player', player)

    while run:
        clock.tick(FPS)
        try:
            game = n.send('get')
        except:
            print("Couldn't get game")
            break

        action = ''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            action = 'left'
        elif keys[pygame.K_RIGHT]:
            action = 'right'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    action = 'un_left'
                elif event.key == pygame.K_RIGHT:
                    action = 'un_right'
                elif event.key == pygame.K_UP:
                    action = 'un_jump'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if keys[pygame.K_LEFT]:
                        action = 'left_jump'
                        jump_sound.play()

                    elif keys[pygame.K_RIGHT]:
                        action = 'right_jump'
                        jump_sound.play()
                    else:
                        action = 'jump'
                        jump_sound.play()
                if event.key == pygame.K_s:
                    action = 'shoot'
                    current_player = game.players[player]
                    if len(current_player.bullets) < 2:
                        shoot_sound.play()
                    else:
                        reload_amor.play()
                if event.key == pygame.K_b:
                    action = 'boom'
                    # count_sound.play(0, 2, 1000)

        if action != '' and game.connected():
            n.send(action)
        redrawWindow(win, game, player, n)

        if game.winner() != -1:
            font = pygame.font.SysFont('comicsans', 60)
            win_text = font.render('You Win', 1, BLACK)
            lose_text = font.render('You Lose', 1, BLACK)
            if game.winner() == player:
                win.blit(win_text, (width / 2 - win_text.get_width() /
                                    2, height / 2 - win_text.get_height() / 2))
            else:
                win.blit(lose_text, (width / 2 - lose_text.get_width() /
                                     2, height / 2 - lose_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            return


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        # Vẽ background
        win.blit(background, (0, 0))

        font = pygame.font.SysFont('comicsans', 60)
        text = font.render('Click to Play!', 1, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() /
                 2, height / 2 - text.get_height() / 2))
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
