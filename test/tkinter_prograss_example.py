import tkinter as tk
from tkinter import ttk
import time
import threading

def start_countdown():
    def countdown():
        for i in range(30, -1, -1):
            time_var.set(i)
            progress_var.set((30 - i) / 30 * 100)
            root.update_idletasks()
            time.sleep(1)

    # Start the countdown in a separate thread to keep the GUI responsive
    threading.Thread(target=countdown).start()

root = tk.Tk()
root.title("Countdown Timer")

time_var = tk.IntVar(value=30)
progress_var = tk.DoubleVar(value=0)

time_label = tk.Label(root, textvariable=time_var, font=("Helvetica", 48))
time_label.pack(pady=20)

progress = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress.pack(fill=tk.X, expand=1, pady=20)

start_button = tk.Button(root, text="Start Countdown", command=start_countdown)
start_button.pack(pady=20)

root.mainloop()