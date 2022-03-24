import pygame
from settings import *


class UI:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, FONT_SIZE)

        self.heath_bar = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapons = [pygame.image.load(weapon['graphic']).convert_alpha()
                        for weapon in weapon_data.values()]  # get graphic weapon

        self.spells = [pygame.image.load(spell['graphic']).convert_alpha()
                        for spell in magic_data.values()]  # get graphic spells

    def display(self, player):
        self.render_bar(player.health, player.stats['health'], self.heath_bar, HEALTH_COLOR)
        self.render_bar(player.energy, player.stats['energy'], self.energy_bar, ENERGY_COLOR)
        self.render_exp(player.exp)
        self.weapon_overlay(player.selected_weapon, not player.can_switch_weapon)
        self.magic_overlay(player.selected_cast, not player.can_switch_cast)

    def weapon_overlay(self, weapon, active):
        bg = self.sel_box(10, 614, active)
        weapon_surf = self.weapons[weapon]
        weapon_rect = weapon_surf.get_rect(center=bg.center)
        self.surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, spell, active):
        bg = self.sel_box(80, 634, active)
        magic_surf = self.spells[spell]
        magic_rect = magic_surf.get_rect(center=bg.center)
        self.surface.blit(magic_surf, magic_rect)

    def render_bar(self, current, amount, bg, color):
        pygame.draw.rect(self.surface, UI_BG_COLOR, bg)

        ratio = current / amount
        curr_width = bg.width * ratio
        curr_rect = bg.copy()
        curr_rect.width = curr_width

        pygame.draw.rect(self.surface, color, curr_rect)
        pygame.draw.rect(self.surface, UI_BORDER_COLOR, bg, 3)

    def render_exp(self, exp):
        text_surface = self.font.render(str(exp), False, TEXT_COLOR)
        x = self.surface.get_size()[0]
        y = self.surface.get_size()[1]
        text_rect = text_surface.get_rect(bottomright=(x - 20, y - 20))
        pygame.draw.rect(self.surface, UI_BG_COLOR, text_rect.inflate(10, 10))
        pygame.draw.rect(self.surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)
        self.surface.blit(text_surface, text_rect)

    def sel_box(self, left, top, highlighted):
        bg = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.surface, UI_BG_COLOR, bg)
        if highlighted:
            pygame.draw.rect(self.surface, UI_BORDER_COLOR_ACTIVE, bg, 3)
        else:
            pygame.draw.rect(self.surface, UI_BORDER_COLOR, bg, 3)

        return bg
