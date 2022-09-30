import requests
from requests.structures import CaseInsensitiveDict
import json

url = "https://api.voiceovermaker.io/login"

es_MX_Dalia_ID = '{"DisplayName":"Dalia","LocalName":"Dalia","ShortName":"es-MX-DaliaNeural","Gender":"Female","Locale":"es-MX","SampleRateHertz":"24000","VoiceType":"Neural","Status":"GA","languageName":"Spanish (es-MX, Female, Neural) - Dalia","pvr":"m"}'
fil_PH_A = '{"languageCodes":["fil-PH"],"name":"fil-PH-Wavenet-A","ssmlGender":"FEMALE","naturalSampleRateHertz":24000,"languageName":"Filipino (fil-PH, Female, Neural) - A","pvr":"g","neural":true,"internalId":"56717faf9ec302dff0070778dadd5a41","locale":"fil-PH"}'

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


def get_voice(data, token, voice_id):
    url = "https://api.voiceovermaker.io/create_voice"
    headers = CaseInsensitiveDict()
    headers["x-auth"] = "Bearer " + token
    headers["content-type"] = "application/json;charset=UTF-8"
    data = '{"pitch":0,"returnRawFile":true,"speakingRate":1.00,"text":"' + data + '","speech":' + voice_id + '}'
    resp = requests.post(url, headers=headers, data=data)
    resp.raise_for_status()
    with open("audio.mp3", "wb") as f:
        f.write(resp.content)
    print('xxx')


token = get_token()
data = 'Ang mangangaso ng ahas ng Aprika ay kumikilos na parang diyos para hulihin ang isang 7 metrong haba ng sawa, isang balat ng sawa na sapat para sa isang taon na pamumuhay'
x = get_voice(data, token, fil_PH_A)
