import json
import requests

url = "https://viettelgroup.ai/voice/api/tts/v1/rest/syn"
data = {"text": "Người Wegmi châu Phi sẽ kết hôn khi lên 9 tuổi, và họ có thể tinh tường phát hiện những con ong bay cách xa hơn chục mét.", "voice": "doanngocle", "id": "2", "without_filter": False, "speed": 1.0, "tts_return_option": 2}
headers = {'Content-type': 'application/json', 'token': '7SZmwcNcDUXXYst4BNT0mZ0hUhtuTMb-rxPy18h-UUDaN6IX2KOSmAAEFHRWNv48'}
response = requests.post(url, data=json.dumps(data), headers=headers)
#if encounter SSL error because of https certificate, please comment out above line and use the line below to  make insecure connections   (this will expose your application to security risks, such as man-in-the-middle attacks.)
#response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
# Headers is a dictionary
print(response.headers)
# Get status_code.
print(response.status_code)
# Get the response data as a python object.
data = response.content
f = open("viettel.mp3", "wb")
f.write(data)
f.close()