import random
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
ball_speed_y = 2
sin_mode = False
sinusoidal_angle = 0

# Racket settings
RACKET_WIDTH, RACKET_HEIGHT = 10, 80
racket_x = 20
racket_y = HEIGHT // 2 - RACKET_HEIGHT // 2
score = 0
max_score = 0
game_over = False

# Slider settings
SLIDER_WIDTH, SLIDER_HEIGHT = 200, 5
SLIDER_X, SLIDER_Y = WIDTH // 2 - SLIDER_WIDTH // 2, 120
THUMB_WIDTH, THUMB_HEIGHT = 10, 20
thumb_x = SLIDER_X + 38  # Initial position of the thumb
thumb_rect = pygame.Rect(thumb_x, SLIDER_Y - (THUMB_HEIGHT // 2), THUMB_WIDTH, THUMB_HEIGHT)
dragging_thumb = False
min_speed = 5
max_speed = 20.8
slider_speed = min_speed + (thumb_x - SLIDER_X) / SLIDER_WIDTH * (max_speed - min_speed)

# Game clock
clock = pygame.time.Clock()

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
            if thumb_rect.collidepoint(event.pos):
                dragging_thumb = True

        if event.type == pygame.MOUSEBUTTONUP:
            dragging_thumb = False

        if event.type == pygame.MOUSEMOTION and dragging_thumb:
            thumb_x = max(SLIDER_X, min(SLIDER_X + SLIDER_WIDTH - THUMB_WIDTH, event.pos[0]))
            slider_speed = min_speed + (thumb_x - SLIDER_X) / SLIDER_WIDTH * (max_speed - min_speed)
            if ball_speed_x > 0:
                ball_speed_x = slider_speed
            else:
                ball_speed_x = -slider_speed
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                sin_mode = not sin_mode

    if not game_over:
        # Move racket with mouse
        mouse_y = pygame.mouse.get_pos()[1]
        racket_y = max(0, min(HEIGHT - RACKET_HEIGHT, mouse_y - RACKET_HEIGHT // 2))

        # Update ball position
        ball_x += ball_speed_x
        if sin_mode:
            sinusoidal_angle += 0.1
            ball_y = ball_y - 5 * math.sin(sinusoidal_angle)
        
        ball_y += ball_speed_y
        ball_rotation_angle = (ball_rotation_angle + rotation_speed) % 360


        # Ball-wall collisions
        if ball_y <= BALL_RADIUS or ball_y >= HEIGHT - BALL_RADIUS:
            ball_speed_y *= -1

        # Ball collision with big wall
        if ball_x >= WIDTH - 50 - BALL_RADIUS:
            ball_speed_x *= -1
            rotation_speed *= -1

        # Ball collision with racket
        if (
            ball_x <= RACKET_WIDTH + BALL_RADIUS * 3
            and racket_y < ball_y < racket_y + RACKET_HEIGHT
        ):
            score += 1
            
            ball_speed_x *= -1
            rotation_speed *= -1
            hit_pos = (ball_y - (racket_y + RACKET_HEIGHT // 2)) / (RACKET_HEIGHT // 2)

            # Adjust ball speed and Y direction based on hit position
            ball_speed_y += hit_pos * 3  # Increase speed variation
            ball_speed_y = max(min(ball_speed_y, 10), -10)  # Cap speed to avoid runaway
            
        if ball_y > GROUND_Y:
            ball_speed_y = -ball_speed_y
            sin_mode = False
        
        if ball_x < 0:
            game_over = True

        # Draw the ground
        pygame.draw.rect(screen, GREEN, (0, GROUND_Y, WIDTH, GROUND_HEIGHT))
        # Draw the wall
        pygame.draw.rect(screen, GRAY, (WALL_X, 0, 50, HEIGHT))
        # Draw the ball image
        animate_ball(screen, ball_x, ball_y, BALL_RADIUS, ball_rotation_angle)
        # Draw the racket
        pygame.draw.rect(screen, GRAY, (racket_x, racket_y, RACKET_WIDTH, RACKET_HEIGHT))


        # Score value Label
        font = pygame.font.SysFont(None, 48)
        score_text = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_text, (SLIDER_X + 40, SLIDER_Y - 80))
        font = pygame.font.SysFont(None, 24)
        # Draw the slider
        pygame.draw.rect(screen, GRAY, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))  # Slider bar
        pygame.draw.rect(screen, RED, thumb_rect)  # Slider thumb
        thumb_rect.x = thumb_x
        # Speed value Label
        speed_text = font.render(f"Speed: {slider_speed:.1f}", True, BLUE)
        screen.blit(speed_text, (SLIDER_X + 60, SLIDER_Y - 30))
        # Throw mode Label
        if not sin_mode:
            mode_text = font.render(f"Mode: Straight", True, BLUE)
        else:
            mode_text = font.render(f"Mode: Sinusoidal", True, BLUE)
        screen.blit(mode_text, (SLIDER_X + 60, SLIDER_Y + 30))

    else:
        if max_score < score:
            max_score = score
        
        # Display game over message
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
        game_score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(game_score_text, (WIDTH // 2 - 80, HEIGHT // 2))
        max_score_text = font.render(f"Record: {max_score}", True, RED)
        screen.blit(max_score_text, (WIDTH // 2 - 80, HEIGHT // 2 + 50))
        
        # Restart game on 'R' key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game state
            ball_x, ball_y = WIDTH // 4, HEIGHT // 2
            ball_speed_x, ball_speed_y = 6, random.choice([-5, 5])
            racket_y = HEIGHT // 2 - RACKET_HEIGHT // 2
            score = 0
            game_over = False
    
    
    # Update display
    pygame.display.flip()
    clock.tick(60)
