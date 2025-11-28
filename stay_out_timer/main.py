import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
import json
import os
from tkinter import font

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
        self.start_time = 0  # Real time when timer started (in ms)
        self.is_running = False
        self.is_paused = False
        self.paused_time = 0  # Real time when paused (in ms)
        self.game_time_at_pause = 0  # Game time at pause (in ms)
        self.initial_game_time = 0  # Initial game time when timer starts (in ms)
        
        # Load saved game time if exists
        self.load_saved_game_time()
        
        # Create UI
        self.create_widgets()
        
        # Start timer update loop
        self.update_timer()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
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
        
        # Define custom styles for buttons
        self.start_button = tk.Button(button_frame, text="Старт", command=self.start_timer, 
                                      bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(button_frame, text="Пауза", command=self.pause_timer, 
                                      bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Стоп", command=self.stop_timer, 
                                     bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(button_frame, text="Сброс", command=self.reset_timer, 
                                      bg="#f44336", fg="white", font=("Arial", 10, "bold"))
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_time_button = tk.Button(button_frame, text="Изменить время", command=self.edit_time, 
                                          bg="#9C27B0", fg="white", font=("Arial", 10, "bold"))
        self.edit_time_button.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to start timer
        self.root.bind('<Return>', lambda event: self.start_timer())
        
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
    
    def load_saved_game_time(self):
        """Load saved game time from file"""
        try:
            if os.path.exists("game_time.json"):
                with open("game_time.json", "r") as f:
                    data = json.load(f)
                    self.initial_game_time = data.get("game_time", 0)
                    # Update the display with the loaded time
                    self.timer_label.config(text=f"Время игры: {self.format_time(self.initial_game_time)}")
        except Exception as e:
            print(f"Не удалось загрузить сохраненное игровое время: {str(e)}")
    
    def save_game_time_on_exit(self):
        """Save current game time to file when exiting"""
        try:
            # Calculate current game time to save
            current_game_time = self.initial_game_time
            if self.is_running and not self.is_paused:
                real_elapsed = (time.time() * 1000 - self.start_time)
                game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
                current_game_time = self.initial_game_time + game_time_ms
            
            with open("game_time.json", "w") as f:
                json.dump({"game_time": current_game_time}, f)
        except Exception as e:
            print(f"Не удалось сохранить игровое время: {str(e)}")
    
    def on_closing(self):
        """Handle window closing event"""
        # Save current game time
        self.save_game_time_on_exit()
        # Destroy the window
        self.root.destroy()
    
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
            
            # Total game time = initial game time + time elapsed since start + time accumulated while paused
            total_game_time = self.initial_game_time + game_time_ms
            
            self.timer_label.config(text=f"Время игры: {self.format_time(total_game_time)}")
        
        # Schedule next update
        self.root.after(1000, self.update_timer)  # Update every second
    
    def start_timer(self):
        if not self.is_running or self.is_paused:
            if self.is_paused:
                # Resume from pause: adjust start_time to account for pause duration
                pause_duration = time.time() * 1000 - self.paused_time
                self.start_time += pause_duration
                self.initial_game_time = self.game_time_at_pause
                self.is_paused = False
            else:
                # First start or after stop/reset
                self.start_time = time.time() * 1000
                # initial_game_time already contains the correct value
            
            self.is_running = True
            self.status_label.config(text="Состояние: Работает")
    
    def pause_timer(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.paused_time = time.time() * 1000
            
            # Calculate the elapsed game time at the moment of pause
            real_elapsed = (time.time() * 1000 - self.start_time)
            game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
            self.game_time_at_pause = self.initial_game_time + game_time_ms
            
            self.status_label.config(text="Состояние: На паузе")
    
    def stop_timer(self):
        if self.is_running:
            if not self.is_paused:
                # Calculate accumulated time before stopping
                real_elapsed = (time.time() * 1000 - self.start_time)
                game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
                self.initial_game_time += game_time_ms
            
            self.is_running = False
            self.is_paused = False
            self.status_label.config(text="Состояние: Остановлен")
    
    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.initial_game_time = 0
        self.start_time = time.time() * 1000
        self.timer_label.config(text="Время игры: 00:00:00")
        self.status_label.config(text="Состояние: Сброшен")
    
    def edit_time(self):
        # Create a custom dialog for time input
        time_window = tk.Toplevel(self.root)
        time_window.title("Установить игровое время")
        time_window.geometry("300x200")
        time_window.resizable(False, False)
        
        # Center the window
        time_window.transient(self.root)
        time_window.grab_set()
        
        # Create time input fields
        tk.Label(time_window, text="Часы (0-23):").pack(pady=5)
        hour_var = tk.StringVar(value="00")
        hour_entry = tk.Entry(time_window, textvariable=hour_var, width=10, justify='center')
        hour_entry.pack(pady=5)
        
        tk.Label(time_window, text="Минуты (0-59):").pack(pady=5)
        minute_var = tk.StringVar(value="00")
        minute_entry = tk.Entry(time_window, textvariable=minute_var, width=10, justify='center')
        minute_entry.pack(pady=5)
        
        tk.Label(time_window, text="Секунды (0-59):").pack(pady=5)
        second_var = tk.StringVar(value="00")
        second_entry = tk.Entry(time_window, textvariable=second_var, width=10, justify='center')
        second_entry.pack(pady=5)
        
        def set_time():
            try:
                hours = int(hour_var.get()) if hour_var.get().isdigit() else 0
                minutes = int(minute_var.get()) if minute_var.get().isdigit() else 0
                seconds = int(second_var.get()) if second_var.get().isdigit() else 0
                
                if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                    raise ValueError("Недопустимые значения")
                
                # Convert to total milliseconds
                total_ms = hours * 3600000 + minutes * 60000 + seconds * 1000
                
                # Set the timer to this time
                self.initial_game_time = total_ms
                self.start_time = time.time() * 1000
                
                # Update display
                self.timer_label.config(text=f"Время игры: {self.format_time(total_ms)}")
                
                time_window.destroy()
                
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректные значения времени. Используйте числа в допустимом диапазоне.")
        
        # Button frame
        button_frame = tk.Frame(time_window)
        button_frame.pack(pady=15)
        
        # Set button
        set_btn = tk.Button(button_frame, text="Установить", command=set_time, bg="#4CAF50", fg="white")
        set_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Отмена", command=time_window.destroy, bg="#f44336", fg="white")
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to set_time function
        time_window.bind('<Return>', lambda event: set_time())
        
        # Focus on hour entry
        hour_entry.focus()
        
        # Wait for window to be closed
        time_window.wait_window()

def main():
    root = tk.Tk()
    app = StayOutTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()