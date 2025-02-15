from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    """FSM states for the set admin process."""
    func: State = State()
    id: State = State()


class MailingState(StatesGroup):
    """FSM states for the set mailing process."""
    menu: State = State()
    text: State = State()
    media: State = State()
    button_text: State = State()
    button_url: State = State()
    delay: State = State()
