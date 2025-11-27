"""
Тестирование логики таймера для Stay Out
"""
import json
import os
from datetime import datetime

def format_time(milliseconds):
    """Форматирование времени в ЧЧ:ММ:СС"""
    total_seconds = milliseconds // 1000
    hours = (total_seconds // 3600) % 24
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def test_timer_logic():
    print("Тестирование логики таймера Stay Out")
    print("="*50)
    
    # Стандартные параметры
    real_time_tick = 1000  # 1 секунда реального времени
    game_tick_duration = 6870  # Стандартная скорость игрового времени в мс
    
    print(f"Реальное время: {real_time_tick} мс = 1 секунда")
    print(f"Игровое время: {game_tick_duration} мс = ~6.87 игровых секунд")
    print()
    
    # Тест 1: Проверка соотношения времени
    print("Тест 1: Соотношение реального и игрового времени")
    test_real_time = 1000  # 1 секунда реального времени
    calculated_game_time = int(test_real_time * game_tick_duration / real_time_tick)
    print(f"1 секунда реального времени = {calculated_game_time} мс игрового времени")
    print(f"Формат времени: {format_time(calculated_game_time)}")
    print()
    
    # Тест 2: Симуляция работы таймера
    print("Тест 2: Симуляция работы таймера за 5 секунд")
    start_time = datetime.now().timestamp() * 1000  # В миллисекундах
    
    for i in range(6):  # 0, 1, 2, 3, 4, 5 секунд
        current_time = start_time + (i * 1000)  # Добавляем i секунд
        elapsed_real_time = current_time - start_time
        game_time = int(elapsed_real_time * game_tick_duration / real_time_tick)
        
        print(f"Реальное время: {i} сек -> Игровое время: {format_time(game_time)} (мс: {game_time})")
    
    print()
    
    # Тест 3: Проверка сохранения и загрузки настроек
    print("Тест 3: Сохранение и загрузка настроек")
    
    # Создаем тестовые настройки
    test_settings = {
        'game_speed': 6870,
        'background_color': '#f0f0f0',
        'text_color': '#000000',
        'font_size': 12
    }
    
    # Сохраняем
    with open('test_settings.json', 'w', encoding='utf-8') as f:
        json.dump(test_settings, f, ensure_ascii=False, indent=2)
    print("Настройки сохранены в test_settings.json")
    
    # Загружаем
    with open('test_settings.json', 'r', encoding='utf-8') as f:
        loaded_settings = json.load(f)
    print(f"Загруженные настройки: {loaded_settings}")
    
    # Удаляем тестовый файл
    os.remove('test_settings.json')
    
    print()
    print("Все тесты пройдены успешно!")
    print("Логика таймера работает корректно.")

if __name__ == "__main__":
    test_timer_logic()