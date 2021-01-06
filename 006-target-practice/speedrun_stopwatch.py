"""
This module represents a speedrunning tracker for pygame modules

It maintains a .db file with past entries, that is read at startup

An active timer tracking will look something like this

Milestone    Total.t      PB        Delta      (Hidden Attributes)

 Stage 1   Total.Time  Total.PB Total.Delta Stage.Time Stage.PB Stage.Delta
 Stage 2   Total.Time  Total.PB Total.Delta Stage.Time Stage.PB Stage.Delta
 Stage 3   Total.Time  Total.PB Total.Delta Stage.Time Stage.PB Stage.Delta
 Stage 4   Active.Time Total.PB     Blank   Active.Stage.Time Stage.PB Blank
 .....
 Stage -1     Blank    Total.PB     Blank

  Total:   Final.Time  Final.PB  Best Possible (sum of PB)

What you need:
1. You need to have a running timer (in ms) that measures time since start of
the game. Example code how to achieve this:

import pygame

pygame.init()
clock = pygame.time.Clock()
timer = 0

run = True
while run:
    clock.tick(60)
    timer += clock.get_rawtime()
    #Insert your game code here

Use the timer variable (or your equivalent) anytime you're asked to input time.

2. You need to divide your game into intervals - stages that you want to
measure splits for.
You will need to know where each stage starts and ends in the code.
You will also need to know how many total stages there are. While there is no
upper limit of stages, if you want to draw them on the screen, best results are
with 3-10 stages.

Example: In a game of Mario, each stage is well defined, starts when the level
loads, ends when you reach the flag / axe. 8 worlds, 4 levels each, you have 32
stages.

Example: Let's say you have a game of Sudoku with a constant given numbers.
You can define each 'stage' as player inputing 5 correct numbers onto the
puzzle. Depending on the number of the given numbers you'll need to calculate
the number of stages.

3. You'll need a txt file in the game directory to store the database of past
runs. The program will create it's own file named 'speedrun.txt' if none is
provided, but it's better to have your own file with a custom name.

Usage:
1. Import the module into your game

import speedrun_stopwatch as ss

2. Initialize the SpeedrunTimer object. It takes two mandatory arguments -
number of stages and the name of the 'txt' database file. It also takes an
optional argument - a list of strings representing names of stages: as default
it will be Stage 1, Stage 2, but if you want a custom set - it's possible.
Best results with short stage names.

speedrun_timer = ss.SpeedrunTimer(10, 'results.txt')

or using the optional argument:

speedrun_timer = ss.SpeedrunTimer(
    4, 'runs.txt', ['world 1-1, 'world 1-2', 'world 1-3', 'world 1-4']
)

3. If you want to start a run, in your code at start of game insert:

speedrun_timer.start_run()  # starts the timer for first stage at 0 ms

or if you want to start at a custom time:

speedrun_timer.start_stage_timer(0, time) # STAGE INDEX STARTS AT 0

4. Now that the first timer is set, if you want to end a stage and start a new
one insert these statements where stages start/end. 'time' represents an
integer - time in ms since start

speedrun_timer.end_stage_timer(index, time)  # STAGE INDEX STARTS AT 0
speedrun_timer.start_stage_timer(index, time)  # STAGE INDEX STARTS AT 0

5. If your current run is done, end the last stage like before
HINT: Pythonic -1 will not work as an index here, STAGE INDEX STARTS AT 0

speedrun_timer.end_stage_timer(last_index, time)

and then to sumbit the results to the local database and file add this line,
and RESET the timers to 0:

speedrun_timer.end_run()

6. If you wish to draw the active timers on the screen while the game is
running or after all stages are done (but before .end_run() is called!) call
the following function:

speedrun_timer.draw_timers(
        window: pygame.Surface,  # game window to draw the timers on
        x: int,  # x coordinate of the top left corner of the timers
        y: int,  # y coordinate of the top left corner of the timers
        timer: int,  # the running timer described at the start of docs
        mode: str = "short",  # 'short' for 3 main timers, "long" for 6 timers
        font: pygame.font = None,  # font to draw the timers in
        color: Tuple[int, int, int] = (255, 255, 0)  # yellow
    )

By default the mode will be "short", font will be Arial 12 Bold Italic and the
color will be yellow. As long as you pass the first three arguments you will be
fine.

Other:
1. Past Results files and run representation.

This is an entry from the database of entries, each represented by a list of
the same length.
Each number represents a time in ms, that a stage has started/ended at
each pair of numbers represents a 'stage' time

sample_record = [0, 2345, 5403, 10435, 23040, 53403, 213133, 215000, 600000]
another_record = [0, 2340, 6534, 9543, 22000, 45232, 200030, 202090, 590232]
third_record = [0, 2140, 7544, 8243, 19000, 51232, 198020, 212000, 597232]

"""
import os
import pygame
from typing import Tuple


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class PastRun(object):
    """
    A past run of the game, separated into intervals with a total time.

    Attributes:
    data: list[int] - raw data, times in ms that delimit each stage
    intervals: list[int] - time it took to complete each stage
    total - int - total time for the run
    """
    def __init__(self, data: list[int]):
        self.data = data
        self.intervals = [
            data[index+1] - data[index] for index in range(len(data)-1)
        ]
        self.total = data[-1]


