import os
import subprocess
import sys
from pathlib import Path

def create_icon():
    """Create a simple icon file for the application"""
    # Create a basic icon using Pillow if available, otherwise skip
    try:
        from PIL import Image
        # Create a simple image for the icon
        img = Image.new('RGB', (64, 64), color=(44, 44, 44))  # STALKER theme dark color
        # Draw a simple symbol - radiation sign
        for x in range(20, 44):
            for y in range(20, 44):
                # Create a simple radiation symbol
                if 20 <= x <= 44 and 20 <= y <= 44:
                    if (x-32)**2 + (y-32)**2 < 144:  # Circle
                        img.putpixel((x, y), (255, 107, 53))  # Accent color
        img.save('icon.ico', format='ICO', sizes=[(64, 64)])
        print("Icon created successfully")
    except ImportError:
        # If Pillow is not available, create a placeholder
        print("Pillow not available, skipping icon creation")
        # For now, we'll just touch the file to have something
        Path('icon.ico').touch()
        return False
    return True

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        # Install PyInstaller if not already installed
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], 
                      check=True, capture_output=True)
        print("PyInstaller installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing PyInstaller: {e}")
        return False

    # Create icon
    icon_created = create_icon()
    
    # Build the executable using the spec file
    try:
        cmd = [sys.executable, '-m', 'PyInstaller', 'stay_out_timer.spec']
        if not icon_created:
            # If icon wasn't created, modify the command to not use an icon
            cmd = [sys.executable, '-m', 'PyInstaller', '--onefile', '--windowed', 
                   '--name=StayOutTimer', 'main.py']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Executable built successfully")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_zip():
    """Create a ZIP archive of the executable and related files"""
    import zipfile
    import shutil
    
    # Ensure dist directory exists
    dist_path = Path('dist')
    if not dist_path.exists():
        print("Distribution directory not found. Build executable first.")
        return False
    
    # Create a ZIP file
    zip_filename = 'StayOutTimer_Windows_v1.0.0.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add the executable
        exe_path = dist_path / 'StayOutTimer.exe'
        if exe_path.exists():
            zipf.write(exe_path, 'StayOutTimer.exe')
        
        # Add documentation
        readme_content = """Таймер для игры Stay Out v1.0.0
Разработчик: Harper_IDS
Для сообщества IgromanDS

ИНСТРУКЦИЯ:
1. Запустите StayOutTimer.exe
2. Используйте вкладки для настройки времени, будильников и параметров
3. Программа сохраняет настройки автоматически

ОПИСАНИЕ:
- Отображает игровое и реальное время одновременно
- Настраиваемая скорость игрового времени (по умолчанию 6870 мс)
- Автономная работа (без интернета)
- Легкий способ ввода игрового времени
- Таймеры и будильники для игрового времени
- Сохранение настроек автоматически
- Кнопка сброса настроек
- Все виды настроек (темы, громкость, звуки)
- Справочник для новичков
- Система автосохранения состояния при выходе
- Автоматический расчет прошедшего игрового времени при перезапуске
- Тематическое оформление в стиле Сталкер
- Исполняемый файл без видимой консоли
- Сменяемая иконка

Ссылка на VK Video Harper: https://vk.com/video/harper_ids

С уважением, Harper_IDS для сообщества IgromanDS
"""
        zipf.writestr('README.txt', readme_content)
    
    print(f"ZIP archive created: {zip_filename}")
    return True

if __name__ == "__main__":
    print("Building Stay Out Timer executable...")
    
    # Change to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = build_executable()
    if success:
        create_zip()
        print("Build process completed!")
    else:
        print("Build process failed!")