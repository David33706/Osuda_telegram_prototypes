from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

mood_emoji_buttons = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="😊", callback_data="happy_emoji"),
                      InlineKeyboardButton(text="😞", callback_data="sad_emoji")],
                      [InlineKeyboardButton(text="😐", callback_data="neutral_emoji"),
                      InlineKeyboardButton(text="😡", callback_data="angry_emoji")],
                      [InlineKeyboardButton(text="😟", callback_data="worried_emoji"), ]])
