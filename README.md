# 🚗 Парковочная система API 🌟

**Управляйте клиентами, парковками и отслеживайте заезды/выезды с помощью этого простого и мощного API!**

---

## 📚 Описание проекта

Это **Flask-приложение** предоставляет REST API для управления парковочной системой. Возможности:

- 🧑💼 **Клиенты**: Создание, просмотр информации о клиентах
- 🟥 **Парковки**: Добавление новых парковочных зон, отслеживание свободных мест
- ⏱️ **Логирование**: Фиксация времени заезда/выезда
- 🔒 **Валидация**: Проверка доступности мест перед заездом

**Технологический стек**:
- Python 3.10 🐍
- Flask 🌐
- SQLAlchemy 🛂
- GitHub Actions 🛠️ (CI с линтингом и тестами)

---

## 🚀 Быстрый старт

### ⚙️ Предварительные требования
- Python 3.10+
- pip (менеджер пакетов Python)
- Git (для клонирования репозитория)

### ⬇️ Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/parking-system.git
   cd parking-system
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

### 🤧 Конфигурация
Создайте файл `.env` в корне проекта:
   ```ini
   FLASK_APP=app
   FLASK_ENV=development
   DATABASE_URL=sqlite:///parking.db
   ```

### 🏃 Запуск приложения
```bash
flask run
```
Сервер будет доступен по адресу: [http://localhost:5000](http://localhost:5000)

### 🧪 Тестирование
Запуск всех тестов:
```bash
pytest tests/ -v
```

Запуск тестов парковки:
```bash
pytest tests/ -v -m parking
```

Проверка качества кода:
```bash
mypy app/                 # Статический анализ типов
black --check --diff app/ # Форматирование
isort --check-only app/   # Сортировка импортов
flake8 app/               # Линтинг
```

---

## 🐝 Примеры API запросов (cURL)

### 🧑💼 Клиенты
Создать клиента:
```bash
curl -X POST http://localhost:5000/clients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Иван",
    "surname": "Иванов",
    "credit_card": "1234-5678-9012-3456",
    "car_number": "A123BC"
  }'
```

Получить всех клиентов:
```bash
curl http://localhost:5000/clients
```

### 🟥 Парковки
Создать парковку:
```bash
curl -X POST http://localhost:5000/parkings \
  -H "Content-Type: application/json" \
  -d '{
    "address": "ул. Ленина, 1",
    "count_places": 50
  }'
```

### ⏱️ Логирование
Заезд на парковку:
```bash
curl -X POST http://localhost:5000/client_parkings \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "parking_id": 1
  }'
```

Выезд с парковки:
```bash
curl -X DELETE http://localhost:5000/client_parkings \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "parking_id": 1
  }'
```

---

## 🛠️ Техническое обслуживание

### Инициализация БД
При первом запуске автоматически создается SQLite база в файле `instance/parking.db`.

### Миграции
Для сложных изменений схемы БД используйте:
```bash
flask db init       # Только при первой настройке
flask db migrate -m "Описание изменений"
flask db upgrade
```

---

## 🤝 Участие в разработке
1. Форкните репозиторий
2. Создайте ветку для фичи/исправления
3. Запустите линтеры перед коммитом:
   ```bash
   black app/    # Автоформатирование
   isort app/    # Сортировка импортов
   ```
4. Создайте Pull Request

---

## 📝 Лицензия
MIT License © 2024 [Ваше имя]. Подробности в файле `LICENSE`.

🚨 Если возникли проблемы, создайте Issue в репозитории.

🌟 Не забудьте поставить звезду, если проект вам понравился!

