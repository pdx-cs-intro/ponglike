# Single-player pong-like game.
# Bart Massey 2021

from math import *
import sys

import pygame
from pygame.locals import *

pygame.init()

# Set frame rate.
FPS = pygame.time.Clock()
FPS.tick(30)

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
PADDLE_OFFSET_X = 20
PADDLE_SPEED = 1

BALL_RADIUS = 15
BALL_SPEED = 1
# Display width and height
WINDOW_SIZE = (1024, 768)
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ball_x = 0
while True:
    # Restart if needed
    if ball_x <= 0:
        ball_x = 100
        ball_y = WINDOW_SIZE[1] / 2
        paddle_y = ball_y
        # Ball angle is in radians.
        ball_angle = pi / 4

    # Clear the screen.
    pygame.draw.rect(DISPLAYSURF, BLACK, Rect((0, 0), WINDOW_SIZE))
    
    # Move the paddle.
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_UP]:
        paddle_y = paddle_y - PADDLE_SPEED
    elif pressed_keys[K_DOWN]:
        paddle_y = paddle_y + PADDLE_SPEED

    # Draw the paddle.
    paddle_top = paddle_y - PADDLE_HEIGHT / 2
    pygame.draw.rect(DISPLAYSURF, WHITE, Rect(
        (PADDLE_OFFSET_X, paddle_top),
        (PADDLE_WIDTH, PADDLE_HEIGHT),
    ))

    # Move the ball.
    ball_x = ball_x + BALL_SPEED * cos(ball_angle)
    ball_y = ball_y - BALL_SPEED * sin(ball_angle)

    # Handle wall bounces.
    if ball_y > WINDOW_SIZE[1]:
        ball_y = WINDOW_SIZE[1] - (ball_y - WINDOW_SIZE[1])
        dx = cos(ball_angle)
        dy = -sin(ball_angle)
        ball_angle = atan2(dy, dx)
    if ball_y < 0:
        ball_y = - ball_y
        dx = cos(ball_angle)
        dy = -sin(ball_angle)
        ball_angle = atan2(dy, dx)
    if ball_x > WINDOW_SIZE[0]:
        ball_x = WINDOW_SIZE[0] - (ball_x - WINDOW_SIZE[0])
        dx = -cos(ball_angle)
        dy = sin(ball_angle)
        ball_angle = atan2(dy, dx)

    # Handle paddle bounces.
    paddle_face = PADDLE_OFFSET_X + PADDLE_WIDTH
    on_paddle_x = ball_x <= paddle_face and ball_x >= PADDLE_OFFSET_X
    on_paddle = on_paddle_x and \
        ball_y >= paddle_top and ball_y <= paddle_top + PADDLE_HEIGHT
    if on_paddle:
        ball_x = paddle_face + (paddle_face - ball_x)
        dx = -cos(ball_angle)
        dy = sin(ball_angle)
        ball_angle = atan2(dy, dx)

    # Draw the ball.
    pygame.draw.circle(DISPLAYSURF, WHITE, (ball_x, ball_y), BALL_RADIUS)

    # Render to the screen.
    pygame.display.update()

    # Check for quit event.
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
