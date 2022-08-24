from pygame_gui import UI_TEXT_ENTRY_FINISHED, UI_BUTTON_PRESSED
from pygame_gui.core import UIContainer
import asyncio

from .base_state import BaseState
from utils.text_box import TextBox
from utils.input_text_box import InputTextBox
from utils.button import Button
from utils.common import create_rect
from utils.constants import settings as set
from utils.database import Database

TITLE = 'Insert new species'
TEXT = '<br> Insert species name:<br> <br><br>Insert species quantity:'
LOCATION_CONTAINER = (0, 300)
LOCATION_INPUT_NAME = (45, 380)
LOCATION_INPUT_QUANTITY = (45, 430)
LOCATION_INSERT = (60, 460)
LOCATION_QUIT = (170, 460)
LOCATION_WARNINGS = (50, 600)
SIZE_WARNINGS = (200, 100)
LAYER = 2

class InsertState(BaseState):
    """Implements the state where the player is inserting a species"""

    def __init__(self, ui_manager):
        super(InsertState, self).__init__()
        self.state_name = 'INSERT'
        self.next_state = 'SITE'
        self.ui_manager = ui_manager

        self.container = UIContainer(create_rect(LOCATION_CONTAINER, set['size_site_textbox']), 
                                    self.ui_manager, 
                                    starting_height = LAYER)
     
        self.text_box = TextBox(set['location_site_text_box'], set['size_site_textbox'], TITLE, TEXT, self.ui_manager).box
        self.text_box.hide()
   
        self.button_insert = Button(LOCATION_INSERT, set['size_button_ins'], 'insert', self.ui_manager).button
        self.button_quit = Button(LOCATION_QUIT, set['size_button_clear'], 'quit', self.ui_manager).button

        self.species_name = None
        self.species_quantity = None

    def startup(self):       
        self.input_box_name = InputTextBox(LOCATION_INPUT_NAME, self.ui_manager).input_box
        self.container.add_element(self.input_box_name)
        self.input_box_quantity = InputTextBox(LOCATION_INPUT_QUANTITY, self.ui_manager).input_box
        self.container.add_element(self.input_box_quantity)
        self.input_box_quantity.disable()

        self.text_box.show()
      
        self.button_insert.show()
        self.button_insert.enable()
        self.button_quit.show()
        self.button_quit.enable()

        self.warning_box = None

    

    def get_event(self, event):
        if event.type == UI_TEXT_ENTRY_FINISHED:
            self.handle_input(event)
        if event.type == UI_BUTTON_PRESSED:
            if self.warning_box:
                self.warning_box.kill()
            self.handle_button(event)

    def handle_button(self, event):       
        if event.ui_element == self.button_quit:
            self.close()
        elif event.ui_element == self.button_insert:
            if not self.species_name or not self.species_quantity:
                self.warning_box = self.create_warnings_box('Please enter both inputs, pressing Enter after entered each one.')
            else:
                if self.check_quantity():
                    ins_dict = self.get_insert_dict()
                    self.insert(ins_dict, ['name', 'site'])
                    self.close()
                else:
                    self.warning_box = self.create_warnings_box('Please enter an integer in the quantity input, pressing Enter after.')
                    self.input_box_quantity.enable()

   
    def handle_input(self, event):
        if event.ui_element == self.input_box_name:
            self.species_name = event.text
            self.input_box_name.disable()
            self.input_box_quantity.enable()
        if event.ui_element == self.input_box_quantity:
            self.species_quantity = event.text
            self.input_box_quantity.disable()

    def check_quantity(self):
        return self.species_quantity.isdigit()

    def get_insert_dict(self):
        return {'name': self.species_name, 'quantity': self.species_quantity, 'site': self.site}

    def insert(self, data, find_keys):
        result = asyncio.run(Database().insert_or_update(data, find_keys))
        if not result: 
            self.warning_box = self.create_warnings_box('An error occured or something went wrong when inserting.')

    def create_warnings_box(self, text):
        return TextBox(LOCATION_WARNINGS, 
                        SIZE_WARNINGS, 
                        'WARNINGS:',
                        text, 
                        self.ui_manager).box

    def close(self):
        self.done = True

        self.text_box.hide()
        if self.warning_box:
            self.warning_box.kill()

        self.button_insert.hide()
        self.button_insert.disable()
        self.button_quit.hide()       
        self.button_quit.disable()

        self.container.kill()
      