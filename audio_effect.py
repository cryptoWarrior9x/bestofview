import pathlib
import os
import subprocess as sp
import os.path
import tils
import time
from datetime import datetime

current_director_path = pathlib.Path().resolve()


def speed_up_audio(temp_path, file_path):
    cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + temp_path + '" -filter:a atempo=1.1 "' + file_path + '"'
    os.system(cmd)


def trim_silence_sound(audio_path, language_code):
    # ['00:00:00:080', '00:00:01:870']
    cmd_length = 'ffprobe -i ' + audio_path + ' -show_entries format=duration -sexagesimal -v quiet -of csv="p=0"'
    output = sp.getoutput(cmd_length)[:-3]
    # '0:00:04.022'
    format = '%H:%M:%S.%f'
    if language_code == 'tl-tl':
        cut_time = '0:00:00.020'
    else:
        cut_time = '0:00:00.095'
    to = str(datetime.strptime(output, format) - datetime.strptime(cut_time, format))
    file_name = audio_path.split('\\')[-1]
    output_path = audio_path[:-len(file_name)] + 'A' + file_name
    cmd_cut = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + audio_path + '" -ss 0:00:00.130 -to ' + to + ' "' + output_path + '"'
    print(cmd_cut)
    os.system(cmd_cut)
    os.remove(audio_path)


def create_raw_video_sound(start_time, end_time, video_name, output_audio_path):
    INPUT_VIDEO_PATH = current_director_path.__str__() + '\\Input\\' + video_name + '.mp4'
    output = current_director_path.__str__() + '\\temp.mp4'
    ss = tils.rreplace(start_time, ':', '.', 1)
    to = tils.rreplace(end_time, ':', '.', 1)
    cmd_cut = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + INPUT_VIDEO_PATH + '" -ss ' + ss + ' -to ' + to + ' "' + output + '"'
    os.system(cmd_cut)
    # extract audio from video
    cmd_extract = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + output + '" "' + output_audio_path + '"'
    os.system(cmd_extract)
    os.remove('temp.mp4')


def get_raw_audio(video_name, audio_name, len_sub_list, sub_video_list):
    for i in range(len(sub_video_list)):
        if sub_video_list[i][2] == '0':
            pass


def audio_effect_v2(video_name, audio_path, sub_video_list, start_list, end_list, duration_list, remove_duration_ratio):
    # Remove before create audio
    dir = current_director_path.__str__() + "\\Temp_audio"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    raw_video_count = 0
    for i in range(len(sub_video_list)):
        if sub_video_list[i][2] == '1':
            ss = round((end_list[i - raw_video_count] - 0.007), 3)
            to = round(
                (start_list[i - raw_video_count + 1] + duration_list[i - raw_video_count + 1] / remove_duration_ratio),
                3)
            # CMD = FFmpeg_path + " -i " + INPUT_VIDEO_PATH + ' -ss ' + ss + " -to " + to + " " + output
            output_path = current_director_path.__str__() + "\\Temp_audio\\" + str(i + 1) + ".mp3"
            cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i ' + audio_path + ' -ss ' + str(ss) + " -to " + str(
                to) + " " + output_path
            os.system(cmd)
        elif sub_video_list[i][2] == '0':
            output_path = current_director_path.__str__() + "\\Temp_audio\\" + str(i + 1) + ".mp3"
            create_raw_video_sound(sub_video_list[i][0], sub_video_list[i][1], video_name, output_path)
            raw_video_count = raw_video_count + 1


def most_common(lst):
    return max(set(lst), key=lst.count)


