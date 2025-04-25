log_analizer/
├── __init__.py
├── cli.py                 # CLI-интерфейс
├── main.py                # Точка входа
├── core/                  # Основная бизнес-логика
│   ├── __init__.py
│   ├── base.py            # Базовые классы и интерфейсы
│   ├── parser.py          # LogParser, который читает строки
│   ├── django_parser.py   # Специализированный парсер логов
│   ├── stats_collector.py # Логика сбора статистики
│   ├── stats_merger.py    # Логика слияния статистик
│   └── report_factory.py  # Логика генерации отчётов
├── reports/               # Отчёты (в т.ч. новые типы в будущем)
│   ├── __init__.py
│   └── handlers.py        # Отчёт по хендлерам
├── tests/                 # Тесты
│   └── __init__.py
├── logs/                  # Логи для примера (или fixtures)
│   ├── app1.log
│   ├── app2.log
│   └── app3.log
├── README.md
├── .gitignore
├── poetry.lock
└── pyproject.toml