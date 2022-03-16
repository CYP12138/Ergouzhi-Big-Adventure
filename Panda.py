import pygame
from Food import Food

class Panda:
    def __init__(self, pa):

        self.main_surf = pa.main_surf
        self.main_surf_width = pa.main_surf_width


        self.surf = pygame.image.load("image/panda/stand/stand(1).png")
        self.eat_music = pygame.mixer.Sound("sound/eat.wav")
        self.jump_music = pygame.mixer.Sound("sound/jump.wav")
        self.slide_music = pygame.mixer.Sound("sound/slide.wav")
        self.dead_music = pygame.mixer.Sound("sound/dead.wav")

        self.rect = self.surf.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.x = self.rect.x#初始x=0
        self.y = self.rect.y
        self.y = 530#初始y
        self.speed = 15
        self.moving_r = False
        self.moving_l = False
        self.stand_number = 0
        self.run_number = 0
        self.face = "right"

        self.jump = False
        self.slide = False

        self.score = 0
        
        
    def panda_run(self):
        if self.run_number < 10:
            self.run_number += 1
            self.surf = pygame.image.load(f"image/panda/run/run({self.run_number}).png")
            if self.face == "left":
                self.surf = pygame.transform.flip(self.surf, True, False)
            if self.run_number == 10:
                self.run_number = 1

            self.panda_x()

    def panda_stand(self):
        if self.stand_number < 10:
            self.stand_number += 1
            self.surf = pygame.image.load(f"image/panda/stand/stand({self.stand_number}).png")
            if self.face == "left":
                self.surf = pygame.transform.flip(self.surf, True, False)

            if self.stand_number == 10:
                self.stand_number = 1

    def panda_jump(self, pa):
        self.jump_music.play()

        for i in range(1, 21):#更改跑步图片
            if i < 11:#上升
                self.surf = pygame.image.load(f"image/panda/jump/jump({i}).png")
                self.y -= 20
            elif i < 21:#下降
                self.surf = pygame.image.load(f"image/panda/fall/fall({i-10}).png")
                self.y += 20
            if self.face == "left":
                self.surf = pygame.transform.flip(self.surf, True, False)
            self.panda_x()#更改水平位置
            pa.update_bg()
            pa.update_food()
            pa.update_barrier()
            pa.panda_barrier_collision()

            #吃食物
            self.eat_food(pa)
            if self.score == 5:
                self.speed = 20
            if self.score == 10:
                pa.boss_come()

            pa.blit_bg()  #画bg
            pa.food.blit_food()  #画食物
            pa.barrier.blit_barrier()
            pa.panda.blit_panda()  #画熊猫
            pa.blit_score()

            pygame.display.update()
            pygame.time.Clock().tick(60)
        self.jump = False

    def panda_slide(self, pa):
        self.slide_music.play()
        self.speed *= 3 / 2  # 滑动加速
        for i in range(1, 11):
            self.surf = pygame.image.load(f"image/panda/slide/slide({i}).png")
            if self.face == "left":
                self.surf = pygame.transform.flip(self.surf, True, False)
            self.panda_x()#更改水平位置
            pa.update_bg()
            pa.update_food()
            pa.update_barrier()
            pa.blit_bg()  # 画bg
            pa.food.blit_food()  # 画食物
            pa.barrier.blit_barrier()

            pa.panda_barrier_collision()

            pa.panda.blit_panda()  # 画熊猫
            pa.blit_score()
            pygame.display.update()
            pygame.time.Clock().tick(60)

        self.speed *= 2/3
        self.slide = False

    def panda_dead(self, pa):
        self.dead_music.play()
        for i in range(1, 11):
            self.surf = pygame.image.load(f"image/panda/dead/dead({i}).png")
            if self.face == "left":
                self.surf = pygame.transform.flip(self.surf, True, False)
            pa.blit_bg()  # 画bg
            pa.food.blit_food()  # 画食物
            pa.barrier.blit_barrier()
            pa.panda.blit_panda()  # 画熊猫
            pa.blit_score()
            pygame.display.update()
            pygame.time.Clock().tick(20)
        pa.again_ui()

    def panda_x(self):
        if self.moving_l:  # 左移位置
            if self.x > 0:
                self.x -= self.speed
        if self.moving_r:  # 右移位置
            if self.x < int(self.main_surf_width / 2 - self.rect.width):  # 右移位置
                self.x += self.speed

    def blit_panda(self):
        self.main_surf.blit(self.surf, (self.x, self.y))

    def eat_food(self, pa):
        if pygame.Rect(self.x, self.y, self.width, self.height).colliderect \
                    (pygame.Rect(pa.food.x + 10, pa.food.y + 10, pa.food.width - 10, pa.food.height - 10)):
            self.eat_music.play()
            del pa.food
            pa.food = Food(pa)
            self.score += 1