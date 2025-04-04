import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont("Verdana", 20)

FPS = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_BONUS = (0, 204, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
bgx1 = 0
bgx2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "animated-goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)


player_size = (20, 20)
player = pygame.image.load("player.png").convert_alpha() #pygame.Surface(player_size)
# player.fill(COLOR_BLACK)
player_rect = pygame.Rect(0, 400, *player_size)
#player_rect = player.get_rect()
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]

def create_enemy():
    enemy_size = (10, 10)
    enemy = pygame.image.load("enemy.png").convert_alpha()#pygame.Surface(enemy_size)
    #enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(30, HEIGHT-30), *enemy_size)
    enemy_move = [random.randint(-8, -4),0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (40, 80)
    bonus = pygame.image.load("bonus.png").convert_alpha() #pygame.Surface(bonus_size)
    #bonus.fill(COLOR_BONUS)
    bonus_rect = pygame.Rect(random.randint(100, WIDTH-100), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 750)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 60)

enemies = []
bonuses = []
score = 0

image_index = 0

playing = True
while playing:
    FPS.tick(100)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append (create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index +=1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
        

    # main_display.fill(COLOR_BLACK)
    bgx1 -= bg_move
    bgx2 -= bg_move
    
    main_display.blit(bg, (bgx1, 0))
    main_display.blit(bg, (bgx2, 0))

    if bgx1 < -bg.get_width():
        bgx1 = bg.get_width()
    if bgx2 < -bg.get_width():
        bgx2 = bg.get_width()

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)


    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
