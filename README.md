# Установка
Проект написан на python 3.10

1. Перейдите в директорию Volga_IT `cd Volga_IT`.    
2. Создайте виртуальное окружение: `python -m venv venv`.
3. Активируйте его: `venv\Scripts\activate.bat`.
4. Перейдите в папку Sibmir_GO: `cd Sibmir_GO`.
5. Установите зависимости: `pip install -r requirements.txt`.
6. Переименовать файл .env.dist в .env и заменить в нём значения перемнных на настоящие данные postgreSQL.  
7. Проведите миграции: `python manage.py migrate`.
8. Создайте админа: `python manage.py createsuperuser`.  
9. Запустить проект `python manage.py runserver`.

### URL http://127.0.0.1:8000/swagger/

## Изменения
1. По заданию написано, что нужно испоьзовать JWT токены. Но при этом в задание не указаны ендпоинты для обновления 
access токена. Возможно, аутентифкацию следовало проводить по обычным токенам, но я всё же сделал по JWT, возвращая
   access и refresh токены и добавил ендпоинт /Account/Token/refresh, возвращающий access и refresh токены. Время жизни
   access токена нужно делать очень маленьким, но для удобного тестирования я установил его 1 час.
   `/Account/SignOut/` теперь принимает refresh токен в теле запроса, чтобы добавить этот токен в чёрный список, чтобы по нему нельзя было обновить access токен.

2. Параметры для GET запросов я сделал обязательными, кроме start, count и rentType. Не указывая их, вы берёте весь диапазон.
Например указав только start возьмутся все записи от start до конца.
   

