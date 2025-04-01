from pygame import *
import random
import time as tm

# Initialize pygame
init()
size = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
window = display.set_mode(size)
display.set_caption("Ball")

FPS = 60
FramePerSec = time.Clock()
Score = 0
Coin_score = 0

# Fonts
ffont = font.SysFont("Verdana", 60)
font_small = font.SysFont("Verdana", 20)    
game_over = ffont.render("LOSER", True, (0, 0, 0))

# Speeds
espeed = 5
pspeed = 7
add_speed = True

class Enemy(sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = transform.scale(transform.rotate(image.load("black_car.png"), 180), (80, 170))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0) 

    def move(self):
        global Score, espeed, pspeed, add_speed
        self.rect.move_ip(0, espeed)
        if self.rect.bottom > SCREEN_HEIGHT + 170:
            Score += 1
            if add_speed:
                espeed += 0.5
                pspeed += 0.5
            if espeed == 12:
                add_speed = False
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = transform.scale(image.load("white_car.png"), (80, 170))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = key.get_pressed()
        if self.rect.left > 0 and (pressed_keys[K_a] or pressed_keys[K_LEFT]):
            self.rect.move_ip(-pspeed, 0)
        if self.rect.right < SCREEN_WIDTH and (pressed_keys[K_d] or pressed_keys[K_RIGHT]):
            self.rect.move_ip(pspeed, 0)

class Coin(sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.size = random.randint(40, 90)
        self.speed = random.randint(4, 9)
        self.image = transform.scale(image.load("coin.png"), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -1000) 

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT + 50:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -1000)

# Initialize game objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Create sprite groups
enemies = sprite.Group(E1)
coins = sprite.Group(C1)
all_sprites = sprite.Group(P1, E1, C1)

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    
    window.fill((0, 0, 0))
    
    # Draw and update all sprites
    for entity in all_sprites:
        window.blit(entity.image, entity.rect)
        entity.move()
    
    # Check collision with enemy
    if sprite.spritecollideany(P1, enemies):
        window.fill((255, 0, 0))
        window.blit(game_over, (305, 250))
        display.update()
        tm.sleep(2)
        running = False
    
    # Check collision with coin
    if sprite.spritecollideany(P1, coins):
        Coin_score += 1
        C1.kill()
        C1 = Coin()
        all_sprites.add(C1)
        coins.add(C1)
    
    # Display scores
    window.blit(font_small.render(f"Cars: {Score}", True, (255, 255, 255)), (10, 10))
    window.blit(font_small.render(f"Coins: {Coin_score}", True, (255, 255, 255)), (10, 30))
    
    display.flip()
    FramePerSec.tick(FPS)
    
quit()