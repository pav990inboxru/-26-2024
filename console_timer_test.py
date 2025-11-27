"""
Консольная версия таймера Stay Out для тестирования функций
"""
import json
import os
from datetime import datetime

class ConsoleStayOutTimer:
    def __init__(self):
        # Загрузка настроек
        self.load_settings()

        # Переменные таймера
        self.start_time = 0
        self.timer_running = False
        self.game_time = 0  # В миллисекундах
        self.real_time_tick = 1000  # 1 секунда реального времени
        self.game_tick_duration = self.settings.get('game_speed', 6870)  # Скорость игрового времени в мс
        
        print("Таймер для Stay Out (Консольная версия)")
        print("Программа создана разработчиком Harper_IDS для сообщества IgromanDS")
        print(f"Текущая скорость игрового времени: {self.game_tick_duration} мс")
        print()

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
                print(f"Загружено последнее сохраненное время: {self.format_time(self.game_time)}")
        except FileNotFoundError:
            print("Последнее время не найдено, начинаем с 00:00:00")

    def save_last_time(self):
        """Сохранение текущего времени"""
        with open('last_time.json', 'w', encoding='utf-8') as f:
            json.dump({'game_time': self.game_time}, f, ensure_ascii=False, indent=2)
        print(f"Время сохранено: {self.format_time(self.game_time)}")

    def format_time(self, milliseconds):
        """Форматирование времени в ЧЧ:ММ:СС"""
        total_seconds = milliseconds // 1000
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def start_timer(self):
        """Запуск таймера"""
        if not self.timer_running:
            self.start_time = datetime.now().timestamp() * 1000 - (self.game_time * self.real_time_tick / self.game_tick_duration)
            self.timer_running = True
            print("Таймер запущен")
        else:
            print("Таймер уже запущен")

    def pause_timer(self):
        """Пауза таймера"""
        if self.timer_running:
            # Вычисляем текущее игровое время на момент паузы
            current_time = datetime.now().timestamp() * 1000
            elapsed_real_time = current_time - self.start_time
            self.game_time = int(elapsed_real_time * self.game_tick_duration / self.real_time_tick)
            self.timer_running = False
            print(f"Таймер на паузе: {self.format_time(self.game_time)}")
        else:
            print("Таймер не запущен")

    def stop_timer(self):
        """Остановка таймера"""
        if self.timer_running:
            # Вычисляем текущее игровое время на момент остановки
            current_time = datetime.now().timestamp() * 1000
            elapsed_real_time = current_time - self.start_time
            self.game_time = int(elapsed_real_time * self.game_tick_duration / self.real_time_tick)
        self.timer_running = False
        print(f"Таймер остановлен: {self.format_time(self.game_time)}")
        self.save_last_time()

    def reset_timer(self):
        """Сброс таймера"""
        self.timer_running = False
        self.game_time = 0
        print("Таймер сброшен")
        # Удаляем сохраненное время при сбросе
        if os.path.exists('last_time.json'):
            os.remove('last_time.json')
            print("Файл последнего времени удален")

    def edit_time(self, time_str):
        """Редактирование времени"""
        try:
            time_parts = time_str.split(':')
            if len(time_parts) != 3:
                raise ValueError("Неверный формат")
            
            hours, minutes, seconds = map(int, time_parts)
            
            if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
                raise ValueError("Неверные значения времени")
            
            self.game_time = hours * 3600000 + minutes * 60000 + seconds * 1000
            print(f"Время изменено на: {self.format_time(self.game_time)}")
            
            # Если таймер запущен, пересчитываем start_time
            if self.timer_running:
                current_time = datetime.now().timestamp() * 1000
                self.start_time = current_time - (self.game_time * self.real_time_tick / self.game_tick_duration)
            
            self.save_last_time()
            
        except ValueError:
            print("Неверный формат времени. Используйте ЧЧ:ММ:СС (например, 12:30:45)")

    def change_game_speed(self, new_speed):
        """Изменение скорости игрового времени"""
        try:
            new_speed = int(new_speed)
            if 100 <= new_speed <= 10000:  # Разумные пределы
                old_speed = self.game_tick_duration
                # Пересчитываем game_time с новой скоростью
                if self.timer_running:
                    current_time = datetime.now().timestamp() * 1000
                    elapsed_real_time = current_time - self.start_time
                    # Сначала получаем реальное прошедшее время в условных "игровых единицах" при старой скорости
                    old_game_units = elapsed_real_time / self.real_time_tick * old_speed
                    # Затем пересчитываем game_time с новой скоростью
                    self.game_time = int(old_game_units)
                    # И пересчитываем start_time для новой скорости
                    self.start_time = current_time - (self.game_time * self.real_time_tick / new_speed)
                
                self.game_tick_duration = new_speed
                self.settings['game_speed'] = new_speed
                self.save_settings()
                print(f"Скорость игрового времени изменена с {old_speed} мс на {new_speed} мс")
            else:
                print("Значение должно быть от 100 до 10000 мс")
        except ValueError:
            print("Введите корректное числовое значение")

    def show_help(self):
        """Показать справку"""
        help_text = """
        Добро пожаловать в Таймер для Stay Out (Консольная версия)!
        
        Команды:
        start - запустить таймер
        pause - поставить таймер на паузу
        stop - остановить таймер
        reset - сбросить таймер
        edit HH:MM:SS - изменить время (например: edit 12:30:45)
        speed N - изменить скорость игрового времени (в мс, например: speed 6870)
        status - показать текущее время
        help - показать эту справку
        quit - выйти из программы
        
        Программа создана разработчиком Harper_IDS для сообщества IgromanDS
        """
        print(help_text)

def main():
    timer = ConsoleStayOutTimer()
    timer.load_last_time()
    
    print("Доступные команды: start, pause, stop, reset, edit HH:MM:SS, speed N, status, help, quit")
    
    while True:
        try:
            command = input("\nВведите команду: ").strip().lower()
            
            if command == "start":
                timer.start_timer()
            elif command == "pause":
                timer.pause_timer()
            elif command == "stop":
                timer.stop_timer()
            elif command == "reset":
                timer.reset_timer()
            elif command.startswith("edit "):
                time_str = command[5:]
                timer.edit_time(time_str)
            elif command.startswith("speed "):
                speed_str = command[6:]
                timer.change_game_speed(speed_str)
            elif command == "status":
                print(f"Текущее время: {timer.format_time(timer.game_time)}")
                print(f"Скорость игрового времени: {timer.game_tick_duration} мс")
                print(f"Таймер запущен: {'Да' if timer.timer_running else 'Нет'}")
            elif command == "help":
                timer.show_help()
            elif command == "quit":
                if timer.timer_running:
                    timer.stop_timer()
                print("До свидания!")
                break
            else:
                print("Неизвестная команда. Введите 'help' для списка команд.")
                
        except KeyboardInterrupt:
            if timer.timer_running:
                timer.stop_timer()
            print("\nПрограмма прервана. До свидания!")
            break
        except EOFError:
            if timer.timer_running:
                timer.stop_timer()
            print("\nДо свидания!")
            break

if __name__ == "__main__":
    main()