def get_audio_list(video_name, audio_name, video_sub_len, sub_video_list, noise, duration, remove_duration_ratio):
    # Dau tien, tu file giong doc se lay ra nhung doan video khong noi trong 20ms
    audio_file_path = current_director_path.__str__() + "\\Audio\\" + audio_name + ".mp3"
    # "C:\\FFmpeg\\bin\\ffmpeg.exe -i C:\\Users\\ADMIN\\PycharmProjects\\AutoReview\\Audio\\ac_quy_1.mp3 -af silencedetect=n=-40dB:d=0.07 -f null -"
    cmd = "C:\\FFmpeg\\bin\\ffmpeg.exe -i " + audio_file_path + " -af silencedetect=n=" + noise + "dB:d=" + duration + " -f null -"
    output = sp.getoutput(cmd)
    # sau do, ghi output vao file silence_log.txt
    f = open('silence_log.txt', 'w')
    f.write(output)
    f.close()

    f_read = open('silence_log.txt', 'r')
    Lines = f_read.readlines()

    start_list = []  # start_list là danh sách bắt đầu 
    for line in Lines:
        if "silence_start:" in line:
            start_list.append(float(line.split(": ")[-1].strip()))

    end_list = []
    duration_silent_list = []
    for line in Lines:
        if "silence_end:" in line:
            end_list.append(float(line.split("|")[0].split(": ")[-1].strip()))
            duration_silent_list.append(float(line.split(" | ")[-1].split(": ")[-1].strip()))
    # Doan nay xác định nếu thời gian giữa 2 khoảng nghỉ bé hơn 0.01s tức là nhiễu thì sẽ xóa đoạn đó và cộng 2 đoạn
    # liên tiếp lại với nhau
    i = 1
    while i < len(start_list):
        if (start_list[i] - end_list[i - 1]) <= 0.01:
            duration_silent_list[i - 1] = duration_silent_list[i - 1] + duration_silent_list[i]
            end_list.pop(i - 1)
            start_list.pop(i)
            duration_silent_list.pop(i)
        else:
            i = i + 1

    while len(duration_silent_list) > video_sub_len + 1:
        min_duration = min(duration_silent_list)
        min_duration_index = duration_silent_list.index(min_duration)
        start_list.pop(min_duration_index)
        end_list.pop(min_duration_index)
        duration_silent_list.pop(min_duration_index)
    print(min(duration_silent_list))
    audio_effect_v2(video_name, audio_file_path, sub_video_list, start_list, end_list, duration_silent_list,
                    remove_duration_ratio)
    f_read.close()


def concet_audio_files(audio_name):
    # remove current video before concat
    output_audio_path = current_director_path.__str__() + "\\Output\\" + audio_name + ".mp3"
    if os.path.exists(output_audio_path):
        os.remove(output_audio_path)

    # Concat video
    mypath = current_director_path.__str__() + "\\Temp_audio"
    file_list = os.listdir(mypath)
    f = open('mylist_audio.txt', 'w')
    for i in range(len(file_list)):
        file_path = current_director_path.__str__() + "\\Temp_audio\\A" + str(i + 1) + '.mp3'
        line_fomat = "file '" + file_path + "'"
        f.write(line_fomat + "\n")
    f.close()
    mylist_path = current_director_path.__str__() + "\\mylist_audio.txt"

    # "ffmpeg -safe 0 -f concat -i list.txt -c copy output.mp4"
    out_path = current_director_path.__str__() + "\\Output\\" + audio_name + ".mp3"

    cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -safe 0 -f concat -i "' + mylist_path + '" "' + out_path + '"'
    print(cmd)
    os.system(cmd)


def concet_audio_files_v1(audio_name):
    # remove current video before concat
    output_audio_path = current_director_path.__str__() + "\\Output\\" + audio_name + ".mp3"
    if os.path.exists(output_audio_path):
        os.remove(output_audio_path)
    text_video_list_path = current_director_path.__str__() + "\\mylist_audio.txt"
    if os.path.exists(text_video_list_path):
        os.remove(text_video_list_path)

    # Concat video
    mypath = current_director_path.__str__() + "\\Temp_audio"
    from os import walk

    filenames = next(walk(mypath), (None, None, []))[2]
    sorted_list = []
    for i in range(1, len(filenames) + 1):
        # file_name = str(i) + ".mp3"
        file_name = 'A' + str(i) + ".mp3"
        sorted_list.append(file_name)
    print(sorted_list)
    f = open('mylist_audio.txt', 'w')
    for file in sorted_list:
        file_path = current_director_path.__str__() + "\\Temp_audio\\" + file
        line_fomat = "file '" + file_path + "'"
        f.write(line_fomat + "\n")
    f.close()
    mylist_path = current_director_path.__str__() + "\\mylist_audio.txt"

    # "ffmpeg -safe 0 -f concat -i list.txt -c copy output.mp4"
    out_path = current_director_path.__str__() + "\\Output\\" + audio_name + ".mp3"

    cmd = "C:\\FFmpeg\\bin\\ffmpeg.exe -safe 0 -f concat -i " + mylist_path + " " + out_path
    print(cmd)
    os.system(cmd)
