import pathlib
import video_effect
import audio_effect
import tils
import viettel_sound_ai
import voiceovermaker_api
import os
import traceback
import logging
# import google_drive_api
import fpt_sound_ai_v2

current_director_path = pathlib.Path().resolve()

'''
HƯỚNG DẪN SỬ DỤNG:
B1: Tải video từ ixigua
B2: Cho video và file sub .srt vào thư mục Input. 
CHÚ Ý: 
 + Đặt tên file không có dấu và nối với nhau bởi dấu "_"
 + Tên file sub: <tên video>-<language_code>.txt
B3: Điền thông tin tham số:
    + video_name: tên video
B4: Chạy review việt:
    + Click chuột phải.
    + Chọn "Run Main"
Sau khi chạy xong, hệ thống sẽ báo "HOANH THANH VIDEO: <tên video>". Khi đó, trong thư mục Output sẽ có 3 file:
    + <tên video>.mp3
    + <tên video>.mp4
    + <tên video>.txt
Tiếp theo chạy review ngoại.
B5: Từ file <tên video>.txt trong thư mục Output. Sử dụng google dịch để tạo ra bản dịch nước muốn làm. Sau đó,
lưu file vào trong thư mục Input với tên: <tên video>_<language_code>.txt
B6: Điền thông tin tham số:
    + language_code: vi-vi(Việt Nam), es-mx(mexico), en-us(Tiếng Anh), tr-tr(Thổ Nhỹ Kỳ), th-th(Thái Lan), pt-br(Brazil)
                    ar-eg (Ai Cập), hi-in (Ấn Độ)
'''

# Tham số xác định tên. video và file sub dành cho sub việt
###################################################
###################################################
video_list = {
    'black_sheep': ['id-id'],
}

editor_list = ['van', 'tra_my', 'anh_tram']
DATE = '14/7'

###################################################
###################################################

DRIVER_FOLDER = {
    'van': '1qPoKVRX8omVxxgmu6eTXSSfyJ3FoqxUM',
    'tra_my': '1zuSrx9xwmSVepLfetKyLOdHYZvdyTcAz',
    'anh_tram': '1gytlFMgcVHCseo1CnCno89hbs-6la57p'
}


###################################################
###################################################

def auto_review(video_name, language_Code, subtitle_name, is_loop=False):
    try:
        # Bước 0: Tạo subtitle cho nước muốn làm. Sử dụng google dịch.
        # tils.create_foreign_subfile(video_name, language_Code)
        # Buoc 1:  Tu danh sach images, lay thong tin thoi gian xuat hien cua cac cau Sub
        # Sau do luu vao sub_list = [[start_time, end_time], [start_time, end_time], ...] vd = [[00:00:00:000,00:00:03:160]]
        sub_list = tils.get_sub_by_srt_file(video_name + '-vi-vi' + '.srt')
        sub_video_list = video_effect.get_raw_video_v2(sub_list)
        # Buoc 0: Tao giong doc cho video tu file sub
        if language_Code == 'vi-vi':
            audio_name = fpt_sound_ai_v2.text_to_speech(sub_video_list['sub_video_list'], subtitle_name,
                                                        video_name)
            # audio_name = "nu_xa-vi-vi"
        else:
            # Tu file dich tu viet nam sang ngoai de lay giong doc tuong ung. audio_name la ten_phim_language_code
            audio_name = voiceovermaker_api.text_to_speech_v2(language_Code, sub_video_list['sub_video_list'],
                                                              subtitle_name, video_name)
            # audio_name = "she_hulk-es-mx"
        # Tao video khong co am thanh. De ghep video sau khi tang/giam speed ko bi loi
        if is_loop is False:
            video_effect.create_no_sound_video(video_name)

        # Buoc 2: Cat video thanh nhung video nho tuong ung voi tung cau sub trong sub_list
        if is_loop is False:
            video_effect.split_video(video_name, sub_video_list['sub_video_list'])

        # Buoc: Cắt phần ko nói đầu và cuối mỗi audio.

        dir = current_director_path.__str__() + "\\Temp_audio"
        audio_list = os.listdir(dir)
        if language_Code == "tl-tl":
            for i in range(len(audio_list)):
                if 'A' in audio_list[i]:
                    break
                file_path = dir + '\\' + audio_list[i]
                new_file_path = dir + '\\A' + audio_list[i]
                os.rename(file_path, new_file_path)
        else:
            for f in audio_list:
                if 'A' in f:
                    break
                audio_effect.trim_silence_sound(dir + '\\' + f, language_Code)

        # Buoc 4: Lay dach sach audio va video sau khi da tach ra
        DURATION_VIDEO_LIST = tils.get_length('in', 'video')
        DURATION_AUDIO_LIST = tils.get_length('in', 'audio')

        # Buoc phu: Kiem tra xem chenh lech giua video va audio sau khi cat la bao nhieu. De xac dinh muc do tang/giam
        # video tuong ung --> Lam cho video muot hon
        ratio_video_audio_list = []
        for i in range(len(DURATION_VIDEO_LIST)):
            ratio_video_audio_list.append(round(DURATION_AUDIO_LIST[i] / DURATION_VIDEO_LIST[i] * 100, 3))

        # Bước phụ: Xử lý những đoạn sub ngắn dưới 80%
        video_effect.smooth_video(ratio_video_audio_list, DURATION_AUDIO_LIST, DURATION_VIDEO_LIST)
        # Buoc 5: Ghep video va audio sau khi da change speed
        audio_effect.concet_audio_files(audio_name)
        video_output_name = video_name + '-' + language_Code
        video_effect.concat_video_to_final(video_output_name)
        return True
    except Exception as e:
        logging.error(traceback.format_exc())
        return False


def main():
    results_list = []
    for video_name in video_list.keys():
        is_loop = False
        for language in video_list[video_name]:
            video_path = current_director_path.__str__() + "\\Output\\" + video_name + "-" + language + ".mp4"
            if os.path.exists(video_path):
                continue
            else:
                subtitle_name = video_name + "-" + language
                result = auto_review(video_name, language, subtitle_name, is_loop)
                if result is False:
                    video_result = {'video_name': video_name + "-" + language,
                                    'result': 'ERROR'}
                    results_list.append(video_result)
                    break
                else:
                    video_result = {'video_name': video_name + "-" + language,
                                    'result': 'Success'}
                    results_list.append(video_result)
                    is_loop = True
    '''
    output_path = current_director_path.__str__() + "\\Output\\"
    folder_id = google_drive_api.create_folder(DATE, DRIVER_FOLDER[editor_list[0]])
    list_video_success = []
    for video in results_list:
        if video['result'] == 'Success':
            list_video_success.append(video['video_name'])
    google_drive_api.upload_media_to_driver(output_path, list_video_success, folder_id)
    '''
    print("KET QUA CHAY TOOL:")
    for video in results_list:
        print(video['video_name'] + ': ' + video['result'])


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
