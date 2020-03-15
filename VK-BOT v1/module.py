# import python libs
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json
from time import strftime

# import interfaces and bot core
import user
import admin
import core

# import settings
with open("lib.json", "r", encoding="utf-8") as lib:
    data = json.load(lib)
lib.close()


# start VK session
vk_session = vk_api.VkApi(token=data['token'])
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, data['groupID'])
print("[INFO] vk session started")


# get contacts
contacts = []
for contact in vk.groups.getById(user_ids=data['site'], fields=['contacts'])[0]['contacts']:
    contacts.append(contact['user_id'])

# export to global cache
with open("global_cache.json", "r", encoding="utf-8") as glc:
    c = json.load(glc)
glc.close()

# создаем ключи при первом запуске
if f'lib{data["libID"]}' not in list(c.keys()):
    c[f'lib{data["libID"]}'] = {}
    c[f"lib{data['libID']}"]['requests'] = []

# добавляем в список детских библиотек (при необходимости)
if data['isKids'] and data['libID'] not in c['kids']:
    c['kids'].append(data['libID'])

# если библиотека перестала быть детской
elif not data['isKids'] and data['libID'] in c['kids']:
    c['kids'].pop(c['kids'].index(data['libID']))

# добавляем особые услуги
c[f"lib{data['libID']}"]['specials'] = []

if data['president']:
    c[f"lib{data['libID']}"]['specials'].append("president")
if data['national']:
    c[f"lib{data['libID']}"]['specials'].append("national")
if data['national_kids']:
    c[f"lib{data['libID']}"]['specials'].append("national_kids")

# генерируем описание
if data['isOpen']:
    services = []

    if data['president']:
        services.append("ПБ")
    if data['national']:
        services.append("НБ")
    if data['national_kids']:
        services.append("НДБ")

    description = f"{data['title']}\n" \
                  f"Адрес: {data['location']}\n" \
                  f"Сайт: {data['site']}\n" \
                  f"Услуги: {' '.join(services)}"

    del services
else:
    description = f"{data['title']}\n" \
                  f"Временно не работает"

# обновляем главные данные
c[f"lib{data['libID']}"]["title"] = data['title']
c[f"lib{data['libID']}"]["isOpen"] = data['isOpen']
c[f"lib{data['libID']}"]["site"] = data['site']
c[f"lib{data['libID']}"]["contacts"] = contacts
c[f"lib{data['libID']}"]["description"] = description

with open("global_cache.json", "w", encoding="utf-8") as glc:
    json.dump(c, glc, ensure_ascii=False)
glc.close()

print("[INFO] global cache exported")


# local cache
cache = {
    'availability': [],
    'extend': [],
    'delivery': [],
    'help': [],

    'admin DND': []
}

print("[INFO] bot started")

