from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from pygame_gui.core import ObjectID

from .common import create_rect
from .constants import settings as set

class InputTextBox():
    """Implements an input text box"""
    def __init__(self, location, ui_manager):
        self.input_box = UITextEntryLine(create_rect(location, 
                                        set['size_input_box']), 
                                        ui_manager,
                                        object_id=ObjectID(class_id="input_box", object_id="#input"))