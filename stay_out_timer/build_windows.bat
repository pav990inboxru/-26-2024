@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo Creating Windows executable...
pyinstaller --onefile --windowed --name=StayOutTimer --icon= --add-data "settings.json;." main.py

echo.
echo Windows executable created in the 'dist' folder
echo You can find it at: /workspace/stay_out_timer/dist/StayOutTimer.exe
echo.
pause