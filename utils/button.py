from pygame_gui.elements import UIButton
from pygame_gui.core import ObjectID

from .common import create_rect

class Button():
    """Implements a button"""
    def __init__(self, location, size, label, ui_manager):
        self.button = UIButton(create_rect(location, size), 
                                label, 
                                ui_manager, 
                                object_id=ObjectID(class_id="#everything_button",
                                                object_id="#button"),
                                starting_height = 2, visible = 0)