from enum import Enum


# class State(Enum):
#     NORMAL = 'q'
#     ERROR = 'e'
#     BACK = ' b'
#     FINAL = 'f'


class Config:
    def __init__(self, start):
        self.state = 'q'
        #print("CONFIG", self.state, State.NORMAL)
        self.pos = 0
        self.working_stack = []
        self.input_stack = [start]
