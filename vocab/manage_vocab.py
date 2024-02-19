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
        if words[i]['word_eng'] == current_word['word_eng']:
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

layout.append([sg.Text('Example rus 1:'), sg.InputText(key='example_rus1')])
layout.append([sg.Text('Example eng 1:'), sg.InputText(key='example_eng1')])

layout.append([sg.Text('Example rus 2:'), sg.InputText(key='example_rus2')])
layout.append([sg.Text('Example eng 2:'), sg.InputText(key='example_eng2')])

layout.append([sg.Text('Example rus 3:'), sg.InputText(key='example_rus3')])
layout.append([sg.Text('Example eng 3:'), sg.InputText(key='example_eng3')])

layout.append([sg.Text('Example rus 4:'), sg.InputText(key='example_rus4')])
layout.append([sg.Text('Example eng 4:'), sg.InputText(key='example_eng4')])

layout.append([sg.Text('Example rus 5:'), sg.InputText(key='example_rus5')])
layout.append([sg.Text('Example eng 5:'), sg.InputText(key='example_eng5')])
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
        examples = word.get('examples', [])
        window['word_eng'].update(word.get('word_eng', ""))
        window['word_esp'].update(word.get('word_esp', ""))
        window['sentence_eng'].update(word.get('sentence_eng', ""))
        window['sentence_rus'].update(word.get('sentence_rus', ""))

        for i in range(5):
            window[f'example_rus{i+1}'].update('')
            window[f'example_eng{i+1}'].update('')

        for i in range(len(examples)):
            window[f'example_rus{i+1}'].update(examples[i]['rus'])
            window[f'example_eng{i+1}'].update(examples[i]['eng'])

    elif event == 'Add':
        new_word = {
            "word_eng": values['word_eng'],
            "word_esp": values['word_esp'],
            "sentence_eng": values['sentence_eng'],
            "sentence_rus": values['sentence_rus'],
            "showed": 0,
            "correct": 0,
            "examples": [
                {"rus": values['example_rus1'], "eng": values['example_eng1']},
                {"rus": values['example_rus2'], "eng": values['example_eng2']},
                {"rus": values['example_rus3'], "eng": values['example_eng3']},
                {"rus": values['example_rus4'], "eng": values['example_eng4']},
                {"rus": values['example_rus5'], "eng": values['example_eng5']},
            ],
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
            "examples": [
                {"rus": values['example_rus1'], "eng": values['example_eng1']},
                {"rus": values['example_rus2'], "eng": values['example_eng2']},
                {"rus": values['example_rus3'], "eng": values['example_eng3']},
                {"rus": values['example_rus4'], "eng": values['example_eng4']},
                {"rus": values['example_rus5'], "eng": values['example_eng5']},
            ],
        }
        update_word(current_word)

window.close()

# if you shoot someone, you want to change something about that person. this is a noble intention