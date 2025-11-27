import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller уже установлен")
    except ImportError:
        print("Установка PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build the executable using PyInstaller"""
    print("Создание исполняемого файла...")
    
    # Change to the project directory
    os.chdir("/workspace/stay_out_timer")
    
    # Build command with options for a clean GUI application
    build_cmd = [
        "pyinstaller",
        "--onefile",           # Create a single executable file
        "--windowed",          # Create a GUI application (no console)
        "--name=StayOutTimer", # Name of the executable
        "--icon=",             # No icon specified
        "main.py"
    ]
    
    try:
        subprocess.run(build_cmd, check=True)
        print("Исполняемый файл успешно создан в папке 'dist'")
        print("Путь к исполняемому файлу: /workspace/stay_out_timer/dist/StayOutTimer.exe")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании исполняемого файла: {e}")
        return False
    
    return True

if __name__ == "__main__":
    install_pyinstaller()
    success = build_executable()
    
    if success:
        print("\nГотово! Исполняемый файл таймера Stay Out создан.")
        print("Вы можете найти его в папке: /workspace/stay_out_timer/dist/")
    else:
        print("\nПроизошла ошибка при создании исполняемого файла.")