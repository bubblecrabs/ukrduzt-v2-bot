from aiogram.fsm.state import State, StatesGroup


class MailingState(StatesGroup):
    """FSM states for managing the mailing process."""
    text: State = State()
    time: State = State()
