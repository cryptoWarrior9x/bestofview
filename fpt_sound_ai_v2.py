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
            temp_path = current_director_path.__str__() + "\\Temp_audio\\temp.mp3"
            make_audio_sound(sub, temp_path)
            audio_effect.speed_up_audio(temp_path, file_path)
            # remove temp audio before create new one
            temp_audio_path = current_director_path.__str__() + "\\Temp_audio\\temp.mp3"
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
        elif sub_video_list[i][2] == '0':
            output_path = current_director_path.__str__() + "\\Temp_audio\\" + str(i + 1) + ".mp3"
            audio_effect.create_raw_video_sound(sub_video_list[i][0], sub_video_list[i][1], video_name, output_path)
            raw_video_count = raw_video_count + 1
    f_read.close()
    return subfile_name

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
                time.sleep(2)
                try:
                    urllib.request.urlretrieve(video_link, media_file_name)
                    break
                except:
                    count = count + 1
        else:
            print('Đã mất tiền nhưng không lấy được giọng đọc!')
    else:
        print('Có lỗi khi truy vấn đến FPT lấy giọng đọc! Check tiền xem còn không!')