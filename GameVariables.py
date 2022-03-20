import os
import pygame
from pygame import mixer
from pokemondata import *

mixer.init()
pygame.init()

# Define project variable:
## Settings variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH*0.8)
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Fonts variabels
font1 = pygame.font.SysFont('Futura', 35)
font = pygame.font.SysFont('Futura', 30)
font_2 = pygame.font.SysFont('Futura', 15)
font_tm = pygame.font.SysFont('Futura', 18)
font_enemy = pygame.font.SysFont('Futura', 20)

## Game variables
MAX_LEVELS = 3
GRAVITY = 0.5
party_states_lvl100_lst = [[],[],[],[],[],[]]
party_lst = []
'''Game style is is under title "game-style" '''

##Functional variabels:
level = 1
ROWS = 16 # MUST BE cording lvl editor
COLS = 150 # according lvl editor
#TYLE_TYPES = len(os.listdir('images\\game_background1\\tiles')) + len(os.listdir('images\\game_background1\\tiles'))
TILE_SIZE = SCREEN_HEIGHT // (ROWS)#-1.2)
menu_SIZE = 0.5*TILE_SIZE
SCROLL_TRESH = SCREEN_WIDTH//2 #the distance the player get to the edge of the screen

### Init variabels:
screen_scroll = 0
bg_scroll = 0
event_timer_s = 0
event_timer_a = 0
event_timer_d = 0
event_timer_sp = 0
event_timer_spd = 0

### Logic variabels:
start_game = False
start_intro = False
tm1_active = False
speed_boost = False
atk_boost = False
deff_boost = False
spa_boost = False
spd_boost = False
pause_activate = False
pause_mode = False
pause_from_esc_keyboard = False
pause_from_pokemon_party_btn = False
settings_mode = False
setting_controller = False
choose_character = True

#define player action variables:
moving_left = False # at the begining the player didnt move
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
pokeball_throw_keyboard = False
draw_menu_keyboard = False
second_for_energy = False
no_enemy = False

lst_251 = ['0','Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle', 'Wartortle', 'Blastoise', 'Caterpie', 'Metapod',
           'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto', 'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok',
           'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'Nidoran♀', 'Nidorina', 'Nidoqueen', 'Nidoran♂', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable',
           'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Venonat',
           'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 'Primeape', 'Growlithe', 'Arcanine', 'Poliwag',
           'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 'Machoke', 'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel',
           'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton',
           "Farfetch'd", 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee',
           'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung',
           'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie',
           'Mr.Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon',
           'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres',
           'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew', 'Chikorita', 'Bayleef', 'Meganium', 'Cyndaquil', 'Quilava', 'Typhlosion', 'Totodile',
           'Croconaw', 'Feraligatr', 'Sentret', 'Furret', 'Hoothoot', 'Noctowl', 'Ledyba', 'Ledian', 'Spinarak', 'Ariados', 'Crobat', 'Chinchou',
           'Lanturn', 'Pichu', 'Cleffa', 'Igglybuff', 'Togepi', 'Togetic', 'Natu', 'Xatu', 'Mareep', 'Flaaffy', 'Ampharos', 'Bellossom', 'Marill',
           'Azumarill', 'Sudowoodo', 'Politoed', 'Hoppip', 'Skiploom', 'Jumpluff', 'Aipom', 'Sunkern', 'Sunflora', 'Yanma', 'Wooper', 'Quagsire',
           'Espeon', 'Umbreon', 'Murkrow', 'Slowking', 'Misdreavus', 'Unown', 'Wobbuffet', 'Girafarig', 'Pineco', 'Forretress', 'Dunsparce', 'Gligar',
           'Steelix', 'Snubbull', 'Granbull', 'Qwilfish', 'Scizor', 'Shuckle', 'Heracross', 'Sneasel', 'Teddiursa', 'Ursaring', 'Slugma', 'Magcargo',
           'Swinub', 'Piloswine', 'Corsola', 'Remoraid', 'Octillery', 'Delibird', 'Mantine', 'Skarmory', 'Houndour', 'Houndoom', 'Kingdra', 'Phanpy',
           'Donphan', 'Porygon2', 'Stantler', 'Smeargle', 'Tyrogue', 'Hitmontop', 'Smoochum', 'Elekid', 'Magby', 'Miltank', 'Blissey', 'Raikou', 'Entei',
           'Suicune', 'Larvitar', 'Pupitar', 'Tyranitar', 'Lugia', 'Ho-Oh', 'Celebi']



