import pygame
import random


# Initialize the pygame module
pygame.init()

# Global Variables
SCREEN_DIMENSIONS = (800, 600)
MAX_TARGET_SIZE = 50

# Create the Game Window
game_window = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption("Target Practice")
clock = pygame.time.Clock()


# Used classes
class Target(object):
    """
    Representation of a shooting target.
    A square centered on a point, with a "size" representing the centers
    distance to nearest edge half of the distance to edge.

    Attributes:
    x: int - x coordinates of the center
    y: int - y coordinated of the center
    size: int - size of target, it will be a square with the edge of 2x size
    hitbox: pygame.Rect - Rectangle representing the hitbox of the target

    Methods:
    draw(Surface): draws the target on a Surface
    """
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.hitbox = pygame.Rect(x - size, y - size, 2*size, 2*size)

    def draw(self, window):
        """
        Draws the target on a Surface window.

        It's represented by a red square, without filling
        """
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


# Define Game Objects
targets = []

# Main Game Loop
run = True

while run:
    clock.tick(60)  # This controls the frame rate

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Keyboard Shortcuts
    keys = pygame.key.get_pressed()

    # Q - Quit
    if keys[pygame.K_q]:
        run = False

    # S - Spawn a target
    if keys[pygame.K_s]:
        targets.append(
            Target(
                random.randint(
                    MAX_TARGET_SIZE, SCREEN_DIMENSIONS[0] - MAX_TARGET_SIZE
                ),
                random.randint(
                    MAX_TARGET_SIZE, SCREEN_DIMENSIONS[1] - MAX_TARGET_SIZE
                ),
                MAX_TARGET_SIZE
            )
        )

    # Draw the Target
    for target in targets:
        target.draw(game_window)

    pygame.display.update()

pygame.quit()


if __name__ == "__main__":
    pass
