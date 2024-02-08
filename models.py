# standard library
from pathlib import Path
from pprint import pprint
import json

# third party
from pydantic import BaseModel
from pydantic_core.core_schema import JsonSchema

class VoiceChoices(BaseModel):
    voices: list = []
    data_file_path: Path
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
                voice_model = Voice(name=name, nationality=nationality, onnx_file=onnx_file, demo_wav=demo_wav)
                self.voices.append(voice_model)

class Voice(BaseModel):
    name: str
    nationality: str
    onnx_file: Path
    demo_wav: Path


voice_choices = VoiceChoices(data_file_path=Path("./data/"))
voice_choices.load_voice_choices()
pprint(voice_choices)


# for nationality, models in voice_choices.items():
#     for name, model_file in models.items():
#         model_path = Path(voice_file_path + model_file)
#         demo_wav_path = Path(voice_file_path + "wav/" + name + "_output.wav")
#
#         voice = Voice(name=name, nationality=nationality, onnx_file=model_path, demo_wav=demo_wav_path)
#         voices.append(voice)
#
# pprint(voices)
