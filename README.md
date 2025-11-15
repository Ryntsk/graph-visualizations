
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

| Файл | Описание | Ошибка |
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

Конечно! Ниже приведено обновлённое содержимое `README.md`, включающее описание **Этапа 2: Сбор данных**. Оно оформлено в стиле, совместимом с предыдущим этапом, и готово к использованию в вашем Git-репозитории.

```markdown
# Инструмент визуализации графа зависимостей

Этот проект представляет собой инструмент для анализа и визуализации графа зависимостей пакетов, разработанный в рамках учебного задания. Инструмент реализуется поэтапно с использованием Python, избегая готовых менеджеров пакетов и библиотек для получения зависимостей. Все этапы сохраняются в Git-репозитории.

## Этап 1: Минимальный прототип с конфигурацией

*(Описание Этапа 1 см. в предыдущих коммитах или в истории README.)*

---

Конечно! Вот обновлённое описание **Этапа 2: Сбор данных** в стиле, полностью соответствующем вашему формату и содержанию:

---

## Этап 2: Сбор данных

### Цель
Реализовать основную логику получения данных о зависимостях для их дальнейшего анализа и визуализации.

### Требования
1. Использовать формат пакетов Rust (Cargo).
2. Информацию получить для заданной пользователем версии пакета.
3. Извлечь информацию о прямых зависимостях заданного пакета, используя URL-адрес репозитория.
4. Вывести на экран все прямые зависимости (только для этого этапа).
5. Результат сохранён в Git.

### Пример конфигурации

#### Валидный `config.json`
```json
{
  "package_name": "serde_json",
  "repository_url_or_path": "https://github.com/serde-rs/json.git",
  "repository_mode": "download",
  "package_version": "1.0.0",
  "max_depth": 3
}
```

**<img width="1228" height="754" alt="image" src="https://github.com/user-attachments/assets/e15ae8bd-0c16-48eb-bb4d-386e3b81fed6" />
**
```
Configuration:
package_name: serde_json
repository_url_or_path: https://github.com/serde-rs/json.git
repository_mode: download
package_version: 1.0.0
max_depth: 3

Cloning repository...
Checking out version 1.0.0...

Direct dependencies:
dtoa = "0.4"
num-traits = "0.1.32"
serde = "1.0"
```

> Вывод основан на содержимом файла `Cargo.toml` в репозитории `serde-rs/json` на теге `1.0.0`.

### Тестирование

- **Успешный случай**:репозиторий `serde-json` с версией `1.0.99`.  
  **Вывод:**  
  `<img width="1226" height="720" alt="image" src="https://github.com/user-attachments/assets/3bb581a4-5a02-4c44-b49e-fb12e081ffa5" />
`

- **Ошибка: Отсутствие тега версии**  
  Конфиг:
  ```json
  { "package_version": "999.0.0", ... }
  ```  
  **Вывод:**  
  `<img width="1221" height="600" alt="image" src="https://github.com/user-attachments/assets/51eaf95d-244c-40ee-b60f-834384ef2a44" />
`

- **Ошибка: Отсутствие Cargo.toml**  
  Используется репозиторий без `Cargo.toml` в корне указанной версии.  
  **Вывод:**  
  `<img width="1248" height="459" alt="image" src="https://github.com/user-attachments/assets/ee408bf7-4eda-473f-88e4-7aee9fa70491" />
`

- **Ошибка: Неверный URL**  
  Конфиг:
  ```json
  { "repository_url_or_path": "https://invalid.git", ... }
  ```  
  **Вывод:**  
  `<img width="1547" height="458" alt="image" src="https://github.com/user-attachments/assets/da10f397-4ff1-44c7-b360-42143613c84e" />
`

- **Ошибка: Неверный режим**  
  Конфиг:
  ```json
  { "repository_mode": "local", ... }
  ```  
  **Вывод:**  
  `<img width="1238" height="208" alt="image" src="https://github.com/user-attachments/assets/eadd0615-2f87-4ef1-a734-f611b6726b40" />
`

- **Ошибка: Неверное имя пакета**  
  Конфиг:
  ```json
  { "package_name": "серде_json", ... }
  ```  
  **Вывод:**  
  `<img width="1431" height="193" alt="image" src="https://github.com/user-attachments/assets/b05e751a-cb34-41d6-b6ef-d173c6af3732" />
`


