import tils
import pathlib
import os
import os.path

FFmpeg_path = "C:\\FFmpeg\\bin\\ffmpeg.exe"
current_director_path = pathlib.Path().resolve()


def split_video(video_name, sub_list):
    # Remove before create video
    dir = current_director_path.__str__() + "\\Temp_video"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    # split video
    video_duration_list = []
    INPUT_VIDEO_PATH = current_director_path.__str__() + "\\Input\\" + video_name + "_no_sound.mp4"
    last_to = ""
    count = 1
    for obj_sub in sub_list:
        if count == 1:
            ss = r"0:00:00.000"
        else:
            ss = last_to
        to = tils.rreplace(obj_sub[1], ":", ".", 1)
        output = current_director_path.__str__() + "\\Temp_video\\" + str(count) + ".mp4"
        CMD = FFmpeg_path + ' -i "' + INPUT_VIDEO_PATH + '" -ss ' + ss + ' -to ' + to + ' "' + output + '"'
        duration_video = tils.duration_by_milisecond(to) - tils.duration_by_milisecond(ss)
        video_duration_list.append(duration_video)
        count = count + 1
        last_to = to
        print(CMD)
        os.system(CMD)
    return video_duration_list


def smooth_video(ratio_list, duration_audio_list, duration_video_list):
    # Remove before create video
    dir = current_director_path.__str__() + "\\Temp_video_output"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    for i in range(len(ratio_list)):
        if float(ratio_list[i]) < 90:
            # Tinh toan thoi gian can phai cut
            delta_time = float(duration_video_list[i]) - float(duration_audio_list[i])
            cut_time = round(float(duration_video_list[i]) - delta_time * 2 / 3, 3)
            # Tinh toan speed can tang
            to = tils.convert_milisecond_to_time_v2(cut_time * 1000)[:-3]
            # cut video
            input_path = current_director_path.__str__() + "\\Temp_video\\" + str(i + 1) + ".mp4"
            output_temp1_path = current_director_path.__str__() + "\\Temp_video\\" + str(i + 1) + "temp1.mp4"
            temp2_output_path = current_director_path.__str__() + "\\Temp_video\\" + str(i + 1) + "temp2.mp4"
            # ffmpeg -sseof -600 -i input.mp4 -c copy output5.mp4
            cmd_cut_eof = FFmpeg_path + ' -i "' + input_path + '" -ss 0:00:00.000 -to ' + to + ' "' + output_temp1_path + '"'
            os.system(cmd_cut_eof)
            # thay doi toc do de dat duoc 90%
            video_duration = tils.get_video_duration(output_temp1_path)
            new_ratio = round(duration_audio_list[i] / video_duration * 100, 3)
            if new_ratio < 90:
                setpts = round((round(duration_audio_list[i] / 92, 3) * 100) /video_duration, 3)
                cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + output_temp1_path + '" -r 32 -filter:v "setpts=' + str(
                    setpts) + '*PTS" "' + temp2_output_path + '"'
                os.system(cmd)
            if os.path.exists(temp2_output_path):
                os.remove(input_path)
                os.rename(temp2_output_path, input_path)
                os.remove(output_temp1_path)
            else:
                os.remove(input_path)
                os.rename(output_temp1_path, input_path)
            # update lai ratio va duration video, audio
            duration_video_list[i] = tils.get_video_duration(input_path)
            ratio_list[i] = round(duration_audio_list[i] / duration_video_list[i] * 100, 3)
        if float(ratio_list[i]) >= 90 and float(ratio_list[i]) <= 100:
            # Tinh toan phan audio be hon va cong them khoang silence
            delta_time = round(float(duration_video_list[i]) - float(duration_audio_list[i]), 3)
            temp_audio_path = current_director_path.__str__() + "\\Temp_audio\\temp1.mp3"
            temp2_audio_path = current_director_path.__str__() + "\\Temp_audio\\temp2.mp3"
            cmd_create_silence = 'C:\\FFmpeg\\bin\\ffmpeg.exe -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t ' + str(
                delta_time) + ' "' + temp_audio_path + '"'
            os.system(cmd_create_silence)
            # concat silence audio va audio file de bang voi video file
            audio_path = current_director_path.__str__() + "\\Temp_audio\\A" + str(i + 1) + ".mp3"
            f = open('audiolist.txt', 'w')
            f.write("file '" + audio_path + "'\n")
            f.write("file '" + temp_audio_path + "'\n")
            f.close()
            audio_list_path = current_director_path.__str__() + "\\audiolist.txt"
            cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -safe 0 -f concat -i "' + audio_list_path + '" "' + temp2_audio_path + '"'
            os.system(cmd)
            # Remove temp file va doi ten temp2 thanh audio file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                os.remove(audio_path)
                os.rename(temp2_audio_path, audio_path)
    for i in range(len(ratio_list)):
        input_path = current_director_path.__str__() + "\\Temp_video\\" + str(i + 1) + ".mp4"
        output_video_path = current_director_path.__str__() + "\\Temp_video_output\\" + str(i + 1) + ".mp4"
        ratio = round(float(ratio_list[i]) / 100, 3)
        cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + input_path + '" -filter:v "setpts=' + str(
            ratio) + '*PTS" "' + output_video_path + '"'
        os.system(cmd)


