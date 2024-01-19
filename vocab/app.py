import json
import random
import time

import PySimpleGUI as sg

# import pandas as pd
# pd.set_option("display.max_rows", 500)
# pd.set_option("display.max_columns", 500)
# pd.set_option("display.width", 1000)


font = ("Verdana", 16)
sg.set_options(font=font)
sg.theme('DarkAmber')

with open("vocab.json", encoding="utf8") as f:
    words = json.loads(f.read())
    # words.sort(key=lambda word: word['correct'])

# for i in range(len(words)):
#     words[i]['probability'] = words[i].get('correct', 0) / words[i].get('showed', 1)
#
# for word in words:
#     try:
#         word['probability'] = 1 - word.get('correct', 0) / word.get('showed', 1)
#     except ZeroDivisionError:
#         word['probability'] = 0.8
#
# for word in words:
#     print(word['word_eng'],word['correct'],word['showed'], word['probability'])
#
# import pandas as pd
# df = pd.DataFrame(words)

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
    time.sleep(300)
