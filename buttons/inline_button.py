from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

mood_emoji_buttons = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="😊", callback_data="happy_emoji"),
                      InlineKeyboardButton(text="😞", callback_data="sad_emoji")],
                     [InlineKeyboardButton(text="😐", callback_data="neutral_emoji"),
                      InlineKeyboardButton(text="😡", callback_data="angry_emoji")],
                     [InlineKeyboardButton(text="😟", callback_data="worried_emoji"), ]])
emoji_keywords = {"happy": ["Joyful", "Cheerful", "Satisfied"], "sad": ["Unhappy", "Gloomy", "Depressed"],
                  "neutral": ["Indifferent", "Unmoved", "Apathetic"], "angry": ["Furious", "Irritated", "Frustrated"],
                  "worried": ["Anxious", "Overwhelmed", "Stressed"]}


async def generate_emoji_keywords(current_mood_emoji):
    emoji_keywords_keyboard = InlineKeyboardBuilder()
    for emoji in emoji_keywords[current_mood_emoji]:
        emoji_keywords_keyboard.add(InlineKeyboardButton(text=emoji, callback_data=f"keyword_{emoji}"))

    emoji_keywords_keyboard.adjust(2)
    emoji_keywords_keyboard.row(InlineKeyboardButton(text="None of the above", callback_data="keyword_other"))

    return emoji_keywords_keyboard.as_markup()
