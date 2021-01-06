import pygame
from pygame import Rect
import random
import speedrun_stopwatch as ss


# Global Variables
SCREEN_DIMENSIONS = (1200, 600)
MAX_TARGET_SIZE = 50


# Used classes
class TargetPractice(object):
    """
    Main Application class that stores the game attributes.

    Attributes:
    game_window - pygame.display - main game window.
    clock - pygame.time.Clock() - controls time things
    targets lst[Target] - current targets
    current_size - targets gets smaller as game progresses
    run - bool - while true, the game runs
    timer - int - handles the time since start of game
    font - pygame.font.SysFont - font used in the game

    Methods:
    spawn_target() - adds a Target object to self.targets
    shoot() - shoots at cursor position, returns targets hit
    draw_crosshair() - draws the crosshair at the cursor position
    clear_screen() - clears screen and
    draw_all_elements() - draws all game_window elements
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Target Practice")
        self.game_window = pygame.display.set_mode(SCREEN_DIMENSIONS)
        self.clock = pygame.time.Clock()
        self.speedrun_timer = ss.SpeedrunTimer(10, "past_runs.txt")
        self.targets = []
        self.stage = 0  # start at 0
        self.stage_shots = 0
        self.current_size = MAX_TARGET_SIZE
        self.run = True
        self.timer = 0
        self.main_font = pygame.font.SysFont("Arial", 30, True, True)
        self.timer_font = pygame.font.SysFont("Arial", 12, True, True)
        self.timer_area = 200
        self.spawn_target()
        self.speedrun_timer.define_stage_names(
            ["Size " + str(50-5*i) for i in range(10)]
        )
        self.speedrun_timer.start_run()

    def spawn_target(self):
        """
        Spawns a Target object in the game_window.
        """
        self.targets.append(
            Target(
                random.randint(
                    self.current_size + self.timer_area,
                    SCREEN_DIMENSIONS[0] - self.current_size
                ),
                random.randint(
                    self.current_size,
                    SCREEN_DIMENSIONS[1] - self.current_size
                ),
                self.current_size
            )
        )

    def shoot(self):
        mouse_position = pygame.mouse.get_pos()
        for target in self.targets:
            if target.hitbox.collidepoint(mouse_position):
                print(f"HIT! Target size was {target.size}")
                self.targets.remove(target)
                self.stage_shots += 1

                if self.stage_shots < 3:
                    self.spawn_target()
                else:
                    self.speedrun_timer.end_stage_timer(self.stage, self.timer)
                    self.stage += 1
                    self.stage_shots = 0
                    if self.stage < 10:
                        self.speedrun_timer.start_stage_timer(
                            self.stage, self.timer
                            )
                        self.current_size -= 5
                        self.spawn_target()
                    else:
                        self.speedrun_timer.end_run()
                        print("Victory!")
                        self.run = False

    def draw_speedrun_timer(self, x: int, y: int):
        self.speedrun_timer.draw_timers(
            self.game_window, x, y, self.timer, "short", self.timer_font
        )

    def draw_crosshair(self):
        """
        Draws the crosshair at cursor position on the 'game_window'.
        """
        mouse_position = pygame.mouse.get_pos()
        pygame.draw.rect(
            self.game_window, (0, 255, 0),
            (mouse_position[0]-5, mouse_position[1], 11, 1)
        )
        pygame.draw.rect(
            self.game_window, (0, 255, 0),
            (mouse_position[0], mouse_position[1]-5, 1, 11)
        )

    def clear_screen(self):
        """
        Clears the 'game_window' screen to just a black background.
        """
        self.game_window.fill((0, 0, 0))

    def draw_timer(self, x: int, y: int):
        """
        Draws the current timer at coordinates (x, y)
        """
        text = self.main_font.render(f"{self.timer/100:.2f}", 1, (0, 0, 255))
        self.game_window.blit(text, (x, y))

    def draw_divider(self):
        pygame.draw.rect(
            self.game_window,
            (255, 255, 0),
            (self.timer_area, 0, 2, SCREEN_DIMENSIONS[1])
        )

    def draw_all_elements(self):
        """
        Clears the screen and draws the elements in the 'game_window'
        """
        if self.run:
            # Clear the Background
            self.clear_screen()
            # Draw timer
            self.draw_timer(70, SCREEN_DIMENSIONS[1] - 50)
            # Draw the Targets
            for target in self.targets:
                target.draw(self.game_window)
            # Draw the crosshair
            self.draw_crosshair()
            self.draw_speedrun_timer(10, 10)
            self.draw_divider()


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
        self.hitbox = Rect(x - size, y - size, 2*size, 2*size)

    def draw(self, window: pygame.Surface):
        """
        Draws the target on a Surface window.

        It's represented by a red square, without filling with 2 black squares
        on top of it, so it forms a targetting bracket of 4 corners.
        """
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        cut = self.hitbox[2]//8  # this defines the size of the corners
        pygame.draw.rect(window, (0, 0, 0), (
            self.hitbox[0] + cut,
            self.hitbox[1],
            self.hitbox[2] - 2*cut,
            self.hitbox[3] + 1
            )
        )
        pygame.draw.rect(window, (0, 0, 0), (
            self.hitbox[0],
            self.hitbox[1] + cut,
            self.hitbox[2] + 1,
            self.hitbox[3] - 2*cut
            )
        )


# Main Game Loop
def main():
    app = TargetPractice()
    pygame.mouse.set_visible(False)
    app.timer = 0

    while app.run:
        app.clock.tick(60)  # This controls the frame rate
        app.timer += app.clock.get_rawtime()
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.run = False
            # LMB - Shoot
            if (
                event.type == pygame.MOUSEBUTTONDOWN and
                pygame.mouse.get_pressed(3)[0]
            ):
                app.shoot()

        # Keyboard Shortcuts
        keys = pygame.key.get_pressed()

        # Q - Quit
        if keys[pygame.K_q]:
            app.run = False

        # S - Spawn a target
        if keys[pygame.K_s]:
            app.spawn_target()

        # Draw the Game Window and Update
        app.draw_all_elements()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
