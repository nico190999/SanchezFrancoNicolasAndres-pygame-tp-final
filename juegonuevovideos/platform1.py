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

    def draw(self, screen):
        if(DEBUG):
            pg.draw.rect(screen, (0,0,0), self.rect)
        screen.blit(self.image, self.rect)