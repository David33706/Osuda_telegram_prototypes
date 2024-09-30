import requests
from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import Router
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Ollama API information from .env
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL')
LLAMA_MODEL = os.getenv('LLAMA_MODEL')

# Store conversation history
conversation_history = [{"role": "system",
                         "content": "You are Osuda AI - psychology assistant, which only answers question related to psychology"}]

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello. I am Osuda AI")


@router.message()
async def handle_message(message: Message):
    user_prompt = message.text
    llama_response = await send_to_llama(user_prompt)
    await message.answer(llama_response)


# Function to send a prompt to LLaMA via Ollama API
async def send_to_llama(user_prompt):
    global conversation_history

    # Append the user message to the conversation history
    conversation_history.append({"role": "user", "content": user_prompt})

    # Prepare the API call payload
    data = {
        "model": LLAMA_MODEL,
        "messages": conversation_history
    }

    # Send the request to Ollama API
    response = requests.post(OLLAMA_API_URL, json=data)

    if response.status_code == 200:
        response_data = response.json()
        assistant_reply = response_data['choices'][0]['message']['content']

        # Append the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
    else:
        return "An error occurred while communicating with the LLaMA model."

# Register command and message handlers
