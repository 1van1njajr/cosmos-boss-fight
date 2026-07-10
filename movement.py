import pygame
import math

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circular Motion - Boss Fight")
clock = pygame.time.Clock()

# Player setup
class Player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        
        # Circular motion parameters
        self.center_x = center_x
        self.center_y = center_y
        self.radius = 150
        self.angle = 0
        self.speed = 3  # degrees per frame
        self.clockwise = True  # True for clockwise, False for counter-clockwise
        
        self.update_position()
    
    def update_position(self):
        """Update player position based on circular motion"""
        # Convert angle to radians
        rad = math.radians(self.angle)
        
        # Calculate position on circle
        if self.clockwise:
            x = self.center_x + self.radius * math.cos(rad)
            y = self.center_y + self.radius * math.sin(rad)
        else:
            x = self.center_x + self.radius * math.cos(-rad)
            y = self.center_y + self.radius * math.sin(-rad)
        
        self.rect.center = (int(x), int(y))
    
    def change_direction(self):
        """Change rotation direction when space is pressed"""
        self.clockwise = not self.clockwise
    
    def update(self):
        """Update player movement"""
        self.angle += self.speed
        if self.angle >= 360:
            self.angle = 0
        self.update_position()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Main game loop
player = Player(WIDTH // 2, HEIGHT // 2)

running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.change_direction()
    
    # Update
    player.update()
    
    # Draw
    screen.fill((20, 20, 40))
    
    # Draw center point
    pygame.draw.circle(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), 5)
    
    # Draw circular path
    pygame.draw.circle(screen, (100, 100, 100), (WIDTH // 2, HEIGHT // 2), player.radius, 1)
    
    # Draw player
    player.draw(screen)
    
    pygame.display.flip()

pygame.quit()
