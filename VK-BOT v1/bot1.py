import requests
import vk_api
import random
import wikipedia
import datetime

vk_session = vk_api.VkApi(token='b41fd4d32a0f975c12103687db7011d79fc960ea085c42c829a963b00cb40e9ab3491292bec36dfd1ffe0')

from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

wikipedia.set_lang("RU")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

        if event.text[:4] == "вики" or event.text[:4] == "Вики":          # Проверяем, не вики-запрос ли это?
            vk.messages.send(
                user_id=event.user_id,
                random_id = random.randint(0, 5645644),
                message='Вот что я нашёл: \n' + str(wikipedia.summary(event.text[3:])))		

        elif event.text == "дата" or event.text == "Дата":            # Проверяем, не дата-запрос ли это?
            today = datetime.datetime.today()
            t = today.strftime("%m/%d/%Y")
            vk.messages.send(
                user_id=event.user_id,
                random_id = random.randint(0, 5645644),
                message=t)

        else:                                                         # В непонятках - выкидываем фразу
            vk.messages.send(
                user_id=event.user_id,
                random_id = random.randint(0, 5645644),
                message="Непонел прекола, дубль 2...")