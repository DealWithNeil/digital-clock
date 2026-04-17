# Core GUI toolkit for frames, canvas drawing, popups, and basic widgets.
import tkinter as tk
# Themed tkinter widgets and the main themed application window.
import ttkbootstrap as ttk
# Time helpers for the clock, stopwatch, timer, and alarm.
from datetime import datetime, timedelta
# Timezone library used by the World Time panel.
import pytz

# Pixel-style digit map for the clock display.
# Each digit is a 5-row by 3-column bitmap where "1" means draw a dot.
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
        """Set up the main window, navigation bar, and all feature screens."""
        self.root = root
        self.root.title("Modern Clock")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        # Animation state used by the clock panel.
        self.glow_phase = 0

        # MAIN CONTAINER:
        # Holds all panels stacked in the same space.
        self.main_container = tk.Frame(root, bg="black")
        self.main_container.pack(fill="both", expand=True)

        # NAV BAR:
        # Bottom row of buttons used to switch between panels.
        self.nav_frame = tk.Frame(root, bg="black")
        self.nav_frame.pack(fill="x", side="bottom")

        # The section names used for both the panels and nav buttons.
        buttons = ["Clock", "World Time", "Stopwatch", "Timer", "Alarm"]
        # Dictionary that maps a panel name to its frame.
        self.panels = {}

        # CREATE PANELS:
        # Build one full-size frame per app section.
        for name in buttons:
            panel = tk.Frame(self.main_container, bg="black")
            panel.place(relwidth=1, relheight=1)
            self.panels[name] = panel

        # NAV BUTTONS:
        # Each button raises the matching panel to the front.
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

        # BUILD UI:
        # Populate each section, then show the default page.
        self.create_clock_ui()
        self.create_world_time_ui()
        self.create_stopwatch_ui()
        self.create_timer_ui()
        self.create_alarm_ui()
        self.show_panel("Clock")

    # ---------------- PANEL SWITCH ---------------- #
    def show_panel(self, name):
        """Bring the selected panel to the front and push the others behind it."""
        for panel_name, panel in self.panels.items():
            if panel_name == name:
                panel.lift()
            else:
                panel.lower()

    # ---------------- CLOCK ---------------- #
    def create_clock_ui(self):
        """Create the canvas used to render the custom digital clock."""
        panel = self.panels["Clock"]

        self.clock_canvas = tk.Canvas(
            panel,
            bg="black",
            highlightthickness=0
        )
        self.clock_canvas.pack(expand=True, fill="both")
        self.update_clock()

    def update_clock(self):
        """Draw the current time on the canvas and schedule the next refresh."""

        import math
        # Format time as HHMMSS so each character can be drawn from DIGITS.
        now = datetime.now().strftime("%H%M%S")

        # Clear the previous frame before redrawing.
        self.clock_canvas.delete("all")

        # Layout values that control the size and spacing of the dots.
        x_offset = 20
        y_offset = 50
        dot_size = 8
        spacing = 4

        # Advance the phase value for the subtle glow animation logic.
        self.glow_phase += 0.2

        # Blend between a dim cyan and a bright white-blue to create a pulse.
        pulse = (math.sin(self.glow_phase) + 1) / 2
        glow_value = int(120 + (135 * pulse))
        edge_value = int(30 + (110 * pulse))
        glow_color = f"#{edge_value:02x}{glow_value:02x}{glow_value:02x}"
        core_color = f"#{glow_value:02x}{glow_value:02x}ff"

        
        
        # Draw each digit from left to right.
        for digit in now:
            pattern = DIGITS[digit]

            # Walk the 5x3 bitmap for the current digit.
            for row in range(5):
                for col in range(3):
                    if pattern[row][col] == "1":
                        # Convert bitmap position into canvas coordinates.
                        x = x_offset + col * (dot_size + spacing)
                        y = y_offset + row * (dot_size + spacing)

                        # Layer dim circles behind the main dot to fake
                        # a soft neon glow using tkinter's solid-color canvas.
                        self.clock_canvas.create_oval(
                            x - 4, y - 4,
                            x + dot_size + 4, y + dot_size + 4,
                            fill=glow_color,
                            outline=""
                        )
                        self.clock_canvas.create_oval(
                            x - 2, y - 2,
                            x + dot_size + 2, y + dot_size + 2,
                            fill=core_color,
                            outline=""
                        )
                        self.clock_canvas.create_oval(
                            x, y,
                            x + dot_size,
                            y + dot_size,
                            fill="white",
                            outline=""
                        )

            x_offset += 3 * (dot_size + spacing) + 20  # space between digits

        # Refresh several times per second so the glow animation looks smooth.
        self.root.after(80, self.update_clock)
        

    # ---------------- WORLD TIME ---------------- #
    def create_world_time_ui(self):
        """Create the timezone selector and output label for world time."""
        panel = self.panels["World Time"]

        # Stores the timezone currently selected in the combobox.
        self.city_var = tk.StringVar(value="UTC")

        # Example timezone choices for the dropdown.
        cities = ["UTC", "Asia/Manila", "US/Eastern", "Europe/London", "Asia/Tokyo"]

        ttk.Label(panel, text="Timezone").pack(pady=10)
        ttk.Combobox(panel, values=cities, textvariable=self.city_var).pack(pady=10)

        self.world_label = ttk.Label(panel, font=("Segoe UI", 30))
        self.world_label.pack(pady=30)

        ttk.Button(panel, text="Show Time", command=self.show_world_time).pack()

    def show_world_time(self):
        """Look up the selected timezone and display its current time."""
        tz = pytz.timezone(self.city_var.get())
        time_now = datetime.now(tz).strftime("%H:%M:%S")
        self.world_label.config(text=time_now)

    # ---------------- STOPWATCH ---------------- #
    def create_stopwatch_ui(self):
        """Create the stopwatch display, buttons, and timing state."""
        panel = self.panels["Stopwatch"]

        # Stopwatch state:
        # running controls whether updates continue,
        # start_time stores the actual start moment,
        # elapsed stores the accumulated duration.
        self.running = False
        self.start_time = None
        self.elapsed = timedelta()

        self.stopwatch_label = ttk.Label(panel, text="00:00:00", font=("Segoe UI", 35))
        self.stopwatch_label.pack(pady=40)

        # Button row for start, stop, and reset.
        frame = ttk.Frame(panel)
        frame.pack()

        ttk.Button(frame, text="Start", command=self.start_stopwatch).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Stop", command=self.stop_stopwatch).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Reset", command=self.reset_stopwatch).grid(row=0, column=2, padx=5)

    def start_stopwatch(self):
        """Start or resume the stopwatch from the previously elapsed time."""
        if not self.running:
            self.running = True
            self.start_time = datetime.now() - self.elapsed
            self.update_stopwatch()

    def stop_stopwatch(self):
        """Pause the stopwatch without clearing its elapsed time."""
        self.running = False

    def reset_stopwatch(self):
        """Stop the stopwatch and reset the display back to zero."""
        self.running = False
        self.elapsed = timedelta()
        self.stopwatch_label.config(text="00:00:00")

    def update_stopwatch(self):
        """Refresh the stopwatch label every second while the stopwatch is running."""
        if self.running:
            self.elapsed = datetime.now() - self.start_time
            self.stopwatch_label.config(text=str(self.elapsed).split('.')[0])
            self.root.after(1000, self.update_stopwatch)

    # ---------------- TIMER ---------------- #
    def create_timer_ui(self):
        """Create a circular countdown timer with seconds input."""
        panel = self.panels["Timer"]

        # Canvas used for the ring, progress arc, and remaining-seconds text.
        self.timer_canvas = tk.Canvas(panel, width=250, height=250, bg="black", highlightthickness=0)
        self.timer_canvas.pack(pady=30)

        # Static outer ring.
        self.timer_canvas.create_oval(20, 20, 230, 230, outline="#222", width=8)

        # Progress arc that shrinks as the countdown runs.
        self.timer_arc = self.timer_canvas.create_arc(
            20, 20, 230, 230,
            start=90, extent=0,
            style="arc", outline="white", width=8
        )

        # Center text showing the current remaining time.
        self.timer_text = self.timer_canvas.create_text(
            125, 125, text="0", fill="white", font=("Courier", 25, "bold")
        )

        # Input where the user enters countdown seconds.
        self.timer_entry = tk.Entry(panel, justify="center")
        self.timer_entry.insert(0, "10")
        self.timer_entry.pack()

        tk.Button(panel, text="Start", command=self.start_timer, bg="black", fg="white").pack(pady=10)

    def start_timer(self):
        """Read the timer input, validate it, and begin the countdown."""
        try:
            self.total_time = int(self.timer_entry.get())
            if self.total_time <= 0:
                raise ValueError("Timer value must be positive")
            self.remaining_time = self.total_time
            self.update_timer()
        except (TypeError, ValueError):
            self.timer_canvas.itemconfig(self.timer_text, text="ERR")

    def update_timer(self):
        """Update the timer text and arc once per second until it finishes."""
        if self.remaining_time >= 0:
            self.timer_canvas.itemconfig(self.timer_text, text=str(self.remaining_time))

            # Convert remaining time into an arc angle for the circular progress.
            progress = (self.remaining_time / self.total_time) * 360
            self.timer_canvas.itemconfig(self.timer_arc, extent=-progress)

            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_canvas.itemconfig(self.timer_text, text="DONE")

    # ---------------- ALARM ---------------- #
    def create_alarm_ui(self):
        """Create the alarm entry field and the button that arms the alarm."""
        panel = self.panels["Alarm"]

        ttk.Label(panel, text="Set Alarm (HH:MM:SS)").pack(pady=10)

        self.alarm_entry = ttk.Entry(panel)
        self.alarm_entry.insert(0, "07:00:00")
        self.alarm_entry.pack()

        ttk.Button(panel, text="Set Alarm", command=self.set_alarm).pack(pady=10)

        # Tracks whether an alarm is currently armed.
        self.alarm_set = False

    def set_alarm(self):
        """Save the target alarm time and start checking once per second."""
        self.alarm_time = self.alarm_entry.get()
        self.alarm_set = True
        self.check_alarm()

    def check_alarm(self):
        """Compare the current time against the alarm time until they match."""
        if self.alarm_set:
            now = datetime.now().strftime("%H:%M:%S")
            if now == self.alarm_time:
                self.alarm_set = False
                self.show_alarm()
            else:
                self.root.after(1000, self.check_alarm)

    def show_alarm(self):
        """Open a popup window to notify the user that the alarm has fired."""
        popup = tk.Toplevel(self.root)
        popup.title("Alarm")
        popup.geometry("250x150")

        ttk.Label(popup, text="⏰ Wake up!", font=("Segoe UI", 20)).pack(pady=30)
        ttk.Button(popup, text="OK", command=popup.destroy).pack()
# RUN:
# Create the themed window, build the app, and start tkinter's event loop.
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ClockApp(root)
    root.mainloop()
