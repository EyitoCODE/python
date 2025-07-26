# Python Snake Game

A simple snake game implemented in Python using [pygame](https://www.pygame.org/).

## How to Play
- Use the arrow keys to move the snake.
Eat the green food block to grow longer.
Avoid hitting the boundaries or your own tail.
- Press F1 for 30 FPS, F2 for 60 FPS, and F3 for 120 FPS.
- The current FPS is displayed on the scoreboard.

## Changelog
- Window Size Increased: The window is now 800x600.
- Scoreboard Border: A top border displays the current score, high score, and current FPS.
- Play Zone Border: A thick black border has been added around the play area.
- Bug Fix: Prevented the snake from reversing direction instantly (which caused a game-over) by ignoring input that would reverse the snake's current direction.
- Game Over Screen: Updated to use a larger, all-caps, centered message.
FPS Options and Viewer: Added options to switch between 30, 60, and 120 FPS and display the current FPS.

## Features

- Basic snake movement controlled by the arrow and wasd keys.
- Muliple difficulty options (30, 45, and 60 FPS).
- Food that appears randomly on the screen.
- Growing snake each time food is eaten.
- Game-over condition when the snake hits the window border or itself.

## Requirements

- Python 3.13.1
- [pygame](https://www.pygame.org/) library

## Current bugs
- Different fps options causes the snake to move faster
- Game over screen overextends the screen

## Future improvements
- Add sfx and better designs for the snake and the food
- Global leader board
- Different map
- Different game modes

