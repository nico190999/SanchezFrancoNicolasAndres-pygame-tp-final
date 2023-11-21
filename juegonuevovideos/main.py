import pygame as pg
import os
from constantes import *
from player import Player
from enemy import Enemy
from platform1 import Platform



#Para inicializar el juego
pg.init()

#Crear ventana
screen = pg.display.set_mode((width_window, height_window))

#Tiempo
clock = pg.time.Clock()

#Cargar imagen
background_image = pg.image.load(r"img\background\allmountain.png")
#Para establecer el tamaño en la pantalla, se pasa como parametro la imagen cargada y el ancho y alto
background_image = pg.transform.scale(background_image, (width_window, height_window))

#Bandera de juego en ejecución
juego_ejecutandose = True

#Asignación de clases
main_player = Player(x=0, y=440, speed_walk=4, speed_run=8, gravity=8, power_jump=16, jump_height=200)
enemy = Enemy(x=935, y=440, speed_walk=5, speed_run=10, gravity=8, power_jump=16, jump_height=200)
platforms_list = []
platforms_list.append(Platform(x=400, y=400, width=40, height=40))
platforms_list.append(Platform(x=440, y=400, width=40, height=40))


player_is_looking_right = True
while juego_ejecutandose:
    for event in pg.event.get(): #Iterar la lista de todos los eventos del juego
        if event.type == pg.QUIT:
            juego_ejecutandose = False #Hace que salga del buvle del juego y vaya directo al pg.quit()
            
        #Acciones automaticas enemigo
        if enemy.rect.x <= 0:
            enemy.walk("Right")
        if enemy.rect.x >= 935:
            enemy.walk("Left")

        #Acciones cuando se apretan las teclas
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                main_player.walk("Right")
            elif event.key == pg.K_a:
                main_player.walk("Left")
            elif event.key == pg.K_LSHIFT:
                main_player.run()
            elif event.key == pg.K_w:
                main_player.jump(True)
            elif event.key == pg.K_f:
                main_player.attack()
        #Acciones si las teclas se dejan de presionar para que se quede quieto
        if event.type == pg.KEYUP:
            if event.key == pg.K_d or event.key == pg.K_a or event.key == pg.K_LSHIFT or event.key == pg.K_f:
                main_player.stay()
            if event.key == pg.K_a:
                main_player.jump(False)
        
    
    # lista_teclas_presionadas = pg.key.get_pressed()
    # if lista_teclas_presionadas[pg.K_d]:
    #     main_player.walk("Right")
    # if lista_teclas_presionadas[pg.K_a]:
    #     main_player.walk("Left")

    delta_ms = clock.tick(FPS) #Cantidad de milisegundos

    #Main Player
    main_player.update(delta_ms) #Cada cuanto queremos que se vaya actualizando, si aumenta el delta, aumenta la velocidad
    main_player.draw(screen) #Para dibujar al personaje en el juego

    #Enemy
    enemy.update(delta_ms)
    enemy.draw(screen)

    #Plataformas
    for platform in platforms_list:
        platform.draw(screen)

    pg.display.flip() #Para que el jugador aparezca, sin esta función no aparece por pantalla
    screen.blit(background_image, background_image.get_rect())
pg.quit()