import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json

# Constants
DATA_DIR = "NotepadData"
SESSION_FILE = os.path.join(DATA_DIR, "session.json")
THEME_FILE = os.path.join(DATA_DIR, "theme.json")

# Define color themes
COLOR_THEMES = {
    "Classic White": {"bg": "#ffffff", "fg": "#000000"},
    "Night Mode": {"bg": "#1e1e1e", "fg": "#d4d4d4"},
    "Light Sky Blue": {"bg": "#add8e6", "fg": "#000000"},
    "Medium Yellow": {"bg": "#dbd770", "fg": "#000000"},
    "Pale Green": {"bg": "#98fb98", "fg": "#000000"}
}

# Default tab settings
DEFAULT_TAB_SIZE = {"width": 100, "height": 30, "font": ("Consolas", 12)}
DEFAULT_THEME = "Classic White"

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def new_tab(name=None, content="", theme=None):
    global tab_count
    tab = tk.Frame(notebook)
    theme_to_use = theme if theme in COLOR_THEMES else DEFAULT_THEME
    theme_colors = COLOR_THEMES[theme_to_use]
    text_widget = tk.Text(
        tab,
        wrap="word",
        bg=theme_colors["bg"],
        fg=theme_colors["fg"],
        insertbackground=theme_colors["fg"],
        font=DEFAULT_TAB_SIZE["font"],
        width=DEFAULT_TAB_SIZE["width"],
        height=DEFAULT_TAB_SIZE["height"]
    )
    text_widget.insert(1.0, content)
    text_widget.pack(expand=True, fill="both")

    tab_title = (name or f"Tab {tab_count}") + "  ×"
    notebook.add(tab, text=tab_title)
    notebook.select(tab)

    text_widgets[tab] = text_widget
    tab_titles[tab] = tab_title
    tab_filepaths[tab] = None
    tab_themes[tab] = theme_to_use
    tab_count += 1

def apply_theme(theme_name):
    global selected_theme
    selected_theme = theme_name
    current_tab_id = notebook.select()
    if not current_tab_id:
        return
    current_tab = notebook.nametowidget(current_tab_id)
    apply_theme_to_tab(current_tab, theme_name)
    tab_themes[current_tab] = theme_name

    with open(THEME_FILE, "w") as f:
        json.dump({"selected_theme": theme_name}, f)

def apply_theme_to_tab(tab, theme_name):
    theme = COLOR_THEMES[theme_name]
    text_widget = text_widgets.get(tab)
    if text_widget:
        text_widget.config(bg=theme["bg"], fg=theme["fg"], insertbackground=theme["fg"])

def save_file_for_tab(tab):
    text_widget = text_widgets.get(tab)
    if not text_widget:
        return False

    file_path = tab_filepaths.get(tab)

    if not file_path:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return False
        tab_filepaths[tab] = file_path

    text_content = text_widget.get(1.0, tk.END)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text_content)

    return True

def save_as_file_for_tab(tab):
    text_widget = text_widgets.get(tab)
    if not text_widget:
        return False

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not file_path:
        return False

    tab_filepaths[tab] = file_path

    text_content = text_widget.get(1.0, tk.END)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text_content)

    return True

def save_file():
    current_tab = notebook.select()
    if current_tab:
        tab = notebook.nametowidget(current_tab)
        return save_file_for_tab(tab)
    return False

def save_as_file():
    current_tab = notebook.select()
    if current_tab:
        tab = notebook.nametowidget(current_tab)
        return save_as_file_for_tab(tab)
    return False

def close_tab(tab):
    text_widget = text_widgets.get(tab)
    if text_widget:
        content = text_widget.get(1.0, tk.END).strip()
        if content:
            response = messagebox.askyesnocancel("Save Changes?", "Do you want to save changes before closing this tab?")
            if response:
                if not save_file_for_tab(tab):
                    return
            elif response is None:
                return
    notebook.forget(tab)
    del text_widgets[tab]
    del tab_titles[tab]
    tab_filepaths.pop(tab, None)
    tab_themes.pop(tab, None)

def close_selected_tab():
    current_tab_id = notebook.select()
    if not current_tab_id:
        return
    tab = notebook.nametowidget(current_tab_id)
    close_tab(tab)

def on_tab_right_click(event):
    x, y = event.x, event.y
    try:
        tab_index = notebook.index(f"@{x},{y}")
        tab_id = notebook.tabs()[tab_index]
        global right_clicked_tab
        right_clicked_tab = notebook.nametowidget(tab_id)
        context_menu.tk_popup(event.x_root, event.y_root)
    except:
        pass

