
import core
import sys
import pygame
import random
from modules import *


def initGame():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(core.SCREENSIZE)
    pygame.display.set_caption('By Rizwan.AR')
    return screen


def main():

    screen = initGame()

    pygame.mixer.music.load(core.BGM_PATH)
    pygame.mixer.music.play(-1)
    audios = {
        'count_down': pygame.mixer.Sound(core.COUNT_DOWN_SOUND_PATH),
        'hammering': pygame.mixer.Sound(core.HAMMERING_SOUND_PATH)
    }

    font = pygame.font.Font(core.FONT_PATH, 40)

    bg_img = pygame.image.load(core.GAME_BG_IMAGEPATH)

    startInterface(screen, core.GAME_BEGIN_IMAGEPATHS)

    hole_pos = random.choice(core.HOLE_POSITIONS)
    change_hole_event = pygame.USEREVENT
    pygame.time.set_timer(change_hole_event, 800)

    mole = Mole(core.MOLE_IMAGEPATHS, hole_pos)

    hammer = Hammer(core.HAMMER_IMAGEPATHS, (500, 250))

    clock = pygame.time.Clock()

    your_score = 0
    flag = False

    init_time = pygame.time.get_ticks()

    while True:

        time_remain = round((61000 - (pygame.time.get_ticks() - init_time)) / 1000.)

        if time_remain == 40 and not flag:
            hole_pos = random.choice(core.HOLE_POSITIONS)
            mole.reset()
            mole.setPosition(hole_pos)
            pygame.time.set_timer(change_hole_event, 650)
            flag = True
        elif time_remain == 20 and flag:
            hole_pos = random.choice(core.HOLE_POSITIONS)
            mole.reset()
            mole.setPosition(hole_pos)
            pygame.time.set_timer(change_hole_event, 500)
            flag = False

        if time_remain == 10:
            audios['count_down'].play()

        if time_remain < 0: break
        count_down_text = font.render('Time: '+str(time_remain), True, core.WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                hammer.setPosition(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    hammer.setHammering()
            elif event.type == change_hole_event:
                hole_pos = random.choice(core.HOLE_POSITIONS)
                mole.reset()
                mole.setPosition(hole_pos)

        if hammer.is_hammering and not mole.is_hammer:
            is_hammer = pygame.sprite.collide_mask(hammer, mole)
            if is_hammer:
                audios['hammering'].play()
                mole.setBeHammered()
                your_score += 10

        your_score_text = font.render('Score: '+str(your_score), True, core.BROWN)

        screen.blit(bg_img, (0, 0))
        screen.blit(count_down_text, (875, 8))
        screen.blit(your_score_text, (800, 430))
        mole.draw(screen)
        hammer.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    try:
        best_score = int(open(core.RECORD_PATH).read())
    except:
        best_score = 0

    if your_score > best_score:
        f = open(core.RECORD_PATH, 'w')
        f.write(str(your_score))
        f.close()

    score_info = {'your_score': your_score, 'best_score': best_score}
    is_restart = endInterface(screen, core.GAME_END_IMAGEPATH, core.GAME_AGAIN_IMAGEPATHS, score_info, core.FONT_PATH, [core.WHITE, core.RED], core.SCREENSIZE)
    return is_restart


if __name__ == '__main__':
    while True:
        is_restart = main()
        if not is_restart:
            break
