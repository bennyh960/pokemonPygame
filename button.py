#button example import

import pygame

RED = (250,0,0)
BLACK = (25,25,25)

class Button():
    def __init__(self, x, y,image,scalex,scaley):
        #pygame.sprite.Sprite.__init__(self)
        width = image.get_width()
        height = image.get_height()
        self.yscale = 1
        self.image = pygame.transform.scale(image,(int(width * scalex),int(height *scaley)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        
        

    def draw(self,surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditons
        if self.rect.collidepoint(pos):
            pygame.draw.rect(surface, BLACK, (self.rect),4)
            if pygame.mouse.get_pressed()[0] and self.clicked == False: # 0:left click button ,1:middle , 2:rihgt click
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

            
        #draw button on screen
        surface.blit(self.image,(self.rect.x,self.rect.y))
        return action

    def draw2(self,surface):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #pygame.draw.ellipse(surface,(191,176,80),self.rect)

        elips_rect = self.rect.left+8,self.rect.top+5,self.rect.w-15,self.rect.h-10
        #check mouseover and clicked conditons
        if self.rect.collidepoint(pos):
            
            pygame.draw.ellipse(surface,(228,209,88),(elips_rect),4)
            if pygame.mouse.get_pressed()[0] and self.clicked == False: # 0:left click button ,1:middle , 2:rihgt click
                self.clicked = True
                action = True
                #print(self.rect,elips_rect)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

            
        
        #draw button on screen
        surface.blit(self.image,(self.rect.x,self.rect.y))
        return action


