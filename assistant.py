import whisper
import ollama
import torch
from TTS.api import TTS
import pyaudio
import wave
from tqdm import tqdm

from capture import record_mic

class Assistant:

    def __init__(
            self,
            whisper_model:str,
            ollama_model:str,
            record_duration:int = 5,
            ):

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
        print(f"\nTranscription: \n{self.transcription}")

    def capture(self):
        self.record()
        self.stt()

    def convert_to_query(self, message):
        query = {"role" : "user", "content" : message + ". Please answer in one or two sentences."}
        return [query]

    def query(self):
        response = ollama.chat(model=self.ollama_model, messages=self.convert_to_query(self.transcription))
        self.response = response['message']['content']

    def render_response(self):
        self.tts_model.tts_to_file(text=self.response, file_path=self.tts_output)

    def play_audio_file(self):

        # Set chunk size of 1024 samples per data frame
        chunk = 1024  

        # Open the sound file 
        wf = wave.open(self.tts_output, 'rb')

        # Create an interface to PortAudio
        p = pyaudio.PyAudio()

        # Open a .Stream object to write the WAV file to. 'output = True' indicates that the sound will be played rather than recorded
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # Read data in chunks
        data = wf.readframes(chunk)

        # Play the sound by writing the audio data to the stream
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)

        # Close and terminate the stream
        stream.close()
        p.terminate()

    def speak(self):
        self.play_audio_file()

    def talk(self):

        # record mic for 5 secs, convert to transcription
        deepthought.capture()
        
        # send transcript to ollama
        deepthought.query()

        # render ollama response to audio file
        deepthought.render_response()

        # play audio file
        deepthought.speak()



deepthought = Assistant(
        whisper_model="base",
        ollama_model="llama2-uncensored"
        )

deepthought.talk()
