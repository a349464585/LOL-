import pygame
from pygame.locals import *
from sys import exit
from Bg_Sprite import *
from properties import *
from Map import *
import os
from Fight import Fight_Window

class Main(object):

    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        self.screen = pygame.display.set_mode(BG_SIZE, RESIZABLE, 32)
        self.clock = pygame.time.Clock()
        # 判断切换图片
        self.flag = 2
        # 用于延迟
        self.delay = 100
        # 创建精灵组
        self.Sprite_Group()

    def Sprite_Group(self):
        ''' 精灵组 '''
        # 背景精灵
        self.bg = Bg_Sprite(BG_IMG)
        self.bg_group = pygame.sprite.Group(self.bg)
        # 人物精灵
        self.role = Role_Sprite()
        self.role_group = pygame.sprite.Group(self.role)
        # 草地精灵组
        self.grass_group = Map_Bulid().grass()
        # 树精灵组
        self.tree_group = Map_Bulid().tree()
        # 房子精灵组
        self.house_group = Map_Bulid().house()
        # 玩家精灵组
        self.player_group = Map_Bulid().player()

    def collide_group(self, sp1, sp2):
        ''' 主角与物品组检测碰撞，如果碰撞就动不了'''
        self.contact = pygame.sprite.spritecollide(sp1, sp2, False)
        if self.contact:
            if self.role.key == "U":
                self.change_direction("Up", "U", -SPEED)
            elif self.role.key == "D":
                self.change_direction("Down", "D", SPEED)
            elif self.role.key == "L":
                self.change_direction("Left", "L", -SPEED)
            elif self.role.key == "R":
                self.change_direction("Right", "R", SPEED)

    def change_direction(self,dire,key, SPEED):
        ''' 监听方向 '''
        eval("self.bg.Move_"+dire+"("+str(SPEED)+")")
        for tree in self.tree_group:
            eval("tree.Move_"+dire+"("+str(SPEED)+")")
        for house in self.house_group:
            eval("house.Move_" + dire + "(" + str(SPEED) + ")")
        for player in self.player_group:
            eval("player.Move_" + dire + "(" + str(SPEED) + ")")
        for grass in self.grass_group:
            eval("grass.Move_" + dire + "(" + str(SPEED) + ")")
        self.role.key = key  # 人物方向
        self.role.flag = self.flag  # 人物切换图片

    def control_keyboard(self):
        ''' 监听事件 '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # 对话框
            if event.type == pygame.KEYDOWN:
                if event.key == K_a:
                    if not proper.is_stop:
                        if self.contact:
                            self.dialog_group = self.contact[0].dialogue()
                            proper.is_dia = True
                    else:
                        Fight_Window().main()
                        proper.is_dia = False
                        proper.is_stop = False
                        self.dialog_group.empty()

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
        if not (self.delay % 5):
            self.flag -= 1
        if self.flag == 0:
            self.flag = 2

        # 延迟
        self.delay -= 1
        if not self.delay:
            self.delay = 100

        # 控制按键
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.change_direction("Up", "U", SPEED)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.change_direction("Down", "D", -SPEED)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.change_direction("Left", "L", SPEED)
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.change_direction("Right", "R", -SPEED)

    def Sprite_Group_Draw(self):
        ''' 显示精灵 '''
        self.collide_group(self.role, self.tree_group)
        self.collide_group(self.role, self.house_group)
        self.collide_group(self.role, self.player_group)
        self.role_group.update()
        self.bg_group.draw(self.screen)
        self.grass_group.draw(self.screen)
        self.tree_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.house_group.draw(self.screen)
        self.role_group.draw(self.screen)
        if proper.is_dia:
            self.dialog_group.draw(self.screen)
            proper.is_stop = True

    def main(self):
        ''' 主函数 '''
        while True:
            self.clock.tick(60)
            # 事件监听
            self.control_keyboard()
            # 显示精灵
            self.Sprite_Group_Draw()
            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.main()