class Stage(object):
    """
    Represents a single stage of the game progression.

    Attributes:
    rank (int) - position of the Stage in SpeedrunTimer
    active (-1, 0, 1) - 0 not active, 1 active, -1 finished
    start_time (int) - time in ms when the Stage began
    end_time (int) - time in ms when the Stage ended
    interval (int) - time it took to complete the stage
    stage_pb (int) - personal best taken from the database
    delta (int) - the difference between current time and pb

    Methods:
    start_stage(time) - starts the Stage at time
    end_stage(time) - ends the stage at time
    """
    def __init__(self, rank: int):
        self.rank = rank
        self.active = 0
        self.start_time = 0
        self.end_time = 0
        self.interval = 0
        self.stage_pb = 0
        self.delta = 0
        self.name = f"Stage {rank+1}"

    def start_stage(self, time: int):
        """ Starts the current stage and updates attributes """
        self.active = 1
        self.start_time = time

    def end_stage(self, time: int):
        """ Ends the current stage and updates attributes """
        self.active = -1
        self.end_time = time
        self.interval = self.end_time - self.start_time
        if self.stage_pb:
            self.delta = self.interval - self.stage_pb

    def set_name(self, name: str):
        self.name = name


class SpeedrunTimer(object):
    def __init__(
        self, number_of_stages: int, database_file: str,
        names: list[str] = None
    ):
        self.database_file = database_file
        self.past_runs = []
        self.pb_run = []
        self.stages = [Stage(index) for index in range(number_of_stages)]
        if names is None:
            self.names = [stage.name for stage in self.stages]
        else:
            self.names = names
        self.define_stage_names(self.names)
        self.read_database()

    def read_database(self):
        """
        Reads past games database and updates the PBs.
        """
        try:
            file = open(f"{CURRENT_DIR}/{self.database_file}", "r")
            self.past_runs.clear()
            data = []

            for line in file.readlines():
                if line.strip():
                    data.append([int(time) for time in line.split()])
            file.close()

            if data:
                for entry in data:
                    self.past_runs.append(PastRun(entry))
                self.update_pb()
                self.update_stage_pbs()
        except OSError:
            print("Read Error, Database not loaded")
            print("Creating empty database file: speedrun.txt")
            open(f"{CURRENT_DIR}/speedrun.txt", "w").close()
            self.database_file = "speedrun.txt"

    def clear_database(self):
        """
        Clears the entire past game database.
        """
        open(f"{CURRENT_DIR}/{self.database_file}", "w").close()
        self.read_database()

    def add_to_database(self, run_data: list[int]):
        """
        Adds a run to the database file (adds it at the end)
        """
        file = open(f"{CURRENT_DIR}/{self.database_file}", "a")
        file.write('\n')
        file.write(" ".join(str(item) for item in run_data))
        file.close()

    def update_pb(self):
        """
        Updates the Personal Best run from the list of past runs
        """
        self.pb_run = min(
            self.past_runs, key=lambda run: run.total
            )

    def update_stage_pbs(self):
        """
        Updates Personal Best for each individual stage from the list of past
        runs.
        """
        for stage in self.stages:
            stage.stage_pb = min(
                run.intervals[stage.rank] for run in self.past_runs
            )

    def complete_a_run(self, run_data: list[int] = None):
        """
        Completes the currently active run.
        Adds the current run data to the database, updates the Personal Bests
        for the best run and each stage.
        """
        if run_data is None:
            run_data = [0] + [stage.end_time for stage in self.stages]
        self.add_to_database(run_data)
        self.past_runs.append(PastRun(run_data))
        self.update_pb()
        self.stages = [Stage(index) for index in range(len(self.stages))]
        self.define_stage_names(self.names)
        self.update_stage_pbs()

    def tester(self):
        """
        Manual test function.
        """
        print("###")
        print("Testing pbs")
        if self.pb_run:
            print("Personal Best run:")
            print(f"Stage End times: {self.pb_run.data}")
            print(f"Intervals: {self.pb_run.intervals}")
        for stage in self.stages:
            print(f"Stage {stage.rank} PB: {stage.stage_pb}")

    def start_stage_timer(self, stage, time):
        """
        Sets the 'stage' start time to 'time'
        """
        self.stages[stage].start_stage(time)

    def end_stage_timer(self, stage, time):
        """
        Sets the 'stage' end time to 'time'
        """
        self.stages[stage].end_stage(time)

    def start_run(self):
        """
        Starts a the run.
        """
        self.start_stage_timer(0, 0)

    def end_run(self):
        """
        Ends the currently active run.
        """
        self.complete_a_run()

    def define_stage_names(self, names: list[str]):
        """
        Renames the stages to names in a list of strings
        """
        if len(self.stages) == len(names):
            for stage, name in zip(self.stages, names):
                stage.set_name(name)

    def draw_timers(
        self, window: pygame.Surface, x: int, y: int, timer: int,
        mode: str = "short",
        font: pygame.font = None,
        color: Tuple[int, int, int] = (255, 255, 0)  # yellow
    ):
        """
        This method draws all the timers on a pygame Surface.txt

        Arguments:
        window: pygame.Surface - the Surface that the timers will be drawn on
        x: int - x coordinate on the Surface (top left corner of the timers)
        y: int - y coordinate on the Surface (top left corner of the timers)
        timer: int - time in ms since start of the entire game
        mode: str - "short" displays 3  basic timers,
                    "long" displays all 6 timers,
        font: pygame.font.SysFont - font used to draw the timers
        color: 3-tuple(int) - RGB trio that most of the timers will be drawn
        """
        if font is None:
            pygame.font.init()
            font = pygame.font.SysFont("Arial", 12, True, True)
        current_x = x
        current_y = y
        no_data = font.render("---.--", 1, color)
        # Draw a set of timers for each stage of the game
        for stage in self.stages:
            # This is not the first run - we have past data
            if self.pb_run:
                # The stage is currently active
                if stage.active == 1:
                    text1 = font.render(
                        f"{timer/100:06.2f}", 1, color  # 000.00 format
                    )
                    text2 = font.render(
                        f"{self.pb_run.data[stage.rank+1]/100:06.2f}", 1, color
                    )
                    text3 = no_data
                    if mode == "long":
                        text4 = font.render(
                            f"{(timer - stage.start_time)/100:06.2f}", 1, color
                        )
                        text5 = font.render(
                            f"{stage.stage_pb/100:06.2f}",  1, color
                        )
                        text6 = no_data
                # This stage has finished
                elif stage.active == -1:
                    text1 = font.render(
                        f"{stage.end_time/100:06.2f}", 1, color
                    )
                    text2 = font.render(
                        f"{self.pb_run.data[stage.rank+1]/100:06.2f}", 1, color
                    )
                    # Delta to the PB, colorcoded green/red
                    end = stage.end_time - self.pb_run.data[stage.rank+1]
                    if end >= 0:
                        text3 = font.render(
                            f"{end/100:+06.2f}", 1, (255, 0, 0)
                        )
                    else:
                        text3 = font.render(
                            f"{end/100:+06.2f}", 1, (0, 255, 0)
                        )
                    if mode == "long":
                        text4 = font.render(
                            f"{stage.interval/100:06.2f}", 1, color
                        )
                        text5 = font.render(
                            f"{stage.stage_pb/100:06.2f}", 1, color
                        )
                        if stage.delta >= 0:
                            text6 = font.render(
                                f"{stage.delta/100:+06.2f}", 1, (255, 0, 0)
                            )
                        else:
                            text6 = font.render(
                                f"{stage.delta/100:+06.2f}", 1, (0, 255, 0)
                            )
                # This stage was not active yet
                else:
                    text1 = no_data
                    text2 = font.render(
                        f"{self.pb_run.data[stage.rank+1]/100:06.2f}", 1, color
                    )
                    text3 = no_data
                    if mode == "long":
                        text4 = text6 = no_data
                        text5 = font.render(
                            f"{stage.stage_pb/100:06.2f}", 1, color
                        )
            # This is for the first run - no past data
            else:
                if stage.active == 1:
                    text1 = font.render(
                        f"{timer/100:06.2f}", 1, color
                    )
                    text2 = text3 = no_data
                    if mode == "long":
                        text4 = font.render(
                            f"{(timer -stage.start_time)/100:06.2f}", 1, color
                        )
                        text5 = text6 = no_data
                elif stage.active == -1:
                    text1 = font.render(
                        f"{stage.end_time/100:06.2f}", 1, color
                    )
                    text2 = text1
                    text3 = no_data
                    if mode == "long":
                        text4 = text5 = font.render(
                            f"{stage.interval/100:06.2f}", 1, color
                        )
                        text6 = no_data
                else:
                    text1 = text2 = text3 = no_data
                    if mode == "long":
                        text4 = text5 = text6 = no_data
            # Draw the texts - the positions are hardcoded atm, this should
            # depend on the size of the font used
            text0 = font.render(f"{stage.name}:", 1, color)
            window.blit(text0, (current_x, current_y))
            current_x += 60
            window.blit(text1, (current_x, current_y))
            current_x += 45
            window.blit(text2, (current_x, current_y))
            current_x += 45
            window.blit(text3, (current_x, current_y))
            if mode == "long":
                current_x += 70
                window.blit(text4, (current_x, current_y))
                current_x += 45
                window.blit(text5, (current_x, current_y))
                current_x += 45
                window.blit(text6, (current_x, current_y))
                current_x -= 160
            current_x -= 150
            current_y += 20
        # Draw the summary of timers
        lines = font.render("-"*40, 1, color)
        window.blit(lines, (current_x, current_y))
        if self.pb_run:
            current_y += 20
            text0 = font.render("PB:", 1, color)
            window.blit(text0, (current_x, current_y))
            text1 = font.render(f"{self.pb_run.data[-1]/100:06.2f}", 1, color)
            window.blit(text1, (current_x+60, current_y))
            text2 = font.render("Possible:", 1, color)
            window.blit(text2, (current_x, current_y+20))
            sum_pb = sum([stage.stage_pb for stage in self.stages])
            text3 = font.render(f"{sum_pb/100:06.2f}", 1, color)
            window.blit(text3, (current_x+60, current_y+20))
