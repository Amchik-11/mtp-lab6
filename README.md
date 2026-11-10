# Книжная гостиная — лабораторная №6

Морозова Анастасия Алексеевна, группа 221341, вариант 3, лабораторная №6.
Методические указания, часть 1, страницы 11–12.

## Как посмотреть результат

Нужен Python 3.12. В PowerShell из папки проекта:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Откройте `http://127.0.0.1:5000`.

| Задание | Страница | Как устроено |
| --- | --- | --- |
| Среднее №3 | `/` | Статический HTML и собственный `reading.css` |
| Среднее №5 | `/showcase` | Таблица, бейджи и кнопка Bootstrap 5 через CDN |
| Среднее №9 | `/recommendations` | Flask передаёт подборку книг в шаблон Jinja2 |
| Повышенное №3 | `/reading-room` | Вход, сессия и выход в модуле `access.py` |
| Повышенное №7 | Heroku | Конфигурация готова, публикация предстоит |

## Вход в читальный зал

Остановите сервер, выполните команду ниже и придумайте отдельный пароль
для учебного сайта. Команда выведет хеш пароля и ключ сессии.

```powershell
.\.venv\Scripts\python.exe -m flask --app main access-values
$env:READING_USER = 'reader'
$env:READING_PASSWORD_HASH = '<значение после READING_PASSWORD_HASH=>'
$env:SECRET_KEY = '<значение после SECRET_KEY=>'
.\.venv\Scripts\python.exe main.py
```

Откройте `/reading-room` и войдите как `reader` с придуманным паролем.
Кнопка «Выйти» завершает сессию. Значения переменных окружения задаются
в терминале или в Heroku Config Vars и не добавляются в Git.

## Что осталось сделать в Heroku

1. Войти в подтверждённый аккаунт Heroku и создать приложение либо открыть
   уже созданное. Для запуска нужен доступный тариф с веб-процессом.
2. В `Settings → Config Vars` задать `READING_USER`, `READING_PASSWORD_HASH`
   и `SECRET_KEY`, используя отдельные значения для опубликованного сайта.
3. В `Deploy → GitHub` подключить репозиторий этой работы, выбрать `main`
   и нажать `Deploy Branch`. `Procfile` запускает `main:app` через Gunicorn.
4. Нажать `Open app`. Проверить главную, витрину, подборку, вход и выход.
   Приложить к ревью HTTPS-ссылку на открывающееся приложение.

Инструкции Heroku: [деплой из GitHub](https://devcenter.heroku.com/articles/github-integration)
и [переменные окружения](https://devcenter.heroku.com/articles/config-vars).

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```
