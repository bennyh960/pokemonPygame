# pokemondata file
import random
import pygame
from math import pi
#import csv

pygame.font.init()

#images
##pysical_tm_img = pygame.image.load(r'images\game_background1\tm_graphic\pysical_tm_img.jpg')#.convert_alpha()
##special_tm_img = pygame.image.load(r'images\game_background1\tm_graphic\special_tm_img.jpg')#.convert_alpha()
##status_tm_img = pygame.image.load(r'images\game_background1\tm_graphic\status_tm_img.jpg')#.convert_alpha()
##
##energy_tm_img = pygame.image.load(r'images\game_background1\tm_graphic\energy_tm_img.png')#.convert_alpha()
##reg_tm_img = pygame.image.load(r'images\game_background1\tm_graphic\reg_tm_img.png')#.convert_alpha()
##range_tm_img = pygame.image.load(r'images\game_background1\tm_graphic\range_tm_img.png')#.convert_alpha()

#img_lst = [pysical_tm_img,eng_text,energy_tm_img,power_text,reg_tm_img,power_text,range_tm_img,power_text]


class Pokemon():
    def __init__(self,name,scale,hp,speed,fake_speed,tm1,tm2,typ1,typ2,energy,atk,deff,spa,spd,form,reg,tm_lvl):#,reg,form):
        self.name = name
        self.scale = scale
        self.hp = hp
        self.speed = speed
        
        
        self.tm1 = tm1 # pp
        self.tm2 = tm2 # pp
        self.typ1 = typ1
        self.typ2 = typ2
        self.energy = energy
        self.atk = atk
        self.deff = deff
        self.spa = spa
        self.spd = spd
        self.fake_speed = fake_speed
        
        


        #self.average = (self.hp + self.speed + self.energy + self.atk + self.deff + self.spa +self.spd)// 7


        self.form = form
        self.reg = reg
        
        self.state_lst = [self.hp,self.atk,self.deff,self.spa,self.spd,self.energy,self.reg,self.fake_speed]

        # for lvl_100 only
        self.hp_100 = hp
        self.atk_100 = atk
        self.deff_100 = deff
        self.spa_100 = spa
        self.spd_100 = spd
        self.speed_100 = speed
        self.energy_100 = energy
        self.reg_100 = reg
        self.fake_speed_100 = fake_speed
        self.lvl_100 = True

        self.tm_lvl = tm_lvl      


    def states_update(self,lvl):
        lvl_up_state = []
        
        for i in range(lvl-5):
            for state in self.state_lst:
                #averege_state = (self.hp + self.atk + self.deff + self.spa + self.spd + self.energy)// len(self.state_lst)-1# + self.reg)// len(self.state_lst)
                #reduced speed from avg calc
                averege_state = sum([self.hp,self.atk,self.deff,self.spa,self.spd,self.energy,self.reg,self.fake_speed])//8
                
                if state < averege_state - 5 :
                    lvl_up = random.randint(0,1)
                elif state < averege_state and state >= averege_state - 5:
                    lvl_up = random.randint(1,2)
                elif state >= averege_state and state < averege_state + 3:
                    lvl_up = 2
                elif state >= averege_state + 5:
                    lvl_up = random.randint(2,4)
                elif state >= averege_state + 10:
                    lvl_up = random.randint(3,4)
                else:
                    lvl_up = random.randint(0,3)
