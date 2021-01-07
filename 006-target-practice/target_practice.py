import pygame
from pygame import Rect
import random
import speedrun_stopwatch as ss


# Global Variables
SCREEN_DIMENSIONS = (1200, 600)
CENTER_OF_SCREEN = (SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2)
MAX_TARGET_SIZE = 50


# Used classes
class TargetPractice(object):
    """
    Main Application class that stores the game attributes.

    Attributes:
    game_window: pygame.Surface - main application window
    clock: pygame.time.Clock() - pygame time control object
    speedrun_timer: ss.SpeedrunTimer() - a module to control speedrun timers
    targets: List[Target] - currently active targets
    stage: int - current game stage - controls flow of the game
    stage_shots: int - number of shoots  taken this stage
    current_size: int - targets gets smaller as game progresses
    run: bool - while true, the game runs
    timer: int - represents time elapsed since start of game in ms
    main_font: pygame.font.SysFont - font used for the main timer
    timer_font: pygame.font.SysFont - font used for the speedrun timers
    timer_area: int - delimiter for the timers and game area (x coord)

    Methods:
    spawn_target() - adds a Target object placed on game area to self.targets
    shoot() - shoots a bullet at cursor position, if hits a target executes
              commands on hit (check the function)
    draw_speedrun_timer(x, y): draws the speedrun timers at x, y (top left)
    draw_crosshair() - draws the crosshair at the cursor position
    clear_screen() - clears screen
    draw_timer(x, y) - draws the main game timer
    draw_divider() - draws a line dividing the timers from the game area
    draw_all_game_elements() - draws all game_window elements
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Target Practice")
        self.game_window = pygame.display.set_mode(SCREEN_DIMENSIONS)
        self.clock = pygame.time.Clock()
        # Game objects
        self.uis = UISelectors(200, 40, 20)
        self.speedrun_timer = ss.SpeedrunTimer(
            10, "past_runs.txt", ["Size " + str(50-5*i) for i in range(10)]
        )
        self.targets = []
        # Game control variables
        self.stage = 0  # start at 0
        self.stage_shots = 0
        self.current_size = MAX_TARGET_SIZE
        # Logic flow control variables
        self.run = True
        self.menu = True
        self.game = False
        self.results_screen = False
        # Other variables
        self.timer = 0
        self.main_font = pygame.font.SysFont("Arial", 30, True, True)
        self.timer_font = pygame.font.SysFont("Arial", 12, True, True)
        self.timer_area = 200

    def spawn_target(self):
        """
        Spawns a Target object in the game area of the game_window.
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
        """
        "Shoots" at the position of the cursor.

        If a target is hit, it is replaced by a new target according to every
        changing stage parameters - successive hits make the targets smaller,
        and the game is divided into stages of 3 shots.

        After each stage is finished, the self.speedrun_timer is called to
        start/end it's stage timers. When the last stage is finished, the game
        ends.
        """
        mouse_position = pygame.mouse.get_pos()
        for target in self.targets:
            # You shot the target
            if target.hitbox.collidepoint(mouse_position):
                self.targets.remove(target)
                self.stage_shots += 1

                if self.stage_shots < 3:  # Stage did not end
                    self.spawn_target()
                else:  # Stage did end
                    self.speedrun_timer.end_stage_timer(self.stage, self.timer)
                    self.stage += 1
                    self.stage_shots = 0
                    if self.stage < 10:  # Game did not end
                        self.speedrun_timer.start_stage_timer(
                            self.stage, self.timer
                            )
                        self.current_size -= 5
                        self.spawn_target()
                    else:  # Game did end
                        self.speedrun_timer.end_run()
                        self.game = False
                        self.results_screen = True

    def draw_speedrun_timer(self, x: int, y: int):
        """
        Draws the speedrun timers in the game_window at (x, y)
        """
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
        """
        Draws a divider between timers and game area.
        """
        pygame.draw.rect(
            self.game_window,
            (255, 255, 0),
            (self.timer_area, 0, 2, SCREEN_DIMENSIONS[1])
        )

    def draw_main_menu(self):
        if self.run and self.menu:
            self.uis.draw_main_menu(self.game_window)

    def menu_select(self):
        mouse_position = pygame.mouse.get_pos()
        if self.uis.play_button.rectangle.collidepoint(mouse_position):
            self.menu = False
            self.game = True
            self.timer = 0
            self.targets.clear()
            self.spawn_target()
            self.speedrun_timer.start_run()

        if self.uis.high_scores.rectangle.collidepoint(mouse_position):
            self.menu = False
            self.results_screen = True

        if self.uis.quit_button.rectangle.collidepoint(mouse_position):
            self.menu = False
            self.run = False

    def draw_back_button(self):
        self.uis.draw_back_button(self.game_window)

    def scores_select(self):
        mouse_position = pygame.mouse.get_pos()
        if self.uis.back_button.rectangle.collidepoint(mouse_position):
            self.menu = True
            self.results_screen = False

    def draw_all_game_elements(self):
        """
        Clears the screen and draws the elements in the 'game_window'.
        """
        if self.run and self.game:
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


