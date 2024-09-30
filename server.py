import tkinter as tk
import subprocess


class FullscreenTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Club Timer")
        self.root.attributes('-fullscreen', True)  # Set the app to fullscreen

        self.time_left = 0
        self.running = False

        self.label = tk.Label(root, text="Set Timer (hh:mm:ss)", font=("Helvetica", 36))
        self.label.pack(pady=20)

        self.entry_hours = tk.Entry(root, width=5, font=("Helvetica", 36))
        self.entry_hours.pack(side=tk.LEFT, padx=(20, 10))
        self.entry_hours.insert(0, "0")

        self.entry_minutes = tk.Entry(root, width=5, font=("Helvetica", 36))
        self.entry_minutes.pack(side=tk.LEFT, padx=(10, 10))
        self.entry_minutes.insert(0, "0")

        self.entry_seconds = tk.Entry(root, width=5, font=("Helvetica", 36))
        self.entry_seconds.pack(side=tk.LEFT, padx=(10, 20))
        self.entry_seconds.insert(0, "0")

        self.start_button = tk.Button(root, text="Start", command=self.start_timer, font=("Helvetica", 24))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop and Lock", command=self.stop_timer, font=("Helvetica", 24))
        self.stop_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, font=("Helvetica", 24))
        self.reset_button.pack(pady=10)

        self.time_display = tk.Label(root, text="00:00:00", font=("Helvetica", 120))
        self.time_display.pack(pady=20)

        self.update_display()

        # Bind ESC key to exit fullscreen
        self.root.bind("<Escape>", self.exit_fullscreen)

    def start_timer(self):
        if not self.running:
            hours = int(self.entry_hours.get())
            minutes = int(self.entry_minutes.get())
            seconds = int(self.entry_seconds.get())
            self.time_left = hours * 3600 + minutes * 60 + seconds
            self.running = True
            self.countdown()

    def countdown(self):
        if self.time_left > 0 and self.running:
            mins, secs = divmod(self.time_left, 60)
            hours, mins = divmod(mins, 60)
            self.time_display.config(text=f"{hours:02}:{mins:02}:{secs:02}")
            self.time_left -= 1
            self.root.after(1000, self.countdown)
        else:
            self.running = False

    def stop_timer(self):
        self.running = False
        # Lock the workstation
        subprocess.run("rundll32.exe user32.dll,LockWorkStation")

    def reset_timer(self):
        self.running = False
        self.time_left = 0
        self.time_display.config(text="00:00:00")

    def update_display(self):
        if self.running:
            self.time_display.after(1000, self.update_display)

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)


if __name__ == "__main__":
    root = tk.Tk()
    app = FullscreenTimerApp(root)
    root.mainloop()
