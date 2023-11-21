import pygame as pg
import os
from constantes import *
from auxiliar import Auxiliar


class Player:
    def __init__(self,x, y, speed_walk, speed_run, gravity, power_jump, jump_height) -> None:
        #Walk
        self.walk_right = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Walk", 120, 120)
        self.walk_left = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Walk", 120, 120, True)

        #Stay 
        self.stay_right = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Stand", 120, 120)
        self.stay_left = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Stand", 120, 120, True)

        #Jump
        self.jump_right = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Jump", 120, 120)
        self.jump_left = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Jump", 120, 120, True)

        #Run
        self.run_right = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Run", 120, 120)
        self.run_left = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Run", 120, 120, True)

        #Attack
        self.attack_right = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Attack1H", 120, 120)
        self.attack_left = Auxiliar.get_animation_list_from_folder(r"img\player\viking_axe\Attack1H", 120, 120, True)

        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.gravity = gravity
        self.power_jump = power_jump
        self.is_looking_right = True
        self.is_jumping = False
        self.is_on_floor = False
        # self.time_elapsed = 0
        self.y_position_start_jump = 0
        self.max_y_jump = jump_height


        self.animation = self.stay_right #Para definir con que accion comienza, animación en curso
        self.image = self.animation[int(self.frame)]
        self.rect = self.image.get_rect() 

        #Coordenadas de spawn del personaje
        self.rect.x = x
        self.rect.y = y

        self.ground_collition_rect = pg.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.width, 10)

    #Función caminar
    def walk(self, direction):
        match direction:
            case "Right":
                self.move_x = self.speed_walk
                self.animation = self.walk_right
                self.is_looking_right = True
            case "Left":
                self.move_x = -self.speed_walk
                self.animation = self.walk_left
                self.is_looking_right = False
        self.frame = 0
        self.is_on_floor = True
        self.is_jumping = False

    #Función quedarse quieto
    def stay(self):
        if self.is_looking_right == True:
            self.animation = self.stay_right
        else:
            self.animation = self.stay_left
        self.frame = 0
        self.move_x = 0
        self.is_on_floor = True
        self.is_jumping = False

    #Función correr
    def run(self):
        if self.is_looking_right:
            self.move_x = self.speed_run
            self.animation = self.run_right
        else:
            self.move_x = -self.speed_run
            self.animation = self.run_left
        self.frame = 0
        self.is_on_floor = True
        self.is_jumping = False


    def attack(self):
        if self.is_on_floor:
            if self.is_looking_right:
                self.move_x = 0
                self.animation = self.attack_right
            else:
                self.move_x = 0
                self.animation = self.attack_left
            self.frame = 0
            self.is_jumping = False
        else:
            self.is_on_floor = False

    #Función saltar
    def jump(self, on_off=True):
        if on_off and self.is_jumping == False:
            self.y_position_start_jump = self.rect.y
            if self.is_looking_right and self.is_on_floor:
                self.move_y = -self.power_jump
                self.move_x = self.speed_walk
                self.animation = self.jump_right
            elif self.is_looking_right == False and self.is_on_floor:
                self.move_y = -self.power_jump
                self.move_x = -self.speed_walk
                self.animation = self.jump_left
            self.frame = 0
            self.is_jumping = True
            self.is_on_floor = False
        else:
            self.is_jumping = False
            self.stay()


    def update(self, delta_ms):
        # self.time_elapsed += delta_ms
        # if self.time_elapsed >= 200:
        #     self.time_elapsed = 0        
        if (self.frame < len(self.animation) - 1):
            self.frame += 0.2
        else:
            self.frame = 0
            if self.is_jumping:
                self.is_jumping = False
                self.move_y = 0
            # if not self.is_on_floor:
            #     self.is_jumping = False
            #     self.move_y = 0
            #     self.player_control("STAY")
            
        #Determinar maxima altura del salto
        if ((abs(self.y_position_start_jump) - abs(self.rect.y)) > self.max_y_jump and self.is_jumping):
            self.move_y = 0
        
        self.add_x(self.move_x)
        self.add_y(self.move_y)

        #Gravedad aplicada
        if self.rect.y < 440:
            self.add_y(self.gravity)
        else:
            self.is_on_floor = True

        #Limites establecidos del personaje
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 935:
            self.rect.x = 935
        if self.rect.y < 0:
            self.rect.y = 0

    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.ground_collition_rect.y += delta_y


    ###########################

    def draw(self, screen):
        pg.draw.rect(screen, (0,0,255), self.ground_collition_rect)
        self.image = self.animation[int(self.frame)]
        screen.blit(self.image, self.rect)
