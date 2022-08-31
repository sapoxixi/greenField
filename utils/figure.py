import pygame
from .common import load_image
from .constants import settings as set

class Figure(pygame.sprite.Sprite):
    """Implements a figure. It can be a background image or a sprite"""

    def __init__(self, image_file, scale, initial_loc):
        super(Figure, self).__init__()

        self.image = load_image(image_file, (set['window_width']/scale, set['window_height']/scale))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = initial_loc