class Button(object):
    def __init__(self, rectangle: Rect, text: str):
        self.rectangle = rectangle
        self.font = pygame.font.SysFont("Arial", 15, True, True)
        self.text = self.font.render(text, 1, (255, 255, 0))

    def draw_with_offset(self, window: pygame.Surface, offset: int):
        """
        Draws the button on the Surface window, with the text as offset from
        the center of button (move text left)

        offset negative - move text to the left
        offset positive - move text to the right
        """
        pygame.draw.rect(window, (255, 0, 0), self.rectangle)
        window.blit(self.text, (
            self.rectangle.x + self.rectangle.width//2 + offset,
            self.rectangle.y + self.rectangle.height//4
            ))


class UISelectors(object):
    def __init__(
        self, button_width: int, button_height: int, button_spacing: int
    ):
        # Class attributes
        self.button_width = button_width  # 200
        self.button_height = button_height  # 40
        self.button_spacing = button_spacing  # 20
        # Main Menu PLAY button
        self.play_button = Button(self.button_above_screen_center(-2), "PLAY")
        # Main Menu HIGH SCORES button
        self.high_scores = Button(
            self.button_above_screen_center(-1), "HIGH SCORES"
        )
        # Main Menu QUIT button
        self.quit_button = Button(self.button_above_screen_center(0), "QUIT")
        # High Scores MAIN MENU button
        self.back_button = Button(
            self.button_above_screen_center(3), "MAIN MENU"
        )
        # instructions = ?
        # title = ?

    def button_above_screen_center(self, elevation: int = 0) -> Rect:
        """
        Creates a button centered on the screen in relation to the screen
        center. A unit of elevation is equal to button height plus spacing

        elevation negative - above screen center
        elevation positive - below screen center
        """
        return Rect(
            CENTER_OF_SCREEN[0] - self.button_width//2,
            CENTER_OF_SCREEN[1] + elevation * (
                self.button_spacing + self.button_height
            ),
            self.button_width,
            self.button_height
        )

    def draw_main_menu(self, window: pygame.Surface):
        self.play_button.draw_with_offset(window, -20)
        self.high_scores.draw_with_offset(window, -52)
        self.quit_button.draw_with_offset(window, -20)

    def draw_back_button(self, window: pygame.Surface):
        self.back_button.draw_with_offset(window, -46)


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

    # run is True
    while app.run:

        app.clock.tick(60)

        # Global Effects
        keys = pygame.key.get_pressed()

        # Q - Quit
        if keys[pygame.K_q]:
            app.run = False
        # H - High Scores
        if keys[pygame.K_h]:
            app.menu = False
            app.game = False
            app.results_screen = True
        # M - Menu
        if keys[pygame.K_m]:
            app.menu = True
            app.game = False
            app.results_screen = False

        # menu is True
        if app.menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    app.run = False
                # LMB - Select
                if (
                    event.type == pygame.MOUSEBUTTONDOWN and
                    pygame.mouse.get_pressed(3)[0]
                ):
                    app.menu_select()

            app.clear_screen()
            app.draw_main_menu()
            app.draw_crosshair()
            pygame.display.update()

        # results_screen is True
        if app.results_screen:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    app.run = False
                # LMB - Select
                if (
                    event.type == pygame.MOUSEBUTTONDOWN and
                    pygame.mouse.get_pressed(3)[0]
                ):
                    app.scores_select()

            app.clear_screen()
            app.speedrun_timer.draw_timers(
                app.game_window, 500, 150, app.timer, "long", app.timer_font
            )
            app.draw_timer(70, SCREEN_DIMENSIONS[1] - 50)
            app.draw_back_button()
            app.draw_crosshair()
            pygame.display.update()

        # game is True
        if app.game:

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

            # Draw the Game Window and Update
            app.draw_all_game_elements()
            pygame.display.update()

    # run is False
    pygame.quit()


if __name__ == "__main__":
    main()
