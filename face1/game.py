from PIL import Image
import pygame
import sys
from pygame.locals import QUIT


pygame.init()
screen_width, screen_height = 1800, 200  
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)


character_image = Image.open("D:/BAP TAP Python/face1/hinhanhtet1.png")
character_image = character_image.convert("RGBA")

initial_width, initial_height = 400, 200
character_surface = pygame.image.fromstring(character_image.tobytes(), character_image.size, character_image.mode)
character_surface = pygame.transform.scale(character_surface, (initial_width, initial_height))

transparent_color = (255, 0, 255, 0)
character_surface.set_colorkey(transparent_color)

character_rect = character_surface.get_rect()

font = pygame.font.SysFont(None, 36)
text_surface = font.render("Xin Chao Đen Voi Chuong trinh Nhân Diên Khuôn Măt", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 20))

current_width, current_height = initial_width, initial_height

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                current_width += 10
                current_height += 10
                character_surface = pygame.transform.scale(character_surface, (current_width, current_height))

    character_rect.x += 2
    if character_rect.x > screen_width:
        character_rect.x = 0
    screen.fill((0, 0, 0))  
    screen.blit(character_surface, character_rect)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(30)
