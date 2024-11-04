from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router

from aiogram import F
from numba.core.cgutils import printf

from buttons.inline_button import mood_emoji_buttons, generate_emoji_keywords, yes_no_mood
from handlers.handler import send_to_llama, process_mood
from states.state import Daily_mood

mood_router = Router()


@mood_router.message(Command("mood"))
async def cmd_mood(message: Message, state: FSMContext):
    await message.answer("How are you feeling today?", reply_markup=mood_emoji_buttons)
    await state.set_state(Daily_mood.emoji_status)


@mood_router.callback_query(F.data.endswith("emoji"), Daily_mood.emoji_status)
async def cmd_keyword(callback: CallbackQuery, state: FSMContext):
    await state.update_data(emoji_status=callback.data)
    await state.set_state(Daily_mood.mood_keyword)
    await callback.message.edit_text(text=f"Do you feel specific emotion associate with this mood?",
                                     reply_markup=await generate_emoji_keywords(callback.data.split("_")[0]))
    await callback.answer()


@mood_router.callback_query(F.data.startswith("keyword"), Daily_mood.mood_keyword)
async def cmd_emoji(callback: CallbackQuery, state: FSMContext):
    await state.update_data(mood_keyword=callback.data.split("_")[-1])
    await state.set_state(Daily_mood.confirmation)
    await callback.message.answer(text=f"Do you want to talk about this?")
    await callback.answer()


@mood_router.message(Daily_mood.confirmation)
async def cmd_yes_no_mood(message: Message, state: FSMContext):
    await state.update_data(confirmation=message.text.split("_")[0])
    mood_data = await state.get_data()
    await process_mood(mood_data)
    user_prompt = f"{message.text.split("_")[0]}"
    llama_response = await send_to_llama(user_prompt)
    await message.answer(llama_response)
    await state.clear()
