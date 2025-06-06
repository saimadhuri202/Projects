# Simple Notepad

A simple and user-friendly Notepad application built with Python and Tkinter. This project supports multiple tabs, theme switching, session persistence, and basic file operations.

---

## Project Overview

This project was developed as a personal coding exercise to build a functional GUI-based notepad app with these main features:

- **Multiple Tabs:** Work on multiple documents within the same window.
- **Theme Support:** Switch between several predefined color themes.
- **Session Persistence:** Automatically save open tabs and their contents when closing, and restore them on next launch.
- **File Operations:** Create new files, open existing files, save, and save as.
- **Close Tab Confirmation:** Prompt user to save or discard changes before closing a tab.
- **Custom Icon Support:** Uses a `.ico` icon for the application window and when creating an `.exe` file.

---

## Technologies Used 🛠️

- **Language:** Python 3
- **GUI Framework:** Tkinter
- **Image Handling:** Pillow (for icon image conversion)
- **Packaging Tool:** PyInstaller (for generating `.exe` file)

---

## Installation & Setup 💻

1. **Ensure Python 3 is installed** on your system.

2. **Install dependencies** using pip:

   ```bash
   pip install Pillow
   pip install pyinstaller
