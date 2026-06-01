"""
Kosmosa Matemātikas Misija - Spēles Konstantes
"""

SCREEN_WIDTH  = 960
SCREEN_HEIGHT = 720
FPS           = 60
WINDOW_TITLE  = "Kosmosa Matemātikas Misija"

SHIP_SCREEN_X = SCREEN_WIDTH  // 2
SHIP_SCREEN_Y = int(SCREEN_HEIGHT * 0.8)

SHIP_WIDTH        = 60
SHIP_HEIGHT       = 72
SHIP_SPEED_X      = 350   
SHIP_MAX_HEALTH   = 100
SHIP_MAX_FUEL     = 100
SHIP_FUEL_DRAIN   = 3.5   
LOW_FUEL_THRESHOLD= 30.0  
SHIP_BOUNCE_SPEED = 280   
SHIP_BOUNCE_TIME  = 0.35  

ASTEROID_MIN_RADIUS = 15
ASTEROID_MAX_RADIUS = 45
ASTEROID_DMG_SMALL  = 10
ASTEROID_DMG_MEDIUM = 20
ASTEROID_DMG_LARGE  = 30

PICKUP_RADIUS          = 20
HEALTH_PICKUP_VALUE    = 25
FUEL_PICKUP_VALUE      = 35
PICKUP_FLOAT_AMPLITUDE = 4.0  
PICKUP_FLOAT_SPEED     = 2.0  

MAX_STRIKES               = 3
EMERGENCY_FUEL_AMOUNT     = 50
BREAKDOWN_FUEL_PENALTY    = 20
BREAKDOWN_FUEL_SAVE_TIME  = 4.5 

PARTICLE_LIFETIME    = 40
PARTICLE_COUNT_HIT   = 25
PARTICLE_COUNT_PICK  = 15

# Krāsas
C_BLACK       = (0,   0,   0)
C_WHITE       = (255, 255, 255)
C_DARK_SPACE  = (4,   4,   18)

C_SHIP_BODY   = (22,  60,  180)
C_SHIP_DARK   = (10,  30,  95)
C_SHIP_WING   = (18,  50,  150)
C_SHIP_ACCENT = (75,  155, 255)
C_COCKPIT_L   = (155, 215, 255)
C_COCKPIT_D   = (60,  140, 220)
C_ENGINE      = (40,  90,  200)
C_FLAME_CORE  = (255, 255, 100)
C_FLAME_MID   = (255, 160, 20)
C_FLAME_OUT   = (255, 80,  10)

C_ASTEROID    = (105, 100, 98)
C_ASTER_DARK  = (62,  58,  56)
C_ASTER_LIGHT = (135, 130, 128)

C_HEALTH      = (0,   210, 75)
C_HEALTH_DIM  = (0,   100, 35)
C_FUEL        = (255, 135, 0)
C_FUEL_DIM    = (120, 60,  0)
C_HUD_BG      = (6,   6,   20)
C_STRIKE_ON   = (220, 30,  30)
C_STRIKE_OFF  = (55,  55,  70)
C_EMERGENCY   = (220, 160, 20)
C_EMERG_USED  = (60,  60,  75)

C_PROG_BG     = (30, 30, 50)
C_PROG_FG     = (70, 180, 255)

C_BTN         = (25,  65,  175)
C_BTN_HOV     = (45,  100, 220)
C_BTN_TXT     = (210, 235, 255)
C_TITLE_CLR   = (100, 205, 255)
C_GOLD        = (255, 215, 50)
C_FINISH_LINE = (0,   255, 100)

C_POPUP_BG    = (7,   10,  32)
C_POPUP_BDR   = (45,  115, 215)
C_BREAK_BG    = (30,  12,  5)
C_BREAK_BDR   = (200, 100, 20)
C_INPUT_ACTI  = (28,  55,  140)
C_TIMER_BAR   = (70,  175, 255)
C_TIMER_LOW   = (215, 75,  25)
C_CORRECT     = (0,   220, 80)
C_WRONG       = (220, 40,  40)

C_HEALTH_PICK = (0,   220, 80)
C_FUEL_PICK   = (220, 100, 20)

# TEKSTI 
TXT_TITLE         = "Kosmosa Matemātikas Misija"
TXT_PLAY          = "Spēlēt"
TXT_EXIT          = "Iziet"
TXT_CHOOSE_LEVEL  = "Izvēlies Līmeni"
TXT_LOCKED        = "Slēgts"
TXT_START         = "SĀKT SPĒLI!"
TXT_HEALTH        = "VESELĪBA"
TXT_FUEL          = "DEGVIELA"
TXT_FINISH        = "F I N I Š S"
TXT_STRIKES       = "Kļūdas:"
TXT_MATH_TASK     = "MATEMĀTIKAS UZDEVUMS"
TXT_BREAKDOWN     = "DZINĒJA BOJĀJUMS"
TXT_ANSWER        = "Atbilde:"
TXT_CONFIRM       = "Nospied ENTER, lai apstiprinātu"
TXT_CORRECT       = "Pareizi!"
TXT_WRONG_ANS     = "Nepareizi!"
TXT_TIMEOUT       = "Laiks beidzies!"
TXT_WIN_TITLE     = "LĪMENIS PABEIGTS!"
TXT_LOSE_TITLE    = "SPĒLE BEIGUSIES"
TXT_NEXT_LVL      = "Nākamais Līmenis"
TXT_REPLAY        = "Atkārtot"
TXT_MENU          = "Uz Izvēlni"
TXT_RETRY         = "Mēģināt Vēlreiz"
TXT_EMERG_FUEL    = "ĀRKĀRTAS\nDEGVIELA"
TXT_OUT_FUEL      = "Degviela beigusies - pēdējā iespēja izmantota!"
TXT_3_STRIKES     = "3 kļūdas - misija neizdevās!"
TXT_NO_HEALTH     = "Veselība = 0 - kuģis sagrauts!"
TXT_BACK          = "Atpakaļ"

FS_SMALL  = 16
FS_MED    = 22
FS_LARGE  = 34
FS_TITLE  = 54
FS_HUGE   = 70