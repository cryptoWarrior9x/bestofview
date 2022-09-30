import requests

USER_TOKEN = ''
voice_login_url = 'https://api.voiceovermaker.io/login'
data = {"email": "huyentrang1375@gmail.com", "password": "huynhduc95"}
response = requests.request('GET', voice_login_url, data=data.encode(),
                            headers={'content-type': 'application/json;charset=UTF-8'})
print(response)
