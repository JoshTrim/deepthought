from dotenv import load_dotenv
load_dotenv()

import traceback
from platformdirs import user_data_dir
import ast
import json
import queue
import os
import datetime
# need to make bytes_to_wav
import re
from fastapi import FastAPI, Request
from fastapi.response import PlainTextResponse
from starlette.websockets import WebSocket, WebSocketDisconnect
from pathlib import Path
import asyncio
import urllib.parse
# need to implement a few functions here
from deepthought.utils.accumulator import Accumulator
from deepthought.utils.utils import split_into_sentences, is_full_sentences

os.environ["STT_RUNNER"] = "server"
os.environ["TTS_RUNNER"] = "server"

accumulator = Accumulator()
app = FastAPI()

app_dir = user_data_dir("deepthought")
conversation_history_path = os.path.join(app_dir, "conversations", "user.json")

SERVER_LOCAL_PORT = int(os.getenv("SERVER_LOCAL_PORT", 10001))

# Queues
from_computer = queue.Queue() # Computer messages from the device
from_user = asyncio.Queue() # User messages from the device
to_device = asyncio.Queue() # Messages we send

# Switch code executor to device, if set

if os.getenv("CODE_RUNNER") == "device":

    class Python:
        # Name that will appear to LLM
        name = "python"

        def __init__(self):
            self.halt = False

        def run(self, code):
            """Generator that yields a dictionary in the LMC format"""

            # Prepare data 
            message = {"role" : "assisstant", "type" : "code", "format" : "python", "content" : code}

            # Unless already sent to device, wrap in start/end flags
            if not (interpreter.messages and interpreter.messages[-1] == message):
                to_device.put({"role" : "assistant", "type" : "code", "format" : "python", "start" : True})
                to_device.put(message)
                to_device.put({"role" : "assistant", "type" : "code", "format" : "python", "end" : True})


