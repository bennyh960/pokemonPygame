import SETTINGS


def Events(pygame, player):
    KEYS_DICT = {pygame.KEYDOWN: (False, True), pygame.KEYUP: (True, False)}
    player.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            print("Game QUIT! -- run = False")
            return run

        # KEYS_DICT = {pygame.KEYDOWN: (False, True), pygame.KEYUP: (True, False)}
        for dict_key, value in KEYS_DICT.items():
            if event.type == dict_key:
                for k in SETTINGS.key_obj_lst:
                    # define each key by user
                    if k.active:
                        k.keyboard = pygame.key.name(event.key)
                        SETTINGS.default = value[0]

                    if event.key == pygame.key.key_code(k.keyboard):
                        if k.description == 'Moving Right':
                            player.__class__.moving_right = value[1]
                        if k.description == 'Moving Left':
                            player.__class__.moving_left = value[1]
                        if k.description == 'Jump' and player.alive:
                            player.jump = value[1]

    return True
