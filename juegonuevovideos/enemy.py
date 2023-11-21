import pygame as pg
from constantes import *
from auxiliar import Auxiliar


class Enemy:
    def __init__(self,x, y, speed_walk, speed_run, gravity, power_jump, jump_height) -> None:
        #Walk
        self.walk_right = Auxiliar.get_surface_from_sprite_sheet("img\player\walk\player_walk.png", 6, 1)
        self.walk_left = Auxiliar.get_surface_from_sprite_sheet("img\player\walk\player_walk.png", 6, 1, True)

        #Stay 
        self.stay_right = Auxiliar.get_surface_from_sprite_sheet("img\player\iddle\player_idle.png", 5, 1)
        self.stay_left = Auxiliar.get_surface_from_sprite_sheet("img\player\iddle\player_idle.png", 5, 1, True)

        #Jump
        self.jump_right = Auxiliar.get_surface_from_sprite_sheet("img\player\jump\player_jump.png", 6, 1)
        self.jump_left = Auxiliar.get_surface_from_sprite_sheet("img\player\jump\player_jump.png", 6, 1, True)

        #Run
        self.run_right = Auxiliar.get_surface_from_sprite_sheet(r"img\player\run\player_run.png", 2, 1)
        self.run_left = Auxiliar.get_surface_from_sprite_sheet(r"img\player\run\player_run.png", 2, 1, True)

        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.gravity = gravity
        self.power_jump = power_jump
        self.is_looking_right = False
        self.is_jumping = False
        self.is_on_floor = False
        # self.time_elapsed = 0
        self.y_position_start_jump = 0
        self.max_y_jump = jump_height


        self.animation = self.stay_left #Para definir con que accion comienza, animación en curso
        self.image = self.animation[int(self.frame)]
        self.rect = self.image.get_rect() 

        #Coordenadas de spawn del personaje
        self.rect.x = x
        self.rect.y = y

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
        
        self.rect.x += self.move_x 
        self.rect.y += self.move_y

        #Gravedad aplicada
        if self.rect.y < 400:
            self.rect.y += self.gravity
        else:
            self.is_on_floor = True

        #Limites establecidos del personaje
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 935:
            self.rect.x = 935
        if self.rect.y < 0:
            self.rect.y = 0

        


    ###########################

    def draw(self, screen):
        self.image = self.animation[int(self.frame)]
        screen.blit(self.image, self.rect)