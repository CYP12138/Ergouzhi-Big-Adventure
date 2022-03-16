import pygame
class Boss:
    def __init__(self, pa):
        self.qw = 0
        self.main_surf = pa.main_surf
        self.main_surf_width = pa.main_surf_width
        self.surf = pygame.image.load("image/boss/idle/idle(1).png")
        self.rect = self.surf.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

        self.x = 900
        self.y = 400  # 初始y
        self.speed = 4
        self.moving_r = False
        self.moving_l = False
        self.idle_number = 0
        self.run_number = 0
        self.attack_number = 5
        self.face = "left"
        self.boss_dead = False
        self.boss_bleed = 5

        self.boss_hurt_music = pygame.mixer.Sound("sound/boss_hurt.wav")


    def boss_run(self):
        if self.run_number < 8:
            self.run_number += 1
            self.surf = pygame.image.load(f"image/boss/run/run({self.run_number}).png")
            if self.face == "right":
                self.surf = pygame.transform.flip(self.surf, True, False)
            if self.run_number == 8:
                self.run_number = 1

            self.boss_x()

    def boss_idle(self):
        if self.idle_number < 8:
            self.idle_number += 1
            self.surf = pygame.image.load(f"image/boss/idle/idle({self.idle_number}).png")
            if self.face == "right":
                self.surf = pygame.transform.flip(self.surf, True, False)
            if self.idle_number == 8:
                self.idle_number = 1
                
    def boss_attack(self):
        if self.attack_number < 40:
            self.attack_number += 1
            self.surf = pygame.image.load(f"image/boss/attack/attack({self.attack_number // 5}).png")
            if self.face == "right":
                self.surf = pygame.transform.flip(self.surf, True, False)
            if self.attack_number == 40:
                self.attack_number = 5

    def boss_hurt(self):
        self.boss_hurt_music.play()
        self.surf = pygame.image.load(f"image/boss/hurt/hurt({1}).png")
        if self.face == "right":
            self.surf = pygame.transform.flip(self.surf, True, False)







    def boss_x(self):
        if self.moving_l:  # 左移位置
            if self.x > 0:
                self.x -= self.speed
        if self.moving_r:  # 右移位置
            if self.x < self.main_surf_width:  # 右移位置
                self.x += self.speed

    def blit_boss(self):
        self.main_surf.blit(self.surf, (self.x, self.y))