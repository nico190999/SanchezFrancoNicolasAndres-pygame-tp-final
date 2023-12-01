import pygame as pg
from constantes import *

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, looking_right:bool):
        super().__init__()
        self.image = pg.image.load(r"img\bullet\player_laser.png")
        self.rect = self.image.get_rect(center=((pos_x + 80), (pos_y + 60)))
        self.looking_right = looking_right

    def update(self):
        #La velocidad con la que se mueve la bala
        if self.looking_right:
            self.rect.x += 5
        else:
            self.rect.x -= 5

        #Para que desaparezca la bala
        if self.rect.x >= (width_window + 50) or self.rect.x <= -50:
            self.kill()