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

records = [sample_record, another_record, third_record]


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
    beats_stage_pb (bool) - does this try beat the personal best

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
        self.beats_stage_pb = False

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
            if self.delta < 0:
                self.beats_stage_pb = True


class SpeedrunTimer(object):
    def __init__(self, number_of_stages: int, database_file: str):
        self.database_file = database_file
        self.past_runs = []
        self.pb_run = []
        self.stages = [Stage(index) for index in range(number_of_stages)]
        self.read_database()

    def read_database(self):
        """ Reads past games database and updates the PBs """
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
        """ Clears past game database """
        open(f"{CURRENT_DIR}/{self.database_file}", "w").close()
        self.read_database()

    def add_to_database(self, run_data: list[int]):
        file = open(f"{CURRENT_DIR}/{self.database_file}", "a")
        file.write('\n')
        file.write(" ".join(str(item) for item in run_data))
        file.close()

    def update_pb(self):
        self.pb_run = min(
            self.past_runs, key=lambda run: run.total
            )

    def update_stage_pbs(self):
        for stage in self.stages:
            stage.stage_pb = min(
                run.intervals[stage.rank] for run in self.past_runs
            )

    def complete_a_run(self, run_data: list[int]):
        self.add_to_database(run_data)
        self.past_runs.append(PastRun(run_data))
        self.update_pb()
        self.stages = [Stage(index) for index in range(len(self.stages))]
        self.update_stage_pbs()

    def tester(self):
        print("###")
        print("Testing pbs")
        if self.pb_run:
            print("Personal Best run:")
            print(f"Stage End times: {self.pb_run.data}")
            print(f"Intervals: {self.pb_run.intervals}")
        for stage in self.stages:
            print(f"Stage {stage.rank} PB: {stage.stage_pb}")
