import psutil
import ctypes
import os
import time
import win32api
import win32con
import win32process
import win32gui
import win32ui
from datetime import datetime

GAME_PROCESS_NAME = "YourGame.exe"  # Replace with your game process

# Known suspicious process or window keywords
SUSPICIOUS_KEYWORDS = [
    "cheat", "injector", "trainer", "engine", "hack", "debug", "cheatengine", "x64dbg", "ollydbg", "extreme injector"
]

# Log directory
LOG_FILE = "anticheat_log.txt"


class AntiCheat:
    def __init__(self):
        self.game_pid = None

    def log(self, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        entry = f"{timestamp} {message}"
        print(entry)
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")

    def message_box(self, title, text):
        ctypes.windll.user32.MessageBoxW(0, text, title, 0x40 | 0x1)

    def find_game_process(self):
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] and proc.info['name'].lower() == GAME_PROCESS_NAME.lower():
                self.game_pid = proc.info['pid']
                self.log(f"Game process found: PID {self.game_pid}")
                return True
        return False

    def scan_processes(self):
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                name = proc.info['name'].lower()
                pid = proc.info['pid']

                for keyword in SUSPICIOUS_KEYWORDS:
                    if keyword in name:
                        self.alert_suspicious_process(name, pid)
                        break

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def alert_suspicious_process(self, name, pid):
        msg = f"Suspicious process detected: {name} (PID {pid})"
        self.log(msg)
        self.message_box("Anti-Cheat Alert", msg)

    def check_handle_access(self):
        if not self.game_pid:
            return
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.pid == self.game_pid:
                    continue

                h_process = ctypes.windll.kernel32.OpenProcess(
                    win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
                    False, proc.pid
                )
                if h_process:
                    target_handle = ctypes.windll.kernel32.OpenProcess(
                        win32con.PROCESS_VM_READ | win32con.PROCESS_VM_WRITE,
                        False, self.game_pid
                    )
                    if target_handle:
                        self.alert_memory_access(proc.name(), proc.pid)
                        ctypes.windll.kernel32.CloseHandle(target_handle)
                ctypes.windll.kernel32.CloseHandle(h_process)
            except Exception:
                continue

    def alert_memory_access(self, name, pid):
        msg = f"Process {name} (PID {pid}) is accessing game memory!"
        self.log(msg)
        self.message_box("Anti-Cheat Alert", msg)

    def scan_windows(self):
        def enum_handler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).lower()
                for keyword in SUSPICIOUS_KEYWORDS:
                    if keyword in title:
                        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
                        self.alert_window_title(title, pid)

        win32gui.EnumWindows(enum_handler, None)

    def alert_window_title(self, title, pid):
        msg = f"Suspicious window title detected: '{title}' (PID {pid})"
        self.log(msg)
        self.message_box("Anti-Cheat Alert", msg)

    def run(self):
        self.log("Starting Anti-Cheat...")
        if not self.find_game_process():
            self.log("Game not found. Make sure it's running.")
            self.message_box("Anti-Cheat", "Game not found. Please start the game first.")
            return

        while True:
            try:
                self.scan_processes()
                self.check_handle_access()
                self.scan_windows()
                time.sleep(5)  # Run every 5 seconds
            except KeyboardInterrupt:
                self.log("Anti-Cheat stopped by user.")
                break
            except Exception as e:
                self.log(f"Error: {e}")


if __name__ == "__main__":
    ac = AntiCheat()
    ac.run()