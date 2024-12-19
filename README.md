# Импорт данных из excel в SQLite

Это приложение предназначено для импорта данных из файлов Excel (.xlsx) или CSV в базу данных SQLite. Программа предоставляет простой графический интерфейс на основе Tkinter для выбора файла и базы данных, а затем переноса данных в базу.

## Функции приложения

### 1. `read_data(file_path)`
Функция для чтения данных из файла (Excel или CSV).

- **Параметры**: 
  - `file_path` (str): Путь к файлу для чтения.
- **Возвращает**: 
  - DataFrame, содержащий данные из файла.
- **Описание**: 
  Функция проверяет расширение файла. Если это Excel файл (`.xlsx`), используется `pandas.read_excel`, если это CSV файл (`.csv`), используется `pandas.read_csv`. Если формат файла не поддерживается, возникает исключение.

### 2. `connect_db(db_name)`
Функция для подключения к базе данных SQLite.

- **Параметры**:
  - `db_name` (str): Путь к файлу базы данных SQLite.
- **Возвращает**:
  - `conn` (sqlite3.Connection): Объект соединения с базой данных.
  - `cursor` (sqlite3.Cursor): Объект для выполнения SQL-запросов.
- **Описание**: 
  Функция устанавливает соединение с базой данных SQLite и возвращает соединение и курсор.

### 3. `create_table(cursor)`
Функция для создания таблицы `orders` в базе данных, если она не существует.

- **Параметры**:
  - `cursor` (sqlite3.Cursor): Курсор для выполнения SQL-запросов.
- **Описание**:
  Эта функция проверяет наличие таблицы `orders` в базе данных и создает ее, если она отсутствует. Таблица содержит поля: `order_id`, `customer_name`, `product`, `quantity`, `price`, `status`.

### 4. `update_or_insert_data(cursor, df)`
Функция для обновления или добавления данных в таблицу базы данных.

- **Параметры**:
  - `cursor` (sqlite3.Cursor): Курсор для выполнения SQL-запросов.
  - `df` (pandas.DataFrame): DataFrame, содержащий данные для добавления или обновления.
- **Описание**:
  Эта функция проверяет, существует ли заказ с данным `order_id` в базе данных. Если заказ существует, он обновляется. Если заказ не найден, он добавляется в таблицу.

### 5. `choose_file(file_label)`
Функция для выбора файла (Excel/CSV) через графический интерфейс.

- **Параметры**:
  - `file_label` (tk.Label): Метка в интерфейсе, которая будет отображать путь к выбранному файлу.
- **Описание**:
  Функция открывает диалоговое окно для выбора файла. Если файл выбран, обновляется текст на метке, отображающий имя выбранного файла. Путь к файлу сохраняется в глобальную переменную `selected_file`.

### 6. `choose_db(db_label)`
Функция для выбора базы данных SQLite через графический интерфейс.

- **Параметры**:
  - `db_label` (tk.Label): Метка в интерфейсе, которая будет отображать путь к выбранной базе данных.
- **Описание**:
  Функция открывает диалоговое окно для выбора файла базы данных. Если база данных выбрана, обновляется текст на метке, отображающий имя базы данных. Путь к базе данных сохраняется в глобальную переменную `selected_db`.

### 7. `import_data(file_label, db_label, tree)`
Функция для обработки импорта данных из выбранного файла в выбранную базу данных.

- **Параметры**:
  - `file_label` (tk.Label): Метка для отображения информации о выбранном файле.
  - `db_label` (tk.Label): Метка для отображения информации о выбранной базе данных.
  - `tree` (tk.Treeview): Виджет для отображения данных в интерфейсе.
- **Описание**:
  Эта функция выполняет все необходимые шаги для импорта данных:
  - Проверяет, был ли выбран файл и база данных.
  - Читает данные из выбранного файла с помощью `read_data`.
  - Подключается к базе данных и создает таблицу, если необходимо.
  - Добавляет или обновляет данные в базе данных с помощью `update_or_insert_data`.
  - Обновляет таблицу на интерфейсе с помощью `update_table`.

### 8. `update_table(tree)`
Функция для обновления данных в таблице на графическом интерфейсе.

- **Параметры**:
  - `tree` (tk.Treeview): Виджет таблицы в интерфейсе.
- **Описание**:
  Функция извлекает все строки из таблицы `orders` базы данных и обновляет содержимое таблицы в интерфейсе. Для каждого заказа из базы данных добавляется новая строка в таблицу.

### 9. `create_gui()`
Функция для создания графического интерфейса приложения с использованием Tkinter.

- **Описание**:
  Эта функция создает основное окно приложения с двумя фреймами: для выбора файла и базы данных, а также для отображения таблицы. В интерфейсе присутствуют следующие элементы:
  - Кнопки для выбора файла и базы данных.
  - Метки для отображения путей к выбранным файлам.
  - Кнопка для импорта данных.
  - Таблица для отображения содержимого базы данных.
  - Кнопка для выхода из приложения.

### 10. `main()`
Главная функция для запуска приложения.
Для запуска кода откройте консоль и пропишите сначала myenv\Scripts\activate потом python main.py

- **Описание**:
  Эта функция вызывает `create_gui()`, которая инициализирует и запускает графический интерфейс приложения.

## Примечания

- Программа использует библиотеки `pandas` для работы с данными и `tkinter` для создания графического интерфейса.
- Логирование выполняется в файл `app.log`, где записываются все ошибки и важные события.
- Важно, чтобы выбранные файлы были в правильном формате (.xlsx для Excel, .csv для CSV, .db для SQLite).
