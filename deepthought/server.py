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

os.environ["STT_RUNNER"] = "server"
os.environ["TTS_RUNNER"] = "server"
