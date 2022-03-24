import pygame.time
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.status = 'idle'
        self.animations = {'idle': [], 'move': [], 'attack': []}
        self.import_graphics(name)

        self.image = self.animations[self.status][self.anim_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        self.can_attack = True
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_cooldown = 1000

    def get_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return direction, distance

    def get_status(self, player):
        distance = self.get_direction(player)[1]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.anim_frame = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def import_graphics(self, name):
        base_path = f'graphics/monsters/{name}/'

        for animation in self.animations.keys():
            self.animations[animation] = load_folder(base_path + animation)

    def actions(self, player):
        if self.status == 'attack':
            self.last_attack_time = pygame.time.get_ticks()
            print('attack')
        elif self.status == 'move':
            self.direction = self.get_direction(player)[0]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.anim_frame += self.anim_speed
        if self.anim_frame >= len(animation):
            self.anim_frame = 0
            self.can_attack = False
        self.image = animation[int(self.anim_frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldowns(self):
        if not self.can_attack:
            if pygame.time.get_ticks() - self.last_attack_time >= self.attack_cooldown:
                self.can_attack = True

    def enemy_update(self, player):
        self.get_status(player)

        self.actions(player)

    def update(self):
        self.cooldowns()
        self.animate()
        self.move(self.speed)

