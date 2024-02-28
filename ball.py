import pygame as pg

class Ball:
    def __init__(self, screen, color, radius, weight, retention, x_cor, y_cor, x_speed, y_speed, friction, id):
        self.screen = screen
        self.color = color
        self.radius = radius
        self.weight = weight
        self.retention = retention
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.id = id
        self.ball = ""
        self.is_click = False
        self.times = False
        self.friction = friction
        self.can_go = False
        self.prev_x = 0
        self.prev_y = 0

    def show_ball(self):
        self.ball = pg.draw.circle(surface=self.screen, color=self.color, radius=self.radius, center=(self.x_cor, self.y_cor))



    def check_gravity(self, height, gravity, wall_thickness, bounce, y_push, x_push):
        if self.is_click:
            self.y_speed = y_push
            self.x_speed = x_push
        else:
            if self.y_cor < height - self.radius - wall_thickness/2:
                if self.y_cor <= 0 + self.radius + wall_thickness/2:
                    if not self.can_go:
                        self.y_speed *= -1 * self.retention
                        self.x_speed *= self.friction
                        self.can_go = True
                else:
                    self.y_speed += gravity
                    self.can_go = False
            else:
                if self.y_speed > bounce:
                    self.y_speed *= -1 * self.retention
                    self.x_speed *= self.friction

                else:
                    if abs(self.y_speed) <= bounce:
                        self.y_speed = 0
                        self.x_speed *= self.friction

        return self.y_speed



    def check_collision(self, width, thickness):
        if self.x_cor < width - (thickness / 2) - self.radius and self.x_cor > 0 + (thickness / 2) + self.radius:
            self.times = False
        else:
            if not self.times:
                self.x_speed *= -1 * self.friction
                self.times = True


    def update_cor(self, mouse, width, thickness, height):
        if not self.is_click:
            self.y_cor += self.y_speed
            self.x_cor += self.x_speed

        else:
            if mouse[0] < width - (thickness / 2) - self.radius:
                if mouse[0] > 0 + (thickness / 2) + self.radius:
                    if mouse[1] < height - (thickness / 2) - self.radius:
                        if mouse[1] > 0 + (thickness / 2) + self.radius:
                            self.y_cor = mouse[1]
                            self.x_cor = mouse[0]




    def check_click(self, pos):
        self.is_click = False
        if self.ball.collidepoint(pos):
            self.is_click = True
        return self.is_click
