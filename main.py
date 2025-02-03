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
wall_y = HEIGHT // 2

# Ball settings
ball_rotation_angle = 0
rotation_speed = 5

BALL_RADIUS = 10
ball_x, ball_y = 140, GROUND_Y - 54
ball_speed_x = 6
ball_speed_y = 2

# Racket settings
RACKET_WIDTH, RACKET_HEIGHT = 10, 80
racket_x = 20
racket_y = HEIGHT // 2 - RACKET_HEIGHT // 2
prev_mouse_pos = pygame.mouse.get_pos()
score = 0
pc_score = 0
loser_score = 0
winner = "PC"
game_over = False

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

    if not game_over:
        # Move racket with mouse
        mouse_y = pygame.mouse.get_pos()[1]
        racket_y = max(0, min(HEIGHT - RACKET_HEIGHT, mouse_y - RACKET_HEIGHT // 2))

        # Wall moves with the ball
        PC_WALL_SPEED = 5
        # Smooth movement toward the ball's position
        if ball_y > wall_y + RACKET_HEIGHT // 2:
            wall_y = min(wall_y + PC_WALL_SPEED, HEIGHT - RACKET_HEIGHT)
        elif ball_y < wall_y + RACKET_HEIGHT // 2:
            wall_y = max(wall_y - PC_WALL_SPEED, 0)

        # Update ball position
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        ball_rotation_angle = (ball_rotation_angle + rotation_speed) % 360

        # Ball-wall collisions
        if ball_y <= BALL_RADIUS or ball_y >= HEIGHT - BALL_RADIUS:
            ball_speed_y *= -1

        # Ball collision with big wall
        if (ball_x >= WIDTH - 50 - BALL_RADIUS and wall_y < ball_y < wall_y + RACKET_HEIGHT):
            ball_speed_x *= -1
            rotation_speed *= -1

            # Adjust ball speed and Y direction based on hit position
            ball_speed_y = int(random.random() * 30) - 15  # Cap speed to avoid runaway
            ball_speed_x = int(random.random() * -12) - 3
            
        # Ball collision with racket
        if (ball_x <= RACKET_WIDTH + BALL_RADIUS * 3 and racket_y < ball_y < racket_y + RACKET_HEIGHT):
            ball_speed_x *= -1
            rotation_speed *= -1
            hit_pos = (ball_y - (racket_y + RACKET_HEIGHT // 2)) / (RACKET_HEIGHT // 2)

            # Compute mouse speed using the Euclidean distance formula   
            current_mouse_pos = pygame.mouse.get_pos()
            dx = current_mouse_pos[0] - prev_mouse_pos[0]
            dy = current_mouse_pos[1] - prev_mouse_pos[1]
            mouse_speed = math.sqrt(dx**2 + dy**2)
            prev_mouse_pos = current_mouse_pos

            # Adjust ball speed and Y direction based on hit position
            ball_speed_y += hit_pos * 3  # Increase speed variation
            ball_speed_y = max(min(ball_speed_y, 10), -10)  # Cap speed to avoid runaway
            ball_speed_x = max(5 + mouse_speed//50, ball_speed_x)

        if ball_y > GROUND_Y:
            ball_speed_y = -ball_speed_y
        
        if ball_x < 0:
            pc_score += 1
            if pc_score == 10:
                winner = "PC"
                loser_score = score
                game_over = True
            ball_x, ball_y = WIDTH // 4, HEIGHT // 2
            ball_speed_x, ball_speed_y = 6, random.choice([-5, 5]) 

        if ball_x > WIDTH:
            score += 1
            if score == 10:
                winner = "You"
                loser_score = pc_score
                game_over = True
            ball_x, ball_y = WIDTH // 4, HEIGHT // 2
            ball_speed_x, ball_speed_y = 6, random.choice([-5, 5])
            
            
        # Draw the ground
        pygame.draw.rect(screen, GREEN, (0, GROUND_Y, WIDTH, GROUND_HEIGHT))
        # Draw the wall
        pygame.draw.rect(screen, GRAY, (WALL_X, wall_y, RACKET_WIDTH, RACKET_HEIGHT))
        # Draw the ball image
        animate_ball(screen, ball_x, ball_y, BALL_RADIUS, ball_rotation_angle)
        # Draw the racket
        pygame.draw.rect(screen, GRAY, (racket_x, racket_y, RACKET_WIDTH, RACKET_HEIGHT))


        # Score value Label
        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Your Score: {score}", True, GREEN)
        screen.blit(score_text, (WIDTH // 2 - 120, 40))
        pc_score_text = font.render(f"Pc Score: {pc_score}", True, GREEN)
        screen.blit(pc_score_text, (WIDTH // 2 + 20, 40))

    else:
        
        # Display game over message
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
        game_score_text = font.render(f"{winner} won 10 - {loser_score}", True, RED)
        screen.blit(game_score_text, (WIDTH // 2 - 80, HEIGHT // 2))
        
        # Restart game on 'R' key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game state
            ball_x, ball_y = WIDTH // 4, HEIGHT // 2
            ball_speed_x, ball_speed_y = 6, random.choice([-5, 5])
            racket_y = HEIGHT // 2 - RACKET_HEIGHT // 2
            score = 0
            pc_score = 0
            game_over = False
    
    
    # Update display
    pygame.display.flip()
    clock.tick(60)
