import requests
import urllib.request
import json
import time
import pathlib
import os
import os.path
import audio_effect

current_director_path = pathlib.Path().resolve()
url = 'https://api.fpt.ai/hmi/tts/v5'

headers = {
    'api-key': 'aDe98pap3GlCkTHYX9HsyxM5qhjWglWG',
    'speed': '',
    'voice': 'banmai'
}


def concat_audio(list_audio_file, audio_name):
    out_path = current_director_path.__str__() + "\\Audio\\" + audio_name + ".mp3"
    # remove before create find
    if os.path.isfile(out_path):
        os.remove(out_path)

    # Tao silent audio de them vao truoc vao sau moi audio
    f = open('temp_audio_list.txt', 'w')
    f.write("file 'silent_audio.mp3'\n")
    for audio_file in list_audio_file:
        f.write("file '" + audio_file + "'\n")
        f.write("file 'silent_audio.mp3'\n")
    f.close()
    # "ffmpeg -safe 0 -f concat -i list.txt -c copy output.mp4"
    cmd = "C:\\FFmpeg\\bin\\ffmpeg.exe -safe 0 -f concat -i temp_audio_list.txt " + out_path
    print(cmd)
    os.system(cmd)
    os.remove("temp_audio_list.txt")


def make_audio_sound(sub_string, media_file_name):
    response = requests.request('POST', url, data=sub_string.encode('utf-8'), headers=headers)
    if response.status_code == 200:
        video_link = ''
        count = 1
        is_get_link = True
        while video_link == '':
            time.sleep(5)
            try:
                video_link = json.loads(response.text)['async']
                if count == 13:
                    is_get_link = False
                    break
            except:
                count = count + 1
        if is_get_link is True:
            count = 0
            while count < 20:
                time.sleep(5)
                try:
                    urllib.request.urlretrieve(video_link, media_file_name)
                    break
                except:
                    count = count + 1
        else:
            print('Đã mất tiền nhưng không lấy được giọng đọc!')
    else:
        print('Có lỗi khi truy vấn đến FPT lấy giọng đọc! Check tiền xem còn không!')


def refactor_line(line):
    line = line.strip()
    line = line.replace('.', '')
    line = line + '.'
    return line + ' '


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


def convert_srt_to_sound_v2(sub_video_list, srt_file_name, video_name):
    # Remove before create audio
    dir = current_director_path.__str__() + "\\Temp_audio"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    srt_file_path = current_director_path.__str__() + "\\Input\\" + srt_file_name + ".srt"
    f = open(srt_file_path, 'r', encoding='utf-8')
    Lines = f.readlines()
    full_sub = []
    len_line = len(Lines)
    for i in range(len_line):
        try:
            if "00:" in Lines[i]:
                full_sub.append(refactor_line(Lines[i + 1]))
        except:
            pass
    f.close()
    raw_video_count = 0
    for i in range(len(sub_video_list)):
        if sub_video_list[i][2] == '1':
            sub = full_sub[i - raw_video_count]
            file_path = current_director_path.__str__() + "\\Temp_audio\\" + str(i + 1) + '.mp3'
            make_audio_sound(sub, file_path)
        elif sub_video_list[i][2] == '0':
            output_path = current_director_path.__str__() + "\\Temp_audio\\" + str(i + 1) + ".mp3"
            audio_effect.create_raw_video_sound(sub_video_list[i][0], sub_video_list[i][1], video_name, output_path)
            raw_video_count = raw_video_count + 1
    return srt_file_name


def convert_srt_to_sound(srt_file_name):
    full_sub = get_full_sub_in_srt_file(srt_file_name)
    text_file_path = current_director_path.__str__() + "\\Output\\" + srt_file_name + ".txt"
    f_w = open(text_file_path, 'w', encoding='utf-8')
    f_w.write(full_sub)
    f_w.close()
    chunk_audio_file_list = make_chunk_audio(srt_file_name, full_sub, 5000)
    concat_audio(chunk_audio_file_list, srt_file_name)
    for audio_chunk in chunk_audio_file_list:
        os.remove(audio_chunk)
    return srt_file_name


def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def make_chunk_audio(audio_name, full_sub, max_read):
    dot_occuren_list = findOccurrences(full_sub, '.')
    print(dot_occuren_list)
    chunk_audio_file_list = []
    if max(dot_occuren_list) <= max_read:
        file_name = audio_name + 'full.mp3'
        make_audio_sound(full_sub, file_name)
        chunk_audio_file_list.append(file_name)
    else:
        count = 0
        current_max = max_read
        max_read_list = []
        max_len = 0
        last_index = 0
        while True:
            for i in dot_occuren_list[max_len:]:
                if i <= current_max:
                    max_read_list.append(i)
            chunk_1 = full_sub[last_index:max_read_list[-1] + 1]
            file_name1 = audio_name + str(count) + '.mp3'
            make_audio_sound(chunk_1, file_name1)
            chunk_audio_file_list.append(file_name1)
            current_max = max_read_list[-1] + max_read
            if max(max_read_list) == max(dot_occuren_list):
                break
            count = count + 1
            max_len = dot_occuren_list.index(max_read_list[-1])
            last_index = max_read_list[-1] + 1
    return chunk_audio_file_list
