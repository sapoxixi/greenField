import os
from pathlib import Path
import pygame

from .constants import settings as set

def get_path(folder, file):
    """Create a file's absolute path, based on  file"""

    home_dir = str(Path.home())
    main_dir = os.path.join(home_dir, set['folder_root'], set['folder_project'])
    
    return os.path.join(main_dir, folder, file)


def load_image(file, scale = None):
    """Loads an image and prepares it for play"""

    file_path = get_path(set['folder_images'], file)

    try:
        surface = pygame.image.load(file_path)
        
        if scale:
            surface = pygame.transform.scale(surface, scale)
    except pygame.error:
        raise SystemExit(f'Could not load image "{file}" {pygame.get_error()}')
    return surface.convert()

def create_rect(location, size):
    """Creates a rectangle"""
    return pygame.Rect(location, size)