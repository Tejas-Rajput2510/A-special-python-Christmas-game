import pygame
import random
import sys
import os
import time

# Initialize Pygame
pygame.init()

# Screen setup (resizable so maximize button works)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Santa's Gift Catcher")

# Base directory (script folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Asset paths (files in same folder as script)
background_path = os.path.join(BASE_DIR, "Background.png")
santa_path = os.path.join(BASE_DIR, "Santa.png")
gift_path = os.path.join(BASE_DIR, "Gift.png")
song_path = os.path.join(BASE_DIR, "Song.mp3")

# Load assets
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
santa_img = pygame.image.load(santa_path)
gift_img = pygame.image.load(gift_path)
pygame.mixer.music.load(song_path)

# Resize Santa
santa_img = pygame.transform.scale(santa_img, (100, 100))
santa_rect = santa_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))

# Santa speed
santa_speed = 5

# Define bag area (lower part of Santa)
def get_bag_rect():
    bag_width = 60
    bag_height = 30
    bag_x = santa_rect.centerx - bag_width // 2
    bag_y = santa_rect.bottom - 30
    return pygame.Rect(bag_x, bag_y, bag_width, bag_height)

# Gift class
class Gift:
    def __init__(self):
        self.image = pygame.transform.scale(gift_img.copy(), (40, 40))
        self.rect = self.image.get_rect(midtop=(random.randint(20, WIDTH - 20), -40))
        self.colorize()

    def colorize(self):
        tint = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        tint.fill((random.randint(50,255), random.randint(50,255), random.randint(50,255)))
        self.image.blit(tint, (0,0), special_flags=pygame.BLEND_MULT)

    def fall(self):
        self.rect.y += 3

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)
start_text = font.render("Press Enter to play.", True, (255, 255, 255))
start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Game state
clock = pygame.time.Clock()
gifts = []
game_active = False
score = 0
last_milestone = 0

# Start music
pygame.mixer.music.play(-1)

# Main loop
while True:
    screen.blit(background, (0, 0))

    if not game_active:
        screen.blit(start_text, start_rect)
    else:
        # Santa movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and santa_rect.left > 0:
            santa_rect.x -= santa_speed
        if keys[pygame.K_RIGHT] and santa_rect.right < WIDTH:
            santa_rect.x += santa_speed
        if keys[pygame.K_UP] and santa_rect.top > 0:
            santa_rect.y -= santa_speed
        if keys[pygame.K_DOWN] and santa_rect.bottom < HEIGHT:
            santa_rect.y += santa_speed

        # Spawn gifts
        if random.randint(1, 20) == 1:
            gifts.append(Gift())

        # Update and draw gifts
        bag_rect = get_bag_rect()
        for gift in gifts[:]:
            gift.fall()
            screen.blit(gift.image, gift.rect)
            if gift.rect.colliderect(bag_rect):
                gifts.remove(gift)
                score += 1
            elif gift.rect.top > HEIGHT:
                gifts.remove(gift)
                score = max(0, score - 1)  # penalty but never below 0

        # Draw Santa
        screen.blit(santa_img, santa_rect)

        # Draw score
        score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 150, 20))

        # Check milestone
        if score >= last_milestone + 100:
            last_milestone += 100
            santa_speed += 2  
            milestone_text = font.render(f"{last_milestone} reached!", True, (255, 255, 255))
            milestone_rect = milestone_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(milestone_text, milestone_rect)
            pygame.display.update()
            time.sleep(2)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_active = True
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            background = pygame.image.load(background_path)
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    pygame.display.update()
    clock.tick(60)