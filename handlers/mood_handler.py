from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Router

from aiogram import F
from numba.core.cgutils import printf

from buttons.inline_button import mood_emoji_buttons, generate_emoji_keywords
from handlers.handler import send_to_llama

mood_router = Router()


@mood_router.message(Command("mood"))
async def cmd_mood(message: Message):
    await message.answer("How are you feeling today?", reply_markup=mood_emoji_buttons)


@mood_router.callback_query(F.data.endswith("emoji"))
async def cmd_emoji(callback: CallbackQuery):
    await callback.message.edit_text(text=f"Do you feel specific emotion associate with this mood?",
                                        reply_markup=await generate_emoji_keywords(callback.data.split("_")[0]))


@mood_router.callback_query(F.data.startswith("keyword"))
async def cmd_emoji(callback: CallbackQuery):
    user_prompt = f"When asked to describe their mood in the list of relevant keywords, user responded with the following word: {callback.data.split("_")[1]}. Adapt your responses according to their mood. You can start by asking why they are feeling this way but don't instantly offer the solution."
    llama_response = await send_to_llama(user_prompt)
    await callback.message.answer(llama_response)
    await callback.answer()
