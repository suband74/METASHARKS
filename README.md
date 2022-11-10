# Backend-сервис для организации учебного процесса в ВУЗе

## Общее описание

Все пользователи системы - зарегистрированные пользователи. На данном этапе в сервисе существуют три роли пользователей ("Администратор", "Куратор", "Студент"), воспользоваться сервисом могут только "Администратор" и назначенные им "Кураторы". Сервис работает следующим образом:
1. Регистрируется "Администратор" и получает токен.
2. "Администратор" регистрирует "Кураторов" (зарегистрированный"куратор" может регистрировать других "Кураторов").
3. "Администратор" регистрирует "Направление обучения" и "Предметы" через админку и управляет этими сущностями.
4. "Куратор" регистрирует пользователей, группы, набирает студентов (из зарегистрированных пользователей с ролью "Студент") и упарвляет этими сущностями.
5. "Администратор" может сформировать два вида отчетов (отчеты генерируются с помощью асинхронной задачи), в формате excel-файла.
6. Посмотреть статус выполнения асинхронной задачи можно в браузере по адресу: `http://localhost:5555/`

## Установка проекта на локальный компьютер:

1. Должен быть предустановлен менеджер зависимостей `poetry`. Или установите `poetry` любым удобным способом. 
   Например: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -` 
2. Выполните клонирование репозитория: `git clone https://github.com/inkoit/sudoku-solver-task.git`
3. Затем выполните установку зависимостей проекта: `poetry install`
4. Установить docker и docker-compose. Инструкции по установке доступны в официальной документации.
5. В папке с проектом выполнить команду:
```
docker-compose up
```
6. Создайте суперюзера с ролью "Администратор"
7. В файле `api.json` используйте `endpoints`.
