import random
import pygame

class BasicEnemy:
    def __init__(self, pos):
        basic_enemy1_1 = pygame.image.load('Graphics/basic_enemy1/basic_enemy1_1.png').convert_alpha()
        basic_enemy1_2 = pygame.image.load('Graphics/basic_enemy1/basic_enemy1_2.png').convert_alpha()
        self.basic_enemy1_list = [basic_enemy1_1, basic_enemy1_2]
        basic_enemy2_1 = pygame.image.load('Graphics/basic_enemy2/basic_enemy2_1.png').convert_alpha()
        basic_enemy2_2 = pygame.image.load('Graphics/basic_enemy2/basic_enemy2_2.png').convert_alpha()
        self.basic_enemy2_list = [basic_enemy2_1, basic_enemy2_2]
        self.enemy_list = [self.basic_enemy1_list,
                           self.basic_enemy2_list]
        self.index = 0

        self.surf_list = (random.choice(self.enemy_list))
        self.surf = self.surf_list[self.index]
        self.missile_surf = pygame.image.load('Graphics/enemy_missile.png').convert_alpha()
        self.rect = self.surf.get_rect(topleft=pos)
        self.health = 1
        self.time_since_fire = 0
        self.time_to_shoot = random.uniform(5, 20)
        self.score_gain = 150

    def animation(self):
        self.index += 0.02
        if self.index >= len(self.enemy_list):
            self.index = 0
        self.surf = self.surf_list[int(self.index)]
        self.rect = self.surf.get_rect(center=self.rect.center)

    def missile_reload(self, current_time):
        self.time_since_fire = current_time
        self.time_to_shoot = random.uniform(5, 7)

    def create_missile(self, current_time):
        if current_time - self.time_since_fire >= self.time_to_shoot * 1000:
            self.missile_reload(current_time)
            return self.missile_surf.get_rect(center=self.rect.midbottom)
