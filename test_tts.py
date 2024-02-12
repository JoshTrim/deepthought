from models import VoiceEngine
from utils import Timer

N_RUNS = 10

with open('./copypasta.py') as f:
    text = f.read().splitlines()

text = ''.join(text)

time_collector = []

for i in range(0, N_RUNS):
    t = Timer()
    engine = VoiceEngine()
    engine.tts(text)
    time_collector.append(t.stop())

average = sum(time_collector) / N_RUNS
print(f"Average time taken: {average}")
