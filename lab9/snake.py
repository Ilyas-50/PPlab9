import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
WHITE, GREEN, RED, BLUE = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Verdana", 20)
score = 0
level = 1

# Initial snake parameters
snake = [(100, 100)]
SPEED = 10  # Controls FPS, not movement step
direction = (CELL_SIZE, 0)

# Generate food at a random position with a random weight
food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
        random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
food_weight = random.randint(1, 3)  # Weight of food (1 to 3 points)
food_time = time.time()  # Time when food was generated

running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)
    
    # Update snake position
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    
    # Check for collisions (Game Over condition)
    if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
        running = False  # Game over
    else:
        snake.insert(0, new_head)
        
        # Check if snake eats food
        if new_head == food:
            score += food_weight
            food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
            food_weight = random.randint(1, 3)
            food_time = time.time()

            # Level up every 5 points 
            if score % 5 == 0:
                level += 1
                SPEED += 2  
        else:
            snake.pop()
    
    # Check if food has expired (disappears after 5 seconds)
    if time.time() - food_time > 5:
        food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        food_weight = random.randint(1, 3)
        food_time = time.time()
    
    # Draw snake and food
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    food_color = RED if food_weight == 1 else BLUE
    pygame.draw.rect(screen, food_color, (*food, CELL_SIZE, CELL_SIZE))

    # Display score and level
    screen.blit(font_small.render(f"Points: {score}", True, (0,0,0)), (10, 10))
    screen.blit(font_small.render(f"Level: {level}", True, (0,0,0)), (10, 30))
    
    pygame.display.flip()
    clock.tick(SPEED)  # Controls game speed properly

pygame.quit()
