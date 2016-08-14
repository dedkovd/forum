# forum
Forum app

В проекте использованы следующие фреймворки:

```
Django version 1.8.4
djangorestframework==3.4.3 - для реализации REST
djangorestframework-recursive==0.1.1 - для реализации иерархии ответов на пост
django-resized==0.3.5 - для реализации ресайза картинки
```

После выполнения manage.py syncdb необходимо запустить на выполнение скрипт init_db.py:

```
python init_db.py
```

Этот скрипт загрузит в базу данные о странах и городах. Данные взяты из этого поста: https://habrahabr.ru/post/21949/

Описание API:

```
# Незарегистрированный пользователь
GET /api/countries/ # получить список стран
GET /api/countries/<id>/ # получить страну с идентификатором "id"
GET /api/countries/<id>/cities/ # получить города страны с идентификатором "id"
POST /api/register/ # зарегистрировать нового пользователя
POST /api-token-auth/ # получить авторизационный токен

# Зарегистрированный пользователь
GET /api/categories/ # получить список категорий
GET /api/categories/<id>/ # получить категорию с идентификатором "id"
GET /api/categories/<id>/posts/ # получить все посты в категории с идентификатором "id"
GET /api/posts/ # получить список всех постов
GET /api/posts/<id>/ # получить пост с идентификатором "id"
GET /api/posts/<id>/images/ # получить изображения для поста с идентификатором "id"
GET /api/starred/ # получить список избранных постов для текущего пользователя
POST /api/categories/<id>/posts/ # добавить пост в категорию с идентификатором "id"
POST /api/posts/<id>/images/ # добавить изображение к посту c идентификатором "id"
PUT /api/posts/<id>/ # редактировать пост с идентификатором "id"
DELETE /api/posts/<id>/ # удалить пост с идентификатором "id"
POST /api/posts/<id>/starred/ # добавить пост с идентификатором "id" в избранное
DELETE /api/posts/<id>/starred/ # удалить пост с идентификтором "id" из избранного

# Администратор
POST /api/categories/ # добавить категорию
PUT /api/categories/<id>/ # редактировать категорию
GET /api/categories/ # получить список категорий
GET /api/posts/<id>/ # получить пост с идентификатором "id"
GET /api/posts/<id>/images/ # получить изображения для поста с идентификатором "id"
PUT /api/posts/<id>/ # редактировать пост с идентификатором "id" (в частности - модерация)
POST /api/ban/<id>/ # бан пользователя с идентификатором "id"
POST /api/unban/<id>/ # снятие бана пользователя с идентификатором "id"
GET /api/posts/ # получить список всех постов
GET /api/categories/<id>/posts/ # получить все посты в категории с идентификатором "id"
```

Дамп базы данных (SQLite) доступен по адресу: https://drive.google.com/open?id=0B0v_-i-STs5bUGtOR0pwVmFVOTA

Дамп запросов Postman доступен по адресу: https://drive.google.com/open?id=0B0v_-i-STs5bZUFITzNmel9iX3c

Схема базы данных доступна по адресам:

 - JPG https://drive.google.com/open?id=0B0v_-i-STs5bM19xRDhJYWlIZ00
 - PDF http:https://drive.google.com/open?id=0B0v_-i-STs5bLWtGWTA5NEh2TVE
