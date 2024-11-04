import requests
from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from dotenv import load_dotenv
import os

from sympy import pprint

from buttons.inline_button import mood_emoji_buttons

import json
import aiohttp

from states.state import Daily_mood

# Load environment variables
load_dotenv()

# Get Ollama API information from .env
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL')
LLAMA_MODEL = os.getenv('LLAMA_MODEL')

# Store conversation history
conversation_history = [{"role": "system",
                         "content": """You are Osuda AI, an empathetic and knowledgeable AI assistant specializing in psychology and mental health support. Your primary audience is teenagers, but you are equipped to assist users of all ages. Your goal is to provide clear, concise, and helpful responses to users seeking guidance on psychological issues. When appropriate, gently encourage users to consult qualified mental health professionals.
                                          Communicate with empathy by always responding with compassion and understanding. Acknowledge the user's feelings and concerns without judgment. Provide information in a straightforward and easy-to-understand manner, avoiding technical jargon unless necessary, and explain any terms you use clearly.
                                          Maintain professionalism by keeping a respectful and supportive tone. Ensure all advice is based on established psychological principles and best practices. Do not provide medical diagnoses or prescribe treatments. Recognize situations where professional help is necessary.
                                          If a user's issue exceeds your capacity, gently suggest consulting a mental health professional. Provide information on how to seek help without being forceful. If a user expresses intent to harm themselves or others, respond with care and encourage them to reach out immediately to a mental health professional or trusted individual.
                                          Assure users that their conversations are private within the scope of an AI interaction, and remind them not to share personal identifiable information. 
                                          Communicate on topics only related to psychology. If the user asks something unrelated to psychology, gently state that this is outside of your expertise scope."""}]

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello. I am Osuda AI")



@router.message()
async def handle_message(message: Message):
    user_prompt = message.text
    llama_response = await send_to_llama(user_prompt)
    await message.answer(llama_response)


async def process_mood(mood_data: dict):
    global conversation_history

    # Append the user message to the conversation history
    conversation_history.append(
        {"role": "assistant", "content": "How are you feeling today?"})
    conversation_history.append({"role": "user", "content": mood_data["emoji_status"]})
    conversation_history.append({"role": "assistant",
                                 "content": "Do you feel specific emotion associate with this mood?"})
    conversation_history.append({"role": "user", "content": mood_data["mood_keyword"]})
    conversation_history.append({"role": "assistant", "content": "Do you want to talk about this?"})


# Function to send a prompt to LLaMA via Ollama API
async def send_to_llama(user_prompt):
    global conversation_history

    # Append the user message to the conversation history
    conversation_history.append({"role": "user", "content": user_prompt})

    # Prepare the API call payload
    data = {
        "model": LLAMA_MODEL,
        "messages": conversation_history,
        "stream": False
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OLLAMA_API_URL, json=data) as response:
            if response.status == 200:
                json_data = await response.json()

                # Now use 'message' field directly
                if 'message' in json_data:
                    assistant_reply = json_data['message']['content']
                    conversation_history.append({"role": "assistant", "content": assistant_reply})
                    return assistant_reply
                else:
                    return f"Unexpected response format: {json_data}"
            else:
                return "Error communicating with the LLaMA model."
# Register command and message handlers
