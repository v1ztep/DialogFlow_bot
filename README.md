# Чатботы [Telegram](https://telegram.org/) и [VK](https://vk.com/) обученные через [DialogFlow](https://cloud.google.com/dialogflow).

Чатботы для [Telegram](https://telegram.org/) и [Вконтакте](https://vk.com/) с 
распознаванием вольной речи через [DialogFlow](https://cloud.google.com/dialogflow).

![gif](media/TG_VK_bots.gif)

[Наглядная демонстрация с возможностью самому написать ботам](#демонстрация)

## Настройки

* Необходимо зарегистрироваться в [Google Cloud](https://cloud.google.com).
* [Создать проект в DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup#project) 
  и забрать ваш идентификатор проекта(project_id).
* [Создать агента DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/build-agent#create-an-agent).
* Натренируйте DialogFlow создав intent вручную, либо можете воспользоваться 
  скриптом `сreate_intent.py`([описание ниже](#обучение-dialogflow-через-api)).
* Создайте [JSON-ключ](https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account).
* Создать бота в Telegram через специального бота:
[@BotFather](https://telegram.me/BotFather), забрать API ключ и написать 
созданному боту.
* Забрать свой `chat_id` через [@userinfobot](https://telegram.me/userinfobot) - 
  необходим для получения логов.
* Создать группу в [Вконтакте](https://vk.com/groups?tab=admin) и в настройках 
  группы -> "Работа с API" создать API-ключ с правами: Управление группой, 
  Отправка сообщений.

### Переменные окружения

Создайте файл `.env` в корневой папке с кодом и запишите туда:
```
DIALOGFLOW_PROJECT_ID=ВАШ_PROJECT_ID
GOOGLE_APPLICATION_CREDENTIALS=ПУТЬ_ДО_JSON_КЛЮЧА
TG_BOT_TOKEN=ВАШ_TELEGRAM_API_КЛЮЧ
TG_CHAT_ID=ВАШ_CHAT_ID
VK_BOT_TOKEN=ВАШ_API_КЛЮЧ_ВК
```


## Запуск

Для запуска у вас уже должен быть установлен [Python 3](https://www.python.org/downloads/release/python-379/).

- Скачайте код.
- Установите зависимости командой:
```
pip install -r requirements.txt
```
- Запустите скрипт командой: 
```
python tg_bot.py
```
```
python vk_bot.py
```


## Демонстрация

Вы можете протестировать работу данных ботов.

* Напишите в [Telegram @v1ztep_bot](https://telegram.me/v1ztep_bot).
* Напишите в [ВК группу](https://vk.com/im?sel=-203205099) - отключены 
  уточняющие фразы.

Боты обучены распознавать вольную речь на следующие темы:
```
Приветствие
Устройство на работу
Забыл пароль
Удаление аккаунта
Вопросы от забаненных
Вопросы от действующих партнёров(совещания, контракты)
```


## Обучение DialogFlow через API

Создайте файл `questions.json` в корневой папке c проектом в формате:
```
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    "Забыл пароль": {
        "questions": [
            ...
        ],
        "answer": ...
    },
    ...
}
```
    

