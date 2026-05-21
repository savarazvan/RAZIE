from pathlib import Path

import pygame
import os

class AssetLoader:
    def __init__(self, base_path: Path=Path("assets")):
        self.base_path = base_path
        self.images = {}
        self.textures = {}
        self.sounds = {}
        self.fonts = {}
        self.create_default_surface(100, 100)

    def load_image(self, name, filename):
        path = os.path.join(self.base_path, "images", filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            self.images[name] = image
        except pygame.error as e:
            print(f"Unable to load image at {path}: {e}")
            return None
        
    def load_texture(self, name, filename):
        path = os.path.join(self.base_path, "textures", filename)
        try:
            texture = pygame.image.load(path).convert_alpha()
            self.textures[name] = texture
        except pygame.error as e:
            print(f"Unable to load texture at {path}: {e}")
            return None


    def load_sound(self, name, filename):
        path = os.path.join(self.base_path, "sounds", filename)
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"Unable to load sound at {path}: {e}")
            return None

    def load_font(self, name, filename, size=24):
        path = os.path.join(self.base_path, "fonts", filename)
        try:
            font = pygame.font.Font(path, size)
            self.fonts[name] = font
        except pygame.error as e:
            print(f"Unable to load font at {path}: {e}")
            return None

    def get_image(self, name):
        return self.images.get(name)

    def get_texture(self, name) -> pygame.Surface:
        if not name in self.textures:
            return self.textures['default']
        return self.textures.get(name)

    def get_sound(self, name):
        return self.sounds.get(name)

    def get_font(self, name):
        return self.fonts.get(name)
    
    def clear_cache(self):
        self.images.clear()
        self.sounds.clear()
        self.textures.clear()
        self.fonts.clear()

    def create_default_surface(self, width, height, fill_color=(150, 150, 150), border_color=(100, 100, 100), border_width=2):
        surface = pygame.Surface((width, height))
        surface.fill(fill_color)
        if border_color and border_width > 0:
            pygame.draw.rect(surface, border_color, surface.get_rect(), border_width)
            font = pygame.font.SysFont(None, 24)
            text_surf = font.render("ERROR", True, (255, 0, 0))
            surface.blit(text_surf, (width // 2 - text_surf.get_width() // 2, height // 2 - text_surf.get_height() // 2))
        self.textures['default'] = surface
