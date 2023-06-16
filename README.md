# img_app

Приложение для поиска изображений и по ключевым словам и цвету, с возможностью добавлять изображения в избранное и составлять из них коллекции.

## Стэк

- Frontend: React, Redux, AntDesign

- Backend: Django, DRF, SQLite, Swagger

- Devops: Docker, NGINX

## Сбор и предобработка данных

Чтобы наполнить базу данных изображениями, я воспользовался [открым датасетом Unsplash](https://github.com/unsplash/datasets). Таким образом в приложении доступно 25К изображений, которые можно легально использовать. 

Для того, чтобы сделать сортировку по цвету, мной был написан скрипт, который с помощью [библиотеки ColorThief](https://pypi.org/project/colorthief/) определяет основной цвет, далее считает евклидово расстояние до цветов RGB, CMYK и белого. Далее по этому расстоянию можно сортировать изображения.

## Запуск

Запустить приложение можно командой

```bash
docker-compose up
```

Документация доступна по адресу `/doc/swagger`