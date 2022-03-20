#pokemon in party class


import pygame


#pygame.init()
pygame.font.init()



#colors
GREEN = (68,255,0)
WHITE = (255,255,255)
BLACK = (40,35,55)

font = pygame.font.SysFont(pygame.font.get_fonts()[8],18)
font3 = pygame.font.SysFont('Futura',27)
font4 = pygame.font.SysFont(pygame.font.get_fonts()[8],23)




class PokemonInParty():
    def __init__(self,name,char_img,x,y,gender,lvl_100_states,hp,atk,deff,spa,spd,speed,max_health,lvl):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.char_img = char_img
        self.char_img_s = pygame.transform.scale(char_img,(45,45))
        self.char_img_l = pygame.transform.scale(char_img,(250,250))
        self.char_img_l_rect = self.char_img_l.get_rect()
        self.char_img_l_rect.center = (800,350)
        
        self.lvl = lvl
        #self.health = 122
        self.max_health = max_health
         
        self.health_green = 350
        #self.health_red = 345
        
        self.x = x+ 30
        self.y = y
        
        self.gender = gender

        self.clicked = False

        self.lvl_100_states = lvl_100_states
        self.hp = int(hp)
        self.atk = int(atk)
        self.deff = int(deff)
        self.spa = int(spa)
        self.spd = int(spd)
        self.speed = int(speed)
        

    def draw(self,surf,img):
        action = False
        #surf.blit(pokemon_in_party_btn_img,(self.x,self.y))
        #surf.blit(img,(self.x,self.y))
        
        pos_on_rect = pygame.Rect(self.x ,self.y,370,78)
        pygame.draw.rect(surf,WHITE,pos_on_rect,0,39)
        #pygame.draw.rect(surf,(185,20,20),pos_on_rect,2,39)
        pygame.draw.line(surf,(185,20,20),(self.x+85,self.y+40),(350,self.y+40),9)
        
        #take mouse curser position
        pos = pygame.mouse.get_pos()
        
##        if pygame.mouse.get_pressed()[0]:
##            print(pos)
##
##        temp_pos_rect = pygame.Rect(0 ,0,100,100)
##        pygame.draw.rect(surf,(0,0,0),temp_pos_rect)
##        if temp_pos_rect.collidepoint(pos):
##            print('self health,max_health,x,y')
##            print(self.hp,self.max_health,self.x,self.y)
##            print(350 * self.hp/self.max_health)
            
            
        if pos_on_rect.collidepoint(pos):
            pygame.draw.rect(surf,BLACK,pos_on_rect,0,39)
            if pygame.mouse.get_pressed()[0]:# and self.clicked == False:
                self.clicked = True
                action = True
                

                

            color = WHITE
        else:
            color = BLACK

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        self.health_green = 350 * self.hp/self.max_health
        
