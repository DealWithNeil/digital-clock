import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime, timedelta
import pytz

class ClockApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Modern Clock")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        self.main_container = tk.Frame(root, bg="black")
        self.main_container.pack(fill="both", expand=True)
        self.nav_frame = tk.Frame(root, bg="black")
        self.nav_frame.pack(fill="x", side="bottom")

        buttons = ["Clock", "World Time", "Stopwatch", "Timer", "Alarm"]
        self.nav_buttons = {}
        for b in buttons:
            btn = tk.Button(
                self.nav_frame,
                text=b,
                fg="white",
                bg="black",
                activebackground="white",
                activeforeground="black",
                bd=0,
                font=("Courier", 14, "bold"),
                command=lambda name=b: self.show_panel(name)
            )
            btn.pack(side="left", expand=True, fill="x", padx=2, pady=2)
        self.nav_buttons[b] = btn

        self.panels = {}

        for name in buttons:
                panel = tk.Frame(self.main_container, bg="black")
                panel.place(relwidth=1, relheight=1)  # full container
                self.panels[name] = panel

        self.clock_label = tk.Label(
            self.panels["Clock"],
            text="00:00:00",
            fg="white",
            bg="black",
            font=("Courier", 60, "bold"),  # dot-matrix feel
        )
        self.clock_label.pack(expand=True)

        self.show_panel("Clock")

        def show_panel(self, name):
           for panel_name, panel in self.panels.items():
                if panel_name == name:
                    panel.lift()  # bring to front
                else:
                    panel.lower()  # send to back

        self.create_clock_tab()
        self.create_world_time_tab()
        self.create_stopwatch_tab()
        self.create_timer_tab()
        self.create_alarm_tab()

    # ---------------- CLOCK ---------------- #
    def create_clock_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Clock")

        container = tk.Frame(tab, bg="black")
        container.pack(fill="both", expand=True)

        self.clock_label = tk.Label(
        container,
        text="00:00:00",
        fg="white",
        bg="black",
        font=("Courier", 60, "bold"),  # dot-matrix feel
        )

        self.clock_label.pack(expand=True)

        self.update_clock()

    def update_clock(self):
        now = datetime.now().strftime("%H %M %S") 
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)
        

    # ---------------- WORLD TIME ---------------- #
    def create_world_time_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="World Time")

        self.city_var = tk.StringVar(value="UTC")

        cities = ["UTC", "Asia/Manila", "US/Eastern", "Europe/London", "Asia/Tokyo"]

        ttk.Label(tab, text="Select Timezone").pack(pady=10)

        ttk.Combobox(tab, values=cities, textvariable=self.city_var).pack(pady=10)

        self.world_label = ttk.Label(tab, font=("Segoe UI", 35))
        self.world_label.pack(pady=40)

        ttk.Button(tab, text="Show Time", command=self.show_world_time).pack()

    def show_world_time(self):
        tz = pytz.timezone(self.city_var.get())
        time_now = datetime.now(tz).strftime("%H:%M:%S")
        self.world_label.config(text=time_now)

    # ---------------- STOPWATCH ---------------- #
    def create_stopwatch_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Stopwatch")

        self.running = False
        self.start_time = None
        self.elapsed = timedelta()

        self.stopwatch_label = ttk.Label(tab, text="00:00:00", font=("Segoe UI", 40))
        self.stopwatch_label.pack(pady=80)

        btn_frame = ttk.Frame(tab)
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

    # ---------------- TIMER ---------------- #
    def create_timer_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Timer")

        ttk.Label(tab, text="Seconds").pack(pady=10)

        self.timer_entry = ttk.Entry(tab)
        self.timer_entry.insert(0, "10")
        self.timer_entry.pack(pady=10)

        self.timer_label = ttk.Label(tab, text="00:00", font=("Segoe UI", 40))
        self.timer_label.pack(pady=40)

        self.timer_running = False

        ttk.Button(tab, text="Start Timer", command=self.start_timer).pack()

        timer_panel = self.panels["Timer"]

        self.timer_canvas = tk.Canvas(
            timer_panel,
            width=300,
            height=300,
            bg="black",
            highlightthickness=0
        )

        self.timer_canvas.pack(pady=40)

        self.timer_canvas.create_oval(20, 20, 280, 280, outline="#222", width=10)

        self.timer_arc = self.timer_canvas.create_arc(
            20, 20, 280, 280,
                start=90,
                extent=0,
                style="arc",
                outline="white",
                width=10
            )

        self.timer_text = self.timer_canvas.create_text(
            150, 150,
            text="00",
            fill="white",
            font=("Courier", 30, "bold")
        )

    def start_timer(self):
        try:
            self.timer_seconds = int(self.timer_entry.get())
            self.timer_running = True
            self.update_timer()
        except:
            self.timer_label.config(text="Invalid")

    def update_timer(self):
        if self.timer_running and self.timer_seconds >= 0:
            mins, secs = divmod(self.timer_seconds, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            self.timer_seconds -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_seconds < 0:
            self.timer_label.config(text="Done 🔔")

    # ---------------- ALARM ---------------- #
    def create_alarm_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Alarm")

        ttk.Label(tab, text="Set Alarm (HH:MM:SS)").pack(pady=10)

        self.alarm_entry = ttk.Entry(tab)
        self.alarm_entry.insert(0, "07:00:00")
        self.alarm_entry.pack(pady=10)

        self.alarm_set = False

        ttk.Button(tab, text="Set Alarm", command=self.set_alarm).pack()

    def set_alarm(self):
        self.alarm_time = self.alarm_entry.get()
        self.alarm_set = True
        self.check_alarm()

    def check_alarm(self):
        if self.alarm_set:
            now = datetime.now().strftime("%H:%M:%S")
            if now == self.alarm_time:
                self.alarm_set = False
                self.show_alarm()
            else:
                self.root.after(1000, self.check_alarm)

    def show_alarm(self):
        popup = tk.Toplevel(self.root)
        popup.title("Alarm")
        popup.geometry("250x150")

        ttk.Label(popup, text="⏰ Wake up!", font=("Segoe UI", 20)).pack(pady=30)
        ttk.Button(popup, text="OK", command=popup.destroy).pack()


# ---------------- RUN APP ---------------- #
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ClockApp(root)
    root.mainloop()