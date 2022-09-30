import requests
from requests.structures import CaseInsensitiveDict
import json
import pathlib
import os
import fpt_sound_api
import audio_effect

url = "https://api.voiceovermaker.io/login"
current_director_path = pathlib.Path().resolve()

# Mexico
es_MX_Dalia_ID = {"DisplayName": "Dalia", "LocalName": "Dalia", "ShortName": "es-MX-DaliaNeural", "Gender": "Female",
                  "Locale": "es-MX", "SampleRateHertz": "24000", "VoiceType": "Neural", "Status": "GA",
                  "languageName": "Spanish (es-MX, Female, Neural) - Dalia", "pvr": "m"}
# English
en_US_Elizabeth = {"DisplayName": "Elizabeth", "LocalName": "Elizabeth", "ShortName": "en-US-ElizabethNeural",
                   "Gender": "Female", "Locale": "en-US", "SampleRateHertz": "24000", "VoiceType": "Neural",
                   "Status": "GA", "languageName": "English (en-US, Female, Neural) - Elizabeth", "pvr": "m"}

en_US_Aria = {"DisplayName": "Aria", "LocalName": "Aria", "ShortName": "en-US-AriaNeural", "Gender": "Female",
              "Locale": "en-US",
              "StyleList": ["chat", "customerservice", "narration-professional", "newscast-casual", "newscast-formal",
                            "cheerful", "empathetic"], "SampleRateHertz": "24000", "VoiceType": "Neural",
              "Status": "GA", "languageName": "English (en-US, Female, Neural) - Aria", "pvr": "m"}

# Turkey
tr_TR_Emel = {"DisplayName": "Emel", "LocalName": "Emel", "ShortName": "tr-TR-EmelNeural", "Gender": "Female",
              "Locale": "tr-TR", "SampleRateHertz": "24000", "VoiceType": "Neural", "Status": "GA",
              "languageName": "Turkish (tr-TR, Female, Neural) - Emel", "pvr": "m"}
# Thailand
th_TH_Premwadee = {"DisplayName": "Premwadee", "ShortName": "th-TH-PremwadeeNeural", "Gender": "Female",
                   "Locale": "th-TH", "SampleRateHertz": "24000", "VoiceType": "Neural", "Status": "GA",
                   "languageName": "Thai (th-TH, Female, Neural) - Premwadee", "pvr": "m"}
# Indonesia
id_ID_Wavenet_A = {"languageCodes": ["id-ID"], "name": "id-ID-Wavenet-A", "ssmlGender": "FEMALE",
                   "naturalSampleRateHertz": "24000", "languageName": "Indonesian (id-ID, Female, Neural) - A",
                   "pvr": "g"}

# Brazil
pt_Br_Francisca = {"DisplayName": "Francisca", "LocalName": "Francisca", "ShortName": "pt-BR-FranciscaNeural",
                   "Gender": "Female",
                   "Locale": "pt-BR", "LocaleName": "Portuguese (Brazil)", "StyleList": ["calm"],
                   "SampleRateHertz": "24000",
                   "VoiceType": "Neural", "Status": "GA",
                   "languageName": "Portuguese (pt-BR, Female, Neural) - Francisca",
                   "pvr": "m"}

# Philippine Filipino
tl_PH_A = {"languageCodes": ["fil-PH"], "name": "fil-PH-Wavenet-A", "ssmlGender": "FEMALE",
           "naturalSampleRateHertz": "24000", "languageName": "Filipino (fil-PH, Female, Neural) - A", "pvr": "g",
           "neural": "true", "internalId": "56717faf9ec302dff0070778dadd5a41", "locale": "fil-PH"}