#Dicts here connect between string names into pokemon obj in pokemondata file.
pokemon_collection = dict(zip(lst_251[0:len(pokemon_object_lst)],pokemon_object_lst))
enemy_collection = dict()

#define colours: (rgb - red,blue,green)
BG = (25,125,215)
RED = (255,0,0)
GREEN = (0,255,0)
GREEN2 = (90,201,75)
WHITE = (250,250,250)
BLACK = (25,25,25)
BLUE = (0,50,250)
PINK = (235,65,54)
GRAY = (125,125,250)
set_color = (250,250,250)


## Images
img_directoriy = r'C:\Users\benny\Desktop\python\pygame_project\images'
## Sounds

#sounds #TODO: theres some work with this subject
BG_MUSIC =['open game','103-professor oak','title_screen','viridian','gym','center']
############ GAME SOUNDS ###################
jump_fx = pygame.mixer.Sound('audio\\jump.wav')
jump_fx.set_volume(0.03)
jump_water_fx = pygame.mixer.Sound('audio\\jump_water.wav')
jump_water_fx.set_volume(0.02)
falling_fx = pygame.mixer.Sound('audio\\falling.wav')
falling_fx.set_volume(0.05)
shooting_fx = pygame.mixer.Sound('audio\\shoot_electric.wav')
shooting_fx.set_volume(0.04)

pokemon_lvl_up_fx = pygame.mixer.Sound('audio\\pokemon_lvl_up.mp3')
pokemon_lvl_up_fx.set_volume(0.05)
end_lvl_fx = pygame.mixer.Sound('audio\\end_lvl.mp3')
end_lvl_fx.set_volume(0.05)
item_fx = pygame.mixer.Sound('audio\\item.wav')
item_fx.set_volume(0.05)
wall_bump_fx = pygame.mixer.Sound('audio\\wall_bump.mp3')
wall_bump_fx.set_volume(0.02)
caught_pokemon_fx = pygame.mixer.Sound('audio\\caught_a_pokemon.mp3')
caught_pokemon_fx.set_volume(0.07)


####### POKEMON SOUNDS
bulba_fx = pygame.mixer.Sound('audio\\pokemon\\Bulbasaur\\bulbasaur-sound.mp3')
bulba_fx.set_volume(0.5)

sound_volume_lst = [jump_fx,jump_water_fx,falling_fx,shooting_fx,item_fx,end_lvl_fx,wall_bump_fx,pokemon_lvl_up_fx,bulba_fx,caught_pokemon_fx]


##LOAD IMAGES
main_bg_img = pygame.image.load('images\\game_background1\\main_bg.png').convert_alpha()
pokemon_bg_img = pygame.image.load('images\\game_background1\\pokemon_bg.png').convert_alpha()
choose_starter_img = pygame.image.load('images\\game_background1\\choose starter.png').convert_alpha()
oak_img = pygame.image.load('images\\game_background1\\oak.png').convert_alpha()
controller_setting_bg_image = pygame.image.load('images\\game_background1\\setting_control_bg.jpg')
#controller_setting_bg_image = pygame.transform.scale(controller_setting_bg_image,(pygame.display.get_surface().get_size()))


bulba_img = pygame.image.load('images\\game_background1\\starters\\bulba starter.png').convert_alpha()
squir_img = pygame.image.load('images\\game_background1\\starters\\squir starter.png').convert_alpha()
charma_img = pygame.image.load('images\\game_background1\\starters\\charma starter.png').convert_alpha()
pikca_img = pygame.image.load('images\\game_background1\\starters\\pikca starter.png').convert_alpha()
#button images
start_img = pygame.image.load('images\\game_background1\\start_btn.png').convert_alpha()
exit_img = pygame.image.load('images\\game_background1\\exit_btn.png').convert_alpha()
restart_img = pygame.image.load('images\\game_background1\\restart_btn.png').convert_alpha()
fullscreen_img = pygame.image.load('images\\buttons\\full_screen_btn.png').convert_alpha()

