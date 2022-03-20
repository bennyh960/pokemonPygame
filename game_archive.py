from GameVariables import *
import random
import csv
import button
import SETTINGS
import pygame



screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Benny's pokemon")

#pygame variabels and events
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT,1000)
pygame.time.set_timer(pygame.USEREVENT+2,100)


def get_image(sheet, pokemon_type, width, height, scalex,
              scaley):  # this function called in pokemoninparty page and maybe in menu draw
    framex, framey = pokemon_type
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (framex, framey, width, height))

    if scalex is not None:
        image = pygame.transform.scale(image, (scalex, scaley))
    image.set_colorkey((0, 0, 0))

    return image


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_multyline_text(surface, text, word_pos, font, color, max_width, max_height, rect_pos=None,
                        button_rect_color=None, text2=None):
    ##    x_fixed , y_fixed = s
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    # max_width , max_height = 200,100
    # word_pos = (500,10)
    a, b = word_pos
    # words_size_total = []
    for line in words:
        for word in line:
            # print(word)
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if a + word_width >= max_width + word_pos[0]:
                # print(max_width , word_width , max_width > word_width)
                a = word_pos[0]  # reset a
                b += word_height  # start new row
            screen.blit(word_surface, (a, b))
            a += word_width + space
        a = word_pos[0]  # reset a
        b += word_height  # start on new row


    if rect_pos is not None:
        # rect_with_color = (200,200,200,100)
        fixed_x, fixed_y = rect_pos  # fixed position between screen and surface in screen

        rect_color_big = pygame.Rect(word_pos[0] - 20 - fixed_x, word_pos[1] - 20 - fixed_y, max_width + 20,
                                     b + 20 - word_pos[1])
        # print(rect_color_big.topleft)
        if button_rect_color is not None:
            rect_color_big.h = b - word_pos[1] + 60

        pygame.draw.rect(surface, (200, 200, 200, 60), (rect_color_big), 0, 2, 2, 2, 2)
        pygame.draw.rect(surface, (255, 188, 0), rect_color_big, 2, 2, 2, 2, 2)

        if button_rect_color is not None:
            left_rect_color_small = pygame.Rect(rect_color_big.x + 10 + fixed_x, fixed_y + rect_color_big.bottom - 35,
                                                50, 28)
            right_rect_color_small = pygame.Rect(rect_color_big.right - 60 + fixed_x,
                                                 fixed_y + rect_color_big.bottom - 35, 50, 28)

            text_left = font.render(text2[0], True, color)
            text_right = font.render(text2[1], True, color)
            text_left_rect = text_left.get_rect(center=left_rect_color_small.center)
            text_right_rect = text_right.get_rect(center=right_rect_color_small.center)

            pygame.draw.rect(screen, button_rect_color, left_rect_color_small, 0, 2, 2, 2, 2)
            pygame.draw.rect(screen, (255, 188, 0), left_rect_color_small, 2, 2, 2, 2, 2)
            pygame.draw.rect(screen, button_rect_color, right_rect_color_small, 0, 2, 2, 2, 2)
            pygame.draw.rect(screen, (255, 188, 0), right_rect_color_small, 2, 2, 2, 2, 2)

            screen.blit(text_left, text_left_rect)
            screen.blit(text_right, text_right_rect)
            return left_rect_color_small, right_rect_color_small


def Music_stop():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()


def Music_start(bg_music):
    pygame.mixer.music.load(f'audio\\game music\\{bg_music}.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)


##_currently_playing_song = None

##def Game_musics():
##    global _currently_playing_song, BG_MUSIC
##    next_song = random.choice(BG_MUSIC[2:])
##
##    while next_song == _currently_playing_song:
##        next_song = random.choice(BG_MUSIC[2:])
##    _currently_playing_song = next_song
##    pygame.mixer.music.load(f'audio\\game music\\{next_song}.mp3')
##    pygame.mixer.music.play()

current_list = []


def Game_musics():
    global current_list
    if not current_list:
        current_list = BG_MUSIC[2:]
        random.shuffle(current_list)

    song = current_list[0]
    current_list.pop(0)
    pygame.mixer.music.load(f'audio\\game music\\{song}.mp3')
    pygame.mixer.music.play()

def draw_bg():
    # screen.fill(BG)
    #print(bg_images_lvl[level])
    img1, img2, img3, img4 = bg_images_lvl[level]

    #img1, img2, img3, img4 = style_winter1
    screen_w = pygame.display.get_surface().get_size()[0]
    screen.fill(BG)
    width = img1.get_width()
    for x in range(5):  # anynumber can be
        screen.blit(img1, ((width * x) - bg_scroll * 0.5, 0))
        if img2 is not None:
            screen.blit(img2, ((width * x) - bg_scroll * 0.6, img1.get_height() - 300))
        if img3 is not None:
            if img2 is not None:
                img3_y = img2.get_height()
            else:
                img3_y = 250
            screen.blit(img3, ((width * x) - bg_scroll * 0.7, img3_y + img1.get_height() - 400))
        if img4 is not None:
            screen.blit(img4, ((width * x) - bg_scroll * 0.8, SCREEN_HEIGHT - img4.get_height()))

    # winter effect if style is winter style
    if bg_images_lvl[level] == style_winter1:
        for i in range(len(snowFall)):
            if i % 2 == 0:
                size = 2
            elif i % 3:
                size = 4
            else:
                size = 3
            pygame.draw.circle(screen, (random.randint(235, 255), random.randint(235, 255), random.randint(235, 255)),
                               snowFall[i], size)

            snowFall[i][1] += 1
            # snowFall[i][0] += 0.3 + screen_scroll/10
            if snowFall[i][1] > SCREEN_HEIGHT:
                snowFall[i][1] = 0
                snowFall[i][0] = random.randrange(-100, SCREEN_WIDTH)


def draw_menue():
    pos = pygame.mouse.get_pos()
    width_rect = 550
    height_rect = 1.5 * TILE_SIZE
    x_cord, y_cord = pygame.display.get_surface().get_size()
    menue_rect = pygame.Rect(x_cord // 2 + screen_scroll - (width_rect // 2), y_cord - height_rect - 25, width_rect,
                             height_rect)
    # small_rect = pygame.Rect(pygame.display.get_surface().get_size()[0]//2 + screen_scroll -40,0,40,5)

    menue_color = (0, 100, 250, 128)

    size = width, height = (pygame.display.get_surface().get_size())
    # size = width, height = (800,600)
    my_image = pygame.Surface(size, pygame.SRCALPHA)

    # Btn and moves obj
    potion_btn = button.Button(menue_rect.right + 10, menue_rect.y, potion_img, 0.2, 0.2)
    pokeball_btn = button.Button(menue_rect.right + 10, menue_rect.y + 25, pokeball_img, 0.2, 0.2)
    pokemon_party_btn = button.Button(menue_rect.left + 10, menue_rect.y + 10, pokemon_party_img, 0.3, 0.3)

    for tm_lvl in player.tm_lvl_dict.keys():
        if player.lvl >= tm_lvl and player.tm_lvl_dict[tm_lvl] not in player.TM_LST and len(player.TM_LST) <= 8:
            player.TM_LST.append(player.tm_lvl_dict[tm_lvl])

        if player.lvl == tm_lvl and player.exp < 150:
            player.exp += 1
            # put sound - dont forget connect that sound to settings .and notice user
            text_new_tm = f'{player.char_type} learned {player.tm_lvl_dict[tm_lvl].text}'
            if player.exp == 1:
                print(text_new_tm)

            if len(player.TM_LST) == 8 and player.exp > 140:
                # need to add sound for reminder
                pygame.draw.rect(screen, (20, 20, 20), (0, 0, SCREEN_WIDTH, 35), 0, 4)
                pygame.draw.rect(screen, (200, 200, 200), (2, 2, SCREEN_WIDTH - 2, 33), 2, 4)
                pygame.draw.rect(screen, (250, 250, 250), (6, 6, SCREEN_WIDTH - 6, 28), 1, 4)
                text_new_tm = f'Reminder: {player.char_type} Cant remmber more then 8 moves.'
                if player.exp > 148:
                    pygame.time.delay(3000)

            text_new_tm = font.render(text_new_tm, True, WHITE)
            screen.blit(text_new_tm, (int((width / 2) - (text_new_tm.get_width() / 2)), 10))

    # if "t" keyboard or mouse colid : user will see menue of tm , pokebal,potion and party btn . Note: all trainer command got trough this command beside moves
    if pos[1] > menue_rect.y - 10 or draw_menu_keyboard:
        pygame.draw.rect(my_image, menue_color, menue_rect, 0, 0, 10, 10, 0)
        if pokemon_party_btn.draw(screen):
            pause_from_pokemon_party_btn = True
            pause_activate = True
            return pause_from_pokemon_party_btn, pause_activate
        # use_item_btn(menue_rect)
        if potion_btn.draw(screen) and player.potion > 0:
            if player.health < player.max_health:
                player.health += 10
            else:
                player.health = player.max_health

            player.potion -= 1

        draw_text("X", font_2, WHITE, menue_rect.right + 40, menue_rect.y + 7)
        draw_text(f"{player.potion}", font1, WHITE, menue_rect.right + 55, menue_rect.y)

        if (pokeball_btn.draw(
                screen) or pokeball_throw_keyboard) and player.pokeball > 0 and player.pokeball_thrown == False:
            pokeball = POKEBALL(player.rect.centerx - int(player.direction * player.rect.size[0] * 0.5),
                                player.rect.top, player.direction)
            pokeball_group.add(pokeball)
            # pokeball_thrown = True
            player.pokeball -= 1
            player.pokeball_thrown = True

        draw_text("X", font_2, WHITE, menue_rect.right + 40, menue_rect.y + 37)
        draw_text(f"{player.pokeball}", font1, WHITE, menue_rect.right + 55, menue_rect.y + 30)

        # define rect where tm1 and other tm's will be draw according this rect
        rect_tm1 = pygame.Rect(menue_rect.x + 65, menue_rect.y + 5, 100, 65)

        for i, lvl in enumerate(player.TM_LST[:4]):
            rect_tm1.x = menue_rect.x + 65 + (i * 110)
            tm_icon = get_image(types_img_2, icon_img_dict[lvl.type][0], 90, 90, 20, 20)
            screen.blit(tm_icon, (menue_rect.x + 68 + (i * 110), rect_tm1.y + 3))
            if lvl.category == "special":
                img_1 = special_tm_img
            elif lvl.category == "pysical":
                img_1 = pysical_tm_img
            else:
                img_1 = status_tm_img

            player.TM_LST[i].draw(rect_tm1, my_image, player, img_1)
            if rect_tm1.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                player.TM_LST[i].clicked = True
                print(id(player.TM_LST))
                # player.shoot()

    screen.blit(my_image, (0, 0))
    return False, False


# function to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    item_box_group.empty()
    water_group.empty()
    decoration_group.empty()
    exit_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS + 1):
        r = [-1] * COLS
        data.append(r)
    return data


