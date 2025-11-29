#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Лаунчер для программы Таблиц рынка Stay Out
"""

import subprocess
import sys
import os

def main():
    print("Запуск программы Таблиц рынка Stay Out...")
    print("Автор: Harper_IDS")
    print("Создано для игрового сообщества IgromanDS")
    print("-" * 50)
    
    # Путь к основному файлу программы
    main_script = "stay_out_market_table_creator.py"
    
    if not os.path.exists(main_script):
        print(f"Ошибка: файл {main_script} не найден!")
        return
    
    try:
        # Запускаем основную программу
        result = subprocess.run([sys.executable, main_script], check=True)
        print("Программа завершена.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске программы: {e}")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")

if __name__ == "__main__":
    main()