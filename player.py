import pygame as pg
import os
from constantes import *
from auxiliar import Auxiliar
from bullet import Bullet


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

        #Rectangulos de colisiones 
        self.rect_ground_collition = pg.Rect(self.rect.x + self.rect.width / 3, self.rect.y + self.rect.height - 30, self.rect.width / 5, 10)
        self.rect_player = pg.Rect(self.rect.x + 45, self.rect.y + 50, self.rect.width / 5, 50)
        self.rect_top_head_player = pg.Rect((self.rect.x + self.rect.width / 3) + 5, self.rect.y + 25, self.rect.width / 5, 10)


        # Atributos para disparar y recargar
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.bullet_group = pg.sprite.Group()
        self.puntaje = 0

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


    def shoot(self):
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



        

    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.rect_ground_collition.x += delta_x
        self.rect_player.x += delta_x
        self.rect_top_head_player.x += delta_x

    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.rect_ground_collition.y += delta_y
        self.rect_player.y += delta_y
        self.rect_top_head_player.y += delta_y


    def is_on_platform(self, platforms_list):
        bool_return = False
        if self.rect.y >= 440:
            bool_return = True
        else:
            for platform in platforms_list:
                if (self.rect_ground_collition.colliderect(platform.rect_ground_collition)): #Corrobora si el rectangulo de los pies del personaje conlisiona contra el rectangulo superior de la plataforma
                    bool_return = True
                    break
                elif (self.rect_top_head_player.colliderect(platform.rect_down_collition)):
                    bool_return = False
                    self.move_y = 0
                    break
        return bool_return
    
    




    def update(self, platform_list, coin_list): 
        if (self.frame < len(self.animation) - 1):
            self.frame += 0.2
        else:
            self.frame = 0
            if self.is_jumping:
                self.is_jumping = False
                self.move_y = 0
            
        #Determinar maxima altura del salto
        if ((abs(self.y_position_start_jump) - abs(self.rect.y)) > self.max_y_jump and self.is_jumping):
            self.move_y = 0
        
        self.add_x(self.move_x)
        self.add_y(self.move_y)
    
        #Gravedad aplicada
        if self.is_on_platform(platform_list) == False:
            self.add_y(self.gravity)
        else:
            self.is_on_floor = True

        #Limites establecidos del personaje
        if self.rect.x < -30:
            self.rect.x = -30
        if self.rect.x > 920:
            self.rect.x = 920
        if self.rect.y < 0:
            self.rect.y = 0
        
        #Limites rectangulo de colision con plataformas
        if self.rect_ground_collition.x < 10:
            self.rect_ground_collition.x = 10
        if self.rect_ground_collition.x > 970:
            self.rect_ground_collition.x = 970
        if self.rect_ground_collition.y < 90:
            self.rect_ground_collition.y = 90

        #Limites rectangulo de colision con coin
        if self.rect_player.x < 10:
            self.rect_player.x = 10
        if self.rect_player.x > 970:
            self.rect_player.x = 970
        if self.rect_player.y < 90:
            self.rect_player.y = 90
            

        #detección colisión con coin
        for coin in coin_list:
            if (self.rect_player.colliderect(coin.rect_coin)):
                print("Estoy colisionando")
                coin_list.remove(coin)




    def create_bullet(self):
        return Bullet(self.rect.x, self.rect.y, self.is_looking_right)


    def draw(self, screen):
        self.image = self.animation[int(self.frame)]
        screen.blit(self.image, self.rect)
        if DEBUG:
            pg.draw.rect(screen, (255,0,0), self.rect_player)
            pg.draw.rect(screen, (0,0,255), self.rect_ground_collition)
            pg.draw.rect(screen, (0,255,0), self.rect_top_head_player)