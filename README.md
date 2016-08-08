# forum
Forum app

После выполнения manage.py syncdb необходимо запустить на выполнение скрипт init_db.py:

```
python init_db.py
```

Этот скрипт загрузит в базу данные о странах и городах.

Данные взяты из этого поста: https://habrahabr.ru/post/21949/

Описание API:

```
# Страны и города
GET /api/countries/ #список стран
GET /api/countries/id/ #страна с идентификатором "id"
GET /api/countries/id/cities/ #города страны с идентификатором "id"

# Категории и посты
GET /api/categories/ #получить список категорий
POST /api/categories/ #добавить категорию
GET /api/categories/id/ #получить категорию с идентификатором "id"
GET /api/categories/id/posts/ #получить все посты в категории с идентификатором "id"
POST /api/categories/id/posts/ #добавить пост в категорию с идентификатором "id"
GET /api/posts/ #получить список всех постов
GET /api/posts/id/ #получить пост с идентификатором "id"
