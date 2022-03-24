import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice
from weapons import Weapon
from ui import *
from enemy import Enemy


class Level:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.visible = VerticalCameraGroup()
        self.obstacles = pygame.sprite.Group()
        self.attack = pygame.sprite.Group()
        self.attackable = pygame.sprite.Group()
        self.player = None
        self.attack_sprite = None
        self.create_map()
        self.ui = UI()

    def create_map(self):

        layouts = {
            'boundary': csv_load('graphics/map/map_FloorBlocks.csv'),
            'grass': csv_load('graphics/map/map_Grass.csv'),
            'objects': csv_load('graphics/map/map_LargeObjects.csv'),
            'entities': csv_load('graphics/map/map_Entities.csv')
        }

        graphics = {
            'grass': load_folder('graphics/sprites/grass'),
            'objects': load_folder('graphics/sprites/objects')
        }

        for style, layout in layouts.items():
            for y, line in enumerate(layout):
                for x, sprite_id in enumerate(line):
                    if sprite_id != '-1':
                        pos_x = x * TILESIZE
                        pos_y = y * TILESIZE
                        if style == 'boundary':
                            Tile((pos_x, pos_y), [self.obstacles], 'obstacle')

                        if style == 'grass':
                            grass = choice(graphics['grass'])
                            Tile((pos_x, pos_y), [self.visible, self.obstacles, self.attackable], 'grass', grass)

                        if style == 'objects':
                            obj = graphics['objects'][int(sprite_id)]
                            Tile((pos_x, pos_y), [self.visible, self.obstacles], 'object', obj)

                        if style == 'entities':
                            if sprite_id == '394':
                                self.player = Player((pos_x, pos_y),
                                                     [self.visible],
                                                     self.obstacles,
                                                     self.perform_attack,
                                                     self.end_attack,
                                                     self.perform_magic)
                            else:
                                if sprite_id == '390':
                                    monster_name = 'bamboo'
                                elif sprite_id == '391':
                                    monster_name = 'spirit'
                                elif sprite_id == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name, (pos_x, pos_y), [self.visible, self.attackable], self.obstacles)

    def perform_attack(self):
        self.attack_sprite = Weapon(self.player, [self.visible, self.attack])

    def check_hitting(self):
        for sprite in self.attack:
            hitted = pygame.sprite.spritecollide(sprite, self.attackable, True)
            for target in hitted:
                target.kill()

    def perform_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def end_attack(self):
        if self.attack_sprite:
            self.attack_sprite.kill()
        self.attack_sprite = None

    def run(self):
        self.visible.custom_draw(self.player)
        self.visible.update()
        self.visible.enemy_update(self.player)
        self.check_hitting()
        self.ui.display(self.player)


class VerticalCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.half_width = self.surface.get_size()[0] // 2
        self.half_height = self.surface.get_size()[1] // 2

        self.floor = pygame.image.load('graphics/map/map.png').convert()
        self.floor_rect = self.floor.get_rect(topleft=(0, 0))

    def enemy_update(self, player):
        for sprite in self.sprites():
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy':
                sprite.enemy_update(player)

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        self.surface.blit(self.floor, (0, 0) - self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprites: sprites.rect.centery):
            sprite_offset = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, sprite_offset)
