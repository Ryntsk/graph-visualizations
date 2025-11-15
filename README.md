
```markdown
# Инструмент визуализации графа зависимостей

Этот проект представляет собой инструмент для анализа и визуализации графа зависимостей пакетов, разработанный в рамках учебного задания. Инструмент реализуется поэтапно с использованием Python, избегая готовых менеджеров пакетов и библиотек для получения зависимостей. Все этапы сохраняются в Git-репозитории.

## Этап 1: Минимальный прототип с конфигурацией

### Цель
Создать минимальное CLI-приложение, которое:
- Читает параметры из JSON-файла.
- Валидирует их (имя пакета, URL/путь к репозиторию, режим работы, версия, максимальная глубина).
- Выводит параметры в формате `key: value`.
- Обрабатывает и демонстрирует ошибки для всех параметров.

### Требования
1. Конфигурация хранится в JSON-файле.
2. Параметры:
   - `package_name`: Имя пакета (только латинские буквы, цифры, дефисы, подчеркивания).
   - `repository_url_or_path`: URL репозитория (режим `"download"`) или путь к файлу/папке (режим `"local"`).
   - `repository_mode`: Только `"download"` или `"local"`.
   - `package_version`: Версия в формате `x.y.z` или `x.y.z-...`.
   - `max_depth`: Целое число больше 0.
3. Вывод параметров в формате `key: value` (только для этого этапа).
4. Обработка ошибок для всех параметров с демонстрацией.
5. Результат сохранён в Git с коммитом.

### Инструкции по запуску
1. Убедитесь, что установлен Python 3.6+.
2. Сохраните конфигурационный файл (например, `config.json`) в корне проекта.
3. Запустите скрипт:
```
```bash
python app.py config.json
```

Или настройте запуск в PyCharm:
- Откройте **Run/Debug Configurations**.
- Укажите **Script path**: `app.py`.
- Укажите **Script parameters**: `config.json`.
- Укажите **Working directory**: путь к корню проекта (например, `D:/Конфигурационное управление/`).
- Нажмите **Run**.

### Пример конфигурации

#### Валидный `config.json`
```json
{
  "package_name": "serde",
  "repository_url_or_path": "https://github.com/serde-rs/serde.git",
  "repository_mode": "download",
  "package_version": "1.0.0",
  "max_depth": 3
}
```

**Вывод:**
```
package_name: serde
repository_url_or_path: https://github.com/serde-rs/serde.git
repository_mode: download
package_version: 1.0.0
max_depth: 3
```

#### Валидный `config_local.json` (режим `"local"`)
```json
{
  "package_name": "A",
  "repository_url_or_path": "test_graph.txt",
  "repository_mode": "local",
  "package_version": "1.0.0",
  "max_depth": 3
}
```
> Требуется файл `test_graph.txt` в корне проекта.

**Вывод:**
```
package_name: A
repository_url_or_path: test_graph.txt
repository_mode: local
package_version: 1.0.0
max_depth: 3
```

### Тестирование ошибок

Для демонстрации обработки ошибок созданы тестовые конфигурации в папке `test_configs`.

| Файл | Описание | Ожидаемая ошибка |
|------|----------|------------------|
| `test_invalid_json.json` | Некорректный JSON | `Error: Config file contains invalid JSON` |
| `test_missing_keys.json` | Отсутствуют обязательные ключи | `Error: Config missing required keys: ...` |
| `test_invalid_name.json` | Имя содержит не латинские символы | `Error: package_name must contain only Latin letters, digits, hyphens, or underscores` |
| `test_invalid_mode.json` | Недопустимый режим | `Error: repository_mode must be 'download' or 'local'` |
| `test_invalid_url.json` | Невалидный URL | `Error: repository_url_or_path must be a valid URL starting with http:// or https://` |
| `test_invalid_path.json` | Не существующий локальный путь | `Error: repository_url_or_path must point to an existing local path` |
| `test_invalid_version.json` | Неверный формат версии | `Error: package_version must be in format like 'x.y.z' or 'x.y.z-...'` |
| `test_negative_depth.json` | Отрицательная глубина | `Error: max_depth must be a positive integer` |

