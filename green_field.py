import sys, traceback
import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from pygame_gui.ui_manager import UIManager
from pygame_gui.core import IncrementalThreadedResourceLoader

from utils.background import Background
from utils.constants import settings as set
from utils.common import get_path, create_rect
from player import Player
from states.wander_state import WanderState
from states.insert_state import InsertState
from states.site_state import SiteState
from states.show_state import ShowState

class GreenField():
    """Runs the 'game' """

    def __init__(self):
        self.loader = IncrementalThreadedResourceLoader()
        self.loader.start()
        self.ui_manager = self.create_ui_manager()
        self.window = pygame.display.set_mode([set['window_width'], set['window_height']])
        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(60)/1000.0
        self.background = Background(set['image_background'], set['scale_background'])
        self.player = Player(set['image_player'], set['scale_player'])
        
        self.sites = self.create_static_sites()
        # instanciates the states - State Machine (semi :) ) implementation
        self.states = self.get_states()

        self.state = self.states['WANDER']
        self.running = True
        
        pygame.display.set_caption(set['window_caption'])

    def create_ui_manager(self):
        """Creates ui manager, which will hold ui elements like text boxes"""

        theme_path = get_path(set['folder_themes'], set['theme'])
        ui_manager = UIManager((set['window_width'], set['window_height']), theme_path, resource_loader=self.loader)
        ui_manager.add_font_paths("Montserrat", get_path(set['folder_fonts'],"Montserrat-Regular.ttf"),get_path(set['folder_fonts'],"Montserrat-Bold.ttf"),
        get_path(set['folder_fonts'],"Montserrat-Italic.ttf"),
        get_path(set['folder_fonts'],"Montserrat-BoldItalic.ttf"))
        ui_manager.preload_fonts([{'name': 'Montserrat', 'html_size': 4.5, 'style': 'bold'},
                            {'name': 'Montserrat', 'html_size': 4.5, 'style': 'regular'},
                            {'name': 'Montserrat', 'html_size': 2, 'style': 'regular'},
                            {'name': 'Montserrat', 'html_size': 2, 'style': 'italic'},
                            {'name': 'Montserrat', 'html_size': 6, 'style': 'bold'},
                            {'name': 'Montserrat', 'html_size': 6, 'style': 'regular'},
                            {'name': 'Montserrat', 'html_size': 6, 'style': 'bold_italic'},
                            {'name': 'Montserrat', 'html_size': 4, 'style': 'bold'},
                            {'name': 'Montserrat', 'html_size': 4, 'style': 'regular'},
                            {'name': 'Montserrat', 'html_size': 4, 'style': 'italic'}
                            ])

        return ui_manager

    def create_static_sites(self):
        self.horta = create_rect(set['location_horta'], set['size_horta'])
        self.pomar = create_rect(set['location_pomar'], set['size_horta'])
        self.olival = create_rect(set['location_olival'], set['size_horta'])

        return {
                'HORTA': self.horta,
                'POMAR': self.pomar,
                'OLIVAL': self.olival
            }
    
    def get_states(self):
        return {
                "WANDER": WanderState(self.player,self.sites),
                "SITE": SiteState(self.ui_manager),
                'SHOW': ShowState(self.ui_manager),
                'INSERT': InsertState(self.ui_manager),
            }

    def run_loop(self):
        for event in pygame.event.get():      
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = False
            elif event.type == QUIT:
                self.running = False

            self.state.get_event(event)
            self.ui_manager.process_events(event)

    def update_state(self):
        if self.state.done:
            self.state.done = False

            previous_state = self.state

            self.state = self.states[previous_state.get_next_state()]

            previous_state_name = previous_state.get_name()
            self.state.put_previous_state(previous_state_name)
            
            #if self.state.state_name == 'SITE' and previous_state_name == 'WANDER':
            site = previous_state.get_site()              
            self.state.update_site(site)
            
            self.state.startup()

    def draw_sprites(self):
        self.ui_manager.update(self.time_delta)

        self.window.blit(self.background.image, self.background.rect)
        for site in self.sites:
            pygame.draw.rect(self.window, set['color_size'], self.sites[site], 0)
        self.window.blit(self.player.image, self.player.rect)

    def display_to_window(self):
        self.ui_manager.draw_ui(self.window)
        pygame.display.flip()
        self.clock.tick(set['fps'])
    
    def run_game(self):
        while self.running:
            self.run_loop()
            self.draw_sprites()
            self.update_state()
            self.display_to_window()

    def kill(self):
        self.loader._stop_threaded_loading()

if __name__ == '__main__':
    pygame.init()
    pygame.freetype.init()

    game = GreenField()
 
    try:
        game.run_game()
        game.kill()
    except Exception:
        print('Something went wrong: \n')
        # to be more generic, with the respect to the exception type
        traceback.print_exc() 
        game.kill()

    pygame.quit()

    # sys.exit()