# An Do hindi
hi_IN_Swara = {"DisplayName": "Swara", "LocalName": "\u0938\u094d\u0935\u0930\u093e", "ShortName": "hi-IN-SwaraNeural",
               "Gender": "Female", "Locale": "hi-IN", "LocaleName": "Hindi (India)", "SampleRateHertz": "24000",
               "VoiceType": "Neural", "Status": "GA", "WordsPerMinute": "117",
               "languageName": "Hindi (hi-IN, Female, Neural) - Swara", "pvr": "m"}

# Egypt Arabic
ar_EG_salma = {"DisplayName": "Salma", "LocalName": "\u0633\u0644\u0645\u0649", "ShortName": "ar-EG-SalmaNeural",
               "Gender": "Female", "Locale": "ar-EG", "LocaleName": "Arabic (Egypt)", "SampleRateHertz": "24000",
               "VoiceType": "Neural", "Status": "GA", "WordsPerMinute": "103",
               "languageName": "Arabic (ar-EG, Female, Neural) - Salma", "pvr": "m"}


def get_token():
    headers = CaseInsensitiveDict()
    headers["content-type"] = "application/json;charset=UTF-8"
    data = '{"email":"duclh1312@gmail.com","password":"KieuSoa@)22"}'
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code == 200:
        token_json = json.loads(resp.text)
    return token_json['token']


def get_all_voice(token):
    url = "https://api.voiceovermaker.io/list_voices"
    headers = CaseInsensitiveDict()
    headers["x-auth"] = "Bearer " + token
    resp = requests.get(url, headers=headers)
    print(resp.status_code)


def get_voice(datax, token, voice_id, file_path, file_name):
    url = "https://api.voiceovermaker.io/create_voice"
    headers = CaseInsensitiveDict()
    headers["x-auth"] = "Bearer " + token
    headers["content-type"] = "application/json;charset=UTF-8"
    data = {"pitch": 0, "returnRawFile": 'true', "speakingRate": 1.00, "text": datax, "speech": voice_id}
    while True:
        voice_ok = False
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(data))
            resp.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(resp.content)
            dir = current_director_path.__str__() + "\\Temp_audio"
            for f in os.listdir(dir):
                if f == file_name:
                    voice_ok = True
        except:
            pass
        if voice_ok == True:
            break


# data = "Perselingkuhan sang istri dengan saudara suami"
# token = get_token()
# get_all_voice(token)
# voice_id = id_ID_Wavenet_A
# get_voice(data, token, voice_id, 'hiihi.mp3')


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
    os.system(cmd)
    os.remove("temp_audio_list.txt")


def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def make_chunk_audio(audio_name, language_code, full_sub, max_read, token):
    voice_id = ''
    if language_code == 'es-mx':  # Tieng Tay Ban Nha
        voice_id = es_MX_Dalia_ID
    elif language_code == 'en-us':  # Tieng Anh
        voice_id = en_US_Aria
    elif language_code == 'tr-tr':  # Tieng Tho Nhy Ky
        voice_id = tr_TR_Emel
    elif language_code == 'th-th':  # Tieng Thai
        voice_id = th_TH_Premwadee
    elif language_code == 'id-id':  # Tieng Indo
        voice_id = id_ID_Wavenet_A
    elif language_code == 'tl-tl':  # Tieng Philippine
        voice_id = tl_PH_A
    elif language_code == 'pt-br':
        voice_id = pt_Br_Francisca
    dot_occuren_list = []
    if language_code == 'th-th':
        dot_occuren_list = findOccurrences(full_sub, '\n')
    else:
        dot_occuren_list = findOccurrences(full_sub, '.')
    chunk_audio_file_list = []
    if max(dot_occuren_list) <= max_read:
        file_name = audio_name + 'full.mp3'
        get_voice(full_sub, token, voice_id, file_name)
        chunk_audio_file_list.append(file_name)
    else:
        max_read_list = []
        for i in dot_occuren_list:
            if i <= max_read:
                max_read_list.append(i)
        chunk_1 = full_sub[:max_read_list[-1] + 1]
        file_name1 = audio_name + '1.mp3'
        get_voice(chunk_1, token, voice_id, file_name1)
        chunk_audio_file_list.append(file_name1)

        chunk_2 = full_sub[max_read_list[-1] + 1:]
        file_name2 = audio_name + '2.mp3'
        get_voice(chunk_2, token, voice_id, file_name2)
        chunk_audio_file_list.append(file_name2)
    return chunk_audio_file_list


