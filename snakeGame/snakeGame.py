
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

# Clock to control game speed and FPS viewer
clock = pygame.time.Clock()

# Snake settings
SNAKE_BLOCK = 10

# Default FPS options and current FPS
FPS_OPTIONS = {pygame.K_F1: 30, pygame.K_F2: 60, pygame.K_F3: 120}
current_fps = 60

# Global high score (persists during session)
HIGH_SCORE = 0

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)

def display_message(msg, color):
    """Display a centered message on the play area (for non-game over messages)."""
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(mesg, text_rect)

def display_game_over(msg, color):
    """Display a larger, all-caps game-over message at the center of the screen."""
    game_over_font = pygame.font.SysFont("bahnschrift", 50)
    mesg = game_over_font.render(msg.upper(), True, color)
    text_rect = mesg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(mesg, text_rect)

def draw_snake(snake_block, snake_list):
    """Draw the snake segments on the screen."""
    for segment in snake_list:
        pygame.draw.rect(screen, BLACK, [segment[0], segment[1], snake_block, snake_block])

def draw_score(current_score, high_score):
    """Draw the scoreboard on the top border with FPS display."""
    fps_display = clock.get_fps()
    score_text = font_style.render(
        f"Score: {current_score}   High Score: {high_score}   FPS: {fps_display:.1f}", True, BLACK
    )
    screen.blit(score_text, (10, 5))

def game_loop():
    global HIGH_SCORE, current_fps

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
            display_game_over("YOU LOST! PRESS Q TO QUIT OR C TO PLAY AGAIN", RED)
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
                # Handle FPS changes with F1, F2, F3 keys
                if event.key in FPS_OPTIONS:
                    current_fps = FPS_OPTIONS[event.key]

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

        clock.tick(current_fps)

    pygame.quit()
    quit()

if __name__ == "__main__":
    game_loop()
