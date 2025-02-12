from aiogram.fsm.state import State, StatesGroup


class SiteState(StatesGroup):
    """FSM states for the set site process."""
    year: State = State()
    semester: State = State()