def close_right_clicked_tab():
    if right_clicked_tab:
        close_tab(right_clicked_tab)

def on_tab_middle_click(event):
    # Middle click closes the tab
    x, y = event.x, event.y
    try:
        tab_index = notebook.index(f"@{x},{y}")
        tab_id = notebook.tabs()[tab_index]
        tab = notebook.nametowidget(tab_id)
        close_tab(tab)
    except:
        pass

def on_tab_double_click(event):
    # Double left click closes the tab
    x, y = event.x, event.y
    try:
        tab_index = notebook.index(f"@{x},{y}")
        tab_id = notebook.tabs()[tab_index]
        tab = notebook.nametowidget(tab_id)
        close_tab(tab)
    except:
        pass

def save_session_and_exit():
    ensure_data_dir()
    session_data = []
    for index, tab_id in enumerate(notebook.tabs()):
        tab = notebook.nametowidget(tab_id)
        text_widget = text_widgets[tab]
        title = tab_titles[tab]
        content = text_widget.get(1.0, tk.END)
        theme = tab_themes.get(tab, DEFAULT_THEME)

        file_path = tab_filepaths.get(tab)
        filename = f"tab{index + 1}.txt"

        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            file_path = filepath

        session_data.append({"title": title, "path": file_path, "theme": theme})

    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session_data, f)

    if selected_theme:
        with open(THEME_FILE, "w") as f:
            json.dump({"selected_theme": selected_theme}, f)

    window.destroy()

def load_session():
    ensure_data_dir()
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session_data = json.load(f)
        for tab_info in session_data:
            title = tab_info.get("title", "Untitled")
            file_path = tab_info.get("path") or os.path.join(DATA_DIR, tab_info.get("file", ""))
            theme = tab_info.get("theme", DEFAULT_THEME)
            content = ""
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            new_tab(name=title, content=content, theme=theme)
            tab = notebook.nametowidget(notebook.tabs()[-1])
            tab_filepaths[tab] = file_path
            tab_themes[tab] = theme
    else:
        new_tab()

def on_tab_changed(event):
    current_tab_id = notebook.select()
    if current_tab_id:
        current_tab = notebook.nametowidget(current_tab_id)
        theme = tab_themes.get(current_tab, DEFAULT_THEME)
        apply_theme_to_tab(current_tab, theme)

# Setup window
window = tk.Tk()
window.title("Simple Notepad")
window.geometry("700x500")
window.configure(bg="#f0f0f0")

# Set default tab width for ttk.Notebook tabs
style = ttk.Style()
style.theme_use('default')
style.configure("TNotebook.Tab", width=15)

# Menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0, bg="#f5f5f5", fg="#333333")
file_menu.add_command(label="New Tab", command=new_tab)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_command(label="Close Tab", command=close_selected_tab)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=save_session_and_exit)
menu_bar.add_cascade(label="File", menu=file_menu)

theme_menu = tk.Menu(menu_bar, tearoff=0, bg="#f5f5f5", fg="#333333")
for theme_name in COLOR_THEMES:
    theme_menu.add_command(label=theme_name, command=lambda name=theme_name: apply_theme(name))
menu_bar.add_cascade(label="Themes", menu=theme_menu)

# Notebook for tabs
notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill="both")
notebook.bind("<Button-3>", on_tab_right_click)
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
notebook.bind("<Button-2>", on_tab_middle_click)      # Middle click to close
notebook.bind("<Double-1>", on_tab_double_click)      # Double left click to close

# Context menu
context_menu = tk.Menu(window, tearoff=0)
context_menu.add_command(label="Close Tab", command=close_right_clicked_tab)

# Globals
tab_count = 1
text_widgets = {}
tab_titles = {}
tab_filepaths = {}
tab_themes = {}
right_clicked_tab = None
selected_theme = None

# Load session and theme
load_session()
if os.path.exists(THEME_FILE):
    with open(THEME_FILE, "r") as f:
        theme_data = json.load(f)
        selected_theme = theme_data.get("selected_theme")
else:
    selected_theme = DEFAULT_THEME

# Keyboard shortcuts
window.bind_all("<Control-s>", lambda event: save_file())

# On window close
window.protocol("WM_DELETE_WINDOW", save_session_and_exit)

window.mainloop()