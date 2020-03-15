# Bots
Универсальный бот, разработанный для Муниципального Объединения Библиотек города Екатеринбург

## Команда
* Солдатов Александр
* Микрюков Иван `@SenkuID`
* Шевелёв Данил `@danilka32188`
* Зарипов Руслан
* Мурашев Иван `@Koldef`

## Создание файла библиотеки
В папке с `module.py` необходимо создать файл `lib.json`:

```
{
  "libID": int,
  "groupID": int,
  "token": str,

  "title": str,
  "isOpen": bool,
  "isKids": bool,

  "location": str,
  "time": str,
  "transport": str,
  "lat": float,
  "long": float,

  "phone": str,
  "contact": str,
  "email": str,
  "site": str,

  "president": bool,
  "national": bool,
  "national_kids": bool,

  "services": str
}
```

### Значение параметров `lib.json`
* **libID** *(int)* - ID библиотеки в системе
* **groupID** *(int)*- ID группы ВКонтакте
* **token** *(str)* - token VkBotLongPoll
* **title** *(str)* - Название библиотеки
* **isOpen** *(bool)* - открыта ли библиотека
* **isKids** *(bool)* - детская библиотека
* **location** *(str)* - адрес библиотеки
* **time** *(str)* - время работы
* **transport** *(str)* - ближайшие остановки транспорта
* **lat** *(float)* - географическая широта
* **long** *(float)* - географическая долгота
* **phone** *(str)* - номер телефона для связи
* **contact** *(str)* - контактное лицо
* **email** *(str)* - электронная почта для связи
* **site** *(str)* - ссылка на группу библиотеки ВКонтакте
* **president** *(bool)* - президентская электронная библиотека
* **national** *(bool)* - национальная электронная библиотека
* **national_kids** *(bool)* - национальная детская электронная библиотека
* **services** *(str)* - услуги библиотеки
