
def draw_multyline_text(surface,text,word_pos,font,color,max_width,max_height,rect_color = None,button_rect_color = None , text2 = None):

   
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  
    a,b = word_pos

    
    for line in words:
        for word in line:
            
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if a + word_width >= max_width + word_pos[0]:
                a = word_pos[0] 
                b += word_height 
            surface.blit(word_surface,(a,b))
            a += word_width + space
        a = word_pos[0] 
        b += word_height 
        

        
    if rect_color is not None:
        
        rect_color_big = pygame.Rect(word_pos[0]-20,word_pos[1]-20,max_width+20,b+20-word_pos[1])
        
        if button_rect_color is not None:
            rect_color_big.h = b-word_pos[1]+60

        #rect_color_big_as_tuple = (rect_color_big.x-word_pos[0],rect_color_big.y-word_pos[1],rect_color_big.w,rect_color_big.h)
        pygame.draw.rect(surface,rect_color,(rect_color_big),0,2,2,2,2)
        pygame.draw.rect(screen,(255,188,0),rect_color_big,2,2,2,2,2)

        if button_rect_color is not None:
            
            left_rect_color_small = pygame.Rect(rect_color_big.x +10 ,rect_color_big.bottom - 35,50,28)
            right_rect_color_small = pygame.Rect(rect_color_big.right - 60,rect_color_big.bottom - 35,50,28)

            text_left = font.render(text2[0], True, color)
            text_right = font.render(text2[1], True, color)
            text_left_rect = text_left.get_rect(center = left_rect_color_small.center)
            text_right_rect = text_right.get_rect(center = right_rect_color_small.center)
            
            pygame.draw.rect(screen,button_rect_color,left_rect_color_small,0,2,2,2,2)
            pygame.draw.rect(screen,(255,188,0),left_rect_color_small,2,2,2,2,2)
            pygame.draw.rect(screen,button_rect_color,right_rect_color_small,0,2,2,2,2)
            pygame.draw.rect(screen,(255,188,0),right_rect_color_small,2,2,2,2,2)

            screen.blit(text_left,text_left_rect)
            screen.blit(text_right,text_right_rect)
            return left_rect_color_small,right_rect_color_small
