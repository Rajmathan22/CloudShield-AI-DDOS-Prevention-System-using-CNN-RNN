
import tkinter as tk
from tkinter import messagebox
import threading
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from network_monitor import handle_client, lock, packet_history, size_history, ip_repetition_history, packet_size_deviation, ip_repetition_frequency

class FullScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Full Screen Layout with Navigation")
        self.root.geometry("800x600")
        self.setup_sidebar()
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self.show_view_page()
        self.running = False  # Flag to stop monitoring thread

        # Initialize Matplotlib figure and axes
        self.fig, self.axs = plt.subplots(3, 1, figsize=(10, 8))
        self.fig.tight_layout()

    def setup_sidebar(self):
        sidebar = tk.Frame(self.root, width=200, bg='#333', height=600, relief='sunken', borderwidth=2)
        sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

        # Sidebar buttons
        btn_view = tk.Button(sidebar, text="View", command=self.show_view_page, bg="#575757", fg="white")
        btn_view.pack(fill=tk.X)

        btn_monitor = tk.Button(sidebar, text="Monitor", command=self.show_monitor_page, bg="#575757", fg="white")
        btn_monitor.pack(fill=tk.X)

        btn_report = tk.Button(sidebar, text="Report", command=self.show_report_page, bg="#575757", fg="white")
        btn_report.pack(fill=tk.X)

        btn_actions = tk.Button(sidebar, text="Actions", command=self.show_actions_page, bg="#575757", fg="white")
        btn_actions.pack(fill=tk.X)

    def show_view_page(self):
        self.clear_frame()
        label = tk.Label(self.content_frame, text="View Page", font=("Arial", 24))
        label.pack(pady=20)

    def show_monitor_page(self):
        self.clear_frame()

        label = tk.Label(self.content_frame, text="Monitor Page", font=("Arial", 24))
        label.pack(pady=20)

        # Embed the Matplotlib figure into the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.content_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Start network monitoring
        start_monitor_button = tk.Button(self.content_frame, text="Start Monitoring", command=self.start_monitoring)
        start_monitor_button.pack(pady=10)

        # # Add buttons for normal traffic and DDoS initialization
        # start_normal_button = tk.Button(self.content_frame, text="Start Normal Traffic", command=self.start_normal_traffic)
        # start_normal_button.pack(pady=5)

        # start_ddos_button = tk.Button(self.content_frame, text="DDoS Init", command=self.start_ddos)
        # start_ddos_button.pack(pady=5)

        # stop_traffic_button = tk.Button(self.content_frame, text="Stop Traffic", command=self.stop_normal_traffic)
        # stop_traffic_button.pack(pady=5)

    def show_report_page(self):
        self.clear_frame()
        label = tk.Label(self.content_frame, text="Report Page", font=("Arial", 24))
        label.pack(pady=20)

    

    def show_actions_page(self):
        self.clear_frame()
        label = tk.Label(self.content_frame, text="Actions Page", font=("Arial", 24))
        label.pack(pady=20)

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def start_monitoring(self):
        if not self.running:
            self.running = True
            messagebox.showinfo("Monitor", "Starting the monitoring process...")
            self.monitor_thread = threading.Thread(target=self.run_socket_monitor, daemon=True)
            self.monitor_thread.start()
            self.update_plot()  # Start updating plot on the main thread

    def stop_monitoring(self):
        self.running = False

    def update_plot(self):
        if self.running:
            with lock:
                # Clear previous data for new plots
                self.axs[0].clear()
                self.axs[1].clear()
                self.axs[2].clear()
                
                # Update for Packet Rate Monitoring
                self.axs[0].plot(packet_history, label='Packets per second', color='blue')
                self.axs[0].set_title("Real-time Packet Rate Monitoring")
                self.axs[0].set_xlabel("Time (seconds)")
                self.axs[0].set_ylabel("Packets per second")
                max_packet_rate = max(max(packet_history), 50)  # Set a minimum limit
                self.axs[0].set_ylim(0, max_packet_rate + 10)  # Dynamically adjust y-axis

                # Update for Packet Size Deviation Monitoring
                self.axs[1].plot(size_history, label='Packet Size Deviation', color='green')
                self.axs[1].set_title("Packet Size Deviation Monitoring")
                self.axs[1].set_xlabel("Time (seconds)")
                self.axs[1].set_ylabel("Packet Size Deviation")
                max_packet_size_deviation = max(max(size_history), 50)  # Set a minimum limit
                self.axs[1].set_ylim(0, max_packet_size_deviation + 10)  # Dynamically adjust y-axis

                # Update for IP Repetition Monitoring
                self.axs[2].plot(ip_repetition_history, label='IP Repetition', color='orange')
                self.axs[2].set_title("IP Repetition Monitoring")
                self.axs[2].set_xlabel("Time (seconds)")
                self.axs[2].set_ylabel("Repetitions")
                max_ip_repetition = max(max(ip_repetition_history), 50)  # Set a minimum limit
                self.axs[2].set_ylim(0, max_ip_repetition + 10)  # Dynamically adjust y-axis

                # Update x-axis limits
                self.axs[0].set_xlim(0, len(packet_history) - 1)
                self.axs[1].set_xlim(0, len(size_history) - 1)
                self.axs[2].set_xlim(0, len(ip_repetition_history) - 1)

                # Redraw the canvas
                self.canvas.draw()
                
            # Call this method again after 1 second
            self.root.after(1000, self.update_plot)

    def run_socket_monitor(self):
        handle_client()

    def start_ddos(self):
        messagebox.showinfo("DDoS", "Starting DDoS attack...")
        # Here you can trigger the DDoS functionality from the other file

    def start_normal_traffic(self):
        messagebox.showinfo("Normal Traffic", "Starting normal traffic...")
        # Here you can trigger the normal traffic functionality from the other file

    def stop_normal_traffic(self):
        messagebox.showinfo("Normal Traffic", "Stopping normal traffic...")
        # Here you can trigger the stop normal traffic functionality from the other file

if __name__ == "__main__":
    root = tk.Tk()
    app = FullScreenApp(root)
    root.mainloop()
