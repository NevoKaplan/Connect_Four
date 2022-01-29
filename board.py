import constants
import asimon
import pygame


class Board:
    def __init__(self):
        self.board = []
        for row in range(constants.BOARD_ROWS):
            self.board.append([])
            lst = self.board[-1]
            for col in range(constants.BOARD_COLS):
                lst.append(asimon.Place(row, col))

    def all_chips(self):
        chips = []
        for row in range(constants.BOARD_ROWS):
            for col in range(constants.BOARD_COLS):
                chips.append(self.board[row][col])
        return chips

    def draw_board(self, screen, has_won, fine):
        # draws all of the boxes in their covered or revealed stage
        for chip in self.all_chips():
            if not chip.image == '':
                if has_won and fine:
                    screen.blit(chip.image_pre, (chip.left, chip.top))
                    for i in range(len(fine)):
                        screen.blit(fine[i].image, (fine[i].left, fine[i].top))
                else:
                    screen.blit(chip.image, (chip.left, chip.top))

    @staticmethod
    def create_call():
        rect_list = []
        rect = pygame.Rect(397, 52, 165, 990)
        rect_list.append(rect)
        n = 0
        for i in range(1, constants.BOARD_COLS):
            n += 1
            rect = pygame.Rect(rect.right, rect.top, 165, 990)
            rect_list.append(rect)
        return rect_list

    @staticmethod
    def find_place_col(x, y, rect_list):
        col = -1
        for rect in rect_list:
            col += 1
            if rect.collidepoint(x, y):
                return col, rect
        return -1, None

    # checks if the col is full
    def legal_col(self, col):
        if self.board[0][col].image == '':
            return True
        return False

    def find_place_row(self, col):
        row = -1
        for chip in range(constants.BOARD_ROWS):
            if self.board[chip][col].image == '':
                row = chip
            else:
                return row
            if chip == constants.BOARD_ROWS - 1:
                return constants.BOARD_ROWS - 1

    def place_asimon(self, asimon, asimon_pre, color, col, screen, FPS_CLOCK, direction_list):
        row = self.find_place_row(col)
        fall = 0
        has_won = False
        fine = []
        asimon_r = asimon.get_rect()
        asimon_r.move_ip(self.board[row][col].left, constants.distance)
        constants.falling_sound.play()
        while self.board[row][col].top >= asimon_r.top:
            pygame.display.flip()
            screen.blit(constants.Board_first_small, (377, 0))
            asimon_r.move_ip(0, fall)
            fall += 0.08
            screen.blit(asimon, asimon_r)
            self.draw_board(screen, has_won, fine)
            screen.blit(constants.Board_last, (341, 157))
            constants.screen.blit(constants.Fix_Box, (340, 515))
            FPS_CLOCK.tick(240)
        constants.falling_sound.stop()
        if row == constants.BOARD_ROWS - 1:
            constants.falling_sound_finish.play()
        else:
            constants.falling_sound_finish2.play()
        self.board[row][col].image = asimon
        self.board[row][col].image_pre = asimon_pre
        self.board[row][col].color = color
        has_won, fine_list = self.check_win(col, row, color, direction_list)
        return has_won, fine_list

    def check_win(self, col, row, color, direction_list):
        fine2 = []
        for i in range(4):
            (x1, x2, x3, x4) = direction_list[i]
            count1, list1 = self.check_line(col, row, color, x1, x2, True)
            count2, list2 = self.check_line(col, row, color, x3, x4, False)
            if count1 + count2 >= 4:
                fine2 += list1 + list2

        if fine2:
            return True, fine2
        return False, []

    def check_line(self, col, row, color, dr, dc, first):
        count = 0
        winning_asimon = []
        if first:
            count = 1
            winning_asimon = [self.board[row][col]]
        while 0 <= col + dc < constants.BOARD_COLS and 0 <= row + dr < constants.BOARD_ROWS and self.board[row + dr][col + dc].color == color:
            row += dr
            col += dc
            winning_asimon.append(self.board[row][col])
            count += 1
        return count, winning_asimon
