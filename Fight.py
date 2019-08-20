import pygame
from pygame.locals import *
import os
from properties import *
from Bg_Sprite import *
import proper

class Fight_Window(object):
    ''' 战斗窗口 '''
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        self.screen = pygame.display.set_mode(BG_SIZE, RESIZABLE, 32)
        self.clock = pygame.time.Clock()
        # 判断是否退出循环
        self.is_exit = True
        # 判断切换图片
        self.flag = 2
        # 用于延迟
        self.delay = 100
        self.Sprite_Group()
        proper.blood = 50
        proper.power = 50
        proper.npc_blood = 50
        proper.npc_power = 50
        proper.is_q_alive = True

    def Sprite_Group(self):
        ''' 精灵组 '''
        # 背景精灵
        self.bg = Bg_Sprite("img/bg.png")
        self.bg_group = pygame.sprite.Group(self.bg)
        # 人物精灵
        self.role = Role_Sprite()
        self.role_group = pygame.sprite.Group(self.role)
        # 英雄精灵
        self.hero = Hero_Sprite()
        self.hero_group = pygame.sprite.Group(self.hero)
        # NPC精灵
        self.npc = NPC_Sprite()
        self.npc_group = pygame.sprite.Group(self.npc)

    def change_direction(self,dire,key, SPEED):
        ''' 监听方向 '''
        eval("self.hero.Move_"+dire+"("+str(SPEED)+")")
        self.hero.key = key  # 人物方向
        self.hero.flag = self.flag  # 人物切换图片

    def control_keyboard(self):
        ''' 监听事件 '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.is_exit = False
                # Q技能
                if event.key == K_q:
                    if proper.is_q_alive:
                        proper.key = self.hero.key
                        self.hero.Create_Skill_q(self.hero.rect)
                        # 影子的Q技能
                        if proper.skill_w:
                            self.hero.Create_Skill_shadow_q(proper.skill_w.rect)
                        proper.is_q_alive = False
                # W技能
                if event.key == K_w:
                    if proper.is_w_alive:
                        proper.key = self.hero.key
                        proper.skill_w = self.hero.Create_Skill_w()
                        proper.is_w_alive = False
                    elif proper.double_w and not proper.is_w_true:
                        # 判断英雄和影子位置交换
                        self.hero.rect.topleft, proper.skill_w.rect.topleft = proper.skill_w.rect.topleft, self.hero.rect.topleft
                        proper.double_w = False

            # 切换图片
            if event.type == pygame.KEYUP:
                # 松开按键时停下
                if self.role.key == "U":
                    self.role.flag = 3
                elif self.role.key == "D":
                    self.role.flag = 3
                elif self.role.key == "L":
                    self.role.flag = 3
                elif self.role.key == "R":
                    self.role.flag = 3
        if not (self.delay % 15):
            self.flag -= 1
        if self.flag == 0:
            self.flag = 2

        # 延迟
        self.delay -= 1
        if not self.delay:
            self.delay = 100

        # 控制按键
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.change_direction("Up", "U", -SPEED)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.change_direction("Down", "D", SPEED)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.change_direction("Left", "L", -SPEED)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.change_direction("Right", "R", SPEED)
        if pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_LEFT]:
            self.change_direction("Empty", "UL", SPEED)
        if pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.change_direction("Empty", "UR", SPEED)
        if pygame.key.get_pressed()[pygame.K_DOWN] and pygame.key.get_pressed()[pygame.K_LEFT]:
            self.change_direction("Empty", "DL", SPEED)
        if pygame.key.get_pressed()[pygame.K_DOWN] and pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.change_direction("Empty", "DR", SPEED)

    def random_npc(self):
        '''npc随机定时'''
        for i in range(60):
            if i % 10 == 0:
                proper.times += 1
        if proper.times >= 100:
            proper.n = random.randint(0, 7)
            proper.times = 0

    def Blood(self,name,blood,power,flag):
        # 英雄或NPC血蓝条空白槽
        pygame.draw.rect(self.screen,(0,255,0),pygame.Rect(name.rect.x - 10,name.rect.top - 15,50,5))
        pygame.draw.rect(self.screen,(0,255,0),pygame.Rect(name.rect.x - 10,name.rect.top - 10,50,5))
        if blood > 0:
            pygame.draw.rect(self.screen,(255,0,0),pygame.Rect(name.rect.x - 10,name.rect.top - 15,blood,5),0)
        if power > 0:
            pygame.draw.rect(self.screen,(0,0,255),pygame.Rect(name.rect.x - 10 ,name.rect.top - 10,power,5),0)
        else:
            if flag == "hero":
                proper.is_q_alive = False

    def collide_group(self, sp1, sp2,flag):
        ''' 英雄与技能碰撞，减去血量 '''
        self.contact = pygame.sprite.groupcollide(sp1, sp2, False, False)
        if flag == "hero":
            if self.contact and proper.hero_skill_and_role:
                proper.blood -= 20
                proper.hero_skill_and_role = False

        ''' NPC与技能碰撞，减去血量 '''
        if flag == "npc":
            for key,value in self.contact.items():
                for skill in value:
                    if self.contact and skill.npc_skill_and_role:
                        if skill.flag == "q": # Q技能
                            proper.npc_blood -= 10
                        elif skill.flag == "sq": # 影子的Q
                            proper.npc_blood -= 10
                        skill.npc_skill_and_role = False


    def Sprite_Group_Draw(self):
        ''' 显示精灵 '''
        self.bg_group.draw(self.screen)
        self.hero_group.update()
        self.hero.skill_group.update()
        self.hero_group.draw(self.screen)
        self.hero.skill_group.draw(self.screen)
        self.npc_group.update(self.delay,self.flag)
        self.npc_group.draw(self.screen)
        self.npc.skill_group.update()
        self.npc.skill_group.draw(self.screen)
        self.collide_group(self.hero_group,self.npc.skill_group,"hero") # 碰撞
        self.collide_group(self.npc_group,self.hero.skill_group,"npc") # 碰撞
        self.Blood(self.hero,proper.blood,proper.power,"hero")
        self.Blood(self.npc,proper.npc_blood,proper.npc_power,"npc")


    def exit(self):
        ''' 判断血量小于0结束战斗 '''
        if proper.blood <= 0 or proper.npc_blood <= 0:
            self.is_exit = False

    def main(self):
        while self.is_exit:
            self.clock.tick(60)
            # npc随机定时
            self.random_npc()
            # 事件监听
            self.control_keyboard()
            # 显示精灵
            self.Sprite_Group_Draw()
            # 战斗结束
            self.exit()
            pygame.display.update()