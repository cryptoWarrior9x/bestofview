import pathlib
import os
import subprocess as sp
import os.path
import tils
import time
from datetime import datetime

current_director_path = pathlib.Path().resolve()
dir = "C:\\Users\\ADMIN\\PycharmProjects\\AutoReview\\Output"
video = dir + '\\Army_of_Thieves_vi-vi.mp4'
audio = dir + '\\Army_of_Thieves-es-mx.mp3'
video_len = tils.get_video_duration(video)
audio_len = tils.get_video_duration(audio)

output_path = dir + '\\test1.mp4'
ratio = round(float(audio_len) / float(video_len), 3)

cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i ' + video + ' -r 32 -filter:v "setpts=' + str(ratio) + '*PTS" ' + output_path
os.system(cmd)
print('x')
