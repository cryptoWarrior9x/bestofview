from math import floor
from os import listdir
from os.path import isfile, join
import pathlib
import os
import datetime
import os.path
from googletrans import Translator
from sympy import symbols, Eq, solve
import fpt_sound_api

current_director_path = pathlib.Path().resolve()


def split_video(video_result_list, editor_list):
    list_of_success = []
    for video in video_result_list:
        if video['result'] == 'Success':
            list_of_success.append(video)
    chunk_size = floor(len(list_of_success) / 3)
    chunked_list = [list_of_success[i:i + chunk_size] for i in range(0, len(list_of_success), chunk_size)]
    result = {}
    for i in range(len(editor_list)):
        result[editor_list[i]] = chunked_list[i]
        if i == len(editor_list) - 1 and len(chunked_list) > len(editor_list):
            for video in chunked_list[-1]:
                result[editor_list[i]].append(video)
    return result


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def get_video_duration(path_file):
    import subprocess
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", path_file],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    file_length = float(result.stdout)
    return file_length


def equations(video1, video2, audio1, audio2, smooth_number):
    x, y = symbols('x y')
    eq1 = Eq(x + y - audio1 - audio2)
    eq2 = Eq(x / video1 - y / video2 - smooth_number / 100)
    sol = solve((eq1, eq2), (x, y))
    result = {}
    result['audio1'] = round(sol[x], 3)
    result['audio2'] = round(sol[y], 3)
    return result


def ratio_list(video_list, audio_list):
    ratio_list = []
    for i in range(0, len(video_list)):
        ratio = (float(audio_list[i]) / float(video_list[i])) * 100
        ratio_list.append("{:.2f}".format(ratio))
    return ratio_list


def get_sub_time_list():
    mypath = "Images"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    sub_list = []
    for f in onlyfiles:
        start_time = f.split("__")[0].replace("_", ":")
        end_time_script = f.split("__")[1].split("_")
        end_time = end_time_script[0] + ":" + end_time_script[1] + ":" + end_time_script[2] + ":" + end_time_script[3]
        time_obj = [start_time, end_time]
        sub_list.append(time_obj)
    return sub_list


def duration_by_milisecond(time_stamp):
    # "0:00:00.000"
    time_stamp = rreplace(time_stamp, ".", ":", 1)
    h, m, s, f = time_stamp.split(':')
    second = int(h) * 3600 + int(m) * 60 + int(s)
    milisecond = second * 1000 + int(f)
    return milisecond


def get_length(type, type_1):
    path_f = ''
    if type_1 == 'audio':
        path_f = current_director_path.__str__() + "\\Temp_audio\\"
    else:
        if type == 'out':
            path_f = current_director_path.__str__() + "\\Temp_video_output\\"
        else:
            path_f = current_director_path.__str__() + "\\Temp_video\\"

    num_of_files = len(os.listdir(path_f))
    lenght_list = []
    for i in range(num_of_files):
        if type_1 == 'audio':
            filename = path_f + "A" + str(i + 1) + ".mp3"
        else:
            filename = path_f + str(i + 1) + ".mp4"
        file_length = get_video_duration(filename)
        lenght_list.append(file_length)
    return lenght_list


def convert_time_to_milisecond(time_stamp):
    # '0:00:00:042'
    hh = int(time_stamp.split(":")[0])
    mm = int(time_stamp.split(":")[1])
    ss = int(time_stamp.split(":")[2])
    ff = int(time_stamp.split(":")[3])
    time_in_milisecond = (hh * 60 * 60 + mm * 60 + ss) * 1000 + ff
    return time_in_milisecond


def convert_milisecond_to_time(milisecond):
    time_stamp = datetime.datetime.fromtimestamp(milisecond / 1000.0).strftime('0:%M:%S:%f')
    return time_stamp

