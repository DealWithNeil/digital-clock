import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime, timedelta
import pytz

DIGITS = {
    "0": ["111","101","101","101","111"],
    "1": ["010","110","010","010","111"],
    "2": ["111","001","111","100","111"],
    "3": ["111","001","111","001","111"],
    "4": ["101","101","111","001","001"],
    "5": ["111","100","111","001","111"],
    "6": ["111","100","111","101","111"],
    "7": ["111","001","001","001","001"],
    "8": ["111","101","111","101","111"],
    "9": ["111","101","111","001","111"],
}


class ClockApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Modern Clock")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # MAIN CONTAINER
        self.main_container = tk.Frame(root, bg="black")
        self.main_container.pack(fill="both", expand=True)

        # NAV BAR
        self.nav_frame = tk.Frame(root, bg="black")
        self.nav_frame.pack(fill="x", side="bottom")

        buttons = ["Clock", "World Time", "Stopwatch", "Timer", "Alarm"]
        self.panels = {}

        # CREATE PANELS
        for name in buttons:
            panel = tk.Frame(self.main_container, bg="black")
            panel.place(relwidth=1, relheight=1)
            self.panels[name] = panel

        # NAV BUTTONS
        for b in buttons:
            btn = tk.Button(
                self.nav_frame,
                text=b,
                fg="white",
                bg="black",
                activebackground="white",
                activeforeground="black",
                bd=0,
                font=("Courier", 12, "bold"),
                command=lambda name=b: self.show_panel(name)
            )
            btn.pack(side="left", expand=True, fill="x")

        # BUILD UI
        self.create_clock_ui()
        self.create_world_time_ui()
        self.create_stopwatch_ui()
        self.create_timer_ui()
        self.create_alarm_ui()

        self.show_panel("Clock")

    # ---------------- PANEL SWITCH ---------------- #
    def show_panel(self, name):
        for panel_name, panel in self.panels.items():
            if panel_name == name:
                panel.lift()
            else:
                panel.lower()

    # ---------------- CLOCK ---------------- #
    
        panel = self.panels["Clock"]

        self.clock_label = tk.Label(
            panel,
            text="00 ● 00 ● 00",
            fg="white",
            bg="black",
            font=("Courier", 50, "bold"),
        )
        self.clock_label.pack(expand=True)

        self.update_clock()

    def update_clock(self):
        now = datetime.now()

        sep = " ● " if now.second % 2 == 0 else "   "
        time_str = now.strftime(f"%H{sep}%M{sep}%S")

        self.clock_label.config(text=time_str)
        self.root.after(1000, self.update_clock)

    # ---------------- WORLD TIME ---------------- #
    def create_world_time_ui(self):
        panel = self.panels["World Time"]

        self.city_var = tk.StringVar(value="UTC")

        cities = ["UTC", "Asia/Manila", "US/Eastern", "Europe/London", "Asia/Tokyo"]

        ttk.Label(panel, text="Timezone").pack(pady=10)
        ttk.Combobox(panel, values=cities, textvariable=self.city_var).pack(pady=10)

        self.world_label = ttk.Label(panel, font=("Segoe UI", 30))
        self.world_label.pack(pady=30)

        ttk.Button(panel, text="Show Time", command=self.show_world_time).pack()

    def show_world_time(self):
        tz = pytz.timezone(self.city_var.get())
        time_now = datetime.now(tz).strftime("%H:%M:%S")
        self.world_label.config(text=time_now)

    # ---------------- STOPWATCH ---------------- #
    def create_stopwatch_ui(self):
        panel = self.panels["Stopwatch"]

        self.running = False
        self.start_time = None
        self.elapsed = timedelta()

        self.stopwatch_label = ttk.Label(panel, text="00:00:00", font=("Segoe UI", 35))
        self.stopwatch_label.pack(pady=40)

        frame = ttk.Frame(panel)
        frame.pack()

        ttk.Button(frame, text="Start", command=self.start_stopwatch).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Stop", command=self.stop_stopwatch).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Reset", command=self.reset_stopwatch).grid(row=0, column=2, padx=5)

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
    def create_timer_ui(self):
        panel = self.panels["Timer"]

        self.timer_canvas = tk.Canvas(panel, width=250, height=250, bg="black", highlightthickness=0)
        self.timer_canvas.pack(pady=30)

        self.timer_canvas.create_oval(20, 20, 230, 230, outline="#222", width=8)

        self.timer_arc = self.timer_canvas.create_arc(
            20, 20, 230, 230,
            start=90, extent=0,
            style="arc", outline="white", width=8
        )

        self.timer_text = self.timer_canvas.create_text(
            125, 125, text="0", fill="white", font=("Courier", 25, "bold")
        )

        self.timer_entry = tk.Entry(panel, justify="center")
        self.timer_entry.insert(0, "10")
        self.timer_entry.pack()

        tk.Button(panel, text="Start", command=self.start_timer, bg="black", fg="white").pack(pady=10)

    def start_timer(self):
        try:
            self.total_time = int(self.timer_entry.get())
            self.remaining_time = self.total_time
            self.update_timer()
        except:
            self.timer_canvas.itemconfig(self.timer_text, text="ERR")

    def update_timer(self):
        if self.remaining_time >= 0:
            self.timer_canvas.itemconfig(self.timer_text, text=str(self.remaining_time))

            progress = (self.remaining_time / self.total_time) * 360
            self.timer_canvas.itemconfig(self.timer_arc, extent=-progress)

            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_canvas.itemconfig(self.timer_text, text="DONE")

    # ---------------- ALARM ---------------- #
    def create_alarm_ui(self):
        panel = self.panels["Alarm"]

        ttk.Label(panel, text="Set Alarm (HH:MM:SS)").pack(pady=10)

        self.alarm_entry = ttk.Entry(panel)
        self.alarm_entry.insert(0, "07:00:00")
        self.alarm_entry.pack()

        ttk.Button(panel, text="Set Alarm", command=self.set_alarm).pack(pady=10)

        self.alarm_set = False

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


# RUN
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ClockApp(root)
    root.mainloop()