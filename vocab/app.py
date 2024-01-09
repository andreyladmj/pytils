import json
import random
import time

import PySimpleGUI as sg

font = ("Verdana", 16)
sg.set_options(font=font)
sg.theme('DarkAmber')

with open("vocab.json", encoding="utf8") as f:
    words = json.loads(f.read())

def update_word(current_word, correct):
    with open("vocab.json", encoding="utf8") as f:
        words = json.loads(f.read())

    for i in range(len(words)):
        if words[i]['word_eng'] == current_word:
            if 'showed' not in words[i].keys():
                words[i]['showed'] = 0
            if 'correct' not in words[i].keys():
                words[i]['correct'] = 0
            words[i]['showed'] += 1

            if correct:
                words[i]['correct'] += 1

            break

    with open("vocab.json", 'w', encoding="utf8") as f:
        f.write(json.dumps(words, ensure_ascii=False))



while True:
    data = random.choice(words)
    # data = words[0]

    word = data['word_eng']
    translation = data['sentence_rus']

    layout = [  [sg.Text(translation, key='sentense')],
                [sg.Text('Enter:'), sg.InputText(key='input')],
                [sg.Text('', key='result', text_color='red')],
                [sg.Button('Ok'),] ] #  sg.Button('Cancel')


    window = sg.Window('Vocabulary', layout, finalize=True)
    window['input'].bind("<Return>", "_Enter")
    correct = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

        if correct is None:
            correct = word == values['input']

        if word != values['input']:
            window['result'].update(word)
        else:
            break

    update_word(word, correct)
    window.close()
    time.sleep(900)