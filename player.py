from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

from utils.constants import settings as set
from utils.figure import Figure

class Player(Figure):
    """Implements the player"""

    def __init__(self, image_file, scale):
        super(Player, self).__init__(image_file, scale, set['location_player'])
        self.image.set_colorkey((0, 0, 0), RLEACCEL)

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -set['speed'])
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, set['speed'])
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-set['speed'], 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(set['speed'], 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > set['window_width']:
            self.rect.right = set['window_width']
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= set['window_height']:
            self.rect.bottom = set['window_height']

    def move_to_right(self):
        self.rect.move_ip(50, 0)