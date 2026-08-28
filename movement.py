import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move on Circle - Press SPACE to reverse direction")
clock = pygame.time.Clock()
FPS = 60

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 200
TRACK_COLOR = (80, 80, 80)
TRACK_WIDTH = 3

PLAYER_RADIUS = 15
PLAYER_COLOR = (255, 80, 80)


angle = 0.0               
angular_speed = 0.03     
direction = 1              

font = pygame.font.SysFont(None, 28)


def get_player_pos(angle_rad):
    """Return (x, y) of the player on the circle for a given angle."""
    x = CENTER[0] + RADIUS * math.cos(angle_rad)
    y = CENTER[1] + RADIUS * math.sin(angle_rad)
    return int(x), int(y)

def draw_scene():
    screen.fill((20, 20, 30))

    pygame.draw.circle(screen, TRACK_COLOR, CENTER, RADIUS, TRACK_WIDTH)

    px, py = get_player_pos(angle)
    pygame.draw.circle(screen, PLAYER_COLOR, (px, py), PLAYER_RADIUS)


    pygame.display.flip()


def main():
    global angle, direction

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    direction *= -1 
                elif event.key == pygame.K_ESCAPE:
                    running = False

        angle += angular_speed * direction
        angle %= (2 * math.pi) 

        draw_scene()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()