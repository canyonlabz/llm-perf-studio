from enum import Enum

class TestState(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    COMPLETED = 2
    FAILED = 3
    STOPPED = 4

# src/utils/test_state.py (add to same file)
class DeepEvalTestState(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    COMPLETED = 2
    FAILED = 3
    STOPPED = 4
