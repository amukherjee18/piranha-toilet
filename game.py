import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Tower Defense")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock to control frame rate
clock = pygame.time.Clock()
FPS = 60

# Load images
tower_image = pygame.image.load("tower.png")
enemy_image = pygame.image.load("enemy.png")
projectile_image = pygame.image.load("projectile.png")

# Scale images
tower_image = pygame.transform.scale(tower_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (40, 40))
projectile_image = pygame.transform.scale(projectile_image, (10, 20))

# Fonts
font = pygame.font.Font(None, 36)

# Tower class
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = tower_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay:
            for enemy in enemies:
                if self.rect.y - 100 < enemy.rect.y < self.rect.y + 100:
                    self.shoot(enemy)
                    self.last_shot = now
                    break

    def shoot(self, target):
        projectile = Projectile(self.rect.centerx, self.rect.centery, target)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health = health
        self.speed = 2

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            global score
            score += 1
            self.kill()

    def draw_health_bar(self, screen):
        if self.health > 0:
            pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100), 5))

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = projectile_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.damage = 20
        self.target = target

    def update(self):
        direction = pygame.math.Vector2(self.target.rect.centerx - self.rect.centerx, 
                                        self.target.rect.centery - self.rect.centery)
        direction = direction.normalize() * self.speed
        self.rect.move_ip(direction)
        if self.rect.colliderect(self.target.rect):
            self.target.health -= self.damage
            if self.target.health <= 0:
                self.target.kill()
            self.kill()

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Create tower
tower = Tower(WIDTH // 2 + 100, HEIGHT // 2)
all_sprites.add(tower)

# Score counter
score = 0

# Main game loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Spawn enemies
    if random.randint(1, 100) <= 2:
        enemy = Enemy(WIDTH // 2, HEIGHT + 40)
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # Update game objects
    all_sprites.update()
    projectiles.update()
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw road
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 25, 0, 50, HEIGHT))
    
    # Draw all sprites
    all_sprites.draw(screen)
    projectiles.draw(screen)
    
    # Draw health bars
    for enemy in enemies:
        enemy.draw_health_bar(screen)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Flip the display
    pygame.display.flip()

pygame.quit()
