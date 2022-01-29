import pygame
pygame.init()
pygame.mixer.init()


def getImage(file, alpha):
    if alpha:
        return pygame.image.load(file).convert_alpha()
    else:
        return pygame.image.load(file).convert()


def getSound(file):
    return pygame.mixer.Sound(file)


# set mouse cursor
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

FPS = 100                # frames per second, the general speed of the program
WINDOW_WIDTH = 1920      # size of window's width in pixels
WINDOW_HEIGHT = 1080     # size of windows' height in pixels
BOX_SIZE_X = 124         # size of box width in pixels
BOX_SIZE_Y = 124         # size of box height in pixels
GAP_SIZE_X = 41          # size of gap between boxes in pixels
GAP_SIZE_Y = 14
BOARD_COLS = 7           # number of columns of icons // 7
BOARD_ROWS = 6           # number of rows of icons // 6
X_MARGIN = (WINDOW_WIDTH - (BOARD_COLS * (BOX_SIZE_X + GAP_SIZE_X))) // 2
Y_MARGIN = (WINDOW_HEIGHT - (BOARD_ROWS * (BOX_SIZE_Y + GAP_SIZE_Y))) // 2
distance = 50
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


#        R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

# images
Board_first = getImage('Assets/Board_First.png', False)
Board_first_small = getImage('Assets/Board_First_small.png', False)  # better sometimes
Board_last = getImage('Assets/Board_Last_smaller.png', True)
Asimon_Red = getImage('Assets/Good_Red.png', True)
Asimon_Yel = getImage('Assets/Good_Yellow.png', True)
Inv_Red = getImage('Assets/Good_Red_Inv.png', True)
Inv_Yel = getImage('Assets/Good_Yellow_Inv.png', True)
Open_Pressed = getImage('Assets/Open.png', False)
Open = getImage('Assets/Open_Pressed.png', False)
EasterEgg = getImage('Assets/hamar.png', False)
Pause_image = getImage('Assets/Connect-Four-Pause.png', False)
Fix_Box = getImage('Assets/Fix_box.png', False)
Glow_Strong = getImage('Assets/Glow.png', True)
Glow_weak = getImage('Assets/lessGlow.png', True)
win_yel = getImage('Assets/yellow finish.png', True)
win_red = getImage('Assets/red finish.png', True)
tie_finish = getImage('Assets/tie finish.png', True)
exit_door = getImage('Assets/exitdoor.png', True)
Asimon_Red = pygame.transform.scale(Asimon_Red, (140, 140))
Asimon_Yel = pygame.transform.scale(Asimon_Yel, (140, 140))
Inv_Red = pygame.transform.scale(Inv_Red, (140, 140))
Inv_Yel = pygame.transform.scale(Inv_Yel, (140, 140))
Glow_Strong = pygame.transform.scale(Glow_Strong, (140, 135))
Glow_weak = pygame.transform.scale(Glow_weak, (140, 135))
exit_door = pygame.transform.scale(exit_door, (140, 140))

# sounds
Mouse_Hover = getSound('Assets/MenuMouse.wav')
falling_sound = getSound('Assets/falling sound.wav')
falling_sound_finish = getSound('Assets/falling sound finish2.wav')
Click_sound = getSound('Assets/Menu Click.wav')
win_sound = getSound('Assets/Winning_Sound.wav')
win_sound_end = getSound('Assets/Winning_sound_end.wav')
falling_sound_finish2 = getSound('Assets/falling sound finish.wav')
tie_sound = getSound('Assets/tie_sound.wav')
