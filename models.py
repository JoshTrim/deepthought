# standard library
from pathlib import Path
from pprint import pprint
import json
from typing import Optional
import time

# third party
from pydantic import BaseModel as PydanticBaseModel
from pydantic_core.core_schema import JsonSchema

from piper.voice import PiperVoice
import wave

from random import randrange

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True # needed because of time.time error

class VoiceChoices(BaseModel):
    voices: list = []
    data_file_path: Path = Path("./data/")
    json_data: JsonSchema = None

    def load_config(self):
        json_file_path = self.data_file_path / "config/" / "json/voices.json"
        
        with open(json_file_path, "r") as f:
            self.json_data = json.load(f)

    def load_voice_choices(self):
        self.load_config()
        
        for nationality, models in self.json_data.items():
            for name, onnx_file in models.items():
                demo_wav = Path(self.data_file_path) / "wav/" / name / "_output.wav"
                onnx_file = Path(self.data_file_path) / "config/onnx/" / onnx_file
                voice_model = Voice(name=name, nationality=nationality, onnx_file=onnx_file, demo_wav=demo_wav)
                self.voices.append(voice_model)

class Voice(BaseModel):
    name: str
    nationality: str
    onnx_file: Path
    demo_wav: Path

class VoiceEngine(BaseModel):
    active_voice: Optional[Voice] = None 
    voice_choices: VoiceChoices = VoiceChoices()
    voice_choices.load_voice_choices()

    def model_post_init(self, *args, **kwargs):
        self.active_voice = self.voice_choices.voices[0]
        print(f"Selected {self.active_voice}")

    def tts(self, script):
        voice = PiperVoice.load(str(self.active_voice.onnx_file.resolve()))
        file_name = f'./output/{self.active_voice.name}_output.wav'
        wav_file = wave.open(file_name, 'wb')
        audio = voice.synthesize(script, wav_file)



# for nationality, models in voice_choices.items():
#     for name, model_file in models.items():
#         model_path = Path(voice_file_path + model_file)
#         demo_wav_path = Path(voice_file_path + "wav/" + name + "_output.wav")
#
#         voice = Voice(name=name, nationality=nationality, onnx_file=model_path, demo_wav=demo_wav_path)
#         voices.append(voice)
#
# pprint(voices)
