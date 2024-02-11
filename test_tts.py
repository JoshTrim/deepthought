from models import VoiceEngine
from utils import Timer

t = Timer()
engine = VoiceEngine()
engine.tts("Here is some text, please synthesize it")
t.stop()
