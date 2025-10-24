# 🎓 Grade View ETIS

**Grade** View ETIS — это веб-приложение для анализа оценок студентов через систему **ETIS**.
Оно позволяет авторизоваться, загрузить данные об успеваемости и получить наглядные графики, статистику и экспорт отчётов в различных форматах.

## 🚀 Возможности

- 🔐 Авторизация через ЕТИС (по логину и паролю)
- 📊 Просмотр и анализ всех оценок по предметам и семестрам
- 📈 Графики динамики успеваемости и средних баллов
- 📁 Экспорт данных в:
    - CSV
    - XLSX (Excel)
    - PNG (графики)
- ⚡ Быстрая визуализация и понятный интерфейс

## 🖥️ Технологии

### Backend

- Python 3.9
- FastAPI
- Pandas
- Matplotlib

### Frontend

- Nuxt 3
- TypeScript
- TailwindCSS
- Nuxt UI
- Nuxt Charts

## ⚙️ Установка и запуск

### Клонирование проекта

```bash
git clone https://github.com/sayranovv/grade-view-etis
```

### Backend

1. Перейдите в папку server:

```bash
cd server
```

2. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

3. Запустите сервер:

```bash
fastapi dev main.py
```

После запуска сервер будет доступен по адресу:

```bash
http://localhost:8000
```

### Frontend

1. Перейдите в папку client:

```bash
cd client
```

2. Установите зависимости:

```bash
npm i
```

3. Запустите сервер разработки:

```bash
npm run dev
```

Приложение откроента по адресу:

```bash
http://localhost:3000
```