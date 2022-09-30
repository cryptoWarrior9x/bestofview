from math import floor

editor_list = ['Van', 'Tra My', 'Anh Tram']
video_result_list = [
    {'video_name': '1',
     'result': 'SUCCESS'},
    {'video_name': '2',
     'result': 'SUCCESS'},
    {'video_name': '3',
     'result': 'SUCCESS'},
    {'video_name': '4',
     'result': 'SUCCESS'},
    {'video_name': '5',
     'result': 'SUCCESS'},
    {'video_name': '6',
     'result': 'SUCCESS'},
    {'video_name': '7',
     'result': 'SUCCESS'},
    {'video_name': '1',
     'result': 'SUCCESS'},
    {'video_name': '2',
     'result': 'SUCCESS'},
    {'video_name': '3',
     'result': 'SUCCESS'},
    {'video_name': '4',
     'result': 'SUCCESS'},
    {'video_name': '5',
     'result': 'SUCCESS'},
    {'video_name': '6',
     'result': 'SUCCESS'},
    {'video_name': '7',
     'result': 'SUCCESS'},
]

list_of_success = []
for video in video_result_list:
    if video['result'] == 'SUCCESS':
        list_of_success.append(video)
chunk_size = floor(len(list_of_success) / 3)
chunked_list = [list_of_success[i:i + chunk_size] for i in range(0, len(list_of_success), chunk_size)]
print(chunked_list)

result = {}
for i in range(len(editor_list)):
    result[editor_list[i]] = chunked_list[i]
    if i == len(editor_list) - 1:
        for video in chunked_list[-1]:
            result[editor_list[i]].append(video)

print(result)
