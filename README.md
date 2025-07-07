# NSFW-Moderator (FastAPI + NudeDetector)

Сервис на FastAPI, который автоматом проверяет изображение на NSFW-контент локальной моделью NudeDetector.

## Возможности
- Эндпоинт `POST /moderate`, принимает `.jpg` или `.png`.
- Решение OK или REJECTED по максимальному score модели.
- Порог 0.7 зашит в `main.py`.
- Полностью офлайн – модель скачивается один раз при первом старте.
- Есть Dockerfile и docker-compose.

## Быстрый старт без Docker
```bash
git clone https://github.com/yourname/nsfw-moderator.git
cd nsfw-moderator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload        # http://localhost:8000
```

## Запуск в Docker

```bash
docker compose up --build        # интерактив
# или
docker compose up -d --build     # в фоне
```

Порт 8000 на хосте должен быть свободен. Если занят – поменяй маппинг в `docker-compose.yml`, например `8010:8000`.

## Тестовые изображения

В репозитории уже лежат четыре файла:

| Имя                   | Описание                      | Ожидание         |
| --------------------- | ----------------------------- | ---------------- |
| `cat.jpg`             | Домашний кот                  | `OK`             |
| `landscape.jpg`       | Пейзаж                        | `OK`             |
| `bikini.jpg`          | Девушка в бикини (погранично) | зависит от score |
| `nude_modigliani.jpg` | Картина Модильяни с наготой   | `REJECTED`       |

Проверить так:

```bash
curl -X POST -F "file=@cat.jpg" http://localhost:8000/moderate
curl -X POST -F "file=@nude_modigliani.jpg" http://localhost:8000/moderate
```

## Как это работает

1. Файл приходит на `/moderate`, проверяем MIME-тип.
2. Пишем байты во временный файл – NudeDetector принимает только путь.
3. `detector.detect()` отдаёт список объектов с `class`, `score`, `box`.
4. Берём максимальный `score`. Если он больше 0.7 – REJECTED.
5. Временный файл удаляется, клиент получает JSON.

## Состав проекта


```text
nsfw-moderator/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── cat.jpg
├── landscape.jpg
├── bikini.jpg
└── nude_modigliani.jpg
```


## Заметки

* В requirements зафиксирован `numpy<2`, иначе OpenCV падает.
* Если нужен другой порог – поменяй `THRESHOLD` в `main.py`.
* Код без внешних ключей и ограничений.




