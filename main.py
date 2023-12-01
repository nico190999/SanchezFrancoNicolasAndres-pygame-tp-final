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
def settings(volume_music, volume_game):
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
                    main_menu(volume_music, volume_game)

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

    paused = True
    while paused:
        mouse_position = pg.mouse.get_pos()
        
        screen.blit(background_image_pause, background_image_pause_rect)


        resume_button = Button(image=None, pos=(width_window / 2,225), text_input="RESUME", font=(pg.font.Font(None, 35)), base_color="black", hovering_color="White")
        return_to_main_menu_button = Button(image=None, pos=(width_window / 2,425), text_input="RETURN TO MAIN MENU", font=(pg.font.Font(None, 35)), base_color="black", hovering_color="White")

        for button in [resume_button, return_to_main_menu_button]:
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
                if return_to_main_menu_button.checkforinput(mouse_position):
                    click_sound.play()
                    main_menu(volume_music, volume_game)

        pg.display.flip()

def play_game(volume_music, volume_game, level, score):
    json_file = read_json_file("json.json")

    #Image
    background_image = pg.image.load(r"img\background\allmountain.png")
    #Para establecer el tamaño en la pantalla, se pasa como parametro la imagen cargada y el ancho y alto
    background_image = pg.transform.scale(background_image, (width_window, height_window))

    if level == 1:
        json_level = json_file["level_one"]
        #main player
        dict_main_player = json_level["main_player"]
        main_player = Player(x=dict_main_player["x"], y=dict_main_player["y"], speed_walk=dict_main_player["speed_walk"], 
                            speed_run=dict_main_player["speed_run"], gravity=dict_main_player["gravity"], 
                            power_jump=dict_main_player["power_jump"], jump_height=dict_main_player["jump_height"], 
                            width_player=dict_main_player["width_player"], height_player=dict_main_player["height_player"], 
                            volume_game=volume_game, volume_music=volume_music, life_bar_path=r"img\life bar\0.png")

        #Platforms
        dict_platforms = json_level["platforms"]
        platform_one = dict_platforms["platform_one"]
        platform_two = dict_platforms["platform_two"]
        platform_three = dict_platforms["platform_three"]
        platform_four = dict_platforms["platform_four"]
        platforms_list = [(Platform(x=platform_one["x"], y=platform_one["y"], 
                        width=dict_platforms["common_width"], height=dict_platforms["common_height"])),

                        (Platform(x=platform_two["x"], y=platform_two["y"], 
                        width=dict_platforms["common_width"], height=dict_platforms["common_height"])),

                        (Platform(x=platform_three["x"], y=platform_three["y"], 
                        width=dict_platforms["common_width"], height=dict_platforms["common_height"])),

                        (Platform(x=platform_four["x"], y=platform_four["y"], 
                        width=dict_platforms["common_width"], height=dict_platforms["common_height"]))]

        #Coin
        coin_one = json_level["coins"]["coin_one"]
        coin_two = json_level["coins"]["coin_two"]
        coin_three = json_level["coins"]["coin_three"]
        coin_four = json_level["coins"]["coin_four"]
        coin_five = json_level["coins"]["coin_five"]
        coin_list = [(Coin(x=coin_one["x"], y=coin_one["y"])),
                    (Coin(x=coin_two["x"], y=coin_two["y"])),
                    (Coin(x=coin_three["x"], y=coin_three["y"])),
                    (Coin(x=coin_four["x"], y=coin_four["y"])),
                    (Coin(x=coin_five["x"], y=coin_five["y"]))]
        
        #Saw(trap)
        saw_one = json_level["saws"]["saw_one"]
        saw_two = json_level["saws"]["saw_two"]
        saw_trap_list = [Saw(x=saw_one["x"], y=saw_one["y"]), Saw(x=saw_two["x"], y=saw_two["y"])]

        #Enemy
        common_height_and_width = json_level["enemies"]["common_height_and_width"]
        common_speed_walk = json_level["enemies"]["common_speed_walk"]
        common_gravity = json_level["enemies"]["common_height_and_width"]
        enemy_one = json_level["enemies"]["enemy_one"]
        enemy_two = json_level["enemies"]["enemy_two"]
        enemies = pg.sprite.Group(
            (Enemy(x=enemy_one["x"], y=enemy_one["y"], speed_walk=common_speed_walk, gravity=common_gravity,
            width_player=common_height_and_width, height_player=common_height_and_width, 
            life_bar_path=r"img\life bar\0.png", volume_game=volume_game, 
            volume_music=volume_music)),

            (Enemy(x=enemy_two["x"], y=enemy_two["y"], speed_walk=common_speed_walk, gravity=common_gravity, 
            width_player=common_height_and_width, height_player=common_height_and_width, 
            life_bar_path=r"img\life bar\0.png", volume_game=volume_game, 
            volume_music=volume_music))
        )

    if level == 2:
        #ASIGNACIÓN DE CLASES
        #main player
        json_level = json_file["level_two"]
        dict_main_player = json_level["main_player"]
        main_player = Player(x=dict_main_player["x"], y=dict_main_player["y"], speed_walk=dict_main_player["speed_walk"], 
                            speed_run=dict_main_player["speed_run"], gravity=dict_main_player["gravity"], 
                            power_jump=dict_main_player["power_jump"], jump_height=dict_main_player["jump_height"], 
                            width_player=dict_main_player["common_width_and_height_player"], 
                            height_player=dict_main_player["common_width_and_height_player"], 
                            volume_game=volume_game, volume_music=volume_music, life_bar_path=r"img\life bar\0.png")

        #Platforms
        platforms_common_height = json_level["platforms"]["common_height"]
        platform_one = json_level["platforms"]["platform_one"]
        platform_two = json_level["platforms"]["platform_two"]
        platform_three = json_level["platforms"]["platform_three"]
        platform_four = json_level["platforms"]["platform_four"]
        platform_five = json_level["platforms"]["platform_five"]
        platform_six = json_level["platforms"]["platform_six"]
        platform_seven = json_level["platforms"]["platform_seven"]
        platforms_list = [(Platform(x=platform_one["x"], y=platform_one["y"], width=platform_one["width"], 
                        height=platforms_common_height)),

                        (Platform(x=platform_two["x"], y=platform_two["y"], width=platform_two["width"], 
                        height=platforms_common_height)),

                        (Platform(x=platform_three["x"], y=platform_three["y"], width=platform_three["width"], 
                        height=platforms_common_height)),

                        (Platform(x=platform_four["x"], y=platform_four["y"], width=platform_four["width"], 
                        height=platforms_common_height)),

                        (Platform(x=platform_five["x"], y=platform_five["y"], width=platform_five["width"],
                        height=platforms_common_height)),

                        (Platform(x=platform_six["x"], y=platform_six["y"], width=platform_six["width"], 
                        height=platforms_common_height)),

                        (Platform(x=platform_seven["x"], y=platform_seven["y"], width=platform_seven["width"], 
                        height=platforms_common_height))]

        #Coin
        coin_one = json_level["coins"]["coin_one"]
        coin_two = json_level["coins"]["coin_two"]
        coin_three = json_level["coins"]["coin_three"]
        coin_four = json_level["coins"]["coin_four"]
        coin_five = json_level["coins"]["coin_five"]
        coin_list = [(Coin(x=coin_one["x"], y=coin_one["y"])),
                    (Coin(x=coin_two["x"], y=coin_two["y"])),
                    (Coin(x=coin_three["x"], y=coin_three["y"])),
                    (Coin(x=coin_four["x"], y=coin_four["y"])),
                    (Coin(x=coin_five["x"], y=coin_five["y"]))]
        
        #Saw(trap)
        saw_one = json_level["saws"]["saw_one"]
        saw_two = json_level["saws"]["saw_two"]
        saw_three = json_level["saws"]["saw_three"]
        saw_four = json_level["saws"]["saw_four"]
        saw_five = json_level["saws"]["saw_five"]
        saw_six = json_level["saws"]["saw_six"]
        saw_seven = json_level["saws"]["saw_seven"]
        saw_eight = json_level["saws"]["saw_eight"]
        saw_nine = json_level["saws"]["saw_nine"]
        saw_trap_list = [Saw(x=saw_one["x"], y=saw_one["y"]),
                        Saw(x=saw_two["x"], y=saw_two["y"]),
                        Saw(x=saw_three["x"], y=saw_three["y"]),
                        Saw(x=saw_four["x"], y=saw_four["y"]),
                        Saw(x=saw_five["x"], y=saw_five["y"]),
                        Saw(x=saw_six["x"], y=saw_six["y"]),
                        Saw(x=saw_seven["x"], y=saw_seven["y"]),
                        Saw(x=saw_eight["x"], y=saw_eight["y"]),
                        Saw(x=saw_nine["x"], y=saw_nine["y"])
                        ]
        
        #Enemy
        common_height_and_width = json_level["enemies"]["common_height_and_width"]
        common_speed_walk = json_level["enemies"]["common_speed_walk"]
        common_gravity = json_level["enemies"]["common_gravity"]
        enemy_one = json_level["enemies"]["enemy_one"]
        enemy_two = json_level["enemies"]["enemy_two"]
        enemies = pg.sprite.Group(
            (Enemy(x=enemy_one["x"], y=enemy_one["y"], speed_walk=common_speed_walk, gravity=common_gravity,
            width_player=common_height_and_width, height_player=common_height_and_width, 
            life_bar_path=r"img\life bar\0.png", volume_game=volume_game, 
            volume_music=volume_music)),

            (Enemy(x=enemy_two["x"], y=enemy_two["y"], speed_walk=common_speed_walk, gravity=common_gravity, 
            width_player=common_height_and_width, height_player=common_height_and_width, 
            life_bar_path=r"img\life bar\0.png", volume_game=volume_game, 
            volume_music=volume_music))
        )

    if level == 3:
        #ASIGNACIÓN DE CLASES
        #main player
        json_level = json_file["level_three"]
        dict_main_player = json_level["main_player"]
        main_player = Player(x=dict_main_player["x"], y=dict_main_player["y"], speed_walk=dict_main_player["speed_walk"], 
                            speed_run=dict_main_player["speed_run"], gravity=dict_main_player["gravity"], 
                            power_jump=dict_main_player["power_jump"], jump_height=dict_main_player["jump_height"], 
                            width_player=dict_main_player["common_width_and_height_player"], 
                            height_player=dict_main_player["common_width_and_height_player"], volume_game=volume_game, 
                            volume_music=volume_music, life_bar_path=r"img\life bar\0.png")

        #Platforms
        common_height = json_level["platforms"]["common_height"]
        platform_one = json_level["platforms"]["platform_one"]
        platform_two = json_level["platforms"]["platform_two"]
        platform_three = json_level["platforms"]["platform_three"]
        platform_four = json_level["platforms"]["platform_four"]
        platform_five = json_level["platforms"]["platform_five"]
        platforms_list = [(Platform(x=platform_one["x"], y=platform_one["y"], width=platform_one["width"], height=common_height)),
                        (Platform(x=platform_two["x"], y=platform_two["y"], width=platform_two["width"], height=common_height)),
                        (Platform(x=platform_three["x"], y=platform_three["y"], width=platform_three["width"], height=common_height)),
                        (Platform(x=platform_four["x"], y=platform_four["y"], width=platform_four["width"], height=common_height)),
                        (Platform(x=platform_five["x"], y=platform_five["y"], width=platform_five["width"], height=common_height))
                        ]

        #Coin
        coin_one = json_level["coins"]["coin_one"]
        coin_two = json_level["coins"]["coin_two"]
        coin_three = json_level["coins"]["coin_three"]
        coin_four = json_level["coins"]["coin_four"]
        coin_five = json_level["coins"]["coin_five"]
        coin_six = json_level["coins"]["coin_six"]
        coin_seven = json_level["coins"]["coin_seven"]
        coin_eight = json_level["coins"]["coin_eight"]
        coin_nine = json_level["coins"]["coin_nine"]
        coin_ten = json_level["coins"]["coin_ten"]
        coin_list = [(Coin(x=coin_one["x"], y=coin_one["y"])),
                    (Coin(x=coin_two["x"], y=coin_two["y"])),
                    (Coin(x=coin_three["x"], y=coin_three["y"])),
                    (Coin(x=coin_four["x"], y=coin_four["y"])),
                    (Coin(x=coin_five["x"], y=coin_five["y"])),
                    (Coin(x=coin_six["x"], y=coin_six["y"])),
                    (Coin(x=coin_seven["x"], y=coin_seven["y"])),
                    (Coin(x=coin_eight["x"], y=coin_eight["y"])),
                    (Coin(x=coin_nine["x"], y=coin_nine["y"])),
                    (Coin(x=coin_ten["x"], y=coin_ten["y"]))
                    ]
        
        #Saw(trap)
        saw_one = json_level["saws"]["saw_one"]
        saw_two = json_level["saws"]["saw_two"]
        saw_three = json_level["saws"]["saw_three"]
        saw_four = json_level["saws"]["saw_four"]
        saw_five = json_level["saws"]["saw_five"]
        saw_six = json_level["saws"]["saw_six"]
        saw_seven = json_level["saws"]["saw_seven"]
        saw_eight = json_level["saws"]["saw_eight"]
        saw_trap_list = [Saw(x=saw_one["x"], y=saw_one["y"]),
                        Saw(x=saw_two["x"], y=saw_two["y"]),
                        Saw(x=saw_three["x"], y=saw_three["y"]),
                        Saw(x=saw_four["x"], y=saw_four["y"]),
                        Saw(x=saw_five["x"], y=saw_five["y"]),
                        Saw(x=saw_six["x"], y=saw_six["y"]),
                        Saw(x=saw_seven["x"], y=saw_seven["y"]),
                        Saw(x=saw_eight["x"], y=saw_eight["y"]),
                        ]
        
        #Enemy
        common_height_and_width = json_level["enemies"]["common_height_and_width"]
        common_speed_walk = json_level["enemies"]["common_speed_walk"]
        common_gravity = json_level["enemies"]["common_gravity"]
        enemy_one = json_level["enemies"]["enemy_one"]
        enemy_two = json_level["enemies"]["enemy_two"]
        enemies = pg.sprite.Group(
            (Enemy(x=enemy_one["x"], y=enemy_one["y"], speed_walk=common_speed_walk, gravity=common_gravity,
            width_player=common_height_and_width, height_player=common_height_and_width, 
            life_bar_path=r"img\life bar\0.png", volume_game=volume_game, 
            volume_music=volume_music)),

            (Enemy(x=enemy_two["x"], y=enemy_two["y"], speed_walk=common_speed_walk, gravity=common_gravity, 
            width_player=common_height_and_width, height_player=common_height_and_width, 
            life_bar_path=r"img\life bar\0.png", volume_game=volume_game, 
            volume_music=volume_music))
        )
    ###########################################################################################################

    #Sounds
    sound_jump = pg.mixer.Sound(r"sounds\cartoon-jump-6462.mp3")
    sound_shoot = pg.mixer.Sound(r"sounds\laser-gun-81720.mp3")
    sound_pause = pg.mixer.Sound(r"sounds\pause-89443.mp3")
    sound_music_game = pg.mixer.Sound(r"sounds\Eric Skiff - A Night Of Dizzy Spells  NO COPYRIGHT 8-bit Music  Background.mp3")
    sound_enemy_hurted = pg.mixer.Sound(r"sounds\uuhhh_iqsgYFh.mp3")
    sound_main_player_hurted = pg.mixer.Sound(r"sounds\pain_sound.mp3")

    start_time = pg.time.get_ticks()
    executing_game = True
    sound_music_game.play()
    pg.display.set_caption("Play Game")
    while executing_game:
        sound_music_game.set_volume(volume_music)
        sound_jump.set_volume(volume_game)
        sound_shoot.set_volume(volume_game)
        sound_pause.set_volume(volume_game)
        sound_main_player_hurted.set_volume(volume_game)
        sound_enemy_hurted.set_volume(volume_game)
        sound_enemy_hurted.set_volume(volume_game)
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
                    main_player.jump()
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

        delta_ms = clock.tick(FPS) #Cantidad de milisegundos

        #Detección para ganar juego
        if len(coin_list) == 0:
            sound_music_game.stop()
            main_player.sound_hurt.stop()
            main_player.get_coin_sound.stop()
            if level < 3:
                level_completed(volume_music, volume_game, (level + 1), ((score + 100) + score_player))
            else:
                winner(volume_music, volume_game, ((score + 100) + score_player))

        #Plataformas
        for platform in platforms_list:
            platform.draw(screen)

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
        score_player = main_player.points
        def show_score(score_player):
            score_text = font.render("Score: {}".format(score_player), True, font_color)
            screen.blit(score_text, (10, 10))
        show_score(score_player + score)

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

        #Enemy
        for enemy in enemies:
            enemy.update(main_player, platforms_list, volume_game)
            enemy.draw(screen)

        #Main Player
        main_player.update(platforms_list, coin_list, saw_trap_list, enemies) #Cada cuanto queremos que se vaya actualizando, si aumenta el delta, aumenta la velocidad
        main_player.draw(screen) #Para dibujar al personaje en el juego

        #Detección de nivel perdido
        if (main_player.hit_counter == 3) or (seconds == 61):
            sound_music_game.stop()
            main_player.sound_hurt.stop()
            main_player.get_coin_sound.stop()
            main_player_death(volume_music, volume_game, level, (score - score_player))

        #Detección de balas de jugador contra enemigo, por cada disparo le resta vida, si llega a 3, desaparece.
        for bullet in main_player.bullet_group:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.kill()
                    enemy.hit_counter += 1
                    sound_enemy_hurted.play()
                    if enemy.hit_counter < 3:
                        enemy.life_bar_path = r"img\life bar\{}.png".format(str(enemy.hit_counter))
                    else:
                        enemy.is_alive = False
                        enemies.remove(enemy)
                        sound_enemy_hurted.play()
                        main_player.points += 50

        #Detección de balas de enemigo contra jugador, por cada disparo le resta vida, si llega a 3, se termina el juego.
        for enemy in enemies:
            for bullet in enemy.bullet_group:
                if bullet.rect.colliderect(main_player.rect):
                    bullet.kill()
                    main_player.hit_counter += 1
                    sound_main_player_hurted.play()
                    if main_player.hit_counter < 3:
                        main_player.life_bar_path = r"img\life bar\{}.png".format(str(main_player.hit_counter))

        pg.display.flip() #Para que el jugador aparezca, sin esta función no aparece por pantalla
        screen.blit(background_image, background_image.get_rect())

