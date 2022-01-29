import random
import pygame, sys
from pygame.locals import *

from scripts.settings import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("NaturesAngry!!")

from scripts.collisions import *
from scripts.spritesheets import *
from scripts.player import Player
from scripts.particle import LeafParticle
from scripts.boss import Boss

background_layers = [
    scale_image(pygame.image.load("assets/backgrounds/plx-1.png")),
    scale_image(pygame.image.load("assets/backgrounds/plx-2.png")),
    scale_image(pygame.image.load("assets/backgrounds/plx-3.png")),
    scale_image(pygame.image.load("assets/backgrounds/plx-4.png")),
    scale_image(pygame.image.load("assets/backgrounds/plx-5.png")),
    scale_image(pygame.image.load("assets/backgrounds/fog.png")),
    scale_image(pygame.image.load("assets/backgrounds/vines.png")),
]
background_layers[5].set_alpha(50)


def terminate():
    pygame.quit()
    sys.exit()


image_size = 16 * SCALE_AMOUNT / 2
no_of_side_borders = SCALE_HEIGHT // image_size
no_of_bottom_borders = SCALE_WIDTH // image_size

side_border = scale_image(pygame.image.load("assets/border/side_border.png"), SCALE_AMOUNT / 2)
bottom_border = scale_image(pygame.image.load("assets/border/bottom_border.png"), SCALE_AMOUNT / 2)

borders = [
    pygame.Rect(0, 0, image_size - 5, SCALE_HEIGHT),
    pygame.Rect(SCALE_WIDTH - image_size + 5, 0, image_size - 5, SCALE_HEIGHT),
    pygame.Rect(-28, no_of_side_borders * image_size - 3, SCALE_WIDTH + 25, 50),
    pygame.Rect(-28, -15, SCALE_WIDTH + 25, image_size),
]

display = pygame.Surface((SCALE_WIDTH, SCALE_HEIGHT))


def draw_all_bg_elements():
    # Draw the parallax background
    for layer in background_layers:
        display.blit(layer, (0, 0))

    # Draw the borders
    for i in range(int(no_of_side_borders) + 1):
        display.blit(side_border, (0, i * image_size))
        display.blit(pygame.transform.flip(side_border, True, False), (SCALE_WIDTH - image_size, i * image_size))
    for i in range(int(no_of_bottom_borders) + 1):
        display.blit(bottom_border, (i * image_size, no_of_side_borders * image_size - 10))
        display.blit(pygame.transform.flip(bottom_border, False, True), (i * image_size, -10))


player = Player(borders)
boss = Boss(player, borders)

leaves_spritesheet = spritesheet("assets/leaves.png")
leaf_images = leaves_spritesheet.load_strip((0, 0, 4, 4), 4, (0, 0, 0))
leaves = [LeafParticle(leaf_images, True) for _ in range(200)]

for i in range(100):
    for leaf in leaves:
        leaf.update()
    player.update()

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN and not player.attacking and not player.rolling:
            if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                if player.air_timer < 3:
                    player.y_momentum = Player.jump_height
        if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]: player.attack()
        if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]: player.roll()

    draw_all_bg_elements()

    boss.update()
    player.update()

    boss.render(display)
    player.render(display)

    for leaf in leaves:
        leaf.update()
        leaf.render(display)
        if leaf.x < -10 or leaf.x > SCALE_WIDTH + 10 or leaf.y > SCALE_HEIGHT + 10:
            leaves.remove(leaf)
            leaves.append(LeafParticle(leaf_images))

    # for border in borders:
    #     pygame.draw.rect(display, (0, 0, 0), border)

    if not boss.entered:
        screen.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)), (random.randint(-5, 5), random.randint(-5, 5)))
    else:
        screen.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)),
                    (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)))

    pygame.display.update()
    clock.tick(30)

# Font: https://www.behance.net/gallery/16531089/Free-Font-Sabo?fbclid=IwAR3Zu7GmHmiNFhNodQz7BF_SZhtVvt_ecp2LF5NQOgiGwuBDqCKQnfUCdVk
# Skeleton: https://jesse-m.itch.io/skeleton-pack
# Enemies: https://pixelfrog-assets.itch.io/pixel-adventure-2
# Kings & Pigs: https://pixelfrog-assets.itch.io/kings-and-pigs
# Knight: https://aamatniekss.itch.io/fantasy-knight-free-pixelart-animated-character
# UI: https://grafxkid.itch.io/mini-fx-items-ui

# Command to Zip
# pyinstaller --noconfirm --onefile --windowed --clean --add-data "C:/Users/Tejas&Shiva/OneDrive/Desktop/GameJams/MyFirstGameJam/scripts;scripts/"  "C:/Users/Tejas&Shiva/OneDrive/Desktop/GameJams/MyFirstGameJam/main.py"
