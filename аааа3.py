# Импорт необходимых библиотек
import random
import sqlite3
from datetime import date
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk


PORTRAITS_IMAGES = ["images/3_meal.jpg","images/4_meal.jpg","images/5_meal.jpg","images/6_meal.jpg"]

# Класс для работы с трекингом калорий
class CalorieTracker:
    # Имя файла базы данных
    db_name = 'calories.db'

    # Конструктор класса - создание окна приложения
    def __init__(self, window):
        self.wind = window
        self.wind.title('Веданіе о Питаниѣ')

        # Устанавливаем размер и позицию главного окна (центрируем на экране)
        window_width = 1200
        window_height = 750
        screen_width = self.wind.winfo_screenwidth()
        screen_height = self.wind.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.wind.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.wind.withdraw()
        self.show_splash()

        # Отображение окна поверх других
        self.wind.lift()
        self.wind.attributes('-topmost', True)
        self.wind.after_idle(self.wind.attributes, '-topmost', False)

        # Инициализация базы данных
        self.init_database()

        # Создание вкладок (табов)
        self.notebook = ttk.Notebook(self.wind)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Вторая вкладка - мой рацион
        self.meals_tab = Frame(self.notebook)
        self.notebook.add(self.meals_tab, text='Мой Пиръ')
        self.setup_meals_tab()

        # Первая вкладка - библиотека продуктов
        self.products_tab = Frame(self.notebook)
        self.notebook.add(self.products_tab, text='Книга Яствъ')
        self.setup_products_tab()


    def get_portrait_photo(self):
        query = 'SELECT DISTINCT meal_type FROM meal_records WHERE date = ?'
        db_rows = self.run_query(query, (self.date_var.get(),))
        unique_cnt = len(db_rows)

        if unique_cnt == 0:
            return "images/0_meal.jpg"
        elif unique_cnt == 1:
            return "images/1_meal.jpg"
        elif unique_cnt == 2:
            return "images/2_meal.jpg"
        else:
            return random.choice(PORTRAITS_IMAGES)

    def show_portrait(self):
        self.get_portrait_photo()
        splash = Toplevel()
        splash.title("Образъ")
        splash.geometry("700x700")
        splash.resizable(False, False)

        # Открывать в том же месте, что и главное окно
        self.wind.update_idletasks()
        x = self.wind.winfo_x()
        y = self.wind.winfo_y()
        splash.geometry(f"700x700+{x}+{y}")

        # Загрузка изображения
        image = Image.open(self.get_portrait_photo())
        image = image.resize((700, 600))
        self.splash_image = ImageTk.PhotoImage(image)

        Label(splash, image=self.splash_image).pack()

        # Кнопка
        Button(
            splash,
            text="Так",
            font=("Arial", 14),
            command=lambda: self.close_splash(splash)
        ).pack(pady=20)

        splash.protocol("WM_DELETE_WINDOW", lambda: splash.destroy())

    def show_splash(self):
        splash = Toplevel()
        splash.title("Милостивый посетитель, здравію тебе")
        splash.geometry("1200x750")
        splash.resizable(False, False)

        # Открывать в том же месте, что и главное окно
        self.wind.update_idletasks()
        x = self.wind.winfo_x()
        y = self.wind.winfo_y()
        splash.geometry(f"1200x750+{x}+{y}")

        # Загрузка изображения
        image = Image.open("images/111.jpg")
        image = image.resize((1200, 600))
        self.splash_image = ImageTk.PhotoImage(image)

        Label(splash, image=self.splash_image).pack()

        # Кнопка
        Button(
            splash,
            text="Приступити къ дѣлу",
            font=("Arial", 14),
            command=lambda: self.close_splash(splash)
        ).pack(pady=20)

        splash.protocol("WM_DELETE_WINDOW", lambda: None)

    def close_splash(self, splash):
        splash.destroy()
        self.wind.deiconify()

    # Настройка вкладки с библиотекой продуктов
    def setup_products_tab(self):
        # Рамка для добавления нового продукта
        frame = LabelFrame(self.products_tab, text='Ново яство')
        frame.grid(row=0, column=0, columnspan=4, pady=20, padx=10, sticky=W + E)

        # Поле для ввода названия продукта
        Label(frame, text='Имя яства: ').grid(row=1, column=0, padx=5, pady=5)
        self.name = Entry(frame, width=30)
        self.name.focus()
        self.name.grid(row=1, column=1, padx=5, pady=5)

        # Поле для ввода калорий
        Label(frame, text='Сила питательная на сотню граммъ: ').grid(row=2, column=0, padx=5, pady=5)
        self.calories = Entry(frame, width=30)
        self.calories.grid(row=2, column=1, padx=5, pady=5)

        # Поле для ввода белков
        Label(frame, text='Бѣлки (г на 100г): ').grid(row=1, column=2, padx=5, pady=5)
        self.proteins = Entry(frame, width=30)
        self.proteins.grid(row=1, column=3, padx=5, pady=5)

        # Поле для ввода углеводов
        Label(frame, text='Углеводы (г на 100г): ').grid(row=2, column=2, padx=5, pady=5)
        self.carbs = Entry(frame, width=30)
        self.carbs.grid(row=2, column=3, padx=5, pady=5)

        # Поле для ввода жиров
        Label(frame, text='Жиры (г на 100г): ').grid(row=3, column=2, padx=5, pady=5)
        self.fats = Entry(frame, width=30)
        self.fats.grid(row=3, column=3, padx=5, pady=5)

        # Кнопка для сохранения продукта
        ttk.Button(frame, text='Внести в Книгу яствъ', command=self.add_product).grid(row=3, column=0, columnspan=2,
                                                                                   sticky=W + E, padx=5, pady=10)

        # Метка для вывода сообщений
        self.message = Label(self.products_tab, text='', fg='red')
        self.message.grid(row=1, column=0, columnspan=4, sticky=W + E, padx=10)

        # Таблица для отображения продуктов
        self.tree = ttk.Treeview(self.products_tab, height=10, columns=('calories', 'proteins', 'carbs', 'fats'))
        self.tree.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky=W + E)
        self.tree.heading('#0', text='Яство', anchor=CENTER)
        self.tree.heading('#1', text='Сила питательная', anchor=CENTER)
        self.tree.heading('#2', text='Бѣлки (г)', anchor=CENTER)
        self.tree.heading('#3', text='Углеводы (г)', anchor=CENTER)
        self.tree.heading('#4', text='Жиры (г)', anchor=CENTER)
        self.tree.column('#0', width=200)
        self.tree.column('#1', width=100)
        self.tree.column('#2', width=100)
        self.tree.column('#3', width=120)
        self.tree.column('#4', width=100)

        # Кнопки для управления продуктами
        (ttk.Button(self.products_tab, text='Убрати', command=self.delete_product).
         grid(row=4, column=0, columnspan=2, sticky=W+E, padx=5, pady=5))
        ttk.Button(self.products_tab, text='Переписати', command=self.edit_product).grid(row=4,
                                                                                            column=2,
                                                                                            columnspan=2,
                                                                                            sticky=W + E,
                                                                                            padx=5, pady=5)

        # Заполнение таблицы данными
        self.get_products()

    # Настройка вкладки с рационом
    def setup_meals_tab(self):
        # Рамка для добавления продукта в рацион
        add_frame = LabelFrame(self.meals_tab, text='Вписаніе новаго яства')
        add_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky=W + E)

        # Выбор продукта из списка
        Label(add_frame, text='Яство: ').grid(row=0, column=0, padx=5, pady=5)
        self.product_var = StringVar()
        self.product_combo = ttk.Combobox(add_frame, textvariable=self.product_var, width=27, state='readonly')
        self.product_combo.grid(row=0, column=1, padx=5, pady=5)
        self.update_product_combo()

        # Поле для ввода количества
        Label(add_frame, text='Мера (г): ').grid(row=1, column=0, padx=5, pady=5)
        self.amount = Entry(add_frame, width=30)
        self.amount.grid(row=1, column=1, padx=5, pady=5)

        # Выбор приема пищи
        Label(add_frame, text='Чин: ').grid(row=2, column=0, padx=5, pady=5)
        self.meal_type_var = StringVar(value='Заутрок')
        meal_combo = ttk.Combobox(add_frame, textvariable=self.meal_type_var, width=27, state='readonly')
        meal_combo['values'] = ('Заутрок', 'Обед', 'Вечеря')
        meal_combo.grid(row=2, column=1, padx=5, pady=5)

        # Поле для ввода даты
        Label(add_frame, text='Дѣнь: ').grid(row=3, column=0, padx=5, pady=5)
        self.date_var = StringVar(value=date.today().strftime('%Y-%m-%d'))

        date_entry = DateEntry(add_frame,
                                width=12,
                                background='red',
                                foreground='black',
                                borderwidth=2,
                                date_pattern='yyyy-mm-dd',
                                locale='ru_RU',
                                textvariable=self.date_var,
                               )

        date_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка для добавления в рацион
        ttk.Button(add_frame, text='Вписати яство в пиръ', command=self.add_meal).grid(
            row=4, columnspan=2, sticky=W + E, padx=5, pady=4
        )
        # Кнопка для добавления в рацион
        ttk.Button(add_frame, text='Ведати Образъ', command=self.show_portrait).grid(
            row=5, columnspan=2, sticky=W + E, padx=5, pady=4
        )

        # Кнопки удаления и очистки дня
        ttk.Button(add_frame, text='Убрати запись', command=self.delete_meal).grid(
            row=6, column=0, columnspan=2, sticky=W + E, padx=5, pady=2
        )

        ttk.Button(add_frame, text='Очистить день', command=self.clear_day).grid(
            row=7, column=0, columnspan=2, sticky=W + E, padx=5, pady=2
        )

        # Метка для вывода сообщений
        self.meal_message = Label(self.meals_tab, text='', fg='red')
        self.meal_message.grid(row=1, column=0, columnspan=2, sticky=W + E, padx=10)

        # Рамка для итоговой статистики
        summary_frame = LabelFrame(self.meals_tab, text='Итоги за денъ')
        summary_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky=W + E)
        self.summary_label = Label(summary_frame, text='', font=('Arial', 11))
        self.summary_label.grid(row=0, column=0, padx=10, pady=10)

        # Таблица для отображения записей рациона
        self.meals_tree = ttk.Treeview(self.meals_tab, height=12,
                                       columns=('amount', 'calories', 'proteins', 'carbs', 'fats', 'meal_type', 'date'))
        self.meals_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=W + E + N + S)
        self.meals_tree.heading('#0', text='Яство', anchor=CENTER)
        self.meals_tree.heading('#1', text='Мера (г)', anchor=CENTER)
        self.meals_tree.heading('#2', text='Сила', anchor=CENTER)
        self.meals_tree.heading('#3', text='Бѣлки (г)', anchor=CENTER)
        self.meals_tree.heading('#4', text='Углеводы (г)', anchor=CENTER)
        self.meals_tree.heading('#5', text='Жиры (г)', anchor=CENTER)
        self.meals_tree.heading('#6', text='Чин', anchor=CENTER)
        self.meals_tree.heading('#7', text='Дѣнь', anchor=CENTER)
        self.meals_tree.column('#0', width=130)
        self.meals_tree.column('#1', width=90)
        self.meals_tree.column('#2', width=70)
        self.meals_tree.column('#3', width=80)
        self.meals_tree.column('#4', width=100)
        self.meals_tree.column('#5', width=80)
        self.meals_tree.column('#6', width=90)
        self.meals_tree.column('#7', width=100)

        # Полоса прокрутки для таблицы
        scrollbar = ttk.Scrollbar(self.meals_tab, orient=VERTICAL, command=self.meals_tree.yview)
        scrollbar.grid(row=3, column=2, sticky=N + S)
        self.meals_tree.configure(yscrollcommand=scrollbar.set)

        # Кнопки для управления записями

        ttk.Button(self.meals_tab, text='Убрати', command=self.delete_meal).grid(row=5, column=0, columnspan=2,
                                                                                         sticky=W + E, padx=5, pady=5)
        ttk.Button(self.meals_tab, text='Переписати', command=self.refresh_meals).grid(row=6, column=0, columnspan=2,
                                                                                     sticky=W + E, padx=5, pady=5)

        # Заполнение таблицы данными
        self.get_meals()

    # Инициализация базы данных
    def init_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Создание таблицы продуктов
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS products
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               name
                               TEXT
                               NOT
                               NULL,
                               calories_per_100g
                               REAL
                               NOT
                               NULL,
                               proteins_per_100g
                               REAL
                               DEFAULT
                               0,
                               carbs_per_100g
                               REAL
                               DEFAULT
                               0,
                               fats_per_100g
                               REAL
                               DEFAULT
                               0
                           )
                           ''')

            # Создание таблицы записей о приемах пищи
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS meal_records
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               product_id
                               INTEGER
                               NOT
                               NULL,
                               product_name
                               TEXT
                               NOT
                               NULL,
                               amount_g
                               REAL
                               NOT
                               NULL,
                               calories
                               REAL
                               NOT
                               NULL,
                               proteins
                               REAL
                               DEFAULT
                               0,
                               carbs
                               REAL
                               DEFAULT
                               0,
                               fats
                               REAL
                               DEFAULT
                               0,
                               meal_type
                               TEXT
                               NOT
                               NULL,
                               date
                               TEXT
                               NOT
                               NULL
                           )
                           ''')

            # Проверка, есть ли уже продукты в базе
            cursor.execute('SELECT COUNT(*) FROM products')
            count = cursor.fetchone()[0]

            # Если база пустая, добавляем библиотеку продуктов
            if count == 0:
                # Библиотека продуктов
                products = {
                    "Ржаной хлеб": {"calories": 210, "proteins": 6.0, "fats": 1.2, "carbs": 44.0},
                    "Пшеничный хлеб": {"calories": 265, "proteins": 8.0, "fats": 1.5, "carbs": 49.0},
                    "Гречневая каша": {"calories": 110, "proteins": 4.5, "fats": 1.6, "carbs": 21.0},
                    "Пшённая каша": {"calories": 115, "proteins": 3.8, "fats": 1.3, "carbs": 23.0},
                    "Пшеничная каша": {"calories": 120, "proteins": 3.5, "fats": 1.1, "carbs": 25.0},
                    "Овсяная каша": {"calories": 120, "proteins": 4.0, "fats": 2.5, "carbs": 20.0},
                    "Репа": {"calories": 32, "proteins": 1.5, "fats": 0.1, "carbs": 6.0},
                    "Капуста": {"calories": 28, "proteins": 1.8, "fats": 0.1, "carbs": 5.4},
                    "Морковь": {"calories": 41, "proteins": 0.9, "fats": 0.2, "carbs": 10.0},
                    "Свёкла": {"calories": 43, "proteins": 1.6, "fats": 0.2, "carbs": 10.0},
                    "Лук репчатый": {"calories": 41, "proteins": 1.4, "fats": 0.0, "carbs": 9.3},
                    "Чеснок": {"calories": 143, "proteins": 6.4, "fats": 0.5, "carbs": 33.0},
                    "Картофель": {"calories": 77, "proteins": 2.0, "fats": 0.1, "carbs": 17.0},
                    "Говядина варёная": {"calories": 250, "proteins": 26.0, "fats": 17.0, "carbs": 0.0},
                    "Свинина": {"calories": 290, "proteins": 21.0, "fats": 24.0, "carbs": 0.0},
                    "Баранина": {"calories": 294, "proteins": 25.0, "fats": 21.0, "carbs": 0.0},
                    "Курица варёная": {"calories": 165, "proteins": 31.0, "fats": 3.6, "carbs": 0.0},
                    "Яйцо куриное": {"calories": 155, "proteins": 13.0, "fats": 11.0, "carbs": 1.1},
                    "Рыба сушёная": {"calories": 180, "proteins": 40.0, "fats": 3.0, "carbs": 0.0},
                    "Рыба солёная": {"calories": 190, "proteins": 20.0, "fats": 12.0, "carbs": 0.0},
                    "Икра": {"calories": 264, "proteins": 24.0, "fats": 18.0, "carbs": 4.0},
                    "Сало": {"calories": 899, "proteins": 1.0, "fats": 100.0, "carbs": 0.0},
                    "Мёд": {"calories": 330, "proteins": 0.8, "fats": 0.0, "carbs": 82.0},
                    "Квас": {"calories": 27, "proteins": 0.2, "fats": 0.0, "carbs": 5.0},
                    "Молоко коровье": {"calories": 60, "proteins": 3.2, "fats": 3.3, "carbs": 5.0},
                    "Сметана": {"calories": 200, "proteins": 2.0, "fats": 20.0, "carbs": 3.0},
                    "Творог": {"calories": 98, "proteins": 11.0, "fats": 5.0, "carbs": 3.0},
                    "Сыр": {"calories": 350, "proteins": 25.0, "fats": 28.0, "carbs": 1.5},
                    "Орехи (грецкие)": {"calories": 654, "proteins": 15.0, "fats": 65.0, "carbs": 14.0},
                    "Ягоды (черника)": {"calories": 57, "proteins": 0.7, "fats": 0.3, "carbs": 14.5},
                    "Ягоды (малина)": {"calories": 52, "proteins": 1.2, "fats": 0.5, "carbs": 12.0},
                    "Сушёные фрукты (яблоки)": {"calories": 243, "proteins": 1.4, "fats": 0.3, "carbs": 65.0},
                    "Сушёные фрукты (груши)": {"calories": 242, "proteins": 1.0, "fats": 0.4, "carbs": 63.0},
                    "Морская капуста": {"calories": 45, "proteins": 1.5, "fats": 0.5, "carbs": 9.0}
                }

                # Преобразование словаря в список кортежей для вставки в базу
                sample_products = []
                for name, data in products.items():
                    sample_products.append((
                        name,
                        data["calories"],
                        data["proteins"],
                        data["carbs"],
                        data["fats"]
                    ))

                # Вставка всех продуктов в базу данных
                cursor.executemany('''
                                   INSERT INTO products (name, calories_per_100g, proteins_per_100g, carbs_per_100g,
                                                         fats_per_100g)
                                   VALUES (?, ?, ?, ?, ?)
                                   ''', sample_products)

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Ошибка при инициализации базы данных: {e}")
            import traceback
            traceback.print_exc()

    # Выполнение SQL запросов
    def run_query(self, query, parameters=()):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        # Если это SELECT запрос, возвращаем результаты (commit не нужен)
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
            conn.close()
            return result
        # Для остальных запросов (INSERT, UPDATE, DELETE) делаем commit
        else:
            conn.commit()
            conn.close()

    # Получение списка продуктов из базы данных
    def get_products(self):
        # Очистка таблицы
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Получение данных из базы
        query = 'SELECT * FROM products ORDER BY name ASC'
        db_rows = self.run_query(query)

        # Заполнение таблицы
        for row in db_rows:
            # Структура строки: (id, name, calories, proteins, carbs, fats)
            calories = float(row[2])
            proteins = float(row[3]) if len(row) > 3 and row[3] is not None else 0.0
            carbs = float(row[4]) if len(row) > 4 and row[4] is not None else 0.0
            fats = float(row[5]) if len(row) > 5 and row[5] is not None else 0.0
            self.tree.insert('', 0, text=row[1],
                             values=(f"{calories:.1f}", f"{proteins:.1f}", f"{carbs:.1f}", f"{fats:.1f}"))

    # Обновление списка продуктов в выпадающем меню
    def update_product_combo(self):
        query = 'SELECT name FROM products ORDER BY name ASC'
        products = self.run_query(query)
        product_list = [row[0] for row in products]
        self.product_combo['values'] = product_list
        if product_list:
            self.product_var.set(product_list[0])

    # Получение записей о приемах пищи из базы данных
    def get_meals(self):
        # Очистка таблицы
        records = self.meals_tree.get_children()
        for element in records:
            self.meals_tree.delete(element)

        # Получение данных из базы с явным указанием полей
        query = 'SELECT id, product_id, product_name, amount_g, calories, proteins, carbs, fats, meal_type, date FROM meal_records ORDER BY date DESC, id DESC'
        db_rows = self.run_query(query)

        # Заполнение таблицы
        for row in db_rows:
            try:
                # Структура строки: (id, product_id, product_name, amount_g, calories, proteins, carbs, fats, meal_type, date)
                if len(row) < 4:
                    continue

                # Безопасное преобразование числовых значений
                try:
                    amount_g = float(row[3])
                except (ValueError, TypeError):
                    amount_g = 0.0

                try:
                    calories = float(row[4])
                except (ValueError, TypeError):
                    calories = 0.0

                # БЖУ могут отсутствовать в старых записях
                if len(row) > 5 and row[5] is not None:
                    try:
                        proteins = float(row[5])
                    except (ValueError, TypeError):
                        proteins = 0.0
                else:
                    proteins = 0.0

                if len(row) > 6 and row[6] is not None:
                    try:
                        carbs = float(row[6])
                    except (ValueError, TypeError):
                        carbs = 0.0
                else:
                    carbs = 0.0

                if len(row) > 7 and row[7] is not None:
                    try:
                        fats = float(row[7])
                    except (ValueError, TypeError):
                        fats = 0.0
                else:
                    fats = 0.0

                # Строковые значения
                meal_type = str(row[8]) if len(row) > 8 and row[8] is not None else ''
                meal_date = str(row[9]) if len(row) > 9 and row[9] is not None else ''

                self.meals_tree.insert('', END, text=row[2], values=(
                    f"{amount_g:.1f}",
                    f"{calories:.1f}",
                    f"{proteins:.1f}",
                    f"{carbs:.1f}",
                    f"{fats:.1f}",
                    meal_type,
                    meal_date
                ))
            except (ValueError, IndexError, TypeError) as e:
                # Пропускаем некорректные записи
                print(f"Ошибка при обработке записи: {e}, строка: {row}")
                continue

        # Обновление итоговой статистики
        self.update_summary()

    # Обновление итоговой статистики за выбранную дату
    def update_summary(self):
        # Используем выбранную дату вместо сегодняшней
        selected_date = self.date_var.get().strip() if hasattr(self, 'date_var') and self.date_var.get() else date.today().strftime('%Y-%m-%d')

        # Получение сумм по приемам пищи
        query = '''
SELECT meal_type,
       SUM(calories) as total_calories,
       SUM(proteins) as total_proteins,
       SUM(carbs)    as total_carbs,
       SUM(fats)     as total_fats
FROM meal_records
WHERE date = ?
GROUP BY meal_type 
                '''
        results = self.run_query(query, (selected_date,))

        totals = {
            'Заутрок': {'calories': 0.0, 'proteins': 0.0, 'carbs': 0.0, 'fats': 0.0},
            'Обед': {'calories': 0.0, 'proteins': 0.0, 'carbs': 0.0, 'fats': 0.0},
            'Вечеря': {'calories': 0.0, 'proteins': 0.0, 'carbs': 0.0, 'fats': 0.0}
        }

        # Сопоставление старых значений (если в БД остались старые надписи) к новым ключам
        canonical_map = {
            'Завтрак': 'Заутрок',
            'Ужин': 'Вечеря'
        }

        # Заполнение словаря данными из базы (с учётом мэппинга)
        for row in results:
            meal_type_raw = str(row[0]) if row[0] is not None else ''
            meal_type = canonical_map.get(meal_type_raw, meal_type_raw)  # приводим к каноничным ключам
            if meal_type in totals:
                # Безопасное преобразование в float
                try:
                    totals[meal_type]['calories'] = float(row[1]) if row[1] is not None and isinstance(row[1], (int, float)) else 0.0
                except (ValueError, TypeError):
                    totals[meal_type]['calories'] = 0.0

                try:
                    totals[meal_type]["proteins"] = (
                        float(row[2]) if row[2] is not None and isinstance(row[2], (int, float)) else 0.0
                    )
                except (ValueError, TypeError):
                    totals[meal_type]["proteins"] = 0.0

                try:
                    totals[meal_type]['carbs'] = float(row[3]) if row[3] is not None and isinstance(row[3], (int,
                                                                                                             float)) else 0.0
                except (ValueError, TypeError):
                    totals[meal_type]['carbs'] = 0.0

                try:
                    totals[meal_type]['fats'] = float(row[4]) if row[4] is not None and isinstance(row[4], (int,
                                                                                                            float)) else 0.0
                except (ValueError, TypeError):
                    totals[meal_type]['fats'] = 0.0

        # Подсчет общих сумм (используем архаичные ключи)
        total_calories = totals['Заутрок']['calories'] + totals['Обед']['calories'] + totals['Вечеря']['calories']
        total_proteins = totals['Заутрок']['proteins'] + totals['Обед']['proteins'] + totals['Вечеря']['proteins']
        total_carbs = totals['Заутрок']['carbs'] + totals['Обед']['carbs'] + totals['Вечеря']['carbs']
        total_fats = totals['Заутрок']['fats'] + totals['Обед']['fats'] + totals['Вечеря']['fats']

        # Формирование текста для отображения
        summary_text = "Калории: "
        summary_text += f"Заутрок: {totals['Заутрок']['calories']:.1f} | "
        summary_text += f"Обед: {totals['Обед']['calories']:.1f} | "
        summary_text += f"Вечеря: {totals['Вечеря']['calories']:.1f} | "
        summary_text += f"ВСЕГО: {total_calories:.1f} ккал\n"
        summary_text += f"Бѣлки: {total_proteins:.1f} г | "
        summary_text += f"Углеводы: {total_carbs:.1f} г | "
        summary_text += f"Жиры: {total_fats:.1f} г"

        self.summary_label['text'] = summary_text

    # Проверка введенных данных для продукта
    def validation(self):
        # Проверка названия
        if len(self.name.get().strip()) == 0:
            return False

        # Проверка калорий
        try:
            calories_value = float(self.calories.get().strip())
            if calories_value < 0:
                return False
        except ValueError:
            return False

        # Проверка белков, углеводов и жиров (могут быть пустыми)
        try:
            if self.proteins.get().strip():
                if float(self.proteins.get().strip()) < 0:
                    return False
            if self.carbs.get().strip():
                if float(self.carbs.get().strip()) < 0:
                    return False
            if self.fats.get().strip():
                if float(self.fats.get().strip()) < 0:
                    return False
        except ValueError:
            return False

        return True

    # Проверка введенных данных для приема пищи
    def meal_validation(self):
        # Проверка выбора продукта
        if len(self.product_var.get().strip()) == 0:
            return False

        # Проверка количества
        try:
            amount_value = float(self.amount.get().strip())
            if amount_value <= 0:
                return False
        except ValueError:
            return False

        return True

    # Добавление нового продукта
    def add_product(self):
        if self.validation():
            # Получение значений из полей ввода
            name = self.name.get().strip()
            calories = float(self.calories.get().strip())
            proteins = float(self.proteins.get().strip() or 0)
            carbs = float(self.carbs.get().strip() or 0)
            fats = float(self.fats.get().strip() or 0)

            # Вставка в базу данных
            query = '''
                    INSERT INTO products (name, calories_per_100g, proteins_per_100g, carbs_per_100g, fats_per_100g)
                    VALUES (?, ?, ?, ?, ?)
                    '''
            parameters = (name, calories, proteins, carbs, fats)
            self.run_query(query, parameters)

            # Очистка полей и обновление таблицы
            self.message['text'] = f'Яство {name} вписано в Книгу Яствъ'
            self.name.delete(0, END)
            self.calories.delete(0, END)
            self.proteins.delete(0, END)
            self.carbs.delete(0, END)
            self.fats.delete(0, END)
            self.get_products()
            self.update_product_combo()
        else:
            self.message['text'] = 'Нужно имя яства и верныя числа (>= 0)'

    # Добавление продукта в рацион
    def add_meal(self):
        try:
            # Проверка введенных данных
            if not self.meal_validation():
                self.meal_message['text'] = 'Избери яство и укажи меру (граммы > 0)'
                return

            # Получение информации о продукте
            product_name = self.product_var.get().strip()
            query = 'SELECT id, calories_per_100g, proteins_per_100g, carbs_per_100g, fats_per_100g FROM products WHERE name = ?'
            result = self.run_query(query, (product_name,))

            if not result or len(result) == 0:
                self.meal_message['text'] = 'В Книге Яствъ нет сего имени'
                return

            # Извлечение данных о продукте
            product_id = result[0][0]
            calories_per_100g = result[0][1]
            proteins_per_100g = result[0][2] if result[0][2] is not None else 0
            carbs_per_100g = result[0][3] if result[0][3] is not None else 0
            fats_per_100g = result[0][4] if result[0][4] is not None else 0

            # Получение данных из полей ввода
            amount_g = float(self.amount.get().strip())
            meal_type = self.meal_type_var.get()
            meal_date = self.date_var.get().strip()

            # Расчет калорий и БЖУ для указанного количества
            total_calories = (calories_per_100g * amount_g) / 100.0
            total_proteins = (proteins_per_100g * amount_g) / 100.0
            total_carbs = (carbs_per_100g * amount_g) / 100.0
            total_fats = (fats_per_100g * amount_g) / 100.0

            # Вставка записи в базу данных
            query = '''
                    INSERT INTO meal_records (product_id, product_name, amount_g, calories, proteins, carbs, fats,
                                              meal_type, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
            parameters = (product_id, product_name, amount_g, total_calories, total_proteins, total_carbs, total_fats,
                          meal_type, meal_date)
            self.run_query(query, parameters)

            # Очистка поля и обновление таблицы
            self.meal_message['text'] = f'Вписано: {product_name} ({amount_g}г) = {total_calories:.1f} ккал'
            self.amount.delete(0, END)
            self.get_meals()
        except Exception as e:
            # Вывод ошибки для отладки
            error_msg = f'Погрѣшка при вписаніи: {str(e)}'
            self.meal_message['text'] = error_msg
            print(f"Погрѣшка в add_meal: {e}")
            import traceback
            traceback.print_exc()

    def clear_day(self):
        day = self.date_var.get()
        if not day:
            self.meal_message['text'] = "Выбери день для очистки"
            return

        query = 'DELETE FROM meal_records WHERE date = ?'
        self.run_query(query, (day,))
        self.get_meals()  # обновляем Treeview
        self.meal_message['text'] = f'Все записи за {day} удалены'

    # Удаление продукта
    def delete_product(self):
        try:
            # Получение выбранной записи
            name = self.tree.item(self.tree.selection())['text']
            # Удаление из базы данных
            query = 'DELETE FROM products WHERE name = ?'
            self.run_query(query, (name,))
            self.message['text'] = f'Запись {name} изъята'
            self.get_products()
            self.update_product_combo()
        except IndexError:
            self.message['text'] = 'Избери запись для изъя́тя'

    # Удаление записи о приеме пищи
    def delete_meal(self):
        try:
            # Получение выбранной записи
            selected_item = self.meals_tree.selection()[0]
            item_data = self.meals_tree.item(selected_item)
            product_name = item_data['text']
            values = item_data['values']

            # Извлечение данных для удаления
            amount = values[0]
            meal_type = values[5]
            meal_date = values[6]

            # Удаление из базы данных
            query = 'DELETE FROM meal_records WHERE product_name = ? AND amount_g = ? AND meal_type = ? AND date = ?'
            self.run_query(query, (product_name, float(amount), meal_type, meal_date))
            self.meal_message['text'] = f'Запись изъята: {product_name}'
            self.get_meals()
        except (IndexError, ValueError):
            self.meal_message['text'] = 'Избери запись для изъя́тя'

    # Обновление данных в таблице рациона
    def refresh_meals(self):
        self.get_meals()
        self.meal_message['text'] = 'Сводъ обновлёнъ'

    # Редактирование продукта
    def edit_product(self):
        try:
            # Получение данных выбранной записи
            name = self.tree.item(self.tree.selection())['text']
            old_calories = self.tree.item(self.tree.selection())['values'][0]
            old_proteins = self.tree.item(self.tree.selection())['values'][1] if len(
                self.tree.item(self.tree.selection())['values']) > 1 else '0'
            old_carbs = self.tree.item(self.tree.selection())['values'][2] if len(
                self.tree.item(self.tree.selection())['values']) > 2 else '0'
            old_fats = self.tree.item(self.tree.selection())['values'][3] if len(
                self.tree.item(self.tree.selection())['values']) > 3 else '0'

            # Создание окна редактирования
            self.edit_wind = Toplevel()
            self.edit_wind.title('Переписати яство')

            # Поля для редактирования
            Label(self.edit_wind, text='Имя нынѣ:').grid(row=0, column=0, padx=5, pady=5)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state='readonly', width=30).grid(
                row=0, column=1, padx=5, pady=5)

            Label(self.edit_wind, text='Нове имя:').grid(row=1, column=0, padx=5, pady=5)
            new_name = Entry(self.edit_wind, width=30)
            new_name.insert(0, name)
            new_name.grid(row=1, column=1, padx=5, pady=5)

            Label(self.edit_wind, text='Сила питательная нынѣ:').grid(row=2, column=0, padx=5, pady=5)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_calories), state='readonly',
                  width=30).grid(row=2, column=1, padx=5, pady=5)

            Label(self.edit_wind, text='Нове сила питательная:').grid(row=3, column=0, padx=5, pady=5)
            new_calories = Entry(self.edit_wind, width=30)
            new_calories.insert(0, old_calories)
            new_calories.grid(row=3, column=1, padx=5, pady=5)

            Label(self.edit_wind, text='Бѣлки нынѣ:').grid(row=4, column=0, padx=5, pady=5)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_proteins), state='readonly',
                  width=30).grid(row=4, column=1, padx=5, pady=5)

            Label(self.edit_wind, text='Нове бѣлки:').grid(row=5, column=0, padx=5, pady=5)
            new_proteins = Entry(self.edit_wind, width=30)
            new_proteins.insert(0, old_proteins)
            new_proteins.grid(row=5, column=1, padx=5, pady=5)

            Label(self.edit_wind, text='Углеводы нынѣ:').grid(row=6, column=0, padx=5, pady=5)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_carbs), state='readonly',
                  width=30).grid(row=6, column=1, padx=5, pady=5)

            Label(self.edit_wind, text='Нове углеводы:').grid(row=7, column=0, padx=5, pady=5)
            new_carbs = Entry(self.edit_wind, width=30)
            new_carbs.insert(0, old_carbs)
            new_carbs.grid(row=7, column=1, padx=5, pady=5)

            Label(self.edit_wind, text='Жиры нынѣ:').grid(row=8, column=0, padx=5, pady=5)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_fats), state='readonly',
                  width=30).grid(row=8, column=1, padx=5, pady=5)

            Label(self.edit_wind, text='Нове жиры:').grid(row=9, column=0, padx=5, pady=5)
            new_fats = Entry(self.edit_wind, width=30)
            new_fats.insert(0, old_fats)
            new_fats.grid(row=9, column=1, padx=5, pady=5)

            # Кнопка для сохранения изменений
            Button(self.edit_wind, text='ПЕРЕПИСАТИ', command=lambda: self.edit_records(
                new_name.get().strip(), name,
                new_calories.get().strip(), old_calories,
                new_proteins.get().strip(), old_proteins,
                new_carbs.get().strip(), old_carbs,
                new_fats.get().strip(), old_fats
            )).grid(row=10, column=1, sticky=W + E, padx=5, pady=10)
        except IndexError:
            self.message['text'] = 'Избери запись для переписи'

    # Сохранение изменений продукта
    def edit_records(self, new_name, old_name, new_calories, old_calories, new_proteins, old_proteins, new_carbs,
                     old_carbs, new_fats, old_fats):
        # Проверка данных
        if not new_name or not new_calories:
            self.message['text'] = 'Имя и сила питательная обязательны для вписанія'
            return

        # Преобразование в числа
        try:
            calories_value = float(new_calories)
            proteins_value = float(new_proteins or 0)
            carbs_value = float(new_carbs or 0)
            fats_value = float(new_fats or 0)

            if calories_value < 0 or proteins_value < 0 or carbs_value < 0 or fats_value < 0:
                self.message['text'] = 'Всѣ числа должни быть неотрицательны'
                return
        except ValueError:
            self.message['text'] = 'Всѣ даны повинны быть числы'
            return

        # Обновление в базе данных
        query = '''
                UPDATE products
                SET name              = ?,
                    calories_per_100g = ?,
                    proteins_per_100g = ?,
                    carbs_per_100g    = ?,
                    fats_per_100g     = ?
                WHERE name = ?
                  AND calories_per_100g = ?
                '''
        parameters = (new_name, calories_value, proteins_value, carbs_value, fats_value, old_name, float(old_calories))
        self.run_query(query, parameters)

        # Закрытие окна и обновление таблицы
        self.edit_wind.destroy()
        self.message['text'] = f'Вписаніе {old_name} Вписаніе'
        self.get_products()
        self.update_product_combo()


# Запуск программы
if __name__ == '__main__':
    try:
        # Создание главного окна
        window = Tk()
        # Создание приложения
        application = CalorieTracker(window)
        # Обновление окна для отображения всех элементов
        window.update()
        # Запуск главного цикла обработки событий
        window.mainloop()
    except Exception as e:
        # Вывод ошибки в консоль для отладки
        print(f"Ошибка при запуске программы: {e}")
        import traceback

        traceback.print_exc()
        input("Нажмите Enter для выхода...")
