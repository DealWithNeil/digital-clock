import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime, timedelta
import pytz
import threading
import time
import winsound 

class ModernClockApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Modern Clock")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        self.style = ttk.Style("darkly")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.create_clock_tab()
        self.create_world_time_tab()
        self.create_stopwatch_tab()
        self.create_timer_tab()
        self.create_alarm_tab()

    def create_clock_tab(self):
        self.clock_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.clock_tab, text="Clock")

        self.clock_label = ttk.Label(
            self.clock_tab,
            font=("Segoe UI", 50, "bold"),
            anchor="center"
        )
        self.clock_label.pack(pady=120)

        self.update_clock()

        def update_clock(self):
            now = datetime.now().strftime("%H:%M:%S")
            self.clock_label.config(text=now)
            self.root.after(1000, self.update_clock)

        def create_world_time_tab(self):
            self.world_tab = ttk.Frame(self.notebook)
            self.notebook.add(self.world_tab, text="World Time")

            self.city_var = tk.StringVar()
            cities = ["UTC", "US/Eastern", "Europe/London", "Asia/Tokyo", "Asia/Kolkata"]
            self.city_menu = ttk.Combobox(self.world_tab, values=cities, textvariable=self.city_var)
            self.city_menu.current(0)
            self.city_menu.pack(pady=20)

            self.world_label = ttk.Label(self.world_tab, font=("Segoe UI", 35))
            self.world_label.pack(pady=50)

            ttk.Button(self.world_tab, text="Show Time", command=self.show_world_time).pack()

        def show_world_time(self):
            timezone = pytz.timezone(self.city_var.get())
            city_time = datetime.now(timezone).strftime("%H:%M:%S")
            self.world_label.config(text=city_time)  

        def create_stopwatch_tab(self):
            self.stopwatch_tab = ttk.Frame(self.notebook)
            self.notebook.add(self.stopwatch_tab, text="Stopwatch")   

            self.running = False
            self.elapsed = timedelta()

            self.stopwatch_label = ttk.Label(self.stopwatch_tab, font=("Segoe UI", 40))
            self.stopwatch_label.pack(pady=80)
            self.stopwatch_label.config(text="00:00:00")

            btn_frame = ttk.Frame(self.stopwatch_tab)
            btn_frame.pack()

            ttk.Button(btn_frame, text="Start", command=self.start_stopwatch).grid(row=0, column=0, padx=10)
            ttk.Button(btn_frame, text="Stop", command=self.stop_stopwatch).grid(row=0, column=1, padx=10)
            ttk.Button(btn_frame, text="Reset", command=self.reset_stopwatch).grid(row=0, column=2, padx=10)
            
            def start_stopwatch(self):
                 if not self.running:
                    self.running = True
                    self.start_time = datetime.now() - self.elapsed
                    self.update_stopwatch()

            def stop_stopwatch(self):
                self.running = False

            def reset_stopwatch(self):
                self.running = False
                self.elapsed = timedelta()
                self.stopwatch_label.config(text="00:00:00")

            def update_stopwatch(self):
                if self.running:
                    self.elapsed = datetime.now() - self.start_time
                    self.stopwatch_label.config(text=str(self.elapsed).split('.')[0])
                    self.root.after(1000, self.update_stopwatch)

            def create_timer_tab(self):
                self.timer_tab = ttk.Frame(self.notebook)
                self.notebook.add(self.timer_tab, text="Timer")

                self.timer_entry = ttk.Entry(self.timer_tab)
                self.timer_entry.pack(pady=20)
                self.timer_entry.insert(0, "10")