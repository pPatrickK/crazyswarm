#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import pygame
import sys
import math
import time

class CrazyflieWrapper(object):
    def __init__(self, start_time, land_time, movement_time, movement_amount, height):
        self.swarm = Crazyswarm()
        self.allcfs = self.swarm.allcfs
        self.start_time = start_time
        self.land_time = land_time
        self.movement_time = movement_time
        self.movement_amount = movement_amount
        self.height = height
        self.time_for_next_command = time.time()
        self.relative_position = Vector2D()

    def check_and_set_time_for_command(self, commands_seconds):
        if self.time_for_next_command <= time.time():
            self.time_for_next_command = time.time() + commands_seconds
            return True
        return False

    def print_debug(self):
        print("time for starting:", self.start_time)
        print("time for landing:", self.land_time)
        print("time for moving:", self.movement_time)
        print("amount of moving:", self.movement_amount)
        print("height:", self.height)

    def move(self, vector):
        if self.check_and_set_time_for_command(self.movement_time):
            vector.scale(self.movement_amount)
            self.relative_position.addX(vector.getX())
            self.relative_position.addY(vector.getY())
            print(vector.getX(), vector.getY())
            for cf in self.allcfs.crazyflies:
                pos = np.array(cf.initialPosition) + np.array([self.relative_position.getX(), self.relative_position.getY(), self.height])
                cf.goTo(pos, 0, self.movement_time)

    def start(self):
        if self.check_and_set_time_for_command(self.start_time):
            self.allcfs.takeoff(targetHeight=self.height, duration=self.start_time)
            print("start")

    def land(self):
        if self.check_and_set_time_for_command(self.land_time):
            self.allcfs.land(targetHeight=0.02, duration=self.land_time)
            print("land")

    def change_movement_time(self, amount):
        self.movement_time += amount

    def change_move_amount(self, amount):
        self.movement_amount += amount

    def change_height(self, amount):
        self.height += amount

class Vector2D(object):
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def sefX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def addX(self, amount):
        self.x += amount
    def addY(self, amount):
        self.y += amount
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    def scale(self, amount):
        own_length = self.length()
        self.x = amount * self.x / own_length
        self.y = amount * self.y / own_length

def format_decimal(number):
    return '{0:.2f}'.format(number)

def main():
    start_time = 1.0
    land_time = 1.0
    movement_time = 1.0
    movement_amount = 0.5
    height = 0.3
    cfs = CrazyflieWrapper(start_time, land_time, movement_time, movement_amount, height)
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("ubuntumono", 30)
    window_size = 800, 600
    screen = pygame.display.set_mode(window_size)
    fill_color = 0, 0, 0
    running = True
    while running:
        current_direction = Vector2D()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    continue
                elif event.key == pygame.K_DOWN:
                    current_direction.addY(-1.0)
                elif event.key == pygame.K_UP:
                    current_direction.addY(1.0)
                elif event.key == pygame.K_RIGHT:
                    current_direction.addX(1.0)
                elif event.key == pygame.K_LEFT:
                    current_direction.addX(-1.0)
                elif event.key == pygame.K_s:
                    cfs.start()
                elif event.key == pygame.K_l:
                    cfs.land()
                elif event.key == pygame.K_KP_PLUS:
                    cfs.change_movement_time(0.1)
                elif event.key == pygame.K_KP_MINUS:
                    cfs.change_movement_time(-0.1)
                elif event.key == pygame.K_KP6:
                    cfs.change_move_amount(0.1)
                elif event.key == pygame.K_KP4:
                    cfs.change_move_amount(-0.1)
                elif event.key == pygame.K_KP8:
                    cfs.change_height(0.1)
                elif event.key == pygame.K_KP2:
                    cfs.change_height(-0.1)
        if current_direction.length() > 0.01:
            cfs.move(current_direction)
        screen.fill(fill_color)
        text_surface = font.render("time for starting:" + format_decimal(cfs.start_time), False, (250, 250, 250))
        screen.blit(text_surface, (10, 10))
        text_surface = font.render("time for landing:" + format_decimal(cfs.land_time), False, (250, 250, 250))
        screen.blit(text_surface, (10, 45))
        text_surface = font.render("time for moving:" + format_decimal(cfs.movement_time), False, (250, 250, 250))
        screen.blit(text_surface, (10, 80))
        text_surface = font.render("amount of moving:" + format_decimal(cfs.movement_amount), False, (250, 250, 250))
        screen.blit(text_surface, (10, 115))
        text_surface = font.render("height:" + format_decimal(cfs.height), False, (250, 250, 250))
        screen.blit(text_surface, (10, 150))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
