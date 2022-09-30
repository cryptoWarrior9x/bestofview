import requests
import urllib.request
import json
import time

url = 'https://api.fpt.ai/hmi/tts/v5'

headers = {
    'api-key': 'aDe98pap3GlCkTHYX9HsyxM5qhjWglWG',
    'speed': '1.1',
    'voice': 'banmai'
}


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


make_audio_sound('Xà yêu tu luyện nghìn năm đang tắm rửa.',
                 'C:\\Users\\ADMIN\\PycharmProjects\\AutoReview\\Temp_audio\\EE.mp3')
