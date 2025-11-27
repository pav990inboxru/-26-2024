import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

class StayOutTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер для Stay Out")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Загрузка настроек
        self.load_settings()

        # Переменные таймера
        self.start_time = 0
        self.timer_running = False
        self.game_time = 0  # В миллисекундах
        self.timer_interval = None
        self.real_time_tick = 1000  # 1 секунда реального времени
        self.game_tick_duration = self.settings.get('game_speed', 6870)  # Скорость игрового времени в мс

        # Создание интерфейса с вкладками
        self.create_widgets()

        # Загрузка последнего сохраненного времени (если есть)
        self.load_last_time()

    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            with open('timer_settings.json', 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                'game_speed': 6870,  # Стандартная скорость - 6870 мс
                'background_color': '#f0f0f0',
                'text_color': '#000000',
                'font_size': 12
            }
            self.save_settings()
    
    def save_settings(self):
        """Сохранение настроек в файл"""
        with open('timer_settings.json', 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)

    def load_last_time(self):
        """Загрузка последнего сохраненного времени"""
        try:
            with open('last_time.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.game_time = data.get('game_time', 0)
                self.update_display()
        except FileNotFoundError:
            pass

    def save_last_time(self):
        """Сохранение текущего времени"""
        with open('last_time.json', 'w', encoding='utf-8') as f:
            json.dump({'game_time': self.game_time}, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        """Создание элементов интерфейса с вкладками"""
        # Создаем ноутбук (табы)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка таймера
        self.timer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.timer_frame, text="⏱ Таймер")

        # Вкладка настроек
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚙ Настройки")

        # Вкладка помощи
        self.help_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.help_frame, text="❓ Помощь")

        # Создаем содержимое для каждой вкладки
        self.create_timer_tab()
        self.create_settings_tab()
        self.create_help_tab()

    def create_timer_tab(self):
        """Создание вкладки таймера"""
        # Стили
        style = ttk.Style()
        style.theme_use('clam')

        # Основной контейнер
        main_frame = ttk.Frame(self.timer_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(main_frame, text="⏱ Таймер для Stay Out", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # Отображение времени
        self.time_label = ttk.Label(main_frame, text="00:00:00", font=('Arial', 32, 'bold'), foreground='blue')
        self.time_label.pack(pady=(0, 20))

        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="▶ Старт", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(button_frame, text="⏸ Пауза", command=self.pause_timer, state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="⏹ Стоп", command=self.stop_timer, state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(button_frame, text="↺ Сброс", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Кнопка редактирования времени
        self.edit_button = ttk.Button(main_frame, text="✏ Редактировать время", command=self.edit_time)
        self.edit_button.pack(pady=10)

        # Информация о программе
        info_label = ttk.Label(main_frame, text="Программа создана разработчиком Harper_IDS для сообщества IgromanDS", 
                              font=('Arial', 9), foreground='gray')
        info_label.pack(pady=(20, 0))

    def create_settings_tab(self):
        """Создание вкладки настроек"""
        settings_main = ttk.Frame(self.settings_frame, padding="10")
        settings_main.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        settings_title = ttk.Label(settings_main, text="⚙ Настройки", font=('Arial', 16, 'bold'))
        settings_title.pack(pady=(0, 20))

        # Настройка скорости игрового времени
        speed_frame = ttk.LabelFrame(settings_main, text="Скорость игрового времени", padding="10")
        speed_frame.pack(fill=tk.X, pady=5)

        ttk.Label(speed_frame, text="Скорость игрового времени (мс):").pack(anchor=tk.W)
        
        # Поле для ввода скорости
        speed_input_frame = ttk.Frame(speed_frame)
        speed_input_frame.pack(fill=tk.X, pady=5)
        
        self.speed_var = tk.IntVar(value=self.settings.get('game_speed', 6870))
        self.speed_entry = ttk.Entry(speed_input_frame, textvariable=self.speed_var)
        self.speed_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(speed_input_frame, text="✓ Применить", command=self.apply_speed_settings).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Подсказка
        ttk.Label(speed_frame, text="Стандартное значение: 6870 мс (1 реальная секунда = ~6.87 игровых секунд)", 
                 font=('Arial', 9), foreground='gray').pack(anchor=tk.W, pady=(5, 0))

    def apply_speed_settings(self):
        """Применение настроек скорости"""
        try:
            new_speed = int(self.speed_var.get())
            if 100 <= new_speed <= 10000:  # Разумные пределы
                self.settings['game_speed'] = new_speed
                self.game_tick_duration = new_speed
                self.save_settings()
                messagebox.showinfo("Настройки", "Настройки скорости применены успешно!")
            else:
                messagebox.showerror("Ошибка", "Значение должно быть от 100 до 10000 мс")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное числовое значение")

    def create_help_tab(self):
        """Создание вкладки помощи"""
        help_main = ttk.Frame(self.help_frame, padding="10")
        help_main.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        help_title = ttk.Label(help_main, text="❓ Помощь", font=('Arial', 16, 'bold'))
        help_title.pack(pady=(0, 20))

        # Текст помощи
        help_text = """
Добро пожаловать в Таймер для Stay Out!

📋 Основные функции:
• Старт - запускает отсчет игрового времени
• Пауза - временно останавливает таймер
• Стоп - останавливает таймер и сохраняет текущее время
• Сброс - обнуляет таймер
• Редактировать время - позволяет установить произвольное время

⚙ Настройки:
• На вкладке 'Настройки' можно изменить скорость игрового времени
• Стандартное значение 6870 мс означает, что 1 реальная секунда равна ~6.87 игровых секунд

💾 Сохранение:
• Программа автоматически сохраняет последнее время при остановке
• При следующем запуске восстанавливает предыдущее состояние

❓ Как пользоваться:
1. Нажмите 'Старт' для начала отсчета
2. Используйте 'Пауза' для временной остановки
3. 'Стоп' сохраняет текущее время
4. 'Сброс' обнуляет таймер
5. 'Редактировать время' позволяет установить произвольное значение

Программа создана разработчиком Harper_IDS для сообщества IgromanDS
        """

        # Текстовое поле с информацией
        text_widget = tk.Text(help_main, wrap=tk.WORD, font=('Arial', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Добавляем текст
        text_widget.insert(tk.END, help_text.strip())
        text_widget.config(state=tk.DISABLED)  # Только для чтения

    def format_time(self, milliseconds):
        """Форматирование времени в ЧЧ:ММ:СС"""
        total_seconds = milliseconds // 1000
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_display(self):
        """Обновление отображения времени"""
        self.time_label.config(text=self.format_time(self.game_time))

    def update_timer(self):
        """Обновление таймера"""
        if self.timer_running:
            current_time = datetime.now().timestamp() * 1000  # Текущее время в мс
            elapsed_real_time = current_time - self.start_time
            # Вычисляем игровое время: прошедшее реальное время * соотношение игрового времени
            self.game_time = int(elapsed_real_time * self.game_tick_duration / self.real_time_tick)
            self.update_display()
            self.timer_interval = self.root.after(1000, self.update_timer)  # Обновляем каждую секунду

    def start_timer(self):
        """Запуск таймера"""
        if not self.timer_running:
            self.start_time = datetime.now().timestamp() * 1000 - (self.game_time * self.real_time_tick / self.game_tick_duration)
            self.timer_running = True
            self.update_timer()
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.stop_button.config(state='normal')

    def pause_timer(self):
        """Пауза таймера"""
        if self.timer_running:
            self.timer_running = False
            if self.timer_interval:
                self.root.after_cancel(self.timer_interval)
            self.start_button.config(state='normal')
            self.pause_button.config(state='disabled')

    def stop_timer(self):
        """Остановка таймера"""
        self.timer_running = False
        if self.timer_interval:
            self.root.after_cancel(self.timer_interval)
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')
        self.stop_button.config(state='disabled')
        self.save_last_time()

    def reset_timer(self):
        """Сброс таймера"""
        self.timer_running = False
        if self.timer_interval:
            self.root.after_cancel(self.timer_interval)
        self.game_time = 0
        self.update_display()
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')
        self.stop_button.config(state='disabled')
        # Удаляем сохраненное время при сбросе
        if os.path.exists('last_time.json'):
            os.remove('last_time.json')

    def edit_time(self):
        """Редактирование времени"""
        current_time_str = self.format_time(self.game_time)
        new_time_str = simpledialog.askstring(
            "Редактировать время",
            f"Введите новое время в формате ЧЧ:ММ:СС\n(текущее: {current_time_str}):"
        )
        
        if new_time_str:
            try:
                time_parts = new_time_str.split(':')
                if len(time_parts) != 3:
                    raise ValueError("Неверный формат")
                
                hours, minutes, seconds = map(int, time_parts)
                
                if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
                    raise ValueError("Неверные значения времени")
                
                self.game_time = hours * 3600000 + minutes * 60000 + seconds * 1000
                self.update_display()
                
                # Если таймер запущен, пересчитываем start_time
                if self.timer_running:
                    current_time = datetime.now().timestamp() * 1000
                    self.start_time = current_time - (self.game_time * self.real_time_tick / self.game_tick_duration)
                
                self.save_last_time()
                
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат времени. Используйте ЧЧ:ММ:СС (например, 12:30:45)")

def main():
    root = tk.Tk()
    app = StayOutTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()