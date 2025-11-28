import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta
import time
import threading
import platform
if platform.system() == "Windows":
    import winsound  # For Windows sound alerts
else:
    import subprocess  # For cross-platform sound alerts

class StayOutClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Часы Stay Out v1.0.0")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Default settings
        self.default_settings = {
            "game_speed": 6870,
            "theme": "light",
            "volume": 70,
            "show_notifications": True,
            "auto_save": True,
            "window_position": (100, 100),
            "window_size": (600, 700),
            "alarms": []
        }
        
        # Load settings
        self.settings = self.load_settings()
        
        # Game time variables
        self.start_time = 0
        self.is_running = False
        self.timer_thread = None
        self.stop_event = threading.Event()
        
        # Create UI
        self.create_ui()
        self.update_time_display()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start update loop
        self.update_loop()

    def load_settings(self):
        """Load settings from file or return defaults"""
        settings_file = "stay_out_settings.json"
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all settings exist
                    settings = self.default_settings.copy()
                    settings.update(loaded_settings)
                    return settings
            else:
                return self.default_settings.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()

    def save_settings(self):
        """Save settings to file"""
        if self.settings.get("auto_save", True):
            settings_file = "stay_out_settings.json"
            try:
                with open(settings_file, 'w', encoding='utf-8') as f:
                    json.dump(self.settings, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Error saving settings: {e}")

    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Сброс настроек", "Вы уверены, что хотите сбросить все настройки к заводским?"):
            self.settings = self.default_settings.copy()
            self.save_settings()
            messagebox.showinfo("Настройки сброшены", "Настройки были сброшены к заводским значениям.")

    def create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Часы Stay Out", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Radiation icon (using text since we can't embed images easily)
        radiation_label = ttk.Label(main_frame, text="☢", font=("Arial", 24), foreground="red")
        radiation_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # Time displays
        self.game_time_label = ttk.Label(main_frame, text="Время игры: --:--:--", font=("Arial", 14))
        self.game_time_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.real_time_label = ttk.Label(main_frame, text="Реальное время: --:--:--", font=("Arial", 14))
        self.real_time_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        
        self.start_button = ttk.Button(button_frame, text="Запустить таймер", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        
        self.stop_button = ttk.Button(button_frame, text="Остановить таймер", command=self.stop_timer)
        self.stop_button.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        self.set_time_button = ttk.Button(button_frame, text="Установить время", command=self.set_game_time)
        self.set_time_button.grid(row=0, column=2, padx=5, sticky=(tk.W, tk.E))
        
        # Game speed control
        speed_frame = ttk.LabelFrame(main_frame, text="Скорость игрового времени", padding="10")
        speed_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(speed_frame, text="Значение (мс):").grid(row=0, column=0, sticky=tk.W)
        self.speed_var = tk.IntVar(value=self.settings["game_speed"])
        self.speed_scale = ttk.Scale(speed_frame, from_=0, to=10000, orient=tk.HORIZONTAL, 
                                     variable=self.speed_var, command=self.update_speed)
        self.speed_scale.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E))
        
        self.speed_value_label = ttk.Label(speed_frame, text=str(self.settings["game_speed"]))
        self.speed_value_label.grid(row=0, column=2, padx=5)
        
        speed_frame.columnconfigure(1, weight=1)
        
        # Alarms section
        alarms_frame = ttk.LabelFrame(main_frame, text="Будильники", padding="10")
        alarms_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(5, weight=1)
        
        self.alarms_listbox = tk.Listbox(alarms_frame)
        self.alarms_listbox.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        alarms_frame.rowconfigure(0, weight=1)
        
        add_alarm_button = ttk.Button(alarms_frame, text="Добавить будильник", command=self.add_alarm)
        add_alarm_button.grid(row=1, column=0, padx=(0, 5))
        
        remove_alarm_button = ttk.Button(alarms_frame, text="Удалить будильник", command=self.remove_alarm)
        remove_alarm_button.grid(row=1, column=1, padx=5)
        
        test_alarm_button = ttk.Button(alarms_frame, text="Тест будильника", command=self.test_alarm)
        test_alarm_button.grid(row=1, column=2, padx=(5, 0))
        
        # Settings and help buttons
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        settings_button = ttk.Button(bottom_frame, text="Настройки", command=self.open_settings)
        settings_button.grid(row=0, column=0, padx=(0, 5))
        
        reset_button = ttk.Button(bottom_frame, text="Сброс настроек", command=self.reset_settings)
        reset_button.grid(row=0, column=1, padx=5)
        
        help_button = ttk.Button(bottom_frame, text="Справка", command=self.open_help)
        help_button.grid(row=0, column=2, padx=(5, 0))
        
        # About section
        about_frame = ttk.LabelFrame(main_frame, text="О программе", padding="10")
        about_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        about_text = "Программа создана для игрового сообщества IgromanDS\n" \
                     "Разработчик: Harper_IDS\n" \
                     "Версия: 1.0.0\n\n" \
                     "Для перехода на сайт Подписывайтесь на мой ВК ВИДЕО Harper:\n" \
                     "https://vkvideo.ru/@igroman_ds"
        
        about_label = ttk.Label(about_frame, text=about_text, justify=tk.LEFT)
        about_label.grid(row=0, column=0, sticky=tk.W)
        
        # Update alarms list
        self.update_alarms_list()

    def update_speed(self, value):
        """Update game speed setting"""
        self.settings["game_speed"] = int(float(value))
        self.speed_value_label.config(text=str(int(float(value))))
        self.save_settings()

    def start_timer(self):
        """Start the game timer"""
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time() * 1000  # Convert to milliseconds
            self.stop_event.clear()
            self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
            self.timer_thread.start()

    def stop_timer(self):
        """Stop the game timer"""
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join(timeout=1)

    def set_game_time(self):
        """Set the game time manually"""
        time_str = simpledialog.askstring("Установить время", 
                                         "Введите время игры в формате ЧЧ:ММ:СС (24-часовой формат):")
        if time_str:
            try:
                hours, minutes, seconds = map(int, time_str.split(':'))
                if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
                    # Calculate the time in milliseconds
                    game_time_ms = hours * 3600000 + minutes * 60000 + seconds * 1000
                    # Calculate start time based on current real time and game time
                    real_time_ms = time.time() * 1000
                    # Adjust start time so that current game time matches the input
                    speed_factor = self.settings["game_speed"] / 1000.0
                    self.start_time = real_time_ms - (game_time_ms / speed_factor)
                    
                    # Update display immediately
                    self.update_time_display()
                else:
                    messagebox.showerror("Ошибка", "Некорректное время. Часы: 0-23, Минуты: 0-59, Секунды: 0-59")
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат времени. Используйте ЧЧ:ММ:СС")

    def timer_loop(self):
        """Main timer loop running in separate thread"""
        while self.is_running and not self.stop_event.is_set():
            time.sleep(0.1)  # Update every 100ms for smooth display

    def update_time_display(self):
        """Update the time displays"""
        if self.is_running:
            current_time_ms = time.time() * 1000
            elapsed_real_time = current_time_ms - self.start_time
            # Calculate game time based on speed setting
            speed_factor = self.settings["game_speed"] / 1000.0
            game_time_ms = elapsed_real_time * speed_factor
            
            # Format game time (24-hour format)
            total_seconds = int(game_time_ms / 1000)
            hours = (total_seconds // 3600) % 24
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            game_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            # If not running, show placeholder or last time
            game_time_str = "--:--:--"
        
        # Get real time
        real_time_str = datetime.now().strftime("%H:%M:%S")
        
        # Update labels
        self.game_time_label.config(text=f"Время игры: {game_time_str}")
        self.real_time_label.config(text=f"Реальное время: {real_time_str}")
        
        # Check alarms
        self.check_alarms(game_time_str)
    
    def check_alarms(self, current_game_time):
        """Check if any alarms should trigger"""
        for alarm_time in self.settings.get("alarms", []):
            if current_game_time == alarm_time and self.settings.get("show_notifications", True):
                self.trigger_alarm()

    def trigger_alarm(self):
        """Trigger alarm notification"""
        if self.settings.get("show_notifications", True):
            # Play system default beep
            self.play_beep()
            # Show notification
            messagebox.showinfo("Будильник", "Время будильника достигнуто!")

    def play_beep(self):
        """Play system beep sound (cross-platform)"""
        if platform.system() == "Windows":
            winsound.MessageBeep()
        else:
            # On Unix-like systems, try to use system beep
            try:
                subprocess.run(["beep"], check=False, timeout=1)  # If beep command is available
            except (subprocess.SubprocessError, FileNotFoundError):
                # Fallback: use tkinter bell
                self.root.bell()

    def update_loop(self):
        """Main update loop running in GUI thread"""
        self.update_time_display()
        # Schedule next update
        self.root.after(100, self.update_loop)  # Update every 100ms

    def add_alarm(self):
        """Add a new alarm"""
        time_str = simpledialog.askstring("Добавить будильник", 
                                         "Введите время будильника в формате ЧЧ:ММ:СС (24-часовой формат):")
        if time_str:
            try:
                hours, minutes, seconds = map(int, time_str.split(':'))
                if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
                    alarm_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                    alarms = self.settings.setdefault("alarms", [])
                    if alarm_time not in alarms:
                        alarms.append(alarm_time)
                        self.settings["alarms"] = sorted(alarms)
                        self.save_settings()
                        self.update_alarms_list()
                    else:
                        messagebox.showinfo("Информация", "Будильник уже существует")
                else:
                    messagebox.showerror("Ошибка", "Некорректное время. Часы: 0-23, Минуты: 0-59, Секунды: 0-59")
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат времени. Используйте ЧЧ:ММ:СС")

    def remove_alarm(self):
        """Remove selected alarm"""
        selection = self.alarms_listbox.curselection()
        if selection:
            idx = selection[0]
            alarms = self.settings.get("alarms", [])
            if 0 <= idx < len(alarms):
                alarms.pop(idx)
                self.settings["alarms"] = alarms
                self.save_settings()
                self.update_alarms_list()
        else:
            messagebox.showinfo("Информация", "Выберите будильник для удаления")

    def test_alarm(self):
        """Test alarm sound"""
        self.play_beep()
        messagebox.showinfo("Тест", "Звук будильника воспроизведен")

    def update_alarms_list(self):
        """Update the alarms listbox"""
        self.alarms_listbox.delete(0, tk.END)
        for alarm in self.settings.get("alarms", []):
            self.alarms_listbox.insert(tk.END, alarm)

    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки")
        settings_window.geometry("400x500")
        
        # Create notebook for different settings categories
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings tab
        general_frame = ttk.Frame(notebook, padding="10")
        notebook.add(general_frame, text="Общие")
        
        ttk.Label(general_frame, text="Скорость игрового времени:").grid(row=0, column=0, sticky=tk.W, pady=5)
        general_speed_var = tk.IntVar(value=self.settings["game_speed"])
        general_speed_scale = ttk.Scale(general_frame, from_=0, to=10000, orient=tk.HORIZONTAL, 
                                        variable=general_speed_var)
        general_speed_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        general_frame.columnconfigure(1, weight=1)
        
        ttk.Label(general_frame, text="Громкость (0-100):").grid(row=1, column=0, sticky=tk.W, pady=5)
        volume_var = tk.IntVar(value=self.settings["volume"])
        volume_scale = ttk.Scale(general_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                 variable=volume_var)
        volume_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        show_notifications_var = tk.BooleanVar(value=self.settings["show_notifications"])
        ttk.Checkbutton(general_frame, text="Показывать уведомления", 
                        variable=show_notifications_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        auto_save_var = tk.BooleanVar(value=self.settings["auto_save"])
        ttk.Checkbutton(general_frame, text="Автосохранение настроек", 
                        variable=auto_save_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Appearance settings tab
        appearance_frame = ttk.Frame(notebook, padding="10")
        notebook.add(appearance_frame, text="Внешний вид")
        
        ttk.Label(appearance_frame, text="Тема:").grid(row=0, column=0, sticky=tk.W, pady=5)
        theme_var = tk.StringVar(value=self.settings["theme"])
        theme_combo = ttk.Combobox(appearance_frame, textvariable=theme_var, 
                                   values=["light", "dark", "default"])
        theme_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        appearance_frame.columnconfigure(1, weight=1)
        
        # Apply settings button
        def apply_settings():
            self.settings["game_speed"] = general_speed_var.get()
            self.settings["volume"] = volume_var.get()
            self.settings["show_notifications"] = show_notifications_var.get()
            self.settings["auto_save"] = auto_save_var.get()
            self.settings["theme"] = theme_var.get()
            
            # Update main UI elements
            self.speed_var.set(self.settings["game_speed"])
            self.speed_scale.set(self.settings["game_speed"])
            self.speed_value_label.config(text=str(self.settings["game_speed"]))
            
            self.save_settings()
            messagebox.showinfo("Настройки", "Настройки сохранены!")
        
        apply_button = ttk.Button(settings_window, text="Применить", command=apply_settings)
        apply_button.pack(pady=10)

    def open_help(self):
        """Open help window with step-by-step guide"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка")
        help_window.geometry("700x600")
        
        # Create scrollable text widget
        text_frame = ttk.Frame(help_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        help_window.columnconfigure(0, weight=1)
        help_window.rowconfigure(0, weight=1)
        
        # Add help content
        help_content = """
Справочник по использованию часов Stay Out
==========================================

1. Основные функции
-------------------
1.1. Просмотр времени
    - Время игры: показывает текущее игровое время
    - Реальное время: показывает текущее системное время

1.2. Управление таймером
    - Запустить таймер: начинает отсчет игрового времени
    - Остановить таймер: останавливает отсчет игрового времени
    - Установить время: позволяет ввести текущее игровое время вручную

2. Настройка скорости времени
------------------------------
2.1. Скорость игрового времени
    - Ползунок позволяет регулировать соотношение игрового и реального времени
    - Значение по умолчанию: 6870 (на основе исходного кода)
    - Диапазон: 0-10000 миллисекунд

3. Работа с будильниками
------------------------
3.1. Добавление будильника
    - Нажмите "Добавить будильник"
    - Введите время в формате ЧЧ:ММ:СС (24-часовой формат)
    - Будильник сработает, когда игровое время достигнет установленного

3.2. Удаление будильника
    - Выберите будильник из списка
    - Нажмите "Удалить будильник"

3.3. Тест будильника
    - Проверяет работу звукового уведомления

4. Настройки программы
----------------------
4.1. Общие настройки
    - Скорость игрового времени: регулировка темпа игры
    - Громкость: уровень звука уведомлений
    - Показывать уведомления: включить/выключить звуковые сигналы
    - Автосохранение настроек: автоматическое сохранение изменений

4.2. Внешний вид
    - Тема: выбор цветовой схемы интерфейса

4.3. Сброс настроек
    - Кнопка "Сброс настроек" возвращает все параметры к значениям по умолчанию

5. Практическое применение
--------------------------
5.1. Синхронизация времени
    - Перед выходом из игры запишите текущее игровое время
    - Введите это время в программе через "Установить время"
    - Запустите таймер для отслеживания игрового времени

5.2. Отслеживание событий
    - Используйте будильники для оповещения о спавне мобов и НПС
    - Установите будильники на важные игровые события
    - Следите за игровым временем для планирования действий

6. Часто задаваемые вопросы
---------------------------
6.1. Для чего нужна синхронизация времени?
    - Позволяет отслеживать игровое время без запуска игры
    - Помогает планировать действия в игре
    - Облегчает отслеживание циклов спавна мобов и НПС

6.2. Как часто нужно синхронизировать время?
    - Достаточно один раз перед выходом из игры
    - Время будет автоматически отсчитываться с учетом игровой скорости

6.3. Что делать если время не совпадает?
    - Проверьте правильность введенного времени
    - Убедитесь, что скорость игрового времени установлена правильно
    - Перезапустите таймер при необходимости

7. О программе
--------------
7.1. Информация
    - Программа создана для игрового сообщества IgromanDS
    - Разработчик: Harper_IDS
    - Версия: 1.0.0

7.2. Дополнительная информация
    - Для перехода на сайт Подписывайтесь на мой ВК ВИДЕО Harper
    - Ссылка: https://vkvideo.ru/@igroman_ds
"""
        
        text_widget.insert(tk.END, help_content)
        text_widget.config(state=tk.DISABLED)

    def on_closing(self):
        """Handle window closing event"""
        self.stop_timer()
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StayOutClock(root)
    root.mainloop()