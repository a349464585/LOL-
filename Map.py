from Bg_Sprite import *

class Map_Bulid(object):
    def tree(self):
        # 创建树精灵组
        self.tree_list = []
        self.Build_Sprite = Build_Sprite(696, 768, TREE_IMG)
        self.tw = self.Build_Sprite.rect.width
        self.th = self.Build_Sprite.rect.height
        self.tree_list.append(self.Build_Sprite)
        for tree in range(0, 105):
            if tree == 0:
                self.tree_list.append(Build_Sprite(1050 + (self.tw * 10), 768 + (self.th), TREE_IMG))
                self.tree_list.append(Build_Sprite(1050 + (self.tw * 10), 725 - (self.th), TREE_IMG))
                self.tree_list.append(Build_Sprite(1371, 768 + (self.th), TREE_IMG))
            if tree < 9:
                self.tree_list.append(Build_Sprite(1784 + (self.tw * tree), 768, TREE_IMG))
                self.tree_list.append(Build_Sprite(1784 + (self.tw * tree), 725, TREE_IMG))
                self.tree_list.append(Build_Sprite(696 + (self.tw * tree), 725, TREE_IMG))
                if tree >= 1:
                    self.tree_list.append(Build_Sprite(696 + (self.tw * tree), 768, TREE_IMG))
                    self.tree_list.append(Build_Sprite(1371, 725 - (self.th * tree), TREE_IMG))
                if tree >= 2:
                    self.tree_list.append(Build_Sprite(1338, 725 - (self.th * tree), TREE_IMG))
            if tree < 11:
                self.tree_list.append(Build_Sprite(1050 + (self.tw * tree), 768, TREE_IMG))
                self.tree_list.append(Build_Sprite(1050 + (self.tw * tree), 725, TREE_IMG))
                self.tree_list.append(Build_Sprite(1371 + (self.tw * tree), 768, TREE_IMG))
                self.tree_list.append(Build_Sprite(1371 + (self.tw * tree), 725, TREE_IMG))
            if tree == 2 or tree == 6 or tree == 7 or tree == 8:
                self.tree_list.append(Build_Sprite(1338, 768 + (self.th * tree), TREE_IMG))
                self.tree_list.append(Build_Sprite(1371, 768 + (self.th * tree), TREE_IMG))

        self.Build_Sprite_group = pygame.sprite.Group()
        for tree in self.tree_list:
            self.Build_Sprite_group.add(tree)
        return self.Build_Sprite_group

    def house(self):
        # 创建小房子精灵组
        self.xhouse = Build_Sprite(1180, 799, S_HOUSE_IMG)
        self.xhouse2 = Build_Sprite(1180, 1000, S_HOUSE_IMG)
        self.house = Build_Sprite(1835, 799, HOUSE_IMG)
        # 创建大房子精灵组
        self.bhouse = Build_Sprite(697, 942, B_HOUSE_IMG)
        self.house_group = pygame.sprite.Group(self.xhouse, self.xhouse2, self.bhouse, self.house)
        return self.house_group

    def player(self):
        # 创建玩家
        self.player = Player(991, 879, MINGREN_PLAYER,"mingren")
        self.player2 = Player(1652, 942, WOAILUO_PLAYER,"woailuo")
        self.player_group = pygame.sprite.Group(self.player, self.player2)
        return self.player_group
    
    def grass(self):
        # 创建草精灵组
        self.grass_list = []
        self.grass = Grass_Sprite(703, 835, GRASS_IMG)
        self.gw = self.grass.rect.width
        self.gh = self.grass.rect.height
        self.grass_list.append(self.grass)
        for grass in range(0, 15):
            if grass < 4:
                self.grass_list.append(Grass_Sprite(703 + self.gw * (grass + 1), 835, GRASS_IMG))
            if grass < 5:
                self.grass_list.append(Grass_Sprite(703 + (self.gw * grass), 835 + (self.gh), GRASS_IMG))
                self.grass_list.append(Grass_Sprite(703 + (self.gw * grass), 835 + (self.gh * 2), GRASS_IMG))
        self.grass_group = pygame.sprite.Group()
        for grass in self.grass_list:
            self.grass_group.add(grass)
        return self.grass_group