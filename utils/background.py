# import pygame
# from common import load_image
from .figure import Figure

INITIAL_LOCATION = [0, 0]

class Background(Figure):
    """Implements the background"""

    def __init__(self, image_file, scale):
        super(Background, self).__init__(image_file, scale, INITIAL_LOCATION)
