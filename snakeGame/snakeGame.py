### snake_game.py

import pygame
import random

# Initialize pygame
pygame.init()

# Window and game area dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCOREBOARD_HEIGHT = 40  # Height for the top scoreboard
PLAY_AREA_HEIGHT = SCREEN_HEIGHT - SCOREBOARD_HEIGHT
BORDER_THICKNESS = 5    # Thick black border for play area

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY  = (200, 200, 200)

# Game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock to control game speed
clock = pygame.time.Clock()

# Snake settings
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Global high score (persists during session)
HIGH_SCORE = 0

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)

def display_message(msg, color):
    """Display a centered message on the play area."""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2])

def draw_snake(snake_block, snake_list):
    """Draw the snake segments on the screen."""
    for segment in snake_list:
        pygame.draw.rect(screen, BLACK, [segment[0], segment[1], snake_block, snake_block])

def draw_score(current_score, high_score):
    """Draw the scoreboard on the top border."""
    score_text = font_style.render(f"Score: {current_score}   High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 5))

def game_loop():
    global HIGH_SCORE

    game_over = False
    game_close = False

    # Starting position of the snake's head (centered in play area)
    x = SCREEN_WIDTH / 2
    y = SCOREBOARD_HEIGHT + (PLAY_AREA_HEIGHT / 2)

    # Movement variables
    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    # Initial food position (inside the play area boundaries)
    food_x = round(random.randrange(BORDER_THICKNESS, SCREEN_WIDTH - BORDER_THICKNESS - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(SCOREBOARD_HEIGHT + BORDER_THICKNESS, SCREEN_HEIGHT - BORDER_THICKNESS - SNAKE_BLOCK) / 10.0) * 10.0

    while not game_over:

        while game_close:
            screen.fill(WHITE)
            display_message("You lost! Press Q-Quit or C-Play Again", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Prevent reverse direction by checking current movement
                if event.key == pygame.K_LEFT and x_change != SNAKE_BLOCK:
                    x_change = -SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change != -SNAKE_BLOCK:
                    x_change = SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_UP and y_change != SNAKE_BLOCK:
                    y_change = -SNAKE_BLOCK
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change != -SNAKE_BLOCK:
                    y_change = SNAKE_BLOCK
                    x_change = 0

        x += x_change
        y += y_change

        # Fill background and draw scoreboard border
        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, [0, 0, SCREEN_WIDTH, SCOREBOARD_HEIGHT])
        draw_score(snake_length - 1, HIGH_SCORE)

        # Draw thick black border for the play area
        pygame.draw.rect(screen, BLACK, [0, SCOREBOARD_HEIGHT, SCREEN_WIDTH, PLAY_AREA_HEIGHT], BORDER_THICKNESS)

        # Collision detection with play area border (inside the thick border)
        if (x < BORDER_THICKNESS or 
            x > SCREEN_WIDTH - BORDER_THICKNESS - SNAKE_BLOCK or 
            y < SCOREBOARD_HEIGHT + BORDER_THICKNESS or 
            y > SCREEN_HEIGHT - BORDER_THICKNESS - SNAKE_BLOCK):
            game_close = True

        # Draw food inside the play area
        pygame.draw.rect(screen, GREEN, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for collision with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(SNAKE_BLOCK, snake_list)
        pygame.display.update()

        # Check if snake has eaten the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(BORDER_THICKNESS, SCREEN_WIDTH - BORDER_THICKNESS - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(SCOREBOARD_HEIGHT + BORDER_THICKNESS, SCREEN_HEIGHT - BORDER_THICKNESS - SNAKE_BLOCK) / 10.0) * 10.0
            snake_length += 1

            # Update high score if necessary
            if (snake_length - 1) > HIGH_SCORE:
                HIGH_SCORE = snake_length - 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

if __name__ == "__main__":
    game_loop()
