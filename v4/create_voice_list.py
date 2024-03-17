from pathlib import Path

root_dir = Path("./models/coqui_voices/")

for file in root_dir.glob("*.wav"):
    file_name = file.name.split("_")[-1].split(".")[0]
    print(file_name)
