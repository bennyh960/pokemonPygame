# LEVEL EDITOR

import pygame
import button
import csv
import os


pygame.init()


clock = pygame.time.Clock()
FPS = 60


#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 580
LOWER_MARGIN = 100
SIDE_MARGIN = 300


screen = pygame.display.set_mode((SCREEN_WIDTH+SIDE_MARGIN ,SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

img_dir = 'C:\\Users\\Hassan\\AppData\\Local\\Programs\\Python\\Python39\\פייתון למתחילים\\images\\game_background1\\bg'

#define game variable

ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT// ROWS
TILE_TYPES =  len(os.listdir('images\\game_background1\\tiles')) + len(os.listdir('images\\game_background1\\pokemon')) #48
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


#define error massage:
load_error = False
temp_time = 50
are_u_sure = False
#load background images

pine1_img = pygame.image.load('images\\game_background1\\bg\\pine1.png').convert_alpha()
pine2_img = pygame.image.load('images\\game_background1\\bg\\pine2.png').convert_alpha()
mountain_img = pygame.image.load('images\\game_background1\\bg\\mountain.png').convert_alpha()
sky_img = pygame.image.load('images\\game_background1\\bg\\sky_cloud.png').convert_alpha()

#store all tile images from folder in a general list "img_list"
img_list = []
for x in range(len(os.listdir('images\\game_background1\\tiles'))):
    img = pygame.image.load(f'images\\game_background1\\tiles\\{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE,TILE_SIZE))
    img_list.append(img)

for x in range(len(os.listdir('images\\game_background1\\pokemon'))):
    img = pygame.image.load(f'images\\game_background1\\pokemon\\{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE,TILE_SIZE))
    img_list.append(img)

#load save and load buttons and next and back btn
save_img = pygame.image.load('images\\game_background1\\save_btn.png').convert_alpha()
load_img = pygame.image.load('images\\game_background1\\load_btn.png').convert_alpha()
restart_img = pygame.image.load('images\\game_background1\\restart_btn.png').convert_alpha()
next_img = pygame.image.load('images\\game_background1\\next_btn.png').convert_alpha()
back_img = pygame.image.load('images\\game_background1\\back_btn.png').convert_alpha()
no_img = pygame.image.load('images\\game_background1\\no_btn.png').convert_alpha()
yes_img = pygame.image.load('images\\game_background1\\yes_btn.png').convert_alpha()

#define colors
GREEN = (144,201,125)
WHITE = (255,255,255)
RED = (200,25,25)
BLACK = (20,25,25)


#create empty tile list to represent the world data 
world_data = []
#feed the list as nested list with [16:rows][150:column] when each index start with -1
for row in range(ROWS+1):
    r = [-1] * MAX_COLS # -1 represent empty tile in grid
    world_data.append(r)

#create ground in that list. 
for tile in range(0,MAX_COLS):
    world_data[ROWS -1][tile] = 0
    world_data[ROWS][tile] = 4

world_reset = world_data

# print to screen
font = pygame.font.SysFont('Futura',30)
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


#create function for drawing background
# make the screen width very wide by using for loop (we can use more than 4 as in here but its important for next while we use 150 columns its dervied from that
def draw_bg():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img,((x * width) - scroll * 0.5 ,0))
        screen.blit(mountain_img, ((x * width)- scroll * 0.6 ,SCREEN_HEIGHT - mountain_img.get_height() - 100))
        screen.blit(pine1_img, ((x * width) - scroll * 0.7 ,SCREEN_HEIGHT - pine1_img.get_height() + 50))
        screen.blit(pine2_img, ((x * width) - scroll * 0.8,SCREEN_HEIGHT - pine2_img.get_height() + 200))
    #print(scroll)
    pygame.draw.rect(screen,GREEN,(0,SCREEN_HEIGHT-(LOWER_MARGIN//2)+20,SCREEN_WIDTH,SCREEN_HEIGHT))

#draw grid
def draw_grid():
    for c in range(MAX_COLS + 1 ):
        #vertical 
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE-scroll, 0),(c * TILE_SIZE-scroll, SCREEN_HEIGHT-20))
    for c in range(ROWS + 1 ):
        #horizontal 
        pygame.draw.line(screen, WHITE, (0,c * TILE_SIZE),(SCREEN_WIDTH,c * TILE_SIZE))



#function for draw world tiles
def draw_world():
    for y,row in enumerate(world_data): # y is index according enumerate and its equal to rows index, row is the internal list represent col 
        for x,tile in enumerate(row): # tile represent each "square in the grid" (each index in row,col)
            if tile >= 0:
                screen.blit(img_list[tile],(x*TILE_SIZE-scroll,y*TILE_SIZE))
    


#create buttons from button import (seperate lecture for that)
# generally , button takes x,y,image, scale and return true/false
save_button = button.Button(200 + (SCREEN_WIDTH - SIDE_MARGIN)//2 ,SCREEN_HEIGHT +25 ,save_img,0.7,0.7)
load_button = button.Button(300 + (SCREEN_WIDTH-SIDE_MARGIN)//2 ,SCREEN_HEIGHT + 25 ,load_img,0.7,0.7)
restart_button = button.Button(400 + (SCREEN_WIDTH-SIDE_MARGIN)//2 ,SCREEN_HEIGHT + 25 ,restart_img,0.26,0.26)

next_button = button.Button(SCREEN_WIDTH + 220, 10 , next_img,0.7,0.7)
pre_button = button.Button(SCREEN_WIDTH + 10, 10 , back_img,0.7,0.7)



no_button = button.Button(SCREEN_WIDTH//3 + 30,SCREEN_HEIGHT//3 + 100 ,no_img,1,1)
yes_button = button.Button(SCREEN_WIDTH//3 + 30 + 4*TILE_SIZE,SCREEN_HEIGHT//3 + 100 ,yes_img,1,1)

# make a button list (for tiles images)
# reminder : Button class take ( x, y,image,scale)
button_list = []
button_col = 0
button_row = 0
counter_tile_page = 0
###arreange colmon and rows of buttons on the screen (in this screen we can only 3 column of 7 rows ,max image is 23 = Load more button)

##for j in range(TILE_TYPES//24): # 24 is the num of images i choose for tile page
##    button_col = 0
##    button_row = 0
for i in range(len(img_list)):
    if counter_tile_page >= 24: # 24 = 3 column * 8 rows in margin icons
        button_col = 0
        button_row = 0
        counter_tile_page = 0
        
    counter_tile_page += 1
    tile_button = button.Button(SCREEN_WIDTH + (75* button_col) +50, 75 * button_row + 50 , img_list[i],1,1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0
        
# print(button_list)
# >> list with class of tile_button (when tile button is instance of class. like mew2 is instance of pokemon class) 

#this is for loading more tiles in the margin screen
#button_list[start_page:next_page]
start_page = 0
next_page = 24
page = 24

run = True
while run:

    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'LEVEL: {level}',font,WHITE,10,SCREEN_HEIGHT - LOWER_MARGIN + 130)
    draw_text('Press UP or Down to change Level',font,WHITE,10,SCREEN_HEIGHT - LOWER_MARGIN + 160)
    if load_error:
        pygame.draw.rect(screen,GREEN,(10,SCREEN_HEIGHT - LOWER_MARGIN + 160,338,SCREEN_HEIGHT - LOWER_MARGIN + 220))
        draw_text(f'Level#{level} not created yet.',font,RED,10,SCREEN_HEIGHT - LOWER_MARGIN + 160)
        temp_time -= 1
        if load_error_start - pygame.time.get_ticks()/1000 > temp_time:
           load_error = False
           load_error_start = 0
           temp_time = 50


    #SAVE LEVEL (with my add of are u sure massage)
    if save_button.draw(screen):
        are_u_sure = True

    if are_u_sure:
        pygame.draw.rect(screen,GREEN,(SCREEN_WIDTH//3,SCREEN_HEIGHT//3,SCREEN_WIDTH//3,SCREEN_HEIGHT//3))
        pygame.draw.rect(screen,BLACK,(SCREEN_WIDTH//3,SCREEN_HEIGHT//3,SCREEN_WIDTH//3,SCREEN_HEIGHT//3),2)
        draw_text('Are you sure?',font,WHITE,SCREEN_WIDTH//3+60,SCREEN_HEIGHT//3 + 40)
        if yes_button.draw(screen):
            with open(f'levels_csv\\level#{level}_data.csv','w',newline ='')as csvfile:
                writer = csv.writer(csvfile,delimiter = ',')
                for row in world_data:
                    writer.writerow(row)
            are_u_sure = False
        if no_button.draw(screen):
            are_u_sure = False




    if load_button.draw(screen):
    #load in level data
        #if f'level#{level}_data.csv' in os.listdir('C:\\Users\\Hassan\\AppData\\Local\\Programs\\Python\\Python39\\פייתון למתחילים\\pygame projects\\pygame2\\youtube scrolling\\levels_csv'):
        if f'level#{level}_data.csv' in os.listdir(
            r'C:\Users\benny\Desktop\Python39\פייתון למתחילים\pygame projects\pygame2\youtube scrolling\levels_csv'):

        #rest scroll back to start of level
            scroll = 0
            with open(f'levels_csv\\level#{level}_data.csv',newline ='')as csvfile:
                reader = csv.reader(csvfile,delimiter = ',')
                for x,row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            load_error = False

        else:
            load_error = True
            load_error_start = pygame.time.get_ticks()/1000
            #draw_text(f'Level#{level} not created yet.',font,RED,10,SCREEN_HEIGHT - LOWER_MARGIN + 160)
            #pygame.draw.rect(screen,GREEN,(10,SCREEN_HEIGHT - LOWER_MARGIN + 160,338,SCREEN_HEIGHT - LOWER_MARGIN + 220))
            print(f'Level#{level} not created yet.')

    if restart_button.draw(screen):
        world_data = world_reset
        for x,row in enumerate(world_data[0:-1]):
                    for y, tile in enumerate(row):
                        world_data[x][y] = -1







    #draw tile panel and tiles
    pygame.draw.rect(screen,GREEN,(SCREEN_WIDTH,0,SIDE_MARGIN,LOWER_MARGIN+SCREEN_HEIGHT))
    #pygame.draw.rect(screen,RED,(1.5*SCREEN_WIDTH-scroll,0,SIDE_MARGIN-20,LOWER_MARGIN))
    draw_text(f'Page#{int(next_page/page)}',font,WHITE,SCREEN_WIDTH+100,10)

    if next_button.draw(screen) and start_page >=0:
        start_page += page
        next_page += page


    if pre_button.draw(screen) and start_page > 0:
        start_page -= page
        next_page -= page

    #print(start_page)


    #curent_button_lst = button_list[start_page:next_page]

    #choose a tile
    # reminder: button list is list with many instances of Button class
    # the enumerate give each instance an index(button_count) when i is the current instance.
    # all the instance got draw methode (see button file)
    # so - if i.draw(screen) is True(when i click on specifice tile) it will draw it on screen and define the current tile
    # current tile is for highlithe the current chosen tile with rect and for more condition (its the real index in world data)
    button_count = 0
    for button_count ,i in enumerate(button_list[start_page:next_page]) :
        if i.draw(screen):
            current_tile = button_count + start_page


    #highlite the selected tile * i already did that in button file but i want practice here
    pygame.draw.rect(screen,RED,button_list[current_tile].rect,3)


    #scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and (scroll < MAX_COLS * TILE_SIZE - SCREEN_WIDTH):
        scroll += 5 * scroll_speed

    #add new tiles to screen
    pos = pygame.mouse.get_pos()
    x = (pos[0] +scroll)// TILE_SIZE
    y = pos[1]//TILE_SIZE

    #check that coordinates are within tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        #x,y = columns and rows
        if pygame.mouse.get_pressed()[0]:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile

        if pygame.mouse.get_pressed()[2]:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1






    pygame.display.update()

pygame.quit()
