import pygame as pg
import os
class Auxiliar:
    @staticmethod
    #Flip es para voltear al personaje, lease que mire para el otro lado 
    def get_surface_from_sprite_sheet(path, columns, rows, flip=False): #Función para obtener cada fotograma del sprite sheet
        lista = []
        surface_image = pg.image.load(path)
        fotograma_width = int(surface_image.get_width()/columns)
        fotograma_height = int(surface_image.get_height()/rows)
        for row in range(rows):
            for column in range(columns):
                x = column * fotograma_width
                y = row * fotograma_height
                surface_fotograma = surface_image.subsurface(x,y,fotograma_width,fotograma_height)
                if flip:
                    surface_fotograma = pg.transform.flip(surface_fotograma, True, False)
                lista.append(surface_fotograma)
        return lista
    
    def get_animation_list_from_folder(path, width, height, flip=False):
        animation_list = sorted([f for f in os.listdir(path)])
        animation_list = [pg.image.load(os.path.join(path, img)) for img in animation_list]
        animation_list = [pg.transform.scale(image, (width, height)) for image in animation_list]
        if flip:
            animation_list = [pg.transform.flip(image, True, False) for image in animation_list]
        return animation_list