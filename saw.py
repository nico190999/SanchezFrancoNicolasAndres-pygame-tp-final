import pygame as pg
from auxiliar import Auxiliar
from constantes import *


class Saw(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.frame = 0
        self.image = Auxiliar.get_surface_from_sprite_sheet_for_saw(r"img\saw\img\sprite_sheet___saw_design_by_abs_olute_dcos8s4-pre.png", 5, 1)
        self.animation = self.image
        self.image = self.animation[int(self.frame)]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.rect_for_collision = pg.Rect(self.rect.x, self.rect.y, self.rect.width, 50)

    def update(self, screen) -> None:
        if DEBUG:
            pg.draw.rect(screen, (255,200,0), self.rect_for_collision)
        if (self.frame < len(self.animation) - 1):
            self.frame += 0.2
        else:
            self.frame = 0
        
    
    def draw(self, screen):
        self.image = self.animation[int(self.frame)]
        screen.blit(self.image, self.rect)