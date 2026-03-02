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