import pygame
import os
import PyEvent


pygame.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SUPER GAME BENNY HASSAN')

# player class of movement , animation , stats and


class Player(pygame.sprite.Sprite):

    moving_right = False
    moving_left = False

    def __init__(self, pokemon_name, PlayerOrEnemy, start_pos, scale, states):  # ,x_states,y_states):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.jump = False
        self.in_air = True
        self.flip = False
        self.direction = 1
        self.vel_y = 0
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        self.pokemon_name = pokemon_name
        self.PlayerOrEnemy = PlayerOrEnemy

        # states
        self.hp, self.speed = states[0], states[1]

        animation_types = ['idle', 'run', 'jump', 'death', 'atk']  # name of folders contain images for frames

        for animation in animation_types:
            num_of_frames = os.listdir('images\\pokemon_images\\' + self.pokemon_name + '\\' + animation)
            for png in num_of_frames:  # my extra for me to ignore files that not png such archive folder
                if 'png' not in png:
                    num_of_frames.remove(png)
            # print(num_of_frames)
            temp_list = []
            for i in range(len(num_of_frames)):
                img = pygame.image.load(
                    'images\\pokemon_images\\' + self.pokemon_name + f'\\{animation}\\{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(TILE_SIZE * scale), int(TILE_SIZE * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.img = self.animation_list[self.action][self.index]
        self.rect = self.img.get_rect()
        self.rect.center = start_pos

    def update(self):
        self.update_animation()
        self.check_alive()

    def move(self):

        dy = 0
        dx = 0
        # assign movement variables
        if self.__class__.moving_left and self.rect.left >= 0:
            dx = -self.speed
            self.flip = True
            self.direction = 1

        if self.__class__.moving_right:
            dx = self.speed
            self.flip = False
            self.direction = -1

        # jump
        if self.jump and not self.in_air:
            self.vel_y = -11
            # self.jump = False
            self.in_air = not self.in_air

        # apply gravity
        self.vel_y += GRAVITY

        if self.vel_y > 10:
            self.vel_y = 0
        dy += self.vel_y

        # check if fall of screen
        if self.rect.bottom > screen_height:
            self.hp = 0

        # TODO delete this rect and collision condition
        bottom_rect = pygame.Rect(0, screen_height-25, screen_width, 25)
        pygame.draw.rect(screen, (10, 50, 40), bottom_rect)
        if player.rect.colliderect(bottom_rect):
            player.rect.bottom -= dy
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.img = self.animation_list[self.action][self.index]

        # check if enough time passed since last update
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
            # update animation settings
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.speed = 0
            self.alive = False
            self.index = 1
            self.action = 3

    def draw(self):
        # screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)
        screen.blit(self.img, self.rect)


# ########################################################################################################
TILE_SIZE = 15

player = Player("Pikachu", "player", (200, 200), 10, [100, 5])

# moving_right, moving_left = False, False
GRAVITY = 0.5

run = True
while run:

    clock.tick(fps)
    screen.fill((20, 50, 100))
  
    player.draw()
    player.update()
    run = PyEvent.Events(pygame, player)

    pygame.display.update()

pygame.quit()
