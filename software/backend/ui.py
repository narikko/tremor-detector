import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import time
import retrieve_data  # Assuming retrieve_data has xyz_queue and index_queue
import queue

# Colors
PRIMARY_COLOR = "#4CAF50"  # Green color for buttons and accents
SECONDARY_COLOR = "#f1f1f1"  # Light background color
TEXT_COLOR = "#333333"  # Dark text color
HEADER_COLOR = "#1E88E5"  # Blue header color

# Modern Font
FONT = ("Segoe UI", 12)

index = 0

serial_thread = threading.Thread(target=retrieve_data.start_serial_reading, daemon=True)
serial_thread.start()

def update_index(new_index):
    global index
    index = new_index
    print(index)

class TremorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tremor Analysis")
        self.geometry("800x600")
        self.frames = {}

        # Initialize frames
        for Page in (StartPage, GraphPage, ThankYouPage):
            frame = Page(self, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        # Start periodic queue checks
        self.check_xyz_queue()
        self.check_index_queue()

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

    def check_xyz_queue(self):
        # Check xyz_queue for new data and update graphs if needed
        try:
            data = retrieve_data.xyz_queue.get_nowait()
            if 'type' in data and data['type'] == 'xyz':
                self.frames[GraphPage].update_graph_data(data['x'], data['y'], data['z'])
        except queue.Empty:  # Correctly refer to queue.Empty
            pass
        self.after(5, self.check_xyz_queue)

    def check_index_queue(self):
        # Check index_queue for new data and update tremor level
        try:
            data = retrieve_data.index_queue.get_nowait()
            if 'type' in data and data['type'] == 'index':
                global index
                index = data['index']
                print(f"Received tremor level: {index}")
                self.frames[ThankYouPage].update_label(index)
        except queue.Empty:  # Correctly refer to queue.Empty
            pass
        self.after(100, self.check_index_queue)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)

        self.time_left = 10  # Set the initial countdown to 10 seconds

        # Title label
        title_label = tk.Label(self, text="Tremor Analysis", font=("Segoe UI", 24, "bold"), fg=HEADER_COLOR, bg=SECONDARY_COLOR)
        title_label.pack(pady=20)

        # Instructions
        instructions = [
            "1. Insert hand in glove.",
            "2. Don't move (voluntarily) for 10 seconds.",
            "3. Remove glove after timer ends."
        ]
        instruction_label = tk.Label(self, text="\n".join(instructions), font=FONT, fg=TEXT_COLOR, bg=SECONDARY_COLOR, justify="left")
        instruction_label.pack(pady=10)

        # Countdown label
        self.countdown_label = tk.Label(self, text=f"Your tests are running... {self.time_left} seconds left", font=FONT, fg=TEXT_COLOR, bg=SECONDARY_COLOR)
        self.countdown_label.pack(pady=20)

        # Start button
        self.start_button = ttk.Button(self, text="See Graphs", command=lambda: controller.show_frame(GraphPage), style="TButton")
        self.start_button.pack(pady=20)

        # Start the countdown timer
        self.update_countdown()

    def update_countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.countdown_label.config(text=f"Your tests are running... {self.time_left} seconds left")
            self.after(1000, self.update_countdown)
        else:
            self.controller.frames[GraphPage].show_and_schedule_thank_you()


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)

        # Create the figure and axes for the plots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
        self.fig.suptitle("Acceleration vs Time", fontsize=14)

        self.ax1.set_ylabel("X Acceleration")
        self.ax2.set_ylabel("Y Acceleration")
        self.ax3.set_ylabel("Z Acceleration")
        self.ax3.set_xlabel("Time (s)")

        self.ax1.grid(True)
        self.ax2.grid(True)
        self.ax3.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initialize data lists
        self.x_data, self.y_data, self.z_data = [], [], []
        self.time_data = []
        self.start_time = time.time()

        # Set up lines for plotting
        self.line_x, = self.ax1.plot([], [], label="X Acceleration", color="red")
        self.line_y, = self.ax2.plot([], [], label="Y Acceleration", color="green")
        self.line_z, = self.ax3.plot([], [], label="Z Acceleration", color="blue")

        # Set a fixed number of data points to store for smoother updates
        self.max_data_points = 100

    def update_graph_data(self, x, y, z):
        current_time = time.time() - self.start_time

        # Add new data points
        self.time_data.append(current_time)
        self.x_data.append(x)
        self.y_data.append(y)
        self.z_data.append(z)

        # Keep only the latest 'max_data_points' data points
        if len(self.time_data) > self.max_data_points:
            self.time_data.pop(0)
            self.x_data.pop(0)
            self.y_data.pop(0)
            self.z_data.pop(0)

        # Update the data of the lines
        self.line_x.set_data(self.time_data, self.x_data)
        self.line_y.set_data(self.time_data, self.y_data)
        self.line_z.set_data(self.time_data, self.z_data)

        # Adjust the axes dynamically
        self.ax1.set_xlim(min(self.time_data), max(self.time_data) if len(self.time_data) > 1 else 1)
        self.ax2.set_xlim(min(self.time_data), max(self.time_data) if len(self.time_data) > 1 else 1)
        self.ax3.set_xlim(min(self.time_data), max(self.time_data) if len(self.time_data) > 1 else 1)

        self.ax1.set_ylim(min(self.x_data) - 10, max(self.x_data) + 10)
        self.ax2.set_ylim(min(self.y_data) - 10, max(self.y_data) + 10)
        self.ax3.set_ylim(min(self.z_data) - 10, max(self.z_data) + 10)

        # Redraw the canvas with improved efficiency
        self.canvas.draw_idle()

    def show_and_schedule_thank_you(self):
        """Show the graph page and schedule transition to ThankYouPage."""
        self.controller.show_frame(GraphPage)
        self.after(1000, lambda: self.controller.show_frame(ThankYouPage))  # Transition after 10 seconds



class ThankYouPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label = tk.Label(self, text="Waiting for tremor level...", font=("Arial", 16))
        self.label.pack(pady=20)

    def update_label(self, tremor_level):
        self.label.config(text=f"Tremor level: {tremor_level}")


if __name__ == "__main__":
    app = TremorApp()
    app.mainloop()
