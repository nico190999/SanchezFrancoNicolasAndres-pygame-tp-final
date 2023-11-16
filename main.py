import pygame as pg
import os
from constantes import *
from player import Player

#Crear ventana
screen = pg.display.set_mode((ancho_ventana, alto_ventana))

#Para inicializar el juego
pg.init()

#Tiempo
clock = pg.time.Clock()

#Cargar imagen
imagen_fondo = pg.image.load(r"img\background\landscape.jpg")
imagen_fondo = pg.transform.scale(imagen_fondo, (ancho_ventana, alto_ventana))

#Bandera de juego en ejecución
juego_ejecutandose = True

#Se le asigna la clase Player
player_uno = Player()

while juego_ejecutandose:
    for event in pg.event.get(): #Iterar todos los eventos del juego
        if event.type == pg.QUIT:
            pg.quit()
            juego_ejecutandose = False
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                player_uno.player_control(5, 0)
            
            if event.key == pg.K_a:
                player_uno.player_control(-5, 0)
    delta_ms =  clock.tick(FPS)
    player_uno.update()
    player_uno.draw(screen) #Para dibujar al personaje en el juego
    pg.display.flip() #Para que el jugador aparezca, sin esta función no aparece por pantalla
    screen.blit(imagen_fondo, imagen_fondo.get_rect())
    # pg.display.update()