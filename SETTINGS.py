import pygame

pygame.init()


#colors
GREEN = (144,201,125)
GREEN2 = (24,221,25)
GREEN3 = (22,220,105)
WHITE = (255,255,255)
BLACK = (20,25,25)
GRAY = (50,125,50)
GRAY2 = (50,200,50)

# fonts
font = pygame.font.SysFont('Futura',25)
font2 = pygame.font.SysFont('Futura',15)
##font_small = pygame.font.SysFont('Futura',10)
##font3 = pygame.font.SysFont('Futura',15)


def draw_bg():
    screen.fill(GREEN)

class Settings():
    def __init__(self,name,MIN,MAX,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.min = MIN
        self.max = MAX
        self.width = 10
        self.height = 20
        self.line_width = 100
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.rect_line  = pygame.Rect(x - (self.line_width//2) + self.width//2 ,y+(self.height//2),self.line_width ,2)
        self.rect_line_transperent  = pygame.Rect(x - (self.line_width//2) + self.width//2,y + 3,self.line_width ,20)
        
        self.rect_value  = pygame.Rect(x + self.line_width ,y,70,25)

        #self.defult_rect = pygame.Rect(600,300,100,40)
        self.defult = self.rect.centerx
        #self.full_screen_rect = pygame.Rect(600,150,100,40)
        #self.ctr_settings_rect = pygame.Rect(600,450,100,40)
        if self.max <= 1:
            self.value = round(self.min + (((x - self.rect_line.x) / self.line_width) * (self.max- self.min)),2)
        else:
            self.value = int((self.min + (((x - self.rect_line.x) / self.line_width) * (self.max- self.min))))

        '''
        DESCRIPTION:
        # name - the setting name
        # min,max - range for that setting
        # width,height and self.rect - the moveable rect by user
        # line width - that rect move acrossing this line
        # rect_line - this is the visual range for setting - his width from "line width"
        # transperent rect - to increase user accuarcy while clicking on the movable rect or the rect line
        # rect_value - in this rect we able to see the numerical value of each state
        # default - this position of the begining "default"
        # value -
        '''
        
        
        
    def draw(self,surface):
        # define defult and full screen button 
##        pygame.draw.rect(surface,GREEN2,self.defult_rect)
##        pygame.draw.rect(surface,GREEN3,self.defult_rect,4)
##        pygame.draw.rect(surface,GREEN2,self.full_screen_rect)
##        pygame.draw.rect(surface,GREEN3,self.full_screen_rect,4)
##        pygame.draw.rect(surface,GREEN2,self.ctr_settings_rect)
##        pygame.draw.rect(surface,GREEN3,self.ctr_settings_rect,4)

        #define range for value and toggle-clicked button rect to set value
        #pygame.draw.rect(screen,RED,(self.rect_line_transperent))
        pygame.draw.rect(surface,BLACK,(self.rect_line))
        pygame.draw.rect(surface,GRAY,(self.rect))
        
        #define min.max.center lines
        pygame.draw.line(surface,BLACK,(self.rect_line.x,self.rect_line.y - 3),(self.rect_line.x,self.rect_line.y + 3))
        pygame.draw.line(surface,BLACK,(self.rect_line.x + (self.line_width//2),self.rect_line.y - 3),(self.rect_line.x + (self.line_width//2),self.rect_line.y + 3))
        pygame.draw.line(surface,BLACK,(self.rect_line.x + self.line_width,self.rect_line.y - 3),(self.rect_line.x+self.line_width,self.rect_line.y + 3))
        
        #print string parameter name
        if self.name in ['Font Color(r)','Font Color(g)','Font Color(b)']:
            text = font2.render(self.name,True,BLACK)
        else: 
            text = font.render(self.name,True,BLACK)
        surface.blit(text,(120,self.rect_line.y - self.height//2))
        #print defult on defult rect
##        text2 = font.render('Deafult',True,BLACK)
##        surface.blit(text2,(620,self.defult_rect.y+10))
##        text_fullscreen = font.render('Full-Screen',True,BLACK)
##        surface.blit(text_fullscreen,(605,self.full_screen_rect.y+10))
##        text_ctr_setting = font.render('Controller',True,BLACK)
##        surface.blit(text_ctr_setting,(605,self.ctr_settings_rect.y+10))

        # rect for numerical value , define numerical text and print it
        pygame.draw.rect(surface,GRAY2,(self.rect_value))
        pygame.draw.rect(surface,GRAY,(self.rect_value),1)
        value_text = font2.render(str(self.value),True,BLACK)
        surface.blit(value_text,((self.rect_value.centerx - 10,self.rect_value.centery-5)))


            

    def update(self,new_pos):
        value = (new_pos - self.rect_line.x) / self.line_width
        if self.max <= 1:
            self.value = round(self.min + (value * (self.max- self.min)),2)
        else:
            self.value = int(self.min + (value * (self.max- self.min)))
        #print(value,self.value)

    def font_example(self,surface,font3,font_x,font_y,R,G,B):
        #font3 = pygame.font.SysFont('Futura',15)
        text = font3.render('AaBbCcDd',True,(R,G,B))
        surface.blit(text,(font_x,font_y))



def Draw_special_settings(screen,window):
        defult_rect_btn = pygame.Rect(window.get_size()[0]-50,300,120,40)
        full_screen_rect_btn = pygame.Rect(window.get_size()[0]-50,150,120,40)
        control_setting_rect_btn = pygame.Rect(window.get_size()[0]-50,450,120,40)
        
        pygame.draw.rect(screen,GREEN2,defult_rect_btn)
        pygame.draw.rect(screen,(22,220,105),defult_rect_btn,4)
        pygame.draw.rect(screen,GREEN2,full_screen_rect_btn)
        pygame.draw.rect(screen,(22,220,105),full_screen_rect_btn,4)
        pygame.draw.rect(screen,GREEN2,control_setting_rect_btn)
        pygame.draw.rect(screen,(22,220,105),control_setting_rect_btn,4)
        
        default_text = font.render('Deafult',True,BLACK)
        screen.blit(default_text,(defult_rect_btn.x+15,defult_rect_btn.y+10))
        text_fullscreen = font.render('Full-Screen',True,BLACK)
        screen.blit(text_fullscreen,(full_screen_rect_btn.x+5,full_screen_rect_btn.y+10))
        text_ctr_setting = font.render('Controller',True,BLACK)
        screen.blit(text_ctr_setting,(control_setting_rect_btn.x+5,control_setting_rect_btn.y+10))

        return defult_rect_btn,full_screen_rect_btn,control_setting_rect_btn



#CONTROLLER SETTINGS

# basic font for user typed
base_font = pygame.font.Font(None, 32)
base_font2 = pygame.font.Font(None, 22)
#SETTING VARIABLES
active = False
key_obj_lst = []
default_keys = ['a','d','w','p','q','space','t']
KEYS_DESCRIPTION = ['Moving Left','Moving Right','Jump','Throw Pokeball','Attack','Defend','Trainer']
#from_unicode = ''
default = False
#error_key = False
start_ticks_key_error = 0


BLUE = (20,20,250)
color_passive = (0,180,255)
color_active = (0,245,245)

class KeyboardSettings():
    def __init__(self,y,description,keyboard):
        self.x = 200
        self.rect = pygame.Rect(self.x,y,100,30)
        self.description = description
        self.color = color_passive#pygame.Color('chartreuse4')
        self.keyboard = keyboard
        self.active = False
        self.default = keyboard
        self.error_key = False


    def draw(self,screen,x_fix,y_fix):

        fixed_rect = self.rect.move(x_fix,y_fix)
        pos = pygame.mouse.get_pos()

        # Draw rect for user keyboard input
        pygame.draw.rect(screen,self.color,self.rect,0,2,2,2,2)
        pygame.draw.rect(screen,(100,100,255),self.rect,2,2,2,2,2)
        pygame.draw.rect(screen,BLUE,self.rect,1,2,2,2,2)
        
        # Change color if user clicked on that rect. if so...
        # Activate object for change by user keyboard
        #if self.rect.collidepoint((pos)) and pygame.mouse.get_pressed()[0]:
        if fixed_rect.collidepoint((pos)):
            pygame.draw.rect(screen,(20,20,230),self.rect,2,2,2,2,2)
            if pygame.mouse.get_pressed()[0]:
                self.color = color_active#pygame.Color('lightskyblue3')
                self.active = True   
        elif pygame.mouse.get_pressed()[0]:
            self.color = color_passive#pygame.Color('chartreuse4')
            self.active = False

        #key_text : BTN DESCRIPTIONS
        #key_keyboard : BTN (by user input).... this attribute called from lst "KEYS_DESCRIPTION"
        description_text = base_font.render(self.description, True, (25, 25, 25))
        keyboard_text = base_font.render(self.keyboard, True, (5, 5, 255))
        
        screen.blit(description_text, (20, self.rect.y+5))

        self.rect.w = max(keyboard_text.get_width()*1.1 + 40, 80)
        keyboard_text_rect = keyboard_text.get_rect(center = self.rect.center)
        screen.blit(keyboard_text, keyboard_text_rect)

        if self.error_key:
            error_time_check = (pygame.time.get_ticks() - start_ticks_key_error)/ 1000
            NA_KEY = base_font2.render('N/A Key', True, (25, 25, 255))
            screen.blit(NA_KEY, (110+self.rect.x, self.rect.y+7))
            if error_time_check > 1:
                self.error_key = False

# default func - dont have to be in event loop 
def IS_DEFAULT(screen,x_fix,y_fix):
    
    screen_rect = screen.get_rect()
    x = screen_rect.topright[0]
    default_rect = pygame.Rect(x - 90,30,80,25)

    #fixing coords by surface rect - due to i use new window in main game , the colliding is bit complicated so i got to move the rect...
    # ...for colliding according difference in screen and new window. notice that the draw methode worke normaly but the colliding not.
    default_rect2 = default_rect.move(x_fix,y_fix)
    
    pos = pygame.mouse.get_pos()

    if default_rect2.collidepoint((pos)) and pygame.mouse.get_pressed()[0]:
            color = color_active#pygame.Color('lightskyblue3')
            default = True
    else:
            color = color_passive#pygame.Color('chartreuse4')
            default = False
    pygame.draw.rect(screen,color,default_rect,0,2,2,2,2)
    pygame.draw.rect(screen,(0,25,255),default_rect,1,2,2,2,2)
    #print('x:',x,default_rect,default_rect2)
    
    text = base_font2.render('Default', True, (25, 25, 255))
    screen.blit(text, (15+default_rect.x, default_rect.y+7))
    return default
        
#THIS SHOULD BE IN MAIN GAME FILE

#define keyboard objects and add them to lst
for i,key in enumerate(KEYS_DESCRIPTION):
    y = 60#pygame.display.get_surface().get_size()[1]//10
    keyboard_key = KeyboardSettings(150+(i*y),key,default_keys[i]) 
    key_obj_lst.append(keyboard_key)

'''
#define dict unicode : pygame key
dict_key = { 'a' : pygame.K_a,
             'b' : pygame.K_b,
             'c' : pygame.K_c,
             'd' : pygame.K_d,
             'e' : pygame.K_e,
             'f' : pygame.K_f,
             'g' : pygame.K_g,
             'h' : pygame.K_h,
             'i' : pygame.K_i,
             'j' : pygame.K_j,
             'k' : pygame.K_k,
             'l' : pygame.K_l,
             'm' : pygame.K_m,
             'n' : pygame.K_n,
             'o' : pygame.K_o,
             'p' : pygame.K_p,
             'q' : pygame.K_q,
             'r' : pygame.K_r,
             's' : pygame.K_s,
             't' : pygame.K_t,
             'u' : pygame.K_u,
             'v' : pygame.K_v,
             'w' : pygame.K_w,
             'x' : pygame.K_x,
             'y' : pygame.K_y,
             'z' : pygame.K_z,

             
             '1' : pygame.K_1,
             '2' : pygame.K_2,
             '3' : pygame.K_3,
             '4' : pygame.K_4,
             '5' : pygame.K_5,
             '6' : pygame.K_6,
             '7' : pygame.K_7,
             '8' : pygame.K_8,
             '9' : pygame.K_9,
             '0' : pygame.K_0,
             
             
             }

'''


    
