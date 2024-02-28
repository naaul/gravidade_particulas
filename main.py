import pygame as pg
from pygame import time
import math
import numpy as np
from ball import Ball

pg.init()

width = 500
height = 500
screen = pg.display.set_mode([width, height])

mouse_trajectory = []


timer = time.Clock()
fps = 60

wall_thickness = 20
wall_color = "white"

background_color = "black"

balls = []
balls_queue = [Ball(screen, "red", 40, 50, 0.8, 200, 100, 0, 0, .9, 0),
               Ball(screen, "blue", 20, 50, 0.8, 450, 200, 0, 0, .9, 1),
               Ball(screen, "green", 30, 60, 0.8, 400, 250, 0, 0, .9, 2),
               ]


def draw_wall(color, width, height, wall_thickness):
    left = pg.draw.line(surface=screen, color=color, start_pos=(0, height), end_pos=(0, 0), width=wall_thickness)
    right = pg.draw.line(surface=screen, color=color, start_pos=(width, height), end_pos=(width, 0), width=wall_thickness)
    bottom = pg.draw.line(surface=screen, color=color, start_pos=(width, height), end_pos=(0, height), width=wall_thickness)
    top = pg.draw.line(surface=screen, color=color, start_pos=(0, 0), end_pos=(width, 0), width=wall_thickness)

    return left, right, bottom, top


id = len(balls_queue)


def create(color, radius, weight, retention, x_cor, y_cor, friction):
    global id
    new_ball = Ball(screen, color, radius, weight, retention, x_cor, y_cor, 2, 0, friction, id)
    balls_queue.append(new_ball)
    id += 1


count = 0


def menu():
    global gravity, wall_thickness, wall_color, height, width, background_color, count
    inp = int(input("1- Create ball\n2- List of balls\n3- Deploy balls\n4- Options\n5- Reset balls\n6- Exit\n"))
    if inp == 1:
        color = input("Type color: ")
        radius = int(input("Type radius: "))
        weight = int(input("Type weight: "))
        retention = float(input("Type retention%: "))
        friction = float(input("Type friction%: "))
        x_cor = int(input("Type x coordinates: "))
        y_cor = int(input("Type y coordinates: "))
        create(color, radius, weight, retention, x_cor, y_cor, friction)
        menu()
    elif inp == 2:
        for ball in balls_queue:
            print(f"Ball id: {ball.id}, color: {ball.color}, radius: {ball.radius}, weight: {ball.weight}, retention: {ball.retention}")
        menu()
    elif inp == 3:
        if len(balls_queue) == 0:
            menu()
        else:
            for ball in balls_queue:
                if ball not in balls:
                    balls.append(ball)
    elif inp == 4:
        opt = int(input(f"What do you want to change:\n"
                        f"1- Gravity({gravity})\n"
                        f"2- Wall thickness({wall_thickness})\n"
                        f"3- Wall color({wall_color})\n"
                        f"4- Height size({height})\n"
                        f"5- Width size({width})\n"
                        f"6- Background color({background_color})\n"
                        f"7- Exit\n"))
        if opt != 7:
            value = input("Type the value: ")
            if opt == 1:
                gravity = float(value)
            elif opt == 2:
                wall_thickness = int(value)
            elif opt == 3:
                wall_color = str(value)
            elif opt == 4:
                height = int(value)
            elif opt == 5:
                width = int(value)
            elif opt == 6:
                background_color = str(value)

        else:
            menu()
    elif inp == 5:
        balls.clear()
        balls_queue.clear()
        menu()
    elif inp == 6:
        pass

def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 5:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)

    return x_speed, y_speed


def calc_distance(x1, y1, x2, y2):
    b = int(abs(x1 - x2))
    c = int(abs(y1 - y2))
    a = math.sqrt(((b * b) + (c * c)))
    return a


def calc_elastic_vector(p1, p2, v1, v2, m1, m2):
    r12 = p1 - p2

    v_rel = v1 - v2

    p_total = m1 * v1 + m2 * v2

    j = 2 * (m1 * m2) / (m1 + m2) * np.dot(v_rel, r12) / np.linalg.norm(r12) ** 2

    v1_novo = v1 - j * m2 / (m1 + m2) * r12 / np.linalg.norm(r12)
    v2_novo = v2 + j * m1 / (m1 + m2) * r12 / np.linalg.norm(r12)

    return v1_novo, v2_novo




def deployBalls():
    global count
    if len(balls) > 0:
        for ball in balls:
            ball.show_ball()
            ball.y_speed = ball.check_gravity(height, gravity, wall_thickness, bounce, y_push, x_push)
            ball.check_collision(width, wall_thickness)
            ball.update_cor(mouse, width, wall_thickness, height)
    else:
        pass




gravity = 0.5
bounce = 0.6

print("Type ESC to open menu")

run = True
while run:

    timer.tick(fps)
    screen.fill(background_color)

    walls = draw_wall(color=wall_color, height=height, width=width, wall_thickness=wall_thickness)
    mouse = pg.mouse.get_pos()
    mouse_trajectory.append(mouse)
    if len(mouse_trajectory) > 10:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()

    deployBalls()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                menu()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for ball in balls:
                    if ball.check_click(event.pos):
                        active_selective = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                active_selective = False
                for i in range(len(balls)):
                    balls[i].check_click((1000, -1000))

    pg.display.flip()

    if count == 0:
        count += 1
        menu()

pg.quit()
