import pygame

class HUDManager:
    def __init__(self):
        self.elements = []

    def add_text(self, text, position, font=None, color=(0, 0, 0)):
        if font is None:
            font = pygame.font.SysFont(None, 36)
        self.elements.append({
            'type': 'text',
            'content': text,
            'position': position,
            'font': font,
            'color': color
        })

    def add_image(self, image, position):
        self.elements.append({
            'type': 'image',
            'content': image,
            'position': position
        })

    def clear_elements(self):
        self.elements.clear()

    def draw(self, screen):
        for element in self.elements:
            if element['type'] == 'text':
                surface = element['font'].render(element['content'], True, element['color'])
                screen.blit(surface, element['position'])
            elif element['type'] == 'image':
                if element['content']:
                    screen.blit(element['content'], element['position'])
