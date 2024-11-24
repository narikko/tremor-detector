import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import time
import queue
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import retrieve_data
from backend import features
from backend import filter_anomalies

# Colors
PRIMARY_COLOR = "#4CAF50"  # Green color for buttons and accents
SECONDARY_COLOR = "#ffffff"  # Light background color
TEXT_COLOR = "#121212"  # Dark text color
HEADER_COLOR = "#5cac94"  # Blue header color

# Modern Font
FONT = ("Segoe UI", 12)

index = 0
index_reached = False

serial_thread = threading.Thread(target=retrieve_data.start_serial_reading, daemon=True)
serial_thread.start()

def update_index(new_index):
    global index
    index = new_index
    print(index)

def fade_in_to_color(widget, start_color, end_color, steps, delay):
    def hex_to_rgb(hex_color):
        """Convert hex color to an RGB tuple."""
        return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    def rgb_to_hex(rgb_color):
        """Convert RGB tuple to a hex color."""
        return f"#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}"

    # Convert start and end colors to RGB
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    # Calculate the difference per step for each color channel
    step_diff = [(end_rgb[i] - start_rgb[i]) / steps for i in range(3)]

    def update_color(step=0):
        if step <= steps:
            # Calculate the intermediate RGB value
            current_rgb = [
                int(start_rgb[i] + step * step_diff[i]) for i in range(3)
            ]
            # Update widget text color
            widget.config(fg=rgb_to_hex(current_rgb))
            # Schedule next step
            widget.after(delay, lambda: update_color(step + 1))

    # Start the fade-in process
    update_color()

class TremorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tremor Analysis")
        self.geometry("800x600")
        self.frames = {}

        # Initialize frames
        for Page in (StartPage, InstructionsPage, GraphPage, ThankYouPage):
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
            global index_reached
            if 'type' in data and data['type'] == 'index' and not(index_reached):
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

        #self.time_left = 10  # Set the initial countdown to 10 seconds

        # Title label
        title_label = tk.Label(self, text="Tremor.", font=("Segoe UI", 96, "bold"), fg=HEADER_COLOR, bg=SECONDARY_COLOR)
        title_label.place(x=30, y=100)

        fade_in_to_color(title_label, SECONDARY_COLOR, HEADER_COLOR, 35, 20)

        description = """
        Tremor provides an objective way to assess 
        tremor ratings by analyzing motion data. Designed 
        to assist doctors in monitoring symptoms, it offers 
        valuable insights into tremor-related conditions.

        Developed as a prototype by four engineering students, 
        Tremor is still in development, with the potential to 
        evolve into a powerful tool for managing tremors.
        """

        description_label = tk.Label(
        self, 
        text=description, 
        font=("Segoe UI", 14),  
        fg=TEXT_COLOR,         
        bg=SECONDARY_COLOR,
        justify="left"
        )
        description_label.place(x=20, y=250)
        fade_in_to_color(description_label, SECONDARY_COLOR, TEXT_COLOR, 35, 20)

        # Countdown label
        #self.countdown_label = tk.Label(self, text=f"Your tests are running... {self.time_left} seconds left", font=FONT, fg=TEXT_COLOR, bg=SECONDARY_COLOR)
        #self.countdown_label.pack(pady=20)

        # Start button
        style = ttk.Style()
        style.configure("Custom.TButton",
                font=("Segoe UI", 24, "bold"),
                foreground=HEADER_COLOR,
                padding=(20, 10),
                borderwidth=1)

        style.map("Custom.TButton",  # Define hover effect
          foreground=[("active", TEXT_COLOR)],
          background=[("active", HEADER_COLOR)])  # Darker blue on hover

        # Apply the custom style
        btn = ttk.Button(self, text="Start a Test", style="Custom.TButton", command=lambda: controller.show_frame(InstructionsPage))
        btn.place(x=525, y=300)

        # Start the countdown timer
        #self.update_countdown()
    """
    def update_countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.countdown_label.config(text=f"Your tests are running... {self.time_left} seconds left")
            self.after(1000, self.update_countdown)
        else:
            self.controller.frames[GraphPage].show_and_schedule_thank_you()
            """
class InstructionsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)

        instructions = """
            1. Insert hand in glove.
            2. Don't move (voluntarily) for 10 seconds.
            3. You may remove your hand from glove after 
               results are ready.

            Click ready to start.
            """
        instructions_label = tk.Label(
            self, 
            text=instructions, 
            font=("Segoe UI", 24),  
            fg=TEXT_COLOR,         
            bg=SECONDARY_COLOR,
            justify="left"
        )
        instructions_label.place(x=0,y=100)
        fade_in_to_color(instructions_label, SECONDARY_COLOR, TEXT_COLOR, 100, 20)

        style = ttk.Style()
        
        # Define the custom style for the button
        style.configure("TButton",
                        font=("Segoe UI", 24, "bold"),
                        foreground="#5CAC94",
                        background="white")
        
        # Create the button using the style
        btn = ttk.Button(self,
                         text="Ready",
                         style="TButton",  # Apply the custom style
                         command=self.start_test)  # Call the start_test method
        btn.place(x=100, y=500)

    def start_test(self):
        """Called when the 'Ready' button is pressed."""
        self.controller.frames[GraphPage].start_countdown()  # Call method in GraphPage to start countdown
        self.controller.show_frame(GraphPage)  # Transition to GraphPage



class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)

        # Create the figure and axes for the plots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
        self.fig.suptitle("Live Hand Acceleration Data", fontsize=14, color=TEXT_COLOR)

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

        # Start the countdown timer
        self.countdown_seconds = 10

    def start_countdown(self):
        """Start the countdown timer when called."""
        self.update_countdown()

    def update_countdown(self):
        """Update the countdown timer every second."""
        if self.countdown_seconds > 0:
            self.countdown_seconds -= 1
            # Schedule the next update in 1 second
            self.after(1000, self.update_countdown)
        else:
            # After the countdown, transition to ThankYouPage
            global index_reached
            index_reached = True
            self.controller.show_frame(ThankYouPage)

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

class ThankYouPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)

        self.label = tk.Label(self, text="Waiting for tremor level...", font=("Segoe UI", 96, "bold"), fg=HEADER_COLOR, bg="white")
        self.label.place(x=100, y=50)

        self.rating_label = tk.Label(self, text="rating", font=("Segoe UI", 56, "bold"), fg="#ccecee", bg="white")
        self.rating_label.place(x=250, y=50)
        

    def update_label(self, tremor_level):
        self.label.config(text=f"{tremor_level}")

        if tremor_level == 0:
                self.rating_label.config(text="Normal\nCondition")
        elif tremor_level == 1:
                self.rating_label.config(text="Slight Tremor\nIntensity")
        elif tremor_level == 2:
                self.rating_label.config(text="Mild Tremor\nIntensity")
        elif tremor_level == 3:
                self.rating_label.config(text="Moderate Tremor\nIntensity")
        else:
                self.rating_label.config(text="Severe Tremor\nIntesity")
        
        


if __name__ == "__main__":
    app = TremorApp()
    app.mainloop()
