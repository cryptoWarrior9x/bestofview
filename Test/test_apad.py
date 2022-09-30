import tils
import pathlib
import os
import os.path

FFmpeg_path = "C:\\FFmpeg\\bin\\ffmpeg.exe"
current_director_path = pathlib.Path().resolve()

input_audio_path = "C:\\Users\\ADMIN\\PycharmProjects\\AutoReview\\Temp_audio\\A15.mp3"
out_audio_path = "C:\\Users\\ADMIN\\PycharmProjects\\AutoReview\\Temp_audio\\DD.mp4"
video_input = "C:\\Users\\ADMIN\\PycharmProjects\\AutoReview\\Temp_video\\15.mp4"

# cmd = 'ffmpeg -i VIDEO -i AUDIO -filter_complex "[1:0]apad" -shortest OUTPUT'
cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + video_input + '" -i "' + input_audio_path + '" -filter_complex "[1:0]apad" -shortest "' + out_audio_path + '"'
# ffmpeg -i input.mp4 -i input.mp3 -c copy -map 0:v:0 -map 1:a:0 output.mp4
# cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + video_input + '" -i "' + input_audio_path + '" -c copy -map 0:v:0 -map 1:a:0 -shortest "' + out_audio_path + '"'
# ffmpeg -i input.wav -f:a atempo=1.25 output.wav
# cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + input_audio_path + '" -filter:a atempo=0.5 "' + input_audio_path + '"'
print(cmd)
os.system(cmd)
