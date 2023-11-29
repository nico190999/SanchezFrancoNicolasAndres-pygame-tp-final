import pygame as pg
from constantes import *
from auxiliar import Auxiliar
from bullet import Bullet


class Enemy(pg.sprite.Sprite):
    def __init__(self,x, y, speed_walk, speed_run, gravity, power_jump, jump_height, width_player, height_player, life_bar_path, volume_game, volume_music) -> None:
        super().__init__()
        #Walk
        self.walk_right = Auxiliar.get_animation_list_from_folder(r"img\player\viking_daxe\Walk", width_player, height_player)
        self.walk_left = Auxiliar.get_animation_list_from_folder(r"img\player\viking_daxe\Walk", width_player, height_player, True)

        #Stay 
        self.stay_right = Auxiliar.get_animation_list_from_folder(r"img\player\viking_daxe\Stand", width_player, height_player)
        self.stay_left = Auxiliar.get_animation_list_from_folder(r"img\player\viking_daxe\Stand", width_player, height_player, True)

        #Attack
        self.attack_right = Auxiliar.get_animation_list_from_folder(r"img\player\viking_daxe\Attack2H", width_player, height_player)
        self.attack_left = Auxiliar.get_animation_list_from_folder(r"img\player\viking_daxe\Attack2H", width_player, height_player, True)

        #Die
        self.die_right = Auxiliar.get_animation_list_from_folder(r"img\player\viking_daxe\Die", width_player, height_player)
        self.die_left = Auxiliar.get_animation_list_from_folder(r"img\player\viking_daxe\Die", width_player, height_player, True)

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
        self.y_position_start_jump = 0
        self.max_y_jump = jump_height
        self.life_bar_path = life_bar_path
        self.hit_counter = 0
        self.sound_enemy_hurted = pg.mixer.Sound(r"sounds\uuhhh_iqsgYFh.mp3")
        self.collision_amunt_for_shoot = 0
        self.action_while_player_is_in_visual_range = False
        self.bullet_group = pg.sprite.Group()

        self.is_alive = True


        self.animation = self.stay_left #Para definir con que accion comienza, animación en curso
        self.image = self.animation[int(self.frame)]
        self.rect = self.image.get_rect() 

        #Coordenadas de spawn del personaje
        self.rect.x = x
        self.rect.y = y

        #Rectangulo de colisiones general
        self.rect_player = pg.Rect(self.rect.x + 45, self.rect.y + 50, self.rect.width / 5, 50)

        #Rectangulo de vision
        self.rect_vision_range = pg.Rect(self.rect.x + (-320), self.rect.y + 35, self.rect.width * 3, 50)

        #Rectangulo de vida
        self.image_life_bar = pg.image.load(self.life_bar_path)
        self.image_life_bar = pg.transform.scale(self.image_life_bar, (802 / 9, 53 / 5))
        self.rect_life_bar = self.image.get_rect()
        self.rect_life_bar.x = x + 13
        self.rect_life_bar.y = y + 10

        #Volumen musica y juego
        self.volume_game = volume_game
        self.volume_music = volume_music

        self.bullet_group = pg.sprite.Group()


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

    #Función morir
    def die(self):
        if self.is_looking_right == True:
            self.animation = self.die_right
        else:
            self.animation = self.die_left
        self.frame_dying = 0
        self.move_x = 0
        self.is_on_floor = True
        self.is_jumping = False
    
    #Función para crear bala
    def create_bullet(self):
        return Bullet(self.rect.x, self.rect.y, self.is_looking_right)

    #Función ataque disparo
    def shoot_attack(self):
        if self.is_on_floor:
            if self.is_looking_right:
                self.animation = self.attack_right
            else:
                self.animation = self.attack_left
            self.move_x = 0
            self.bullet_group.add(self.create_bullet())
            self.frame = 0
            self.is_jumping = False
        else:
            self.is_on_floor = False

    #Función para que aumente en el eje X
    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.rect_player.x += delta_x
        self.rect_life_bar.x += delta_x
        self.rect_vision_range.x += delta_x

    #Función para que aumente en el eje X
    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.rect_player.y += delta_y
        self.rect_life_bar.y += delta_y

    #Movimientos automaticos
    def automatic_movement(self, pos_x_positive, pos_x_negative):
        if self.rect.x <= pos_x_negative:
            self.walk("Right")
        elif self.rect.x >= pos_x_positive:
            self.walk("Left")

    def update(self, player):
        #Para que actualice la clase de balas
        self.bullet_group.update()
        #Para que vaya actualizando la barra de vida y volumen
        self.image_life_bar = pg.image.load(self.life_bar_path)
        self.image_life_bar = pg.transform.scale(self.image_life_bar, (802 / 9, 53 / 5))
        self.sound_enemy_hurted.set_volume(self.volume_game)


        if (self.frame < len(self.animation) - 1):
            self.frame += 0.2
        else:
            self.frame = 0
            if self.is_jumping:
                self.is_jumping = False
                self.move_y = 0
        
        self.add_x(self.move_x)
        self.add_y(self.move_y)

        self.automatic_movement(920, -30)


        #Gravedad aplicada
        if self.rect.y < 400:
            self.rect.y += self.gravity
        else:
            self.is_on_floor = True
        
        #Limites establecidos del personaje
        if self.rect.x < -30:
            self.rect.x = -30
        if self.rect.x > 920:
            self.rect.x = 920
        if self.rect.y < 0:
            self.rect.y = 0

        #Limites rectangulo de colision general
        if self.rect_player.x < 10:
            self.rect_player.x = 10
        if self.rect_player.x > 970:
            self.rect_player.x = 970
        if self.rect_player.y < 40:
            self.rect_player.y = 40

        #Limites rectangulo de barra de vida
        if self.rect_life_bar.x < -8:
            self.rect_life_bar.x = -8
        if self.rect_life_bar.x > 940:
            self.rect_life_bar.x = 940
        if self.rect_life_bar.y < 15:
            self.rect_life_bar.y = 15

        #Para que vaya actualizando de lado el rectangulo
        if self.is_looking_right:
            self.rect_vision_range = pg.Rect(self.rect.x + 80, self.rect.y + 35, self.rect.width * 3, 50)
        else:
            self.rect_vision_range = pg.Rect(self.rect.x + (-320), self.rect.y + 35, self.rect.width * 3, 50)


        #Detección de colision de jugador con campo de vision del enemigo
        if self.rect_vision_range.colliderect(player.rect_player):            
            self.collision_amunt_for_shoot += 0.1
            if self.collision_amunt_for_shoot > 8:
                self.shoot_attack()
                self.collision_amunt_for_shoot = 0
        else:
            if self.is_looking_right:
                self.walk("Right")
            else:
                self.walk("Left")
        
        #Detección de colision de bala con enemigo
        # for bullet in self.bullet_group:
        #     if bullet.rect.collide(player):
        #         print("Colisiono la bala del enemigo con el player")
        # if pg.sprite.groupcollide(self.bullet_group, player, True, False):
        #     print("Colision de bala del enemigo con jugador")
            # if self.hit_counter < 3:
            #     self.hit_counter += 1
            #     self.sound_enemy_hurted.play()
            # self.life_bar_path = r"img\life bar\{}.png".format(str(self.hit_counter))
            # if self.hit_counter == 3:
            #     self.die()
            #     # enemies.remove(self)

    def draw(self, screen):
        if self.is_alive:
            self.image = self.animation[int(self.frame)]
            screen.blit(self.image, self.rect)
            screen.blit(self.image_life_bar, self.rect_life_bar)
            self.bullet_group.draw(screen)
            if DEBUG:
                pg.draw.rect(screen, (255,0,0), self.rect_player)
                pg.draw.rect(screen, (0,255,0), self.rect_vision_range)