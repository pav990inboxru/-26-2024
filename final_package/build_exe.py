"""
Скрипт для создания исполняемого файла Stay Out Timer
"""
import subprocess
import sys
import os

def build_exe():
    print("Создание исполняемого файла Stay Out Timer...")
    print("Убедитесь, что PyInstaller установлен: pip install pyinstaller")
    
    try:
        # Проверяем, установлен ли PyInstaller
        subprocess.run([sys.executable, "-m", "pip", "show", "pyinstaller"], 
                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("PyInstaller найден")
    except subprocess.CalledProcessError:
        print("PyInstaller не установлен. Установите его командой:")
        print("pip install pyinstaller")
        return
    
    # Путь к основному файлу
    main_file = "stay_out_timer_full.py"
    
    if not os.path.exists(main_file):
        print(f"Файл {main_file} не найден!")
        return
    
    # Команда для создания .exe
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Один файл
        "--windowed",          # Без консоли (для GUI приложений)
        "--name", "StayOutTimer",  # Имя исполняемого файла
        "--clean",             # Очистить кэш перед сборкой
        main_file
    ]
    
    print("Выполняется команда:", " ".join(cmd))
    
    try:
        result = subprocess.run(cmd, check=True)
        print("Исполняемый файл успешно создан!")
        print("Найдите его в папке 'dist' как 'StayOutTimer.exe'")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании исполняемого файла: {e}")
        print("Проверьте, что все зависимости установлены и файл доступен.")

if __name__ == "__main__":
    build_exe()