import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

class StayOutTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер для Stay Out")
        self.root.geometry("500x400")
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

        # Создание интерфейса
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
        """Создание элементов интерфейса"""
        # Стили
        style = ttk.Style()
        style.theme_use('clam')

        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Заголовок
        title_label = ttk.Label(main_frame, text="⏱ Таймер для Stay Out", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Отображение времени
        self.time_label = ttk.Label(main_frame, text="00:00:00", font=('Arial', 24, 'bold'), foreground='blue')
        self.time_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(button_frame, text="▶ Старт", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(button_frame, text="⏸ Пауза", command=self.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = ttk.Button(button_frame, text="⏹ Стоп", command=self.stop_timer)
        self.stop_button.grid(row=0, column=2, padx=5)

        self.reset_button = ttk.Button(button_frame, text="↺ Сброс", command=self.reset_timer)
        self.reset_button.grid(row=0, column=3, padx=5)

        # Кнопка редактирования времени
        self.edit_button = ttk.Button(main_frame, text="✏ Редактировать время", command=self.edit_time)
        self.edit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Информация о программе
        info_label = ttk.Label(main_frame, text="Программа создана разработчиком Harper_IDS для сообщества IgromanDS", 
                              font=('Arial', 9), foreground='gray')
        info_label.grid(row=4, column=0, columnspan=2, pady=(20, 0))

        # Настройка весов для адаптивности
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

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