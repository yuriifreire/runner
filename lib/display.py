from pygame import Rect

def draw_screen(screen,area,player,terrain,score_display):
    screen.fill((255,255,255))

    screen_rect = screen.get_rect()

    screen_rect.centerx = player.rect.centerx

    screen_rect.clamp_ip(area)

    blit_image,blit_rect = player.get_blit_info()

    blit_rect.left -= screen_rect.left

    screen.blit(blit_image, blit_rect.topleft)

    for tile in terrain:
        blit_image, blit_rect = tile.image, tile.rect

        if blit_rect.colliderect(screen_rect):
            blit_rect = Rect(blit_rect)
            blit_rect.left -= screen_rect.left

            screen.blit(blit_image,blit_rect.topleft)
