import fpt_sound_api
import pathlib

vietsub = 'ke_san_lung'
foreignsub = 'ke_san_lung_en-us'

current_director_path = pathlib.Path().resolve()


def refactor_line(line):
    line = line.strip()
    if line[-1] != ',' and line[-1] != '.':
        last_charac = '.'
    else:
        last_charac = line[-1]
    line = line.replace('.', '')
    line = line.replace(',', '')
    line = line + last_charac
    return line + ' '


def get_full_sub_in_srt_file(srt_file_name):
    srt_file_path = current_director_path.__str__() + "\\Input\\" + srt_file_name + ".srt"
    f = open(srt_file_path, 'r', encoding='utf-8')
    Lines = f.readlines()
    full_sub = ''
    len_line = len(Lines)
    for i in range(len_line):
        try:
            if "00:" in Lines[i]:
                full_sub = full_sub + refactor_line(Lines[i + 1])
        except:
            pass
    f.close()
    return full_sub


def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def refactor_subfile(foreign_subfile_name, subtitle_name):
    full_vietsub = get_full_sub_in_srt_file(subtitle_name)
    foreign_subfile_path = current_director_path.__str__() + "\\Input\\" + foreign_subfile_name + ".txt"
    fr = open(foreign_subfile_path, 'r', encoding='utf-8')
    lines = fr.readlines()
    fw = open('check_spell.txt', 'w', encoding='utf-8')
    full_foreignsub = ''
    for line in lines:
        full_foreignsub = full_foreignsub + line
    dot_vietsub_list = findOccurrences(full_vietsub, '.')
    dot_foreignsub_list = findOccurrences(full_foreignsub, '.')
    count = 0
    for i in range(min(len(dot_vietsub_list), len(dot_foreignsub_list))):
        if count == 0:
            vietsub_chunk = full_vietsub[0:dot_vietsub_list[i]]
            foreignsub_chunk = full_foreignsub[0:dot_foreignsub_list[i]]
            comma_list_vietsub = findOccurrences(vietsub_chunk, ',')
            comma_list_foreignsub = findOccurrences(foreignsub_chunk, ',')
            if len(comma_list_foreignsub) != len(comma_list_vietsub):
                fw.write(vietsub_chunk)
            count = count + 1
        else:
            vietsub_chunk = full_vietsub[dot_vietsub_list[i-1] + 1:dot_vietsub_list[i]]
            foreignsub_chunk = full_foreignsub[dot_foreignsub_list[i-1] + 1:dot_foreignsub_list[i]]
            comma_list_vietsub = findOccurrences(vietsub_chunk, ',')
            comma_list_foreignsub = findOccurrences(foreignsub_chunk, ',')
            if len(comma_list_foreignsub) != len(comma_list_vietsub):
                fw.write(vietsub_chunk + '\n')
    fr.close()
    fw.close()


def main():
    refactor_subfile(foreignsub, vietsub)


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
