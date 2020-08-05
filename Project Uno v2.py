import pygame
import random
import sys
import math
from pygame import mixer

mixer.init()
pygame.init()

icon = pygame.image.load("C:\\Users\\richa\\Desktop\\Projects\\download.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Brave the Storm")

mixer.music.load("C:\\Users\\richa\\Desktop\\Projects\\a.mp3")
mixer.music.play(-1)

length = 800
width = 600

green = (0,255,0)
cyan = (0,255,255)
player_rad = 15
player_pos = [400,575]
background_colour = (0,0,0)
pygame.key.set_repeat(10,10)

num_enemies = 10
enemy_color = [random.randint(1,255),random.randint(1,255),random.randint(1,255)]
enemy_rad = 50
enemy_pos = [random.randint(0,length), 0]
enemy_list = [enemy_pos]
speed = 10
screen = pygame.display.set_mode((length,width))
collision_rad = player_rad + enemy_rad

game_over = False
score = 0
level = 1

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace",35)

def number_enemies(level,num_enemies):
    if level == 1:
        num_enemies = 10
    elif level == 2:
        num_enemies = 12
    elif level == 3:
        num_enemies = 14
    elif level == 4:
        num_enemies = 16
    else:
        num_enemies = 18

    return num_enemies

def display_level(score, level):
    if score < 50:
        level = 1
    elif score < 150:
        level = 2
    elif score < 300:
        level = 3
    elif score < 500:
        level = 4
    else:
        level = 5
    return level

def set_level(score, speed):

    speed = score/5 + 5

    return speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < num_enemies and delay < 0.075:
        x_pos = random.randint(0,length-enemy_rad)
        y_pos = 0
        enemy_list.append([x_pos,y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.circle(screen, enemy_color, enemy_pos, enemy_rad)

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and (enemy_pos[1]+enemy_rad) < length:
            enemy_pos[1] += int(speed/2)
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detectCollision(player_pos, enemy_pos):
            return True
    return False

def detectCollision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (math.sqrt((e_x-p_x)**2+(e_y-p_y)**2) <=collision_rad):
        return True
    return False

while not game_over:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_UP:
                if player_pos[1] > (player_rad):
                    y -= int(player_rad/2)
            elif event.key == pygame.K_DOWN:
                if player_pos[1] < (width-player_rad):
                    y += int(player_rad/2)
            elif event.key == pygame.K_RIGHT:
                if player_pos[0] < (length-player_rad):
                    x += int(player_rad/2)
            elif event.key == pygame.K_LEFT:
                if player_pos[0] > (player_rad):
                    x -= int(player_rad/2)

            player_pos = [x,y]



    screen.fill(background_colour)

    if detectCollision(player_pos,enemy_pos):
        game_over = True


    clock.tick(30)
    num_enemies = number_enemies(level,num_enemies)
    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    speed = set_level(score, speed)
    level = display_level(score, level)
    text_level = "Level: " + str(level)
    text = "Score: " + str(score)
    label = myFont.render(text, 1, green)
    label_level = myFont.render(text_level, 1, green)
    screen.blit(label, (length-250,width-35))
    screen.blit(label_level, (length-250,(width - 70)))
    if collision_check(enemy_list, player_pos):
        game_over = True
    draw_enemies(enemy_list)
    player = pygame.draw.circle(screen, cyan , (player_pos[0],player_pos[1]) , player_rad)
    pygame.display.update()
