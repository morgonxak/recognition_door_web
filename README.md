# recognition_raspberry_web
Программа для Raspberry pi 4 8GB Предназначена для работы с базой данных пользователей

# Функционал:
0. Добавить пользователя в систему
0. Удалить пользователя из системы
0. Изменить параметры поьзователя
0. Обучить классификатор для текщех пользователей

# Настроки:
0. распользаются в settings
0. PATH_DATA_BASE - Путь для базы данных SQLite
0. PATH_SAVE_MODEL - Путь где будут хранится обученные модели, классификатор каскада хаара, временные данные
0. PATH_DATASET - пользовательская база данных хранятся фотографии пользователей
0. ID_CARARA - Номер камеры в операционной системе изначально 0

# Создание Сервиса в Systemd
0. Создать файл: sudo touch /etc/systemd/system/door_server.service
0. Меняем права: sudo chmod 664 /etc/systemd/system/door_server.service
0. Пример формирования: rc/door_server.service
0. Добовляем в автозапуск: systemctl enable door_server.service
0. перезапустить systemD: sudo systemctl daemon-reload

# Технологии:
0. Python 3.7.3
0. SQLite

## Установка:
0. Создать виртуальное окружения python3 -m venv door, активировать source door/bin/activate
0. pip install -r requirements.txt
0. Запуск: pyhton run_server.py

## Описание папок проекта
0. expirements - Тестовые файлы.
0. rs - ресурсы проекта (содержат обученные модели и классификатор для поискаа лиц).
0. modul - основные компоненты с которыми работает программа

