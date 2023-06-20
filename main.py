import sys
import pygame
import pyganim

from game_objects import Player, Background, Opponent
from settings import SIZE


pygame.init()
pygame.display.set_caption('Galaxy')

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

explotion_animation = pyganim.PygAnimation([
    ('assets/blue_explosion/1_{}.png'.format(i), 50) for i in range(17)
], loop=False)

music = pygame.mixer.Sound('assets/music/game.wav')
music.play(-1)

# Group
all_objects = pygame.sprite.Group()
plasmoids = pygame.sprite.Group()
opponents = pygame.sprite.Group()

explotions = []

# Game object
player = Player(clock, plasmoids)
background = Background()


all_objects.add(background)
all_objects.add(player)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    Opponent.process_opponents(clock, opponents)

    all_objects.update()
    plasmoids.update()
    opponents.update()

    opponents_and_plasmoids_collided = pygame.sprite.groupcollide(opponents, plasmoids, True, True)

    for collided in opponents_and_plasmoids_collided:
        explotion = explotion_animation.getCopy()
        explotion.play()
        explotions.append((explotion, (collided.rect.center)))

    player_and_opponents_collided = pygame.sprite.spritecollide(player, opponents, True)

    if player_and_opponents_collided:
        all_objects.remove(player)

    all_objects.draw(screen)
    plasmoids.draw(screen)
    opponents.draw(screen)


    for explotion, position in explotions.copy():
        if explotion.isFinished():
            explotions.remove((explotion, position))
        else:
            x, y = position
            explotion.blit(screen, (x - 128, y - 128))

    pygame.display.flip()
    clock.tick(30)


