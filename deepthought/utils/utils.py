import subprocess
import re

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def is_full_sentences(text):
    return text.endswith((".", "!", "?"))

def split_into_sentences(text):
    return re.split(f"(?<=[.!?]s+", text)
