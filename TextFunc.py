



def draw_text(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))

def draw_multyline_text(surface, screen, pygame, text, word_pos, font, color, max_width, max_height, rect_pos=None,
                        button_rect_color=None, text2=None):

    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    a, b = word_pos
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