##                    print('else',state)
                
                if self.form == 2:
                    lvl_up += random.randint(0,1)
                elif self.form == 3:
                    lvl_up += random.randint(1,2)
                elif self.form == "legend":
                    lvl_up += random.randint(1,3)
                
                lvl_up_state.append(lvl_up)
            
        #for i in range(lvl-5):
            self.hp += lvl_up_state[0]
            self.atk += lvl_up_state[1]
            self.deff += lvl_up_state[2]
            self.spa += lvl_up_state[3]
            self.spd += lvl_up_state[4]
            #self.speed += lvl_up_state[5]
            self.energy += lvl_up_state[5]
            self.reg += lvl_up_state[6]
            self.fake_speed += lvl_up_state[7]
            lvl_up_state = []

        #update_state_lst = [self.hp,self.atk,self.deff,self.spa,self.spd,self.speed,self.energy,self.reg]
            
        #return update_state_lst
        return self.hp,self.atk,self.deff,self.spa,self.spd,self.speed,self.energy,self.reg,self.fake_speed

    def lvl_100_states(self,lvl):
        lvl_up_state = []
        hp,atk,deff,spa,spd,energy,reg,fake_speed = 0,0,0,0,0,0,0,0
        for i in range(lvl-5):
            for state in self.state_lst:
                averege_state = sum([self.hp,self.atk,self.deff,self.spa,self.spd,self.energy,self.reg,self.fake_speed])//8
                #averege_state = sum([self.hp_100,self.atk_100,self.deff_100,self.spa_100,self.spd_100,self.energy_100,self.reg_100,self.fake_speed_100])//8
                
                if state < averege_state - 5 :
                    lvl_up = 1
                elif state < averege_state and state >= averege_state - 5:
                    lvl_up = 2
                elif state >= averege_state and state < averege_state + 3:
                    lvl_up = 2
                elif state >= averege_state + 5:
                    lvl_up = 4
                elif state >= averege_state + 10:
                    lvl_up = 4
                else:
                    lvl_up = 3
                
                if self.form == 2:
                    lvl_up += 1
                elif self.form == 3:
                    lvl_up += 2
                elif self.form == "legend":
                    lvl_up += 3
                
                lvl_up_state.append(lvl_up)
            
        #for i in range(lvl-5):
            hp += lvl_up_state[0]
            atk += lvl_up_state[1]
            deff += lvl_up_state[2]
            spa += lvl_up_state[3]
            spd += lvl_up_state[4]
            #speed += lvl_up_state[5]
            energy += lvl_up_state[5]
            reg += lvl_up_state[6]
            fake_speed += lvl_up_state[7]
            lvl_up_state = []
                        
        self.hp_100 += hp
        self.atk_100 += atk
        self.deff_100 += deff
        self.spa_100 += spa
        self.spd_100 += spd
        #self.speed += lvl_up_state[5]
        self.energy_100 += energy
        self.reg_100 += reg
        self.fake_speed_100 += fake_speed
            

        lvl_100_state_lst = [self.hp_100,self.atk_100,self.deff_100,self.spa_100,self.spd_100,self.speed_100,self.energy_100,self.reg_100,self.fake_speed_100]
            
        return lvl_100_state_lst

########################################################################################################################################################
########################################################################################################################################################

#TM function and view
Pokemon_types = ['electric','normal','steel','grass','ghost','poison','fly','fire','water','dragon','dark','psychic','fairy','ice','bug','rock','ground','fight']
types_color   = [(210,240,10),(149,140,110),(100,100,100),(36,209,71),(186,36,209),(220,110,238),(122,110,238),(253,121,65),(65,209,253),\
                 (109,65,253),(70,41,30),(255,251,15),(255,122,229),(186,250,248),(102,151,4),(168,144,80),(169,127,11),(246,72,136)]
#yello,lightgray,gray,
types_color_dict = dict(zip(Pokemon_types,types_color))

