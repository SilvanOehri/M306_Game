import pygame
import config
import os

KRUG_SIZE = (80, 80)
BIER_SIZE = (32, 40)
ZAPFHAHN_SIZE = (64, 64)

class Zapfhahn:
    def __init__(self, x):
        self.x = x
        self.y = 40
        self.images = [
            pygame.transform.smoothscale(pygame.image.load("assets/zapfhahn_0.png"), ZAPFHAHN_SIZE),
            pygame.transform.smoothscale(pygame.image.load("assets/zapfhahn_1.png"), ZAPFHAHN_SIZE)
        ]
        self.rect = self.images[0].get_rect(midtop=(self.x, self.y))
        self.frame = 0

    def update(self, tropft=False):
        self.frame = 1 if tropft else 0

    def draw(self, screen):
        screen.blit(self.images[self.frame], self.rect)

class Krug:
    def __init__(self):
        self.images = [
            pygame.transform.smoothscale(pygame.image.load("assets/krug_leer.png"), KRUG_SIZE),
            pygame.transform.smoothscale(pygame.image.load("assets/krug_voll.png"), KRUG_SIZE)
        ]
        self.rect = self.images[0].get_rect(midbottom=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 10))
        self.speed = config.KRUG_SPEED
        self.voll = False

    def move(self, direction):
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > config.SCREEN_WIDTH:
            self.rect.right = config.SCREEN_WIDTH

    def set_voll(self, voll):
        self.voll = voll

    def draw(self, screen):
        idx = 1 if self.voll else 0
        screen.blit(self.images[idx], self.rect)

class Bier:
    ANIMATION_FRAMES = [
        pygame.transform.smoothscale(pygame.image.load(os.path.join("assets", f)), BIER_SIZE)
        for f in sorted(os.listdir("assets")) if f.startswith("bier_") and f.endswith(".png")
    ] if os.path.exists("assets") else [pygame.Surface(BIER_SIZE)]

    def __init__(self, x):
        self.x = x
        self.rect = Bier.ANIMATION_FRAMES[0].get_rect(midtop=(x, 80))
        self.speed = config.BIER_SPEED
        self.frame = 0
        self.frame_timer = 0

    def update(self):
        self.rect.y += self.speed
        self.frame_timer += 1
        if self.frame_timer >= 5:
            self.frame = (self.frame + 1) % len(Bier.ANIMATION_FRAMES)
            self.frame_timer = 0

    def draw(self, screen):
        screen.blit(Bier.ANIMATION_FRAMES[self.frame], self.rect)

    def is_caught_by(self, krug):
        return self.rect.colliderect(krug.rect)

    def is_missed(self):
        return self.rect.top > config.SCREEN_HEIGHT