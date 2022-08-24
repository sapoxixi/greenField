import pygame
from .base_state import BaseState

class WanderState(BaseState):
    """Implements the state where the player is wandering"""

    def __init__(self, player, sites):
        super(WanderState, self).__init__()
        self.state_name = 'WANDER'
        self.next_state = "SITE"
        self.player = player
        self.sites = sites
        

    def get_event(self, event):
        # make the player get out of site to wander
        if self.previous_state == 'SITE':       
            self.player.move_to_right()
            self.previous_state = 'WANDER'

        pressed_keys = pygame.key.get_pressed()
        self.player.update(pressed_keys)

        self.check_collisions()

    def check_collisions(self):
        for state, site_at in self.sites.items():
            if site_at.colliderect(self.player):
                self.done = True
                self.site = state
                break

