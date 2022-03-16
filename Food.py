import pygame, random


class Food:
    def __init__(self, pa):
        self.main_surf = pa.main_surf
        self.main_surf_width = pa.main_surf_width

        self.surf = pygame.image.load(f"image/food/food({random.randint(1, 8)}).png")
        self.width = self.surf.get_rect().width
        self.height = self.surf.get_rect().height
        self.x = random.randint(self.main_surf_width, 2 * self.main_surf_width - self.width)
        self.y = random.randint(300, 400)



    def blit_food(self):
        self.main_surf.blit(self.surf, (self.x, self.y))