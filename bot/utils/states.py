from aiogram.fsm.state import State, StatesGroup


class Schedule(StatesGroup):
    """FSM states for managing the schedule process."""
    day: State = State()
    faculty: State = State()
    course: State = State()
    group: State = State()
