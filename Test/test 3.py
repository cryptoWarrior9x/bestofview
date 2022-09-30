import tils
import pathlib
import os
import os.path

FFmpeg_path = "C:\\FFmpeg\\bin\\ffmpeg.exe"
current_director_path = "C:\\Users\\ADMIN\\PycharmProjects\\AutoReview"

input_path = current_director_path + "\\Temp_video\\2.mp4"
output_video_path = current_director_path + "\\Temp_video_output\\A4.mp4"
ratio = 1
cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + input_path + '" -filter:v "setpts=' + str(ratio) + '*PTS" "' + output_video_path + '"'
os.system(cmd)
output_vd_len = tils.get_video_duration(output_video_path)
ad_len = tils.get_video_duration(current_director_path + "\\Temp_audio\\A2.mp3")
input_vd_len = tils.get_video_duration(input_path)
print(ad_len)
