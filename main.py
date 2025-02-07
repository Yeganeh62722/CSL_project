import pygame
import sys
import math
import ctypes
from ctypes import CDLL, c_float, byref, POINTER
import time

# Initialize Pygame
pygame.init()

# Load the assembly object file
straight_lib = ctypes.CDLL(r'./straight.dll')
curvy_lib = ctypes.CDLL(r'./curvy.dll')
sinusoidal_lib = ctypes.CDLL(r'./sinusoidal.dll')

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Throw Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
STRIPE_COLOR = (255, 255, 0)  # Yellow stripes on the ball

GROUND_HEIGHT = 50
GROUND_Y = HEIGHT - GROUND_HEIGHT
WALL_X = WIDTH - 50
CANNON_WIDTH = 50
CANNON_HEIGHT = 30


# Cannon setting
cannon_image = pygame.image.load('cannon.png')
cannon_image = pygame.transform.scale(cannon_image, (180, 150))
cannon_shooting = False
cannon_animation_speed = 3
cannon_x, cannon_y = 30, GROUND_Y - 55
cannon_angle = 0
min_cannon_angle = -30  # Maximum tilt angle for animation

# Ball settings
ball_rotation_angle = 0
rotation_speed = 5

BALL_RADIUS = 10
ball_x, ball_y = 140, GROUND_Y - 54
ball_speed_x = 6
ball_speed_y = 0
sinusoidal_angle = 0
ball_thrown_straight = False
ball_thrown_sinusoidal = False
ball_thrown_curve = False

