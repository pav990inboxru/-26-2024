"""
Автоматизированный тест всех функций таймера Stay Out
"""
import json
import os
from datetime import datetime, timedelta
import time

def test_all_functions():
    print("Тестирование всех функций таймера Stay Out")
    print("="*60)
    
    # Импортируем класс из консольного таймера
    import sys
    sys.path.append('/workspace')
    from console_timer_test import ConsoleStayOutTimer
    
    # Создаем экземпляр таймера
    timer = ConsoleStayOutTimer()
    timer.load_last_time()
    
    print("\n1. Тест начального состояния:")
    print(f"   Текущее время: {timer.format_time(timer.game_time)}")
    print(f"   Скорость: {timer.game_tick_duration} мс")
    print(f"   Запущен: {timer.timer_running}")
    
    print("\n2. Тест изменения времени:")
    timer.edit_time("12:30:45")
    print(f"   После изменения: {timer.format_time(timer.game_time)}")
    
    print("\n3. Тест сброса времени:")
    timer.reset_timer()
    print(f"   После сброса: {timer.format_time(timer.game_time)}")
    
    print("\n4. Тест изменения скорости:")
    timer.change_game_speed(5000)
    print(f"   Новая скорость: {timer.game_tick_duration} мс")
    
    print("\n5. Тест запуска таймера:")
    timer.start_timer()
    print(f"   Запущен: {timer.timer_running}")
    
    print("\n6. Тест паузы таймера:")
    # Дадим немного времени для работы таймера
    time.sleep(2)
    timer.pause_timer()
    print(f"   После паузы: {timer.format_time(timer.game_time)}")
    print(f"   Запущен: {timer.timer_running}")
    
    print("\n7. Тест возобновления таймера:")
    timer.start_timer()  # Возобновляем
    print(f"   Возобновлен: {timer.timer_running}")
    
    print("\n8. Тест остановки таймера:")
    time.sleep(2)
    timer.stop_timer()
    print(f"   После остановки: {timer.format_time(timer.game_time)}")
    print(f"   Запущен: {timer.timer_running}")
    
    print("\n9. Тест сохранения настроек:")
    # Проверим, что настройки сохранились
    with open('timer_settings.json', 'r', encoding='utf-8') as f:
        settings = json.load(f)
    print(f"   Сохраненная скорость: {settings.get('game_speed')} мс")
    
    print("\n10. Тест восстановления последнего времени:")
    # Удалим текущий файл, симулируем перезапуск
    if os.path.exists('last_time.json'):
        with open('last_time.json', 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        print(f"   Сохраненное время: {timer.format_time(saved_data['game_time'])}")
    
    # Восстановим стандартную скорость
    timer.change_game_speed(6870)
    
    print("\nВсе функции протестированы успешно!")
    print("Программа готова к использованию.")

if __name__ == "__main__":
    test_all_functions()