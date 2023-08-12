import os
import requests
import json
import random
import webbrowser
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

def create_final_video_with_background_music(video_files, background_music, output_file, fade_duration=1.5):
    # Read all video clips and the background music clip
    video_clips = [VideoFileClip("./videos/" + file) for file in video_files]

    # Calculate the total duration of the video clips
    total_video_duration = sum([clip.duration for clip in video_clips])

    # Calculate the ratio to scale the video duration to match the background music duration
    print(background_music.duration)
    duration_ratio = background_music.duration / total_video_duration

    # Trim and add fade in/out to the video clips
    trimmed_and_faded_clips = []
    for clip in video_clips:
        trimmed_clip = clip.subclip(0, clip.duration * duration_ratio)
        trimmed_and_faded_clip = trimmed_clip.crossfadein(fade_duration).crossfadeout(fade_duration)
        trimmed_and_faded_clips.append(trimmed_and_faded_clip)

    # Concatenate the trimmed and faded video clips
    final_video = concatenate_videoclips(trimmed_and_faded_clips, method="compose")

    # Set the background music as the audio of the final video
    final_video = final_video.set_audio(background_music)

    # Export the final video with background music
    final_video.write_videofile("./outputs/"+output_file, codec="libx264", audio_codec="aac")

    # Close the video clips and background music clip
    final_video.close()
    for clip in video_clips:
        clip.close()
    background_music.close()

def clean_file(root_path):
    dir_list = os.listdir(root_path)
    for i in dir_list:
        os.system("rm -r {}{}".format(root_path,i))

def file_download(root_path):
    url = "http://16.171.160.129/favorites/get_video_link"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.text
    y = json.loads(res)
    count = 0
    for i in y['data']:
        count = count + 1
        os.system("wget '{}' -O {}video_'{}'.mp4".format(i, root_path, count))


def more_file_download(root_path):
    dir_list = os.listdir(root_path)
    dir_list.remove('video.py')
    dir_list.remove('audio.mp3')
    print(len(dir_list))
    url = "http://16.171.160.129/favorites/get_video_link"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.text
    y = json.loads(res)
    count = len(dir_list)
    for i in y['data']:
        count = count + 1
        os.system("wget '{}' -O {}video_'{}'.mp4".format(i, root_path, count))

def more_video_download():
    more = input("Do you download more videos? y/n: ")
    if more == "y":
        return True
    if more == "n":
        return False

def clean_videos():
    more = input("Do you download clean previous videos? y/n: ")
    if more == "y":
        return True
    if more == "n":
        return False
    
def get_video_durations():
    url = "http://16.171.160.129/favorites/get_video_durations"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.text
    y = json.loads(res)
    duration = 0
    for i in y['data']:
        duration = duration + i['duration']
    return duration

# Example usage
root_path = './videos/'
dir_list = os.listdir(root_path)
video_files = dir_list[1:-1]
output_file = "final_output.mp4"

audio_path = './audios'
audio_file = random.choice(os.listdir(audio_path))
audio_file = random.choice(os.listdir(audio_path))
background_music = AudioFileClip("./audios/" + audio_file)

# more_video = more_video_download()
# if more_video:
#     more_file_download(root_path)
# else:
#     clean_file(root_path)
#     file_download(root_path)

clean_video = clean_videos()
if clean_video:
    clean_file(root_path)
    
if background_music.duration > get_video_durations():
    print("Need more videos")
    url = "http://16.171.160.129/stocks-videos"
    webbrowser.open(url, new=0, autoraise=True)
else:
    file_download(root_path)
    create_final_video_with_background_music(video_files, background_music, output_file, fade_duration=1)


