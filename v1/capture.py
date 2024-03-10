import pyaudio
import wave

# Constants
CHUNK = 1024
SAMPLE_FORMAT = pyaudio.paInt16
CHANNELS = 1
FS = 44100 # sample rate
SECONDS = 3 # duration
FILENAME = "output.wav"

p = pyaudio.PyAudio()

def record_mic(
        duration:int = 5, 
        file_name=FILENAME):


    print('\n> Recording...')

    stream = p.open(format=SAMPLE_FORMAT,
                    input_device_index=0,
                    channels=CHANNELS,
                    rate=FS,
                    frames_per_buffer=CHUNK,
                    input=True)

    frames = []

    # Record loop
    for i in range(0, int(FS / CHUNK * SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Close stream
    stream.stop_stream()
    stream.close()

    # Close portaudio interface
    p.terminate()

    print('\n> Finished recording')

    # Save file
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
    wf.setframerate(FS)
    wf.writeframes(b''.join(frames))
    wf.close()

    return file_name
