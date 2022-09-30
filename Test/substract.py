from datetime import datetime

s1 = '0:00:04.022'
s2 = '0:00:00.100'  # for example
format = '%H:%M:%S.%f'
time = datetime.strptime(s1, format) - datetime.strptime(s2, format)
print(time)