class TMS_TIMERS():
    
    def __init__(self,text,reg,eng,power,typ,category,rang):
        self.tm_active = False
        self.event_timer_tm = 0

        #self.x = x
        #self.y = y
        self.text = text

        self.clicked = False

        self.reg = reg
        self.eng = eng
        self.power = power
        self.type = typ
        self.color = types_color_dict[self.type]
        self.category = category

        self.num_in_movset = 5#None
        #in future
        #self.speed = speed
        self.range = rang

        #self.already_clicked = False
        #for draw2 only 
        self.rect = None
        self.moving_rect = False

        self.RemovedByUser = False

    def draw(self,rect,surface,player,category_img):
        
        
        color_100  = self.color + (150,)
        color_168 = self.color + (168,)
        #draw tm rect
        pygame.draw.rect(surface,(color_100),rect,0,3,3,3,3)
        pygame.draw.rect(surface,(self.color),rect,3,3,3,3,3)        
        
        # define tm name and pos it.
        text = font_tm.render(self.text,True,(255,255,255))
        text_rect = text.get_rect(center=(rect.center))
        
        #typ_text = font0_0.render(self.type,True,(255,255,255))
        #typ_text_rect = text.get_rect(topleft=(text_rect.centerx-45,text_rect.centery-31))
        #pwr_text = font0_0.render('Power:'+str(self.power),True,(255,255,255))
        #pwr_text_rect = text.get_rect(topleft=(text_rect.centerx-45,text_rect.centery))

        eng_text = font0_0.render('Eng:'+str(self.eng),True,(255,255,255))
        eng_text_rect = text.get_rect(topleft = (rect.centerx+15,text_rect.centery-28))

        # if clicked activate timer and tm 
        if self.clicked == True and player.energy > self.eng and self.tm_active == False:
            self.tm_active = True
            #self.clicked = False
            #self.already_clicked = True
            player.energy -= self.eng
            #print(player.energy , self.eng)
        
       

        #radius = 30 * percentage
        surface.blit(text, text_rect)
        #surface.blit(typ_text, typ_text_rect)
        #surface.blit(pwr_text, pwr_text_rect)
        surface.blit(eng_text, eng_text_rect)

        category_img_rect = category_img.get_rect(center = (rect.centerx,rect.centery+17))
        surface.blit(category_img,category_img_rect)

        #timer regeneration
        percentage = self.event_timer_tm/self.reg
        end_angle = 2 * pi * percentage
        #draw timer 
        pygame.draw.arc(surface, (color_168), (rect.x+5,rect.y+5,rect.w-10,rect.h-5), 0, end_angle,120)


    def draw2(self,surface,img1,img2,img3,img4,img_typ_icon):
        

        color_text = (20,20,20)
        color_100  = self.color + (140,)
        color_168 = self.color + (188,)
        #draw tm rect
        pygame.draw.rect(surface,(color_100),self.rect,0,5)
        pygame.draw.rect(surface,(self.color),self.rect,4,5)        
        
        # define tm name and pos it.
        text = font_tm2.render(self.text,True,color_text)
        text_rect = text.get_rect(center=(self.rect.center))
        
        typ_text = font0_02.render('Type:'+self.type,True,color_text)
        typ_text_rect = typ_text.get_rect(center=(self.rect.centerx,self.rect.centery+typ_text.get_height()))

        
##        eng_text_rect = eng_text.get_rect(topleft = (self.rect.centerx+15,text_rect.centery-31))
        if self.category == 'status':
            text_power = '-'
        else:
             text_power = str(self.power)
             
        power_text = font0_0.render(text_power,True,color_text)
        eng_text = font0_0.render(str(self.eng),True,color_text)
        reg_text = font0_0.render(str(self.reg),True,color_text)
        range_text = font0_0.render(str(self.range),True,color_text)
        
        surface.blit(text, text_rect)
        surface.blit(typ_text, typ_text_rect)

        surface.blit(img_typ_icon, (self.rect.x + 5,self.rect.y + 25 ))
        

        #img_lst = [pysical_tm_img,eng_text,energy_tm_img,power_text,reg_tm_img,power_text,range_tm_img,power_text]
        img_lst = [img1,power_text,img2,eng_text,img3,reg_text,img4,range_text]
        space_width,space_height = img2.get_width(),img2.get_height()  
        
        for i,img in enumerate(img_lst):         
            if i % 2 == 0 :
                img_rect = img.get_rect(center=(self.rect.x +20 +  (i *space_width*2),self.rect.top + space_height))
                surface.blit(img,img_rect)
            else:
                img_rect = img.get_rect(center=(self.rect.x +20 + space_width + ((i-1) *space_width*2),self.rect.top + space_height))
                surface.blit(img,img_rect)

                      


