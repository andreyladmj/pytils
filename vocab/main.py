import openai

openai.api_key = "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"
messages = [ {"role": "system", "content": "Дай мне перевод слова assistant в формате json."} ]

# while True:
#     message = input("User : ")
#     if message:
#         messages.append(
#             {"role": "user", "content": message},
#         )
#         chat = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo", messages=messages
#         )
#     reply = chat.choices[0].message.content
#     print(f"ChatGPT: {reply}")
#     messages.append({"role": "assistant", "content": reply})

chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
reply = chat.choices[0].message.content
print(f"ChatGPT: {reply}")