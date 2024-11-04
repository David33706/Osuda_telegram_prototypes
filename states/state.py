from aiogram.fsm.state import StatesGroup, State


class Daily_mood(StatesGroup):
    emoji_status = State()
    mood_keyword = State()
    confirmation = State()
    messaging_status = State()