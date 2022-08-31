from pygame_gui import UI_BUTTON_PRESSED, TEXT_EFFECT_TYPING_APPEAR
from pygame.locals import KEYDOWN, K_q
import asyncio

from states.base_state import BaseState
from utils.text_box import TextBox
from utils.button import Button
from utils.constants import settings as set 
from utils.database import Database

TEXT = "Please click on an action or press q to quit"

SITES = {
    'HORTA': "Welcome to H0rt4!",
    'POMAR': 'Welcome to P0m4r!',
    'OLIVAL': 'Welcome to 0liv4l!'
}

class SiteState(BaseState):
    """Implements the state where the player is on a site"""

    def __init__(self, ui_manager):
        super(SiteState, self).__init__()
        self.state_name = 'SITE'
        self.ui_manager = ui_manager
        # buttons
        self.button_insert = Button(set['location_button_ins'], set['size_button_ins'], 'insert', self.ui_manager).button
        self.button_clear = Button(set['location_button_clear'], set['size_button_clear'], 'clear', self.ui_manager).button
        self.button_show = Button(set['location_button_show'], set['size_button_show'], 'show', self.ui_manager).button

    def startup(self):
        self.horta_text_box = TextBox(set['location_site_text_box'], set['size_site_textbox'], SITES[self.site], TEXT, self.ui_manager)
        self.horta_text_box.set_effect(TEXT_EFFECT_TYPING_APPEAR)
        # enable buttons
        self.button_insert.show()
        self.button_insert.enable()
        self.button_show.show()
        self.button_show.enable()
        self.button_clear.show()
        self.button_clear.enable()

    def get_event(self, event):       
        if event.type == KEYDOWN:
            self.handle_key(event)
        if event.type == UI_BUTTON_PRESSED:
            self.handle_button(event)
    
    def handle_button(self, event):
        if event.ui_element == self.button_insert:
            self.next_state = 'INSERT'
            self.close()
        elif event.ui_element == self.button_show:
            self.next_state = 'SHOW'
            self.close()
        elif event.ui_element == self.button_clear:
            self.clear()

    def handle_key(self, event):
        if event.key == K_q:
            self.next_state = 'WANDER'
            self.close()

    def clear(self):
        asyncio.run(Database().clear_by_dict({'site': self.site}))
    
    def close(self):
        self.done = True
        # disable box and buttons
        self.horta_text_box.box.hide()
        self.button_insert.disable()
        self.button_insert.hide()
        self.button_show.disable()
        self.button_show.hide()
        self.button_clear.disable()
        self.button_clear.hide()
  