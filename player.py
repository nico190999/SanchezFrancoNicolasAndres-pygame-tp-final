import pygame as pg
from constantes import *

def get_surface_from_sprite_sheet(path, columns, rows): #Función para obtener cada fotograma del sprite sheet
    lista = []
    surface_image = pg.image.load(path)
    fotograma_width = int(surface_image.get_width()/columns)
    fotograma_height = int(surface_image.get_height()/rows)
    for columna in range(columns):
        for fila in range(rows):
            x = columna * fotograma_width
            y = fila * fotograma_height
            surface_fotograma = surface_image.subsurface(x,y,fotograma_width,fotograma_height)
            lista.append(surface_fotograma)
    return lista

class Player:
    def __init__(self) -> None:
        self.walk = get_surface_from_sprite_sheet("img\player\walk\player_walk.png", 6, 1)
        self.stay = get_surface_from_sprite_sheet("img\player\iddle\player_idle.png", 5, 1)
        self.frame = 0
        self.score = 0 #Empieza con 0 puntos
        self.move_x = 0
        self.move_y = 0

        self.animation = self.walk #Para definir con que accion comienza, animación en curso
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect() 

    def player_control(self, x, y):
        self.move_x = x
        self.move_y = y


    def update(self):
        if (self.frame < len(self.animation) - 1):
            self.frame += 1            
        else:
            self.frame = 0
        self.rect.x = self.move_x
        self.rect.y = self.move_y

    def draw(self, screen):
        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
