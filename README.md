
```markdown
# Инструмент визуализации графа зависимостей

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

**<img width="1235" height="360" alt="image" src="https://github.com/user-attachments/assets/80441f51-5fe1-455a-b112-8f316976c5ca" />
**
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

**<img width="1216" height="404" alt="image" src="https://github.com/user-attachments/assets/ea28523c-f9d7-41ba-bb5a-328fb19dc3e9" />
**
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
| `test_invalid_json.json` | Некорректный JSON | `<img width="1230" height="217" alt="image" src="https://github.com/user-attachments/assets/5c31bc6d-7026-4df0-92bb-8d541531a23d" />
` |
| `test_missing_keys.json` | Отсутствуют обязательные ключи | `<img width="1725" height="192" alt="image" src="https://github.com/user-attachments/assets/47620386-2fa2-4e14-a60f-b4ecd8804e70" />
` |
| `test_invalid_name.json` | Имя содержит не латинские символы | `<img width="1402" height="199" alt="image" src="https://github.com/user-attachments/assets/c86b6b93-ba9c-449d-9b42-0bf8e80b6321" />
` |
| `test_invalid_mode.json` | Недопустимый режим | `<img width="1242" height="230" alt="image" src="https://github.com/user-attachments/assets/60a9ead6-74e9-473c-881b-b8ec1ed48d05" />
` |
| `test_invalid_url.json` | Невалидный URL | `<img width="1383" height="216" alt="image" src="https://github.com/user-attachments/assets/83bdc816-f311-4c41-bb48-92f5f2df0bd8" />
` |
| `test_invalid_path.json` | Не существующий локальный путь | `<img width="1223" height="244" alt="image" src="https://github.com/user-attachments/assets/e52ff6c1-1700-41af-a044-b3da271cf94b" />
` |
| `test_invalid_version.json` | Неверный формат версии | `<img width="1243" height="255" alt="image" src="https://github.com/user-attachments/assets/5fefe9a0-9d77-44bf-a220-6a64ae07b410" />
` |
| `test_negative_depth.json` | Отрицательная глубина | `<img width="1284" height="232" alt="image" src="https://github.com/user-attachments/assets/92aaec7b-ff79-43b3-8594-fa14e291711a" />
` |

