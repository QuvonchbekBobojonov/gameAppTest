from tkinter import Tk, Label
import platform


class FullscreenMessageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Over")
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        self.label = Label(root, text="Time's up!", font=("Helvetica", 120))
        self.label.pack(pady=20)

        self.root.bind("<Escape>", lambda: print("Escape key pressed"))
        self.root.bind("<F11>", lambda: print("F11 key pressed"))
        if platform.system() == "Windows":
            self.root.bind("<Alt_L><F4>", lambda: print("Alt+F4 key pressed"))

    def exit_fullscreen(self, event):
        self.root.attributes('-fullscreen', False)
        self.root.destroy()


class TimerWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Club Timer")
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.geometry("300x80")

        # Timer settings
        self.time_left = 10  # Set initial timer value
        self.running = False

        self.label = Label(root, text="Set Timer (hh:mm:ss)", font=("Helvetica", 26, "bold"))
        self.label.pack(pady=20)

        self.start_timer()

    def start_timer(self):
        self.running = True
        self.countdown()

    def countdown(self):
        if self.time_left > 0 and self.running:
            mins, secs = divmod(self.time_left, 60)
            hours, mins = divmod(mins, 60)
            self.label.config(text=f"{hours:02}:{mins:02}:{secs:02}")
            self.time_left -= 1
            self.label.after(1000, self.countdown)
        else:
            self.running = False
            self.label.config(text="Time's up!")
            self.root.after(2000, self.root.destroy)
            fullscreen_app = Tk()
            FullscreenMessageApp(fullscreen_app)
            fullscreen_app.mainloop()


if __name__ == "__main__":
    root = Tk()
    TimerWidget(root)
    root.mainloop()
