Итоговый проект по курсу "Backend-Разработчик". Выполнил Степанов А. А.
# Инструкция по запуску
Склонировать репозиторий
```
git clone https://github.com/Vispers0/foodgram-st
```
Перейти в директорию infra
```
cd ./footgram-st/infra
```
Запустить контейнеры docker
```
docker-compose up --build
```
Применить миграции
```
docker-compose exec backend python manage.py migrate
```
Загрузить данные об ингредиентах
```
curl -X http://localhost/loaddata
```
После вышеуказанных действий приложение будет доступно по адресу http://localhost/