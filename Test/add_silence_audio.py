import tils
import pathlib
import os
import os.path


input_path = 'C:\\Users\\ADMIN\\PycharmProjects\\AutoReview\\Temp_audio\\A1.mp3'
temp_audio_path = 'C:\\Users\\ADMIN\\PycharmProjects\\AutoReview\\Temp_audio\\CC.mp3'
#cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 0.04 "' + temp_audio_path + '"'
cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 0.04 "' + temp_audio_path + '"'
ffmpeg -i input.wav -af "apad=pad_dur=1" output.m4a
os.system(cmd)
