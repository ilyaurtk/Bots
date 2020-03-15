import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import random
import datetime


def main():
    keyboard = VkKeyboard(one_time= False) # Основная клавиатура

    keyboard.add_button('Как пройти', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Время работы', color=VkKeyboardColor.POSITIVE)

    keyboard.add_line() 
    keyboard.add_location_button()


    vk_session = vk_api.VkApi(token= 'b41fd4d32a0f975c12103687db7011d79fc960ea085c42c829a963b00cb40e9ab3491292bec36dfd1ffe0') #Токен группы
    vk = vk_session.get_api()
                                      
    longpoll = VkLongPoll(vk_session)


    for event in longpoll.listen(): 
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            vk.messages.send(
                    peer_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard(), #Вызов основной клавиатуры
                    message='Выбирай!!!')

            if event.text == 'Как пройти':          # как пройти
                vk.messages.send(
                    user_id=event.user_id,
                    random_id = random.randint(0, 5645644),
                    message='Ногами АХАХАХАХАХАХ')  
                
            elif event.text == 'Время работы':            #Время работы
                vk.messages.send(
                    user_id=event.user_id,
                    random_id = random.randint(0, 5645644),
                    message="Когда надо, тогда и работаем АХАХАХАХХАХ")

            else:                                                         # В непонятках - выкидываем фразу
                vk.messages.send(
                    user_id=event.user_id,
                    random_id = random.randint(0, 5645644),
                    message="Непонел прекола, дубль 2...")




if __name__ == '__main__':
    main()