import requests
import json
import pathlib
import os
import os.path
import audio_effect

current_director_path = pathlib.Path().resolve()


def text_to_speech(sub_video_list, subfile_name, video_name):
    # Remove before create audio
    dir = current_director_path.__str__() + "\\Temp_audio"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    # Lay toan bo sub vao mot string full_sub
    subfile_path = current_director_path.__str__() + '\\Input\\' + subfile_name + '.txt'
    f_read = open(subfile_path, 'r', encoding='utf-8')
    Lines = f_read.readlines()
    raw_video_count = 0
    for i in range(len(sub_video_list)):
        if sub_video_list[i][2] == '1':
            sub = Lines[i - raw_video_count]
            file_path = current_director_path.__str__() + "\\Temp_audio\\" + str(i + 1) + '.mp3'
            file_name = str(i + 1) + '.mp3'
            get_voice(sub, file_path, file_name)
        elif sub_video_list[i][2] == '0':
            output_path = current_director_path.__str__() + "\\Temp_audio\\" + str(i + 1) + ".mp3"
            audio_effect.create_raw_video_sound(sub_video_list[i][0], sub_video_list[i][1], video_name, output_path)
            raw_video_count = raw_video_count + 1
    f_read.close()
    return subfile_name


def get_voice(sub, output_path, file_name):
    url = "https://viettelgroup.ai/voice/api/tts/v1/rest/syn"
    headers = {'Content-type': 'application/json',
               'token': '7SZmwcNcDUXXYst4BNT0mZ0hUhtuTMb-rxPy18h-UUDaN6IX2KOSmAAEFHRWNv48'}
    data = {"text": sub, "voice": "doanngocle", "id": "2", "without_filter": False, "speed": 1.0,
            "tts_return_option": 2}
    while True:
        voice_ok = False
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(data))
            resp.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(resp.content)
            dir = current_director_path.__str__() + "\\Temp_audio"
            for f in os.listdir(dir):
                if f == file_name:
                    voice_ok = True
        except:
            pass
        if voice_ok == True:
            break