def text_to_speech(language_code, foreign_subfile_name):
    # Lay token cua tai khoan voiceovermaker
    token = get_token()
    # Lay toan bo sub vao mot string full_sub
    subfile_path = current_director_path.__str__() + '\\Input\\' + foreign_subfile_name + '.txt'
    f_read = open(subfile_path, 'r', encoding='utf-8')
    Lines = f_read.readlines()
    full_sub = ''
    for line in Lines:
        full_sub = full_sub + line
    f_read.close()
    # Tach full_sub ra thanh tung doan va goi den API de tao giong doc
    chunk_audio_file_list = make_chunk_audio(foreign_subfile_name, language_code, full_sub, 8000, token)
    # Sau khi tao xong thi noi cac file giong doc lai voi nhau
    concat_audio(chunk_audio_file_list, foreign_subfile_name)
    # Xoa cac file giong doc nho sau khi noi xong
    for audio_chunk in chunk_audio_file_list:
        os.remove(audio_chunk)
    return foreign_subfile_name


def text_to_speech_v2(language_code, sub_video_list, foreign_subfile_name, video_name):
    # Remove before create audio
    dir = current_director_path.__str__() + "\\Temp_audio"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    # get voice_id
    voice_id = ''
    if language_code == 'es-mx':  # Tieng Tay Ban Nha
        voice_id = es_MX_Dalia_ID
    elif language_code == 'en-us':  # Tieng Anh
        voice_id = en_US_Aria
    elif language_code == 'tr-tr':  # Tieng Tho Nhy Ky
        voice_id = tr_TR_Emel
    elif language_code == 'th-th':  # Tieng Thai
        voice_id = th_TH_Premwadee
    elif language_code == 'tl-tl':  # Tieng Philippine
        voice_id = tl_PH_A
    elif language_code == 'id-id':  # Tieng Indo
        voice_id = id_ID_Wavenet_A
    elif language_code == 'pt-br':  # Brazil
        voice_id = pt_Br_Francisca
    elif language_code == 'hi-in':  # An Do
        voice_id = hi_IN_Swara
    elif language_code == 'ar-eg':  # Egypt
        voice_id = ar_EG_salma
    # Lay token cua tai khoan voiceovermaker
    token = get_token()
    # Lay toan bo sub vao mot string full_sub
    subfile_path = current_director_path.__str__() + '\\Input\\' + foreign_subfile_name + '.txt'
    f_read = open(subfile_path, 'r', encoding='utf-8')
    Lines = f_read.readlines()
    raw_video_count = 0
    for i in range(len(sub_video_list)):
        if sub_video_list[i][2] == '1':
            sub = Lines[i - raw_video_count]
            file_path = current_director_path.__str__() + "\\Temp_audio\\" + str(i + 1) + '.mp3'
            temp_path = current_director_path.__str__() + "\\Temp_audio\\temp.mp3"
            temp_file = "temp.mp3"
            get_voice(sub, token, voice_id, temp_path, temp_file)
            audio_effect.speed_up_audio(temp_path, file_path)
            # remove temp audio before create new one
            if os.path.exists(temp_path):
                os.remove(temp_path)
        elif sub_video_list[i][2] == '0':
            output_path = current_director_path.__str__() + "\\Temp_audio\\" + str(i + 1) + ".mp3"
            audio_effect.create_raw_video_sound(sub_video_list[i][0], sub_video_list[i][1], video_name, output_path)
            raw_video_count = raw_video_count + 1
    f_read.close()
    return foreign_subfile_name
