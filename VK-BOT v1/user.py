from vk_api.utils import get_random_id
import vk_api.keyboard
from time import strftime


def start(vk, event):
    greeting = ''
    greetings = {
        "morning": "Доброе утро",
        "day": "Добрый день",
        "afternoon": "Добрый вечер",
        "night": "Доброй ночи"
    }

    if 4 <= int(strftime("%H")) <= 12:
        greeting = greetings['morning']
    if 13 <= int(strftime("%H")) <= 16:
        greeting = greetings['day']
    if 17 <= int(strftime("%H")) <= 23:
        greeting = greetings['afternoon']
    if 0 <= int(strftime("%H")) <= 3:
        greeting = greetings['night']

    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("Наша библиотека", vk_api.keyboard.VkKeyboardColor.PRIMARY,
                        {"section": "about us"})
    keyboard.add_line()
    keyboard.add_button("Мероприятия", vk_api.keyboard.VkKeyboardColor.PRIMARY,
                        {"section": "events"})

    keyboard.add_button("Услуги", vk_api.keyboard.VkKeyboardColor.PRIMARY,
                        {"section": "services"})
    keyboard.add_line()
    keyboard.add_button("Мне нужна помощь человека", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"command": "help"})

    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message=f"{greeting}, "
                f"{vk.users.get(user_ids=event.object.message['from_id'],name_case='Nom')[0]['first_name']}\n" +
                f"Для получения необходимой информации выберите кнопку с интересующим разделом",
        keyboard=keyboard.get_keyboard()
    )


def unexpected_word(vk, event):
    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message=f"Пожалуйста, используйте встроенную клавиатуру!")


def about_us(vk, event, data):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("Муниципальное Объединение Библиотек", vk_api.keyboard.VkKeyboardColor.PRIMARY,
                        {"section": "mob"})
    keyboard.add_line()
    keyboard.add_button("Назад", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"command": "start"})

    president = ""
    national = ""
    national_kids = ""

    if data['president']:
        president = "• Президентская библиотека\n"

    if data['national']:
        national = "• Национальная электронная библиотека\n"

    if data['national_kids']:
        national_kids = "• Национальная электронная детская библиотека\n"

    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message=f"{data['title']}\n\n"

                f"Адрес: {data['location']}\n"
                f"Телефон: {data['phone']}\n"
                f"e-mail: {data['email']}\n"
                f"Сайт: {data['site']}\n\n"

                f"Часы работы: {data['time']}\n\n"

                f"Услуги:\n"
                f"{president}{national}{national_kids}\n"
                f"{data['services']}\n\n"
                
                f"Транспорт: {data['transport']}",
        keyboard=keyboard.get_keyboard(),
        lat=data['lat'],
        long=data['long'],
        dont_parse_links=1
    )


def mob(vk, event, list):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
    keyboard.add_button("назад", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"section": "about us"})

    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message=f"Наши библиотеки:\n"
                f"{list}\n\n"
                
                f"Условные обозначения:\n"
                f"ПБ - президентская библиотека\n"
                f"НБ - национальная библиотека\n"
                f"НДБ - национальная детская библиотека",
        keyboard=keyboard.get_keyboard(),
        dont_parse_links=1
    )


def services(vk, event):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("Узнать о наличии книги", vk_api.keyboard.VkKeyboardColor.PRIMARY,
                        {"section": "availability"})
    keyboard.add_line()
    keyboard.add_button("Продлить срок", vk_api.keyboard.VkKeyboardColor.PRIMARY,
                        {"section": "extend"})
    # keyboard.add_line()
    keyboard.add_button("Доставить книгу", vk_api.keyboard.VkKeyboardColor.PRIMARY,
                        {"section": "delivery"})
    keyboard.add_line()
    keyboard.add_button("Назад", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"command": "start"})

    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message=f"Через бота Вы можете воспользоваться следущими услугами:\n"
                f"• Узнать о наличии книги в наших библиотеках\n"
                f"• Продлить книгу в нашей библиотеке\n"
                f"• Доставить нужную книгу в удобную библиотеку\n\n"
                
                f"С остальными услугами можно ознакомиться на нашем сайте: "
                f"https://моб.екатеринбург.рф/about/services/",
        keyboard=keyboard.get_keyboard(),
        dont_parse_links=1
    )


def extend(vk, event):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("Отмена", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"section": "services", "command": "del cache", "cache": "extend"})

    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message=f"Пожалуйста, пришлите Ваше ФИО\nЗапрос будет отправлен библиотекарю, и Вы получите уведомление о его "
                f"результате",
        keyboard=keyboard.get_keyboard()
    )


def availability(vk, event):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("Отмена", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"section": "services", "command": "del cache", "cache": "availability"})

    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message=f"Пожалуйста, пришлите название книги, которая Вам нужна\nЗапрос будет отправлен библиотекарю, и Вы получите уведомление о его "
                f"результате",
        keyboard=keyboard.get_keyboard()
    )


def delivery(vk, event):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("Отмена", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"section": "services", "command": "del cache", "cache": "delivery"})

    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message="Пожалуйста, пришлите название книги, которая Вам нужна\n"
                "Узнать о наличии книги в МОБ можно в соответствующем пункте\n"
                "Запрос будет отправлен библиотекарю, и Вы получите уведомление о его результате",
        keyboard=keyboard.get_keyboard()
    )


def request_confirmed(vk, event, type):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("Ок", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"section": "services", "command": "del cache", "cache": "extend"})

    type_text = ''

    if type == "extend":
        type_text = "на продление книги"

    if type == "delivery":
        type_text = "на доставку книги"

    if type == "availability":
        type_text = "о наличии книги"

    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message=f"Ваш запрос {type_text} принят. Ожидайте уведомления.\n"
                f"Обратите внимание! Если Вы отправите новый запрос, то этот будет удалён",
        keyboard=keyboard.get_keyboard()
    )


def alert(vk, userID, message):
    vk.messages.send(
        user_id=userID,
        random_id=get_random_id(),
        message=message
    )


def help(vk, event):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    keyboard.add_button("Вернуться к боту", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"command": "start"}
                        )
    vk.messages.send(
        user_id=event.message.from_id,
        random_id=get_random_id(),
        message="Сейчас вы общаетесь с библиотекарем, если захотите вернуться в режим бота, просто нажмите "
                "кнопку ниже. Напишите свое первое сообщение",
        keyboard=keyboard.get_keyboard()
    )


def events(vk, event, post, groupID, site):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
    keyboard.add_button("Назад", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"command": "start"}
                        )

    vk.messages.send(
        user_id=event.message.from_id,
        random_id=get_random_id(),
        message=f"Последнее новое мероприятие:\n"
        f"{site}?w=wall-{groupID}_{post}\n\n"
        f"Все мероприятия МОБ:\n"
        f"https://моб.екатеринбург.рф/663/",
        keyboard=keyboard.get_keyboard(),
        attachments=[f"wall{groupID}_{post}"],
        dont_parse_links=1
    )