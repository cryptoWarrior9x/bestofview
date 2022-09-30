import pathlib

current_director_path = pathlib.Path().resolve()
import googletrans
from googletrans import Translator


def create_foreign_subtitle():
    sub_path = current_director_path.__str__() + '\\vietsub.txt'
    translator = Translator()
    file = open(sub_path, 'r', encoding='utf-8')
    f = open('transalated.txt', 'w', encoding='utf-8')
    lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i].strip()
        if line[-1] is not '.':
            line = line + '.'
        translated = translator.translate(line, src='vi', dest='ar')
        f.write(translated.text + '\n')
    file.close()
    f.close()

create_foreign_subtitle()