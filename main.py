import random, os

audio_path = './audios'
audio_file = random.choice(os.listdir(audio_path))
print("./audios" + audio_file)