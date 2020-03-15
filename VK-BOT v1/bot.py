import requests
import vk_api
import random

vk_session = vk_api.VkApi(token='b41fd4d32a0f975c12103687db7011d79fc960ea085c42c829a963b00cb40e9ab3491292bec36dfd1ffe0')

from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:		
        if event.text != "iop":
            vk.messages.send( #Отправляем сообщение
                user_id=event.user_id,
                random_id = random.randint(2654, 35465436541),
                message='ъаъъ')
        else:
        	break