def convert_milisecond_to_time_v2(milisecond):
    time_stamp = datetime.datetime.fromtimestamp(milisecond / 1000.0).strftime('0:%M:%S.%f')
    return time_stamp


def get_sub_by_srt_file(subtitle_name):
    # sub_list = [[start_time, end_time], [start_time, end_time], ...]
    subtitle_path = "Input\\" + subtitle_name
    print(subtitle_path)
    f = open(subtitle_path, 'r', encoding='utf-8')
    lines = f.readlines()
    sub_list = []
    for line in lines:
        if '00:' in line:
            start_time = line.split(" --> ")[0].strip()
            end_time = line.split(" --> ")[1].strip()
            sub_list.append([start_time.replace(',', ':'), end_time.replace(',', ':')])
    f.close()
    return sub_list


def get_sub_by_time_list():
    mypath = "Images"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    sub_list = []
    for f in onlyfiles:
        start_time = f.split("__")[0].replace("_", ":")
        end_time_script = f.split("__")[1].split("_")
        end_time = end_time_script[0] + ":" + end_time_script[1] + ":" + end_time_script[2] + ":" + end_time_script[3]
        time_obj = [start_time, end_time]
        sub_list.append(time_obj)
    return sub_list


def create_foreign_subfile(video_name, language):
    language_code = ''
    if language == 'es-mx':  # Tay Ban Nha
        language_code = 'es'
    elif language == 'id-id':  # Indonesia
        language_code = 'id'
    elif language == 'hi-in':  # An Do
        language_code = 'hi'
    elif language == 'ar-eg':  # Ai Cap
        language_code = 'ar'
    elif language == 'tl-tl':  # Philippine
        language_code = 'tl'
    elif language == 'th-th':  # Thai Lan
        language_code = 'th'
    elif language == 'vi-vi':  # Viet Nam
        language_code = 'vi'
    srt_file_name = video_name + '-vi-vi'
    vietsub_path = current_director_path.__str__() + "\\Input\\" + srt_file_name + ".txt"
    output_foreign_path = current_director_path.__str__() + "\\Input\\" + video_name + '-' + language + ".txt"
    if os.path.exists(vietsub_path):
        os.remove(vietsub_path)
    if os.path.exists(output_foreign_path):
        os.remove(output_foreign_path)
    full_sub = fpt_sound_api.get_full_sub_in_srt_file(srt_file_name)
    f_w = open(vietsub_path, 'w', encoding='utf-8')
    f_w.write(full_sub)
    f_w.close()
    if language == 'vi-vi':  # Neu edit vietnam thi den day la da co ban text tieng viet nen se return
        return
    translator = Translator()
    f = open(output_foreign_path, 'w', encoding='utf-8')
    len_sub = len(full_sub)
    if len_sub < 4800:
        translated = translator.translate(full_sub, src='vi', dest=language_code)
        f.write(translated.text)
    elif len_sub >= 4800 and len_sub < 9600:
        for i in range(4700, 4990):
            if full_sub[i] == '.':
                chunk_1 = translator.translate(full_sub[:i + 1], src='vi', dest=language_code)
                f.write(chunk_1.text + '\n')
                chunk_2 = translator.translate(full_sub[i + 1:], src='vi', dest=language_code)
                f.write(chunk_2.text)
                break
    elif len_sub >= 9600:
        int_1 = 0
        for i in range(4700, 4990):
            if full_sub[i] == '.':
                chunk_1 = translator.translate(full_sub[:i + 1], src='vi', dest=language_code)
                f.write(chunk_1.text + '\n')
                int_1 = i + 1
                break
        for i in range(9400, 9600):
            if full_sub[i] == '.':
                chunk_2 = translator.translate(full_sub[int_1:i + 1], src='vi', dest=language_code)
                f.write(chunk_2.text + '\n')
                chunk_3 = translator.translate(full_sub[i + 1:], src='vi', dest=language_code)
                f.write(chunk_3.text)
                break
    f.close()
