from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    """FSM states for the set admin process."""
    func: State = State()
    id: State = State()


class MailingState(StatesGroup):
    """FSM states for the set mailing process."""
    text: State = State()
    time: State = State()
