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