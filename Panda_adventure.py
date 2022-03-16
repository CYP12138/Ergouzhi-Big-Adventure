import pygame, sys, random, time
from pygame.locals import *
from Panda import Panda
from Food import Food
from Barrier import Barrier
from Boss import Boss

class Panda_adventure():
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 1, 1024)
        self.main_surf_width = 1280
        self.main_surf_height = 720
        self.fps = 60
        self.font = pygame.font.Font("font/font.ttf", 30)

        self.main_surf = pygame.display.set_mode((self.main_surf_width, self.main_surf_height))
        pygame.display.set_caption("二狗子大冒险")

        self.bg_number = random.randint(1, 2)
        self.bg_surf = pygame.image.load(f"image/bg/bg{self.bg_number}.png")

        self.bgm = pygame.mixer.Sound("sound/bg.ogg")
        self.start_music = pygame.mixer.Sound("sound/start.wav")
        self.again_music = pygame.mixer.Sound("sound/again.wav")
        self.see_boss_music = pygame.mixer.Sound("sound/see_boss.wav")
        self.win_music = pygame.mixer.Sound("sound/win.wav")
        self.bg_boss_music = pygame.mixer.Sound("sound/bg_boss.ogg")

        self.start_ui()

        self.bg_x = 0
        self.panda = Panda(self)
        self.food = Food(self)
        self.barrier = Barrier(self)


        self.attack = False


    def run_game(self):
        while True:
            self.check_events()
            self.update_obj()
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN: #keydown
                if event.key == K_RIGHT:
                    self.panda.moving_r = True
                    self.panda.moving_l = False
                    self.panda.face = "right"
                if event.key == K_LEFT:
                    self.panda.moving_l = True
                    self.panda.moving_r = False
                    self.panda.face = "left"

                if event.key == K_SPACE:
                    self.panda.jump = True
                if event.key == K_LCTRL:
                    self.panda.slide = True

                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == KEYUP:#keyup
                if event.key == K_RIGHT:
                    self.panda.moving_r = False
                if event.key == K_LEFT:
                    self.panda.moving_l = False

    def update_obj(self):
        self.update_panda()
        self.panda_barrier_collision()
        self.update_food()
        self.update_barrier()
        self.update_bg()

    def update_panda(self):
        if self.panda.moving_l or self.panda.moving_r:  # 水平移动
            if self.panda.jump:  # 跳跃
                self.panda.panda_jump(self)
            elif self.panda.slide:  # 滑动
                self.panda.panda_slide(self)
            else:  # 跑动
                self.panda.panda_run()
        else:  # 水平不动
            if self.panda.jump:  # 跳跃
                self.panda.panda_jump(self)
            else:  # 站立
                self.panda.panda_stand()

    def update_food(self):
        if self.panda.moving_l or self.panda.moving_r:#更新食物
            if self.panda.x >= int(self.main_surf_width / 2 - self.panda.rect.width):
                self.food.x -= self.panda.speed
                if self.food.x + self.food.width <= 0:
                    del self.food
                    self.food = Food(self)
                    
    def update_barrier(self):
        if self.panda.moving_l or self.panda.moving_r:#更新障碍
            if self.panda.x >= int(self.main_surf_width / 2 - self.panda.rect.width):
                self.barrier.x -= self.panda.speed
                if self.barrier.x + self.barrier.width <= 0:
                    del self.barrier
                    self.barrier = Barrier(self)

    def update_bg(self):
        if self.panda.moving_l or self.panda.moving_r:#更新背景
            if self.panda.x >= int(self.main_surf_width / 2 - self.panda.rect.width):
                self.bg_x -= self.panda.speed
                if self.bg_x <= -int(2560 - self.main_surf_width):
                    self.bg_x = 0

    def update_screen(self):
        self.blit_bg()#画bg
        self.food.blit_food()#画食物
        self.barrier.blit_barrier()
        self.panda.blit_panda()#画熊猫
        self.blit_score()

        pygame.display.update()
        pygame.time.Clock().tick(self.fps)

    def blit_bg(self):
        self.main_surf.blit(self.bg_surf, (self.bg_x, 0))

    def blit_score(self):
        score_surf = self.font.render(f"boss还有{10 - self.panda.score}分到达战场", True, (255, 255, 255))
        self.main_surf.blit(score_surf, (50, 50))

    def panda_barrier_collision(self):
        if pygame.Rect(self.panda.x + 30, self.panda.y, self.panda.width - 60, self.panda.height - 50).colliderect \
                    (pygame.Rect(self.barrier.x + 45, self.barrier.y + 60, self.barrier.width - 75, self.barrier.height)):
            self.panda.panda_dead(pa)

    def start_ui(self):
        self.bg_x = 0
        start_y = - 700
        start_surf = pygame.image.load("image/start.png")
        self.start_music.play(-1)
        first_enter = False
        while True:
            self.bg_x -= 10
            if start_y < 0:
                start_y += 50
            if self.bg_x <= -int(2560 - self.main_surf_width):
                self.bg_x = 0
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        first_enter = True
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if first_enter:
                self.start_music.stop()
                self.bgm.play(-1)
                key_surf = pygame.image.load(f"image/key.png")
                self.main_surf.blit(key_surf, (0, 0))
                pygame.display.update()
                time.sleep(2)
                break
            self.main_surf.blit(self.bg_surf, (self.bg_x, 0))
            self.main_surf.blit(start_surf, (235, start_y))
            pygame.display.update()
            pygame.time.Clock().tick(self.fps)
            
    def again_ui(self):
        self.bgm.stop()
        self.again_music.play(-1)
        again_enter = False
        again_surf = pygame.image.load(f"image/over.png")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        again_enter = True
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if again_enter:
                self.again_music.stop()
                break
            self.main_surf.blit(self.bg_surf, (self.bg_x, 0))
            self.main_surf.blit(again_surf, (235, 0))
            pygame.display.update()
            pygame.time.Clock().tick(self.fps)
        del self.panda,self.food, self.barrier
        self.bg_number = random.randint(1, 2)
        self.bg_surf = pygame.image.load(f"image/bg/bg{self.bg_number}.png")
        self.bgm.play(-1)
        self.bg_x = 0
        self.panda = Panda(self)
        self.food = Food(self)
        self.barrier = Barrier(self)
        time.sleep(1)

    def again_play(self):
        self.bgm.stop()
        self.again_music.play(-1)
        again_enter = False
        again_surf = pygame.image.load(f"image/over.png")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        again_enter = True
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if again_enter:
                self.again_music.stop()
                break
            self.main_surf.blit(self.bg_surf, (self.bg_x, 0))
            self.main_surf.blit(again_surf, (235, 0))
            pygame.display.update()
            pygame.time.Clock().tick(self.fps)
        del self.panda
        self.bg_number = random.randint(1, 2)
        self.bg_surf = pygame.image.load(f"image/bg/bg{self.bg_number}.png")
        self.bgm.play(-1)
        self.bg_x = 0
        self.panda = Panda(self)
        self.food = Food(self)
        self.barrier = Barrier(self)
        self.attack = False
        time.sleep(1)
        self.run_game()

    def boss_come(self):
        self.bgm.stop()
        self.see_boss_music.play()
        self.bg_boss_music.play(-1)
        del self.panda, self.barrier, self.food
        self.boss = Boss(self)
        self.panda = Panda(self)

        while True:
            self.check_events()
            self.boss_update_panda()
            self.update_boss()

            self.bg_x = 0
            self.blit_bg()

            self.boss.blit_boss()
            self.panda.blit_panda()
            self.boss_bleed_surf = self.font.render(f"boss血量: {self.boss.boss_bleed}", True, (255, 255, 255))
            self.main_surf.blit(self.boss_bleed_surf, (50, 50))
            pygame.display.update()
            pygame.time.Clock().tick(60)
            if self.boss.boss_dead == True:
                break
            if pygame.Rect(self.panda.x + 80, self.panda.y, self.panda.width - 140, self.panda.height - 100).colliderect \
                    (pygame.Rect(self.boss.x + 150, self.boss.y + 50, self.boss.width - 330, self.boss.height - 100)):
                if not self.attack:
                    self.bg_boss_music.stop()
                    self.panda_killed()
            self.attack = False


        self.bg_boss_music.stop()
        self.win_music.play()



        del self.panda, self.boss
        self.bg_x = 0
        start_y = - 700
        self.start_music.play(-1)
        first_enter = False
        while True:
            self.bg_x -= 10
            if start_y < 0:
                start_y += 50
            if self.bg_x <= -int(2560 - self.main_surf_width):
                self.bg_x = 0
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        first_enter = True
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if first_enter:
                self.start_music.stop()
                self.bgm.play(-1)
                key_surf = pygame.image.load(f"image/key.png")
                self.main_surf.blit(key_surf, (0, 0))
                pygame.display.update()
                time.sleep(2)
                break
            self.main_surf.blit(self.bg_surf, (self.bg_x, 0))
            self.again_surf = pygame.image.load("image/again.png")
            self.main_surf.blit(self.again_surf, (235, start_y))
            font_big = pygame.font.Font("font/font.ttf", 90)
            win_surf = font_big.render("You Win!!!", True, (255, 0, 0))
            self.main_surf.blit(win_surf, (406, start_y + 260))
            pygame.display.update()
            pygame.time.Clock().tick(self.fps)


        self.bg_number = random.randint(1, 2)
        self.bg_surf = pygame.image.load(f"image/bg/bg{self.bg_number}.png")
        self.bg_x = 0
        self.panda = Panda(self)
        self.food = Food(self)
        self.barrier = Barrier(self)
        self.attack = False
        time.sleep(1)
        self.run_game()

    def boss_update_panda(self):
        if self.panda.moving_l or self.panda.moving_r:  # 水平移动
            if self.panda.jump:  # 跳跃
                self.boss_panda_jump()
            elif self.panda.slide:  # 滑动
                self.boss_panda_slide()
                self.attack = True
            else:  # 跑动
                self.boss_panda_run()
        else:  # 水平不动
            if self.panda.jump:  # 跳跃
                self.boss_panda_jump()
            else:  # 站立
                self.panda.panda_stand()

    def update_boss(self):
        if self.panda.x + self.panda.width / 2 < self.boss.x + self.boss.width / 2:
            self.boss.face = "left"
        else:
            self.boss.face = "right"
        if self.panda.x + 50 < self.boss.x:
            self.boss.moving_l = True
            self.boss.moving_r = False
        elif self.panda.x + self.panda.width - 50 > self.boss.x + self.boss.width:
            self.boss.moving_l = False
            self.boss.moving_r = True
        else:
            self.boss.moving_l = False
            self.boss.moving_r = False
            self.boss.boss_attack()
        if self.boss.moving_r or self.boss.moving_l:
            self.boss.boss_run()

    def boss_panda_jump(self):
        self.panda.jump_music.play()
        for i in range(1, 21):  # 更改跑步图片
            if i < 11:  # 上升
                self.panda.surf = pygame.image.load(f"image/panda/jump/jump({i}).png")
                self.panda.y -= 20
            elif i < 21:  # 下降
                self.panda.surf = pygame.image.load(f"image/panda/fall/fall({i - 10}).png")
                self.panda.y += 20
            if self.panda.face == "left":
                self.panda.surf = pygame.transform.flip(self.panda.surf, True, False)

            if self.panda.moving_l:  # 左移位置
                if self.panda.x > 0:
                    self.panda.x -= self.panda.speed
            if self.panda.moving_r:  # 右移位置
                if self.panda.x < self.panda.main_surf_width:  # 右移位置
                    self.panda.x += self.panda.speed

            self.update_boss()

            self.bg_x = 0
            self.blit_bg()

            self.boss.blit_boss()
            self.panda.blit_panda()
            self.main_surf.blit(self.boss_bleed_surf, (50, 50))


            pygame.display.update()
            pygame.time.Clock().tick(60)
        self.panda.jump = False

    def boss_panda_slide(self):
        self.panda.slide_music.play()
        self.panda.speed *= 3 / 2  # 滑动加速
        for i in range(1, 11):
            self.panda.surf = pygame.image.load(f"image/panda/slide/slide({i}).png")
            if self.panda.face == "left":
                self.panda.surf = pygame.transform.flip(self.panda.surf, True, False)

            if self.panda.moving_l:  # 左移位置
                if self.panda.x > 0:
                    self.panda.x -= self.panda.speed
            if self.panda.moving_r:  # 右移位置
                if self.panda.x < self.panda.main_surf_width:  # 右移位置
                    self.panda.x += self.panda.speed
            self.update_boss()
            if pygame.Rect(self.panda.x + 30, self.panda.y, self.panda.width - 60, self.panda.height).colliderect \
                        (pygame.Rect(self.boss.x - 40, self.boss.y, self.boss.width - 80, self.boss.height)):
                self.boss.boss_hurt()

            self.bg_x = 0
            self.blit_bg()

            self.boss.blit_boss()
            self.panda.blit_panda()
            self.main_surf.blit(self.boss_bleed_surf, (50, 50))
            pygame.display.update()
            pygame.time.Clock().tick(60)
        self.panda.speed *= 2 / 3
        self.panda.slide = False
        if pygame.Rect(self.panda.x + 30, self.panda.y, self.panda.width - 60, self.panda.height).colliderect \
                    (pygame.Rect(self.boss.x, self.boss.y, self.boss.width, self.boss.height)):
            self.boss.boss_bleed -= 1
            if self.boss.boss_bleed == 0:
                self.boss.boss_dead = True

    def boss_panda_run(self):
        if self.panda.run_number < 10:
            self.panda.run_number += 1
            self.panda.surf = pygame.image.load(f"image/panda/run/run({self.panda.run_number}).png")
            if self.panda.face == "left":
                self.panda.surf = pygame.transform.flip(self.panda.surf, True, False)
            if self.panda.run_number == 10:
                self.panda.run_number = 1
            if self.panda.moving_l:  # 左移位置
                if self.panda.x > 0:
                    self.panda.x -= self.panda.speed
            if self.panda.moving_r:  # 右移位置
                if self.panda.x < self.panda.main_surf_width:  # 右移位置
                    self.panda.x += self.panda.speed

    def panda_killed(self):
        self.panda.dead_music.play()
        for i in range(1, 11):
            self.panda.surf = pygame.image.load(f"image/panda/dead/dead({i}).png")
            if self.panda.face == "left":
                self.panda.surf = pygame.transform.flip(self.panda.surf, True, False)
            self.bg_x = 0
            self.blit_bg()

            self.boss.blit_boss()
            self.panda.blit_panda()  # 画熊猫
            pygame.display.update()
            pygame.time.Clock().tick(20)

        self.again_play()



if __name__ == "__main__":
    pa = Panda_adventure()
    pa.run_game()