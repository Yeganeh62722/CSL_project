import pygame
import sys
import math

# Initialize Pygame
pygame.init()

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

cannon_image = pygame.image.load('cannon.png')
cannon_image = pygame.transform.scale(cannon_image, (200, 180))


GROUND_HEIGHT = 50
GROUND_Y = HEIGHT - GROUND_HEIGHT
WALL_X = WIDTH - 50
CANNON_WIDTH = 50
CANNON_HEIGHT = 30

BALL_RADIUS = 15
ball_x, ball_y = 177, GROUND_Y - BALL_RADIUS * 2
ball_speed_x = 0
ball_speed_y = 0
cannon_x, cannon_y = 0, GROUND_Y - 85

ball_thrown_straight = False
ball_thrown_sinusoidal = False
ball_thrown_curve = False
sinusoidal_angle = 0

# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 160, 40
straight_button_rect = pygame.Rect(WIDTH // 6 - BUTTON_WIDTH // 2, 60, BUTTON_WIDTH, BUTTON_HEIGHT)
curve_button_rect = pygame.Rect(WIDTH // 6 - BUTTON_WIDTH // 2, 120, BUTTON_WIDTH, BUTTON_HEIGHT)
sinusoidal_button_rect = pygame.Rect(WIDTH // 6 - BUTTON_WIDTH // 2, 180, BUTTON_WIDTH, BUTTON_HEIGHT)
reset_button_rect = pygame.Rect(WIDTH // 6 - BUTTON_WIDTH // 2, 240, BUTTON_WIDTH, BUTTON_HEIGHT)

# Game clock
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if straight_button_rect.collidepoint(event.pos):
                ball_speed_x = 8
                ball_thrown_straight = True
                ball_thrown_curve = False
                ball_thrown_sinusoidal = False
            if curve_button_rect.collidepoint(event.pos):
                ball_speed_x = 6
                ball_speed_y = -4
                ball_thrown_straight = False
                ball_thrown_curve = True
                ball_thrown_sinusoidal = False
            if sinusoidal_button_rect.collidepoint(event.pos):
                ball_speed_x = 6
                ball_thrown_straight = False
                ball_thrown_curve = False
                ball_thrown_sinusoidal = True
                sinusoidal_angle = 0
            if reset_button_rect.collidepoint(event.pos):
                # Reset ball position and speed
                ball_x, ball_y = 177, GROUND_Y - BALL_RADIUS * 2
                ball_speed_x = 0
                ball_thrown_straight = False
                ball_thrown_curve = False
                ball_thrown_sinusoidal = False
                sinusoidal_angle = 0

    # Update ball position if thrown straight
    if ball_thrown_straight:
        ball_x += ball_speed_x
        if ball_x + BALL_RADIUS >= WALL_X:
            ball_x = WALL_X - BALL_RADIUS
            ball_speed_x = 0

    # Update ball position for curve throw
    if ball_thrown_curve:
        ball_x += ball_speed_x
        ball_y +=  ball_speed_y
        ball_speed_y += 0.07
        if ball_x + BALL_RADIUS >= WALL_X:
            ball_x = WALL_X - BALL_RADIUS
            ball_speed_x = 0
            ball_speed_y = 0
    
    # Update ball position for sinusoidald throw
    if ball_thrown_sinusoidal:
        ball_x += ball_speed_x
        sinusoidal_angle += 0.1
        ball_y = (GROUND_Y - BALL_RADIUS * 2) - 50 * math.sin(sinusoidal_angle)
        if ball_x + BALL_RADIUS >= WALL_X:
            ball_x = WALL_X - BALL_RADIUS
            ball_speed_x = 0
            sinusoidal_angle = 0

    # Draw the ground
    pygame.draw.rect(screen, GREEN, (0, GROUND_Y, WIDTH, GROUND_HEIGHT))

    # Draw the wall
    pygame.draw.rect(screen, GRAY, (WALL_X, 0, 50, HEIGHT))

    # Draw the ball with stripes
    pygame.draw.circle(screen, BLUE, (int(ball_x), int(ball_y)), BALL_RADIUS)
    for i in range(-BALL_RADIUS, BALL_RADIUS, 4):
        pygame.draw.line(screen, STRIPE_COLOR, 
                         (ball_x - i, ball_y - math.sqrt(BALL_RADIUS**2 - i**2)),
                         (ball_x - i, ball_y + math.sqrt(BALL_RADIUS**2 - i**2)))

    # Draw the cannon image
    screen.blit(cannon_image, (cannon_x, cannon_y))

    # Draw the buttons
    font = pygame.font.SysFont(None, 24)

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
