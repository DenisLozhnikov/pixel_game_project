import pygame
from support import *
from settings import *
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, attack, end_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('sprites/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.obstacle_sprites = obstacle_sprites
        self.hitbox = self.rect.inflate(0, -25)

        self.can_attack = True
        self.attack_cooldown = 400
        self.last_attack = pygame.time.get_ticks()

        self.player_status = 'down'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        self.import_player_assets()

        self.selected_weapon = 0
        self.attack = attack
        self.end_attack = end_attack
        self.weapon_name = list(weapon_data.keys())[self.selected_weapon]
        self.weapons = len(list(weapon_data.keys())) - 1
        self.can_switch_weapon = True
        self.last_switch_weapon = pygame.time.get_ticks()
        self.switch_cooldown = 200

        self.create_magic = create_magic
        self.selected_cast = 0
        self.cast_name = list(magic_data.keys())[self.selected_cast]
        self.casts = len(list(magic_data.keys())) - 1
        self.can_switch_cast = True
        self.last_switch_cast = pygame.time.get_ticks()

        self.stats = {'health': 100,
                      'energy': 60,
                      'attack': 10,
                      'magic': 4,
                      'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 50
        self.speed = self.stats['speed']

    def import_player_assets(self):
        path = 'graphics/player/'

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = load_folder(full_path)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0 and not 'idle' in self.player_status:
            if  'attack' not in self.player_status:
                self.player_status += '_idle'
            if self.can_attack:
                self.player_status = self.player_status.replace('_attack', '_idle')
                self.end_attack()

        if not self.can_attack and  'attack' not in self.player_status:
            self.direction.x = 0
            self.direction.y = 0
            if 'idle' in self.player_status:
                self.player_status = self.player_status.replace('_idle', '_attack')
            else:
                self.player_status += '_attack'

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_attack:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.player_status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.player_status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.player_status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.player_status = 'right'
            else:
                self.direction.x = 0

        # attack
        if keys[pygame.K_SPACE] and self.can_attack:
            self.can_attack = False
            self.last_attack = pygame.time.get_ticks()
            self.attack()

        # spell
        if keys[pygame.K_c] and self.can_attack:
            self.can_attack = False
            self.last_attack = pygame.time.get_ticks()
            style = list(magic_data.keys())[self.selected_cast]
            strength = list(magic_data.values())[self.selected_cast]['strength'] + self.stats['magic']
            cost = list(magic_data.values())[self.selected_cast]['cost']
            self.create_magic(style, strength, cost)

        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.last_switch_weapon = pygame.time.get_ticks()
            self.selected_weapon = self.selected_weapon + 1 if self.selected_weapon != self.weapons else 0
            self.weapon_name = list(weapon_data.keys())[self.selected_weapon]

        if keys[pygame.K_e] and self.can_switch_cast:
            self.can_switch_cast = False
            self.last_switch_cast = pygame.time.get_ticks()
            self.selected_cast = self.selected_cast + 1 if self.selected_cast != self.casts else 0
            self.cast_name = list(magic_data.keys())[self.selected_cast]

    def check_cooldowns(self):
        curr_time = pygame.time.get_ticks()
        if curr_time - self.last_attack >= self.attack_cooldown:
            self.can_attack = True

        if curr_time - self.last_switch_weapon >= self.switch_cooldown:
            self.can_switch_weapon = True

        if curr_time - self.last_switch_cast >= self.switch_cooldown:
            self.can_switch_cast = True

    def animate(self):
        animation = self.animations[self.player_status]

        self.anim_frame += self.anim_speed
        if self.anim_frame >= len(animation):
            self.anim_frame = 0

        self.image = animation[int(self.anim_frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.check_cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
