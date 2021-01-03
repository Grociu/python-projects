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

"""
import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# This is an entry from the database of entries, each represented by a list of
# the same length
# Each number represents a time in ms, that a stage has started/ended at
# each pair of numbers represents a 'stage' time
sample_record = [0, 2345, 5403, 10435, 23040, 53403, 213133, 215000, 600000]
another_record = [0, 2340, 6534, 9543, 22000, 45232, 200030, 202090, 590232]
third_record = [0, 2140, 7544, 8243, 19000, 51232, 198020, 212000, 597232]


class Stage(object):
    """
    Represents a single stage of the game progression

    Attributes:
    rank (int) - position of the Stage in SpeedrunTimer
    active (bool) - Is this a currently active stage
    start_time (int) - time in ms when the Stage began
    end_time (int) - time in ms when the Stage ended
    interval (int) - time it took to complete the stage
    pb (int) - personal best taken from the database
    delta (int) - the difference between current time and pb
    beats_pb (bool) - does this try beat the personal best

    Methods:
    start_stage(time) - starts the Stage at time
    end_stage(time) - ends the stage at time
    """
    def __init__(self, rank: int):
        self.rank = rank
        self.active = False
        self.start_time = 0
        self.end_time = 0
        self.interval = 0
        self.pb = 0
        self.delta = 0
        self.beats_pb = False

    def start_stage(self, time: int):
        """ Starts the current stage and updates attributes """
        self.active = True
        self.start_time = time

    def end_stage(self, time: int):
        """ Ends the current stage and updates attributes """
        self.active = True
        self.end_time = time
        self.interval = self.end_time - self.start_time
        if self.pb:
            self.delta = self.interval - self.pb
            if self.delta < 0:
                self.beats_pb = True


class SpeedrunTimer(object):
    def __init__(self, number_of_stages: int, database_file: str):
        self.database_file = database_file
        self.past_runs = []
        self.stages = [Stage(index) for index in range(number_of_stages)]
        self.read_database()

    def read_database(self):
        """ Reads past games database and updates the PBs """
        try:
            self.past_runs.clear()
            file = open(f"{CURRENT_DIR}/{self.database_file}", "r")
            for line in file.readlines():
                self.past_runs.append(
                    [int(time) for time in line.split()]
                )
        except OSError:
            print("Read Error, Database not loaded")
            print("Creating empty database file: speedrun.txt")
            open(f"{CURRENT_DIR}/speedrun.txt", "w").close()
            self.database = "speedrun.txt"

    def clear_database(self):
        """ Clears past game database """
        open(f"{CURRENT_DIR}/{self.database_file}", "w").close()
        self.read_database()
