# src/database/__init__.py

# 1) Спочатку моделі (щоб уникнути циклів)
from .models import (
    Base,
    MovieModel,
    GenreModel,
    ActorModel,
    CountryModel,
    LanguageModel,
)

# 2) Потім утиліти для SQLite-сесії (які використовуються в тестах)
from .session_sqlite import (
    init_db,
    close_db,
    get_db,
    get_sqlite_db_contextmanager as get_db_contextmanager,
    reset_sqlite_database,
    reset_database,  # алиас під тести
)

# 3) (не обов’язково, але корисно) — сідер, якщо десь потрібен
try:
    from .populate import CSVDatabaseSeeder  # noqa: F401
except Exception:
    CSVDatabaseSeeder = None  # опціонально

__all__ = [
    # моделі
    "Base",
    "MovieModel",
    "GenreModel",
    "ActorModel",
    "CountryModel",
    "LanguageModel",
    # сесія / ініт
    "init_db",
    "close_db",
    "get_db",
    "get_db_contextmanager",
    "reset_sqlite_database",
    "reset_database",
    # опц. сідер
    "CSVDatabaseSeeder",
]
