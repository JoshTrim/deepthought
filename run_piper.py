import os
import wave
from piper.voice import PiperVoice
from tqdm import tqdm

voices = {
        'british' : {
            'alan' : 'en_GB-alan-medium.onnx',
            'alba' : 'en_GB-alba-medium.onnx',
            'aru' : 'en_GB-aru-medium.onnx',
            'jenny_dioco' : 'en_GB-jenny_dioco-medium.onnx',
            'northern_english_male' : 'en_GB-northern_english_male-medium.onnx',
            'semaine' : 'en_GB-semaine-medium.onnx',
            'southern_english_female' : 'en_GB-semaine-medium.onnx',
            'vctk' : 'en_GB-vctk-medium.onnx',
        },
        'american' : {
            'amy' : 'en_US-amy-medium.onnx',
            'arctic' : 'en_US-arctic-medium.onnx',
            'danny' : 'en_US-danny-low.onnx',
            # 'hfc_male' : 'en_US-hfc-male-medium.onnx',
            'joe' : 'en_US-joe-medium.onnx',
            'kathleen' : 'en_US-kathleen-low.onnx',
            'kusal' : 'en_US-kusal-medium.onnx',
            'l2arctic' : 'en_US-l2arctic-medium.onnx',
            # do later
            #'lessac' : 'en_US-lessac-medium',
            #'libritts' : 'en_US-libritts-medium',
            #'libritts_r' : 'en_US-librittes_r-medium',
            #'ryan' : 'en_US-ryan-medium',
            },
    }


voicedir = os.path.expanduser('/Users/joshtrim/Development/Python/deepthought/voices/') #Where onnx model files are stored on my machine

def introduce_yourselves():
    for nationality, value in tqdm(voices.items()):
        for name, voice in tqdm(value.items()):
            model = voicedir+voice
            voice = PiperVoice.load(model)
            wav_file = wave.open(f'{name}_output.wav', 'w')
            text = f"Hello, my name is {name}. This is an example of how I sound."
            audio = voice.synthesize(text,wav_file)
            


introduce_yourselves()



