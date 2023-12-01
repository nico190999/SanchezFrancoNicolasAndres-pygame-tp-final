import pygame as pg
from auxiliar import Auxiliar
from constantes import *

class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame = 0
        self.image = Auxiliar.get_surface_from_sprite_sheet(r"img\coin\quoin__x1_1_x1_2_x1_3_x1_4_x1_5_x1_6_x1_7_x1_8_png_1354829599.png", 24, 8)[72:96]
        self.animation = self.image
        self.image = self.animation[int(self.frame)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_coin = pg.Rect(self.rect.x, self.rect.y, self.rect.width, 50)

    def update(self, screen) -> None:
        if DEBUG:
            pg.draw.rect(screen, (255,0,0), self.rect_coin)
        if (self.frame < len(self.animation) - 1):
            self.frame += 0.2
        else:
            self.frame = 0
        
    
    def draw(self, screen):
        self.image = self.animation[int(self.frame)]
        screen.blit(self.image, self.rect)