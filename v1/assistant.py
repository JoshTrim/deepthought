import whisper
import ollama
import torch
from TTS.api import TTS
import pyaudio
import wave
from tqdm import tqdm
from pathlib import Path
import time
from piper.voice import PiperVoice
from random import randrange

from capture import record_mic

from langchain_community.llms import Ollama

class Assistant:

    def __init__(
            self,
            whisper_model:str,
            ollama_model:str,
            record_duration:int = 5,
            ):

        self.RUNNING = True
        
        self.whisper_model = whisper.load_model(whisper_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts_output = "tts_output.wav"
        self.record_duration = record_duration

        if torch.backends.mps.is_available():
            mps_device = torch.device("mps")
        else:
            pass

        self.tts_model = TTS("tts_models/en/jenny/jenny").to(device)
        self.ollama_model = ollama_model
        self.llm = Ollama(model=ollama_model)

        

        self.voices_file_path = "./voices/"

        self.voice_demos = []
        self.voice_models = []

        for nationality in self.voices.values():
            for name, model in nationality.items():
                self.voice_demos.append(Path(self.voices_file_path + "wav/" + name + "_output.wav"))
                self.voice_models.append(Path(self.voices_file_path + model))

        self.voice_model = str(self.voice_models[randrange(len(self.voice_models))].resolve())
        self.voice = PiperVoice.load(self.voice_model)


    def record(self):

        # Recording parameters
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        fs = 44100 # sample rate
        file_name = "recording_output.wav"
        input_device = 1

        p = pyaudio.PyAudio()

        stream = p.open(format=sample_format,
                        channels=1,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []

        print('\n> Recording...')

        # Record loop
        for i in tqdm(range(0, int(fs / chunk * self.record_duration))):
            data = stream.read(chunk)
            frames.append(data)

        # Close stream
        stream.stop_stream()
        stream.close()

        # Close portaudio interface
        p.terminate()

        print('\n> Finished recording')

        # Save file
        wf = wave.open(file_name, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        self.recording = file_name

    def stt(self):
        self.transcription = self.whisper_model.transcribe(self.recording)['text']
        
        # Detect stop word
        if "quit" in self.transcription:
            self.RUNNING = False

        print(f"\nTranscription: \n{self.transcription}")

    def capture(self):
        self.record()
        self.stt()

    def convert_to_query(self, message):
        query = {"role" : "user", "content" : message + ". Please answer in one or two sentences."}
        return [query]

    def query(self):
        response = []
        for chunks in self.llm.stream(self.transcription):
            response.append(chunks)
            print(chunks, sep='', end='')
        self.response = ''.join(response)
        # response = ollama.chat(model=self.ollama_model, messages=self.convert_to_query(self.transcription))
        # self.response = response['message']['content']

    def tts(self):
        if not self.response:
            return "Error, no transcription available."
        else:
            wav_file = wave.open(self.tts_output, 'w')
            audio = self.voice.synthesize(self.response, wav_file)
        # self.tts_model.tts_to_file(text=self.response, file_path=self.tts_output, preset="ultra_fast")

    def play_audio_file(self, file=None):
        CHUNK = 1024
        if file == None: file = self.tts_output

        with wave.open(file, 'rb') as wf:
            # Instantiate PyAudio and initialize PortAudio system resources (1)
            p = pyaudio.PyAudio()

            # Open stream (2)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            # Play samples from the wave file (3)
            while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
                stream.write(data)

            # Close stream (4)
            stream.close()

            # Release PortAudio system resources (5)
            p.terminate()

    def speak(self):
        self.play_audio_file()

    def talk(self):

        while self.RUNNING:

            # record mic for 5 secs, convert to transcription
            self.capture()
            
            # send transcript to ollama
            self.query()

            # render ollama response to audio file
            self.tts()

            # play audio file
            self.speak()

    def demo_voices(self):
        for voice in self.voice_demos:
           self.play_audio_file(file=str(voice.resolve()))
           time.sleep(1)

    def select_voice(self):
        self.demo_voices()


        


# Initialise assistant
deepthought = Assistant(
        whisper_model="base",
        ollama_model="llama2-uncensored"
        )

deepthought.talk()
# deepthought.demo_voices()
