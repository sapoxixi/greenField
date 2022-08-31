from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.core import ObjectID

from .common import create_rect

class TextBox():
    """Implements a text box"""

    def __init__(self, location, size, title, text, ui_manager):
        self.box = UITextBox('<font face=Montserrat size=2 color=#000000><b>' + title + '</b>'
                             '<br><br>'
                             '<body>' + text + '</body>',
                             create_rect(location, size),
                             manager=ui_manager,
                             object_id=ObjectID(class_id="white_text_box", object_id="#text_box_2"))
    
    def set_effect(self, effect):
        """Sets a text effect to the text box"""
        self.box.set_active_effect(effect)
