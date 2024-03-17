from collections.abc import Iterable
from pydantic import BaseModel
from RealtimeTTS import TextToAudioStream, CoquiEngine
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

class Voice(BaseModel):
    name:str = "Henriette Usha"

class Voices(BaseModel):
    voices_dir:Path = Path("../models/coqui_voices/")
    voice_list:list = [file.name.split("_")[-1].split(".")[0] for file in voices_dir.glob("*.wav")]
    voices:list = [Voice(name=voice) for voice in voice_list]

class Generator(BaseModel):
    chunks:list = ["Hey guys! These here are realtime spoken sentences based on local text synthesis. ",
                  "With a local, neuronal, cloned voice. So every spoken sentence sounds unique."]

class DeepThought(BaseModel):

    engine:CoquiEngine = CoquiEngine(level=logging.INFO, thread_count=6, stream_chunk_size=50, full_sentences=False, voice="Henriette Usha")
    stream:TextToAudioStream = TextToAudioStream(engine)
    generator:Generator = Generator()
    logging:bool = True

    def speak(self):
        self.stream.feed(self.generator.chunks).play(log_synthesized_text=self.logging)
        self.engine.shutdown()

deepthought = DeepThought()

deepthought.speak()
