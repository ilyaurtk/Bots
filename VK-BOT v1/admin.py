from vk_api.utils import get_random_id
import vk_api.keyboard
from time import strftime


def start(vk, adminID, requests, **data):
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

    DNDstatus = ""
    DNDbutton = ""
    color = vk_api.keyboard.VkKeyboardColor.DEFAULT

    if data:
        if data['DND']:
            DNDstatus = "Уведомления выключены"
            DNDbutton = "Включить уведомления"
            color = vk_api.keyboard.VkKeyboardColor.PRIMARY
        else:
            DNDstatus = "Уведомления о новых запросах включены"
            DNDbutton = "Выключить уведомления"

    if requests['count'] > 0:
        req_txt = f"Количество запросов для библиотеки: {requests['count']}"
        keyboard.add_button("Рассмотреть запросы", vk_api.keyboard.VkKeyboardColor.PRIMARY,
                            {"command": "send requests", "requestID": requests['requests'][-1]}
                            )
    else:
        keyboard.add_button("Расмотреть запросы", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                            {"command": "send requests", "requestID": "None"})
        req_txt = "На данный момент запросов нет. Вам придет уведомление, если что-то появится"

    keyboard.add_line()
    keyboard.add_button(f"{DNDbutton}", color, {"command": "switch DND"})

    vk.messages.send(
            user_id=adminID,
            random_id=get_random_id(),
            message=f"{greeting}, "
                    f"{vk.users.get(user_ids=adminID, name_case='Nom')[0]['first_name']}\n\n" +
                    f"{req_txt}\n\n{DNDstatus}",
            keyboard=keyboard.get_keyboard()
        )


def send_request(vk, event, msg, requestID):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("Да", vk_api.keyboard.VkKeyboardColor.POSITIVE,
                        {"command": "request accepted", "requestID": requestID})

    keyboard.add_button("Нет", vk_api.keyboard.VkKeyboardColor.NEGATIVE,
                        {"command": "request denied", "requestID": requestID})
    keyboard.add_line()
    keyboard.add_button("Назад", vk_api.keyboard.VkKeyboardColor.DEFAULT,
                        {"command": "del cache", "cache": "admin DND"})

    vk.messages.send(
        user_id=event.object.message['from_id'],
        random_id=get_random_id(),
        message=f"{msg}",
        keyboard=keyboard.get_keyboard()
    )


def send_request_error(vk, event, type):
    msg = ''

    if type == "no requests":
        msg = "Новых запросов нет"
    elif type == "was processed":
        msg = "Запрос был обработан другим библиотекарем"

    vk.messages.send(
        user_id=event.message.from_id,
        random_id=get_random_id(),
        message=f"{msg}"
    )


def alert(vk, adminID, message):
    vk.messages.send(
        user_id=adminID,
        random_id=get_random_id(),
        message=message
    )