def level_completed(volume_music, volume_game, level, score):
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
                    main_menu(volume_music, volume_game)
                if next_level_button.checkforinput(mouse_position):
                    click_sound.play()
                    play_game(volume_music, volume_game, level, score)
        pg.display.update()

def winner(volume_music, volume_game, score):
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

        score_text = (pg.font.Font(None, 30)).render(f"CONGRATULATIONS!! FINAL SCORE: {str(score)}", True, "#b68f40")
        score_rect = score_text.get_rect(center=(750, 140))


        return_to_main_menu_button = Button(image=None, pos=(830,210), text_input="RETURN TO MAIN MENU", font=(pg.font.Font(None, 30)), base_color="black", hovering_color="White")

        screen.blit(score_text, score_rect)
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
                    main_menu(volume_music, volume_game)
        pg.display.update()

def main_player_death(volume_music, volume_game, level, score):
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
                    main_menu(volume_music, volume_game)
                if try_again_button.checkforinput(mouse_position):
                    click_sound.play()
                    play_game(volume_music, volume_game, level, score)
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
                    play_game(volume_music, volume_game, 1, 0)
                elif level_two__button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    play_game(volume_music, volume_game, 2, 0)
                elif level_three_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    play_game(volume_music, volume_game, 3, 0)
                elif return_to_main_menu_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    main_menu(volume_music, volume_game)

        pg.display.update()

def main_menu(volume_music, volume_game):
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
                    play_game(volume_music, volume_game, 1, 0)
                elif quit_button.checkforinput(mouse_position):
                    click_sound.play()
                    pg.quit()
                    sys.exit()
                elif options_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    settings(volume_music, volume_game)
                elif select_level_button.checkforinput(mouse_position):
                    click_sound.play()
                    background_music.stop()
                    select_level_window(volume_music, volume_game)
        pg.display.update()

main_menu(0.05, 0.2)