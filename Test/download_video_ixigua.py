import base64
import json
import os
import re
import pathlib

import requests


class XGSP:
    main_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55'
    }

    video_headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'origin': 'https://www.ixigua.com',
        'referer': 'https://www.ixigua.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57'
    }

    def __init__(self, s_url):
        self.url = s_url
        self.path = pathlib.Path().resolve()

    def XGSP_download(self):
        r = requests.get(self.url, headers=self.main_headers)
        r.encoding = 'utf-8'
        video_info = (re.findall('"packerData":{"video":(.*?)}},"', r.text)[0] + "}}}}").Replace("undefined",
                                                                                                     '"undefined"')
        video_json = json.loads(video_info)
        video_name = video_json["title"].replace("|", "-").replace(" ", "")
        print("Video name: " + video_name)
        video_url = base64.b64decode(
            video_json['videoResource']['dash']['dynamic_video']['dynamic_video_list'][1]['main_url']).decode('utf-8')
        print("Video link: " + video_url)
        audio_url = base64.b64decode(
            video_json['videoResource']['dash']['dynamic_video']['dynamic_audio_list'][1]['main_url']).decode('utf-8')
        print('Audio link: ' + audio_url)
        with open(self.path + video_name + ".flv", 'wb') as f:
            f.write(requests.get(video_url, headers=self.video_headers).content)
            print("Video file download complete...")
        with open(self.path + video_name + "-1.flv", "wb") as f:
            f.write(requests.get(audio_url, headers=self.video_headers).content)
            print("Audio and video are downloaded, about to start splicing...")
        self.video_add_mp3("C:\\FFmpeg\\bin\\ffmpeg.exe", self.path, self.path + video_name + ".flv", self.path
                           + video_name + "-1.flv")

    def video_add_mp3(self, ffmpeg_path, save_path, file1_path, file2_path):
        mp4_name = file1_path.split('/')[-1].split('.')[0] + '-temp.mp4'
        mp3_name = file1_path.split('/')[-1].split('.')[0] + '-temp.mp3'
        outfile_name = file1_path.split('.')[0] + '.mp4'
        os.system(r'%sffmpeg -i %s %s' % (ffmpeg_path, file1_path, save_path + mp4_name))
        os.system(r'%sffmpeg -i %s -i %s -c:v copy -c:a copy %s' % (
            ffmpeg_path, save_path + mp4_name, save_path + mp3_name, outfile_name))
        os.remove(save_path + mp4_name)
        os.remove(save_path + mp3_name)
        os.remove(file1_path)
        os.remove(file2_path)


xg = XGSP('https://www.ixigua.com/7124738484153090567')
xg.XGSP_download()
