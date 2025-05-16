# 🛡️ Anti-Cheat System for Windows Games

This script is a lightweight, real-time **anti-cheat system** designed to detect suspicious software or memory access targeting a running game. It checks for known cheat tools, debuggers, suspicious window titles, and unauthorized memory access.

---

## 🎯 Features

- 🔍 Scans running processes for suspicious tools (e.g., Cheat Engine, injectors, debuggers)
- 🧠 Detects **window titles** related to cheating tools
- 🔐 Monitors for **unauthorized memory access** to your game
- 📝 Logs all events with timestamps
- 💬 Shows Windows alert messages for flagged activities

---

## 🧰 Requirements

Install dependencies using `pip`:

```bash
pip install psutil pywin32
```

---

## 🛠️ Configuration

Set your game's process name in the script:

```python
GAME_PROCESS_NAME = "YourGame.exe"  # Change to your actual game's executable
```

---

## 🧾 Log Output

All alerts are printed in the console and saved in:

```bash
anticheat_log.txt
```

Example log entry:

```
[2025-05-16 12:34:56] Suspicious process detected: cheatengine.exe (PID 1234)
```

---

## 📋 What It Detects

### ✅ Process Scan
Checks for known **cheat-related process names** like:
- cheatengine
- injector
- x64dbg
- ollydbg

### ✅ Window Scan
Looks at visible window titles for suspicious keywords.

### ✅ Memory Handle Check
Flags processes that attempt to access the game’s memory space.

---

## 🚀 How to Run

```bash
python anticheat.py
```

The script will:
- Search for the game process
- Begin scanning every 5 seconds
- Show alerts and write to log file

---

## 🖼️ Example Alerts

- 💬 "Suspicious process detected: cheatengine.exe"
- 💬 "Suspicious window title detected: 'Extreme Injector'"
- 💬 "Process x64dbg.exe is accessing game memory!"

---

## ⚠️ Notes

- This script is designed for **Windows only**
- Should be run with sufficient privileges to access other process handles
- Customize `SUSPICIOUS_KEYWORDS` for your use case
