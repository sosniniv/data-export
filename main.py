import pandas as pd
import sqlite3
import logging
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Глобальные переменные для хранения пути к выбранным файлам
selected_file = ""
selected_db = ""

# Функция для чтения данных из Excel или CSV
def read_data(file_path):
    try:
        if file_path.endswith('.xlsx'):
            logging.info(f"Чтение данных из Excel файла: {file_path}")
            return pd.read_excel(file_path, sheet_name='Лист1')
        elif file_path.endswith('.csv'):
            logging.info(f"Чтение данных из CSV файла: {file_path}")
            return pd.read_csv(file_path)
        else:
            raise ValueError("Поддерживаются только файлы .xlsx и .csv")
    except Exception as e:
        logging.error(f"Ошибка при чтении файла {file_path}: {e}")
        raise

# Подключение к базе данных SQLite
def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

# Создание таблицы в базе данных, если она не существует
def create_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_name TEXT,
        product TEXT,
        quantity INTEGER,
        price REAL,
        status TEXT
    )
    ''')
    logging.info("Таблица 'orders' проверена и создана, если не существовала.")

# Функция для обновления или добавления данных в базу
def update_or_insert_data(cursor, df):
    for index, row in df.iterrows():
        cursor.execute("SELECT 1 FROM orders WHERE order_id = ?", (row['order_id'],))
        if cursor.fetchone() is None:  # Если заказа нет в базе, вставляем новый
            cursor.execute('''
            INSERT INTO orders (order_id, customer_name, product, quantity, price, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (row['order_id'], row['customer_name'], row['product'], row['quantity'], row['price'], row['status']))
            logging.info(f"Добавлен новый заказ с order_id {row['order_id']}.")
        else:  # Если заказ уже существует, обновляем его
            cursor.execute('''
            UPDATE orders
            SET customer_name = ?, product = ?, quantity = ?, price = ?, status = ?
            WHERE order_id = ?
            ''', (row['customer_name'], row['product'], row['quantity'], row['price'], row['status'], row['order_id']))
            logging.info(f"Обновлен заказ с order_id {row['order_id']}.")

# Функция для выбора файла (Excel/CSV)
def choose_file(file_label):
    global selected_file
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
    if file_path:
        selected_file = file_path
        file_label.config(text=f"Выбран файл: {file_path.split('/')[-1]}")
        logging.info(f"Файл выбран: {file_path}")
    else:
        messagebox.showwarning("Ошибка", "Файл не выбран.")

# Функция для выбора базы данных
def choose_db(db_label):
    global selected_db
    db_path = filedialog.askopenfilename(filetypes=[("SQLite files", "*.db")])
    if db_path:
        selected_db = db_path
        db_label.config(text=f"Выбрана база: {db_path.split('/')[-1]}")
        logging.info(f"База данных выбрана: {db_path}")
    else:
        messagebox.showwarning("Ошибка", "База данных не выбрана.")

# Функция для обработки импорта данных
def import_data(file_label, db_label, tree):
    global selected_file, selected_db
    try:
        if not selected_file:
            messagebox.showwarning("Ошибка", "Вы не выбрали файл для импорта.")
            return
        if not selected_db:
            messagebox.showwarning("Ошибка", "Вы не выбрали базу данных.")
            return

        # Чтение данных
        df = read_data(selected_file)

        # Подключение к базе данных
        conn, cursor = connect_db(selected_db)

        # Создание таблицы, если она не существует
        create_table(cursor)

        # Обновление или добавление данных в базу
        update_or_insert_data(cursor, df)

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        # Обновление таблицы интерфейса
        update_table(tree)

        # Уведомление об успешном завершении
        logging.info(f"Данные успешно перенесены в базу данных: {selected_db}")
        messagebox.showinfo("Успех", f"Данные успешно перенесены в базу данных: {selected_db}")
        file_label.config(text="Файл не выбран")
        db_label.config(text="База данных не выбрана")
        selected_file = ""
        selected_db = ""
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Функция для обновления таблицы интерфейса
def update_table(tree):
    global selected_db
    if not selected_db:
        return

    conn, cursor = connect_db(selected_db)
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    conn.close()

    # Очистка таблицы
    for item in tree.get_children():
        tree.delete(item)

    # Заполнение новыми данными
    for row in rows:
        tree.insert("", "end", values=row)

# Создание графического интерфейса
def create_gui():
    root = tk.Tk()
    root.title("Импорт данных в SQLite")

    # Основной фрейм
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Верхняя часть: выбор файлов и базы
    file_label = ttk.Label(main_frame, text="Файл не выбран", font=("Arial", 10))
    file_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    choose_file_button = ttk.Button(main_frame, text="Выбрать файл", command=lambda: choose_file(file_label))
    choose_file_button.grid(row=0, column=1, padx=5, pady=5)

    db_label = ttk.Label(main_frame, text="База данных не выбрана", font=("Arial", 10))
    db_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

    choose_db_button = ttk.Button(main_frame, text="Выбрать базу данных", command=lambda: choose_db(db_label))
    choose_db_button.grid(row=1, column=1, padx=5, pady=5)

    import_button = ttk.Button(main_frame, text="Импортировать данные", command=lambda: import_data(file_label, db_label, tree))
    import_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Нижняя часть: таблица с прокруткой
    table_frame = tk.Frame(root)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree = ttk.Treeview(table_frame, columns=("order_id", "customer_name", "product", "quantity", "price", "status"), show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for col in ("order_id", "customer_name", "product", "quantity", "price", "status"):
        tree.heading(col, text=col)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Кнопка выхода
    exit_button = ttk.Button(root, text="Выход", command=root.quit)
    exit_button.pack(pady=5)

    root.geometry("600x500")
    root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    create_gui()
