import pygame
import sys
import constants
import board
from datetime import datetime


def main():
    global FPS_CLOCK, screen, main_board, turn, last_turn

    main_board = board.Board()
    pygame.init()
    pygame.mixer.init()
    #pygame.mixer.music.play(-1, 0.0)

    FPS_CLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    pygame.display.set_caption('Connect 4 - The Game')
    start_game = True
    constants.screen.blit(constants.Board_first, (0, 0))
    restart = True
    flag = False
    do_again = False

    while start_game:
        restart, flag = start(restart, flag, do_again)
        start_game, restart, do_again = main_game(flag)


# the main menu
def start(restart, flag, do_again):
    rect = pygame.Rect(728, 768, 415, 128)
    rect2 = pygame.Rect(470, 744, 15, 15)
    exit_door_r = constants.exit_door.get_rect()
    exit_door_r.move_ip(1645, 800)
    while restart:
        if do_again:
            restart = False
            flag = True
            return restart, flag
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # if touch the play - change pic
        if rect2.collidepoint(mouse_x, mouse_y) and event.type == pygame.MOUSEBUTTONDOWN:
            show = True
            if show:
                constants.screen.blit(constants.EasterEgg, (0, 0))
                pygame.display.flip()
                pygame.time.wait(100)
                show = False
        if rect.collidepoint(mouse_x, mouse_y):
            constants.screen.blit(constants.Open, (0, 0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                constants.Click_sound.play()
                restart = True
                flag = True
                return restart, flag
        else:
            constants.screen.blit(constants.Open_Pressed, (0, 0))
        if exit_door_r.collidepoint(mouse_x, mouse_y):
            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
                exit()
        screen.blit(constants.exit_door, exit_door_r)
        pygame.display.flip()


def main_game(play):
    global turn, last_turn, main_board
    start_game = True
    main_board = board.Board()
    last_turn = -1
    turn = 0
    rect_list = main_board.create_call()
    col = 0
    col_rect = rect_list[0]
    asimon = constants.Asimon_Red
    color = 'red'
    x, y = 0, 0
    pygame.event.clear()
    # rect creation
    play_area = pygame.Rect(rect_list[0].left, rect_list[0].top, rect_list[-1].right - rect_list[0].left,
                       rect_list[-1].bottom - rect_list[0].top)
    pre_area_rect = pygame.Rect(rect_list[0].left, 1, rect_list[-1].right - rect_list[0].left, 199)
    Continue = pygame.Rect(651, 251, 669, 208)
    BackToMenu = pygame.Rect(651, 494, 669, 208)
    Desktop = pygame.Rect(651, 737, 669, 208)
    Restart_rect = pygame.Rect(850, 447, 272, 74)
    Main_rect = pygame.Rect(759, 601, 428, 74)
    Exit_rect = pygame.Rect(912, 763, 141, 74)
    constants.screen.blit(constants.Board_first, (0, 0))
    list_of_pre_rects, list_of_dy = pre_bounce()
    direction_list = [(0, 1, 0, -1), (1, 0, -1, 0), (1, 1, -1, -1), (1, -1, -1, 1)]
    has_won = False
    fine_list = []
    wait = 0
    sound = True
    play_win_sound = True
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.load('Assets/Zelda & Chill.mp3')
    pygame.mixer.music.play(-1, 0.0)
    while play:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                restart = False
                start_game = False
                return start_game, restart, False
            if event.type == pygame.MOUSEBUTTONDOWN and play_area.collidepoint(x, y) and main_board.legal_col(col) and not has_won:
                has_won, fine_list = main_board.place_asimon(asimon, asimon_pre, color, col, constants.screen, FPS_CLOCK, direction_list)
                pygame.event.clear()  # ignores any previous clicks during animation
                turn += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.pause()
                play, restart = pause(Continue, BackToMenu, Desktop)
                constants.screen.blit(constants.Board_first, (0, 0))
                pygame.event.clear()
                if not play:
                    if restart:
                        return start_game, restart, False
                    else:
                        start_game = False
                        return start_game, restart, False
                pygame.mixer.music.unpause()

        # red or yellow turn
        if turn % 2 == 0:
            asimon = constants.Asimon_Red
            asimon_pre = constants.Inv_Red
            color = 'red'
        else:
            asimon = constants.Asimon_Yel
            asimon_pre = constants.Inv_Yel
            color = 'yel'

        constants.screen.blit(constants.Board_first_small, (377, 0))
        main_board.draw_board(constants.screen, has_won, fine_list)
        constants.screen.blit(constants.Board_last, (341, 157))
        constants.screen.blit(constants.Fix_Box, (340, 515))
        if not has_won:
            col, col_rect, sound = handle_motion(asimon, rect_list, x, y, col, col_rect, play_area, sound)
            pre_bounce_blit(list_of_pre_rects, list_of_dy, asimon_pre, pre_area_rect, col)
            play, restart, do_again = check_tie(Restart_rect, Main_rect, Exit_rect)
        else:
            if play_win_sound:
                pygame.mixer.music.stop()
                constants.win_sound.play()
                play_win_sound = False
            now = datetime.now()
            MicroSecond = now.microsecond
            for i in range(len(fine_list)):
                if MicroSecond < 500000:
                    screen.blit(constants.Glow_Strong, (fine_list[i].left, fine_list[i].top))
                else:
                    screen.blit(constants.Glow_weak, (fine_list[i].left, fine_list[i].top))
            wait += 1
            if wait > 450:
                play, restart, do_again = winning_screen(Restart_rect, Main_rect, Exit_rect, fine_list)
        pygame.display.flip()
        if not play:
            if restart:
                return start_game, restart, do_again
            else:
                start_game = False
                return start_game, restart, do_again
        FPS_CLOCK.tick(100)


def handle_motion(asimon, rect_list, x, y, col, col_rect, area, sound):
    # places the chips at the top of the board
    if col_rect:
        if not col_rect.collidepoint(x, y):
            col, col_rect = main_board.find_place_col(x, y, rect_list)
            sound = True
    elif area.collidepoint(x, y):
        col, col_rect = main_board.find_place_col(x, y, rect_list)
        sound = True
    if col != -1:
        if main_board.legal_col(col):
            constants.screen.blit(asimon, (main_board.board[0][col].left, constants.distance))
            if sound:
                constants.Mouse_Hover.play()
                sound = False

    return col, col_rect, sound


def pre_bounce():
    list_of_pre_rects = []
    list_of_dy = []
    top = 35
    left = main_board.board[0][0].left
    for i in range(constants.BOARD_COLS):
        list_of_pre_rects.append(constants.Inv_Red.get_rect())
        list_of_dy.append(1)

    for i in range(len(list_of_pre_rects)):
        list_of_pre_rects[i].move_ip(left, top)
        left += 165
    return list_of_pre_rects, list_of_dy

def pre_bounce_blit(list_of_pre_rects, list_of_dy, asimon_pre, pre_area_rect, col):
    for i in range(len(list_of_pre_rects)):
        if i != col and main_board.legal_col(i):
            if asimon_pre == constants.Inv_Red:
                constants.screen.blit(constants.Inv_Red, list_of_pre_rects[i])
            else:
                constants.screen.blit(constants.Inv_Yel, list_of_pre_rects[i])
        if list_of_pre_rects[i].top <= pre_area_rect.top:
            list_of_dy[i] *= -1
        elif list_of_pre_rects[i].bottom >= pre_area_rect.bottom:
            list_of_dy[i] *= -1
        list_of_pre_rects[i].move_ip(0, list_of_dy[i])


def pause(Continue, BackToMenu, Desktop):
    play = True
    restart = False
    sound = True
    while True:
        event = pygame.event.poll()
        x, y = pygame.mouse.get_pos()
        constants.screen.blit(constants.Pause_image, (0, 0))
        if event.type == pygame.QUIT:
            play = False
            return play, restart
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return play, restart
        elif Continue.collidepoint(x, y):
            pygame.draw.rect(constants.screen, constants.GREEN, Continue, 10)
            if event.type == pygame.MOUSEBUTTONUP:
                constants.Click_sound.play()
                return play, restart
            if sound:
                constants.Mouse_Hover.play()
                sound = False
        elif BackToMenu.collidepoint(x, y):
            pygame.draw.rect(constants.screen, constants.YELLOW, BackToMenu, 10)
            if sound:
                constants.Mouse_Hover.play()
                sound = False
            if event.type == pygame.MOUSEBUTTONUP:
                constants.Click_sound.play()
                play = False
                restart = True
                return play, restart
        elif Desktop.collidepoint(x, y) or event.type == pygame.QUIT:
            if sound:
                constants.Mouse_Hover.play()
                sound = False
            pygame.draw.rect(constants.screen, constants.ORANGE, Desktop, 10)
            if event.type == pygame.MOUSEBUTTONUP:
                constants.Click_sound.play()
                play = False
                return play, restart
        else:
            sound = True
        pygame.display.flip()


def winning_screen(restart, main_menu, exit, fine_list):
    sound = True
    constants.win_sound_end.play()
    while True:
        event = pygame.event.poll()
        x, y = pygame.mouse.get_pos()
        if fine_list[0].color == 'red':
            screen.blit(constants.win_red, (0, 0))
        else:
            screen.blit(constants.win_yel, (0, 0))
        if event.type == pygame.QUIT:
            return False, False, False
        elif restart.collidepoint(x, y):
            if sound:
                constants.Mouse_Hover.play()
                sound = False
            if fine_list[0].color == 'red':
                pygame.draw.line(screen, constants.YELLOW, (850, 521), (1122, 521), 2)
            else:
                pygame.draw.line(screen, constants.RED, (850, 521), (1122, 521), 2)
            if event.type == pygame.MOUSEBUTTONUP:
                constants.Click_sound.play()
                return False, True, True  # returns values to quick restart
        elif main_menu.collidepoint(x, y):
            if sound:
                constants.Mouse_Hover.play()
                sound = False
            if fine_list[0].color == 'red':
                pygame.draw.line(screen, constants.YELLOW, (759, 675), (1187, 675), 2)
            else:
                pygame.draw.line(screen, constants.RED, (759, 675), (1187, 675), 2)
            if event.type == pygame.MOUSEBUTTONUP:
                constants.Click_sound.play()
                return False, True, False  # returns values to main
        elif exit.collidepoint(x, y):
            if sound:
                constants.Mouse_Hover.play()
                sound = False
            if fine_list[0].color == 'red':
                pygame.draw.line(screen, constants.YELLOW, (912, 837), (1053, 837), 2)
            else:
                pygame.draw.line(screen, constants.RED, (912, 837), (1053, 837), 2)
            if event.type == pygame.MOUSEBUTTONUP:
                constants.Click_sound.play()
                return False, False, False  # quits game
        else:
            sound = True
        pygame.display.flip()


# checks for a tie
# tie can only be if 42 chips were placed
def check_tie(restart, main_menu, exit_r):
    global turn
    if turn == 42:
        constants.tie_sound.play()
        pygame.mixer.music.stop()
        while True:
            event = pygame.event.poll()
            x, y = pygame.mouse.get_pos()
            screen.blit(constants.tie_finish, (0, 0))
            if event.type == pygame.QUIT:
                return False, False, False
            elif restart.collidepoint(x, y):
                if sound:
                    constants.Mouse_Hover.play()
                    sound = False
                pygame.draw.line(screen, constants.BLACK, (850, 521), (1122, 521), 2)
                if event.type == pygame.MOUSEBUTTONUP:
                    constants.Click_sound.play()
                    return False, True, True  # returns values to quick restart
            elif main_menu.collidepoint(x, y):
                if sound:
                    constants.Mouse_Hover.play()
                    sound = False
                pygame.draw.line(screen, constants.BLACK, (759, 675), (1187, 675), 2)
                if event.type == pygame.MOUSEBUTTONUP:
                    constants.Click_sound.play()
                    return False, True, False  # returns values to main
            elif exit_r.collidepoint(x, y):
                if sound:
                    constants.Mouse_Hover.play()
                    sound = False
                pygame.draw.line(screen, constants.BLACK, (912, 837), (1053, 837), 2)
                if event.type == pygame.MOUSEBUTTONUP:
                    constants.Click_sound.play()
                    return False, False, False  # quits game
            else:
                sound = True
            pygame.display.flip()
    else:
        return True, False, True


if __name__ == '__main__':
    main()