##        if self.name == "Bulbasaur":
##            #print(self.health_green,self.x)
##            print(self.hp,self.max_health,self.x)
            
        surf.blit(self.char_img_s,(self.x+35,self.y+20))
        pygame.draw.line(surf,GREEN,(self.x+85,self.y+40),(int(self.health_green),self.y+40),10)
        #pygame.draw.line(surf,BLACK,(self.x+85+30,10),(self.health_green,10),10)

        
        name_text = font3.render(self.name,True,color)
        lv_text = font3.render(f"Lv. {self.lvl}",True,color)
        health_text = font3.render(f'{self.hp}/{self.max_health}',True,color)


        # draw gender
        
        
        if self.gender in ['male','Male','MALE']:
            gender = font4.render('\u2642',True,WHITE) #male
            g_color = (0,0,255)
        else:
            gender = font4.render(chr(0x2640),True,WHITE) #female
            g_color = (255,0,0)
            
        gender_rect = gender.get_rect()
        gender_rect.center = (self.x + 280,self.y+23)
        
        surf.blit(name_text,(self.x+85,self.y+15))
        surf.blit(lv_text,(self.x+285,self.y+50))
        surf.blit(health_text,(self.x+85,self.y+50))

        
        pygame.draw.circle(surf,g_color,(gender_rect.center),11)
        surf.blit(gender,gender_rect)

            
        
        return action


    def draw_state(self,surf):
        #define Trigo
        cos30 = (3**0.5)/2
        tan30 = (3**0.5)/3

        # Center of polygone
        cx = 940
        cy = 165


        # polygone variable (x only)
        X = 110

        # affected from x
        V = X/cos30
        Y = -((V**2)-(X**2))**0.5

        #define colors
        bg_color = (225,254,250)
        gray = (229,229,229)

        #define states related to V ###self.lvl_100_states[self.hp,self.atk,self.deff,self.spa,self.spd,self.speed,self.energy]
        hp = int(V * self.max_health / self.lvl_100_states[0])
        atk = int(X * self.atk / self.lvl_100_states[1])  
        deff = int(X * self.deff / self.lvl_100_states[2])
        spa = int(X * self.spa / self.lvl_100_states[3])
        spd = int(X * self.spd / self.lvl_100_states[4])
        
        speed = int(self.speed * V/ (self.lvl_100_states[5]+120))
        
        #drawing
        pygame.draw.polygon(surf,gray,[(cx+X,cy+Y),(cx+X,cy-Y),(cx,cy+V),(cx-X,cy-Y),(cx-X,cy+Y),(cx,cy-V)])
        
        pygame.draw.line(surf,bg_color,(cx+X,cy+Y),(cx-X,cy-Y),3)
        pygame.draw.line(surf,bg_color,(cx+X,cy-Y),(cx-X,cy+Y),3)
        pygame.draw.line(surf,bg_color,(cx,cy+V),(cx,cy-V),3)

        BLUE = (0, 50, 255, 100) # transperent color on new surface "my_image"
        
        #size = width, height = (surf_WIDTH+300, surf_HEIGHT) pygame.display.get_surface().get_size()
        size = width, height = (pygame.display.get_surface().get_size())
        #size = width, height = (800,600)
        my_image = pygame.Surface(size, pygame.SRCALPHA)  # Creates an empty per-pixel alpha Surface.
        #transperent polygon - actual pokemon states
        pygame.draw.polygon(my_image,BLUE,[(cx,cy-hp),(cx+atk,cy-(atk*tan30)),(cx+deff,cy+(deff*tan30)),(cx,cy+speed),(cx-spa,cy+(spa*tan30)),(cx-spd,cy-(spd*tan30))])
        surf.blit(my_image, (0,0))

        # draw text
        
        
        hp1 = font.render('HP',True,BLACK)
        hp2 = font.render(f'{self.hp}/{self.max_health}',True,BLACK)
        surf.blit(hp1,(cx-10,cy-V-30))
        surf.blit(hp2,(cx-35,cy-V-13))
        speed1 = font.render('SPEED',True,BLACK)
        speed2 = font.render(f'{self.speed}',True,BLACK)
        surf.blit(speed1,(cx-18,cy+V))
        surf.blit(speed2,(cx-15,cy+V+20))
        atk_spa1 = font.render('Sp.Atk                       Attack',True,BLACK)
        atk_spa2 = font.render(f'{self.spa}                          {self.atk}',True,BLACK)
        surf.blit(atk_spa1,(cx-X-60,cy+Y-30))
        surf.blit(atk_spa2,(cx-X-40,cy+Y-10))
        def_spd1 = font.render('Sp.Def                       Deffence',True,BLACK)
        def_spd2 = font.render(f'{self.spd}                          {self.deff}',True,BLACK)
        surf.blit(def_spd1,(cx-X-60,cy-Y+10))
        surf.blit(def_spd2,(cx-X-40,cy-Y+30))
            
        
    def update(self,atk,deff,spa,spd,speed):
        self.atk = atk
        self.deff = deff
        self.spa = spa
        self.spd = spd
        self.speed = speed
        #self.energy
        #self.reg
##
##bulba = PokemonInParty("bulba",bulba_img,25,90,'male',Bulbasaur.states_update(100),129,60,80,20,40,100,130,52)
##squirtle = PokemonInParty("squir",squir_img,25,180,'male',Squirtle.states_update(100),119,60,80,20,40,100,120,5)
##charma = PokemonInParty("charma",charma_img,25,270,'female',Charmander.states_update(100),119,60,80,20,40,100,190,10)
##charma2 = PokemonInParty("charma",charma_img,25,360,'female',Charmander.states_update(100),59,60,80,20,40,100,115,20)
##charma3 = PokemonInParty("charma",charma_img,25,450,'male',Charmander.states_update(100),69,60,80,20,40,100,101,30)
##charma4 = PokemonInParty("charma",charma_img,25,538,'female',Charmander.states_update(100),139,60,80,20,40,100,100,21)
##
##
##
##
##characters = [bulba,squirtle,charma,charma2,charma3,charma4]
##show_pokemon = characters[0]
##
##run = True
##while run:
##    
##    draw_bg()
##
##    for i,character in enumerate(characters):
##        if character.draw():
##            show_pokemon = characters[i]        
##    surf.blit(show_pokemon.char_img_l,(850,330))
##    show_pokemon.draw_state()
##    
##    
##
##    for event in pygame.event.get():
##        # quit game
##        if event.type == pygame.QUIT:
##            run = False
##
##
##    
##    pygame.display.update()
##
##pygame.quit()
