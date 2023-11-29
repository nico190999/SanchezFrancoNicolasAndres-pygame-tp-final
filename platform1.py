import pygame as pg
from constantes import *
from auxiliar import Auxiliar

class Platform:
    def __init__(self, x, y, width, height) -> None:
        self.image = pg.image.load(r"img\tiles\BGTile (1).png")
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_ground_collition = pg.Rect(self.rect.x, self.rect.y, self.rect.width, 10)
        self.rect_down_collition = pg.Rect(self.rect.x, self.rect.y + 30, self.rect.width, 10)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if(DEBUG):
            pg.draw.rect(screen, (0,0,255), self.rect_ground_collition)
            pg.draw.rect(screen, (0,255,0), self.rect_down_collition)
