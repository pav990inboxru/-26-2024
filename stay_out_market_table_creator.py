import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
import json
import os
from PIL import Image, ImageTk
import webbrowser

class StayOutMarketTableCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Таблицы рынка Stay Out | Harper_IDS для IgromanDS")
        self.root.geometry("1000x700")
        
        # Устанавливаем стиль S.T.A.L.K.E.R.
        self.setup_stalker_style()
        
        # Инициализация данных
        self.categories = {}
        self.current_category = ""
        self.current_item = ""
        
        # Создаем вкладки
        self.create_tabs()
        
        # Загружаем сохраненные данные
        self.load_data()
        
        # Привязываем событие закрытия для автосохранения
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_stalker_style(self):
        """Настройка стиля в стиле S.T.A.L.K.E.R."""
        self.root.configure(bg="#2d2d2d")
        
        # Определяем цвета в стиле S.T.A.L.K.E.R.
        self.colors = {
            'bg': '#2d2d2d',
            'fg': '#dcdcdc',
            'accent': '#a0a000',
            'button_bg': '#4a4a4a',
            'button_fg': '#ffffff',
            'entry_bg': '#3a3a3a',
            'entry_fg': '#ffffff',
            'header_bg': '#5a5a5a'
        }
        
        # Настройка стиля ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Настройка цветов для различных элементов
        self.style.configure('TNotebook', background=self.colors['bg'])
        self.style.configure('TNotebook.Tab', background=self.colors['button_bg'], foreground=self.colors['fg'])
        self.style.map('TNotebook.Tab', background=[('selected', self.colors['accent'])])
        
        self.style.configure('TFrame', background=self.colors['bg'])
        self.style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        self.style.configure('TButton', background=self.colors['button_bg'], foreground=self.colors['button_fg'])
        self.style.map('TButton', background=[('active', self.colors['accent'])])

    def create_tabs(self):
        """Создание вкладок приложения"""
        # Основной ноутбук для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка создания таблиц
        self.create_main_tab()
        
        # Вкладка библиотеки
        self.create_library_tab()
        
        # Вкладка ссылок
        self.create_links_tab()

    def create_main_tab(self):
        """Создание основной вкладки для создания таблиц"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="Создание таблиц")
        
        # Заголовок
        title_label = tk.Label(main_frame, text="Создание таблиц для рынка Stay Out", 
                               font=("Arial", 16, "bold"), 
                               bg=self.colors['header_bg'], 
                               fg=self.colors['fg'], 
                               padx=10, pady=5)
        title_label.pack(fill=tk.X, pady=(0, 10))
        
        # Левая часть - управление категориями
        left_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Категории
        cat_label = tk.Label(left_frame, text="Категории товаров:", 
                             font=("Arial", 12), 
                             bg=self.colors['bg'], 
                             fg=self.colors['fg'])
        cat_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Список категорий
        self.cat_listbox = tk.Listbox(left_frame, 
                                      bg=self.colors['entry_bg'], 
                                      fg=self.colors['entry_fg'], 
                                      selectbackground=self.colors['accent'],
                                      height=10)
        self.cat_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.cat_listbox.bind('<<ListboxSelect>>', self.on_category_select)
        
        # Кнопки управления категориями
        cat_btn_frame = tk.Frame(left_frame, bg=self.colors['bg'])
        cat_btn_frame.pack(fill=tk.X)
        
        self.add_cat_btn = tk.Button(cat_btn_frame, 
                                     text="Добавить категорию", 
                                     command=self.add_category, 
                                     bg=self.colors['button_bg'], 
                                     fg=self.colors['button_fg'],
                                     relief=tk.FLAT)
        self.add_cat_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.del_cat_btn = tk.Button(cat_btn_frame, 
                                     text="Удалить", 
                                     command=self.delete_category, 
                                     bg=self.colors['button_bg'], 
                                     fg=self.colors['button_fg'],
                                     relief=tk.FLAT)
        self.del_cat_btn.pack(side=tk.LEFT)
        
        # Правая часть - детали товара
        right_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=10)
        
        # Форма для добавления товара
        item_frame = tk.LabelFrame(right_frame, 
                                   text="Детали товара", 
                                   bg=self.colors['bg'], 
                                   fg=self.colors['fg'],
                                   font=("Arial", 12))
        item_frame.pack(fill=tk.BOTH, expand=True)
        
        # Название товара
        name_frame = tk.Frame(item_frame, bg=self.colors['bg'])
        name_frame.pack(fill=tk.X, pady=5)
        tk.Label(name_frame, text="Название товара:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.item_name = tk.Entry(name_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        self.item_name.pack(fill=tk.X)
        
        # Цена покупки
        buy_price_frame = tk.Frame(item_frame, bg=self.colors['bg'])
        buy_price_frame.pack(fill=tk.X, pady=5)
        tk.Label(buy_price_frame, text="Цена покупки (мин. на доске):", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.buy_price = tk.Entry(buy_price_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        self.buy_price.pack(fill=tk.X)
        
        # Цена продажи
        sell_price_frame = tk.Frame(item_frame, bg=self.colors['bg'])
        sell_price_frame.pack(fill=tk.X, pady=5)
        tk.Label(sell_price_frame, text="Цена продажи (если сам продаю):", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.sell_price = tk.Entry(sell_price_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        self.sell_price.pack(fill=tk.X)
        
        # Где продавать
        location_frame = tk.Frame(item_frame, bg=self.colors['bg'])
        location_frame.pack(fill=tk.X, pady=5)
        tk.Label(location_frame, text="Где и у какого кладовщика продавать:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.location = tk.Entry(location_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        self.location.pack(fill=tk.X)
        
        # Ссылка на товар
        link_frame = tk.Frame(item_frame, bg=self.colors['bg'])
        link_frame.pack(fill=tk.X, pady=5)
        tk.Label(link_frame, text="Ссылка на товар:", bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.item_link = tk.Entry(link_frame, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'])
        self.item_link.pack(fill=tk.X)
        
        # Кнопка добавления товара
        self.add_item_btn = tk.Button(item_frame, 
                                      text="Добавить/Обновить товар", 
                                      command=self.add_item, 
                                      bg=self.colors['button_bg'], 
                                      fg=self.colors['button_fg'],
                                      relief=tk.FLAT)
        self.add_item_btn.pack(pady=10)
        
        # Кнопка вставки изображения
        self.image_btn = tk.Button(item_frame, 
                                   text="Вставить изображение/иконку", 
                                   command=self.insert_image, 
                                   bg=self.colors['button_bg'], 
                                   fg=self.colors['button_fg'],
                                   relief=tk.FLAT)
        self.image_btn.pack(pady=5)
        
        # Список товаров в выбранной категории
        items_frame = tk.LabelFrame(right_frame, 
                                    text="Товары в категории", 
                                    bg=self.colors['bg'], 
                                    fg=self.colors['fg'],
                                    font=("Arial", 12))
        items_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.items_listbox = tk.Listbox(items_frame, 
                                        bg=self.colors['entry_bg'], 
                                        fg=self.colors['entry_fg'], 
                                        selectbackground=self.colors['accent'])
        self.items_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.items_listbox.bind('<<ListboxSelect>>', self.on_item_select)
        
        # Кнопки управления товарами
        item_btn_frame = tk.Frame(items_frame, bg=self.colors['bg'])
        item_btn_frame.pack(fill=tk.X)
        
        self.del_item_btn = tk.Button(item_btn_frame, 
                                      text="Удалить товар", 
                                      command=self.delete_item, 
                                      bg=self.colors['button_bg'], 
                                      fg=self.colors['button_fg'],
                                      relief=tk.FLAT)
        self.del_item_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_form_btn = tk.Button(item_btn_frame, 
                                        text="Очистить форму", 
                                        command=self.clear_form, 
                                        bg=self.colors['button_bg'], 
                                        fg=self.colors['button_fg'],
                                        relief=tk.FLAT)
        self.clear_form_btn.pack(side=tk.LEFT)

    def create_library_tab(self):
        """Создание вкладки библиотеки"""
        library_frame = ttk.Frame(self.notebook)
        self.notebook.add(library_frame, text="Библиотека")
        
        title_label = tk.Label(library_frame, text="Библиотека созданных таблиц", 
                               font=("Arial", 16, "bold"), 
                               bg=self.colors['header_bg'], 
                               fg=self.colors['fg'], 
                               padx=10, pady=5)
        title_label.pack(fill=tk.X, pady=(0, 10))
        
        # Здесь будет список сохраненных таблиц
        self.library_listbox = tk.Listbox(library_frame, 
                                          bg=self.colors['entry_bg'], 
                                          fg=self.colors['entry_fg'], 
                                          selectbackground=self.colors['accent'])
        self.library_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Кнопки управления библиотекой
        btn_frame = tk.Frame(library_frame, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, 
                  text="Загрузить таблицу", 
                  command=self.load_table, 
                  bg=self.colors['button_bg'], 
                  fg=self.colors['button_fg'],
                  relief=tk.FLAT).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, 
                  text="Сохранить таблицу", 
                  command=self.save_table, 
                  bg=self.colors['button_bg'], 
                  fg=self.colors['button_fg'],
                  relief=tk.FLAT).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, 
                  text="Экспорт в CSV", 
                  command=self.export_csv, 
                  bg=self.colors['button_bg'], 
                  fg=self.colors['button_fg'],
                  relief=tk.FLAT).pack(side=tk.LEFT)

    def create_links_tab(self):
        """Создание вкладки ссылок"""
        links_frame = ttk.Frame(self.notebook)
        self.notebook.add(links_frame, text="Ссылки")
        
        title_label = tk.Label(links_frame, text="Полезные ссылки", 
                               font=("Arial", 16, "bold"), 
                               bg=self.colors['header_bg'], 
                               fg=self.colors['fg'], 
                               padx=10, pady=5)
        title_label.pack(fill=tk.X, pady=(0, 10))
        
        # Ссылка на вики
        wiki_frame = tk.Frame(links_frame, bg=self.colors['bg'])
        wiki_frame.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(wiki_frame, text="Википедия игры Stay Out:", 
                 font=("Arial", 12), 
                 bg=self.colors['bg'], 
                 fg=self.colors['fg']).pack(anchor=tk.W)
        wiki_link = tk.Label(wiki_frame, 
                             text="https://so-wiki.ru/", 
                             fg="blue", 
                             cursor="hand2", 
                             bg=self.colors['bg'])
        wiki_link.pack(anchor=tk.W, pady=5)
        wiki_link.bind("<Button-1>", lambda e: webbrowser.open("https://so-wiki.ru/"))
        
        # Ссылка на Steam
        steam_frame = tk.Frame(links_frame, bg=self.colors['bg'])
        steam_frame.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(steam_frame, text="Игра в Steam:", 
                 font=("Arial", 12), 
                 bg=self.colors['bg'], 
                 fg=self.colors['fg']).pack(anchor=tk.W)
        steam_link = tk.Label(steam_frame, 
                              text="https://store.steampowered.com/app/1180380/Stay_Out/", 
                              fg="blue", 
                              cursor="hand2", 
                              bg=self.colors['bg'])
        steam_link.pack(anchor=tk.W, pady=5)
        steam_link.bind("<Button-1>", lambda e: webbrowser.open("https://store.steampowered.com/app/1180380/Stay_Out/"))
        
        # Ссылка на профиль
        profile_frame = tk.Frame(links_frame, bg=self.colors['bg'])
        profile_frame.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(profile_frame, text="Профиль автора в Steam:", 
                 font=("Arial", 12), 
                 bg=self.colors['bg'], 
                 fg=self.colors['fg']).pack(anchor=tk.W)
        profile_link = tk.Label(profile_frame, 
                                text="https://steamcommunity.com/id/Harper_IDS/", 
                                fg="blue", 
                                cursor="hand2", 
                                bg=self.colors['bg'])
        profile_link.pack(anchor=tk.W, pady=5)
        profile_link.bind("<Button-1>", lambda e: webbrowser.open("https://steamcommunity.com/id/Harper_IDS/"))
        
        # Информация об авторстве
        author_frame = tk.Frame(links_frame, bg=self.colors['bg'])
        author_frame.pack(fill=tk.X, padx=20, pady=20)
        tk.Label(author_frame, 
                 text="Авторство: Harper_IDS", 
                 font=("Arial", 12, "bold"), 
                 bg=self.colors['bg'], 
                 fg=self.colors['fg']).pack(anchor=tk.W)
        tk.Label(author_frame, 
                 text="Создано для игрового сообщества IgromanDS", 
                 font=("Arial", 10), 
                 bg=self.colors['bg'], 
                 fg=self.colors['accent']).pack(anchor=tk.W, pady=5)

    def add_category(self):
        """Добавление новой категории"""
        category_name = tk.simpledialog.askstring("Новая категория", "Введите название категории:")
        if category_name and category_name.strip():
            if category_name not in self.categories:
                self.categories[category_name] = {}
                self.cat_listbox.insert(tk.END, category_name)
                messagebox.showinfo("Успех", f"Категория '{category_name}' добавлена!")
            else:
                messagebox.showwarning("Предупреждение", "Категория с таким именем уже существует!")

    def delete_category(self):
        """Удаление выбранной категории"""
        selection = self.cat_listbox.curselection()
        if selection:
            index = selection[0]
            category_name = self.cat_listbox.get(index)
            if messagebox.askyesno("Подтверждение", f"Удалить категорию '{category_name}' и все товары в ней?"):
                del self.categories[category_name]
                self.cat_listbox.delete(index)
                self.items_listbox.delete(0, tk.END)
                self.clear_form()

    def on_category_select(self, event):
        """Обработка выбора категории"""
        selection = self.cat_listbox.curselection()
        if selection:
            self.current_category = self.cat_listbox.get(selection[0])
            self.update_items_list()
        else:
            self.current_category = ""

    def update_items_list(self):
        """Обновление списка товаров в выбранной категории"""
        self.items_listbox.delete(0, tk.END)
        if self.current_category in self.categories:
            for item_name in self.categories[self.current_category]:
                self.items_listbox.insert(tk.END, item_name)

    def add_item(self):
        """Добавление или обновление товара"""
        if not self.current_category:
            messagebox.showwarning("Предупреждение", "Сначала выберите категорию!")
            return
        
        name = self.item_name.get().strip()
        buy_price = self.buy_price.get().strip()
        sell_price = self.sell_price.get().strip()
        location = self.location.get().strip()
        link = self.item_link.get().strip()
        
        if not name:
            messagebox.showwarning("Предупреждение", "Введите название товара!")
            return
        
        # Сохраняем товар
        item_data = {
            'buy_price': buy_price,
            'sell_price': sell_price,
            'location': location,
            'link': link
        }
        
        self.categories[self.current_category][name] = item_data
        
        # Обновляем список товаров
        self.update_items_list()
        
        # Выбираем добавленный/обновленный элемент
        items = list(self.categories[self.current_category].keys())
        index = items.index(name)
        self.items_listbox.selection_clear(0, tk.END)
        self.items_listbox.selection_set(index)
        
        messagebox.showinfo("Успех", f"Товар '{name}' добавлен/обновлен в категории '{self.current_category}'!")

    def delete_item(self):
        """Удаление выбранного товара"""
        if not self.current_category:
            messagebox.showwarning("Предупреждение", "Сначала выберите категорию!")
            return
        
        selection = self.items_listbox.curselection()
        if selection:
            index = selection[0]
            item_name = self.items_listbox.get(index)
            if messagebox.askyesno("Подтверждение", f"Удалить товар '{item_name}'?"):
                del self.categories[self.current_category][item_name]
                self.items_listbox.delete(index)
                self.clear_form()

    def on_item_select(self, event):
        """Обработка выбора товара"""
        selection = self.items_listbox.curselection()
        if selection and self.current_category:
            self.current_item = self.items_listbox.get(selection[0])
            item_data = self.categories[self.current_category][self.current_item]
            
            # Заполняем форму данными
            self.item_name.delete(0, tk.END)
            self.item_name.insert(0, self.current_item)
            
            self.buy_price.delete(0, tk.END)
            self.buy_price.insert(0, item_data.get('buy_price', ''))
            
            self.sell_price.delete(0, tk.END)
            self.sell_price.insert(0, item_data.get('sell_price', ''))
            
            self.location.delete(0, tk.END)
            self.location.insert(0, item_data.get('location', ''))
            
            self.item_link.delete(0, tk.END)
            self.item_link.insert(0, item_data.get('link', ''))

    def clear_form(self):
        """Очистка формы ввода"""
        self.item_name.delete(0, tk.END)
        self.buy_price.delete(0, tk.END)
        self.sell_price.delete(0, tk.END)
        self.location.delete(0, tk.END)
        self.item_link.delete(0, tk.END)
        self.current_item = ""

    def insert_image(self):
        """Вставка изображения/иконки"""
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            try:
                # Показываем сообщение о добавлении изображения
                messagebox.showinfo("Изображение", f"Изображение добавлено: {file_path}")
                # В реальной реализации здесь будет логика сохранения пути к изображению
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")

    def save_data(self):
        """Сохранение данных в файл"""
        try:
            with open('stay_out_market_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.categories, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def load_data(self):
        """Загрузка данных из файла"""
        try:
            if os.path.exists('stay_out_market_data.json'):
                with open('stay_out_market_data.json', 'r', encoding='utf-8') as f:
                    self.categories = json.load(f)
                
                # Обновляем список категорий
                for category in self.categories:
                    self.cat_listbox.insert(tk.END, category)
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")

    def on_closing(self):
        """Обработка закрытия приложения с автосохранением"""
        self.save_data()
        self.root.destroy()

    def save_table(self):
        """Сохранение таблицы в файл"""
        if not self.categories:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")],
            title="Сохранить таблицу как"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.categories, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Успех", "Таблица успешно сохранена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить таблицу: {str(e)}")

    def load_table(self):
        """Загрузка таблицы из файла"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")],
            title="Загрузить таблицу"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                # Обновляем текущие данные
                self.categories = loaded_data
                self.cat_listbox.delete(0, tk.END)
                
                # Обновляем список категорий
                for category in self.categories:
                    self.cat_listbox.insert(tk.END, category)
                
                messagebox.showinfo("Успех", "Таблица успешно загружена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить таблицу: {str(e)}")

    def export_csv(self):
        """Экспорт таблицы в CSV"""
        if not self.categories:
            messagebox.showwarning("Предупреждение", "Нет данных для экспорта!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")],
            title="Экспортировать таблицу как CSV"
        )
        if file_path:
            try:
                import csv
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Категория', 'Название товара', 'Цена покупки', 'Цена продажи', 'Место продажи', 'Ссылка'])
                    
                    for category, items in self.categories.items():
                        for item_name, item_data in items.items():
                            writer.writerow([
                                category,
                                item_name,
                                item_data.get('buy_price', ''),
                                item_data.get('sell_price', ''),
                                item_data.get('location', ''),
                                item_data.get('link', '')
                            ])
                
                messagebox.showinfo("Успех", "Таблица успешно экспортирована в CSV!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать таблицу: {str(e)}")


def main():
    root = tk.Tk()
    app = StayOutMarketTableCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()