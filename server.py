import pickle
import socket
import sys
import threading
from _thread import *

import pygame

from game import Game

width = 400
height = 300

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Server')
background = pygame.image.load(r'assets\Images\backgrounds\bg_server.png')
background = pygame.transform.scale(background, (width, height))


def drawWindow():
    win.blit(background, (0, 0))
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Server is running', 1, (255, 0, 0), True)
    win.blit(text, (width / 2 - text.get_width() /
             2, height / 2 - text.get_height() / 2))
    pygame.display.update()


server = 'localhost'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print('Waiting for a connection, Server Started')
drawWindow()

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    while True:
        # print('Da vao vong lap true cua thread_client')
        try:
            # print('Chuan bi thuc hien nhan du lieu tu client')
            data = conn.recv(4096).decode('UTF-8')
            # print('Da nhan du lieu xong tu client')
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data != 'get':
                        if data == 'shoot':
                            game.createBullet(p)
                        elif data == 'boom':
                            # game.createBoom(p)
                            print(data)
                        # Kiểm tra trạng thái của 2 người chơi
                        elif data == 'on_step':
                            game.players[p].on_step = True
                        elif data == 'not_on_step':
                            if p == 0:
                                game.players[0].on_step = False
                                game.players[0].fallDone = False
                            if p == 1:
                                game.players[1].on_step = False
                                game.players[1].fallDone = False
                        elif data == 'attach':
                            print(data)
                        elif data.startswith('get_shot'):
                            id_dan = int(data.replace('get_shot', ''))
                            current_player = game.players[p]
                            for player in game.players:
                                for bullet in player.bullets:
                                    if bullet.id == id_dan:
                                        player.bullets.remove(bullet)
                                        break
                            current_player.hp -= 20
                            current_player.hurting = True
                        elif data == 'reset':
                            game.reset()
                        else:
                            # Cập nhật di chuyển của người chơi
                            game.move(p, data)
                    game.update()
                    game.capNhatDan()
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except socket.error as e:
            print(e)
            break
    print('Lost connection')
    try:
        del games[gameId]
        print('Closing Game', gameId)
    except:
        pass
    idCount -= 1
    conn.close()


is_running = True
is_shutdown = threading.Event()


def accept_connections(is_shutdown):
    global idCount
    s.settimeout(0.5)
    while True:
        # print('IS_SHUTDOWN SET: ', is_shutdown.is_set())
        if is_shutdown.is_set():
            break
        try:
            conn, addr = s.accept()
            print('Connected to:', addr)

            idCount += 1
            p = 0
            gameId = (idCount - 1) // 2
            if idCount % 2 == 1:
                games[gameId] = Game(gameId)
                print('Creating a new game with id... ' + str(gameId))
            else:
                games[gameId].ready = True
                p = 1
            start_new_thread(threaded_client, (conn, p, gameId))
        except:
            pass


accept_thread = threading.Thread(
    target=accept_connections, args=(is_shutdown,))
accept_thread.start()

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            is_shutdown.set()

print('Ready to join')
accept_thread.join()
pygame.quit()
s.close()
sys.exit()
