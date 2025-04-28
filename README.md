# LogAnalyzer

**LogAnalyzer** — это CLI-инструмент для анализа логов с возможностью генерации настраиваемых отчётов.

---

## Структура проекта

```
LogParser/
├── log_analizer/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── parser.py
│   │   └── report_factory.py
│   ├── reports/
│   │   ├── plugins/
│   │   │   ├── __init__.py
│   │   │   └── django_handlers.py
│   │   └── __init__.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_log_processor.py
│   │   ├── test_parser.py
│   │   └── test_plugin.py
│   ├── __init__.py
│   └── main.py
├── README.md
├── pytest.ini
└── requirements.txt

```

---

## Установка и запуск

1. **Создать виртуальное окружение** (если еще не создано):

```bash
python -m venv .venv
```

2. **Активировать виртуальное окружение**:

- На Linux/macOS:

```bash
source .venv/bin/activate
```

- На Windows:

```bash
.venv\Scriptsctivate
```

3. **Установить зависимости**:

```bash
pip install -r requirements.txt
```

4. **Запустить анализ логов (прописать путь к логам)**:

```bash
python -m log_analizer.main app1.log app2.log --report handlers
```

---

## Доступные отчёты

- `handlers` — группирует записи `django.request` по эндпоинтам, считает количество по уровням логов, сортирует по
  убыванию ошибок и добавляет итоговую строку.

---

## Тестирование

Запуск всех тестов:

```bash
pytest
```

---

## Пример расширения

Чтобы добавить новый тип отчёта:

Создайте новый файл в `reports/plugins`, реализующий классы, наследующиеся от абстрактных:
`LogRecord`,
`BaseStatsCollector`,
`BaseLineParser`,
`BaseReport`,
.

---
