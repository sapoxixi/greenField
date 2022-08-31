from pygame.locals import KEYDOWN, K_q
import asyncio

from .base_state import BaseState
from utils.text_box import TextBox
from utils.constants import settings as set
from utils.database import Database

TITLE = 'Show species (press q to exit)'

class ShowState(BaseState):
    """Implements the state where is shown to the player the list of species existent in a site"""
    
    def __init__(self, ui_manager):
        super(ShowState, self).__init__()
        self.state_name = 'SHOW'
        self.next_state = 'SITE'
        self.ui_manager = ui_manager
        
    def startup(self):
        data = self.get_data({'site': self.site})
        if data:
            text = self.build_html(data)
        else:
            text = 'Nothing to show :('

        self.text_box = TextBox(set['location_site_text_box'], set['size_site_textbox'], TITLE, text, self.ui_manager).box

    def get_data(self, find_dict):
        data = asyncio.run(Database().find_all_by_dict(find_dict))
        return data

    def build_html(self, list_name_quantity):
        string = ''
        for item in list_name_quantity:
            string += item['name'] + ', ' + str(item['quantity']) + '<br>'
            
        return string

    def get_event(self, event):       
        if event.type == KEYDOWN:
            self.handle_key(event)

    def handle_key(self, event):
        if event.key == K_q:
            self.close()

    def close(self):
        self.done = True
        self.text_box.kill()