def speed_up_down_sub_video(ratio_list, duration_audio_list):
    # Remove before create video
    dir = current_director_path.__str__() + "\\Temp_video_output"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    # change speed
    in_put_folder = current_director_path.__str__() + "\\Temp_video\\"
    out_put_folder = current_director_path.__str__() + "\\Temp_video_output\\"
    for i in range(len(ratio_list)):
        input_path = in_put_folder + str(i + 1) + ".mp4"
        input_audio_path = current_director_path.__str__() + "\\Temp_audio\\A" + str(i + 1) + ".mp3"
        output_video_path = out_put_folder + str(i + 1) + ".mp4"
        ratio = round(float(ratio_list[i]) / 100, 3)
        if ratio > 1:
            cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + input_path + '" -r 32 -filter:v "setpts=' + str(
                ratio) + '*PTS" "' + output_video_path + '"'
            os.system(cmd)
        else:
            # T
            cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + input_path + '" -i "' + input_audio_path + '" -filter_complex "[1:0]apad" -shortest "' + output_video_path + '"'
            os.system(cmd)


def concat_video_to_final(video_name):
    # remove current video before concat
    output_video_path = current_director_path.__str__() + "\\Output\\" + video_name + ".mp4"
    if os.path.exists(output_video_path):
        os.remove(output_video_path)

    # Concat video
    mypath = current_director_path.__str__() + "\\Temp_video_output"
    from os import walk

    filenames = next(walk(mypath), (None, None, []))[2]
    sorted_list = []
    for i in range(1, len(filenames) + 1):
        file_name = str(i) + ".mp4"
        sorted_list.append(file_name)
    print(sorted_list)
    f = open('mylist.txt', 'w')
    for file in sorted_list:
        file_path = current_director_path.__str__() + "\\Temp_video_output\\" + file
        line_fomat = "file '" + file_path + "'"
        f.write(line_fomat + "\n")
    f.close()
    mylist_path = current_director_path.__str__() + "\\mylist.txt"

    # "ffmpeg -safe 0 -f concat -i list.txt -c copy output.mp4"
    out_path = current_director_path.__str__() + "\\Output\\" + video_name + ".mp4"

    # cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -safe 0 -f concat -i "' + mylist_path + '" "' + out_path + '"'
    cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -safe 0 -f concat -i "' + mylist_path + '" -vf "setpts=N/30/TB" "' + out_path + '"'
    print(cmd)
    os.system(cmd)


def get_raw_video_v2(sub_list):
    last_sub_end = 0  # xác định thời gian của câu sub cuối cùng nhất
    temp_sub_list = []  # danh sách thời gian bắt đầu của các câu sub [,,'0']
    raw_video_index_list = []  # danh sách thời gian bắt đầu và kết thúc của các đoạn video gốc [,,'1']
    count = 0
    for sub in sub_list:
        delta_in_milisecond = tils.convert_time_to_milisecond(sub[0]) - last_sub_end
        if delta_in_milisecond >= 1500:  # nếu khoảng cách giữa 2 câu sub >= 1.5s thì sẽ con là 1 đoạn video gốc
            start_time = tils.convert_milisecond_to_time(last_sub_end + 1)
            end_time = tils.convert_milisecond_to_time(tils.convert_time_to_milisecond(sub[0]) - 1)
            raw_video_obj = [start_time[:-3], end_time[:-3], '0']
            temp_sub_list.append(raw_video_obj)
            temp_sub_list.append([sub[0], sub[1], '1'])
            raw_video_index_list.append(
                [count, round((delta_in_milisecond - 2) / 1000, 3),
                 tils.convert_milisecond_to_time(last_sub_end + 50)[:11],
                 tils.convert_milisecond_to_time(tils.convert_time_to_milisecond(sub[0]) - 50)[:11]])
            count = count + 2
        else:
            temp_sub_list.append([sub[0], sub[1], '1'])
            count = count + 1
        last_sub_end = tils.convert_time_to_milisecond(sub[1])
    return {'sub_video_list': temp_sub_list,
            'raw_video_index_list': raw_video_index_list
            }


def get_raw_video(sub_list):
    last_sub_end = 0
    temp_sub_list = []
    raw_video_index_list = []
    count = 0
    for sub in sub_list:
        delta_in_milisecond = tils.convert_time_to_milisecond(sub[0]) - last_sub_end
        if delta_in_milisecond >= 1500:
            start_time = tils.convert_milisecond_to_time(last_sub_end + 1)
            end_time = tils.convert_milisecond_to_time(tils.convert_time_to_milisecond(sub[0]) - 1)
            raw_video_obj = [start_time, end_time]
            temp_sub_list.append(raw_video_obj)
            temp_sub_list.append(sub)
            raw_video_index_list.append(
                [count, round((delta_in_milisecond - 2) / 1000, 3),
                 tils.convert_milisecond_to_time(last_sub_end + 50)[:11],
                 tils.convert_milisecond_to_time(tils.convert_time_to_milisecond(sub[0]) - 50)[:11]])
            count = count + 2
        else:
            temp_sub_list.append(sub)
            count = count + 1
        last_sub_end = tils.convert_time_to_milisecond(sub[1])
    return {'sub_video_list': temp_sub_list,
            'raw_video_index_list': raw_video_index_list
            }


def create_no_sound_video(video_name):
    # remove current video before concat
    output_video_path = current_director_path.__str__() + "\\Input\\" + video_name + "_no_sound.mp4"
    if os.path.exists(output_video_path):
        os.remove(output_video_path)

    # create video with no sound
    video_path = current_director_path.__str__() + "\\Input\\" + video_name + ".mp4"
    out_path = current_director_path.__str__() + "\\Input\\" + video_name + "_no_sound.mp4"
    cmd = 'C:\\FFmpeg\\bin\\ffmpeg.exe -i "' + video_path + '" -c copy -an "' + out_path + '"'
    os.system(cmd)
