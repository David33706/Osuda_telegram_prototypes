from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import Router

from functions import send_to_llama, process_prompt

# Get Ollama API information from .env

# Store conversation history
conversation_history = [{"role": "system",
                         "content": "You are Osuda AI - psychology assistant, which only answers question related to psychology"}]

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello. I am Osuda AI")


@router.message()
async def handle_message(message: Message):
    global conversation_history

    user_prompt = await process_prompt(message)
    llama_response = await send_to_llama(user_prompt, conversation_history)
    await message.answer(llama_response)

# Function to send a prompt to LLaMA via Ollama API

# Register command and message handlers
