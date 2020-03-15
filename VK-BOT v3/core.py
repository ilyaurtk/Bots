import json
import vk_api.vk_api
from os import listdir, remove


def form_request(userID, libID, data):
    # общее начало запроса
    req = {"userID": userID,
           "libID": libID,
           "type": data['type']
           }

    with open(f"global_cache.json", "r", encoding="UTF-8") as cache:
        c = json.load(cache)
    cache.close()

    if userID not in c[f'lib{libID}']['requests']:
        c[f'lib{libID}']['requests'].append(userID)

    # формирование на запрос о продлении книги
    if data['type'] == "extend":
        req["name"] = data['name']

        with open(f"global_cache.json", "w", encoding="UTF-8") as cache:
            json.dump(c, cache, ensure_ascii=False)
        cache.close()

        print(f"[REQUEST] {data['name']} просит продлить книгу")

    # формирование запроса о наличии книги
    if data['type'] == "availability":
        req["book"] = data['book']

        with open(f"global_cache.json", "w", encoding="UTF-8") as cache:
            json.dump(c, cache, ensure_ascii=False)
        cache.close()

    # формирование запроса на доставку книги
    if data['type'] == "delivery":
        req["book"] = data['book']
        req['contact'] = data['contact']

        with open(f"global_cache.json", "w", encoding="UTF-8") as cache:
            json.dump(c, cache, ensure_ascii=False)
        cache.close()

    # сохранение запроса в глобальном кеше
    with open(f"./requests/{userID}.json", "w", encoding="UTF-8") as request:
        json.dump(req, request, ensure_ascii=False)
    request.close()



def get_requests(libID):
    with open(f"global_cache.json", "r", encoding="UTF-8") as cache:
        requests = json.load(cache)[f'lib{libID}']['requests']
    cache.close()

    return {
        "requests": requests,
        "count": len(requests)
    }


def req_msg_generator(requestID):
    with open(f"./requests/{requestID}.json", "r", encoding="UTF-8") as request:
        r = json.load(request)
    request.close()

    if r['type'] == "extend":
        return f"{r['name']} просит продлить срок выдачи книги"

    if r['type'] == "availability":
        return f"Есть ли книга «{r['book']}» в объединении библиотек (в общей базе данных)?"

    if r['type'] == "delivery":
        return f"Возможно ли доставить в Вашу библиотеку?\nКнига: {r['book']}\nКонтакт: {r['contact']}"


def alert_generator(requestID, status, **data):

    if requestID != 0:
        with open(f"./requests/{requestID}.json", "r", encoding="UTF-8") as request:
            r = json.load(request)
        request.close()

        if status == "accepted":
            if r['type'] == 'extend':
                return "Ваш запрос на продление одобрен. Вы можете вернуть литературу через 14 календарных дней"

            if r['type'] == 'availability':
                return f"Книга «{r['book']}» есть в библиотеках"

            if r['type'] == 'delivery':
                return f"Запрос на доставку книги «{r['book']}» принят. С Вами свяжутся после доставки"

        elif status == "denied":
            if r['type'] == 'extend':
                return "Ваш запрос на продление отклонен. Просьба вернуть литературу в ближайшее время"

            if r['type'] == 'availability':
                return f"Книга «{r['book']}» отсутствует в библиотеках"

            if r['type'] == 'delivery':
                return f"Доставка книги «{r['book']}» отклонена. Возможно, она отсутствует"

    elif status == 'new request':
        return "Появился новый запрос!"
    elif status == "need help":
        return f"Требуется личная помощь. Вы можете ответить в личных сообщениях группы: " \
               f"https://vk.com/gim{data['groupID']}"


def request_delete(requestID, libID):
    # remove from global cache
    with open(f"global_cache.json", "r", encoding="UTF-8") as cache:
        c = json.load(cache)
        c[f'lib{libID}']['requests'].remove(requestID)
    cache.close()

    with open(f"global_cache.json", "w", encoding="UTF-8") as cache:
        json.dump(c, cache, ensure_ascii=False)
    cache.close()

    # remove from directory
    remove(f"./requests/{requestID}.json")


def get_lib_list():
    with open(f"./global_cache.json", "r", encoding="UTF-8") as glc:
        data = json.load(glc)
    glc.close()

    libs = []

    for library in list(data.keys())[1:]:
        try:
            libs.append(data[library]['description'])
        except KeyError:
            pass

    lib_list = "\n\n".join(libs)
    del libs

    return lib_list


def add_event(post, libID):
    with open(f"global_cache.json", "r", encoding="UTF-8") as cache:
        c = json.load(cache)
    cache.close()

    c[f'lib{libID}']['last event'] = post

    with open(f"global_cache.json", "w", encoding="UTF-8") as cache:
        json.dump(c, cache, ensure_ascii=False)
    cache.close()


def get_last_event(libID):
    with open(f"global_cache.json", "r", encoding="UTF-8") as cache:
        c = json.load(cache)
    cache.close()

    return c[f'lib{libID}']['last event']


def db(author):
    with open("./db.json", "r", encoding="UTF-8") as file:
        f = json.load(file)
    file.close()

    try:
        list = "\n".join(f[author])
        return f"Книги автора {author}:\n{list}"
    except KeyError:
        return "Автор не найден или доступных книг нет"
