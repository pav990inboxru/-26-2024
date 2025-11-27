"""
Test script to verify the timer logic without GUI dependencies
"""

import time
import json
import os

class TimerLogic:
    def __init__(self):
        # Default settings
        self.settings = {
            "game_tick_duration": 6870,  # Default speed from original code
            "real_time_tick": 1000,
        }
        
        # Timer variables
        self.start_time = 0
        self.is_running = False
        self.is_paused = False
        self.paused_time = 0
        self.elapsed_at_pause = 0
    
    def format_time(self, elapsed_time_ms):
        """Format time in milliseconds to HH:MM:SS format"""
        total_seconds = int(elapsed_time_ms // 1000)
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_current_game_time(self):
        """Get the current game time in milliseconds"""
        if self.is_running and not self.is_paused:
            # Calculate current game time
            real_elapsed = (time.time() * 1000 - self.start_time)  # in ms
            game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
            
            # Add any time that was accumulated while paused
            total_game_time = game_time_ms + self.elapsed_at_pause
            return total_game_time
        else:
            # If not running, return the accumulated time
            return self.elapsed_at_pause
    
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
            print("Таймер запущен")
    
    def pause_timer(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.paused_time = time.time() * 1000
            
            # Calculate the elapsed game time at the moment of pause
            real_elapsed = (time.time() * 1000 - self.start_time)
            game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
            self.elapsed_at_pause += game_time_ms
            
            self.is_running = False
            print(f"Таймер на паузе. Текущее время: {self.format_time(self.elapsed_at_pause)}")
    
    def stop_timer(self):
        if self.is_running:
            if not self.is_paused:
                # Calculate accumulated time before stopping
                real_elapsed = (time.time() * 1000 - self.start_time)
                game_time_ms = real_elapsed * self.settings["game_tick_duration"] / self.settings["real_time_tick"]
                self.elapsed_at_pause += game_time_ms
            
            self.is_running = False
            self.is_paused = False
            print(f"Таймер остановлен. Текущее время: {self.format_time(self.elapsed_at_pause)}")
    
    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.elapsed_at_pause = 0
        self.start_time = time.time() * 1000
        print("Таймер сброшен")
    
    def set_time(self, hours, minutes, seconds):
        """Set the timer to a specific time"""
        total_ms = hours * 3600000 + minutes * 60000 + seconds * 1000
        self.elapsed_at_pause = total_ms
        self.start_time = time.time() * 1000
        print(f"Время установлено: {self.format_time(total_ms)}")

def main():
    print("Тестирование логики таймера Stay Out...")
    timer = TimerLogic()
    
    print("\n1. Тест форматирования времени:")
    print(f"0 мс: {timer.format_time(0)}")
    print(f"3661000 мс (1ч 1м 1с): {timer.format_time(3661000)}")
    
    print("\n2. Тест установки времени:")
    timer.set_time(12, 30, 45)  # 12:30:45
    print(f"Текущее игровое время: {timer.format_time(timer.get_current_game_time())}")
    
    print("\n3. Тест запуска таймера:")
    timer.start_timer()
    print(f"Таймер запущен, время: {timer.format_time(timer.get_current_game_time())}")
    
    print("\n4. Тест паузы:")
    time.sleep(0.1)  # Simulate some time passing
    timer.pause_timer()
    print(f"После паузы: {timer.format_time(timer.get_current_game_time())}")
    
    print("\n5. Тест возобновления:")
    timer.start_timer()
    print(f"После возобновления: {timer.format_time(timer.get_current_game_time())}")
    
    print("\n6. Тест остановки:")
    time.sleep(0.1)  # Simulate some time passing
    timer.stop_timer()
    
    print("\n7. Тест сброса:")
    timer.reset_timer()
    print(f"После сброса: {timer.format_time(timer.get_current_game_time())}")
    
    print("\nТестирование завершено успешно!")

if __name__ == "__main__":
    main()