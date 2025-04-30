"""
Drum Machine Game
Date: [2005-04-30]
Version: 1.0
Python Version: 3.13.1
"""

import pygame


pygame.init()

"Screen size"
WIDTH = 1400
HEIGHT = 800

"Colour options"
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font('D:\iCloudDrive\CODE\GiTHUB\python\drum machine\Roboto\Roboto-Italic-VariableFont_wdth,wght.ttf', 32)

fps = 60
timer = pygame.time.Clock()

"Function to draw the grid"
def draw_grid():
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]

    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30, 30))



run = True
while run:
    timer.tick(fps) 
    
    "Making background black"
    screen.fill(black) 

    draw_grid()

    "Checking inputs"
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False  

    pygame.display.flip()
pygame.quit()