# Slider settings
SLIDER_WIDTH, SLIDER_HEIGHT = 200, 5
SLIDER_X, SLIDER_Y = WIDTH // 2 - SLIDER_WIDTH // 2, 80
THUMB_WIDTH, THUMB_HEIGHT = 10, 20
thumb_x = SLIDER_X + 57  # Initial position of the thumb
thumb_rect = pygame.Rect(thumb_x, SLIDER_Y - (THUMB_HEIGHT // 2), THUMB_WIDTH, THUMB_HEIGHT)
dragging_thumb = False
min_speed = 5
max_speed = 15.5
slider_speed = min_speed + (thumb_x - SLIDER_X) / SLIDER_WIDTH * (max_speed - min_speed)


# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 160, 40
straight_button_rect = pygame.Rect(WIDTH // 6 - BUTTON_WIDTH // 2, 60, BUTTON_WIDTH, BUTTON_HEIGHT)
curve_button_rect = pygame.Rect(WIDTH // 6 - BUTTON_WIDTH // 2, 120, BUTTON_WIDTH, BUTTON_HEIGHT)
sinusoidal_button_rect = pygame.Rect(WIDTH // 6 - BUTTON_WIDTH // 2, 180, BUTTON_WIDTH, BUTTON_HEIGHT)
reset_button_rect = pygame.Rect(WIDTH // 6 - BUTTON_WIDTH // 2, 240, BUTTON_WIDTH, BUTTON_HEIGHT)

# Game clock
clock = pygame.time.Clock()
start_time = end_time = 0


def animate_cannon(screen, cannon_image, x, y, angle):
    rotated_cannon = pygame.transform.rotate(cannon_image, -angle)  # Rotate counterclockwise
    cannon_rect = rotated_cannon.get_rect(center=(x + 50, y + 25))  # Adjust position for rotation
    screen.blit(rotated_cannon, cannon_rect)

def animate_ball(screen, x, y, radius, rotation_angle):
    stripe_count  = 8
    pygame.draw.circle(screen, BLUE, (int(x), int(y)), radius)  # Draw ball base

    # Calculate rotated stripes
    for stripe_offset in range(0, 360, int(360 / stripe_count)):
        angle = rotation_angle + stripe_offset
        offset_x = int(radius * math.cos(math.radians(angle)))
        offset_y = int(radius * math.sin(math.radians(angle)))

        # Draw the stripe as a line across the ball
        pygame.draw.line(
            screen,
            STRIPE_COLOR,
            (x - offset_x, y - offset_y),
            (x + offset_x, y + offset_y),
            1  # Line thickness
        )


while True:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if straight_button_rect.collidepoint(event.pos):
                ball_speed_x = slider_speed
                ball_thrown_straight = True
                ball_thrown_curve = False
                ball_thrown_sinusoidal = False
                cannon_shooting = True
                start_time = time.time()
            if curve_button_rect.collidepoint(event.pos):
                ball_speed_x = slider_speed
                ball_speed_y = -4
                ball_thrown_straight = False
                ball_thrown_curve = True
                ball_thrown_sinusoidal = False
                cannon_shooting = True
            if sinusoidal_button_rect.collidepoint(event.pos):
                ball_speed_x = slider_speed
                ball_thrown_straight = False
                ball_thrown_curve = False
                ball_thrown_sinusoidal = True
                cannon_shooting = True
                sinusoidal_angle = 0
            if reset_button_rect.collidepoint(event.pos):
                # Reset ball position and speed
                ball_x, ball_y = 140, GROUND_Y - 54
                ball_speed_x = 0
                ball_thrown_straight = False
                ball_thrown_curve = False
                ball_thrown_sinusoidal = False
                cannon_shooting = False
                sinusoidal_angle = 0
            if thumb_rect.collidepoint(event.pos):
                dragging_thumb = True

        if event.type == pygame.MOUSEBUTTONUP:
            dragging_thumb = False

        if event.type == pygame.MOUSEMOTION and dragging_thumb:
            thumb_x = max(SLIDER_X, min(SLIDER_X + SLIDER_WIDTH - THUMB_WIDTH, event.pos[0]))
            slider_speed = min_speed + (thumb_x - SLIDER_X) / SLIDER_WIDTH * (max_speed - min_speed)
            ball_speed_x = slider_speed

    
    # # Update ball position if thrown straight
    # if ball_thrown_straight:
    #     ball_x += ball_speed_x
    #     if ball_x + BALL_RADIUS >= WALL_X:
    #         print(time.time() - start_time)
    #         ball_speed_x = -ball_speed_x

    # Update ball position if thrown straight
    if ball_thrown_straight:
        # Example game variables
        ball_x = ctypes.c_int(int(ball_x))
        ball_speed_x = ctypes.c_int(int(ball_speed_x))
        straight_lib.update_ball_position.argtypes = [POINTER(ctypes.c_int), POINTER(ctypes.c_int)]
        straight_lib.update_ball_position.restype = None
        # Call the Assembly function
        straight_lib.update_ball_position(byref(ball_x), byref(ball_speed_x))
        ball_x = int(ball_x.value)
        ball_speed_x = int(ball_speed_x.value)
        if ball_x + BALL_RADIUS >= WALL_X:
            print(time.time() - start_time)
            ball_speed_x = -ball_speed_x

    # # Update ball position for curve throw
    # if ball_thrown_curve:
    #     ball_x += ball_speed_x
    #     ball_y +=  ball_speed_y
    #     ball_speed_y += 0.07
    #     if ball_x + BALL_RADIUS >= WALL_X:
    #         ball_speed_x = -ball_speed_x
    #         ball_speed_y = 0
    
    # Update ball position for curve throw
    curvy_lib.update_curve_ball_position.argtypes = (POINTER(c_float), 
                                                     POINTER(c_float), 
                                                     POINTER(c_float), 
                                                     POINTER(c_float))
    curvy_lib.update_curve_ball_position.restype = None
    if ball_thrown_curve:
        ball_x = c_float(ball_x)
        ball_y = c_float(ball_y)
        ball_speed_x = c_float(ball_speed_x)
        ball_speed_y = c_float(ball_speed_y)

        # Call the Assembly function
        curvy_lib.update_curve_ball_position(
            ball_x, ball_y, ball_speed_x, ball_speed_y
        )
        ball_x = float(ball_x.value)
        ball_y = float(ball_y.value)
        ball_speed_x = float(ball_speed_x.value)
        ball_speed_y = float(ball_speed_y.value)
        if ball_x + BALL_RADIUS >= WALL_X:
            ball_speed_x = -ball_speed_x
            ball_speed_y = 0
    
    # # Update ball position for sinusoidald throw
    # if ball_thrown_sinusoidal:
    #     ball_x += ball_speed_x
    #     sinusoidal_angle += 0.1
    #     ball_y = (GROUND_Y - 54) - 50 * math.sin(sinusoidal_angle)
    #     if ball_x + BALL_RADIUS >= WALL_X:
    #         ball_speed_x = -ball_speed_x


    # Update ball position for sinusoidald throw
        sinusoidal_lib.update_sinusoidal_ball_position.argtypes = (c_float, c_float, c_float, c_float)
        sinusoidal_lib.update_sinusoidal_ball_position.restype = None
    if ball_thrown_sinusoidal:
        ball_x = c_float(ball_x)
        ball_y = c_float(ball_y)
        ball_speed_x = c_float(ball_speed_x)
        sinusoidal_angle = c_float(sinusoidal_angle)

        # Call the Assembly function
        sinusoidal_lib.update_sinusoidal_ball_position(byref(ball_x), byref(ball_y), byref(ball_speed_x), byref(sinusoidal_angle))
        
        ball_x = float(ball_x.value)
        ball_y = -float(ball_y.value) - 200
        ball_speed_x = float(ball_speed_x.value)
        sinusoidal_angle = float(sinusoidal_angle.value)
        if ball_x + BALL_RADIUS >= WALL_X:
            ball_speed_x = -ball_speed_x

    if ball_thrown_straight or ball_thrown_curve or ball_thrown_sinusoidal:
        ball_rotation_angle = (ball_rotation_angle + rotation_speed) % 360

    if cannon_shooting:
        if cannon_angle > min_cannon_angle:
            cannon_angle -= cannon_animation_speed  # Rotate forward
        else:
            cannon_shooting = False  # Reset after full rotation
    
    if not cannon_shooting and cannon_angle < 0:
        cannon_angle += cannon_animation_speed

    if ball_y > GROUND_Y:
        ball_speed_y = -ball_speed_y
    
    if ball_x < 0:
        ball_speed_x = 0
        ball_speed_y = 0
        ball_x = -20

    # Draw the ground
    pygame.draw.rect(screen, GREEN, (0, GROUND_Y, WIDTH, GROUND_HEIGHT))
    # Draw the wall
    pygame.draw.rect(screen, GRAY, (WALL_X, 0, 50, HEIGHT))
    # Draw the ball image
    animate_ball(screen, ball_x, ball_y, BALL_RADIUS, ball_rotation_angle)
    # Draw the cannon image
    animate_cannon(screen, cannon_image, cannon_x, cannon_y, cannon_angle)
    # Draw the buttons
    font = pygame.font.SysFont(None, 24)
    # Draw the slider
    pygame.draw.rect(screen, GRAY, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))  # Slider bar
    pygame.draw.rect(screen, RED, thumb_rect)  # Slider thumb
    thumb_rect.x = thumb_x
    # Speed value Label
    speed_text = font.render(f"Speed: {slider_speed:.1f}", True, BLUE)
    screen.blit(speed_text, (SLIDER_X, SLIDER_Y - 30))

    # Straight throw button
    pygame.draw.rect(screen, RED, straight_button_rect)
    straight_text = font.render("Throw Straight", True, WHITE)
    screen.blit(straight_text, (straight_button_rect.x + 10, straight_button_rect.y + 8))
    # Curve throw button
    pygame.draw.rect(screen, RED, curve_button_rect)
    curve_text = font.render("Throw Curvy", True, WHITE)
    screen.blit(curve_text, (curve_button_rect.x + 5, curve_button_rect.y + 8))
    # Sinusoidal throw button
    pygame.draw.rect(screen, RED, sinusoidal_button_rect)
    sinusoidal_text = font.render("Throw Sinusoidal", True, WHITE)
    screen.blit(sinusoidal_text, (sinusoidal_button_rect.x + 5, sinusoidal_button_rect.y + 8))
    # Draw reset button (add this in the drawing section)
    pygame.draw.rect(screen, RED, reset_button_rect)
    reset_text = font.render("Reset Game", True, WHITE)
    screen.blit(reset_text, (reset_button_rect.x + 10, reset_button_rect.y + 8))


    # Update display
    pygame.display.flip()
    clock.tick(60)
