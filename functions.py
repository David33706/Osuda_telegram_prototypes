from aiogram.types import Message

import os
from dotenv import load_dotenv
import json
import aiohttp
import whisper

import tempfile

from config import bot

load_dotenv()

OLLAMA_API_URL = os.getenv('OLLAMA_API_URL')
LLAMA_MODEL = os.getenv('LLAMA_MODEL')


async def process_prompt(message: Message):
    if message.voice:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            await bot.download_file(file.file_path, temp_file.name)
            temp_filename = temp_file.name

        model = whisper.load_model("turbo")
        result = model.transcribe(temp_filename)
        return result["text"]
    else:
        return message.text


async def send_to_llama(user_prompt, conversation_history):
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
