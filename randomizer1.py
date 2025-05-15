import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
import os
from tkinter import scrolledtext, filedialog

DATA_FILE = "randomizer_data.txt"

def is_valid_number(new_value):
    return new_value.isdigit() or new_value == ""

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[('Text files', "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(history_box.get('1.0', tk.END))

def generate():
    try:
        start = int(entry_start.get())
        end = int(entry_end.get())
        range_options = list(map(str, range(start, end + 1)))
    except ValueError:
        range_options = []

    list_input = entry_list.get()
    custom_options = [item.strip() for item in list_input.split(",") if item.strip()]

    options = range_options + custom_options

    if check_var.get():
        options[:] = [opt for opt in options if opt not in history]

    if not options:
        messagebox.showerror("Помилка", "Немає доступних варіантів для генерації.")
        return

    choice = random.choice(options)
    result_label.config(text=choice)
    history.append(choice)
    save_history(choice)

def save_history(item):
    history_box.config(state="normal")
    history_box.insert(END, item + "\n")
    history_box.config(state="disabled")
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(item + "\n")

def clear_all():
    entry_start.delete(0, END)
    entry_end.delete(0, END)
    entry_list.delete(0, END)
    result_label.config(text="")
    history_box.config(state="normal")
    history_box.delete("1.0", END)
    history_box.config(state="disabled")
    global history
    history = []
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        pass

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                item = line.strip()
                if item:
                    history.append(item)
                    history_box.config(state="normal")
                    history_box.insert(END, item + "\n")
                    history_box.config(state="disabled")

win = Tk()
win.title("LuckyPick")
win.geometry("620x410")
win.resizable(False, False)

history = []

# Надписи
Label(win, text="Діапазон:", font=('Comic Sans MS', 14)).place(x=20, y=10)
Label(win, text="Від", font=('Comic Sans MS', 12)).place(x=20, y=40)
Label(win, text="До", font=('Comic Sans MS', 12)).place(x=140, y=40)

# Поля введення для діапазону
vcmd = (win.register(is_valid_number), "%P") # Для блокування писання тексту замість чисел
entry_start = Entry(win, font=('Comic Sans MS', 12), width=5, validate="key", validatecommand=vcmd)
entry_start.place(x=60, y=40)
entry_end = Entry(win, font=('Comic Sans MS', 12), width=5, validate="key", validatecommand=vcmd)
entry_end.place(x=180, y=40)

# Користувацький список
Label(win, text="Список (через кому):", font=('Comic Sans MS', 14)).place(x=300, y=10)
entry_list = Entry(win, font=('Comic Sans MS', 12), width=30)
entry_list.place(x=300, y=40)

# Кнопка генерації
generate_btn = Button(win, text="Згенерувати", font=('Comic Sans MS', 14), bg="lightgreen", command=generate)
generate_btn.place(x=50, y=100)

# Кнопка очищення
clear_btn = Button(win, text="Очистити", font=('Comic Sans MS', 14), bg="orange", command=clear_all)
clear_btn.place(x=200, y=100)

# Кнопка збережння файлу
save_button = Button(win, text='Збереження файлу', command=save_file)
save_button.place(x=20, y=366)

# Виведення результату
result_label = Label(win, text="", font=('Comic Sans MS', 20), fg="blue")
result_label.place(x=250, y=150)

# Чекбокс без повторів
check_var = IntVar()
check_btn = Checkbutton(win, text="Виключити повтори", variable=check_var, font=('Comic Sans MS', 12))
check_btn.place(x=20, y=160)

# Поле історії
Label(win, text="Історія:", font=('Comic Sans MS', 14)).place(x=20, y=200)
history_box = scrolledtext.ScrolledText(win, height=7, width=70, font=('Comic Sans MS', 10), state="disabled")
history_box.place(x=20, y=230)

load_history()
win.mainloop()
