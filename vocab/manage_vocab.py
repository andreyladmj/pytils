import json
import random
import time

import PySimpleGUI as sg

sg.theme('DarkAmber')

with open("vocab.json", encoding="utf8") as f:
    words = json.loads(f.read())

def get_word(selected_word):
    with open("vocab.json", encoding="utf8") as f:
        words = json.loads(f.read())

    for i in range(len(words)):
        if words[i]['word_eng'] == selected_word:
            return words[i]

def add_word(selected_word):
    with open("vocab.json", encoding="utf8") as f:
        words = json.loads(f.read())

    words.append(selected_word)

    with open("vocab.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(words, ensure_ascii=False))

def update_word(current_word):
    with open("vocab.json", encoding="utf8") as f:
        words = json.loads(f.read())

    for i in range(len(words)):
        if words[i]['word_eng'] == current_word:
            words[i].update(current_word)
            break

    with open("vocab.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(words, ensure_ascii=False))


layout = []
combobox = sg.InputCombo(values=[word['word_eng'] for word in words], size=(20,1), key='selected_word')
layout.append([sg.Text("Words"), combobox, sg.Button('Select')])
layout.append([sg.Text('Word eng:'), sg.InputText(key='word_eng')])
layout.append([sg.Text('Word esp:'), sg.InputText(key='word_esp')])
layout.append([sg.Text('Sentence eng:'), sg.InputText(key='sentence_eng')])
layout.append([sg.Text('Sentence rus:'), sg.InputText(key='sentence_rus')])
layout.append([sg.Button('Add'), sg.Button('Update')])

# for word in words:
#     layout.append([sg.Text(word['word_eng']), sg.Button('Select')])

window = sg.Window('Vocabulary', layout, finalize=True)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Select':
        word = get_word(values['selected_word'])
        window['word_eng'].update(word.get('word_eng', ""))
        window['word_esp'].update(word.get('word_esp', ""))
        window['sentence_eng'].update(word.get('sentence_eng', ""))
        window['sentence_rus'].update(word.get('sentence_rus', ""))
    elif event == 'Add':
        new_word = {
            "word_eng": values['word_eng'],
            "word_esp": values['word_esp'],
            "sentence_eng": values['sentence_eng'],
            "sentence_rus": values['sentence_rus'],
            "showed": 0,
            "correct": 0,
        }
        add_word(new_word)
    elif event == 'Update':
        current_word = {
            "word_eng": values['word_eng'],
            "word_esp": values['word_esp'],
            "sentence_eng": values['sentence_eng'],
            "sentence_rus": values['sentence_rus'],
            "showed": 0,
            "correct": 0,
        }
        update_word(current_word)

window.close()