########################################################################################################################################################
'''TM OBJECT CREATION '''
########################################################################################################################################################
                  
        
#Timer for TM cooldown
font_tm = pygame.font.SysFont('Futura',15)
font_tm2 = pygame.font.SysFont('Futura',25)
font0_0 = pygame.font.SysFont(pygame.font.get_fonts()[0],12)
font0_02 = pygame.font.SysFont(pygame.font.get_fonts()[0],17)
#electric
#                                         ,reg,eng,power,typ,caregory,range
thundershock = TMS_TIMERS("THUNDERSHOCK ",3,10,20,'electric','special',5)
thunder = TMS_TIMERS("THUNDER",15,60,120,'electric','special',7)
thunderbolt = TMS_TIMERS("THUNDERBOLT",7,40,95,'electric','special',8)
electro_web = TMS_TIMERS("ELECTRO WEB",20,5,0,'electric','status',3)
volt_switch = TMS_TIMERS("VOLT SWITCH",20,45,45,'electric','special',5)

#normal
tackle = TMS_TIMERS("TACKLE",3,10,20,'normal','pysical',2)
quick_atk = TMS_TIMERS("QUICK ATTACK",6,10,40,'normal','pysical',1)
scratch = TMS_TIMERS("SCRATCH",1,10,10,'normal','pysical',1)
witherdaw = TMS_TIMERS("WITHERDAW",10,30,0,'normal','status',0)
skull_bush  = TMS_TIMERS("SKULL BUSH",6,40,50,'normal','pysical',1)

#grass
bullet_seed = TMS_TIMERS("BULLET SEED",3,10,20,'grass','pysical',7)
vine_wheep = TMS_TIMERS("VINE WHEEP",4,12,30,'grass','pysical',4)
reazor_leaf = TMS_TIMERS("REAZOR LEAF",5,30,40,'grass','special',8)
par_pdr = TMS_TIMERS("PARALYZE POWDER",20,40,0,'grass','status',3)

#poison
psn_pdr = TMS_TIMERS("POISON POWDER",20,40,0,'poison','status',2)
sludge_bmb = TMS_TIMERS("SLUDGE BOMB",6,50,85,'poison','special',5)

#steel
iron_tail = TMS_TIMERS("IRON TAIL",5,10,40,'steel','pysical',3)


#fire
ember = TMS_TIMERS("EMBER",3,10,20,'fire','special',3)
fire_punch = TMS_TIMERS("FIRE PUNCH",5,20,40,'fire','pysical',2)
sunny_day = TMS_TIMERS("SUNNY DAY",20,60,0,'fire','status',8)
Flamthrowr = TMS_TIMERS("FLAMTHROWER",6,30,40,'fire','special',7)
Fire_Blast = TMS_TIMERS("FIRE BLAST",20,55,95,'fire','special',10)

#water
boublle = TMS_TIMERS("BOUBLLE",3,10,20,'water','special',4)
water_gun = TMS_TIMERS("WATER GUN",4,20,40,'water','special',6)
rain_dance = TMS_TIMERS("RAIN DANCE",20,60,0,'water','status',8)
hydro_pump = TMS_TIMERS("HYDRO PUMP",6,50,95,'water','special',10)


##
#######
##trainer_teach_tm = [sludge_bmb,rain_dance]

# pokemon moves per level dict
picka_tm_lvl = {3: thundershock,8:quick_atk,15 :iron_tail , 21:electro_web ,27: thunderbolt,35:volt_switch,49:thunder}
bulba_tm_lvl = {3: bullet_seed,7:tackle,12 :vine_wheep , 17:reazor_leaf ,24: psn_pdr,33:par_pdr,44:sludge_bmb}
suir_tm_lvl = {3: boublle, 7:tackle,13 :witherdaw , 15:water_gun ,22:rain_dance,30:skull_bush,48:hydro_pump}
#char_tm_lvl = {3: ember,6 :scratch , 7:fire_punch ,8: sunny_day,9:Flamthrowr,10:Fire_Blast,4: thundershock,5:quick_atk,2 :iron_tail }
char_tm_lvl = {3: ember,6 :scratch , 13:fire_punch ,23: sunny_day,34:Flamthrowr,46:Fire_Blast}



