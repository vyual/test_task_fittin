# Fittin Test Task E-commerce backend (использован boilerplate https://github.com/vyual/django_boilerplate)

# Пошаговый деплой

1. ```git clone https://github.com/vyual/test_task```
2. ```cd test_task/```
3. Создаете файл окружения ```cp .env.dist .env```
4. Изменяете ```nano .env```
5. Указываете переменные окружения
6. ```sudo apt install certbot python3-certbot-nginx```
7. Получаем сертификат Let's Encrypt ```sudo certbot certonly --nginx -d example.ru --config-dir ssl/```
8. ```docker compose up -d --build```
9. Мигрируем базу данных ```docker compose exec web python manage.py migrate --settings=test_task.settings.prod```
10. Создаем суперпользователя```docker compose exec web python manage.py createsuperuser```

# Запуск окружения разработчика

1. ```git clone https://github.com/vyual/test_task```
2. ```cd test_task/```
3. ```docker compose -f docker-compose-dev.yml up```
4. Мигрируйте базу и создайте суперпользователя

## CI CD

https://gist.github.com/s-lyn/81767ed6c67138eaba681d7739a9db61

## Инструкции по деплою (НЕ ПО ШАГАМ)

- Настроить переменные Github actions secret
- ЕСЛИ ОШИБКА ДОСТУПА К ФАЙЛУ wait-for-it.sh

```
chmod +x wait-for-it.sh 
```

- Получение сертификата

```
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d example.ru --config-dir ssl/
```
- Переменные GITHUB_ACTIONS (**В ДАННОМ ТЕСТОВОМ ЗАДАНИИ ПОЛНОЦЕННЫЙ CI/CD НЕ РЕАЛИЗОВАН**) Параметры актуальны и для Gitlab
``` 
SSH_PRIVATE_KEY - приватный ключ
SSH_HOST - хост сервера
SSH_USER - пользователь
GIT_USER - пользователь Git
GIT_TOKEN - git token пользователя
```
- Миграция бд sqlite -> postgresql
```
./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
./manage.py loaddata db.json
```
- Сбор статики
```
docker compose exec web python manage.py collectstatic --settings=test_task.settings.prod
```
- Ошибки с loaddata
https://stackoverflow.com/questions/42125730/how-to-manage-py-loaddata-in-django



## Возможен также деплой с траефик, для этого нужна развернутая сеть Traefik на сервере

```
docker compose -f docker-compose-traefik.yml up --build -d
```
