import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
import json
import os

class StayOutTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер Stay Out - Harper_IDS")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Default settings
        self.settings = {
            "game_tick_duration": 6870,  # Default speed from original code
            "real_time_tick": 1000,
            "background_color": "#f0f0f0",
            "text_color": "#000000"
        }
        self.load_settings()
        
        # Timer variables
        self.start_time = 0
        self.is_running = False
        self.is_paused = False
        self.paused_time = 0
        self.elapsed_at_pause = 0
        
        # Create UI
        self.create_widgets()
        
        # Start timer update loop
        self.update_timer()
    
    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main timer tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Таймер")
        
        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Настройки")
        
        # Help tab
        self.help_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.help_frame, text="Помощь")
        
        # Main timer widgets
        self.setup_main_tab()
        
        # Settings widgets
        self.setup_settings_tab()
        
        # Help widgets
        self.setup_help_tab()
    
    def setup_main_tab(self):
        # Timer display
        self.timer_label = ttk.Label(self.main_frame, text="Время игры: 00:00:00", 
                                     font=("Arial", 24), foreground="#333")
        self.timer_label.pack(pady=20)
        
        # Control buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Старт", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="Пауза", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Стоп", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(button_frame, text="Сброс", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_time_button = ttk.Button(button_frame, text="Изменить время", command=self.edit_time)
        self.edit_time_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="Состояние: Остановлен", 
                                      font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Info label
        self.info_label = ttk.Label(self.main_frame, 
                                   text="Программа создана разработчиком Harper_IDS для сообщества IgromanDS", 
                                   font=("Arial", 10), foreground="#555")
        self.info_label.pack(pady=10)
    
    def setup_settings_tab(self):
        # Settings frame
        settings_container = ttk.Frame(self.settings_frame)
        settings_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Game time speed
        speed_frame = ttk.LabelFrame(settings_container, text="Скорость игрового времени")
        speed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(speed_frame, text="Продолжительность игровой секунды (мс):").pack(anchor=tk.W, padx=10, pady=5)
        
        self.speed_var = tk.IntVar(value=self.settings["game_tick_duration"])
        speed_scale = ttk.Scale(speed_frame, from_=100, to=10000, variable=self.speed_var, 
                                orient=tk.HORIZONTAL, command=self.update_speed)
        speed_scale.pack(fill=tk.X, padx=10, pady=5)
        
        self.speed_label = ttk.Label(speed_frame, text=f"{self.settings['game_tick_duration']} мс")
        self.speed_label.pack(pady=5)
        
        # Default speed button
        ttk.Button(speed_frame, text="Сбросить к стандарту (6870 мс)", 
                   command=self.reset_speed_to_default).pack(pady=5)
        
        # Appearance settings
        appearance_frame = ttk.LabelFrame(settings_container, text="Настройки внешнего вида")
        appearance_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(appearance_frame, text="Цвет фона:").pack(anchor=tk.W, padx=10, pady=5)
        self.bg_color_var = tk.StringVar(value=self.settings["background_color"])
        bg_color_entry = ttk.Entry(appearance_frame, textvariable=self.bg_color_var)
        bg_color_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(appearance_frame, text="Цвет текста:").pack(anchor=tk.W, padx=10, pady=5)
        self.text_color_var = tk.StringVar(value=self.settings["text_color"])
        text_color_entry = ttk.Entry(appearance_frame, textvariable=self.text_color_var)
        text_color_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Save settings button
        ttk.Button(settings_container, text="Сохранить настройки", 
                   command=self.save_settings).pack(pady=20)
    
    def setup_help_tab(self):
        help_text = """
        Добро пожаловать в таймер для игры Stay Out!
        
        ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:
        
        1. ВКЛАДКА "ТАЙМЕР":
           - Старт: Начать отсчет игрового времени
           - Пауза: Приостановить таймер (время сохраняется)
           - Стоп: Остановить таймер (время не сбрасывается)
           - Сброс: Сбросить таймер до 00:00:00
           - Изменить время: Установить произвольное время в формате ЧЧ:ММ:СС
        
        2. ВКЛАДКА "НАСТРОЙКИ":
           - Регулируйте скорость игрового времени с помощью ползунка
           - Изменяйте цвета интерфейса
           - Сохраняйте настройки для постоянного использования
        
        3. ВКЛАДКА "ПОМОЩЬ":
           - Здесь вы находитесь сейчас
           - Информация о программе и инструкции
        
        ВАЖНО:
        - Стандартная скорость игрового времени: 6870 мс
        - Это означает, что 1 реальная секунда = примерно 6.87 игровых секунд
        - Программа создана разработчиком Harper_IDS для сообщества IgromanDS
        
        Для получения дополнительной помощи:
        - Обратитесь к сообществу IgromanDS
        - Используйте стандартные настройки, если не уверены
        
        Приятной игры в Stay Out!
        """
        
        help_text_widget = tk.Text(self.help_frame, wrap=tk.WORD, padx=20, pady=20)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
        help_text_widget.pack(fill=tk.BOTH, expand=True)
    
    def update_speed(self, value):
        self.settings["game_tick_duration"] = int(float(value))
        self.speed_label.config(text=f"{int(float(value))} мс")
    
    def reset_speed_to_default(self):
        self.speed_var.set(6870)
        self.settings["game_tick_duration"] = 6870
        self.speed_label.config(text="6870 мс")
    
    def save_settings(self):
        self.settings["game_tick_duration"] = self.speed_var.get()
        self.settings["background_color"] = self.bg_color_var.get()
        self.settings["text_color"] = self.text_color_var.get()
        
        try:
            with open("settings.json", "w") as f:
                json.dump(self.settings, f)
            messagebox.showinfo("Настройки", "Настройки успешно сохранены!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {str(e)}")
    
    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except Exception as e:
            print(f"Не удалось загрузить настройки: {str(e)}")
    
    def format_time(self, elapsed_time_ms):
        """Format time in milliseconds to HH:MM:SS format"""
        total_seconds = int(elapsed_time_ms // 1000)
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def update_timer(self):
        if self.is_running and not self.is_paused:
            # Calculate current game time
            real_elapsed = (time.time() * 1000 - self.start_time)  # in ms
            game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
            
            # Add any time that was accumulated while paused
            total_game_time = game_time_ms + self.elapsed_at_pause
            
            self.timer_label.config(text=f"Время игры: {self.format_time(total_game_time)}")
        
        # Schedule next update
        self.root.after(1000, self.update_timer)  # Update every second
    
    def start_timer(self):
        if not self.is_running or self.is_paused:
            if self.is_paused:
                # Resume from pause: adjust start_time to account for pause duration
                pause_duration = time.time() * 1000 - self.paused_time
                self.start_time += pause_duration * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
                self.is_paused = False
            else:
                # First start or after stop/reset
                self.start_time = time.time() * 1000 - self.elapsed_at_pause * self.settings["real_time_tick"] / self.settings["game_tick_duration"]
            
            self.is_running = True
            self.status_label.config(text="Состояние: Работает")
    
    def pause_timer(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.paused_time = time.time() * 1000
            
            # Calculate the elapsed game time at the moment of pause
            real_elapsed = (time.time() * 1000 - self.start_time)
            game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
            self.elapsed_at_pause += game_time_ms
            
            self.status_label.config(text="Состояние: На паузе")
    
    def stop_timer(self):
        if self.is_running:
            if not self.is_paused:
                # Calculate accumulated time before stopping
                real_elapsed = (time.time() * 1000 - self.start_time)
                game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
                self.elapsed_at_pause += game_time_ms
            
            self.is_running = False
            self.is_paused = False
            self.status_label.config(text="Состояние: Остановлен")
    
    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.elapsed_at_pause = 0
        self.start_time = time.time() * 1000
        self.timer_label.config(text="Время игры: 00:00:00")
        self.status_label.config(text="Состояние: Сброшен")
    
    def edit_time(self):
        time_str = simpledialog.askstring("Изменить время", 
                                         "Введите время в формате ЧЧ:ММ:СС (например, 12:30:45):")
        
        if time_str:
            try:
                # Parse the input time
                parts = time_str.split(':')
                if len(parts) != 3:
                    raise ValueError("Неверный формат")
                
                hours, minutes, seconds = map(int, parts)
                
                if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                    raise ValueError("Недопустимые значения")
                
                # Convert to total milliseconds
                total_ms = hours * 3600000 + minutes * 60000 + seconds * 1000
                
                # Set the timer to this time
                self.elapsed_at_pause = total_ms
                self.start_time = time.time() * 1000
                
                # Update display
                self.timer_label.config(text=f"Время игры: {self.format_time(total_ms)}")
                
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат времени. Используйте ЧЧ:ММ:СС в 24-часовом формате.")

def main():
    root = tk.Tk()
    app = StayOutTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()