# Formula to calculate the exp for next lvl
def lvl_up_pts(n):
    return n * (100 + n ** 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, char, x, y, hp, scale, speed, fake_speed, ammo, grenades, typ1, typ2, energy, atk,
                 deff, spa, spd, tm_lvl_dict):  # ,x_states,y_states):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.char = char
        self.shoot_cooldown = 20
        self.health = hp
        self.max_health = self.health
        self.speed = speed
        self.start_speed = speed

        self.ammo = ammo  # energy
        self.start_ammo = ammo
        self.grenades = grenades
        self.direction = 1
        self.jump = False
        self.vel_y = 0  # velocity in y direction -for jumping
        self.in_air = True  # for jump animation see part3 youtube 39:10
        self.flip = False
        self.animation_list = []
        # self.animation_list_states = [] #idle and run only without scaling
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # self.update_energy_time = 0
        self.altitude = 0
        self.altitude_damage = False
        # create ai specified self variabels
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 550, 20)  # the ai vision rect
        self.idling = False
        self.idling_counter = 0

        self.typ1 = typ1
        self.typ2 = typ2
        self.max_energy = energy
        self.energy = energy

        self.atk = atk
        self.deff = deff
        self.spa = spa
        self.spd = spd
        self.fake_speed = fake_speed

        self.start_atk = atk
        self.start_deff = deff
        self.start_spa = spa
        self.start_spd = spd
        self.max_fake_speed = fake_speed
        self.exp = 0
        self.lvl = 5
        self.reg = 1

        self.potion = 0
        self.pokeball = 6
        self.stop_draw = False
        self.in_pokeball = False
        self.pokeball_thrown = False

        self.gender = random.choice(['female', 'male', 'male'])

        self.collidWithPokeball = 0

        animation_types = ['idle', 'run', 'jump', 'death', 'atk']  # name of folders contain images for frames

        for animation in animation_types:
            # count numbers of files in folder
            num_of_frames = os.listdir('images\\pokemon_images\\' + self.char_type + '\\' + animation)
            for png in num_of_frames:  # my extra for me to ignore files that not png such archive folder
                if 'png' not in png:
                    num_of_frames.remove(png)
            # print(num_of_frames)
            temp_list = []
            for i in range(len(num_of_frames)):
                img = pygame.image.load(
                    'images\\pokemon_images\\' + self.char_type + f'\\{animation}\\{i}.png').convert_alpha()  # added from part4 only "convert_alpha()"
                # img = pygame.transform.scale(img,(int(img.get_width()*0.2),int(img.get_height()*0.2))) # image according screen scale
                img = pygame.transform.scale(img, (
                int(TILE_SIZE * scale), int(TILE_SIZE * scale)))  # image according screen scale
                temp_list.append(img)
            self.animation_list.append(temp_list)

        ##        for i in range(3):
        ##            img_for_states = pygame.image.load('images\\pokemon_images\\' + self.char_type + f'\\idle\\{i}.png').convert_alpha()
        ##            self.animation_list_states.append(img_for_states)

        self.img = self.animation_list[self.action][self.index]
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

        '''
        instance to add
        ,lvl_100_states
        '''
        # Party members photos
        self.img_for_states = pygame.image.load(
            'images\\pokemon_images\\' + self.char_type + '\\idle\\0.png').convert_alpha()  # main img
        self.char_img_s = pygame.transform.scale(self.img_for_states, (45, 45))  # for left side small photo
        self.char_img_l = pygame.transform.scale(self.img_for_states, (250, 250))  # for center large photo
        self.char_img_l_rect = self.char_img_l.get_rect()
        self.char_img_l_rect.center = (800, 350)
        # party member present in screen
        # self.clicked = False
        self.state_blit = False
        self.index_methode = 0
        # self.lvl_100_states = lvl_100_states if is not None else 100

        self.tm_lvl_dict = tm_lvl_dict
        self.TM_LST = []

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):

        screen_scroll = 0

        dx = 0
        dy = 0
        altitude = 75

        # assign movment variables
        if moving_left and self.rect.left > 0:
            dx = -self.speed
            self.flip = True
            self.direction = 1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = -1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY

        if self.vel_y > 10:
            self.vel_y = 0

        altitude_damage = 0
        dy = self.vel_y
        self.altitude += 1
        if self.altitude > altitude and not pygame.sprite.spritecollide(self, water_group,
                                                                        False) and self.char == 'player' and \
                'fly' not in [self.typ1, self.typ2]:
            self.altitude_damage = True
            altitude_damage = self.altitude - altitude
        else:
            self.altitude_damage = False

        # check for collision
        for tile in world.obstacle_list:
            # x direction

            # if tile[1].colliderect(self.rect.x + dx ,self.rect.y,self.img.get_width(),self.img.get_height()):
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
                if self.char == 'player':
                    wall_bump_fx.play()
            # y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.altitude_damage:
                    self.health -= altitude_damage
                    self.altitude_damage = False
                    print('damaege from falling from hight alltittude', altitude_damage)
                    pygame.draw.rect(screen, RED, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                    if self.char == 'player':
                        falling_fx.play()
                self.altitude = 0

                # check if below the ground , i.e jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    wall_bump_fx.play()
                # check if above the ground i.e falling
                elif self.vel_y >= 0:
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # check for collide with water (if not a water type)
        if pygame.sprite.spritecollide(self, water_group, False) and (self.typ1 != 'water' and self.typ2 != 'water'):
            water_weak = ['fire', 'ground', 'rock']
            if self.typ1 in water_weak or self.typ2 in water_weak:
                water_damage = 1
            else:
                water_damage = 0.2
            if self.energy >= water_damage:
                self.energy -= water_damage * 0.5
            self.health -= water_damage
            jump_water_fx.play()

        # check if fall of screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
            if self.exp > 10 * (level ** 2) / 3:
                self.exp -= 10 * (level ** 2) / 3
            else:
                self.exp = 0

        # check collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False) and len(enemy_group) == 0:
            level_complete = True
            end_lvl_fx.play()
            self.exp += 100 * (level ** 2) / 3

        # update scroll based on player position
        if self.char == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_TRESH and bg_scroll < (
                    world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_TRESH and bg_scroll >= abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20

            bullet = Bullet(self.rect.centerx + (1.5 * self.rect.size[0] * -self.direction), self.rect.centery + 10,
                            self.direction, (self.img.get_width(), self.img.get_height()))
            bullet_group.add(bullet)
            # reduce ammo each shoot
            self.ammo -= 1
            shooting_fx.play()
            self.energy -= 1
            # self.energy -= TM1_TIMER.eng

    def ai(self):  # ,ai_lvl,player_once_lvl):
        # self.lvl = level +  ai_lvl + player_once_lvl #player_once_lvl is a number that arrive at the begining of new lvl

        if self.alive and player.alive:

            for tm_lvl in self.tm_lvl_dict.keys():
                if self.lvl >= tm_lvl and self.tm_lvl_dict[tm_lvl] not in self.TM_LST:
                    self.TM_LST.append(self.tm_lvl_dict[tm_lvl])

            if self.idling == False and random.randint(1, 50) == 10:
                self.idling = True
                self.update_action(0)
                self.idling_counter = 50

            # check if the AI is near the player
            if self.vision.colliderect(player.rect) and random.randint(1, 20) == 10:
                # stop running and face the player
                self.update_action(4)

                # shoot
                # self.shoot()

                # jump
                if player.jump == True and self.in_air == False:  # and random.randint(1,3) == 2:
                    self.vel_y = -11
                    self.in_air = True
                    self.in_air = True

                # apply gravity

                self.vel_y += GRAVITY * 1.1

                if self.vel_y > 10:
                    self.vel_y = 0
                    self.in_air = False
                dy = self.vel_y

                for tile in world.obstacle_list:
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):

                        if self.vel_y < 0:
                            self.vel_y = 0
                            dy = tile[1].bottom - self.rect.top
                            # self.in_air = False

                        # check if above the ground i.e falling
                        elif self.vel_y >= 0:

                            # self.vel_y = 0
                            self.in_air = False
                            # pygame.draw.rect(screen,RED,tile[1])
                            dy = tile[1].top - self.rect.bottom
                self.rect.y += dy
            else:

                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = False
                    else:
                        ai_moving_right = True

                    self.update_action(1)  # 1 : run , 0: idle *dont have run animation yet
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.move_counter += 1

                    # update ai vision (x,y ) as the enemy moves while the width of this rect define in init methode above (for shooting when im in thier sig
                    self.vision.center = (self.rect.centerx + 75 * -self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter < 0:
                        self.idling = False

        else:
            self.max_health += -2  # just for timer
            if self.max_health <= 0:
                player.exp += self.lvl * 20 * (level ** 2) / 3
                self.kill()

        # scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        # update image dpending on current frameddd
        self.img = self.animation_list[self.action][self.index]

        # check if enogh time passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.index += 1
            # reset timer
            self.update_time = pygame.time.get_ticks()
        if self.index == len(self.animation_list[self.action]):
            self.index = 0

    def update_action(self, new_action):
        # check if new action is different from the previews
        if new_action != self.action:
            self.action = new_action
            # updtae animation settings
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def update_energy(self):
        if self.energy < self.max_energy:
            self.energy += self.reg / 10
            if self.energy >= self.max_energy:
                self.energy = self.max_energy

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.index = 1
            self.action = 3

    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)

    def PokemonInParty(self, x, y, lvl_100_states):
        action = False

        # i have img for that but for run time is better to draw
        # screen.blit(pokemon_in_party_img,(x,y-3)) # pokemon_in_party_img :
        pygame.draw.rect(screen, (230, 230, 230), (x, y, 370, 78), 0, 39)

        pos_on_pokemon_rect = pygame.Rect(x, y, 370, 78)

        pos = pygame.mouse.get_pos()

        if pos_on_pokemon_rect.collidepoint(pos):
            pygame.draw.rect(screen, (25, 25, 25), pos_on_pokemon_rect, 0, 39)
            if pygame.mouse.get_pressed()[2]:
                self.state_blit = True

            color = (250, 250, 250)

        else:
            color = (25, 25, 25)
            if pygame.mouse.get_pressed()[2]:
                self.state_blit = False

        health_green = 220 * self.health / self.max_health

        # bliting pok data(hp,gender,lvl etc) the left side of the page
        screen.blit(self.char_img_s, (x + 35, y + 20))
        pygame.draw.line(screen, (255, 10, 0), (x + 85, y + 41), (int(x + 85 + 220), y + 41), 8)
        pygame.draw.line(screen, (68, 255, 0), (x + 85, y + 40), (int(x + 85 + health_green), y + 40), 10)

        name_text = font2_n.render(self.char_type, True, color)
        lv_text = font2_n.render(f"Lv. {self.lvl}", True, color)
        health_text = font2_n.render(f'{int(self.health)}/{self.max_health}', True, color)

        # draw gender
        if self.gender in ['male', 'Male', 'MALE']:
            gender = font5_g.render('\u2642', True, WHITE)  # male
            g_color = (0, 0, 255)
        else:
            gender = font5_g.render(chr(0x2640), True, WHITE)  # female
            g_color = (255, 0, 0)

        gender_rect = gender.get_rect()
        gender_rect.center = (x + 280, y + 23)

        screen.blit(name_text, (x + 85, y + 11))
        screen.blit(lv_text, (x + 285, y + 50))
        screen.blit(health_text, (x + 85, y + 50))

        pygame.draw.circle(screen, g_color, (gender_rect.center), 11)
        screen.blit(gender, gender_rect)

        if self.state_blit:
            # define Trigo
            cos30 = (3 ** 0.5) / 2
            tan30 = (3 ** 0.5) / 3

            # Center of polygone
            cx = 990
            cy = 170

            # polygone variable (x only)
            X = 110

            # affected from x
            V = X / cos30
            Y = -((V ** 2) - (X ** 2)) ** 0.5

            # define colors
            bg_color = (225, 254, 250)
            gray = (229, 229, 229)

            # size = width, height = (surf_WIDTH+300, surf_HEIGHT) pygame.display.get_surface().get_size()
            size = width, height = (pygame.display.get_surface().get_size())
            # size = width, height = (800,600)
            my_image = pygame.Surface(size, pygame.SRCALPHA)  # Creates an empty per-pixel alpha Surface.
            # transperent polygon - actual pokemon states

            screen.blit(self.char_img_l, (850, 330))

            type_icon = get_image(types_img_1, icon_img_dict[self.typ1][1], 200, 44, 100, 30)
            screen.blit(type_icon, (980, 588))

            if self.typ2 != '':
                type2_icon = get_image(types_img_1, icon_img_dict[self.typ2][1], 200, 44, 100, 30)
                screen.blit(type2_icon, (1080, 588))

            methode_lst = [1, 2, 3, 4, 5, 6]
            # define states related to V
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # and change_methode < methode:
                        self.index_methode += 1
                        if self.index_methode > len(methode_lst) - 1:
                            self.index_methode = 0
                    if event.key == pygame.K_DOWN:
                        self.index_methode -= 1
                        if self.index_methode < 0:
                            self.index_methode = len(methode_lst) - 1

                    if event.key == pygame.K_ESCAPE:
                        global pause_activate
                        pause_activate = False

            if methode_lst[self.index_methode] == 2:
                ##self.lvl_100_states[self.hp,self.atk,self.deff,self.spa,self.spd,self.speed,self.energy]
                # comparison to lvl 100
                hp1 = int(V * self.max_health / lvl_100_states[0])
                atk1 = int(X * self.atk / lvl_100_states[1])
                deff1 = int(X * self.deff / lvl_100_states[2])
                spa1 = int(X * self.spa / lvl_100_states[3])
                spd1 = int(X * self.spd / lvl_100_states[4])
                speed1 = int(self.fake_speed * V / (lvl_100_states[8]))

                BLUE = (0, 50, 255, 100)  # transperent color on new surface "my_image"
                COLOR_POLYGONE = BLUE
                states_methode_text = font2_n.render('Normal', True, COLOR_POLYGONE)
                # description_state_text = font2_n.render('Blue: Each state compared to same state in maximum level and power.',True,BLACK)
                text = 'States compared to same maximum state.\nin maximum level and power.\n'

            elif methode_lst[self.index_methode] == 1:
                # comparison to his own avg in lvl 100
                # print(lvl_100_states)
                avg_states = sum(lvl_100_states) // len(lvl_100_states)
                hp1 = int(V * self.max_health / avg_states)
                atk1 = int(X * self.atk / avg_states)
                deff1 = int(X * self.deff / avg_states)
                spa1 = int(X * self.spa / avg_states)
                spd1 = int(X * self.spd / avg_states)
                speed1 = int(self.fake_speed * V / avg_states)

                YELLOW = (240, 250, 40, 100)
                COLOR_POLYGONE = YELLOW
                states_methode_text = font2_n.render('Average', True, COLOR_POLYGONE)
                # description_state_text = font2_n.render('Yellow: All states compared to average states in maximum level and power.',True,BLACK)
                text = 'States compared to average state\nin maximum level and power.\n'

            elif methode_lst[self.index_methode] == 3:
                # comparison to his own max state
                max_state = max(lvl_100_states)
                hp1 = int(V * self.max_health / max_state)
                atk1 = int(X * self.atk / max_state)
                deff1 = int(X * self.deff / max_state)
                spa1 = int(X * self.spa / max_state)
                spd1 = int(X * self.spd / max_state)
                speed1 = int(self.fake_speed * V / max_state)

                GREEN = (0, 225, 70, 100)
                COLOR_POLYGONE = GREEN
                states_methode_text = font2_n.render('Maximum', True, COLOR_POLYGONE)
                text = 'States compared to biggest state\nin maximum level and power.\n'

            elif methode_lst[self.index_methode] == 4 or methode_lst[self.index_methode] == 5:

                state_lst_text = ['HP :', 'Attack :', 'Deffence :', 'Sp.Atk :', 'Sp.Def :', 'Energy :', 'Reg-Eng :',
                                  'Speed :']
                state_lst = [self.max_health, self.atk, self.deff, self.spa, self.spd, self.energy, self.reg,
                             self.fake_speed]
                state_lst_lvl100 = [i for i in lvl_100_states if i > 20]
                # print(state_lst_lvl100)

                # table compared to lvl 100
                if methode_lst[self.index_methode] == 4:
                    # GREEN =
                    COLOR_POLYGONE = (0, 225, 70, 100)

                    lst_to_compare = state_lst_lvl100
                    division_state = max(lvl_100_states)
                    states_methode_text = font2_n.render('Est. level 100', True, COLOR_POLYGONE)
                    text = 'All states in table form.\nCompared to pokemon max state in his max level, with perfect Ev pts each during lvl-up.\n'


                # table compared to 250 num
                elif methode_lst[self.index_methode] == 5:
                    # BLUE = (0, 50, 255, 100)
                    COLOR_POLYGONE = (0, 50, 255, 100)
                    lst_to_compare = state_lst
                    division_state = 250
                    states_methode_text = font2_n.render('Base 250', True, COLOR_POLYGONE)
                    text = 'Base 250 :All current states in table form.\nCompared to 250 pts per state.'

                for i, state in enumerate(state_lst_text):
                    state_text = font2_n.render(state, True, BLACK)
                    screen.blit(state_text, (
                    880 + (font2_n.render('Reg-Eng :', True, BLACK).get_width()) - state_text.get_width(),
                    35 + (i * state_text.get_height())))
                for i, state in enumerate(lst_to_compare):
                    state_text = font2_n.render(str(int(state)), True, BLACK)
                    screen.blit(state_text, (880 + (font2_n.render('Reg-Eng :', True, BLACK).get_width()) + 5,
                                             35 + (i * state_text.get_height())))
                    state_bar_lengh = 200
                    ratio_state = state / division_state
                    if ratio_state > 0.65:
                        rect_state_color = (100, 250, 70)
                    elif ratio_state <= 0.65 and ratio_state > 0.5:
                        rect_state_color = (206, 250, 70)
                    elif ratio_state <= 0.5 and ratio_state > 0.3:
                        rect_state_color = (255, 190, 70)
                    else:
                        rect_state_color = (255, 70, 70)

                    pygame.draw.rect(screen, rect_state_color,
                                     (1005, 42 + (i * state_text.get_height()), int(ratio_state * state_bar_lengh), 15))

            elif methode_lst[self.index_methode] == 6:  # show moves
                COLOR_POLYGONE = (100, 230, 243, 100)

                states_methode_text = font2_n.render('Move Set', True, COLOR_POLYGONE)
                text = 'Pokemon Can remmber up to 8 moves.\nand use only the 4 first moves.\n\nMouse left click for re-ordering.\nDelete move - drag it to trash.\n\nTm information include:\nCategory,Energy,Regeneration and Range.'

                rect_width_TM, rect_hight_TM, space_rect_tm = 330, 70, 5

                # FAKE RECT JUST FOR COLLISION
                tm_rect_grid_lst = []
                for i in range(len(self.TM_LST)):
                    TM_RECT_grid = pygame.Rect(width - rect_width_TM, 67 + (i * (rect_hight_TM + space_rect_tm)),
                                               rect_width_TM - 180, rect_hight_TM - 50)
                    tm_rect_grid_lst.append(TM_RECT_grid)
                    # pygame.draw.rect(screen,(25,25,25),TM_RECT_grid,2,3)

                trash_del_tm_img_rect.topleft = (width // 2 - 15, height - 150)

                my_image.blit(trash_del_tm_img, trash_del_tm_img_rect)

                for i, tm in enumerate(self.TM_LST):
                    TM_RECT_PARTY_PAGE = pygame.Rect(width - rect_width_TM - 90,
                                                     42 + (i * (rect_hight_TM + space_rect_tm)), rect_width_TM,
                                                     rect_hight_TM)

                    if tm.moving_rect == False:
                        tm.rect = TM_RECT_PARTY_PAGE

                    # Re ordering moves
                    if tm.rect.collidepoint(pos) and len(self.TM_LST) > 1:
                        # print(trash_del_tm_img_rect)

                        pygame.draw.rect(screen, (25, 25, 25), tm.rect, 5, 5)
                        # self.clicked = False
                        if pygame.mouse.get_pressed()[0]:
                            tm.moving_rect = True
                            # tm.rect.centery = pos[1]
                            tm.rect.center = pos

                            ##                            if test_del_TM:
                            ##                                print('TM deleted')

                            if i > 0 and tm.rect.colliderect(tm_rect_grid_lst[i - 1]):
                                self.TM_LST[i - 1].rect.centery = tm_rect_grid_lst[i].centery
                                tm.rect.centery = tm_rect_grid_lst[i - 1].centery
                                self.TM_LST[i - 1], self.TM_LST[i] = self.TM_LST[i], self.TM_LST[i - 1]

                            if i < len(self.TM_LST) - 1 and tm.rect.colliderect(tm_rect_grid_lst[i + 1]):
                                self.TM_LST[i + 1].rect.centery = tm_rect_grid_lst[i].centery
                                tm.rect.centery = tm_rect_grid_lst[i + 1].centery
                                self.TM_LST[i + 1], self.TM_LST[i] = self.TM_LST[i], self.TM_LST[i + 1]
                        else:
                            tm.rect.center = tm_rect_grid_lst[i].center

                    if tm.category == "special":
                        img_1 = special_tm_img
                    elif tm.category == "pysical":
                        img_1 = pysical_tm_img
                    else:
                        img_1 = status_tm_img

                    # remoe moe from tm set warning
                    if trash_del_tm_img_rect.collidepoint(tm.rect.center):
                        print(tm.text, 'warning -delete move')
                        tm.RemovedByUser = True
                        warning_del_tm_rect = pygame.Rect(0, 0, 200, 100)
                        warning_del_tm_rect.center = trash_del_tm_img_rect.center
                        pygame.draw.rect(screen, (125, 125, 125, 150), warning_del_tm_rect, 0, 3)
                        pygame.draw.rect(screen, (25, 25, 25, 150), warning_del_tm_rect, 3, 3)

                    if tm.RemovedByUser:
                        warning_del_tm_text = f'{self.char_type} will forget\n            {tm.text}\n      Are you sure?'
                        # draw_multyline_text(screen,warning_del_tm_text,(warning_del_tm_rect.x+10,warning_del_tm_rect.y+20),font,BLACK,warning_del_tm_rect.w-15,warning_del_tm_rect.h-10,(10,30,240,180))
                        no_btn_del_tm, yes_btn_del_tm = draw_multyline_text(my_image, warning_del_tm_text,
                                                                            (0.5 * width - 105, 0.5 * height + 15),
                                                                            font, WHITE \
                                                                            , 210, 85, (0, 5), (30, 30, 30),
                                                                            ['No', 'Yes'])
                        if no_btn_del_tm.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                            tm.RemovedByUser = False
                        if yes_btn_del_tm.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                            # tm.RemovedByUser = False
                            self.TM_LST.remove(tm)
                            self.tm_lvl_dict = {k: v for k, v in self.tm_lvl_dict.items() if v != tm}
                            print(tm.text, 'deleted move')

                    # show tm icon
                    tm_icon = get_image(types_img_2, icon_img_dict[tm.type][0], 90, 90, 38, 38)

                    # draw all data on tm rect
                    tm.draw2(my_image, img_1, energy_tm_img, reg_tm_img, range_tm_img, tm_icon)

                    # tm_icon_rect = tm_icon.get_rect(topleft = (TM_RECT_PARTY_PAGE.x+5,TM_RECT_PARTY_PAGE.centery-8))
                    # screen.blit(tm_icon,(tm_icon_rect))

                    if trainer_box_button.draw(screen):  # trainer.tm_lst:
                        trainer.show_tm_preview = True

                    if trainer.show_tm_preview:
                        trainer.draw_menue()

            if methode_lst[self.index_methode] < 4:
                # drawing
                pygame.draw.polygon(screen, gray, [(cx + X, cy + Y), (cx + X, cy - Y), (cx, cy + V), (cx - X, cy - Y),
                                                   (cx - X, cy + Y), (cx, cy - V)])

                pygame.draw.line(screen, bg_color, (cx + X, cy + Y), (cx - X, cy - Y), 3)
                pygame.draw.line(screen, bg_color, (cx + X, cy - Y), (cx - X, cy + Y), 3)
                pygame.draw.line(screen, bg_color, (cx, cy + V), (cx, cy - V), 3)
                # draw polygone# and states methode
                pygame.draw.polygon(my_image, COLOR_POLYGONE, [(cx, cy - hp1), (cx + atk1, cy - (atk1 * tan30)),
                                                               (cx + deff1, cy + (deff1 * tan30)), (cx, cy + speed1),
                                                               (cx - spa1, cy + (spa1 * tan30)),
                                                               (cx - spd1, cy - (spd1 * tan30))])

                # draw states
                hp1 = font2_n.render('HP', True, BLACK)
                hp2 = font2_n.render(f'{int(self.health)}/{self.max_health}', True, BLACK)
                screen.blit(hp1, (cx - 10, cy - V - 40))
                screen.blit(hp2, (cx - 22, cy - V - 20))
                speed1 = font2_n.render('SPEED', True, BLACK)
                speed2 = font2_n.render(f'{self.fake_speed}', True, BLACK)
                screen.blit(speed1, (cx - 22, cy + V))
                screen.blit(speed2, (cx - 5, cy + V + 20))
                atk_spa1 = font2_n.render('Sp.Atk                                                Attack', True, BLACK)
                atk_spa2 = font2_n.render(
                    f'{int(self.spa)}                                                     {int(self.atk)}', True, BLACK)
                screen.blit(atk_spa1, (cx - X - 60, cy + Y - 30))
                screen.blit(atk_spa2, (cx - X - 40, cy + Y - 10))
                def_spd1 = font2_n.render('Sp.Def                                                Deffence', True, BLACK)
                def_spd2 = font2_n.render(
                    f'{int(self.spd)}                                                     {int(self.deff)}', True,
                    BLACK)
                screen.blit(def_spd1, (cx - X - 60, cy - Y - 30))
                screen.blit(def_spd2, (cx - X - 40, cy - Y - 10))

            # create description of each methode
            description_rect = pygame.Rect(515, 8, states_methode_text.get_width() + 17,
                                           states_methode_text.get_height() + 6)
            screen.blit(states_methode_text, (525, 10))
            pygame.draw.rect(my_image, COLOR_POLYGONE, (description_rect), 0, 2, 2, 2, 2)
            pygame.draw.rect(screen, COLOR_POLYGONE, (description_rect), 2, 2, 2, 2, 2)
            if description_rect.collidepoint(pos):
                draw_multyline_text(my_image, text, (535, 85), font0_0, BLACK, 200, 50, rect_pos=(0, 0))
            screen.blit(my_image, (0, 0))

    def HealthBar(self, a, b, z):  # ,health,max_health,energy,name):
        # update with new health
        # fixed position
        x = a + 10
        y = b + 10

        ratio = self.health / (
            self.max_health if self.max_health != 0 else 100)  # the max HP reduced to null when self.kill apearntly

        if self.max_health < 2:
            print(self.char_type, "Max HP:", self.max_health, "HP:", self.health, "Lvl", self.lvl)

        width = 180

        ##        GREEN1 = (0,255,0)
        ##        GREEN2 = (0,204,0)
        ##        GREEN3 = (0,153,0)
        ##        GREEN4 = (230,255,230)
        ##        GRAY = (110,110,110)
        ##        WHITE = (255,255,255)
        ##        BLACK = (25,25,25)

        if self.char == "enemy":

            pygame.draw.rect(screen, (110, 110, 110), (x - 40, y + z, x + 20, 14), 0, 4)
            HP_text = font0_0.render(f'{int(100 * ratio)}%', True, WHITE)
            # HP_text = font0_0.render(str(self.max_health),True,WHITE)
            screen.blit(HP_text, (x - 30, y - 1 + z))
            # print(self.max_health)
        else:
            pygame.draw.rect(screen, (110, 110, 110), (x + width - 30, y + z, x + 55, 14), 0, 4)
            HP_text = font0_0.render(f'{int(100 * ratio)}%', True, WHITE)
            screen.blit(HP_text, (x + width + 8, y - 1))

            distance = 35
            energy_ratio = self.energy / self.max_energy

            pygame.draw.rect(screen, (110, 110, 110), (x + width - 30, y + distance, x + 55, 14), 0, 4)
            energy_text = font0_0.render(f'{int(100 * energy_ratio)}%', True, WHITE)
            # energy_text = font0_0.render(str(self.character.energy),True,WHITE)
            screen.blit(energy_text, (x + width + 8, distance + y - 1))

            pygame.draw.rect(screen, (150, 150, 255), (x, y + distance, width, 15), 0, 4)  # general bar rect
            # energy bar rects with 3 colors

            pygame.draw.rect(screen, (0, 0, 153), (x, y + distance, width * energy_ratio, 15), 0, 4)
            pygame.draw.rect(screen, (0, 0, 204), (x, y + distance, width * energy_ratio, 10), 0, 4)
            pygame.draw.rect(screen, (0, 0, 255), (x, y + distance, width * energy_ratio, 8), 0, 4)

            # frame to general bar
            pygame.draw.rect(screen, WHITE, (x, y + distance, width, 15), 2, 4)
            pygame.draw.rect(screen, GRAY, (x, y + distance, width, 15), 1, 4)

        pygame.draw.rect(screen, WHITE, (x, y + z, width, 15), 0, 4)  # general bar rect
        # health bar rects with 3 colors
        pygame.draw.rect(screen, (0, 153, 0), (x, y + z, width * ratio, 15), 0, 4)
        pygame.draw.rect(screen, (0, 204, 0), (x, y + z, width * ratio, 10), 0, 4)
        pygame.draw.rect(screen, (0, 255, 0), (x, y + z, width * ratio, 8), 0, 4)

        # frame to general bar
        pygame.draw.rect(screen, WHITE, (x, y + z, width, 15), 2, 4)
        pygame.draw.rect(screen, GRAY, (x, y + z, width, 15), 1, 4)

        # good fon lst = [24,52,55,30,69,174,184]

        boost_lst = ['Atk+', 'Def+', 'Spa+', 'Spd+', 'Spe+']
        current_states = [self.atk, self.deff, self.spa, self.spd, self.speed]
        start_states = [self.start_atk, self.start_deff, self.start_spa, self.start_spd, self.start_speed]

        j = 0
        for i in range(len(start_states)):
            if i > 0:
                if current_states[i - 1] == start_states[i - 1]:
                    space = ((i - 1) * 0.225 * width)
                    j += 1
            space = ((i - j) * 0.225 * width)
            if current_states[i] > start_states[i]:
                # print('x')
                pygame.draw.rect(screen, (230, 255, 230), (x + space, y + z + 15, 0.22 * width, 15), 0,
                                 4)  # for boosting########################
                pygame.draw.rect(screen, (0, 153, 0), (x + space, y + z + 15, 0.22 * width, 15), 1,
                                 4)  # for boosting########################
                boost_text = font0_0.render(boost_lst[i], True, (0, 153, 0))
                screen.blit(boost_text, (x + 10 + space, y + z + 15))

        if self.gender in ['male', 'Male', 'MALE']:
            gender = font4_g.render('\u2642', True, (0, 153, 153))  # male
            gender2 = font5_g.render('\u2642', True, (25, 25, 25))

        else:
            gender = font4_g.render(chr(0x2640), True, (255, 0, 0))  # female
            gender2 = font5_g.render(chr(0x2640), True, (25, 25, 25))
            # g_color = (255,0,0)

        name_text0 = font1_n.render(self.char_type, True, WHITE)
        name_text1 = font2_n.render(self.char_type + '        L' + str(self.lvl), True, BLACK)

        text0_rect = name_text0.get_rect(center=(x + (width // 2) - 23, y - 14 + z))
        text1_rect = name_text0.get_rect(center=(x + (width // 2) - 20, y - 14 + z))
        gender_rect = name_text0.get_rect(center=(x + (width // 2) - 10 + font1_n.size(self.char_type)[0], y - 8 + z))

        screen.blit(name_text0, text0_rect)
        screen.blit(name_text1, text1_rect)

        screen.blit(gender2, gender_rect)
        screen.blit(gender, gender_rect)


font0_0 = pygame.font.SysFont(pygame.font.get_fonts()[0], 13)
font1_n = pygame.font.SysFont(pygame.font.get_fonts()[55], 20)
font2_n = pygame.font.SysFont(pygame.font.get_fonts()[55], 19)
font4_g = pygame.font.SysFont(pygame.font.get_fonts()[8], 23)
font5_g = pygame.font.SysFont(pygame.font.get_fonts()[8], 22)
font_big = pygame.font.SysFont(pygame.font.get_fonts()[8], 35)


######################################################################## END OF PLAYER CLASS  #################################################################3
###################################################################################################################################################3


def pause():
    transperent_screen = pygame.Surface((pygame.display.get_surface().get_size()))  # the size of your rect
    transperent_screen.set_alpha(128)  # alpha level
    transperent_screen.fill((255, 255, 255))  # this fills the entire surface
    screen.blit(transperent_screen, (0, 0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, char_size):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 20
        self.image = thundershock_img
        self.flip = False

        # self.image = pygame.transform.scale(self.image,(char_size.img.get_width()*2,char_size.img.get_height()*0.5))
        self.image = pygame.transform.scale(self.image, (char_size[0] * 2, char_size[1] * 0.5))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, d):

        if d == 1:
            self.flip = True
        else:
            self.flip = False

        self.image = pygame.transform.flip(self.image, self.flip, False)
        # move bullet
        self.rect.x += (-self.direction * self.speed) + screen_scroll

        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # check collision with levle(tile?)
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive and enemy.rect.x in range(self.rect.x - 10,
                                                         self.rect.x + 10) and enemy.stop_draw == False:
                    enemy.health -= 5
                    # print('Enemy HP:',enemy.health)
                    self.kill()


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, character):
        pygame.sprite.Sprite.__init__(self)
        self.speed = character.speed * 3
        self.image = thundershock_img
        self.range = 5
        self.duration = 30
        self.flip = False
        self.img_lst = []
        self.index = 0
        for i in range(1, self.range + 1):
            self.image = pygame.transform.scale(self.image,
                                                (character.img.get_width() * i, character.img.get_height() * 0.5))
            self.img_lst.append(self.image)

        self.image = self.img_lst[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x + (-direction * (1.5 * character.rect.width)), y + 20)
        self.direction = direction

    def update(self, d, char):

        self.index += 1

        if self.index == self.range:
            self.index = 0
        self.image = self.img_lst[self.index]

        # i choose to try this flip due to the animation effect from that
        self.image = pygame.transform.flip(self.image, True, False)

        # move bullet
        self.rect.x += (-self.direction)  # * self.speed) + screen_scroll
        self.rect.y = player.rect.y

        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # check collision with levle(tile?)
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 25
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive and enemy.stop_draw == False:
                    enemy.health -= 25
                    print('Enemy HP:', enemy.health)
                    # self.kill()
        self.duration -= 1
        if self.duration <= 0:
            self.kill()
            self.duration = 20


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -5
        self.speed = 7
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.damege = 50
        self.explosion_range = 4 * TILE_SIZE
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.vel_y += GRAVITY
        dx = self.speed * self.direction
        dy = self.vel_y

        # check collison with level
        for tile in world.obstacle_list:
            # check collision with walls
            if tile[1].colliderect(self.rect.x - dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                # check if below the ground , i.e thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    # self.speed = 0

                # check if above the ground i.e falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
                    self.speed = 0

        # pygame.draw.rect(screen,RED,self.rect,0)
        # update grenade position
        self.rect.x -= dx - screen_scroll
        self.rect.y += dy

        # countdown timer
        self.timer -= 2
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y - 3 * self.rect.size[1], 0.5, explosion_anim_direction, 0,
                                  16, 1)
            explosion_group.add(explosion)
            # do damage to anyone that is nearby
            distance_player = (((self.rect.centerx - player.rect.centerx) ** 2) + (
                        (self.rect.centery - player.rect.centery) ** 2)) ** 0.5
            if distance_player < self.explosion_range:
                damage_grenade = self.damege - (self.damege * (distance_player / self.explosion_range))
                player.health -= int(damage_grenade)
                # print('player HP:',player.health)
                # print(damage_grenade)

            for enemy in enemy_group:
                distance_enemy = (((self.rect.centerx - enemy.rect.centerx) ** 2) + (
                            (self.rect.centery - enemy.rect.centery) ** 2)) ** 0.5
                if distance_enemy < self.explosion_range:
                    damage_grenade = self.damege - (self.damege * distance_enemy / self.explosion_range)
                    enemy.health -= int(damage_grenade)


class POKEBALL(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 200
        # self.timer2 = 0
        self.vel_y = -6
        self.speed = 6
        self.image = pokeball_img
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.contain_pokemon = False
        # self.char_draw_again = False
        # self.red_animation = False
        # self.angle = 0

    def update(self):
        self.vel_y += GRAVITY
        dx = self.speed * self.direction
        dy = self.vel_y

        # check collison with level
        for tile in world.obstacle_list:
            # check collision with walls
            if tile[1].colliderect(self.rect.x - dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                # check if below the ground , i.e thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    # self.speed = 0

                # check if above the ground i.e falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
                    self.speed = 0

        # update grenade position
        self.rect.x -= dx - screen_scroll
        self.rect.y += dy

        # activate pokeball- wild pokemon logic
        for enemy in enemy_group:

            if self.contain_pokemon == False:

                # define collide with only 1 pokemon
                if pygame.sprite.spritecollide(enemy, pokeball_group, False):  # and not collided_already:
                    if enemy.alive:
                        # collided_already = True
                        # enemy.in_pokeball = True # will paint enemy in red color for 0.1 sec
                        self.contain_pokemon = True
                        enemy.stop_draw = True

                        if CatchingRate(enemy):  # function that check catching rate of each wild pokemone.
                            # n = 78
                            player.exp += enemy.lvl * (
                                        enemy.max_health + enemy.atk + enemy.deff + enemy.spa + enemy.spd + enemy.energy) // 6
                            anim_file = 'catched'  # 'catched\\'

                        else:
                            # n = 85
                            enemy.rect.center = self.rect.center
                            anim_file = 'escaped'  # 'escape\\'
                            # enemy.in_pokeball = False
                        print(anim_file)

                        # paint in red for cathing moment only
                        # if enemy.in_pokeball == True:
                        # colorImage = pygame.Surface(enemy.img.get_size()).convert_alpha()
                        # colorImage.fill((255,0,0))
                        # enemy.img.blit(colorImage, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

                        # if self.timer < 192:
                        # activate animation
                        cathing_animation = Explosion(self.rect.x, self.rect.y - 3 * self.rect.size[1], 0.5,
                                                      into_pokeball_anim_direction, 0, 72, 1, anim_file)
                        explosion_group.add(cathing_animation)
                        self.kill()

        # countdown timer
        self.timer -= 2
        # self.timer2 -= 2

        if self.timer <= 0:
            # if collided_already == False:
            if self.contain_pokemon == False:
                print(' not collided and self kill activate')
                player.pokeball_thrown = False
            self.kill()


into_pokeball_anim_direction = 'images\\into_pokeball_anim\\'
explosion_anim_direction = 'images\\explosion\\'


def CatchingRate(enemy):
    EnemyHPlost = 100 * (enemy.max_health - enemy.health) // enemy.max_health
    # print("EnemyHPlost:",EnemyHPlost)

    if pokemon_collection[enemy.char_type].form == 1:
        random_catch_range = 50
        enemy.collidWithPokeball += 10

    elif pokemon_collection[enemy.char_type].form == 2:
        random_catch_range = 70
        enemy.collidWithPokeball += 8


    elif pokemon_collection[enemy.char_type].form == 3:
        random_catch_range = 250
        enemy.collidWithPokeball += 5

    elif pokemon_collection[enemy.char_type].form == "legendary":
        random_catch_range = 300
        enemy.collidWithPokeball += 3

    else:
        print('raise error or add in future;')

    ##    if playr.lvl > enemy.lvl and random_catch_range >= 30:
    ##        random_catch_range -= (playr.lvl-enemy.lvl) * 3

    if random_catch_range > 2:
        if random_catch_range - enemy.collidWithPokeball < 2:
            enemy.collidWithPokeball = 0
        random_catch_range -= enemy.collidWithPokeball

        if random_catch_range - EnemyHPlost < 2:
            random_catch_range = 2
        else:
            random_catch_range -= EnemyHPlost

    random_catch = random.randint(1, random_catch_range)

    if random_catch == 1:
        PokemonCaught = True
        if len(party_lst) < 6:
            enemy.char = 'player'
            enemy.rect.center = player.rect.center
            party_lst.append(enemy)
        else:
            print('Already 6 pokemon in party')
        enemy.kill()
    else:
        PokemonCaught = False

    return PokemonCaught


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, file, start, end, step, extra_file=None):
        pygame.sprite.Sprite.__init__(self)
        self.file = file
        self.images = []
        self.max_range = (start, end, step)
        self.extra_file = extra_file if extra_file is not None else ''
        for num in range(self.max_range[0], self.max_range[1], self.max_range[2]):
            # for num in range(0,16):
            # img = pygame.image.load(img_directoriy + f'explosion\\{num}.png').convert_alpha()

            img = pygame.image.load(self.file + f'{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)

        # escape from pokeball
        if self.extra_file == 'escaped':
            for num in range(72, 85):
                img = pygame.image.load(self.file + 'escape\\' + f'{num}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.images.append(img)

        # cathced
        if self.extra_file == 'catched':
            for num in range(72, 78):
                img = pygame.image.load(self.file + 'catched\\' + f'{num}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.images.append(img)

        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                if self.extra_file == 'catched':
                    caught_pokemon_fx.play()
                player.pokeball_thrown = False  # prevent from user to throw pokeball during throwing animation.
                self.kill()
            else:
                self.image = self.images[self.frame_index]

        for enemy in enemy_group:
            if enemy.stop_draw and self.frame_index > 84:
                enemy.stop_draw = False


class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color,
                             (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))

        if self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_HEIGHT:
            fade_complete = True
        return fade_complete


intro_fade = ScreenFade(1, BLACK, 5)

death_fade = ScreenFade(2, PINK, 5)


class World():
    def __init__(self):
        self.obstacle_list = []
        self.ground_zero = []

    def process_data(self, data):
        enemies_num = 32
        self.level_length = len(data[0])
        # itereate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    ##                    if tile == 4:
                    ##                        img = img_list[tile]
                    ##                        img_rect = img.get_rect()
                    ##                        img_rect.x = 0
                    ##                        img_rect.y = pygame.display.get_surface().get_size()[1]
                    ##                        tile_data2 = (img,img_rect)
                    ##                        self.ground_zero.append(tile_data2)

                    elif tile >= 9 and tile <= 10:  # water
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14 or tile == 31:  # decoration
                        if tile == 31:
                            pass
                            # img = pygame.transform.scale(img,(2*TILE_SIZE,4*TILE_SIZE))
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # health and tile <= 18:
                        item_box = ItemBox('HEALTH', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 16:
                        item_box = ItemBox('HEALTH2', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 17:
                        item_box = ItemBox('ENERGY', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:
                        item_box = ItemBox('SPEED', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox('ATK', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:
                        item_box = ItemBox('DEFF', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 21:
                        item_box = ItemBox('SPD', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 22:
                        item_box = ItemBox('SPA', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 23:
                        item_box = ItemBox('EXP2', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 24:
                        item_box = ItemBox('TM', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 25:
                        pass  # tm
                    elif tile == 26:
                        item_box = ItemBox('POKEBALL', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 27:
                        item_box = ItemBox('EXP', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 28:
                        pass  # lucky egg
                    elif tile == 29:  # person
                        pass
                    elif tile == 30:  # create exit
                        img = pygame.transform.scale(img, (4 * TILE_SIZE, 4 * TILE_SIZE))
                        exit1 = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit1)

                    elif tile == 32:  # create player
                        # this tile very important. any modification in level editor need to verify player got this tile
                        #        self   (char_type,x         ,y     ,scale,speed,ammo,grenades):
                        # self,name,scale,hp,speed,tm1,tm2,typ1,typ2,energy,atk,deff,spa,spd,x_states,y_states)
                        player = Player(CHARACTER.name, "player", x * TILE_SIZE, y * TILE_SIZE, CHARACTER.hp,
                                        CHARACTER.scale, CHARACTER.speed, CHARACTER.fake_speed, CHARACTER.tm1,
                                        CHARACTER.tm2 \
                                        , CHARACTER.typ1, CHARACTER.typ2, CHARACTER.energy, CHARACTER.atk,
                                        CHARACTER.deff, CHARACTER.spa, CHARACTER.spd, CHARACTER.tm_lvl)  # ,25,90)

                        # print(party_lst)
                    elif tile > enemies_num:  # create enemies
                        for z in os.listdir('images\\game_background1\\pokemon'):
                            if z == str(tile - enemies_num) + '.png':
                                if enemy_collection[tile - enemies_num] in os.listdir('images\\pokemon_images'):
                                    # self,char_type,char, x, y,scale, speed,ammo,grenades)
                                    enemy = Player(enemy_collection[tile - enemies_num], 'enemy', x * TILE_SIZE,
                                                   y * TILE_SIZE,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].hp, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].scale \
                                                   , pokemon_collection[enemy_collection[tile - enemies_num]].speed,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].fake_speed,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].tm1, 0, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].typ1,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].typ2, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].energy,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].atk, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].deff,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].spa, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].spd,
                                                   pokemon_collection[
                                                       enemy_collection[tile - enemies_num]].tm_lvl)  # ,None,None)
                                    enemy_group.add(enemy)

                                    enemy.lvl = level * 2 + 5 + x // 10
                                    enemy.max_health, enemy.atk, enemy.deff, enemy.spa, enemy.spd, enemy.speed, enemy.energy, enemy.reg, enemy.fake_speed = \
                                    pokemon_collection[enemy_collection[tile - enemies_num]].states_update(enemy.lvl)

                                    enemy.max_energy = enemy.energy
                                    enemy.start_atk = enemy.atk
                                    enemy.start_deff = enemy.deff
                                    enemy.start_spa = enemy.spa
                                    enemy.start_spd = enemy.spd
                                    enemy.start_speed = enemy.speed
                                    enemy.max_fake_speed = enemy.fake_speed

        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


# pokemon learean move - dict
trainer_teach_tm = {  # 1:random.choice([sunny_day,rain_dance,par_pdr]),
    1: random.choice([ember, boublle, bullet_seed]),
    2: random.choice([ember, boublle, bullet_seed]),
    3: random.choice([sludge_bmb, rain_dance, water_gun]),
    4: random.choice([sludge_bmb, rain_dance, water_gun]),
    5: random.choice([sludge_bmb, rain_dance, water_gun]), }


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type

        self.image = item_boxes[self.item_type]
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

        # check if the player has picked up the berry
        if pygame.sprite.collide_rect(self, player):
            item_fx.play()
            # check what kind of box
            if self.item_type == 'HEALTH2':
                player.potion += 1
                player.exp += 50

            elif self.item_type == 'HEALTH':
                player.health = player.max_health
                player.exp += 250
            elif self.item_type == 'ENERGY':
                player.ammo += 25
                player.energy = player.max_energy
                player.exp += 250
            elif self.item_type == 'ATK':
                player.grenades += 15
                player.atk *= 1.1
                player.exp += 150

            elif self.item_type == 'DEFF':
                player.grenades += 3
                player.deff *= 1.1
                player.exp += 150

            elif self.item_type == 'SPEED':
                player.speed += 2
                player.exp += 100


            elif self.item_type == 'SPA':
                player.spa *= 1.1
                player.exp += 100

            elif self.item_type == 'SPD':
                player.spd *= 1.1
                player.exp += 100

            elif self.item_type == 'EXP':
                player.speed += 1
                player.spd *= 1.1
                player.spa *= 1.1
                player.atk *= 1.1
                player.deff *= 1.1
                # player.health = player.max_health
                player.energy = player.max_energy
                player.exp += 3000
            elif self.item_type == 'EXP2':
                player.exp += 300
            elif self.item_type == 'POKEBALL':
                player.pokeball += 1
                player.exp += 100

            elif self.item_type == 'TM' and len(trainer.tm_lst) < 16:
                trainer.tm_lst.append(trainer_teach_tm[level])
                # player.TM_LST.append(trainer_teach_tm[level])
                player.exp += 300

            self.kill()


y_axis_trainer = 0


class Trainer():
    def __init__(self):
        self.lvl = 1
        self.exp = 0
        # self.pokeball = 0
        # self.badge = 0
        # self.potion = 0
        self.tm_lst = [water_gun]
        self.clicked = False
        self.warning = False
        self.warning2 = False

        # self.tm = []
        self.text_new_move = ''
        self.counter = 0

        self.switch_pokemon = 0

        self.tm_delete = ''

        self.show_tm_preview = False

    def draw_menue(self):
        x_pos, y_pos = 400, 150  # define my image position (include transperent and not)
        x_text_rects, y0 = 100, 170  # position where text start

        global y_axis_trainer

        screen.blit(trainer_box_img, (x_pos, 100))
        my_image = pygame.Surface((trainer_box_img.get_width(), trainer_box_img.get_height() - 100), pygame.SRCALPHA)
        my_image_rect = my_image.get_rect()

        my_image_rect.topleft = (x_pos, y_pos)
        my_image_rect.h = 280
        pygame.draw.rect(screen, (10, 100, 200), my_image_rect, 2, 2)

        # draw up and down scrolling rects
        pygame.draw.rect(screen, (178, 138, 28), up_rect_trainer, 0, 4)
        pygame.draw.rect(screen, (178, 138, 28), down_rect_trainer, 0, 4)

        pos = pygame.mouse.get_pos()

        # close_btn
        close_btn_rect = pygame.Rect((my_image_rect.centerx - 45, trainer_box_img.get_height() + 70, 80, 20))

        pygame.draw.rect(screen, (200, 140, 60), close_btn_rect, 0, 4)

        if close_btn_rect.collidepoint(pos):
            pygame.draw.rect(screen, (150, 110, 90), close_btn_rect, 0, 4)
            if pygame.mouse.get_pressed()[0]:
                self.warning, self.warning2 = False, False
                self.show_tm_preview = False
                self.counter = 0
                self.text_new_move = ''

        pygame.draw.rect(screen, (120, 50, 30), close_btn_rect, 2, 4)
        close_text = font.render('close', True, (20, 20, 20))
        close_text_rect = close_text.get_rect(center=close_btn_rect.center)
        screen.blit(close_text, close_text_rect)

        space = 30
        fixed_y = 50

        for i, t in enumerate(self.tm_lst):
            text_rect = pygame.Rect(x_pos + x_text_rects, (y_axis_trainer + y0 + i * space), 180, 20)
            action1_rect = pygame.Rect(text_rect.right + 25, text_rect.y, 50, 20)
            # print(t.text)
            if text_rect.y > y0 - space and text_rect.bottom <= my_image_rect.bottom - space:
                TM_text = font.render(str(i + 1) + '. ' + t.text[0] + t.text[1:].lower(), True, (20, 20, 20))
                screen.blit(TM_text, text_rect)
                screen.blit(trash_del_tm_img2, action1_rect)
                # pygame.draw.rect(screen,(2,2,2),action1_rect,4,4)
            z = y0 + i * (len(self.tm_lst))

            # del tm action
            if action1_rect.collidepoint(pos):
                pygame.draw.circle(screen, (20, 20, 20),
                                   (action1_rect.centerx - action1_rect.h // 2, action1_rect.centery),
                                   action1_rect.h // 2, 3)
                if pygame.mouse.get_pressed()[0]:  # and self.clicked == False:
                    self.warning = True
                    self.tm_delete = t.text
            if text_rect.collidepoint(pos) and text_rect.bottom <= my_image_rect.bottom - space:
                fixed_rect = pygame.Rect(text_rect.x - x_pos, text_rect.y - y_pos, text_rect.w, text_rect.h)
                pygame.draw.rect(my_image, (200, 200, 200, 100), fixed_rect, 0, 4)

                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(my_image, (100, 100, 100, 150), fixed_rect, 2, 4)

                    for pokemon in party_lst:
                        if pokemon.state_blit:  # and t not in pokemon.TM_LST:
                            self.warning2 = True
                            # print(t.type,[pokemon.typ1,pokemon.typ1])
                            if t.type.lower() in [pokemon.typ1, pokemon.typ1]:

                                if len(pokemon.TM_LST) > 8:
                                    self.text_new_move = f"{pokemon.char_type} Can't remmber more than 8 moves."
                                    # self.option = 3

                                elif len(pokemon.TM_LST) == 8:
                                    self.text_new_move = f'{pokemon.char_type} learned {t.text} and forget {pokemon.TM_LST[-1].text}'
                                    pokemon.TM_LST[-1] = t
                                    # self.option = 2
                                else:

                                    if t in pokemon.TM_LST:
                                        self.text_new_move = f'{pokemon.char_type} already know {t.text}.'
                                    else:
                                        self.text_new_move = f'{pokemon.char_type} learn {t.text}'
                                        pokemon.TM_LST.append(t)
                                        # pokemon.TM_LST.add(t)
                                        self.tm_lst.remove(t)
                            else:
                                self.text_new_move = f"{pokemon.char_type} can't learn {t.text}"

        if self.warning2 and self.counter < 150:

            pygame.draw.rect(screen, (230, 200, 200), (x_pos + 90, 340, 250, 50), 0, 4)
            pygame.draw.rect(screen, (25, 20, 20), (x_pos + 90, 340, 250, 50), 3, 4)
            draw_multyline_text(my_image, self.text_new_move, (x_pos + 100, 350), font, (60, 60, 60), 200, 250)

            self.counter += 1
            if self.counter > 145:
                self.warning2 = False
                self.counter = 0
                self.text_new_move = ''

        # scroll list
        if down_rect_trainer.collidepoint(pos) and y_axis_trainer > -z - (
                fixed_y * 6) + 550:  # window_rect.bottom:#and y_axis_trainer > -z+(space*window_rect.h/(y0-space)):# and y_axis_trainer > 0:
            pygame.draw.rect(screen, (255, 188, 0), down_rect_trainer, 0, 4)
            y_axis_trainer -= 2
            # print(y_axis_trainer,z)

        if up_rect_trainer.collidepoint(pos) and y_axis_trainer < 0:  # and y_axis_trainer < z:
            pygame.draw.rect(screen, (255, 188, 0), up_rect_trainer, 0, 4)
            y_axis_trainer += 2

        pygame.draw.polygon(screen, (100, 72, 2), (
        (down_rect_trainer.x + 5, down_rect_trainer.top + 5), (down_rect_trainer.centerx, down_rect_trainer.bottom - 5),
        (down_rect_trainer.right - 5, down_rect_trainer.top + 5)), 3)
        pygame.draw.polygon(screen, (100, 72, 2), (
        (up_rect_trainer.x + 5, up_rect_trainer.bottom - 5), (up_rect_trainer.centerx, up_rect_trainer.top + 5),
        (up_rect_trainer.right - 5, up_rect_trainer.bottom - 5)), 3)

        if self.warning:
            warning_rect = pygame.Rect(100, 100, 200, 250)
            # warning_del_tm = 'Are you sure to deleete TM?'
            pygame.draw.rect(screen, (200, 200, 120), (1.5 * x_pos - 15, 1.5 * y_pos - 15, 210, 90))
            text_tm_del = f"  {self.tm_delete}\nWill be deleted?"
            answer_no_rect, answer_yes_rect = draw_multyline_text(my_image, text_tm_del, (1.5 * x_pos, 1.5 * y_pos),
                                                                  font, (60, 60, 60), 200, 250, \
                                                                  (x_pos, y_pos), (150, 150, 150, 150),
                                                                  text2=['No', 'Yes'])
            if answer_no_rect.collidepoint(pos):
                pygame.draw.rect(screen, (200, 200, 180), answer_no_rect, 4, 4)
                if pygame.mouse.get_pressed()[0]:
                    self.warning = False
            if answer_yes_rect.collidepoint(pos):
                pygame.draw.rect(screen, (200, 200, 180), answer_yes_rect, 4, 4)
                if pygame.mouse.get_pressed()[0]:
                    self.tm_lst.remove(t)
                    print('tm_lst amount:', len(self.tm_lst))
                    self.warning = False

        test_rect = pygame.Rect(0, 0, 200, 200)
        test_rect.center = my_image.get_width() // 2, my_image.get_height() // 2
        # pygame.draw.rect(my_image,(200,20,20),test_rect,0)
        # pygame.draw.rect(screen,(20,200,20),(x_pos,y_pos,200,200),3)
        screen.blit(my_image, my_image_rect)
        return y_axis_trainer


trainer = Trainer()


##def switching_animation(pok_rect):
##    trainer_pos = 0,150
##    for i in range(5):
##        pygame.draw.line(screen,(240,0,0),(i+1,140+2*i),(pok_rect.center),i)
##        pygame.draw.polygon(screen,(200+10*i,i,12-2*i),((trainer_pos),(100,120-3*i),(200,80-5*i),(pok_rect.center)),5-i)

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


# create buttons
start_btn = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 100, start_img, 0.5, 0.5)
exit_btn = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 50, exit_img, 0.5, 0.5)
restart_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, restart_img, 0.5, 0.5)

# pause menue buttons
play_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 200, play_img, 0.5, 0.5)
save_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 100, save_img, 0.5, 0.5)
settings_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, settings_img, 0.5, 0.5)
exit2_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 100, exit2_img, 0.5, 0.5)
fullscreen_button = button.Button(10, 10, fullscreen_img, 0.3, 0.3)

left_ball_btn = button.Button(122, 290, left_ball_img, 1, 1)
center_ball_btn = button.Button(360, 292, center_ball_img, 1, 1)
right_ball_btn = button.Button(590, 291, right_ball_img, 1, 1)

trainer_box_button = button.Button(SCREEN_WIDTH - 170, 5, trainer_box_img, 0.1, 0.1)

# create sprite group
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
pokeball_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
# party_group = pygame.sprite.Group()


# settings
screen_width = SETTINGS.Settings('Screen width:', 800, 1200, 350, 150)
screen_height = SETTINGS.Settings('Screen Height:', 500, 700, 350, 210)
fps = SETTINGS.Settings('FPS:', 10, 130, 350, 270)
sound_setting = SETTINGS.Settings('Sound:', 0, 0.1, 350, 330)
music_setting = SETTINGS.Settings('Music:', 0, 1, 350, 390)
font_size = SETTINGS.Settings('Font Size:', 20, 35, 350, 450)
##font_color_r = SETTINGS.Settings('Font Color(r):',0,255,350,430)
##font_color_g = SETTINGS.Settings('Font Color(g):',0,255,350,455)
##font_color_b = SETTINGS.Settings('Font Color(b):',0,255,350,480)

settings = [screen_width, screen_height, fps, sound_setting, music_setting,
            font_size]  # ,font_color_r,font_color_g,font_color_b]

# Create empty tile list
world_data = []
for row in range(ROWS + 1):  # +1 is the floor data i created
    r = [-1] * COLS
    world_data.append(r)

# load in level data and create world
with open(f'levels_csv\\level#{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
##player,health_bar,energy_bar,health_bar_enemy = world.process_data(world_data)
##speed_timer = 0


pygame.mixer.music.load(f'audio\\game music\\{BG_MUSIC[0]}.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)

run = True
while run:

    clock.tick(FPS)

    if start_game == False:

        # Music_start(BG_MUSIC[0])

        screen.blit(main_bg_img, (0, 0))
        screen.blit(pokemon_bg_img, (SCREEN_WIDTH // 3 - 50, 0))

        if fullscreen_button.draw(screen):
            screen = pygame.display.set_mode((0, 0))
            SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

            menu_SIZE = 85  # 0.5 * SCREEN_HEIGHT // ROWS

            start_btn = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 150, start_img, 0.5, 0.5)
            exit_btn = button.Button(SCREEN_WIDTH - 150, 10, exit_img, 0.5, 0.5)
            restart_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, restart_img, 0.6, 0.6)

            main_bg_img = pygame.transform.scale(main_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            pokemon_bg_img = pygame.transform.scale(pokemon_bg_img, (SCREEN_WIDTH // 2, 150))
            oak_img = pygame.transform.scale(oak_img,
                                             (SCREEN_WIDTH - choose_starter_img.get_width(), 1.2 * SCREEN_HEIGHT - 10))

        if start_btn.draw(screen):
            start_game = True
            start_intro = True  # relate to opening scene
            Music_stop()
            Music_start(BG_MUSIC[1])

        if exit_btn.draw(screen):
            run = False


    elif choose_character == True:

        # take mouse curser position
        pos = pygame.mouse.get_pos()
        # print(pos)
        screen.blit(oak_img, (choose_starter_img.get_width(), 0))
        screen.blit(choose_starter_img, (0, 0))

        if left_ball_btn.draw(screen):
            CHARACTER = Bulbasaur
            choose_character = False
            start_intro = True
            player = world.process_data(world_data)
            # party_lst.append(CHARACTER)
            party_lst.append(player)
            bulba_fx.play()
            Music_stop()
            # Music_start(BG_MUSIC[2])
            # show_pokemon = CHARACTER # line in test , searching word related :party2

        elif center_ball_btn.draw(screen):
            CHARACTER = Charmander
            choose_character = False
            start_intro = True
            player = world.process_data(world_data)
            party_lst.append(player)
            Music_stop()
            # Music_start(BG_MUSIC[2])
            # show_pokemon = CHARACTER # line in test , searching word related :party2

        elif right_ball_btn.draw(screen):
            CHARACTER = Squirtle
            choose_character = False
            start_intro = True
            player = world.process_data(world_data)
            party_lst.append(player)
            Music_stop()
            # Music_start(BG_MUSIC[2])
            # show_pokemon = CHARACTER # line in test , searching word related :party2

        if left_ball_btn.rect.collidepoint(pos):
            screen.blit(bulba_img, (30, 0))
        if center_ball_btn.rect.collidepoint(pos):
            screen.blit(charma_img, (300, 0))
        if right_ball_btn.rect.collidepoint(pos):
            screen.blit(squir_img, (530, 0))


    else:
        ##        if not pygame.mixer.music.get_busy():
        ##            Game_musics()
        Music_start(BG_MUSIC[2])

        # update bg
        draw_bg()
        # update world map
        world.draw()

        ##        pygame.draw.rect(screen,GRAY,(0,SCREEN_HEIGHT - menu_SIZE,SCREEN_WIDTH-screen_scroll,SCREEN_HEIGHT))

        # TM1_TIMER.draw()
        # TM2_TIMER.draw()
        # TM3_TIMER.draw()
        # TM4_TIMER.draw()

        ##        if party_lst:
        ##            player = party_lst[trainer.switch_pokemon]

        draw_text(f'Game Level: {level}', font, set_color, 50,
                  pygame.display.get_surface().get_size()[1] - 2 * TILE_SIZE)

        pokeball_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()

        pokeball_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)

        water_group.draw(screen)

        if pause_activate:
            pause()
            # Music_stop()
            pygame.mixer.music.pause()

            pause_mode = True
            player.draw()
            # pygame.draw.line(screen,WHITE,(SCREEN_WIDTH//2,0),(SCREEN_WIDTH//2,SCREEN_HEIGHT))

            for enemy in enemy_group:
                if enemy.stop_draw == False:
                    enemy.draw()

            if pause_from_pokemon_party_btn:
                pause_from_esc_keyboard = False
                screen.blit(pokemon_party_bg_img, (30, 0))

                for party_index, pokemon in enumerate(party_lst):
                    if hasattr(pokemon_collection[pokemon.char_type], "lvl_100"):
                        for i in pokemon_collection[pokemon.char_type].lvl_100_states(100):
                            party_states_lvl100_lst[party_index].append(i)
                        del pokemon_collection[pokemon.char_type].lvl_100
                        print(party_states_lvl100_lst)

                    pokemon.PokemonInParty(55, 90 * (party_index + 1), party_states_lvl100_lst[party_index])

            if pause_from_esc_keyboard:  # and not pause_from_pokemon_party_btn:
                # pause_from_pokemon_party_btn = False

                if play_btn.draw(screen) and not settings_mode:
                    pause_activate = False
                    pause_mode = False

                    pygame.mixer.music.unpause()

                if save_btn.draw(screen) and not settings_mode:
                    pause_activate = False
                    pause_mode = False
                    pygame.mixer.music.unpause()

                if settings_btn.draw(screen) and not settings_mode:
                    settings_mode = True

                if exit2_btn.draw(screen) and not settings_mode:
                    run = False

                if settings_mode:
                    pygame.mixer.music.unpause()

                    '''
                    if fullscreen_button.draw(screen):
                        screen = pygame.display.set_mode((0,0))
    ##                else:
    ##                    screen = pygame.display.set_mode((screen_width.value,screen_height.value))
                    '''

                    # Change settings:
                    # fps
                    FPS = fps.value
                    # music
                    pygame.mixer.music.set_volume(float(music_setting.value))
                    # sound
                    for sett in sound_volume_lst:
                        sett.set_volume(20 * sound_setting.value)

                    # create setting window - i belive i didnt used it correctly but it was at the begining of my project so nvm
                    setting_window = pygame.Surface((650, 450))
                    setting_window.fill(GREEN2)
                    pygame.draw.rect(setting_window, WHITE, (0, 0, 650, 20))

                    # draw x like in WINDOWS 10 window
                    x_rect = pygame.Rect(720, 100, 30, 20)
                    pygame.draw.line(setting_window, BLACK, (630, 5), (640, 15))
                    pygame.draw.line(setting_window, BLACK, (630, 15), (640, 5))

                    # define font and size - in future i can add chenge font but its waste of time now
                    font = pygame.font.SysFont('Futura', font_size.value)
                    font_size.font_example(setting_window, font, 50, setting_window.get_size()[1] - 50, 230, 230, 230)
                    # font_size.font_example(setting_window,font,450,font_size.rect.centery ,font_color_r.value,font_color_g.value,font_color_b.value)
                    # set_color = (font_color_r.value,font_color_g.value,font_color_b.value)

                    screen.blit(setting_window, (100, 100))

                    # create special settings buttons from SETTINGS file func
                    defult_rect_btn, full_screen_rect_btn, control_setting_rect_btn = SETTINGS.Draw_special_settings(
                        screen, setting_window)

                    pos = pygame.mouse.get_pos()

                    if not setting_controller:
                        # define close window rect (as on regullar pc)
                        if x_rect.collidepoint((pos)):
                            pygame.draw.rect(screen, RED, x_rect)
                            pygame.draw.line(screen, WHITE, (730, 105), (740, 115))
                            pygame.draw.line(screen, WHITE, (730, 115), (740, 105))
                            if pygame.mouse.get_pressed()[0]:
                                settings_mode = False
                                setting_controller = False

                        for func in settings:
                            func.draw(screen)  # dont understand yet why not working "setting_window" instead screen
                            if func.rect.collidepoint((pos)) and pygame.mouse.get_pressed()[0] and pos[0] in range(
                                    func.rect_line.x, func.rect_line.x + func.line_width + 1):
                                pygame.draw.rect(screen, BLACK, (func.rect), 1)
                                func.rect.centerx = pos[0]
                                func.update(pos[0])
                                if pos[1] in range(screen_width.rect_line.y, screen_height.rect_line.y):
                                    screen = pygame.display.set_mode((screen_width.value, screen_height.value))

                            elif func.rect_line_transperent.collidepoint((pos)) and pygame.mouse.get_pressed()[
                                0]:  # clicking area are wider then visible line
                                func.rect.centerx = pos[0]
                                func.update(pos[0])

                            # restore settings to default
                            if defult_rect_btn.collidepoint((pos)):
                                pygame.draw.rect(screen, (0, 250, 30), (defult_rect_btn), 3)
                                if pygame.mouse.get_pressed()[0]:
                                    func.rect.centerx = func.defult
                                    func.update(func.defult)

                        # Full screen in setting mode
                        if full_screen_rect_btn.collidepoint((pos)):
                            pygame.draw.rect(screen, (0, 250, 30), (full_screen_rect_btn), 3)
                            if pygame.mouse.get_pressed()[0]:
                                screen = pygame.display.set_mode((0, 0))
                                pokemon_party_btn = button.Button(pygame.display.get_surface().get_size()[0] - 40, 20,
                                                                  pokemon_party_img, 0.3, 0.3)
                                # controller_setting_bg_image = pygame.transform.scale(controller_setting_bg_image,(pygame.display.get_surface().get_size()))

                        if control_setting_rect_btn.collidepoint((pos)):
                            pygame.draw.rect(screen, (0, 250, 30), (control_setting_rect_btn), 3)
                            if pygame.mouse.get_pressed()[0]:
                                setting_controller = True

                    # reminder : setting_controller = False in game variable
                    if setting_controller:

                        # define new window size
                        setting_controller_width, setting_controller_height = pygame.display.get_surface().get_size()
                        # define the location of X for close that window
                        closing_rect = 0.85 * setting_controller_width - 20
                        # define window and draw white rect on it and define x,y coord for bliting this window
                        controller_window = pygame.Surface(
                            (setting_controller_width * 0.85, setting_controller_height * 0.9))
                        pygame.draw.rect(controller_window, WHITE, (0, 0, setting_controller_width * 0.85, 20))

                        # define the position of new window comparing to screen (new begin of axes is 100,30 of all what will draw on ne window
                        # use as x_fix and y_fix in SETTING controler functions
                        x_cord_control_window, y_cord_control_window = 100, 30

                        # define rect for new window
                        controller_window_rect = controller_window.get_rect()
                        # print("controller_window_rect",controller_window_rect)

                        # define rect where the X will draw and mouse wll collide with and move that rect into new window coords
                        rect_in_sub_window = pygame.Rect(-30, 0, 30, 20)
                        closing_rect_x_rect = rect_in_sub_window.move(
                            controller_window_rect.right + x_cord_control_window, y_cord_control_window)

                        pygame.draw.line(controller_window, BLACK, (closing_rect, 5), (closing_rect + 10, 15))
                        pygame.draw.line(controller_window, BLACK, (closing_rect, 15), (closing_rect + 10, 5))

                        for event in pygame.event.get():

                            # game controls
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    setting_controller = False

                                for k in SETTINGS.key_obj_lst:
                                    # define each key by user
                                    if k.active:
                                        # k.keyboard  = event.unicode
                                        k.keyboard = pygame.key.name(event.key)
                                        SETTINGS.default = False

                        ##                        #define close window rect (as on regullar pc) # i choode to define those rect for learning the rect.move
                        if closing_rect_x_rect.collidepoint((pos)):
                            pygame.draw.rect(controller_window, RED, (closing_rect - 5, 0, 30, 20))
                            # pygame.draw.rect(screen,RED,closing_rect_x_rect) # untill i will find a solution i got use it
                            pygame.draw.line(controller_window, WHITE, (closing_rect, 5), (closing_rect + 10, 15))
                            pygame.draw.line(controller_window, WHITE, (closing_rect, 15), (closing_rect + 10, 5))
                            if pygame.mouse.get_pressed()[0]:
                                setting_controller = False

                        # bliting bg

                        controller_window.blit(controller_setting_bg_image, (0, 20))
                        controller_setting_bg_image = pygame.transform.scale(controller_setting_bg_image, (
                        controller_window.get_size()[0], controller_window.get_size()[1] - 20))

                        for k in SETTINGS.key_obj_lst:
                            k.draw(controller_window, x_cord_control_window, y_cord_control_window)
                            if SETTINGS.default:
                                k.keyboard = k.default
                        if SETTINGS.IS_DEFAULT(controller_window, x_cord_control_window,
                                               y_cord_control_window):  # this func take the x,y_fix position due to collideing with rect issue
                            SETTINGS.default = True

                        # bliting that controler window with all rect and text on it
                        screen.blit(controller_window, (x_cord_control_window, y_cord_control_window))


        else:
            '''
            #actual game play
            '''

            pause_mode = False
            if len(enemy_group) <= 0:
                no_enemy = True
            else:
                no_enemy = False

            if no_enemy:
                exit_group.draw(screen)
                draw_text('Exit avilable.', font, WHITE, SCREEN_WIDTH // 2 - 100, 70)

            enemy_vision = []
            # for Lvl,enemy in enumerate(enemy_group):
            for enemy in enemy_group:

                enemy.update()
                if enemy.stop_draw == False:
                    enemy.draw()
                    # enemy.ai(Lvl,player_once_lvl)
                    enemy.ai()
                    # if enemy.vision.colliderect(player.rect):
                    x_dis = 350
                    y_dis = 200

                    # states are updated in enemy-tile class
                    # enemy.lvl += Lvl
                    # enemy.max_health,enemy.atk,enemy.deff,enemy.spa,enemy.spd,enemy.speed,enemy.energy,enemy.reg = pokemon_collection[enemy.char_type].states_update(enemy.lvl)

                    # enemy.states_update(lvl)
                    if enemy.rect.x in range(player.rect.x - x_dis, player.rect.x + x_dis) and enemy.rect.y in range(
                            player.rect.y - y_dis, player.rect.y + y_dis) \
                            or enemy.vision.colliderect(player.rect):
                        enemy_vision.append(enemy)

            for i, enemy in enumerate(enemy_vision):
                # health_bar_enemy.z = i*35
                # health_bar_enemy()#.draw(enemy.health,enemy.max_health,enemy.energy,enemy.char_type)
                enemy.HealthBar(pygame.display.get_surface().get_size()[0] - 200, 10, i * 35)

            player.draw()
            player.update()  # animation and cooldown in 1 function see player class above
            player.HealthBar(10, 20, 0)
            # player.update_energy(second_for_energy)

            bullet_group.draw(screen)
            bullet_group.update(player.direction)

            # show intro (screen fade )
            if start_intro == True:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            if player.alive:
                # draw menue - draw pokemon attacks , pokeball, potion and party_btn
                # if party btn activate then pasue is activated also
                pause_from_pokemon_party_btn, pause_activate = draw_menue()

                if player.exp > lvl_up_pts(player.lvl):
                    player.lvl += 1
                    pokemon_lvl_up_fx.play()
                    player.exp = 0

                    print(player.fake_speed, player.max_fake_speed)
                    # adding the hp up from lvl up
                    temp_hp_to_add = player.health

                    temp_just_for_print_hp_change = player.max_health
                    # update player states per lvl up
                    player.max_health, player.atk, player.deff, player.spa, player.spd, player.speed, player.energy, player.reg, player.fake_speed = CHARACTER.states_update(
                        player.lvl)
                    player.health += player.max_health - temp_hp_to_add
                    # player_states_lst = [player.max_health,player.atk,player.deff,player.spa,player.spd,player.speed,player.energy,player.reg]

                    print('Level up :', player.lvl)
                    print(player.max_health, player.atk, player.deff, player.spa, player.spd, player.speed,
                          player.energy, player.reg, player.fake_speed)
                    ##                        print('HP(player): +',player.max_health - temp_just_for_print_hp_change)
                    ##                        print('Atk(player) +',player.atk-player.start_atk)
                    ##                        print('Def(player) +',player.deff-player.start_deff)
                    ##                        print('Spa(player) +',player.spa-player.start_spa)
                    ##                        print('Spd(player) +',player.spd-player.start_spd)
                    print('Speed(player) +', player.fake_speed - player.max_fake_speed)
                    ##                        print('Eng(player) +',player.energy-player.max_energy)
                    ##                        print('\n')
                    # print('Reg(player) +',player.spd-player.start_spd)

                    player.max_energy = player.energy
                    player.start_atk = player.atk
                    player.start_deff = player.deff
                    player.start_spa = player.spa
                    player.start_spd = player.spd
                    player.start_speed = player.speed
                    player.max_fake_speed = player.fake_speed
                    # self.hp,      self.atk,  self.deff,  self.spa,  self.spd,  self.speed,self.energy,self.reg
                ##                        print('Level up :',player.lvl)
                ##                        print('HP(player):',player.health,'HP(char):',CHARACTER.hp,'max_hp:',player.max_health)
                ##                        print('Atk(player):',player.atk,'Atk(char):',CHARACTER.atk,'start_atk:',player.start_atk)
                ##                        print('Def(player):',player.deff,'Def(char):',CHARACTER.deff,'start_def:',player.start_deff)
                ##                        print('Spa(player):',player.spa,'Spa(char):',CHARACTER.spa,'start_spa:',player.start_spa)
                ##                        print('Spd(player):',player.spd,'Spd(char):',CHARACTER.spd,'start_spd:',player.start_spd)

                if player.speed > player.start_speed:
                    # player.speed = player.start_speed

                    speed_boost = True
                    # draw_text(f'DOUBLE SPEED ({15 - event_timer_s})',font,set_color,SCREEN_WIDTH - 350,SCREEN_HEIGHT - 2*TILE_SIZE)
                    speed_img = pygame.transform.scale(speed_img,
                                                       (int(player.rect.size[0] * 1.5), int(player.rect.size[1] * 1.5)))

                    # if speed_timer % 2 == 0 : #moving_left or moving_right:
                    screen.blit(speed_img, (player.rect.x, player.rect.y))
                    if event_timer_s >= 15:
                        speed_boost = False
                        player.speed = player.start_speed
                        event_timer_s = 0

                if player.atk > player.start_atk:
                    atk_boost = True
                    if event_timer_a >= 15:
                        atk_boost = False
                        player.atk = player.start_atk
                        event_timer_a = 0
                if player.deff > player.start_deff:
                    deff_boost = True

                    # screen.blit(speed_img,(player.rect.x,player.rect.y))
                    if event_timer_d >= 15:
                        deff_boost = False
                        player.deff = player.start_deff
                        event_timer_d = 0
                if player.spa > player.start_spa:
                    spa_boost = True

                    # screen.blit(speed_img,(player.rect.x,player.rect.y))
                    if event_timer_sp >= 15:
                        sp_boost = False
                        player.sp = player.start_spa
                        event_timer_sp = 0

                if player.spd > player.start_spd:
                    spd_boost = True

                    # screen.blit(speed_img,(player.rect.x,player.rect.y))
                    if event_timer_spd >= 15:
                        spd_boost = False
                        player.spd = player.start_spd
                        event_timer_spd = 0

                # clicking on potion/pokeball btn
                # use_item_btn()

                # shoot bullet
                if shoot:
                    player.shoot()

                # throw grenade # i want to forbit shoot and throw grenade at same time
                elif grenade and grenade_thrown == False and player.grenades > 0:
                    grenade = Grenade(player.rect.centerx - int(player.direction * player.rect.size[0] * 0.5), \
                                      player.rect.top, player.direction)
                    grenade_group.add(grenade)
                    grenade_thrown = True
                    player.grenades -= 1

                if moving_left or moving_right:
                    player.update_action(1)
                elif player.in_air:
                    player.update_action(2)
                elif shoot:
                    player.update_action(4)
                else:
                    player.update_action(0)

                screen_scroll, level_complete = player.move(moving_left, moving_right)
                bg_scroll -= screen_scroll
                # print(screen_scroll,bg_scroll)

                if level_complete:
                    party_temp_data = []
                    for pok in party_lst:
                        pok_temp_data = pok.exp, pok.lvl, pok.TM_LST
                        party_temp_data.append(pok_temp_data)  # = [player.exp,player.lvl,player.TM_LST]

                    start_intro = True
                    level += 1
                    bg_scroll = 0
                    world_data = reset_level()
                    if level <= MAX_LEVELS:
                        # load next level
                        with open(f'levels_csv\\level#{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)

                        for i, pok in enumerate(party_lst):
                            pok.exp, pok.lvl, pok.TM_LST = party_temp_data[i]
                            pok.health = pok.max_health
            else:
                screen_scroll = 0
                temp_lvl = player.lvl
                temp_exp = player.exp
                if death_fade.fade():
                    if restart_btn.draw(screen):
                        bg_scroll = 0
                        world_data = reset_level()
                        death_fade.fade_counter = 0
                        start_intro = True
                        with open(f'levels_csv\\level#{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        # choose_character = True
                        player = world.process_data(world_data)
                        player.lvl = temp_lvl
                        player.exp = 0

    for event in pygame.event.get():

        # quit game
        if event.type == pygame.QUIT:
            run = False

        # player is not definded while this line is running in order to solve that i added if party_lst not empty whats mean theres player inside it
        if party_lst:
            if event.type == pygame.USEREVENT:
                player.update_energy()

            if event.type == pygame.USEREVENT and speed_boost:
                event_timer_s += 1
            if event.type == pygame.USEREVENT and atk_boost:
                event_timer_a += 1
            if event.type == pygame.USEREVENT and deff_boost:
                event_timer_d += 1
            if event.type == pygame.USEREVENT and spa_boost:
                event_timer_sp += 1
            if event.type == pygame.USEREVENT and spd_boost:
                event_timer_spd += 1

            # activate TM
            for tm in player.TM_LST:
                if event.type == pygame.USEREVENT + 2 and tm.tm_active:
                    tm.event_timer_tm += 0.1
                    # tm.clicked = False
                    if tm.event_timer_tm >= tm.reg:
                        tm.event_timer_tm = 0
                        tm.tm_active = False
                        # tm.clicked = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE and not pause_mode:
                pause_activate = True
                pause_from_esc_keyboard = True
                pause_from_pokemon_party_btn = False
            if event.key == pygame.K_ESCAPE and pause_mode:
                pause_activate = False
                pause_from_esc_keyboard = False

            if event.key == pygame.K_RIGHT:
                trainer.switch_pokemon += 1
                if trainer.switch_pokemon >= len(party_lst):
                    trainer.switch_pokemon = 0
                else:
                    ##        if party_lst:
                    # party_lst[1],party_lst[0] = party_lst[0],party_lst[1]
                    # temp_pok_in_party = party_lst[0]
                    # print(type(temp_pok_in_party),temp_pok_in_party.char_type)
                    # player = party_lst[trainer.switch_pokemon]
                    # party_lst[trainer.switch_pokemon-1] = temp_pok_in_party
                    # player = party_lst[0]
                    ##                    switching_animation(player.rect)
                    ##                    pygame.draw.line(screen,(240,0,0),(0,150),(player.rect.center),3)
                    ##                    pygame.draw.line(screen,(240,0,0),(10,145),(player.rect.center),2)
                    ##                    pygame.draw.line(screen,(240,0,0),(0,152),(player.rect.center),4)

                    party_lst[trainer.switch_pokemon], party_lst[0] = party_lst[0], party_lst[trainer.switch_pokemon]
                    player = party_lst[0]

            for k in SETTINGS.key_obj_lst:
                try:
                    if event.key == pygame.key.key_code(k.keyboard):
                        if k.description == 'Moving Right':
                            moving_right = True
                        if k.description == 'Moving Left':
                            moving_left = True
                        if k.description == 'Jump' and player.alive:
                            player.jump = True
                            # test_del_TM = True
                            if pause_activate == False:
                                jump_fx.play()
                        if k.description == 'Throw Pokeball':
                            pokeball_throw_keyboard = True
                        if k.description == 'Attack':
                            grenade = True
                        if k.description == 'Defend':
                            shoot = True
                        if k.description == 'Trainer':  # and not draw_menu_keyboard:
                            draw_menu_keyboard = not draw_menu_keyboard

                        # if k.description == 'Show TM' and draw_menu_keyboard:
                        #   draw_menu_keyboard = False

                except ValueError:
                    k.keyboard = k.default
                    start_ticks_key_error = pygame.time.get_ticks()
                    k.error_key = True

        if event.type == pygame.KEYUP:
            for k in SETTINGS.key_obj_lst:
                if event.key == pygame.key.key_code(k.keyboard):

                    if k.description == 'Moving Right':  # d
                        moving_right = False
                    if k.description == 'Moving Left':  # a
                        moving_left = False
                    if k.description == 'Throw Pokeball':  # p
                        pokeball_throw_keyboard = False
                    if k.description == 'Attack':  # q
                        grenade = False
                        grenade_thrown = False
                    if k.description == 'Defend':  # r
                        shoot = False

    # pygame.draw.circle(screen, (25,25,55), (100, 100), event_timer_tm1, 0)
    ##    if trainer.tm_lst:
    ##        trainer.draw_menue()
    pygame.display.update()

pygame.quit()
import pygame
from pygame import mixer
import os
import random
import csv
import button
from pokemondata import *
import SETTINGS

mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Benny's pokemon")

'''
BUGS:
priority 1-10 (1 is high....10 is low )

3. music - 9
4. settings - need to fix low screen view - 8
8. need to blit image in red before and after cathing pokemon animation - 10
9. need to fix speed in state page also seems that other stats have same issue as speed when user in high lvl-  5
10. continue to part 9 : error detection division by zero 

# need to do next

3. replace character - p2
4. more moves - p8
5. moves cooldown and enrgy reduction and regenration (currently for eng only) - p5
6. fly typ - fly abilty , water typ - swim ability - p9
7. more animation for characters and more pokemoon to add -p10
8. moves animation -p10


# currently work on :
tm_timers draw are on pause due to thinking on other view methode


'''

# define game variable
clock = pygame.time.Clock()
FPS = 60

MAX_LEVELS = 3
# img_directoriy = r'C:\Users\benny\Desktop\Python39\פייתון למתחילים\pygame projects\pygame2\youtube scrolling\images'
img_directoriy = r'C:\Users\benny\Desktop\python\pygame_project\images'
GRAVITY = 0.5
SCROLL_TRESH = SCREEN_WIDTH // 2  # the distance the player get to the edge of the screen
# TILE_SIZE = 40
level = 1
ROWS = 16  # MUST BE cording lvl editor
COLS = 150  # according lvl editor
TILE_SIZE = SCREEN_HEIGHT // (ROWS)  # -1.2)
TYLE_TYPES = len(os.listdir('images\\game_background1\\tiles')) + len(os.listdir('images\\game_background1\\tiles'))
screen_scroll = 0
bg_scroll = 0
start_game = False
start_intro = False
pygame.time.set_timer(pygame.USEREVENT, 1000)
pygame.time.set_timer(pygame.USEREVENT + 2, 100)

event_timer_s = 0
event_timer_a = 0
event_timer_d = 0
event_timer_sp = 0
event_timer_spd = 0
# event_timer_tm1 = 0

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
menu_SIZE = 0.5 * TILE_SIZE
# party_1_lvl_100 = []
# party_2_lvl_100 = []
# party_3_lvl_100 = []
# party_4_lvl_100 = []
# party_5_lvl_100 = []
# party_6_lvl_100 = []
# party_states_lvl100_lst = [party_1_lvl_100,party_2_lvl_100,party_3_lvl_100,party_4_lvl_100,party_5_lvl_100,party_6_lvl_100]
party_states_lvl100_lst = [[], [], [], [], [], []]
party_lst = []
# switch_pokemon = 0
# party_i = 0 #index for next pokemon party
# player_once_lvl = 6 # just for begining of the game it help me to defince enemy lvl. this value update at end of each lvl

##methode = 5 # related to states page
##change_methode = 1 #same as methode


##throw_pokeball = False

# define player action variables:
moving_left = False  # at the begining the player didnt move
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
pokeball_throw_keyboard = False
draw_menu_keyboard = False
second_for_energy = False
##cathing_animation_time = 0
# pokeball_thrown = False

no_enemy = False
##test_del_TM = False


# load images
# thundershock
lst_251 = ['0', 'Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle', 'Wartortle',
           'Blastoise', 'Caterpie', 'Metapod',
           'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto', 'Pidgeot', 'Rattata', 'Raticate',
           'Spearow', 'Fearow', 'Ekans', 'Arbok',
           'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'Nidoran♀', 'Nidorina', 'Nidoqueen', 'Nidoran♂', 'Nidorino',
           'Nidoking', 'Clefairy', 'Clefable',
           'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume',
           'Paras', 'Parasect', 'Venonat',
           'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 'Primeape',
           'Growlithe', 'Arcanine', 'Poliwag',
           'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 'Machoke', 'Machamp', 'Bellsprout',
           'Weepinbell', 'Victreebel',
           'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro',
           'Magnemite', 'Magneton',
           "Farfetch'd", 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly',
           'Haunter', 'Gengar', 'Onix', 'Drowzee',
           'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak',
           'Hitmonlee', 'Hitmonchan', 'Lickitung',
           'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen',
           'Seaking', 'Staryu', 'Starmie',
           'Mr.Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 'Lapras',
           'Ditto', 'Eevee', 'Vaporeon',
           'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax',
           'Articuno', 'Zapdos', 'Moltres',
           'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew', 'Chikorita', 'Bayleef', 'Meganium', 'Cyndaquil',
           'Quilava', 'Typhlosion', 'Totodile',
           'Croconaw', 'Feraligatr', 'Sentret', 'Furret', 'Hoothoot', 'Noctowl', 'Ledyba', 'Ledian', 'Spinarak',
           'Ariados', 'Crobat', 'Chinchou',
           'Lanturn', 'Pichu', 'Cleffa', 'Igglybuff', 'Togepi', 'Togetic', 'Natu', 'Xatu', 'Mareep', 'Flaaffy',
           'Ampharos', 'Bellossom', 'Marill',
           'Azumarill', 'Sudowoodo', 'Politoed', 'Hoppip', 'Skiploom', 'Jumpluff', 'Aipom', 'Sunkern', 'Sunflora',
           'Yanma', 'Wooper', 'Quagsire',
           'Espeon', 'Umbreon', 'Murkrow', 'Slowking', 'Misdreavus', 'Unown', 'Wobbuffet', 'Girafarig', 'Pineco',
           'Forretress', 'Dunsparce', 'Gligar',
           'Steelix', 'Snubbull', 'Granbull', 'Qwilfish', 'Scizor', 'Shuckle', 'Heracross', 'Sneasel', 'Teddiursa',
           'Ursaring', 'Slugma', 'Magcargo',
           'Swinub', 'Piloswine', 'Corsola', 'Remoraid', 'Octillery', 'Delibird', 'Mantine', 'Skarmory', 'Houndour',
           'Houndoom', 'Kingdra', 'Phanpy',
           'Donphan', 'Porygon2', 'Stantler', 'Smeargle', 'Tyrogue', 'Hitmontop', 'Smoochum', 'Elekid', 'Magby',
           'Miltank', 'Blissey', 'Raikou', 'Entei',
           'Suicune', 'Larvitar', 'Pupitar', 'Tyranitar', 'Lugia', 'Ho-Oh', 'Celebi']

# define a dict for connect ebemy name to the current tile position (from level editor)
enemy_collection = dict()

# define a dict for connect enemy name to thier original states and typs
pokemon_collection = dict(zip(lst_251[0:len(pokemon_object_lst)], pokemon_object_lst))
# pokemon_object_list imported from pokemondata

# print(pokemon_collection['Bulbasaur'].speed)

# define colours: (rgb - red,blue,green)
BG = (25, 125, 215)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN2 = (90, 201, 75)
WHITE = (250, 250, 250)
BLACK = (25, 25, 25)
BLUE = (0, 50, 250)
PINK = (235, 65, 54)
GRAY = (125, 125, 250)
set_color = (250, 250, 250)

BG_MUSIC = ['open game', '103-professor oak', 'title_screen', 'viridian', 'gym', 'center']

# load music and sounds
##game_music = pygame.mixer.music.load('audio\\title_screen.mp3')
##open_screen_music = pygame.mixer.music.load('audio\\open game.mp3')
##choosepokemon_music = pygame.mixer.music.load('audio\\103-professor oak.mp3')
##
###define bg music
##open_screen_music = pygame.mixer.music.set_volume(0.3)
##game_music = pygame.mixer.music.set_volume(0.3)
##choosepokemon_music = pygame.mixer.music.set_volume(0.3)
###active music func
##pygame.mixer.music.set_volume(0.3)
##pygame.mixer.music.play(-1,0.0,5000) # ( -1 = loop forever , 0.0 = delay , "kind of accelreation to full volume)

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

sound_volume_lst = [jump_fx, jump_water_fx, falling_fx, shooting_fx, item_fx, end_lvl_fx, wall_bump_fx,
                    pokemon_lvl_up_fx, bulba_fx, caught_pokemon_fx]

##LOAD IMAGES
main_bg_img = pygame.image.load('images\\game_background1\\main_bg.png').convert_alpha()
pokemon_bg_img = pygame.image.load('images\\game_background1\\pokemon_bg.png').convert_alpha()
choose_starter_img = pygame.image.load('images\\game_background1\\choose starter.png').convert_alpha()
oak_img = pygame.image.load('images\\game_background1\\oak.png').convert_alpha()
controller_setting_bg_image = pygame.image.load('images\\game_background1\\setting_control_bg.jpg')
# controller_setting_bg_image = pygame.transform.scale(controller_setting_bg_image,(pygame.display.get_surface().get_size()))


bulba_img = pygame.image.load('images\\game_background1\\starters\\bulba starter.png').convert_alpha()
squir_img = pygame.image.load('images\\game_background1\\starters\\squir starter.png').convert_alpha()
charma_img = pygame.image.load('images\\game_background1\\starters\\charma starter.png').convert_alpha()
pikca_img = pygame.image.load('images\\game_background1\\starters\\pikca starter.png').convert_alpha()
# button images
start_img = pygame.image.load('images\\game_background1\\start_btn.png').convert_alpha()
exit_img = pygame.image.load('images\\game_background1\\exit_btn.png').convert_alpha()
restart_img = pygame.image.load('images\\game_background1\\restart_btn.png').convert_alpha()
fullscreen_img = pygame.image.load('images\\buttons\\full_screen_btn.png').convert_alpha()

left_ball_img = pygame.image.load('images\\game_background1\\starters\\left_ball.png').convert_alpha()
center_ball_img = pygame.image.load('images\\game_background1\\starters\\center_ball.png').convert_alpha()
right_ball_img = pygame.image.load('images\\game_background1\\starters\\right_ball.png').convert_alpha()

# pokemon types images from spritesheet
types_img_1 = pygame.image.load(r'images\type_icons\types.png').convert_alpha()
types_img_2 = pygame.image.load(r'images\type_icons\type_icons.png').convert_alpha()
types_img_2 = pygame.transform.scale(types_img_2, (800, 200))
icon_img_dict = {'bug': [(3, 0), (2, 60)], 'dark': [(90, 0), (805, 105)], 'dragon': [(180, 0), (605, 105)],
                 'electric': [(270, 0), (2, 105)] \
    , 'fairy': [(360, 0), (1006, 105)], 'fight': [(450, 0), (203, 15)], 'fire': [(540, 0), (605, 60)],
                 'fly': [(630, 0), (403, 15)] \
    , 'steel': [(720, 0), (403, 15)], 'rock': [(720, 100), (1006, 15)], 'psychic': [(630, 100), (203, 15)],
                 'poison': [(540, 100), (605, 15)] \
    , 'normal': [(450, 100), (2, 15)], 'ice': [(360, 100), (403, 105)], 'ground': [(270, 100), (805, 15)],
                 'grass': [(180, 100), (1006, 60)] \
    , 'ghost': [(90, 100), (203, 60)], 'water': [(0, 100), (805, 60)]}


def get_image(sheet, pokemon_type, width, height, scalex,
              scaley):  # this function called in pokemoninparty page and maybe in menu draw
    framex, framey = pokemon_type
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (framex, framey, width, height))

    if scalex is not None:
        image = pygame.transform.scale(image, (scalex, scaley))
    image.set_colorkey((0, 0, 0))

    return image


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

# define font
font1 = pygame.font.SysFont('Futura', 35)
font = pygame.font.SysFont('Futura', 30)
font_2 = pygame.font.SysFont('Futura', 15)
font_tm = pygame.font.SysFont('Futura', 18)
font_enemy = pygame.font.SysFont('Futura', 20)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_multyline_text(surface, text, word_pos, font, color, max_width, max_height, rect_pos=None,
                        button_rect_color=None, text2=None):
    ##    x_fixed , y_fixed = s
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    # max_width , max_height = 200,100
    # word_pos = (500,10)
    a, b = word_pos
    # words_size_total = []
    for line in words:
        for word in line:
            # print(word)
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if a + word_width >= max_width + word_pos[0]:
                # print(max_width , word_width , max_width > word_width)
                a = word_pos[0]  # reset a
                b += word_height  # start new row
            screen.blit(word_surface, (a, b))
            a += word_width + space
        a = word_pos[0]  # reset a
        b += word_height  # start on new row
        # print(a,b)

    # sum_size = [sum(x) for x in zip(*words_size_total)]
    # print(sum_size)

    if rect_pos is not None:
        # rect_with_color = (200,200,200,100)
        fixed_x, fixed_y = rect_pos  # fixed position between screen and surface in screen

        rect_color_big = pygame.Rect(word_pos[0] - 20 - fixed_x, word_pos[1] - 20 - fixed_y, max_width + 20,
                                     b + 20 - word_pos[1])
        # print(rect_color_big.topleft)
        if button_rect_color is not None:
            rect_color_big.h = b - word_pos[1] + 60

        pygame.draw.rect(surface, (200, 200, 200, 60), (rect_color_big), 0, 2, 2, 2, 2)
        pygame.draw.rect(surface, (255, 188, 0), rect_color_big, 2, 2, 2, 2, 2)

        if button_rect_color is not None:
            left_rect_color_small = pygame.Rect(rect_color_big.x + 10 + fixed_x, fixed_y + rect_color_big.bottom - 35,
                                                50, 28)
            right_rect_color_small = pygame.Rect(rect_color_big.right - 60 + fixed_x,
                                                 fixed_y + rect_color_big.bottom - 35, 50, 28)

            text_left = font.render(text2[0], True, color)
            text_right = font.render(text2[1], True, color)
            text_left_rect = text_left.get_rect(center=left_rect_color_small.center)
            text_right_rect = text_right.get_rect(center=right_rect_color_small.center)

            pygame.draw.rect(screen, button_rect_color, left_rect_color_small, 0, 2, 2, 2, 2)
            pygame.draw.rect(screen, (255, 188, 0), left_rect_color_small, 2, 2, 2, 2, 2)
            pygame.draw.rect(screen, button_rect_color, right_rect_color_small, 0, 2, 2, 2, 2)
            pygame.draw.rect(screen, (255, 188, 0), right_rect_color_small, 2, 2, 2, 2, 2)

            screen.blit(text_left, text_left_rect)
            screen.blit(text_right, text_right_rect)
            return left_rect_color_small, right_rect_color_small


def Music_stop():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()


def Music_start(bg_music):
    pygame.mixer.music.load(f'audio\\game music\\{bg_music}.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)


##_currently_playing_song = None

##def Game_musics():
##    global _currently_playing_song, BG_MUSIC
##    next_song = random.choice(BG_MUSIC[2:])
##
##    while next_song == _currently_playing_song:
##        next_song = random.choice(BG_MUSIC[2:])
##    _currently_playing_song = next_song
##    pygame.mixer.music.load(f'audio\\game music\\{next_song}.mp3')
##    pygame.mixer.music.play()

current_list = []


def Game_musics():
    global current_list
    if not current_list:
        current_list = BG_MUSIC[2:]
        random.shuffle(current_list)

    song = current_list[0]
    current_list.pop(0)
    pygame.mixer.music.load(f'audio\\game music\\{song}.mp3')
    pygame.mixer.music.play()

##    if not pygame.mixer.music.get_busy():
##        pygame.mixer.music.play()

def draw_bg():
    # screen.fill(BG)
    img1, img2, img3, img4 = style_winter1
    screen_w = pygame.display.get_surface().get_size()[0]
    screen.fill(BG)
    width = img1.get_width()
    for x in range(5):  # anynumber can be
        screen.blit(img1, ((width * x) - bg_scroll * 0.5, 0))
        if img2 is not None:
            screen.blit(img2, ((width * x) - bg_scroll * 0.6, img1.get_height() - 300))
        if img3 is not None:
            if img2 is not None:
                img3_y = img2.get_height()
            else:
                img3_y = 250
            screen.blit(img3, ((width * x) - bg_scroll * 0.7, img3_y + img1.get_height() - 400))
        if img4 is not None:
            screen.blit(img4, ((width * x) - bg_scroll * 0.8, SCREEN_HEIGHT - img4.get_height()))

    # winter effect if style is winter style

    for i in range(len(snowFall)):
        if i % 2 == 0:
            size = 2
        elif i % 3:
            size = 4
        else:
            size = 3
        pygame.draw.circle(screen, (random.randint(235, 255), random.randint(235, 255), random.randint(235, 255)),
                           snowFall[i], size)

        snowFall[i][1] += 1
        # snowFall[i][0] += 0.3 + screen_scroll/10
        if snowFall[i][1] > SCREEN_HEIGHT:
            snowFall[i][1] = 0
            snowFall[i][0] = random.randrange(-100, SCREEN_WIDTH)


def draw_menue():
    pos = pygame.mouse.get_pos()
    width_rect = 550
    height_rect = 1.5 * TILE_SIZE
    x_cord, y_cord = pygame.display.get_surface().get_size()
    menue_rect = pygame.Rect(x_cord // 2 + screen_scroll - (width_rect // 2), y_cord - height_rect - 25, width_rect,
                             height_rect)
    # small_rect = pygame.Rect(pygame.display.get_surface().get_size()[0]//2 + screen_scroll -40,0,40,5)

    menue_color = (0, 100, 250, 128)

    size = width, height = (pygame.display.get_surface().get_size())
    # size = width, height = (800,600)
    my_image = pygame.Surface(size, pygame.SRCALPHA)

    # Btn and moves obj
    potion_btn = button.Button(menue_rect.right + 10, menue_rect.y, potion_img, 0.2, 0.2)
    pokeball_btn = button.Button(menue_rect.right + 10, menue_rect.y + 25, pokeball_img, 0.2, 0.2)
    pokemon_party_btn = button.Button(menue_rect.left + 10, menue_rect.y + 10, pokemon_party_img, 0.3, 0.3)

    for tm_lvl in player.tm_lvl_dict.keys():
        if player.lvl >= tm_lvl and player.tm_lvl_dict[tm_lvl] not in player.TM_LST and len(player.TM_LST) <= 8:
            player.TM_LST.append(player.tm_lvl_dict[tm_lvl])

        if player.lvl == tm_lvl and player.exp < 150:
            player.exp += 1
            # put sound - dont forget connect that sound to settings .and notice user
            text_new_tm = f'{player.char_type} learned {player.tm_lvl_dict[tm_lvl].text}'
            if player.exp == 1:
                print(text_new_tm)

            if len(player.TM_LST) == 8 and player.exp > 140:
                # need to add sound for reminder
                pygame.draw.rect(screen, (20, 20, 20), (0, 0, SCREEN_WIDTH, 35), 0, 4)
                pygame.draw.rect(screen, (200, 200, 200), (2, 2, SCREEN_WIDTH - 2, 33), 2, 4)
                pygame.draw.rect(screen, (250, 250, 250), (6, 6, SCREEN_WIDTH - 6, 28), 1, 4)
                text_new_tm = f'Reminder: {player.char_type} Cant remmber more then 8 moves.'
                if player.exp > 148:
                    pygame.time.delay(3000)

            text_new_tm = font.render(text_new_tm, True, WHITE)
            screen.blit(text_new_tm, (int((width / 2) - (text_new_tm.get_width() / 2)), 10))

    # if "t" keyboard or mouse colid : user will see menue of tm , pokebal,potion and party btn . Note: all trainer command got trough this command beside moves
    if pos[1] > menue_rect.y - 10 or draw_menu_keyboard:
        pygame.draw.rect(my_image, menue_color, menue_rect, 0, 0, 10, 10, 0)
        if pokemon_party_btn.draw(screen):
            pause_from_pokemon_party_btn = True
            pause_activate = True
            return pause_from_pokemon_party_btn, pause_activate
        # use_item_btn(menue_rect)
        if potion_btn.draw(screen) and player.potion > 0:
            if player.health < player.max_health:
                player.health += 10
            else:
                player.health = player.max_health

            player.potion -= 1

        draw_text("X", font_2, WHITE, menue_rect.right + 40, menue_rect.y + 7)
        draw_text(f"{player.potion}", font1, WHITE, menue_rect.right + 55, menue_rect.y)

        if (pokeball_btn.draw(
                screen) or pokeball_throw_keyboard) and player.pokeball > 0 and player.pokeball_thrown == False:
            pokeball = POKEBALL(player.rect.centerx - int(player.direction * player.rect.size[0] * 0.5),
                                player.rect.top, player.direction)
            pokeball_group.add(pokeball)
            # pokeball_thrown = True
            player.pokeball -= 1
            player.pokeball_thrown = True

        draw_text("X", font_2, WHITE, menue_rect.right + 40, menue_rect.y + 37)
        draw_text(f"{player.pokeball}", font1, WHITE, menue_rect.right + 55, menue_rect.y + 30)

        # define rect where tm1 and other tm's will be draw according this rect
        rect_tm1 = pygame.Rect(menue_rect.x + 65, menue_rect.y + 5, 100, 65)

        for i, lvl in enumerate(player.TM_LST[:4]):
            rect_tm1.x = menue_rect.x + 65 + (i * 110)
            tm_icon = get_image(types_img_2, icon_img_dict[lvl.type][0], 90, 90, 20, 20)
            screen.blit(tm_icon, (menue_rect.x + 68 + (i * 110), rect_tm1.y + 3))
            if lvl.category == "special":
                img_1 = special_tm_img
            elif lvl.category == "pysical":
                img_1 = pysical_tm_img
            else:
                img_1 = status_tm_img

            player.TM_LST[i].draw(rect_tm1, my_image, player, img_1)
            if rect_tm1.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                player.TM_LST[i].clicked = True
                print(id(player.TM_LST))
                # player.shoot()

    screen.blit(my_image, (0, 0))
    return False, False


# function to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    item_box_group.empty()
    water_group.empty()
    decoration_group.empty()
    exit_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS + 1):
        r = [-1] * COLS
        data.append(r)
    return data


# Formula to calculate the exp for next lvl
def lvl_up_pts(n):
    return n * (100 + n ** 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, char, x, y, hp, scale, speed, fake_speed, ammo, grenades, typ1, typ2, energy, atk,
                 deff, spa, spd, tm_lvl_dict):  # ,x_states,y_states):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.char = char
        self.shoot_cooldown = 20
        self.health = hp
        self.max_health = self.health
        self.speed = speed
        self.start_speed = speed

        self.ammo = ammo  # energy
        self.start_ammo = ammo
        self.grenades = grenades
        self.direction = 1
        self.jump = False
        self.vel_y = 0  # velocity in y direction -for jumping
        self.in_air = True  # for jump animation see part3 youtube 39:10
        self.flip = False
        self.animation_list = []
        # self.animation_list_states = [] #idle and run only without scaling
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # self.update_energy_time = 0
        self.altitude = 0
        self.altitude_damage = False
        # create ai specified self variabels
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 550, 20)  # the ai vision rect
        self.idling = False
        self.idling_counter = 0

        self.typ1 = typ1
        self.typ2 = typ2
        self.max_energy = energy
        self.energy = energy

        self.atk = atk
        self.deff = deff
        self.spa = spa
        self.spd = spd
        self.fake_speed = fake_speed

        self.start_atk = atk
        self.start_deff = deff
        self.start_spa = spa
        self.start_spd = spd
        self.max_fake_speed = fake_speed
        self.exp = 0
        self.lvl = 5
        self.reg = 1

        self.potion = 0
        self.pokeball = 6
        self.stop_draw = False
        self.in_pokeball = False
        self.pokeball_thrown = False

        self.gender = random.choice(['female', 'male', 'male'])

        self.collidWithPokeball = 0

        animation_types = ['idle', 'run', 'jump', 'death', 'atk']  # name of folders contain images for frames

        for animation in animation_types:
            # count numbers of files in folder
            num_of_frames = os.listdir('images\\pokemon_images\\' + self.char_type + '\\' + animation)
            for png in num_of_frames:  # my extra for me to ignore files that not png such archive folder
                if 'png' not in png:
                    num_of_frames.remove(png)
            # print(num_of_frames)
            temp_list = []
            for i in range(len(num_of_frames)):
                img = pygame.image.load(
                    'images\\pokemon_images\\' + self.char_type + f'\\{animation}\\{i}.png').convert_alpha()  # added from part4 only "convert_alpha()"
                # img = pygame.transform.scale(img,(int(img.get_width()*0.2),int(img.get_height()*0.2))) # image according screen scale
                img = pygame.transform.scale(img, (
                int(TILE_SIZE * scale), int(TILE_SIZE * scale)))  # image according screen scale
                temp_list.append(img)
            self.animation_list.append(temp_list)

        ##        for i in range(3):
        ##            img_for_states = pygame.image.load('images\\pokemon_images\\' + self.char_type + f'\\idle\\{i}.png').convert_alpha()
        ##            self.animation_list_states.append(img_for_states)

        self.img = self.animation_list[self.action][self.index]
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

        '''
        instance to add
        ,lvl_100_states
        '''
        # Party members photos
        self.img_for_states = pygame.image.load(
            'images\\pokemon_images\\' + self.char_type + '\\idle\\0.png').convert_alpha()  # main img
        self.char_img_s = pygame.transform.scale(self.img_for_states, (45, 45))  # for left side small photo
        self.char_img_l = pygame.transform.scale(self.img_for_states, (250, 250))  # for center large photo
        self.char_img_l_rect = self.char_img_l.get_rect()
        self.char_img_l_rect.center = (800, 350)
        # party member present in screen
        # self.clicked = False
        self.state_blit = False
        self.index_methode = 0
        # self.lvl_100_states = lvl_100_states if is not None else 100

        self.tm_lvl_dict = tm_lvl_dict
        self.TM_LST = []

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):

        screen_scroll = 0

        dx = 0
        dy = 0
        altitude = 75

        # assign movment variables
        if moving_left and self.rect.left > 0:
            dx = -self.speed
            self.flip = True
            self.direction = 1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = -1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY

        if self.vel_y > 10:
            self.vel_y = 0

        altitude_damage = 0
        dy = self.vel_y
        self.altitude += 1
        if self.altitude > altitude and not pygame.sprite.spritecollide(self, water_group,
                                                                        False) and self.char == 'player' and \
                'fly' not in [self.typ1, self.typ2]:
            self.altitude_damage = True
            altitude_damage = self.altitude - altitude
        else:
            self.altitude_damage = False

        # check for collision
        for tile in world.obstacle_list:
            # x direction

            # if tile[1].colliderect(self.rect.x + dx ,self.rect.y,self.img.get_width(),self.img.get_height()):
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
                if self.char == 'player':
                    wall_bump_fx.play()
            # y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.altitude_damage:
                    self.health -= altitude_damage
                    self.altitude_damage = False
                    print('damaege from falling from hight alltittude', altitude_damage)
                    pygame.draw.rect(screen, RED, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
                    if self.char == 'player':
                        falling_fx.play()
                self.altitude = 0

                # check if below the ground , i.e jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    wall_bump_fx.play()
                # check if above the ground i.e falling
                elif self.vel_y >= 0:
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # check for collide with water (if not a water type)
        if pygame.sprite.spritecollide(self, water_group, False) and (self.typ1 != 'water' and self.typ2 != 'water'):
            water_weak = ['fire', 'ground', 'rock']
            if self.typ1 in water_weak or self.typ2 in water_weak:
                water_damage = 1
            else:
                water_damage = 0.2
            if self.energy >= water_damage:
                self.energy -= water_damage * 0.5
            self.health -= water_damage
            jump_water_fx.play()

        # check if fall of screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
            if self.exp > 10 * (level ** 2) / 3:
                self.exp -= 10 * (level ** 2) / 3
            else:
                self.exp = 0

        # check collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False) and len(enemy_group) == 0:
            level_complete = True
            end_lvl_fx.play()
            self.exp += 100 * (level ** 2) / 3

        # update scroll based on player position
        if self.char == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_TRESH and bg_scroll < (
                    world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_TRESH and bg_scroll >= abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20

            bullet = Bullet(self.rect.centerx + (1.5 * self.rect.size[0] * -self.direction), self.rect.centery + 10,
                            self.direction, (self.img.get_width(), self.img.get_height()))
            bullet_group.add(bullet)
            # reduce ammo each shoot
            self.ammo -= 1
            shooting_fx.play()
            self.energy -= 1
            # self.energy -= TM1_TIMER.eng

    def ai(self):  # ,ai_lvl,player_once_lvl):
        # self.lvl = level +  ai_lvl + player_once_lvl #player_once_lvl is a number that arrive at the begining of new lvl

        if self.alive and player.alive:

            for tm_lvl in self.tm_lvl_dict.keys():
                if self.lvl >= tm_lvl and self.tm_lvl_dict[tm_lvl] not in self.TM_LST:
                    self.TM_LST.append(self.tm_lvl_dict[tm_lvl])

            if self.idling == False and random.randint(1, 50) == 10:
                self.idling = True
                self.update_action(0)
                self.idling_counter = 50

            # check if the AI is near the player
            if self.vision.colliderect(player.rect) and random.randint(1, 20) == 10:
                # stop running and face the player
                self.update_action(4)

                # shoot
                # self.shoot()

                # jump
                if player.jump == True and self.in_air == False:  # and random.randint(1,3) == 2:
                    self.vel_y = -11
                    self.in_air = True
                    self.in_air = True

                # apply gravity

                self.vel_y += GRAVITY * 1.1

                if self.vel_y > 10:
                    self.vel_y = 0
                    self.in_air = False
                dy = self.vel_y

                for tile in world.obstacle_list:
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):

                        if self.vel_y < 0:
                            self.vel_y = 0
                            dy = tile[1].bottom - self.rect.top
                            # self.in_air = False

                        # check if above the ground i.e falling
                        elif self.vel_y >= 0:

                            # self.vel_y = 0
                            self.in_air = False
                            # pygame.draw.rect(screen,RED,tile[1])
                            dy = tile[1].top - self.rect.bottom
                self.rect.y += dy
            else:

                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = False
                    else:
                        ai_moving_right = True

                    self.update_action(1)  # 1 : run , 0: idle *dont have run animation yet
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.move_counter += 1

                    # update ai vision (x,y ) as the enemy moves while the width of this rect define in init methode above (for shooting when im in thier sig
                    self.vision.center = (self.rect.centerx + 75 * -self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter < 0:
                        self.idling = False

        else:
            self.max_health += -2  # just for timer
            if self.max_health <= 0:
                player.exp += self.lvl * 20 * (level ** 2) / 3
                self.kill()

        # scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        # update image dpending on current frameddd
        self.img = self.animation_list[self.action][self.index]

        # check if enogh time passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.index += 1
            # reset timer
            self.update_time = pygame.time.get_ticks()
        if self.index == len(self.animation_list[self.action]):
            self.index = 0

    def update_action(self, new_action):
        # check if new action is different from the previews
        if new_action != self.action:
            self.action = new_action
            # updtae animation settings
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def update_energy(self):
        if self.energy < self.max_energy:
            self.energy += self.reg / 10
            if self.energy >= self.max_energy:
                self.energy = self.max_energy

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.index = 1
            self.action = 3

    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)

    def PokemonInParty(self, x, y, lvl_100_states):
        action = False

        # i have img for that but for run time is better to draw
        # screen.blit(pokemon_in_party_img,(x,y-3)) # pokemon_in_party_img :
        pygame.draw.rect(screen, (230, 230, 230), (x, y, 370, 78), 0, 39)

        pos_on_pokemon_rect = pygame.Rect(x, y, 370, 78)

        pos = pygame.mouse.get_pos()

        if pos_on_pokemon_rect.collidepoint(pos):
            pygame.draw.rect(screen, (25, 25, 25), pos_on_pokemon_rect, 0, 39)
            if pygame.mouse.get_pressed()[2]:
                self.state_blit = True

            color = (250, 250, 250)

        else:
            color = (25, 25, 25)
            if pygame.mouse.get_pressed()[2]:
                self.state_blit = False

        health_green = 220 * self.health / self.max_health

        # bliting pok data(hp,gender,lvl etc) the left side of the page
        screen.blit(self.char_img_s, (x + 35, y + 20))
        pygame.draw.line(screen, (255, 10, 0), (x + 85, y + 41), (int(x + 85 + 220), y + 41), 8)
        pygame.draw.line(screen, (68, 255, 0), (x + 85, y + 40), (int(x + 85 + health_green), y + 40), 10)

        name_text = font2_n.render(self.char_type, True, color)
        lv_text = font2_n.render(f"Lv. {self.lvl}", True, color)
        health_text = font2_n.render(f'{int(self.health)}/{self.max_health}', True, color)

        # draw gender
        if self.gender in ['male', 'Male', 'MALE']:
            gender = font5_g.render('\u2642', True, WHITE)  # male
            g_color = (0, 0, 255)
        else:
            gender = font5_g.render(chr(0x2640), True, WHITE)  # female
            g_color = (255, 0, 0)

        gender_rect = gender.get_rect()
        gender_rect.center = (x + 280, y + 23)

        screen.blit(name_text, (x + 85, y + 11))
        screen.blit(lv_text, (x + 285, y + 50))
        screen.blit(health_text, (x + 85, y + 50))

        pygame.draw.circle(screen, g_color, (gender_rect.center), 11)
        screen.blit(gender, gender_rect)

        if self.state_blit:
            # define Trigo
            cos30 = (3 ** 0.5) / 2
            tan30 = (3 ** 0.5) / 3

            # Center of polygone
            cx = 990
            cy = 170

            # polygone variable (x only)
            X = 110

            # affected from x
            V = X / cos30
            Y = -((V ** 2) - (X ** 2)) ** 0.5

            # define colors
            bg_color = (225, 254, 250)
            gray = (229, 229, 229)

            # size = width, height = (surf_WIDTH+300, surf_HEIGHT) pygame.display.get_surface().get_size()
            size = width, height = (pygame.display.get_surface().get_size())
            # size = width, height = (800,600)
            my_image = pygame.Surface(size, pygame.SRCALPHA)  # Creates an empty per-pixel alpha Surface.
            # transperent polygon - actual pokemon states

            screen.blit(self.char_img_l, (850, 330))

            type_icon = get_image(types_img_1, icon_img_dict[self.typ1][1], 200, 44, 100, 30)
            screen.blit(type_icon, (980, 588))

            if self.typ2 != '':
                type2_icon = get_image(types_img_1, icon_img_dict[self.typ2][1], 200, 44, 100, 30)
                screen.blit(type2_icon, (1080, 588))

            methode_lst = [1, 2, 3, 4, 5, 6]
            # define states related to V
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # and change_methode < methode:
                        self.index_methode += 1
                        if self.index_methode > len(methode_lst) - 1:
                            self.index_methode = 0
                    if event.key == pygame.K_DOWN:
                        self.index_methode -= 1
                        if self.index_methode < 0:
                            self.index_methode = len(methode_lst) - 1

                    if event.key == pygame.K_ESCAPE:
                        global pause_activate
                        pause_activate = False

            if methode_lst[self.index_methode] == 2:
                ##self.lvl_100_states[self.hp,self.atk,self.deff,self.spa,self.spd,self.speed,self.energy]
                # comparison to lvl 100
                hp1 = int(V * self.max_health / lvl_100_states[0])
                atk1 = int(X * self.atk / lvl_100_states[1])
                deff1 = int(X * self.deff / lvl_100_states[2])
                spa1 = int(X * self.spa / lvl_100_states[3])
                spd1 = int(X * self.spd / lvl_100_states[4])
                speed1 = int(self.fake_speed * V / (lvl_100_states[8]))

                BLUE = (0, 50, 255, 100)  # transperent color on new surface "my_image"
                COLOR_POLYGONE = BLUE
                states_methode_text = font2_n.render('Normal', True, COLOR_POLYGONE)
                # description_state_text = font2_n.render('Blue: Each state compared to same state in maximum level and power.',True,BLACK)
                text = 'States compared to same maximum state.\nin maximum level and power.\n'

            elif methode_lst[self.index_methode] == 1:
                # comparison to his own avg in lvl 100
                # print(lvl_100_states)
                avg_states = sum(lvl_100_states) // len(lvl_100_states)
                hp1 = int(V * self.max_health / avg_states)
                atk1 = int(X * self.atk / avg_states)
                deff1 = int(X * self.deff / avg_states)
                spa1 = int(X * self.spa / avg_states)
                spd1 = int(X * self.spd / avg_states)
                speed1 = int(self.fake_speed * V / avg_states)

                YELLOW = (240, 250, 40, 100)
                COLOR_POLYGONE = YELLOW
                states_methode_text = font2_n.render('Average', True, COLOR_POLYGONE)
                # description_state_text = font2_n.render('Yellow: All states compared to average states in maximum level and power.',True,BLACK)
                text = 'States compared to average state\nin maximum level and power.\n'

            elif methode_lst[self.index_methode] == 3:
                # comparison to his own max state
                max_state = max(lvl_100_states)
                hp1 = int(V * self.max_health / max_state)
                atk1 = int(X * self.atk / max_state)
                deff1 = int(X * self.deff / max_state)
                spa1 = int(X * self.spa / max_state)
                spd1 = int(X * self.spd / max_state)
                speed1 = int(self.fake_speed * V / max_state)

                GREEN = (0, 225, 70, 100)
                COLOR_POLYGONE = GREEN
                states_methode_text = font2_n.render('Maximum', True, COLOR_POLYGONE)
                text = 'States compared to biggest state\nin maximum level and power.\n'

            elif methode_lst[self.index_methode] == 4 or methode_lst[self.index_methode] == 5:

                state_lst_text = ['HP :', 'Attack :', 'Deffence :', 'Sp.Atk :', 'Sp.Def :', 'Energy :', 'Reg-Eng :',
                                  'Speed :']
                state_lst = [self.max_health, self.atk, self.deff, self.spa, self.spd, self.energy, self.reg,
                             self.fake_speed]
                state_lst_lvl100 = [i for i in lvl_100_states if i > 20]
                # print(state_lst_lvl100)

                # table compared to lvl 100
                if methode_lst[self.index_methode] == 4:
                    # GREEN =
                    COLOR_POLYGONE = (0, 225, 70, 100)

                    lst_to_compare = state_lst_lvl100
                    division_state = max(lvl_100_states)
                    states_methode_text = font2_n.render('Est. level 100', True, COLOR_POLYGONE)
                    text = 'All states in table form.\nCompared to pokemon max state in his max level, with perfect Ev pts each during lvl-up.\n'


                # table compared to 250 num
                elif methode_lst[self.index_methode] == 5:
                    # BLUE = (0, 50, 255, 100)
                    COLOR_POLYGONE = (0, 50, 255, 100)
                    lst_to_compare = state_lst
                    division_state = 250
                    states_methode_text = font2_n.render('Base 250', True, COLOR_POLYGONE)
                    text = 'Base 250 :All current states in table form.\nCompared to 250 pts per state.'

                for i, state in enumerate(state_lst_text):
                    state_text = font2_n.render(state, True, BLACK)
                    screen.blit(state_text, (
                    880 + (font2_n.render('Reg-Eng :', True, BLACK).get_width()) - state_text.get_width(),
                    35 + (i * state_text.get_height())))
                for i, state in enumerate(lst_to_compare):
                    state_text = font2_n.render(str(int(state)), True, BLACK)
                    screen.blit(state_text, (880 + (font2_n.render('Reg-Eng :', True, BLACK).get_width()) + 5,
                                             35 + (i * state_text.get_height())))
                    state_bar_lengh = 200
                    ratio_state = state / division_state
                    if ratio_state > 0.65:
                        rect_state_color = (100, 250, 70)
                    elif ratio_state <= 0.65 and ratio_state > 0.5:
                        rect_state_color = (206, 250, 70)
                    elif ratio_state <= 0.5 and ratio_state > 0.3:
                        rect_state_color = (255, 190, 70)
                    else:
                        rect_state_color = (255, 70, 70)

                    pygame.draw.rect(screen, rect_state_color,
                                     (1005, 42 + (i * state_text.get_height()), int(ratio_state * state_bar_lengh), 15))

            elif methode_lst[self.index_methode] == 6:  # show moves
                COLOR_POLYGONE = (100, 230, 243, 100)

                states_methode_text = font2_n.render('Move Set', True, COLOR_POLYGONE)
                text = 'Pokemon Can remmber up to 8 moves.\nand use only the 4 first moves.\n\nMouse left click for re-ordering.\nDelete move - drag it to trash.\n\nTm information include:\nCategory,Energy,Regeneration and Range.'

                rect_width_TM, rect_hight_TM, space_rect_tm = 330, 70, 5

                # FAKE RECT JUST FOR COLLISION
                tm_rect_grid_lst = []
                for i in range(len(self.TM_LST)):
                    TM_RECT_grid = pygame.Rect(width - rect_width_TM, 67 + (i * (rect_hight_TM + space_rect_tm)),
                                               rect_width_TM - 180, rect_hight_TM - 50)
                    tm_rect_grid_lst.append(TM_RECT_grid)
                    # pygame.draw.rect(screen,(25,25,25),TM_RECT_grid,2,3)

                trash_del_tm_img_rect.topleft = (width // 2 - 15, height - 150)

                my_image.blit(trash_del_tm_img, trash_del_tm_img_rect)

                for i, tm in enumerate(self.TM_LST):
                    TM_RECT_PARTY_PAGE = pygame.Rect(width - rect_width_TM - 90,
                                                     42 + (i * (rect_hight_TM + space_rect_tm)), rect_width_TM,
                                                     rect_hight_TM)

                    if tm.moving_rect == False:
                        tm.rect = TM_RECT_PARTY_PAGE

                    # Re ordering moves
                    if tm.rect.collidepoint(pos) and len(self.TM_LST) > 1:
                        # print(trash_del_tm_img_rect)

                        pygame.draw.rect(screen, (25, 25, 25), tm.rect, 5, 5)
                        # self.clicked = False
                        if pygame.mouse.get_pressed()[0]:
                            tm.moving_rect = True
                            # tm.rect.centery = pos[1]
                            tm.rect.center = pos

                            ##                            if test_del_TM:
                            ##                                print('TM deleted')

                            if i > 0 and tm.rect.colliderect(tm_rect_grid_lst[i - 1]):
                                self.TM_LST[i - 1].rect.centery = tm_rect_grid_lst[i].centery
                                tm.rect.centery = tm_rect_grid_lst[i - 1].centery
                                self.TM_LST[i - 1], self.TM_LST[i] = self.TM_LST[i], self.TM_LST[i - 1]

                            if i < len(self.TM_LST) - 1 and tm.rect.colliderect(tm_rect_grid_lst[i + 1]):
                                self.TM_LST[i + 1].rect.centery = tm_rect_grid_lst[i].centery
                                tm.rect.centery = tm_rect_grid_lst[i + 1].centery
                                self.TM_LST[i + 1], self.TM_LST[i] = self.TM_LST[i], self.TM_LST[i + 1]
                        else:
                            tm.rect.center = tm_rect_grid_lst[i].center

                    if tm.category == "special":
                        img_1 = special_tm_img
                    elif tm.category == "pysical":
                        img_1 = pysical_tm_img
                    else:
                        img_1 = status_tm_img

                    # remoe moe from tm set warning
                    if trash_del_tm_img_rect.collidepoint(tm.rect.center):
                        print(tm.text, 'warning -delete move')
                        tm.RemovedByUser = True
                        warning_del_tm_rect = pygame.Rect(0, 0, 200, 100)
                        warning_del_tm_rect.center = trash_del_tm_img_rect.center
                        pygame.draw.rect(screen, (125, 125, 125, 150), warning_del_tm_rect, 0, 3)
                        pygame.draw.rect(screen, (25, 25, 25, 150), warning_del_tm_rect, 3, 3)

                    if tm.RemovedByUser:
                        warning_del_tm_text = f'{self.char_type} will forget\n            {tm.text}\n      Are you sure?'
                        # draw_multyline_text(screen,warning_del_tm_text,(warning_del_tm_rect.x+10,warning_del_tm_rect.y+20),font,BLACK,warning_del_tm_rect.w-15,warning_del_tm_rect.h-10,(10,30,240,180))
                        no_btn_del_tm, yes_btn_del_tm = draw_multyline_text(my_image, warning_del_tm_text,
                                                                            (0.5 * width - 105, 0.5 * height + 15),
                                                                            font, WHITE \
                                                                            , 210, 85, (0, 5), (30, 30, 30),
                                                                            ['No', 'Yes'])
                        if no_btn_del_tm.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                            tm.RemovedByUser = False
                        if yes_btn_del_tm.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                            # tm.RemovedByUser = False
                            self.TM_LST.remove(tm)
                            self.tm_lvl_dict = {k: v for k, v in self.tm_lvl_dict.items() if v != tm}
                            print(tm.text, 'deleted move')

                    # show tm icon
                    tm_icon = get_image(types_img_2, icon_img_dict[tm.type][0], 90, 90, 38, 38)

                    # draw all data on tm rect
                    tm.draw2(my_image, img_1, energy_tm_img, reg_tm_img, range_tm_img, tm_icon)

                    # tm_icon_rect = tm_icon.get_rect(topleft = (TM_RECT_PARTY_PAGE.x+5,TM_RECT_PARTY_PAGE.centery-8))
                    # screen.blit(tm_icon,(tm_icon_rect))

                    if trainer_box_button.draw(screen):  # trainer.tm_lst:
                        trainer.show_tm_preview = True

                    if trainer.show_tm_preview:
                        trainer.draw_menue()

            if methode_lst[self.index_methode] < 4:
                # drawing
                pygame.draw.polygon(screen, gray, [(cx + X, cy + Y), (cx + X, cy - Y), (cx, cy + V), (cx - X, cy - Y),
                                                   (cx - X, cy + Y), (cx, cy - V)])

                pygame.draw.line(screen, bg_color, (cx + X, cy + Y), (cx - X, cy - Y), 3)
                pygame.draw.line(screen, bg_color, (cx + X, cy - Y), (cx - X, cy + Y), 3)
                pygame.draw.line(screen, bg_color, (cx, cy + V), (cx, cy - V), 3)
                # draw polygone# and states methode
                pygame.draw.polygon(my_image, COLOR_POLYGONE, [(cx, cy - hp1), (cx + atk1, cy - (atk1 * tan30)),
                                                               (cx + deff1, cy + (deff1 * tan30)), (cx, cy + speed1),
                                                               (cx - spa1, cy + (spa1 * tan30)),
                                                               (cx - spd1, cy - (spd1 * tan30))])

                # draw states
                hp1 = font2_n.render('HP', True, BLACK)
                hp2 = font2_n.render(f'{int(self.health)}/{self.max_health}', True, BLACK)
                screen.blit(hp1, (cx - 10, cy - V - 40))
                screen.blit(hp2, (cx - 22, cy - V - 20))
                speed1 = font2_n.render('SPEED', True, BLACK)
                speed2 = font2_n.render(f'{self.fake_speed}', True, BLACK)
                screen.blit(speed1, (cx - 22, cy + V))
                screen.blit(speed2, (cx - 5, cy + V + 20))
                atk_spa1 = font2_n.render('Sp.Atk                                                Attack', True, BLACK)
                atk_spa2 = font2_n.render(
                    f'{int(self.spa)}                                                     {int(self.atk)}', True, BLACK)
                screen.blit(atk_spa1, (cx - X - 60, cy + Y - 30))
                screen.blit(atk_spa2, (cx - X - 40, cy + Y - 10))
                def_spd1 = font2_n.render('Sp.Def                                                Deffence', True, BLACK)
                def_spd2 = font2_n.render(
                    f'{int(self.spd)}                                                     {int(self.deff)}', True,
                    BLACK)
                screen.blit(def_spd1, (cx - X - 60, cy - Y - 30))
                screen.blit(def_spd2, (cx - X - 40, cy - Y - 10))

            # create description of each methode
            description_rect = pygame.Rect(515, 8, states_methode_text.get_width() + 17,
                                           states_methode_text.get_height() + 6)
            screen.blit(states_methode_text, (525, 10))
            pygame.draw.rect(my_image, COLOR_POLYGONE, (description_rect), 0, 2, 2, 2, 2)
            pygame.draw.rect(screen, COLOR_POLYGONE, (description_rect), 2, 2, 2, 2, 2)
            if description_rect.collidepoint(pos):
                draw_multyline_text(my_image, text, (535, 85), font0_0, BLACK, 200, 50, rect_pos=(0, 0))
            screen.blit(my_image, (0, 0))

    def HealthBar(self, a, b, z):  # ,health,max_health,energy,name):
        # update with new health
        # fixed position
        x = a + 10
        y = b + 10

        ratio = self.health / (
            self.max_health if self.max_health != 0 else 100)  # the max HP reduced to null when self.kill apearntly

        if self.max_health < 2:
            print(self.char_type, "Max HP:", self.max_health, "HP:", self.health, "Lvl", self.lvl)

        width = 180

        ##        GREEN1 = (0,255,0)
        ##        GREEN2 = (0,204,0)
        ##        GREEN3 = (0,153,0)
        ##        GREEN4 = (230,255,230)
        ##        GRAY = (110,110,110)
        ##        WHITE = (255,255,255)
        ##        BLACK = (25,25,25)

        if self.char == "enemy":

            pygame.draw.rect(screen, (110, 110, 110), (x - 40, y + z, x + 20, 14), 0, 4)
            HP_text = font0_0.render(f'{int(100 * ratio)}%', True, WHITE)
            # HP_text = font0_0.render(str(self.max_health),True,WHITE)
            screen.blit(HP_text, (x - 30, y - 1 + z))
            # print(self.max_health)
        else:
            pygame.draw.rect(screen, (110, 110, 110), (x + width - 30, y + z, x + 55, 14), 0, 4)
            HP_text = font0_0.render(f'{int(100 * ratio)}%', True, WHITE)
            screen.blit(HP_text, (x + width + 8, y - 1))

            distance = 35
            energy_ratio = self.energy / self.max_energy

            pygame.draw.rect(screen, (110, 110, 110), (x + width - 30, y + distance, x + 55, 14), 0, 4)
            energy_text = font0_0.render(f'{int(100 * energy_ratio)}%', True, WHITE)
            # energy_text = font0_0.render(str(self.character.energy),True,WHITE)
            screen.blit(energy_text, (x + width + 8, distance + y - 1))

            pygame.draw.rect(screen, (150, 150, 255), (x, y + distance, width, 15), 0, 4)  # general bar rect
            # energy bar rects with 3 colors

            pygame.draw.rect(screen, (0, 0, 153), (x, y + distance, width * energy_ratio, 15), 0, 4)
            pygame.draw.rect(screen, (0, 0, 204), (x, y + distance, width * energy_ratio, 10), 0, 4)
            pygame.draw.rect(screen, (0, 0, 255), (x, y + distance, width * energy_ratio, 8), 0, 4)

            # frame to general bar
            pygame.draw.rect(screen, WHITE, (x, y + distance, width, 15), 2, 4)
            pygame.draw.rect(screen, GRAY, (x, y + distance, width, 15), 1, 4)

        pygame.draw.rect(screen, WHITE, (x, y + z, width, 15), 0, 4)  # general bar rect
        # health bar rects with 3 colors
        pygame.draw.rect(screen, (0, 153, 0), (x, y + z, width * ratio, 15), 0, 4)
        pygame.draw.rect(screen, (0, 204, 0), (x, y + z, width * ratio, 10), 0, 4)
        pygame.draw.rect(screen, (0, 255, 0), (x, y + z, width * ratio, 8), 0, 4)

        # frame to general bar
        pygame.draw.rect(screen, WHITE, (x, y + z, width, 15), 2, 4)
        pygame.draw.rect(screen, GRAY, (x, y + z, width, 15), 1, 4)

        # good fon lst = [24,52,55,30,69,174,184]

        boost_lst = ['Atk+', 'Def+', 'Spa+', 'Spd+', 'Spe+']
        current_states = [self.atk, self.deff, self.spa, self.spd, self.speed]
        start_states = [self.start_atk, self.start_deff, self.start_spa, self.start_spd, self.start_speed]

        j = 0
        for i in range(len(start_states)):
            if i > 0:
                if current_states[i - 1] == start_states[i - 1]:
                    space = ((i - 1) * 0.225 * width)
                    j += 1
            space = ((i - j) * 0.225 * width)
            if current_states[i] > start_states[i]:
                # print('x')
                pygame.draw.rect(screen, (230, 255, 230), (x + space, y + z + 15, 0.22 * width, 15), 0,
                                 4)  # for boosting########################
                pygame.draw.rect(screen, (0, 153, 0), (x + space, y + z + 15, 0.22 * width, 15), 1,
                                 4)  # for boosting########################
                boost_text = font0_0.render(boost_lst[i], True, (0, 153, 0))
                screen.blit(boost_text, (x + 10 + space, y + z + 15))

        if self.gender in ['male', 'Male', 'MALE']:
            gender = font4_g.render('\u2642', True, (0, 153, 153))  # male
            gender2 = font5_g.render('\u2642', True, (25, 25, 25))

        else:
            gender = font4_g.render(chr(0x2640), True, (255, 0, 0))  # female
            gender2 = font5_g.render(chr(0x2640), True, (25, 25, 25))
            # g_color = (255,0,0)

        name_text0 = font1_n.render(self.char_type, True, WHITE)
        name_text1 = font2_n.render(self.char_type + '        L' + str(self.lvl), True, BLACK)

        text0_rect = name_text0.get_rect(center=(x + (width // 2) - 23, y - 14 + z))
        text1_rect = name_text0.get_rect(center=(x + (width // 2) - 20, y - 14 + z))
        gender_rect = name_text0.get_rect(center=(x + (width // 2) - 10 + font1_n.size(self.char_type)[0], y - 8 + z))

        screen.blit(name_text0, text0_rect)
        screen.blit(name_text1, text1_rect)

        screen.blit(gender2, gender_rect)
        screen.blit(gender, gender_rect)


font0_0 = pygame.font.SysFont(pygame.font.get_fonts()[0], 13)
font1_n = pygame.font.SysFont(pygame.font.get_fonts()[55], 20)
font2_n = pygame.font.SysFont(pygame.font.get_fonts()[55], 19)
font4_g = pygame.font.SysFont(pygame.font.get_fonts()[8], 23)
font5_g = pygame.font.SysFont(pygame.font.get_fonts()[8], 22)
font_big = pygame.font.SysFont(pygame.font.get_fonts()[8], 35)


######################################################################## END OF PLAYER CLASS  #################################################################3
###################################################################################################################################################3


def pause():
    transperent_screen = pygame.Surface((pygame.display.get_surface().get_size()))  # the size of your rect
    transperent_screen.set_alpha(128)  # alpha level
    transperent_screen.fill((255, 255, 255))  # this fills the entire surface
    screen.blit(transperent_screen, (0, 0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, char_size):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 20
        self.image = thundershock_img
        self.flip = False

        # self.image = pygame.transform.scale(self.image,(char_size.img.get_width()*2,char_size.img.get_height()*0.5))
        self.image = pygame.transform.scale(self.image, (char_size[0] * 2, char_size[1] * 0.5))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, d):

        if d == 1:
            self.flip = True
        else:
            self.flip = False

        self.image = pygame.transform.flip(self.image, self.flip, False)
        # move bullet
        self.rect.x += (-self.direction * self.speed) + screen_scroll

        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # check collision with levle(tile?)
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive and enemy.rect.x in range(self.rect.x - 10,
                                                         self.rect.x + 10) and enemy.stop_draw == False:
                    enemy.health -= 5
                    # print('Enemy HP:',enemy.health)
                    self.kill()


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, character):
        pygame.sprite.Sprite.__init__(self)
        self.speed = character.speed * 3
        self.image = thundershock_img
        self.range = 5
        self.duration = 30
        self.flip = False
        self.img_lst = []
        self.index = 0
        for i in range(1, self.range + 1):
            self.image = pygame.transform.scale(self.image,
                                                (character.img.get_width() * i, character.img.get_height() * 0.5))
            self.img_lst.append(self.image)

        self.image = self.img_lst[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x + (-direction * (1.5 * character.rect.width)), y + 20)
        self.direction = direction

    def update(self, d, char):

        self.index += 1

        if self.index == self.range:
            self.index = 0
        self.image = self.img_lst[self.index]

        # i choose to try this flip due to the animation effect from that
        self.image = pygame.transform.flip(self.image, True, False)

        # move bullet
        self.rect.x += (-self.direction)  # * self.speed) + screen_scroll
        self.rect.y = player.rect.y

        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # check collision with levle(tile?)
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 25
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive and enemy.stop_draw == False:
                    enemy.health -= 25
                    print('Enemy HP:', enemy.health)
                    # self.kill()
        self.duration -= 1
        if self.duration <= 0:
            self.kill()
            self.duration = 20


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -5
        self.speed = 7
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.damege = 50
        self.explosion_range = 4 * TILE_SIZE
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.vel_y += GRAVITY
        dx = self.speed * self.direction
        dy = self.vel_y

        # check collison with level
        for tile in world.obstacle_list:
            # check collision with walls
            if tile[1].colliderect(self.rect.x - dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                # check if below the ground , i.e thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    # self.speed = 0

                # check if above the ground i.e falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
                    self.speed = 0

        # pygame.draw.rect(screen,RED,self.rect,0)
        # update grenade position
        self.rect.x -= dx - screen_scroll
        self.rect.y += dy

        # countdown timer
        self.timer -= 2
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y - 3 * self.rect.size[1], 0.5, explosion_anim_direction, 0,
                                  16, 1)
            explosion_group.add(explosion)
            # do damage to anyone that is nearby
            distance_player = (((self.rect.centerx - player.rect.centerx) ** 2) + (
                        (self.rect.centery - player.rect.centery) ** 2)) ** 0.5
            if distance_player < self.explosion_range:
                damage_grenade = self.damege - (self.damege * (distance_player / self.explosion_range))
                player.health -= int(damage_grenade)
                # print('player HP:',player.health)
                # print(damage_grenade)

            for enemy in enemy_group:
                distance_enemy = (((self.rect.centerx - enemy.rect.centerx) ** 2) + (
                            (self.rect.centery - enemy.rect.centery) ** 2)) ** 0.5
                if distance_enemy < self.explosion_range:
                    damage_grenade = self.damege - (self.damege * distance_enemy / self.explosion_range)
                    enemy.health -= int(damage_grenade)


class POKEBALL(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 200
        # self.timer2 = 0
        self.vel_y = -6
        self.speed = 6
        self.image = pokeball_img
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.contain_pokemon = False
        # self.char_draw_again = False
        # self.red_animation = False
        # self.angle = 0

    def update(self):
        self.vel_y += GRAVITY
        dx = self.speed * self.direction
        dy = self.vel_y

        # check collison with level
        for tile in world.obstacle_list:
            # check collision with walls
            if tile[1].colliderect(self.rect.x - dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                # check if below the ground , i.e thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    # self.speed = 0

                # check if above the ground i.e falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
                    self.speed = 0

        # update grenade position
        self.rect.x -= dx - screen_scroll
        self.rect.y += dy

        # activate pokeball- wild pokemon logic
        for enemy in enemy_group:

            if self.contain_pokemon == False:

                # define collide with only 1 pokemon
                if pygame.sprite.spritecollide(enemy, pokeball_group, False):  # and not collided_already:
                    if enemy.alive:
                        # collided_already = True
                        # enemy.in_pokeball = True # will paint enemy in red color for 0.1 sec
                        self.contain_pokemon = True
                        enemy.stop_draw = True

                        if CatchingRate(enemy):  # function that check catching rate of each wild pokemone.
                            # n = 78
                            player.exp += enemy.lvl * (
                                        enemy.max_health + enemy.atk + enemy.deff + enemy.spa + enemy.spd + enemy.energy) // 6
                            anim_file = 'catched'  # 'catched\\'

                        else:
                            # n = 85
                            enemy.rect.center = self.rect.center
                            anim_file = 'escaped'  # 'escape\\'
                            # enemy.in_pokeball = False
                        print(anim_file)

                        # paint in red for cathing moment only
                        # if enemy.in_pokeball == True:
                        # colorImage = pygame.Surface(enemy.img.get_size()).convert_alpha()
                        # colorImage.fill((255,0,0))
                        # enemy.img.blit(colorImage, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

                        # if self.timer < 192:
                        # activate animation
                        cathing_animation = Explosion(self.rect.x, self.rect.y - 3 * self.rect.size[1], 0.5,
                                                      into_pokeball_anim_direction, 0, 72, 1, anim_file)
                        explosion_group.add(cathing_animation)
                        self.kill()

        # countdown timer
        self.timer -= 2
        # self.timer2 -= 2

        if self.timer <= 0:
            # if collided_already == False:
            if self.contain_pokemon == False:
                print(' not collided and self kill activate')
                player.pokeball_thrown = False
            self.kill()


into_pokeball_anim_direction = 'images\\into_pokeball_anim\\'
explosion_anim_direction = 'images\\explosion\\'


def CatchingRate(enemy):
    EnemyHPlost = 100 * (enemy.max_health - enemy.health) // enemy.max_health
    # print("EnemyHPlost:",EnemyHPlost)

    if pokemon_collection[enemy.char_type].form == 1:
        random_catch_range = 50
        enemy.collidWithPokeball += 10

    elif pokemon_collection[enemy.char_type].form == 2:
        random_catch_range = 70
        enemy.collidWithPokeball += 8


    elif pokemon_collection[enemy.char_type].form == 3:
        random_catch_range = 250
        enemy.collidWithPokeball += 5

    elif pokemon_collection[enemy.char_type].form == "legendary":
        random_catch_range = 300
        enemy.collidWithPokeball += 3

    else:
        print('raise error or add in future;')

    ##    if playr.lvl > enemy.lvl and random_catch_range >= 30:
    ##        random_catch_range -= (playr.lvl-enemy.lvl) * 3

    if random_catch_range > 2:
        if random_catch_range - enemy.collidWithPokeball < 2:
            enemy.collidWithPokeball = 0
        random_catch_range -= enemy.collidWithPokeball

        if random_catch_range - EnemyHPlost < 2:
            random_catch_range = 2
        else:
            random_catch_range -= EnemyHPlost

    random_catch = random.randint(1, random_catch_range)

    if random_catch == 1:
        PokemonCaught = True
        if len(party_lst) < 6:
            enemy.char = 'player'
            enemy.rect.center = player.rect.center
            party_lst.append(enemy)
        else:
            print('Already 6 pokemon in party')
        enemy.kill()
    else:
        PokemonCaught = False

    return PokemonCaught


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, file, start, end, step, extra_file=None):
        pygame.sprite.Sprite.__init__(self)
        self.file = file
        self.images = []
        self.max_range = (start, end, step)
        self.extra_file = extra_file if extra_file is not None else ''
        for num in range(self.max_range[0], self.max_range[1], self.max_range[2]):
            # for num in range(0,16):
            # img = pygame.image.load(img_directoriy + f'explosion\\{num}.png').convert_alpha()

            img = pygame.image.load(self.file + f'{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)

        # escape from pokeball
        if self.extra_file == 'escaped':
            for num in range(72, 85):
                img = pygame.image.load(self.file + 'escape\\' + f'{num}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.images.append(img)

        # cathced
        if self.extra_file == 'catched':
            for num in range(72, 78):
                img = pygame.image.load(self.file + 'catched\\' + f'{num}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.images.append(img)

        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                if self.extra_file == 'catched':
                    caught_pokemon_fx.play()
                player.pokeball_thrown = False  # prevent from user to throw pokeball during throwing animation.
                self.kill()
            else:
                self.image = self.images[self.frame_index]

        for enemy in enemy_group:
            if enemy.stop_draw and self.frame_index > 84:
                enemy.stop_draw = False


class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color,
                             (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))

        if self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_HEIGHT:
            fade_complete = True
        return fade_complete


intro_fade = ScreenFade(1, BLACK, 5)

death_fade = ScreenFade(2, PINK, 5)


class World():
    def __init__(self):
        self.obstacle_list = []
        self.ground_zero = []

    def process_data(self, data):
        enemies_num = 32
        self.level_length = len(data[0])
        # itereate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    ##                    if tile == 4:
                    ##                        img = img_list[tile]
                    ##                        img_rect = img.get_rect()
                    ##                        img_rect.x = 0
                    ##                        img_rect.y = pygame.display.get_surface().get_size()[1]
                    ##                        tile_data2 = (img,img_rect)
                    ##                        self.ground_zero.append(tile_data2)

                    elif tile >= 9 and tile <= 10:  # water
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14 or tile == 31:  # decoration
                        if tile == 31:
                            pass
                            # img = pygame.transform.scale(img,(2*TILE_SIZE,4*TILE_SIZE))
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # health and tile <= 18:
                        item_box = ItemBox('HEALTH', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 16:
                        item_box = ItemBox('HEALTH2', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 17:
                        item_box = ItemBox('ENERGY', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:
                        item_box = ItemBox('SPEED', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox('ATK', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:
                        item_box = ItemBox('DEFF', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 21:
                        item_box = ItemBox('SPD', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 22:
                        item_box = ItemBox('SPA', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 23:
                        item_box = ItemBox('EXP2', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 24:
                        item_box = ItemBox('TM', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 25:
                        pass  # tm
                    elif tile == 26:
                        item_box = ItemBox('POKEBALL', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 27:
                        item_box = ItemBox('EXP', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 28:
                        pass  # lucky egg
                    elif tile == 29:  # person
                        pass
                    elif tile == 30:  # create exit
                        img = pygame.transform.scale(img, (4 * TILE_SIZE, 4 * TILE_SIZE))
                        exit1 = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit1)

                    elif tile == 32:  # create player
                        # this tile very important. any modification in level editor need to verify player got this tile
                        #        self   (char_type,x         ,y     ,scale,speed,ammo,grenades):
                        # self,name,scale,hp,speed,tm1,tm2,typ1,typ2,energy,atk,deff,spa,spd,x_states,y_states)
                        player = Player(CHARACTER.name, "player", x * TILE_SIZE, y * TILE_SIZE, CHARACTER.hp,
                                        CHARACTER.scale, CHARACTER.speed, CHARACTER.fake_speed, CHARACTER.tm1,
                                        CHARACTER.tm2 \
                                        , CHARACTER.typ1, CHARACTER.typ2, CHARACTER.energy, CHARACTER.atk,
                                        CHARACTER.deff, CHARACTER.spa, CHARACTER.spd, CHARACTER.tm_lvl)  # ,25,90)

                        # print(party_lst)
                    elif tile > enemies_num:  # create enemies
                        for z in os.listdir('images\\game_background1\\pokemon'):
                            if z == str(tile - enemies_num) + '.png':
                                if enemy_collection[tile - enemies_num] in os.listdir('images\\pokemon_images'):
                                    # self,char_type,char, x, y,scale, speed,ammo,grenades)
                                    enemy = Player(enemy_collection[tile - enemies_num], 'enemy', x * TILE_SIZE,
                                                   y * TILE_SIZE,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].hp, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].scale \
                                                   , pokemon_collection[enemy_collection[tile - enemies_num]].speed,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].fake_speed,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].tm1, 0, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].typ1,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].typ2, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].energy,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].atk, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].deff,
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].spa, \
                                                   pokemon_collection[enemy_collection[tile - enemies_num]].spd,
                                                   pokemon_collection[
                                                       enemy_collection[tile - enemies_num]].tm_lvl)  # ,None,None)
                                    enemy_group.add(enemy)

                                    enemy.lvl = level * 2 + 5 + x // 10
                                    enemy.max_health, enemy.atk, enemy.deff, enemy.spa, enemy.spd, enemy.speed, enemy.energy, enemy.reg, enemy.fake_speed = \
                                    pokemon_collection[enemy_collection[tile - enemies_num]].states_update(enemy.lvl)

                                    enemy.max_energy = enemy.energy
                                    enemy.start_atk = enemy.atk
                                    enemy.start_deff = enemy.deff
                                    enemy.start_spa = enemy.spa
                                    enemy.start_spd = enemy.spd
                                    enemy.start_speed = enemy.speed
                                    enemy.max_fake_speed = enemy.fake_speed

        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


# pokemon learean move - dict
trainer_teach_tm = {  # 1:random.choice([sunny_day,rain_dance,par_pdr]),
    1: random.choice([ember, boublle, bullet_seed]),
    2: random.choice([ember, boublle, bullet_seed]),
    3: random.choice([sludge_bmb, rain_dance, water_gun]),
    4: random.choice([sludge_bmb, rain_dance, water_gun]),
    5: random.choice([sludge_bmb, rain_dance, water_gun]), }


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type

        self.image = item_boxes[self.item_type]
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

        # check if the player has picked up the berry
        if pygame.sprite.collide_rect(self, player):
            item_fx.play()
            # check what kind of box
            if self.item_type == 'HEALTH2':
                player.potion += 1
                player.exp += 50

            elif self.item_type == 'HEALTH':
                player.health = player.max_health
                player.exp += 250
            elif self.item_type == 'ENERGY':
                player.ammo += 25
                player.energy = player.max_energy
                player.exp += 250
            elif self.item_type == 'ATK':
                player.grenades += 15
                player.atk *= 1.1
                player.exp += 150

            elif self.item_type == 'DEFF':
                player.grenades += 3
                player.deff *= 1.1
                player.exp += 150

            elif self.item_type == 'SPEED':
                player.speed += 2
                player.exp += 100


            elif self.item_type == 'SPA':
                player.spa *= 1.1
                player.exp += 100

            elif self.item_type == 'SPD':
                player.spd *= 1.1
                player.exp += 100

            elif self.item_type == 'EXP':
                player.speed += 1
                player.spd *= 1.1
                player.spa *= 1.1
                player.atk *= 1.1
                player.deff *= 1.1
                # player.health = player.max_health
                player.energy = player.max_energy
                player.exp += 3000
            elif self.item_type == 'EXP2':
                player.exp += 300
            elif self.item_type == 'POKEBALL':
                player.pokeball += 1
                player.exp += 100

            elif self.item_type == 'TM' and len(trainer.tm_lst) < 16:
                trainer.tm_lst.append(trainer_teach_tm[level])
                # player.TM_LST.append(trainer_teach_tm[level])
                player.exp += 300

            self.kill()


y_axis_trainer = 0


class Trainer():
    def __init__(self):
        self.lvl = 1
        self.exp = 0
        # self.pokeball = 0
        # self.badge = 0
        # self.potion = 0
        self.tm_lst = [water_gun]
        self.clicked = False
        self.warning = False
        self.warning2 = False

        # self.tm = []
        self.text_new_move = ''
        self.counter = 0

        self.switch_pokemon = 0

        self.tm_delete = ''

        self.show_tm_preview = False

    def draw_menue(self):
        x_pos, y_pos = 400, 150  # define my image position (include transperent and not)
        x_text_rects, y0 = 100, 170  # position where text start

        global y_axis_trainer

        screen.blit(trainer_box_img, (x_pos, 100))
        my_image = pygame.Surface((trainer_box_img.get_width(), trainer_box_img.get_height() - 100), pygame.SRCALPHA)
        my_image_rect = my_image.get_rect()

        my_image_rect.topleft = (x_pos, y_pos)
        my_image_rect.h = 280
        pygame.draw.rect(screen, (10, 100, 200), my_image_rect, 2, 2)

        # draw up and down scrolling rects
        pygame.draw.rect(screen, (178, 138, 28), up_rect_trainer, 0, 4)
        pygame.draw.rect(screen, (178, 138, 28), down_rect_trainer, 0, 4)

        pos = pygame.mouse.get_pos()

        # close_btn
        close_btn_rect = pygame.Rect((my_image_rect.centerx - 45, trainer_box_img.get_height() + 70, 80, 20))

        pygame.draw.rect(screen, (200, 140, 60), close_btn_rect, 0, 4)

        if close_btn_rect.collidepoint(pos):
            pygame.draw.rect(screen, (150, 110, 90), close_btn_rect, 0, 4)
            if pygame.mouse.get_pressed()[0]:
                self.warning, self.warning2 = False, False
                self.show_tm_preview = False
                self.counter = 0
                self.text_new_move = ''

        pygame.draw.rect(screen, (120, 50, 30), close_btn_rect, 2, 4)
        close_text = font.render('close', True, (20, 20, 20))
        close_text_rect = close_text.get_rect(center=close_btn_rect.center)
        screen.blit(close_text, close_text_rect)

        space = 30
        fixed_y = 50

        for i, t in enumerate(self.tm_lst):
            text_rect = pygame.Rect(x_pos + x_text_rects, (y_axis_trainer + y0 + i * space), 180, 20)
            action1_rect = pygame.Rect(text_rect.right + 25, text_rect.y, 50, 20)
            # print(t.text)
            if text_rect.y > y0 - space and text_rect.bottom <= my_image_rect.bottom - space:
                TM_text = font.render(str(i + 1) + '. ' + t.text[0] + t.text[1:].lower(), True, (20, 20, 20))
                screen.blit(TM_text, text_rect)
                screen.blit(trash_del_tm_img2, action1_rect)
                # pygame.draw.rect(screen,(2,2,2),action1_rect,4,4)
            z = y0 + i * (len(self.tm_lst))

            # del tm action
            if action1_rect.collidepoint(pos):
                pygame.draw.circle(screen, (20, 20, 20),
                                   (action1_rect.centerx - action1_rect.h // 2, action1_rect.centery),
                                   action1_rect.h // 2, 3)
                if pygame.mouse.get_pressed()[0]:  # and self.clicked == False:
                    self.warning = True
                    self.tm_delete = t.text
            if text_rect.collidepoint(pos) and text_rect.bottom <= my_image_rect.bottom - space:
                fixed_rect = pygame.Rect(text_rect.x - x_pos, text_rect.y - y_pos, text_rect.w, text_rect.h)
                pygame.draw.rect(my_image, (200, 200, 200, 100), fixed_rect, 0, 4)

                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(my_image, (100, 100, 100, 150), fixed_rect, 2, 4)

                    for pokemon in party_lst:
                        if pokemon.state_blit:  # and t not in pokemon.TM_LST:
                            self.warning2 = True
                            # print(t.type,[pokemon.typ1,pokemon.typ1])
                            if t.type.lower() in [pokemon.typ1, pokemon.typ1]:

                                if len(pokemon.TM_LST) > 8:
                                    self.text_new_move = f"{pokemon.char_type} Can't remmber more than 8 moves."
                                    # self.option = 3

                                elif len(pokemon.TM_LST) == 8:
                                    self.text_new_move = f'{pokemon.char_type} learned {t.text} and forget {pokemon.TM_LST[-1].text}'
                                    pokemon.TM_LST[-1] = t
                                    # self.option = 2
                                else:

                                    if t in pokemon.TM_LST:
                                        self.text_new_move = f'{pokemon.char_type} already know {t.text}.'
                                    else:
                                        self.text_new_move = f'{pokemon.char_type} learn {t.text}'
                                        pokemon.TM_LST.append(t)
                                        # pokemon.TM_LST.add(t)
                                        self.tm_lst.remove(t)
                            else:
                                self.text_new_move = f"{pokemon.char_type} can't learn {t.text}"

        if self.warning2 and self.counter < 150:

            pygame.draw.rect(screen, (230, 200, 200), (x_pos + 90, 340, 250, 50), 0, 4)
            pygame.draw.rect(screen, (25, 20, 20), (x_pos + 90, 340, 250, 50), 3, 4)
            draw_multyline_text(my_image, self.text_new_move, (x_pos + 100, 350), font, (60, 60, 60), 200, 250)

            self.counter += 1
            if self.counter > 145:
                self.warning2 = False
                self.counter = 0
                self.text_new_move = ''

        # scroll list
        if down_rect_trainer.collidepoint(pos) and y_axis_trainer > -z - (
                fixed_y * 6) + 550:  # window_rect.bottom:#and y_axis_trainer > -z+(space*window_rect.h/(y0-space)):# and y_axis_trainer > 0:
            pygame.draw.rect(screen, (255, 188, 0), down_rect_trainer, 0, 4)
            y_axis_trainer -= 2
            # print(y_axis_trainer,z)

        if up_rect_trainer.collidepoint(pos) and y_axis_trainer < 0:  # and y_axis_trainer < z:
            pygame.draw.rect(screen, (255, 188, 0), up_rect_trainer, 0, 4)
            y_axis_trainer += 2

        pygame.draw.polygon(screen, (100, 72, 2), (
        (down_rect_trainer.x + 5, down_rect_trainer.top + 5), (down_rect_trainer.centerx, down_rect_trainer.bottom - 5),
        (down_rect_trainer.right - 5, down_rect_trainer.top + 5)), 3)
        pygame.draw.polygon(screen, (100, 72, 2), (
        (up_rect_trainer.x + 5, up_rect_trainer.bottom - 5), (up_rect_trainer.centerx, up_rect_trainer.top + 5),
        (up_rect_trainer.right - 5, up_rect_trainer.bottom - 5)), 3)

        if self.warning:
            warning_rect = pygame.Rect(100, 100, 200, 250)
            # warning_del_tm = 'Are you sure to deleete TM?'
            pygame.draw.rect(screen, (200, 200, 120), (1.5 * x_pos - 15, 1.5 * y_pos - 15, 210, 90))
            text_tm_del = f"  {self.tm_delete}\nWill be deleted?"
            answer_no_rect, answer_yes_rect = draw_multyline_text(my_image, text_tm_del, (1.5 * x_pos, 1.5 * y_pos),
                                                                  font, (60, 60, 60), 200, 250, \
                                                                  (x_pos, y_pos), (150, 150, 150, 150),
                                                                  text2=['No', 'Yes'])
            if answer_no_rect.collidepoint(pos):
                pygame.draw.rect(screen, (200, 200, 180), answer_no_rect, 4, 4)
                if pygame.mouse.get_pressed()[0]:
                    self.warning = False
            if answer_yes_rect.collidepoint(pos):
                pygame.draw.rect(screen, (200, 200, 180), answer_yes_rect, 4, 4)
                if pygame.mouse.get_pressed()[0]:
                    self.tm_lst.remove(t)
                    print('tm_lst amount:', len(self.tm_lst))
                    self.warning = False

        test_rect = pygame.Rect(0, 0, 200, 200)
        test_rect.center = my_image.get_width() // 2, my_image.get_height() // 2
        # pygame.draw.rect(my_image,(200,20,20),test_rect,0)
        # pygame.draw.rect(screen,(20,200,20),(x_pos,y_pos,200,200),3)
        screen.blit(my_image, my_image_rect)
        return y_axis_trainer


trainer = Trainer()


##def switching_animation(pok_rect):
##    trainer_pos = 0,150
##    for i in range(5):
##        pygame.draw.line(screen,(240,0,0),(i+1,140+2*i),(pok_rect.center),i)
##        pygame.draw.polygon(screen,(200+10*i,i,12-2*i),((trainer_pos),(100,120-3*i),(200,80-5*i),(pok_rect.center)),5-i)

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


# create buttons
start_btn = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 100, start_img, 0.5, 0.5)
exit_btn = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 50, exit_img, 0.5, 0.5)
restart_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, restart_img, 0.5, 0.5)

# pause menue buttons
play_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 200, play_img, 0.5, 0.5)
save_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 100, save_img, 0.5, 0.5)
settings_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, settings_img, 0.5, 0.5)
exit2_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 100, exit2_img, 0.5, 0.5)
fullscreen_button = button.Button(10, 10, fullscreen_img, 0.3, 0.3)

left_ball_btn = button.Button(122, 290, left_ball_img, 1, 1)
center_ball_btn = button.Button(360, 292, center_ball_img, 1, 1)
right_ball_btn = button.Button(590, 291, right_ball_img, 1, 1)

trainer_box_button = button.Button(SCREEN_WIDTH - 170, 5, trainer_box_img, 0.1, 0.1)

# create sprite group
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
pokeball_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
# party_group = pygame.sprite.Group()


# settings
screen_width = SETTINGS.Settings('Screen width:', 800, 1200, 350, 150)
screen_height = SETTINGS.Settings('Screen Height:', 500, 700, 350, 210)
fps = SETTINGS.Settings('FPS:', 10, 130, 350, 270)
sound_setting = SETTINGS.Settings('Sound:', 0, 0.1, 350, 330)
music_setting = SETTINGS.Settings('Music:', 0, 1, 350, 390)
font_size = SETTINGS.Settings('Font Size:', 20, 35, 350, 450)
##font_color_r = SETTINGS.Settings('Font Color(r):',0,255,350,430)
##font_color_g = SETTINGS.Settings('Font Color(g):',0,255,350,455)
##font_color_b = SETTINGS.Settings('Font Color(b):',0,255,350,480)

settings = [screen_width, screen_height, fps, sound_setting, music_setting,
            font_size]  # ,font_color_r,font_color_g,font_color_b]

# Create empty tile list
world_data = []
for row in range(ROWS + 1):  # +1 is the floor data i created
    r = [-1] * COLS
    world_data.append(r)

# load in level data and create world
with open(f'levels_csv\\level#{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
##player,health_bar,energy_bar,health_bar_enemy = world.process_data(world_data)
##speed_timer = 0


pygame.mixer.music.load(f'audio\\game music\\{BG_MUSIC[0]}.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)

run = True
while run:

    clock.tick(FPS)

    if start_game == False:

        # Music_start(BG_MUSIC[0])

        screen.blit(main_bg_img, (0, 0))
        screen.blit(pokemon_bg_img, (SCREEN_WIDTH // 3 - 50, 0))

        if fullscreen_button.draw(screen):
            screen = pygame.display.set_mode((0, 0))
            SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

            menu_SIZE = 85  # 0.5 * SCREEN_HEIGHT // ROWS

            start_btn = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 150, start_img, 0.5, 0.5)
            exit_btn = button.Button(SCREEN_WIDTH - 150, 10, exit_img, 0.5, 0.5)
            restart_btn = button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, restart_img, 0.6, 0.6)

            main_bg_img = pygame.transform.scale(main_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            pokemon_bg_img = pygame.transform.scale(pokemon_bg_img, (SCREEN_WIDTH // 2, 150))
            oak_img = pygame.transform.scale(oak_img,
                                             (SCREEN_WIDTH - choose_starter_img.get_width(), 1.2 * SCREEN_HEIGHT - 10))

        if start_btn.draw(screen):
            start_game = True
            start_intro = True  # relate to opening scene
            Music_stop()
            Music_start(BG_MUSIC[1])

        if exit_btn.draw(screen):
            run = False


    elif choose_character == True:

        # take mouse curser position
        pos = pygame.mouse.get_pos()
        # print(pos)
        screen.blit(oak_img, (choose_starter_img.get_width(), 0))
        screen.blit(choose_starter_img, (0, 0))

        if left_ball_btn.draw(screen):
            CHARACTER = Bulbasaur
            choose_character = False
            start_intro = True
            player = world.process_data(world_data)
            # party_lst.append(CHARACTER)
            party_lst.append(player)
            bulba_fx.play()
            Music_stop()
            # Music_start(BG_MUSIC[2])
            # show_pokemon = CHARACTER # line in test , searching word related :party2

        elif center_ball_btn.draw(screen):
            CHARACTER = Charmander
            choose_character = False
            start_intro = True
            player = world.process_data(world_data)
            party_lst.append(player)
            Music_stop()
            # Music_start(BG_MUSIC[2])
            # show_pokemon = CHARACTER # line in test , searching word related :party2

        elif right_ball_btn.draw(screen):
            CHARACTER = Squirtle
            choose_character = False
            start_intro = True
            player = world.process_data(world_data)
            party_lst.append(player)
            Music_stop()
            # Music_start(BG_MUSIC[2])
            # show_pokemon = CHARACTER # line in test , searching word related :party2

        if left_ball_btn.rect.collidepoint(pos):
            screen.blit(bulba_img, (30, 0))
        if center_ball_btn.rect.collidepoint(pos):
            screen.blit(charma_img, (300, 0))
        if right_ball_btn.rect.collidepoint(pos):
            screen.blit(squir_img, (530, 0))


    else:
        ##        if not pygame.mixer.music.get_busy():
        ##            Game_musics()
        Music_start(BG_MUSIC[2])

        # update bg
        draw_bg()
        # update world map
        world.draw()

        ##        pygame.draw.rect(screen,GRAY,(0,SCREEN_HEIGHT - menu_SIZE,SCREEN_WIDTH-screen_scroll,SCREEN_HEIGHT))

        # TM1_TIMER.draw()
        # TM2_TIMER.draw()
        # TM3_TIMER.draw()
        # TM4_TIMER.draw()

        ##        if party_lst:
        ##            player = party_lst[trainer.switch_pokemon]

        draw_text(f'Game Level: {level}', font, set_color, 50,
                  pygame.display.get_surface().get_size()[1] - 2 * TILE_SIZE)

        pokeball_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()

        pokeball_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)

        water_group.draw(screen)

        if pause_activate:
            pause()
            # Music_stop()
            pygame.mixer.music.pause()

            pause_mode = True
            player.draw()
            # pygame.draw.line(screen,WHITE,(SCREEN_WIDTH//2,0),(SCREEN_WIDTH//2,SCREEN_HEIGHT))

            for enemy in enemy_group:
                if enemy.stop_draw == False:
                    enemy.draw()

            if pause_from_pokemon_party_btn:
                pause_from_esc_keyboard = False
                screen.blit(pokemon_party_bg_img, (30, 0))

                for party_index, pokemon in enumerate(party_lst):
                    if hasattr(pokemon_collection[pokemon.char_type], "lvl_100"):
                        for i in pokemon_collection[pokemon.char_type].lvl_100_states(100):
                            party_states_lvl100_lst[party_index].append(i)
                        del pokemon_collection[pokemon.char_type].lvl_100
                        print(party_states_lvl100_lst)

                    pokemon.PokemonInParty(55, 90 * (party_index + 1), party_states_lvl100_lst[party_index])

            if pause_from_esc_keyboard:  # and not pause_from_pokemon_party_btn:
                # pause_from_pokemon_party_btn = False

                if play_btn.draw(screen) and not settings_mode:
                    pause_activate = False
                    pause_mode = False

                    pygame.mixer.music.unpause()

                if save_btn.draw(screen) and not settings_mode:
                    pause_activate = False
                    pause_mode = False
                    pygame.mixer.music.unpause()

                if settings_btn.draw(screen) and not settings_mode:
                    settings_mode = True

                if exit2_btn.draw(screen) and not settings_mode:
                    run = False

                if settings_mode:
                    pygame.mixer.music.unpause()

                    '''
                    if fullscreen_button.draw(screen):
                        screen = pygame.display.set_mode((0,0))
    ##                else:
    ##                    screen = pygame.display.set_mode((screen_width.value,screen_height.value))
                    '''

                    # Change settings:
                    # fps
                    FPS = fps.value
                    # music
                    pygame.mixer.music.set_volume(float(music_setting.value))
                    # sound
                    for sett in sound_volume_lst:
                        sett.set_volume(20 * sound_setting.value)

                    # create setting window - i belive i didnt used it correctly but it was at the begining of my project so nvm
                    setting_window = pygame.Surface((650, 450))
                    setting_window.fill(GREEN2)
                    pygame.draw.rect(setting_window, WHITE, (0, 0, 650, 20))

                    # draw x like in WINDOWS 10 window
                    x_rect = pygame.Rect(720, 100, 30, 20)
                    pygame.draw.line(setting_window, BLACK, (630, 5), (640, 15))
                    pygame.draw.line(setting_window, BLACK, (630, 15), (640, 5))

                    # define font and size - in future i can add chenge font but its waste of time now
                    font = pygame.font.SysFont('Futura', font_size.value)
                    font_size.font_example(setting_window, font, 50, setting_window.get_size()[1] - 50, 230, 230, 230)
                    # font_size.font_example(setting_window,font,450,font_size.rect.centery ,font_color_r.value,font_color_g.value,font_color_b.value)
                    # set_color = (font_color_r.value,font_color_g.value,font_color_b.value)

                    screen.blit(setting_window, (100, 100))

                    # create special settings buttons from SETTINGS file func
                    defult_rect_btn, full_screen_rect_btn, control_setting_rect_btn = SETTINGS.Draw_special_settings(
                        screen, setting_window)

                    pos = pygame.mouse.get_pos()

                    if not setting_controller:
                        # define close window rect (as on regullar pc)
                        if x_rect.collidepoint((pos)):
                            pygame.draw.rect(screen, RED, x_rect)
                            pygame.draw.line(screen, WHITE, (730, 105), (740, 115))
                            pygame.draw.line(screen, WHITE, (730, 115), (740, 105))
                            if pygame.mouse.get_pressed()[0]:
                                settings_mode = False
                                setting_controller = False

                        for func in settings:
                            func.draw(screen)  # dont understand yet why not working "setting_window" instead screen
                            if func.rect.collidepoint((pos)) and pygame.mouse.get_pressed()[0] and pos[0] in range(
                                    func.rect_line.x, func.rect_line.x + func.line_width + 1):
                                pygame.draw.rect(screen, BLACK, (func.rect), 1)
                                func.rect.centerx = pos[0]
                                func.update(pos[0])
                                if pos[1] in range(screen_width.rect_line.y, screen_height.rect_line.y):
                                    screen = pygame.display.set_mode((screen_width.value, screen_height.value))

                            elif func.rect_line_transperent.collidepoint((pos)) and pygame.mouse.get_pressed()[
                                0]:  # clicking area are wider then visible line
                                func.rect.centerx = pos[0]
                                func.update(pos[0])

                            # restore settings to default
                            if defult_rect_btn.collidepoint((pos)):
                                pygame.draw.rect(screen, (0, 250, 30), (defult_rect_btn), 3)
                                if pygame.mouse.get_pressed()[0]:
                                    func.rect.centerx = func.defult
                                    func.update(func.defult)

                        # Full screen in setting mode
                        if full_screen_rect_btn.collidepoint((pos)):
                            pygame.draw.rect(screen, (0, 250, 30), (full_screen_rect_btn), 3)
                            if pygame.mouse.get_pressed()[0]:
                                screen = pygame.display.set_mode((0, 0))
                                pokemon_party_btn = button.Button(pygame.display.get_surface().get_size()[0] - 40, 20,
                                                                  pokemon_party_img, 0.3, 0.3)
                                # controller_setting_bg_image = pygame.transform.scale(controller_setting_bg_image,(pygame.display.get_surface().get_size()))

                        if control_setting_rect_btn.collidepoint((pos)):
                            pygame.draw.rect(screen, (0, 250, 30), (control_setting_rect_btn), 3)
                            if pygame.mouse.get_pressed()[0]:
                                setting_controller = True

                    # reminder : setting_controller = False in game variable
                    if setting_controller:

                        # define new window size
                        setting_controller_width, setting_controller_height = pygame.display.get_surface().get_size()
                        # define the location of X for close that window
                        closing_rect = 0.85 * setting_controller_width - 20
                        # define window and draw white rect on it and define x,y coord for bliting this window
                        controller_window = pygame.Surface(
                            (setting_controller_width * 0.85, setting_controller_height * 0.9))
                        pygame.draw.rect(controller_window, WHITE, (0, 0, setting_controller_width * 0.85, 20))

                        # define the position of new window comparing to screen (new begin of axes is 100,30 of all what will draw on ne window
                        # use as x_fix and y_fix in SETTING controler functions
                        x_cord_control_window, y_cord_control_window = 100, 30

                        # define rect for new window
                        controller_window_rect = controller_window.get_rect()
                        # print("controller_window_rect",controller_window_rect)

                        # define rect where the X will draw and mouse wll collide with and move that rect into new window coords
                        rect_in_sub_window = pygame.Rect(-30, 0, 30, 20)
                        closing_rect_x_rect = rect_in_sub_window.move(
                            controller_window_rect.right + x_cord_control_window, y_cord_control_window)

                        pygame.draw.line(controller_window, BLACK, (closing_rect, 5), (closing_rect + 10, 15))
                        pygame.draw.line(controller_window, BLACK, (closing_rect, 15), (closing_rect + 10, 5))

                        for event in pygame.event.get():

                            # game controls
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    setting_controller = False

                                for k in SETTINGS.key_obj_lst:
                                    # define each key by user
                                    if k.active:
                                        # k.keyboard  = event.unicode
                                        k.keyboard = pygame.key.name(event.key)
                                        SETTINGS.default = False

                        ##                        #define close window rect (as on regullar pc) # i choode to define those rect for learning the rect.move
                        if closing_rect_x_rect.collidepoint((pos)):
                            pygame.draw.rect(controller_window, RED, (closing_rect - 5, 0, 30, 20))
                            # pygame.draw.rect(screen,RED,closing_rect_x_rect) # untill i will find a solution i got use it
                            pygame.draw.line(controller_window, WHITE, (closing_rect, 5), (closing_rect + 10, 15))
                            pygame.draw.line(controller_window, WHITE, (closing_rect, 15), (closing_rect + 10, 5))
                            if pygame.mouse.get_pressed()[0]:
                                setting_controller = False

                        # bliting bg

                        controller_window.blit(controller_setting_bg_image, (0, 20))
                        controller_setting_bg_image = pygame.transform.scale(controller_setting_bg_image, (
                        controller_window.get_size()[0], controller_window.get_size()[1] - 20))

                        for k in SETTINGS.key_obj_lst:
                            k.draw(controller_window, x_cord_control_window, y_cord_control_window)
                            if SETTINGS.default:
                                k.keyboard = k.default
                        if SETTINGS.IS_DEFAULT(controller_window, x_cord_control_window,
                                               y_cord_control_window):  # this func take the x,y_fix position due to collideing with rect issue
                            SETTINGS.default = True

                        # bliting that controler window with all rect and text on it
                        screen.blit(controller_window, (x_cord_control_window, y_cord_control_window))


        else:
            '''
            #actual game play
            '''

            pause_mode = False
            if len(enemy_group) <= 0:
                no_enemy = True
            else:
                no_enemy = False

            if no_enemy:
                exit_group.draw(screen)
                draw_text('Exit avilable.', font, WHITE, SCREEN_WIDTH // 2 - 100, 70)

            enemy_vision = []
            # for Lvl,enemy in enumerate(enemy_group):
            for enemy in enemy_group:

                enemy.update()
                if enemy.stop_draw == False:
                    enemy.draw()
                    # enemy.ai(Lvl,player_once_lvl)
                    enemy.ai()
                    # if enemy.vision.colliderect(player.rect):
                    x_dis = 350
                    y_dis = 200

                    # states are updated in enemy-tile class
                    # enemy.lvl += Lvl
                    # enemy.max_health,enemy.atk,enemy.deff,enemy.spa,enemy.spd,enemy.speed,enemy.energy,enemy.reg = pokemon_collection[enemy.char_type].states_update(enemy.lvl)

                    # enemy.states_update(lvl)
                    if enemy.rect.x in range(player.rect.x - x_dis, player.rect.x + x_dis) and enemy.rect.y in range(
                            player.rect.y - y_dis, player.rect.y + y_dis) \
                            or enemy.vision.colliderect(player.rect):
                        enemy_vision.append(enemy)

            for i, enemy in enumerate(enemy_vision):
                # health_bar_enemy.z = i*35
                # health_bar_enemy()#.draw(enemy.health,enemy.max_health,enemy.energy,enemy.char_type)
                enemy.HealthBar(pygame.display.get_surface().get_size()[0] - 200, 10, i * 35)

            player.draw()
            player.update()  # animation and cooldown in 1 function see player class above
            player.HealthBar(10, 20, 0)
            # player.update_energy(second_for_energy)

            bullet_group.draw(screen)
            bullet_group.update(player.direction)

            # show intro (screen fade )
            if start_intro == True:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            if player.alive:
                # draw menue - draw pokemon attacks , pokeball, potion and party_btn
                # if party btn activate then pasue is activated also
                pause_from_pokemon_party_btn, pause_activate = draw_menue()

                if player.exp > lvl_up_pts(player.lvl):
                    player.lvl += 1
                    pokemon_lvl_up_fx.play()
                    player.exp = 0

                    print(player.fake_speed, player.max_fake_speed)
                    # adding the hp up from lvl up
                    temp_hp_to_add = player.health

                    temp_just_for_print_hp_change = player.max_health
                    # update player states per lvl up
                    player.max_health, player.atk, player.deff, player.spa, player.spd, player.speed, player.energy, player.reg, player.fake_speed = CHARACTER.states_update(
                        player.lvl)
                    player.health += player.max_health - temp_hp_to_add
                    # player_states_lst = [player.max_health,player.atk,player.deff,player.spa,player.spd,player.speed,player.energy,player.reg]

                    print('Level up :', player.lvl)
                    print(player.max_health, player.atk, player.deff, player.spa, player.spd, player.speed,
                          player.energy, player.reg, player.fake_speed)
                    ##                        print('HP(player): +',player.max_health - temp_just_for_print_hp_change)
                    ##                        print('Atk(player) +',player.atk-player.start_atk)
                    ##                        print('Def(player) +',player.deff-player.start_deff)
                    ##                        print('Spa(player) +',player.spa-player.start_spa)
                    ##                        print('Spd(player) +',player.spd-player.start_spd)
                    print('Speed(player) +', player.fake_speed - player.max_fake_speed)
                    ##                        print('Eng(player) +',player.energy-player.max_energy)
                    ##                        print('\n')
                    # print('Reg(player) +',player.spd-player.start_spd)

                    player.max_energy = player.energy
                    player.start_atk = player.atk
                    player.start_deff = player.deff
                    player.start_spa = player.spa
                    player.start_spd = player.spd
                    player.start_speed = player.speed
                    player.max_fake_speed = player.fake_speed
                    # self.hp,      self.atk,  self.deff,  self.spa,  self.spd,  self.speed,self.energy,self.reg
                ##                        print('Level up :',player.lvl)
                ##                        print('HP(player):',player.health,'HP(char):',CHARACTER.hp,'max_hp:',player.max_health)
                ##                        print('Atk(player):',player.atk,'Atk(char):',CHARACTER.atk,'start_atk:',player.start_atk)
                ##                        print('Def(player):',player.deff,'Def(char):',CHARACTER.deff,'start_def:',player.start_deff)
                ##                        print('Spa(player):',player.spa,'Spa(char):',CHARACTER.spa,'start_spa:',player.start_spa)
                ##                        print('Spd(player):',player.spd,'Spd(char):',CHARACTER.spd,'start_spd:',player.start_spd)

                if player.speed > player.start_speed:
                    # player.speed = player.start_speed

                    speed_boost = True
                    # draw_text(f'DOUBLE SPEED ({15 - event_timer_s})',font,set_color,SCREEN_WIDTH - 350,SCREEN_HEIGHT - 2*TILE_SIZE)
                    speed_img = pygame.transform.scale(speed_img,
                                                       (int(player.rect.size[0] * 1.5), int(player.rect.size[1] * 1.5)))

                    # if speed_timer % 2 == 0 : #moving_left or moving_right:
                    screen.blit(speed_img, (player.rect.x, player.rect.y))
                    if event_timer_s >= 15:
                        speed_boost = False
                        player.speed = player.start_speed
                        event_timer_s = 0

                if player.atk > player.start_atk:
                    atk_boost = True
                    if event_timer_a >= 15:
                        atk_boost = False
                        player.atk = player.start_atk
                        event_timer_a = 0
                if player.deff > player.start_deff:
                    deff_boost = True

                    # screen.blit(speed_img,(player.rect.x,player.rect.y))
                    if event_timer_d >= 15:
                        deff_boost = False
                        player.deff = player.start_deff
                        event_timer_d = 0
                if player.spa > player.start_spa:
                    spa_boost = True

                    # screen.blit(speed_img,(player.rect.x,player.rect.y))
                    if event_timer_sp >= 15:
                        sp_boost = False
                        player.sp = player.start_spa
                        event_timer_sp = 0

                if player.spd > player.start_spd:
                    spd_boost = True

                    # screen.blit(speed_img,(player.rect.x,player.rect.y))
                    if event_timer_spd >= 15:
                        spd_boost = False
                        player.spd = player.start_spd
                        event_timer_spd = 0

                # clicking on potion/pokeball btn
                # use_item_btn()

                # shoot bullet
                if shoot:
                    player.shoot()

                # throw grenade # i want to forbit shoot and throw grenade at same time
                elif grenade and grenade_thrown == False and player.grenades > 0:
                    grenade = Grenade(player.rect.centerx - int(player.direction * player.rect.size[0] * 0.5), \
                                      player.rect.top, player.direction)
                    grenade_group.add(grenade)
                    grenade_thrown = True
                    player.grenades -= 1

                if moving_left or moving_right:
                    player.update_action(1)
                elif player.in_air:
                    player.update_action(2)
                elif shoot:
                    player.update_action(4)
                else:
                    player.update_action(0)

                screen_scroll, level_complete = player.move(moving_left, moving_right)
                bg_scroll -= screen_scroll
                # print(screen_scroll,bg_scroll)

                if level_complete:
                    party_temp_data = []
                    for pok in party_lst:
                        pok_temp_data = pok.exp, pok.lvl, pok.TM_LST
                        party_temp_data.append(pok_temp_data)  # = [player.exp,player.lvl,player.TM_LST]

                    start_intro = True
                    level += 1
                    bg_scroll = 0
                    world_data = reset_level()
                    if level <= MAX_LEVELS:
                        # load next level
                        with open(f'levels_csv\\level#{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)

                        for i, pok in enumerate(party_lst):
                            pok.exp, pok.lvl, pok.TM_LST = party_temp_data[i]
                            pok.health = pok.max_health
            else:
                screen_scroll = 0
                temp_lvl = player.lvl
                temp_exp = player.exp
                if death_fade.fade():
                    if restart_btn.draw(screen):
                        bg_scroll = 0
                        world_data = reset_level()
                        death_fade.fade_counter = 0
                        start_intro = True
                        with open(f'levels_csv\\level#{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        # choose_character = True
                        player = world.process_data(world_data)
                        player.lvl = temp_lvl
                        player.exp = 0

    for event in pygame.event.get():

        # quit game
        if event.type == pygame.QUIT:
            run = False

        # player is not definded while this line is running in order to solve that i added if party_lst not empty whats mean theres player inside it
        if party_lst:
            if event.type == pygame.USEREVENT:
                player.update_energy()

            if event.type == pygame.USEREVENT and speed_boost:
                event_timer_s += 1
            if event.type == pygame.USEREVENT and atk_boost:
                event_timer_a += 1
            if event.type == pygame.USEREVENT and deff_boost:
                event_timer_d += 1
            if event.type == pygame.USEREVENT and spa_boost:
                event_timer_sp += 1
            if event.type == pygame.USEREVENT and spd_boost:
                event_timer_spd += 1

            # activate TM
            for tm in player.TM_LST:
                if event.type == pygame.USEREVENT + 2 and tm.tm_active:
                    tm.event_timer_tm += 0.1
                    # tm.clicked = False
                    if tm.event_timer_tm >= tm.reg:
                        tm.event_timer_tm = 0
                        tm.tm_active = False
                        # tm.clicked = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE and not pause_mode:
                pause_activate = True
                pause_from_esc_keyboard = True
                pause_from_pokemon_party_btn = False
            if event.key == pygame.K_ESCAPE and pause_mode:
                pause_activate = False
                pause_from_esc_keyboard = False

            if event.key == pygame.K_RIGHT:
                trainer.switch_pokemon += 1
                if trainer.switch_pokemon >= len(party_lst):
                    trainer.switch_pokemon = 0
                else:
                    ##        if party_lst:
                    # party_lst[1],party_lst[0] = party_lst[0],party_lst[1]
                    # temp_pok_in_party = party_lst[0]
                    # print(type(temp_pok_in_party),temp_pok_in_party.char_type)
                    # player = party_lst[trainer.switch_pokemon]
                    # party_lst[trainer.switch_pokemon-1] = temp_pok_in_party
                    # player = party_lst[0]
                    ##                    switching_animation(player.rect)
                    ##                    pygame.draw.line(screen,(240,0,0),(0,150),(player.rect.center),3)
                    ##                    pygame.draw.line(screen,(240,0,0),(10,145),(player.rect.center),2)
                    ##                    pygame.draw.line(screen,(240,0,0),(0,152),(player.rect.center),4)

                    party_lst[trainer.switch_pokemon], party_lst[0] = party_lst[0], party_lst[trainer.switch_pokemon]
                    player = party_lst[0]

            for k in SETTINGS.key_obj_lst:
                try:
                    if event.key == pygame.key.key_code(k.keyboard):
                        if k.description == 'Moving Right':
                            moving_right = True
                        if k.description == 'Moving Left':
                            moving_left = True
                        if k.description == 'Jump' and player.alive:
                            player.jump = True
                            # test_del_TM = True
                            if pause_activate == False:
                                jump_fx.play()
                        if k.description == 'Throw Pokeball':
                            pokeball_throw_keyboard = True
                        if k.description == 'Attack':
                            grenade = True
                        if k.description == 'Defend':
                            shoot = True
                        if k.description == 'Trainer':  # and not draw_menu_keyboard:
                            draw_menu_keyboard = not draw_menu_keyboard

                        # if k.description == 'Show TM' and draw_menu_keyboard:
                        #   draw_menu_keyboard = False

                except ValueError:
                    k.keyboard = k.default
                    start_ticks_key_error = pygame.time.get_ticks()
                    k.error_key = True

        if event.type == pygame.KEYUP:
            for k in SETTINGS.key_obj_lst:
                if event.key == pygame.key.key_code(k.keyboard):

                    if k.description == 'Moving Right':  # d
                        moving_right = False
                    if k.description == 'Moving Left':  # a
                        moving_left = False
                    if k.description == 'Throw Pokeball':  # p
                        pokeball_throw_keyboard = False
                    if k.description == 'Attack':  # q
                        grenade = False
                        grenade_thrown = False
                    if k.description == 'Defend':  # r
                        shoot = False

    # pygame.draw.circle(screen, (25,25,55), (100, 100), event_timer_tm1, 0)
    ##    if trainer.tm_lst:
    ##        trainer.draw_menue()
    pygame.display.update()

pygame.quit()

