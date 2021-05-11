##### Тестовый проект для проверки работоспособности marshmallow-enum и errand-boy на Python 3 & Django 1.11

#### Для запуска
1. Создать окружение с python 3
2. Установить зависимости
3. Запустить errand-boy
`python -m errand_boy.run`
4. Запустить проект
`./manage.py runserver 9000`
5. Открыть `http://127.0.0.1:9000/test/`  
В поле "Content" вставить данные: `{"paymentMethod": "CASH", "type": "SELL"}`  
Отправить запрос