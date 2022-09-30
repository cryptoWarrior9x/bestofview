import requests
import urllib.request
import json
import time
import pathlib
import os
import os.path
import audio_effect

current_director_path = pathlib.Path().resolve()
video_name = "orphan"

def refactor_line(line):
    line = line.strip()
    line = line.replace('.', '')
    line = line + '.'
    return line + ''


def get_full_sub_in_srt_file(srt_file_name):
    srt_file_path = current_director_path.__str__() + "\\Input\\" + srt_file_name + ".srt"
    f = open(srt_file_path, 'r', encoding='utf-8')
    Lines = f.readlines()
    full_sub = ''
    len_line = len(Lines)
    for i in range(len_line):
        try:
            if "00:" in Lines[i]:
                full_sub = full_sub + refactor_line(Lines[i + 1]) + '\n'
        except:
            pass
    f.close()
    return full_sub

str_file_name = video_name + '-vi-vi'

full_sub = get_full_sub_in_srt_file(str_file_name)
text_file_path = current_director_path.__str__() + "\\Output\\" + str_file_name + ".txt"
f_w = open(text_file_path, 'w', encoding='utf-8')
f_w.write(full_sub)
f_w.close()