########################################################################################################################################################
'''POKEMON OBJECT CREATION '''
########################################################################################################################################################

####################name,scale, hp,speed,fake_speed,tm1,tm2,typ1,typ2,energy,atk,deff,spa,spd,form,reg,tm_lvl)
Pikachu = Pokemon("Pikachu",1.15,50,6,90,500,50,'electric','',120,100,200,100,210,1,3,picka_tm_lvl)

Bulbasaur = Pokemon("Bulbasaur",1.3,55,5,60,500,50,'grass','poison',60,45,52,57,65,1,4,bulba_tm_lvl)
Ivysaur = Pokemon("Ivysaur",2,60,5.2,85,500,50,'grass','poison',80,62,63,80,80,2,5,bulba_tm_lvl)
Venusaur = Pokemon("Venusaur",2.7,86,5.3,100,500,50,'grass','poison',108,83,94,93,94,3,6,bulba_tm_lvl)

Charmander = Pokemon("Charmander",1.3,39,5,63,500,50,'fire','fly',70,52,43,53,47,1,2,char_tm_lvl)
Charmeleon = Pokemon("Charmeleon",1.55,58,5.1,80,500,50,'fire','fly',90,64,58,65,62,2,3,char_tm_lvl)
Charizard = Pokemon("Charizard",2.7,78,5.5,110,500,50,'fire','fly',110,84,78,85,81,3,4,char_tm_lvl)

Squirtle = Pokemon("Squirtle",1.3,44,4,48,500,50,'water','',62,50,65,53,54,1,2,suir_tm_lvl)
Wartortle = Pokemon("Wartortle",1.55,59,4.6,69,500,50,'water','',78,63,80,65,68,2,3,suir_tm_lvl)
Blastoise = Pokemon("Blastoise",2.7,79,4.9,93,500,50,'water','',85,84,101,85,93,3,4,suir_tm_lvl)

# do not touch in '' string its important (related to dictionary of game world and tiles-pokemon)
pokemon_object_lst = ['',Bulbasaur,Ivysaur,Venusaur,
       Charmander,Charmeleon,Charizard,
       Squirtle,Wartortle,Blastoise
                      ]

##for i in range(100):
##    if i in Squirtle.tm_lvl.keys():
##        print("lvl:",i,Squirtle.tm_lvl[i])
        
##while True:
##    if hasattr(Bulbasaur, "lvl_100"):
##        x = int(input('enter pokemon lvl value'))
##        print(x,Bulbasaur.states_update(x))
##        del Bulbasaur.lvl_100 
##print(7,Bulbasaur.states_update(7))
##print(8,Bulbasaur.states_update(8))
##print(9,Bulbasaur.states_update(9))
##print(10,Bulbasaur.states_update(10))
##print(50,Bulbasaur.states_update(50))
##print(51,Bulbasaur.states_update(51))
##print(52,Bulbasaur.states_update(52))
##print(53,Bulbasaur.states_update(53))
##print(54,Bulbasaur.states_update(54))
#print(90,Bulbasaur.states_update(90))
#print(100,Bulbasaur.lvl_100_states(99))
#print(100,Squirtle.lvl_100_states(99))

#print(Bulbasaur.states_update(11))

##with open('pokemon_levels_csv\\pokemon_level_states#p1.csv',newline = '') as csvfile:
##                            reader = csv.reader(csvfile,delimiter =',')
##
##
##                            for x,row in enumerate(reader):
##                                for y, tile in enumerate(row):
##                                    world_data[x][y] = int(tile)
##                        world = World()
##                        player,health_bar,energy_bar,health_bar_enemy = world.process_data(world_data)
##                        player.exp = temp_exp
##                        player.lvl = temp_lvl

##for pokemon in pokemon_object_lst[1:]:
##    
##    with open(f'pokemon_levels_csv\\{pokemon.name} states#p1.csv','w',newline ='')as csvfile:
##        writer = csv.writer(csvfile,delimiter = ',')
##        for i in range(6,101):
##            writer.writerow(pokemon.states_update(i))


