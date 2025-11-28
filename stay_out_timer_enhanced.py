import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import time
import threading
import json
import os
import winsound  # For sound alerts on Windows
from datetime import datetime
import webbrowser

class StayOutTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер Stay Out v1.0.0 - Harper_IDS")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Default settings
        self.settings = {
            "game_tick_duration": 6870,  # Default speed from original code
            "real_time_tick": 1000,
            "background_color": "#2c2c2c",
            "text_color": "#ffffff",
            "accent_color": "#ff6b35",
            "alarm_sound_enabled": True,
            "volume_level": 100,
            "theme": "stalker",
            "auto_save_on_exit": True,
            "show_real_time": True
        }
        self.load_settings()
        
        # Timer variables
        self.start_time = 0
        self.is_running = False
        self.is_paused = False
        self.paused_time = 0
        self.elapsed_at_pause = 0
        
        # Alarms and timers
        self.alarms = []
        self.timers = []
        
        # Create UI
        self.create_widgets()
        
        # Start timer update loop
        self.update_timer()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        # Configure root window for STALKER theme
        self.root.configure(bg=self.settings["background_color"])
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main timer tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Таймер")
        
        # Alarms tab
        self.alarms_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alarms_frame, text="Будильники")
        
        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Настройки")
        
        # Help tab
        self.help_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.help_frame, text="Помощь")
        
        # Main timer widgets
        self.setup_main_tab()
        
        # Alarms widgets
        self.setup_alarms_tab()
        
        # Settings widgets
        self.setup_settings_tab()
        
        # Help widgets
        self.setup_help_tab()
    
    def setup_main_tab(self):
        # Configure frame for STALKER theme
        self.main_frame.configure(style="STALKER.TFrame")
        
        # Timer display
        timer_frame = ttk.Frame(self.main_frame)
        timer_frame.pack(pady=20)
        
        # Game time display
        self.game_timer_label = ttk.Label(timer_frame, text="Время игры: 00:00:00", 
                                     font=("Arial", 24), foreground=self.settings["text_color"])
        self.game_timer_label.pack(pady=5)
        
        # Real time display (if enabled)
        if self.settings["show_real_time"]:
            self.real_time_label = ttk.Label(timer_frame, text="Реальное время: --:--:--", 
                                       font=("Arial", 16), foreground=self.settings["text_color"])
            self.real_time_label.pack(pady=5)
        
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
                                      font=("Arial", 12), foreground=self.settings["text_color"])
        self.status_label.pack(pady=10)
        
        # Info label
        self.info_label = ttk.Label(self.main_frame, 
                                   text="Программа создана разработчиком Harper_IDS для сообщества IgromanDS", 
                                   font=("Arial", 10), foreground="#cccccc")
        self.info_label.pack(pady=10)
    
    def setup_alarms_tab(self):
        # Configure frame for STALKER theme
        self.alarms_frame.configure(style="STALKER.TFrame")
        
        # Title
        title_label = ttk.Label(self.alarms_frame, text="Управление будильниками и таймерами", 
                               font=("Arial", 16, "bold"), foreground=self.settings["text_color"])
        title_label.pack(pady=10)
        
        # Add alarm frame
        add_alarm_frame = ttk.LabelFrame(self.alarms_frame, text="Добавить будильник")
        add_alarm_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Alarm time input
        ttk.Label(add_alarm_frame, text="Время будильника (ЧЧ:ММ:СС):").pack(anchor=tk.W, padx=10, pady=5)
        self.alarm_time_entry = ttk.Entry(add_alarm_frame)
        self.alarm_time_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Alarm description
        ttk.Label(add_alarm_frame, text="Описание:").pack(anchor=tk.W, padx=10, pady=5)
        self.alarm_desc_entry = ttk.Entry(add_alarm_frame)
        self.alarm_desc_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Add alarm button
        ttk.Button(add_alarm_frame, text="Добавить будильник", command=self.add_alarm).pack(pady=10)
        
        # Alarms list
        alarms_list_frame = ttk.LabelFrame(self.alarms_frame, text="Список будильников")
        alarms_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create treeview for alarms
        self.alarms_tree = ttk.Treeview(alarms_list_frame, columns=("time", "desc", "status"), show="headings")
        self.alarms_tree.heading("time", text="Время")
        self.alarms_tree.heading("desc", text="Описание")
        self.alarms_tree.heading("status", text="Статус")
        self.alarms_tree.column("time", width=100)
        self.alarms_tree.column("desc", width=200)
        self.alarms_tree.column("status", width=100)
        
        # Scrollbar for alarms list
        scrollbar = ttk.Scrollbar(alarms_list_frame, orient=tk.VERTICAL, command=self.alarms_tree.yview)
        self.alarms_tree.configure(yscrollcommand=scrollbar.set)
        
        self.alarms_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons for alarms
        alarm_buttons_frame = ttk.Frame(alarms_list_frame)
        alarm_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(alarm_buttons_frame, text="Удалить", command=self.delete_alarm).pack(side=tk.LEFT, padx=5)
        ttk.Button(alarm_buttons_frame, text="Сбросить все", command=self.clear_alarms).pack(side=tk.LEFT, padx=5)
    
    def setup_settings_tab(self):
        # Configure frame for STALKER theme
        self.settings_frame.configure(style="STALKER.TFrame")
        
        # Settings notebook for organization
        settings_notebook = ttk.Notebook(self.settings_frame)
        settings_notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # General settings tab
        general_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(general_frame, text="Общие")
        
        # Appearance settings tab
        appearance_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(appearance_frame, text="Внешний вид")
        
        # Audio settings tab
        audio_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(audio_frame, text="Звук")
        
        # Advanced settings tab
        advanced_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(advanced_frame, text="Дополнительно")
        
        # General settings
        self.setup_general_settings(general_frame)
        
        # Appearance settings
        self.setup_appearance_settings(appearance_frame)
        
        # Audio settings
        self.setup_audio_settings(audio_frame)
        
        # Advanced settings
        self.setup_advanced_settings(advanced_frame)
    
    def setup_general_settings(self, parent):
        # Game time speed
        speed_frame = ttk.LabelFrame(parent, text="Скорость игрового времени")
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
        
        # Save settings button
        ttk.Button(parent, text="Сохранить настройки", 
                   command=self.save_settings).pack(pady=20)
        
        # Reset settings button
        ttk.Button(parent, text="Сбросить все настройки", 
                   command=self.reset_settings).pack(pady=5)
    
    def setup_appearance_settings(self, parent):
        # Appearance settings
        appearance_frame = ttk.LabelFrame(parent, text="Настройки внешнего вида")
        appearance_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(appearance_frame, text="Цвет фона:").pack(anchor=tk.W, padx=10, pady=5)
        self.bg_color_var = tk.StringVar(value=self.settings["background_color"])
        bg_color_entry = ttk.Entry(appearance_frame, textvariable=self.bg_color_var)
        bg_color_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(appearance_frame, text="Цвет текста:").pack(anchor=tk.W, padx=10, pady=5)
        self.text_color_var = tk.StringVar(value=self.settings["text_color"])
        text_color_entry = ttk.Entry(appearance_frame, textvariable=self.text_color_var)
        text_color_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(appearance_frame, text="Цвет акцента:").pack(anchor=tk.W, padx=10, pady=5)
        self.accent_color_var = tk.StringVar(value=self.settings["accent_color"])
        accent_color_entry = ttk.Entry(appearance_frame, textvariable=self.accent_color_var)
        accent_color_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Theme selection
        theme_frame = ttk.LabelFrame(parent, text="Тема оформления")
        theme_frame.pack(fill=tk.X, pady=5)
        
        self.theme_var = tk.StringVar(value=self.settings["theme"])
        themes = [("STALKER", "stalker"), ("Темная", "dark"), ("Светлая", "light")]
        for text, value in themes:
            ttk.Radiobutton(theme_frame, text=text, variable=self.theme_var, value=value).pack(anchor=tk.W, padx=10, pady=2)
        
        # Save settings button
        ttk.Button(parent, text="Сохранить настройки", 
                   command=self.save_settings).pack(pady=20)
    
    def setup_audio_settings(self, parent):
        # Audio settings
        audio_frame = ttk.LabelFrame(parent, text="Настройки звука")
        audio_frame.pack(fill=tk.X, pady=5)
        
        # Sound toggle
        self.sound_var = tk.BooleanVar(value=self.settings["alarm_sound_enabled"])
        sound_check = ttk.Checkbutton(audio_frame, text="Включить звуковые уведомления", 
                                      variable=self.sound_var, command=self.toggle_sound)
        sound_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Volume control
        ttk.Label(audio_frame, text="Громкость будильника:").pack(anchor=tk.W, padx=10, pady=5)
        self.volume_var = tk.IntVar(value=self.settings["volume_level"])
        volume_scale = ttk.Scale(audio_frame, from_=0, to=100, variable=self.volume_var, 
                                orient=tk.HORIZONTAL, command=self.update_volume)
        volume_scale.pack(fill=tk.X, padx=10, pady=5)
        
        self.volume_label = ttk.Label(audio_frame, text=f"Уровень: {self.settings['volume_level']}%")
        self.volume_label.pack(pady=5)
        
        # Test sound button
        ttk.Button(audio_frame, text="Тест звука", command=self.test_sound).pack(pady=10)
        
        # Save settings button
        ttk.Button(parent, text="Сохранить настройки", 
                   command=self.save_settings).pack(pady=20)
    
    def setup_advanced_settings(self, parent):
        # Advanced settings
        advanced_frame = ttk.LabelFrame(parent, text="Дополнительные настройки")
        advanced_frame.pack(fill=tk.X, pady=5)
        
        # Show real time toggle
        self.show_real_time_var = tk.BooleanVar(value=self.settings["show_real_time"])
        real_time_check = ttk.Checkbutton(advanced_frame, text="Показывать реальное время", 
                                          variable=self.show_real_time_var, command=self.toggle_real_time)
        real_time_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Auto-save toggle
        self.auto_save_var = tk.BooleanVar(value=self.settings["auto_save_on_exit"])
        auto_save_check = ttk.Checkbutton(advanced_frame, text="Автосохранение настроек при выходе", 
                                          variable=self.auto_save_var, command=self.toggle_auto_save)
        auto_save_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Reset all settings button
        ttk.Button(parent, text="Сбросить все настройки до стандартных", 
                   command=self.reset_settings).pack(pady=10)
        
        # Save settings button
        ttk.Button(parent, text="Сохранить настройки", 
                   command=self.save_settings).pack(pady=20)
    
    def setup_help_tab(self):
        # Configure frame for STALKER theme
        self.help_frame.configure(style="STALKER.TFrame")
        
        # Title
        title_label = ttk.Label(self.help_frame, text="Руководство для новичков", 
                               font=("Arial", 16, "bold"), foreground=self.settings["text_color"])
        title_label.pack(pady=10)
        
        # Help text
        help_text = """
        Добро пожаловать в таймер для игры Stay Out!
        
        ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:
        
        1. ВКЛАДКА "ТАЙМЕР":
           - Старт: Начать отсчет игрового времени
           - Пауза: Приостановить таймер (время сохраняется)
           - Стоп: Остановить таймер (время не сбрасывается)
           - Сброс: Сбросить таймер до 00:00:00
           - Изменить время: Установить произвольное время в формате ЧЧ:ММ:СС
        
        2. ВКЛАДКА "БУДИЛЬНИКИ":
           - Добавьте будильники для игрового времени
           - Установите время в формате ЧЧ:ММ:СС
           - Добавьте описание для будильника
           - Будильник сработает когда игровое время достигнет заданного
        
        3. ВКЛАДКА "НАСТРОЙКИ":
           - Регулируйте скорость игрового времени с помощью ползунка
           - Изменяйте цвета интерфейса
           - Настройте звуковые уведомления
           - Выберите тему оформления (STALKER, темная, светлая)
           - Сохраняйте настройки для постоянного использования
        
        4. ВКЛАДКА "ПОМОЩЬ":
           - Здесь вы находитесь сейчас
           - Информация о программе и инструкции
        
        ВАЖНО:
        - Стандартная скорость игрового времени: 6870 мс
        - Это означает, что 1 реальная секунда = примерно 6.87 игровых секунд
        - Программа создана разработчиком Harper_IDS для сообщества IgromanDS
        - Программа работает в автономном режиме (без интернета)
        
        ПОДСКАЗКИ:
        - Используйте будильники для напоминаний о важных событиях в игре
        - Настройте внешний вид под свой вкус
        - Всегда сохраняйте настройки после изменения
        
        Для получения дополнительной помощи:
        - Обратитесь к сообществу IgromanDS
        - Используйте стандартные настройки, если не уверены
        - Посетите канал Harper в VK Video для обновлений
        
        Приятной игры в Stay Out!
        """
        
        help_text_widget = tk.Text(self.help_frame, wrap=tk.WORD, padx=20, pady=20, 
                                   bg=self.settings["background_color"], 
                                   fg=self.settings["text_color"],
                                   font=("Arial", 10))
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
    
    def toggle_sound(self):
        self.settings["alarm_sound_enabled"] = self.sound_var.get()
    
    def update_volume(self, value):
        self.settings["volume_level"] = int(float(value))
        self.volume_label.config(text=f"Уровень: {int(float(value))}%")
    
    def toggle_real_time(self):
        self.settings["show_real_time"] = self.show_real_time_var.get()
        if self.settings["show_real_time"]:
            if not hasattr(self, 'real_time_label'):
                self.real_time_label = ttk.Label(self.main_frame, text="Реальное время: --:--:--", 
                                           font=("Arial", 16), foreground=self.settings["text_color"])
                self.real_time_label.pack(pady=5)
        else:
            if hasattr(self, 'real_time_label'):
                self.real_time_label.pack_forget()
    
    def toggle_auto_save(self):
        self.settings["auto_save_on_exit"] = self.auto_save_var.get()
    
    def save_settings(self):
        self.settings["game_tick_duration"] = self.speed_var.get()
        self.settings["background_color"] = self.bg_color_var.get()
        self.settings["text_color"] = self.text_color_var.get()
        self.settings["accent_color"] = self.accent_color_var.get()
        self.settings["alarm_sound_enabled"] = self.sound_var.get()
        self.settings["volume_level"] = self.volume_var.get()
        self.settings["theme"] = self.theme_var.get()
        self.settings["show_real_time"] = self.show_real_time_var.get()
        self.settings["auto_save_on_exit"] = self.auto_save_var.get()
        
        try:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Настройки", "Настройки успешно сохранены!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {str(e)}")
    
    def reset_settings(self):
        # Reset to default settings
        self.settings = {
            "game_tick_duration": 6870,
            "real_time_tick": 1000,
            "background_color": "#2c2c2c",
            "text_color": "#ffffff",
            "accent_color": "#ff6b35",
            "alarm_sound_enabled": True,
            "volume_level": 100,
            "theme": "stalker",
            "auto_save_on_exit": True,
            "show_real_time": True
        }
        
        # Update UI elements
        self.speed_var.set(6870)
        self.bg_color_var.set("#2c2c2c")
        self.text_color_var.set("#ffffff")
        self.accent_color_var.set("#ff6b35")
        self.sound_var.set(True)
        self.volume_var.set(100)
        self.theme_var.set("stalker")
        self.show_real_time_var.set(True)
        self.auto_save_var.set(True)
        
        # Apply changes
        self.root.configure(bg="#2c2c2c")
        self.game_timer_label.configure(foreground="#ffffff")
        self.status_label.configure(foreground="#ffffff")
        self.info_label.configure(foreground="#cccccc")
        
        messagebox.showinfo("Настройки", "Все настройки сброшены до стандартных значений!")
        self.save_settings()
    
    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
                    
                # Apply loaded settings
                self.root.configure(bg=self.settings["background_color"])
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
        # Update real time display if enabled
        if hasattr(self, 'real_time_label') and self.settings["show_real_time"]:
            current_real_time = datetime.now().strftime("%H:%M:%S")
            self.real_time_label.config(text=f"Реальное время: {current_real_time}")
        
        if self.is_running and not self.is_paused:
            # Calculate current game time
            real_elapsed = (time.time() * 1000 - self.start_time)  # in ms
            game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
            
            # Add any time that was accumulated while paused
            total_game_time = game_time_ms + self.elapsed_at_pause
            
            self.game_timer_label.config(text=f"Время игры: {self.format_time(total_game_time)}")
            
            # Check for alarms
            current_game_time_str = self.format_time(total_game_time)
            for alarm in self.alarms:
                if alarm["time"] == current_game_time_str and not alarm["fired"]:
                    self.trigger_alarm(alarm)
                    alarm["fired"] = True
        
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
        self.game_timer_label.config(text="Время игры: 00:00:00")
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
                self.game_timer_label.config(text=f"Время игры: {self.format_time(total_ms)}")
                
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат времени. Используйте ЧЧ:ММ:СС в 24-часовом формате.")
    
    def add_alarm(self):
        time_str = self.alarm_time_entry.get()
        desc = self.alarm_desc_entry.get()
        
        if not time_str:
            messagebox.showerror("Ошибка", "Введите время будильника в формате ЧЧ:ММ:СС")
            return
        
        try:
            # Validate time format
            parts = time_str.split(':')
            if len(parts) != 3:
                raise ValueError("Неверный формат")
            
            hours, minutes, seconds = map(int, parts)
            
            if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
                raise ValueError("Недопустимые значения")
            
            # Add alarm to list
            alarm = {
                "time": time_str,
                "description": desc or "Будильник",
                "fired": False
            }
            self.alarms.append(alarm)
            
            # Add to treeview
            status = "Ожидает" if not alarm["fired"] else "Сработал"
            self.alarms_tree.insert("", "end", values=(alarm["time"], alarm["description"], status))
            
            # Clear input fields
            self.alarm_time_entry.delete(0, tk.END)
            self.alarm_desc_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат времени. Используйте ЧЧ:ММ:СС в 24-часовом формате.")
    
    def delete_alarm(self):
        selected = self.alarms_tree.selection()
        if selected:
            # Get the selected item
            item = self.alarms_tree.item(selected[0])
            time_val = item['values'][0]
            
            # Remove from alarms list
            for i, alarm in enumerate(self.alarms):
                if alarm["time"] == time_val:
                    del self.alarms[i]
                    break
            
            # Remove from treeview
            self.alarms_tree.delete(selected)
    
    def clear_alarms(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить все будильники?"):
            self.alarms = []
            for item in self.alarms_tree.get_children():
                self.alarms_tree.delete(item)
    
    def trigger_alarm(self, alarm):
        if self.settings["alarm_sound_enabled"]:
            # Play system beep or sound
            try:
                # Try to play a system sound
                for _ in range(3):  # Play 3 times
                    winsound.Beep(1000, 500)  # Frequency, duration
                    time.sleep(0.1)
            except:
                # If winsound fails, use tkinter bell
                self.root.bell()
        
        # Show notification
        messagebox.showinfo("Будильник", f"Сработал будильник!\nВремя: {alarm['time']}\nОписание: {alarm['description']}")
    
    def test_sound(self):
        try:
            # Test the alarm sound
            winsound.Beep(800, 300)  # Frequency, duration
            time.sleep(0.1)
            winsound.Beep(1000, 300)
            time.sleep(0.1)
            winsound.Beep(1200, 300)
        except:
            # If winsound fails, use tkinter bell
            self.root.bell()
            messagebox.showinfo("Тест", "Звук протестирован (использован системный звонок)")
    
    def on_closing(self):
        # Save settings if auto-save is enabled
        if self.settings["auto_save_on_exit"]:
            self.save_settings()
        
        # Destroy the window
        self.root.destroy()

def main():
    root = tk.Tk()
    app = StayOutTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()