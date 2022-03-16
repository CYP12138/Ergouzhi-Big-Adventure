import pygame, random

class Barrier:
    def __init__(self, pa):
        self.main_surf = pa.main_surf
        self.main_surf_width = pa.main_surf_width
        if pa.bg_number == 1:
            self.surf = pygame.image.load(f"image/barrier/barrier1({random.randint(1, 5)}).png")
        else:
            self.surf = pygame.image.load(f"image/barrier/barrier2({random.randint(1, 6)}).png")
        self.width = self.surf.get_rect().width
        self.height = self.surf.get_rect().height
        self.x = random.randint(self.main_surf_width, 2 * self.main_surf_width - self.width)
        self.y = 550

    def blit_barrier(self):
        self.main_surf.blit(self.surf, (self.x, self.y))