left_ball_img = pygame.image.load('images\\game_background1\\starters\\left_ball.png').convert_alpha()
center_ball_img = pygame.image.load('images\\game_background1\\starters\\center_ball.png').convert_alpha()
right_ball_img = pygame.image.load('images\\game_background1\\starters\\right_ball.png').convert_alpha()


#pokemon types images from spritesheet
types_img_1 = pygame.image.load(r'images\type_icons\types.png').convert_alpha()
types_img_2 = pygame.image.load(r'images\type_icons\type_icons.png').convert_alpha()
types_img_2 = pygame.transform.scale(types_img_2,(800,200))
icon_img_dict = {'bug' : [(3,0),(2,60)] , 'dark' : [(90,0),(805,105)] , 'dragon' : [(180,0),(605,105)] , 'electric' : [(270,0),(2,105)]\
                 , 'fairy' : [(360,0),(1006,105)], 'fight' : [(450,0),(203,15)] , 'fire' : [(540,0),(605,60)],'fly' : [(630,0),(403,15)]\
                 , 'steel' : [(720,0),(403,15)] , 'rock' : [(720,100),(1006,15)] , 'psychic' : [(630,100),(203,15)] , 'poison': [(540,100),(605,15)]\
                 , 'normal': [(450,100),(2,15)], 'ice': [(360,100),(403,105)],'ground' : [(270,100),(805,15)], 'grass' : [(180,100),(1006,60)]\
                 , 'ghost' : [(90,100),(203,60)], 'water' : [(0,100),(805,60)]}


###############################################################################################
###graphic on tm rect in tm party
tm_images_lst = []
for i in range(8):
    img = pygame.image.load(f'images\\game_background1\\tm_graphic\\{i}.png').convert_alpha()
    tm_images_lst.append(img)
pysical_tm_img, special_tm_img, status_tm_img, energy_tm_img, reg_tm_img, range_tm_img, trash_del_tm_img, trainer_box_img = \
tm_images_lst[0], tm_images_lst[1], tm_images_lst[2] \
    , tm_images_lst[3], tm_images_lst[4], tm_images_lst[5] \
    , tm_images_lst[6], tm_images_lst[7]
trash_del_tm_img_rect = trash_del_tm_img.get_rect()
# for tm lst trainer
trash_del_tm_img2 = pygame.transform.scale(trash_del_tm_img, (30, 20))



# trainer window size
down_rect_trainer = pygame.Rect(760, 310, 40, 40)
up_rect_trainer = pygame.Rect(760, 260, 40, 40)
trainer_box_img = pygame.transform.scale(trainer_box_img, (450, 400))
# trainer_box_button_img = pygame.transform.scale(trainer_box_img,(50,40))

###############################################################################3333

pokemon_party_bg_img = pygame.image.load('images\\game_background1\\pokemon_party_bg.png').convert_alpha()
pokemon_party_img = pygame.image.load('images\\buttons\\pokemon_party_btn.png').convert_alpha()
pokemon_in_party_img = pygame.image.load('images\\game_background1\\pokemon_in_party_btn.png').convert_alpha()

# pause menue

play_img = pygame.image.load('images\\buttons\\play_btn.png').convert_alpha()
save_img = pygame.image.load('images\\buttons\\save_btn.png').convert_alpha()
settings_img = pygame.image.load('images\\buttons\\settings_btn.png').convert_alpha()
exit2_img = pygame.image.load('images\\buttons\\exit2_btn.png').convert_alpha()
# game images
# BACKGROUNDS IMAGES
pine1_img = pygame.image.load('images\\game_background1\\bg\\pine1.png').convert_alpha()
pine2_img = pygame.image.load('images\\game_background1\\bg\\pine2.png').convert_alpha()
mountain_img = pygame.image.load('images\\game_background1\\bg\\mountain.png').convert_alpha()
sky_img = pygame.image.load('images\\game_background1\\bg\\sky_cloud.png').convert_alpha()
forest_img = pygame.image.load('images\\game_background1\\bg\\forest.png').convert_alpha()
forest_img = pygame.transform.scale(forest_img, (1400, SCREEN_HEIGHT))
ocean_img = pygame.image.load('images\\game_background1\\bg\\ocean.png').convert_alpha()
ocean_img = pygame.transform.scale(ocean_img, (1400, SCREEN_HEIGHT))