# event handle
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        if "payload" in event.object.message.keys():

            if "command" in eval(event.object.message['payload']).keys():

                # стартовое сообщение
                if eval(event.object.message['payload'])['command'] == "start":
                    if event.from_user:
                        if event.message.from_id in contacts:
                            admin.start(vk, event.message.from_id, core.get_requests(data['libID']),
                                        DND=event.message.from_id in cache['admin DND'])
                        else:
                            # проверка на выход из режима человек-человек
                            if event.message.from_id in cache['help']:
                                cache['help'].remove(event.message.from_id)

                            user.start(vk, event)

                # удаления пользователя из очереди на ожидание сообщения (см. else)
                if eval(event.object.message['payload'])['command'] == "del cache":
                    try:
                        if eval(event.object.message['payload'])['cache'] == "admin DND":
                            cache['admin DND'].remove(event.message.from_id)
                            admin.start(vk, event.message.from_id, core.get_requests(data['libID']),
                                        DND=False)
                        else:
                            cache[eval(event.object.message['payload'])['cache']].remove(event.message.from_id)
                    except ValueError:
                        pass

                # отправка запроса библиотекарю
                if eval(event.object.message['payload'])['command'] == "send requests":
                    if eval(event.object.message['payload'])['requestID'] == "None":
                        admin.send_request_error(vk, event, "no requests")
                        admin.start(vk, event.message.from_id, core.get_requests(data['libID']),
                                    DND=event.message.from_id in cache['admin DND'])

                    else:
                        cache['admin DND'].append(event.message.from_id)
                        admin.send_request(vk, event,
                                           core.req_msg_generator(eval(event.object.message['payload'])['requestID']),
                                           requestID=eval(event.object.message['payload'])['requestID'])

                # запрос одобрен
                if eval(event.object.message['payload'])['command'] == "request accepted":
                    try:
                        user.alert(vk,
                                   userID=eval(event.object.message['payload'])['requestID'],
                                   message=core.alert_generator(eval(event.object.message['payload'])['requestID'],
                                                                "accepted")
                                   )
                        core.request_delete(eval(event.object.message['payload'])['requestID'],
                                            data['libID'])
                    except FileNotFoundError:
                        admin.send_request_error(vk, event, "was processed")

                    cache['admin DND'].remove(event.message.from_id)
                    admin.start(vk, event.message.from_id, core.get_requests(data['libID']),
                                DND=False)

                # запрос отклонен
                if eval(event.object.message['payload'])['command'] == "request denied":
                    try:
                        user.alert(vk,
                                   userID=eval(event.object.message['payload'])['requestID'],
                                   message=core.alert_generator(eval(event.object.message['payload'])['requestID'],
                                                                "denied")
                                   )

                        core.request_delete(eval(event.object.message['payload'])['requestID'],
                                            data['libID'])
                    except FileNotFoundError:
                        admin.send_request_error(vk, event, "was processed")

                    cache['admin DND'].remove(event.message.from_id)
                    admin.start(vk, event.message.from_id, core.get_requests(data['libID']),
                                DND=False)

                # переключение DND
                if eval(event.object.message['payload'])['command'] == "switch DND":
                    if event.message.from_id in cache['admin DND']:
                        cache['admin DND'].remove(event.message.from_id)
                    else:
                        cache['admin DND'].append(event.message.from_id)

                    admin.start(vk, event.message.from_id, core.get_requests(data['libID']),
                                DND=event.message.from_id in cache['admin DND'])

                # переход в режим человек-человек
                if eval(event.object.message['payload'])['command'] == "help":
                    cache['help'].append(event.message.from_id)
                    user.help(vk, event)

            # разделы для обычных пользователей
            if "section" in eval(event.object.message['payload']).keys():
                # наша библиотека
                if eval(event.object.message['payload'])['section'] == "about us":
                    if event.from_user:
                        user.about_us(vk, event, data=data)

                # Муниципальное ОБъединение Библиотек
                if eval(event.object.message['payload'])['section'] == "mob":
                    if event.from_user:
                        user.mob(vk, event, core.get_lib_list())

                # услуги
                if eval(event.object.message['payload'])['section'] == "services":
                    if event.from_user:
                        user.services(vk, event)

                # продлить книгу
                if eval(event.object.message['payload'])['section'] == "extend":
                    if event.from_user:
                        cache['extend'].append(event.message.from_id)
                        user.extend(vk, event)

                # узнать о наличии книги
                if eval(event.object.message['payload'])['section'] == "availability":
                    if event.from_user:
                        cache['availability'].append(event.message.from_id)
                        user.availability(vk, event)

                # доставка книги
                if eval(event.object.message['payload'])['section'] == "delivery":
                    if event.from_user:
                        cache['delivery'].append(event.message.from_id)
                        user.delivery(vk, event)

                # мероприятия
                if eval(event.object.message['payload'])['section'] == "events":
                    if event.from_user:
                        user.events(vk, event, core.get_last_event(data['libID']),
                                    data['groupID'], data['site'])

        # отлов сообщений, не связанных с кнопкой
        else:

            # указывается ФИО для продления
            if event.message.from_id in cache['extend']:
                core.form_request(event.message.from_id, data['libID'],
                                  {"type": "extend",
                                   "name": event.message.text}
                                  )
                user.request_confirmed(vk, event, "extend")
                cache['extend'].remove(event.message.from_id)

                for contact in contacts:
                    if contact not in cache['admin DND']:
                        admin.alert(vk, contact,
                                    core.alert_generator(0, 'new request'))
                        admin.start(vk, contact, core.get_requests(data['libID']), DND=False)

            # указывается книга для запроса о наличии
            elif event.message.from_id in cache['availability']:
                core.form_request(event.message.from_id, data['libID'],
                                  {"type": "availability",
                                   "book": event.message.text}
                                  )
                user.request_confirmed(vk, event, "availability")
                cache['availability'].remove(event.message.from_id)

                for contact in contacts:
                    if contact not in cache['admin DND']:
                        admin.alert(vk, contact,
                                    core.alert_generator(0, 'new request'))
                        admin.start(vk, contact, core.get_requests(data['libID']), DND=False)

            # указывается книга для запроса на доставку
            elif event.message.from_id in cache['delivery']:
                core.form_request(event.message.from_id, data['libID'],
                                  {"type": "delivery",
                                   "book": event.message.text,
                                   "contact": f"vk.com/id{event.message.from_id}"}
                                  )
                user.request_confirmed(vk, event, "delivery")
                cache['delivery'].remove(event.message.from_id)

                for contact in contacts:
                    if contact not in cache['admin DND']:
                        admin.alert(vk, contact,
                                    core.alert_generator(0, 'new request'))
                        admin.start(vk, contact, core.get_requests(data['libID']), DND=False)

            # пользователь находится в режиме человек-человек
            elif event.message.from_id in cache['help']:
                for contact in contacts:
                    if contact not in cache['admin DND']:
                        admin.alert(vk, contact,
                                    core.alert_generator(0, 'need help', groupID=data['groupID']))

            # не относящиеся к исключениям
            else:
                user.unexpected_word(vk, event)

                if event.message.from_id in contacts:
                    admin.start(vk, event.message.from_id, core.get_requests(data['libID']),
                                DND=event.message.from_id in cache['admin DND'])
                else:
                    user.start(vk, event)
        print(cache)
    
    if event.type == VkBotEventType.WALL_POST_NEW:
        if "#мероприятие" in event.object.text.lower():
            core.add_event(event.object.id, data['libID'])
    

