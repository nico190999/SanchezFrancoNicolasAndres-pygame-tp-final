import pygame as pg
import sys
from constantes import *
from player import Player
from enemy import Enemy
from platform1 import Platform
from coin import Coin
from button import Button
from saw import Saw

#Para inicializar el juego
pg.init()

#Crear ventana
screen = pg.display.set_mode((width_window, height_window))

#Tiempo
clock = pg.time.Clock()

#Pantallas
def settings(volume_music, volume_game, level):
    level = level
    #Image
    background_image_main_menu = pg.image.load(r"img\background\backgroundimage_main_menu.jpg")
    background_image_main_menu = pg.transform.scale(background_image_main_menu, (width_window, height_window))

    #Sounds
    click_sound = pg.mixer.Sound(r"sounds\click_sound.mp3")
    background_music = pg.mixer.Sound(r"sounds\main_menu_sound.mp3")

    pg.display.set_caption("Settings")
    background_music.play()
    executing_volume_menu = True
    while executing_volume_menu:
        click_sound.set_volume(volume_game)
        background_music.set_volume(volume_music)
        screen.blit(background_image_main_menu, (0,0))
        font = pg.font.Font(None, 30)
        mouse_position = pg.mouse.get_pos()

        volume_text = font.render("VOLUME", True, "#b68f40")
        volume_rect = volume_text.get_rect(center=(width_window / 2, 110))

        game_name_text = font.render("VIKINGS OF THE FUTURE", True, "#b68f40")
        rect_game_name = game_name_text.get_rect(center=(width_window / 2, 45))

        music_text = font.render("MUSIC", True, "#FFFFFF")
        rect_music = music_text.get_rect(center=((width_window / 2) - 150, 250))

        sound_text = font.render("SOUND", True, "#FFFFFF")
        rect_sound = sound_text.get_rect(center=((width_window / 2) - 150, 300))

        plus_music_volume_button = Button(image=None, pos=((width_window / 2),247), text_input="+", font=font, base_color="grey", hovering_color="White")
        less_music_volume_button = Button(image=None, pos=((width_window / 2)- 50,247), text_input="-", font=font, base_color="grey", hovering_color="White")

        plus_sound_volume_button = Button(image=None, pos=((width_window / 2),297), text_input="+", font=font, base_color="grey", hovering_color="White")
        less_sound_volume_button = Button(image=None, pos=((width_window / 2)- 50,297), text_input="-", font=font, base_color="grey", hovering_color="White")

        return_to_main_menu_button = Button(image=None, pos=(width_window / 2,513), text_input="RETURN TO MAIN MENU", font=font, base_color="grey", hovering_color="White")

        screen.blit(volume_text, volume_rect)
        screen.blit(game_name_text, rect_game_name)
        screen.blit(music_text, rect_music)
        screen.blit(sound_text, rect_sound)

        for button in [plus_music_volume_button, less_music_volume_button, return_to_main_menu_button, plus_sound_volume_button, less_sound_volume_button]:
            button.changecolor(mouse_position)
            button.update(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if plus_music_volume_button.checkforinput(mouse_position):
                    click_sound.play()
                    volume_music = plus_volume(volume_music)
                elif less_music_volume_button.checkforinput(mouse_position):
                    click_sound.play()
                    volume_music = less_volume(volume_music)
                elif plus_sound_volume_button.checkforinput(mouse_position):
                    click_sound.play()
                    volume_game = plus_volume(volume_game)
                elif less_sound_volume_button.checkforinput(mouse_position):
                    click_sound.play()
                    volume_game = less_volume(volume_game)
                elif return_to_main_menu_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    main_menu(volume_music, volume_game, level)

        show_music_level = font.render(f"({volume_music:.2f})", True, (255,255,255))
        screen.blit(show_music_level, (527, 238))

        show_sound_level = font.render(f"({volume_game:.2f})", True, (255,255,255))
        screen.blit(show_sound_level, (527, 290))

        pg.display.update()

def pause(volume_music, volume_game):
    #Image
    background_image_pause = pg.image.load(r"img\background\pause.png")
    background_image_pause = pg.transform.scale(background_image_pause, ((background_image_pause.get_width() / 2), (background_image_pause.get_height() / 2)))
    background_image_pause_rect = background_image_pause.get_rect()
    background_image_pause_rect.center = (width_window / 2, height_window / 2)
    #Sounds
    sound_unpause = pg.mixer.Sound(r"sounds\unpause-106278.mp3")
    click_sound = pg.mixer.Sound(r"sounds\click_sound.mp3")
    sound_music_game = pg.mixer.Sound(r"sounds\Eric Skiff - A Night Of Dizzy Spells  NO COPYRIGHT 8-bit Music  Background.mp3")

    paused = True
    while paused:
        mouse_position = pg.mouse.get_pos()
        
        screen.blit(background_image_pause, background_image_pause_rect)


        resume_button = Button(image=None, pos=(width_window / 2,225), text_input="RESUME", font=(pg.font.Font(None, 35)), base_color="black", hovering_color="White")
        settings_button = Button(image=None, pos=(width_window / 2,325), text_input="SETTINGS", font=(pg.font.Font(None, 35)), base_color="black", hovering_color="White")
        return_to_main_menu_button = Button(image=None, pos=(width_window / 2,425), text_input="RETURN TO MAIN MENU", font=(pg.font.Font(None, 35)), base_color="black", hovering_color="White")

        for button in [resume_button, settings_button, return_to_main_menu_button]:
            button.changecolor(mouse_position)
            button.update(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sound_unpause.play()
                    paused = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if resume_button.checkforinput(mouse_position):
                    sound_unpause.play()
                    paused = False
                if settings_button.checkforinput(mouse_position):
                    click_sound.play()
                if return_to_main_menu_button.checkforinput(mouse_position):
                    click_sound.play()
                    main_menu(volume_music, volume_game, 1)

        pg.display.flip()

def play_game(volume_music, volume_game, level):
    #Para inicializar el juego
    pg.init()
    #Image
    background_image = pg.image.load(r"img\background\allmountain.png")
    background_image = pg.transform.scale(background_image, (width_window, height_window))#Para establecer el tamaño en la pantalla, se pasa como parametro la imagen cargada y el ancho y alto

    ###########################################################################################################
    #ASIGNACIÓN DE NIVEL

    level = level
    ###########################################################################################################
    if level ==1:
        #ASIGNACIÓN DE CLASES
        #main player
        main_player = Player(x=-30, y=440, speed_walk=4, speed_run=8, gravity=8, power_jump=16, jump_height=200, width_player=120, height_player=120, volume_game=volume_game, volume_music=volume_music, life_bar_path=r"img\life bar\0.png")


        #Platforms
        platforms_list = [(Platform(x=380, y=400, width=200, height=40)),
                        (Platform(x=100, y=280, width=200, height=40)),
                        (Platform(x=650, y=280, width=200, height=40)),
                        (Platform(x=380, y=150, width=200, height=40))]
        #Bullet
        bullet_group = pg.sprite.Group()

        #Coin
        coin_list = [(Coin(pos_x=180, pos_y=220)),
                    (Coin(pos_x=460, pos_y=350)),
                    (Coin(pos_x=730, pos_y=220)),
                    (Coin(pos_x=460, pos_y=100)),
                    (Coin(pos_x=870, pos_y=480))]
        
        #Saw(trap)
        saw_trap_list = [Saw(pos_x=100, pos_y=247),
                        Saw(pos_x=650, pos_y=247)]

        #Enemy
        enemies = pg.sprite.Group()
        enemy = Enemy(x=935, y=440, speed_walk=0.6, speed_run=10, gravity=8, power_jump=16, jump_height=200, width_player=120, height_player=120, life_bar_path=r"img\life bar\0.png", volume_game=volume_game, volume_music=volume_music)
        enemy_1 = Enemy(x=500, y=440, speed_walk=0.6, speed_run=10, gravity=8, power_jump=16, jump_height=200, width_player=120, height_player=120, life_bar_path=r"img\life bar\0.png", volume_game=volume_game, volume_music=volume_music)
        enemies.add(enemy)
        enemies.add(enemy_1)

    if level == 2:
        #ASIGNACIÓN DE CLASES
        #main player
        main_player = Player(x=-30, y=440, speed_walk=4, speed_run=8, gravity=8, power_jump=16, jump_height=200, width_player=120, height_player=120, volume_game=volume_game, volume_music=volume_music, life_bar_path=r"img\life bar\0.png")


        #Platforms
        platforms_list = [(Platform(x=0, y=400, width=600, height=40)),
                        (Platform(x=20, y=320, width=50, height=40)),
                        (Platform(x=900, y=420, width=100, height=40)),
                        (Platform(x=650, y=275, width=350, height=40)),
                        (Platform(x=150, y=280, width=250, height=40)),
                        (Platform(x=600, y=140, width=300, height=40)),
                        (Platform(x=450, y=200, width=50, height=40))]
        #Bullet
        bullet_group = pg.sprite.Group()

        #Coin
        coin_list = [(Coin(pos_x=25, pos_y=280)),
                    (Coin(pos_x=460, pos_y=350)),
                    (Coin(pos_x=920, pos_y=220)),
                    (Coin(pos_x=455, pos_y=150)),
                    (Coin(pos_x=930, pos_y=360))]
        
        #Saw(trap)
        saw_trap_list = [Saw(pos_x=150, pos_y=367),
                        Saw(pos_x=210, pos_y=367),
                        Saw(pos_x=270, pos_y=367),
                        Saw(pos_x=330, pos_y=367),
                        Saw(pos_x=150, pos_y=248),
                        Saw(pos_x=650, pos_y=242),
                        Saw(pos_x=710, pos_y=242),
                        Saw(pos_x=770, pos_y=242),
                        Saw(pos_x=830, pos_y=242)
                        ]
        
        #Enemy
        enemies = pg.sprite.Group()
        enemy = Enemy(x=935, y=440, speed_walk=0.6, speed_run=10, gravity=8, power_jump=16, jump_height=200, width_player=120, height_player=120, life_bar_path=r"img\life bar\0.png", volume_game=volume_game, volume_music=volume_music)
        enemies.add(enemy)

    if level == 3:
        #ASIGNACIÓN DE CLASES
        #main player
        main_player = Player(x=-30, y=200, speed_walk=4, speed_run=8, gravity=8, power_jump=16, jump_height=200, width_player=120, height_player=120, volume_game=volume_game, volume_music=volume_music, life_bar_path=r"img\life bar\0.png")


        #Platforms
        platforms_list = [(Platform(x=0, y=300, width=800, height=40)),
                        (Platform(x=200, y=200, width=50, height=40)),
                        (Platform(x=400, y=200, width=50, height=40)),
                        (Platform(x=0, y=100, width=50, height=40)),
                        (Platform(x=900, y=400, width=100, height=40))
                        ]
        #Bullet
        bullet_group = pg.sprite.Group()

        #Coin
        coin_list = [(Coin(pos_x=5, pos_y=50)),
                    (Coin(pos_x=205, pos_y=160)),
                    (Coin(pos_x=405, pos_y=160)),
                    (Coin(pos_x=470, pos_y=250)),
                    (Coin(pos_x=660, pos_y=250)),
                    (Coin(pos_x=930, pos_y=350)),
                    (Coin(pos_x=750, pos_y=470)),
                    (Coin(pos_x=500, pos_y=470)),
                    (Coin(pos_x=300, pos_y=470)),
                    (Coin(pos_x=100, pos_y=470))
                    ]
        
        #Saw(trap)
        saw_trap_list = [Saw(pos_x=230, pos_y=268),
                        Saw(pos_x=290, pos_y=268),
                        Saw(pos_x=350, pos_y=268),
                        Saw(pos_x=550, pos_y=268),
                        Saw(pos_x=600, pos_y=495),
                        Saw(pos_x=400, pos_y=495),
                        Saw(pos_x=200, pos_y=495),
                        Saw(pos_x=0, pos_y=495),
                        ]
        
        #Enemy
        enemies = pg.sprite.Group()
        enemy = Enemy(x=935, y=440, speed_walk=0.6, speed_run=10, gravity=8, power_jump=16, jump_height=200, width_player=120, height_player=120, life_bar_path=r"img\life bar\0.png", volume_game=volume_game, volume_music=volume_music)
        enemies.add(enemy)
    ###########################################################################################################

    #Sounds
    sound_jump = pg.mixer.Sound(r"sounds\cartoon-jump-6462.mp3")
    sound_shoot = pg.mixer.Sound(r"sounds\laser-gun-81720.mp3")
    sound_pause = pg.mixer.Sound(r"sounds\pause-89443.mp3")
    sound_music_game = pg.mixer.Sound(r"sounds\Eric Skiff - A Night Of Dizzy Spells  NO COPYRIGHT 8-bit Music  Background.mp3")

    start_time = pg.time.get_ticks()
    executing_game = True
    sound_music_game.play()
    pg.display.set_caption("Play Game")
    while executing_game:
        sound_music_game.set_volume(volume_music)
        sound_jump.set_volume(volume_game)
        sound_shoot.set_volume(volume_game)
        sound_pause.set_volume(volume_game)
        for event in pg.event.get(): #Iterar la lista de todos los eventos del juego
            if event.type == pg.QUIT:
                executing_game = False #Hace que salga del buvle del juego y vaya directo al pg.quit()
                pg.quit()


            #Acciones cuando se apretan las teclas para que accione el jugador principal
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    main_player.walk("Right")
                elif event.key == pg.K_a:
                    main_player.walk("Left")
                elif event.key == pg.K_LSHIFT:
                    main_player.run()
                elif event.key == pg.K_w:
                    main_player.jump(True)
                    sound_jump.play()
                elif event.key == pg.K_f:
                    main_player.shoot_attack()
                    sound_shoot.play()
                elif event.key == pg.K_ESCAPE:
                    sound_music_game.stop()
                    sound_pause.play()
                    pause(volume_music, volume_game)

            #Acciones si las teclas se dejan de presionar para que se quede quieto
            if event.type == pg.KEYUP:
                if event.key == pg.K_d or event.key == pg.K_a or event.key == pg.K_LSHIFT or event.key == pg.K_f:
                    main_player.stay()
                if event.key == pg.K_a:
                    main_player.jump(False)

        delta_ms = clock.tick(FPS) #Cantidad de milisegundos

        #Detección para ganar juego
        if len(coin_list) == 0:
            sound_music_game.stop()
            main_player.sound_hurt.stop()
            main_player.get_coin_sound.stop()
            if level < 3:
                level_completed(volume_music, volume_game, (level + 1))
            else:
                winner(volume_music, volume_game)

        #Enemy
        enemy.update(main_player)
        enemy.draw(screen)
        enemy_1.update(main_player)
        enemy_1.draw(screen)


        #Plataformas
        for platform in platforms_list:
            platform.draw(screen)
        
        # #Bullet
        # bullet_group.draw(screen)
        # bullet_group.update()

        #Saw
        for saw_trap in saw_trap_list:
            saw_trap.draw(screen)
            saw_trap.update(screen)

        #Coin
        for coin in coin_list:
            coin.draw(screen)
            coin.update(screen)

        #Score
        font_color = (0, 0, 255)
        font = pg.font.Font(None, 36)
        score = main_player.points
        def show_score(score):
            score_text = font.render("Score: {}".format(score), True, font_color)
            screen.blit(score_text, (10, 10))
        show_score(score)

        ###########################################################
        #Cronometro por pantalla
        # Calcula el tiempo transcurrido en segundos
        elapsed_time = pg.time.get_ticks() - start_time
        seconds = elapsed_time // 1000
        # Formatea el tiempo en una cadena de texto
        timer_text = f"Time: {seconds} s"
        # Muestra el cronómetro
        timer_surface = font.render(timer_text, True, font_color)
        screen.blit(timer_surface, (10, 40))
        ###########################################################

        #Main Player
        main_player.update(platforms_list, coin_list, saw_trap_list, enemies) #Cada cuanto queremos que se vaya actualizando, si aumenta el delta, aumenta la velocidad
        main_player.draw(screen) #Para dibujar al personaje en el juego
        #Detección de nivel perdido
        if (main_player.hit_counter == 3) or (seconds == 61):
            sound_music_game.stop()
            main_player.sound_hurt.stop()
            main_player.get_coin_sound.stop()
            main_player_death(volume_music, volume_game, level)
        
        # enemies.update(main_player)
        # enemies.draw(screen)

        pg.display.flip() #Para que el jugador aparezca, sin esta función no aparece por pantalla
        screen.blit(background_image, background_image.get_rect())

def level_completed(volume_music, volume_game, level):
    #Image
    background_image_main_menu = pg.image.load(r"img\background\level_completed_2.png")
    background_image_main_menu = pg.transform.scale(background_image_main_menu, (width_window, height_window))

    #Sounds
    click_sound = pg.mixer.Sound(r"sounds\click_sound.mp3")
    background_music = pg.mixer.Sound(r"sounds\brass-new-level-151765.mp3")

    #Nombre de la ventana
    pg.display.set_caption("Level_completed")

    background_music.play()
    while True:
        background_music.set_volume(volume_music)
        click_sound.set_volume(volume_game)

        screen.blit(background_image_main_menu, (0,0))

        mouse_position = pg.mouse.get_pos()


        return_to_main_menu_button = Button(image=None, pos=(230,220), text_input="RETURN TO MAIN MENU", font=(pg.font.Font(None, 35)), base_color="black", hovering_color="White")
        next_level_button = Button(image=None, pos=(230,160), text_input="NEXT LEVEL", font=(pg.font.Font(None, 35)), base_color="black", hovering_color="White")

        for button in [return_to_main_menu_button, next_level_button]:
            button.changecolor(mouse_position)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if return_to_main_menu_button.checkforinput(mouse_position):
                    click_sound.play()
                    main_menu(volume_music, volume_game, 1)
                if next_level_button.checkforinput(mouse_position):
                    click_sound.play()
                    play_game(volume_music, volume_game, level)
        pg.display.update()

def winner(volume_music, volume_game):
    #Image
    background_image_main_menu = pg.image.load(r"img\background\john_cena.jpg")
    background_image_main_menu = pg.transform.scale(background_image_main_menu, (width_window, height_window))

    #Sounds
    click_sound = pg.mixer.Sound(r"sounds\click_sound.mp3")
    background_music = pg.mixer.Sound(r"sounds\John Cena - The Time Is Now (Entrance Theme) (mp3cut.net).mp3")

    #Nombre de la ventana
    pg.display.set_caption("YOU ARE A WINNER!!!!")

    background_music.play()
    while True:
        background_music.set_volume(volume_music)
        click_sound.set_volume(volume_game)

        screen.blit(background_image_main_menu, (0,0))

        mouse_position = pg.mouse.get_pos()


        return_to_main_menu_button = Button(image=None, pos=(830,210), text_input="RETURN TO MAIN MENU", font=(pg.font.Font(None, 30)), base_color="black", hovering_color="White")

        for button in [return_to_main_menu_button]:
            button.changecolor(mouse_position)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if return_to_main_menu_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    main_menu(volume_music, volume_game, 1)
        pg.display.update()

def main_player_death(volume_music, volume_game, level):
    level = level
    #Image
    background_image_main_menu = pg.image.load(r"img\background\sad_viking.png")
    background_image_main_menu = pg.transform.scale(background_image_main_menu, (width_window, height_window))

    #Sounds
    click_sound = pg.mixer.Sound(r"sounds\click_sound.mp3")
    background_music = pg.mixer.Sound(r"sounds\violin-lose-1-175615.mp3")

    #Nombre de la ventana
    pg.display.set_caption("Level_completed")

    background_music.play()
    while True:
        background_music.set_volume(volume_music)
        click_sound.set_volume(volume_game)

        screen.blit(background_image_main_menu, (0,0))

        mouse_position = pg.mouse.get_pos()

        return_to_main_menu_button = Button(image=None, pos=(190,200), text_input="RETURN TO MAIN MENU", font=(pg.font.Font(None, 35)), base_color="black", hovering_color="White")
        try_again_button = Button(image=None, pos=(190,160), text_input="TRY AGAIN", font=(pg.font.Font(None, 35)), base_color="black", hovering_color="White")


        for button in [return_to_main_menu_button, try_again_button]:
            button.changecolor(mouse_position)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if return_to_main_menu_button.checkforinput(mouse_position):
                    click_sound.play()
                    main_menu(volume_music, volume_game, 1)
                if try_again_button.checkforinput(mouse_position):
                    click_sound.play()
                    play_game(volume_music, volume_game, level)
        pg.display.update()

def select_level_window(volume_music, volume_game):
    #Image
    background_image_main_menu = pg.image.load(r"img\background\backgroundimage_main_menu.jpg")
    background_image_main_menu = pg.transform.scale(background_image_main_menu, (width_window, height_window))

    #Sounds
    click_sound = pg.mixer.Sound(r"sounds\click_sound.mp3")
    background_music = pg.mixer.Sound(r"sounds\main_menu_sound.mp3")

    pg.display.set_caption("Select Level")
    background_music.play()
    while True:
        click_sound.set_volume(volume_game)
        background_music.set_volume(volume_music)
        screen.blit(background_image_main_menu, (0,0))
        font = pg.font.Font(None, 30)
        mouse_position = pg.mouse.get_pos()

        volume_text = font.render("SELECT LEVEL", True, "#b68f40")
        volume_rect = volume_text.get_rect(center=(width_window / 2, 110))

        game_name_text = font.render("VIKINGS OF THE FUTURE", True, "#b68f40")
        rect_game_name = game_name_text.get_rect(center=(width_window / 2, 45))

        level_one_button = Button(image=None, pos=(width_window / 2,210), text_input="LEVEL 1", font=font, base_color="grey", hovering_color="White")
        level_two__button = Button(image=None, pos=(width_window / 2,310), text_input="LEVEL 2", font=font, base_color="grey", hovering_color="White")
        level_three_button = Button(image=None, pos=(width_window / 2,410), text_input="LEVEL 3", font=font, base_color="grey", hovering_color="White")

        return_to_main_menu_button = Button(image=None, pos=(width_window / 2,513), text_input="RETURN TO MAIN MENU", font=font, base_color="grey", hovering_color="White")

        screen.blit(volume_text, volume_rect)
        screen.blit(game_name_text, rect_game_name)

        for button in [level_one_button, level_two__button, level_three_button, return_to_main_menu_button]:
            button.changecolor(mouse_position)
            button.update(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if level_one_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    play_game(volume_music, volume_game, 1)
                elif level_two__button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    play_game(volume_music, volume_game, 2)
                elif level_three_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    play_game(volume_music, volume_game, 3)
                elif return_to_main_menu_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    main_menu(volume_music, volume_game, 1)

        pg.display.update()

def main_menu(volume_music, volume_game, level):
    #Para inicializar el juego
    pg.init()
    #Image
    background_image_main_menu = pg.image.load(r"img\background\backgroundimage_main_menu.jpg")
    background_image_main_menu = pg.transform.scale(background_image_main_menu, (width_window, height_window))

    #Sounds
    click_sound = pg.mixer.Sound(r"sounds\click_sound.mp3")
    background_music = pg.mixer.Sound(r"sounds\main_menu_sound.mp3")

    pg.display.set_caption("Menu")
    background_music.play()
    executing_main_menu = True
    while executing_main_menu:
        click_sound.set_volume(volume_game)
        background_music.set_volume(volume_music)
        screen.blit(background_image_main_menu, (0,0))
        font = pg.font.Font(None, 30)
        mouse_position = pg.mouse.get_pos()

        menu_text = font.render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(width_window / 2, 110))

        game_name_text = font.render("VIKINGS OF THE FUTURE", True, "#b68f40")
        rect_game_name = game_name_text.get_rect(center=(width_window / 2, 45))

        play_button = Button(image=None, pos=(width_window / 2,210), text_input="PLAY", font=font, base_color="grey", hovering_color="White")
        options_button = Button(image=None, pos=(width_window / 2,410), text_input="SETTINGS", font=font, base_color="grey", hovering_color="White")
        quit_button = Button(image=None, pos=(width_window / 2,513), text_input="QUIT", font=font, base_color="grey", hovering_color="White")
        select_level_button = Button(image=None, pos=(width_window / 2,310), text_input="SELECT LEVEL", font=font, base_color="grey", hovering_color="White")

        screen.blit(menu_text, menu_rect)
        screen.blit(game_name_text, rect_game_name)

        for button in [play_button, options_button, quit_button, select_level_button]:
            button.changecolor(mouse_position)
            button.update(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    play_game(volume_music, volume_game, level)
                elif quit_button.checkforinput(mouse_position):
                    click_sound.play()
                    pg.quit()
                    sys.exit()
                elif options_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    settings(volume_music, volume_game, level)
                elif select_level_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    select_level_window(volume_music, volume_game)
        pg.display.update()

main_menu(0, 0.2, 1)