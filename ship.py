import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''A class to manage the ship'''

    def __init__(self, ai_game):
        '''Initialize the ship and set its starting position'''
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect(angle)
        self.image = pygame.image.load('images/invasion_ship.bmp')
        self.rect = self.image.get_rect()

        # Ship turned to alien wessel
        # self.alien_ship = pygame.transform.flip(self.image, False, True)

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value of the ship's horizontal position
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Update ship position using the movement flag'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        '''Draw the ship at its current location'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Center ship at bottom of screen'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)