snow_img = pygame.image.load('images\\game_background1\\bg\\snow.png').convert_alpha()
snow_img = pygame.transform.scale(snow_img, (1376, 420))
sky_img2 = pygame.image.load('images\\game_background1\\bg\\sky_cloud_snow.png').convert_alpha()
# load tiles in list
img_list = []
for x in range(len(os.listdir('images\\game_background1\\tiles'))):
    img = pygame.image.load(f'images\\game_background1\\tiles\\{x}.png')
    ##    if x == 30:#exit group
    ##        img = pygame.transform.scale(img,(TILE_SIZE*6,TILE_SIZE*5))
    if x == 31:  # tree
        img = pygame.transform.scale(img, (TILE_SIZE * 5, TILE_SIZE * 7))
    if x not in [30, 31]:
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    img_list.append(img)
for x in range(len(os.listdir('images\\game_background1\\pokemon'))):
    img = pygame.image.load(f'images\\game_background1\\pokemon\\{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
    enemy_collection[1 + x] = lst_251[1 + x]

bullet_img = pygame.image.load(img_directoriy + r'\TM\bullet_seed.png').convert_alpha()
thundershock_img = pygame.image.load(img_directoriy + r'\TM\thundershock.png').convert_alpha()
speed_img = pygame.image.load(img_directoriy + r'\TM\speed.png').convert_alpha()
##paralyze_img = pygame.image.load(img_directoriy + 'TM\\paralyze.png').convert_alpha()


# pick up itemes
health_img_berry = pygame.image.load('images\\collecting items\\hp1.png').convert_alpha()
potion_img = pygame.image.load('images\\collecting items\\hp2.png').convert_alpha()
speed_img_berry = pygame.image.load('images\\collecting items\\speed.png').convert_alpha()
spa_img_berry = pygame.image.load('images\\collecting items\\spa.png').convert_alpha()
spd_img_berry = pygame.image.load('images\\collecting items\\spd.png').convert_alpha()
# grenade_img_berry = pygame.image.load('images\\collecting items\\pinap.png').convert_alpha()
atk_img_berry = pygame.image.load('images\\collecting items\\atk.png').convert_alpha()
def_img_berry = pygame.image.load('images\\collecting items\\deff.png').convert_alpha()
energy_img_berry = pygame.image.load('images\\collecting items\\energy.png').convert_alpha()
exp_img_berry = pygame.image.load('images\\collecting items\\exp.png').convert_alpha()
exp2_img_berry = pygame.image.load('images\\collecting items\\exp2.png').convert_alpha()
tm_in_map_img = pygame.image.load('images\\collecting items\\tm.png').convert_alpha()
# potion_img = pygame.image.load('images\\buttons\\potion.png').convert_alpha()
pokeball_img = pygame.image.load('images\\buttons\\pokeball.png').convert_alpha()

#game-style
#wether and game view style
style_1 = (sky_img, mountain_img, pine1_img, pine2_img)  # v
style_2 = (forest_img, None, None, None)  # v
style_3 = (ocean_img, None, None, None)  # V
style_winter1 = (sky_img2, None, None, snow_img)  # V
style_5 = (sky_img, None, pine1_img, pine2_img)  # V
style_6 = (sky_img, mountain_img, pine1_img, pine2_img)
bg_images_lvl = {1: style_1, 2: style_2, 3: style_3, 4: style_winter1, 5: style_5, 6: style_6}
snowFall = []
for i in range(100):
    x_cord_snow = random.randrange(0, SCREEN_WIDTH)
    y_cord_snow = random.randrange(0, SCREEN_HEIGHT)
    snowFall.append([x_cord_snow, y_cord_snow])


item_boxes = {
    'HEALTH': health_img_berry,
    'HEALTH2': potion_img,
    'SPEED': speed_img_berry,
    'SPA': spa_img_berry,
    'SPD': spd_img_berry,
    'ATK': atk_img_berry,
    'DEFF': def_img_berry,
    'ENERGY': energy_img_berry,
    'EXP': exp_img_berry,
    'EXP2': exp2_img_berry,
    'POKEBALL': pokeball_img,
    'TM': tm_in_map_img

}