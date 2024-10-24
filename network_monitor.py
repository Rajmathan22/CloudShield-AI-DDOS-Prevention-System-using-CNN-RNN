# # import socket
# # import threading
# # import time
# # from collections import deque, defaultdict
# # import tkinter as tk
# # from tkinter import messagebox

# # # Configuration
# # BUFFER_SIZE = 33000
# # IP_ADDRESS = '192.168.1.6'
# # PORT = 12345

# # # Thresholds
# # PACKET_SIZE_THRESHOLD = 5000  # Set your packet size deviation threshold
# # MAX_IP_REPETITION_THRESHOLD = 10  # Set your max IP repetition threshold
# # SPIKE_THRESHOLD = 8000  # Spike threshold to detect major deviations
# # ALERT_DURATION = 5  # Duration in seconds to monitor thresholds

# # # Packet data tracking history
# # history_length = 20  # Increased length to better show dynamic changes
# # packet_history = deque([0] * history_length, maxlen=history_length)
# # size_history = deque([0] * history_length, maxlen=history_length)
# # ip_repetition_history = deque([0] * history_length, maxlen=history_length)

# # # Metrics
# # lock = threading.Lock()
# # packet_size_deviation = 0
# # ip_repetition_frequency = defaultdict(float)

# # # Malicious activity tracking
# # malicious_activity_detected = False
# # malicious_activity_start_time = 0

# # # Function to display malicious activity alert in a dialog box
# # def show_alert():
# #     root = tk.Tk()
# #     root.withdraw()  # Hide the root window
# #     messagebox.showwarning("Malicious Traffic Detected", "A major deviation pattern was detected, indicating potential malicious traffic!")
# #     root.destroy()

# # # Function to handle incoming packets
# # def handle_client():
# #     global packet_size_deviation, malicious_activity_detected, malicious_activity_start_time
# #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #     sock.bind((IP_ADDRESS, PORT))
# #     print(f"Receiver started at {IP_ADDRESS}:{PORT}")

# #     packet_count = 0
# #     start_time = time.time()
# #     last_packet_size = 0
# #     ip_counts_per_second = defaultdict(int)

# #     while True:
# #         data, addr = sock.recvfrom(BUFFER_SIZE)
# #         packet_count += 1
# #         packet_size = len(data)
# #         ip_counts_per_second[addr[0]] += 1

# #         # Calculate packet size deviation
# #         packet_size_deviation = abs(packet_size - last_packet_size)
# #         last_packet_size = packet_size

# #         # Update packet count and reset every second
# #         if time.time() - start_time >= 1:
# #             with lock:
# #                 # Update packets per second
# #                 packet_history.append(packet_count)

# #                 # Update packet size deviation history
# #                 size_history.append(packet_size_deviation)

# #                 # Update IP repetition frequency history
# #                 ip_repetition_frequency.clear()
# #                 for ip, count in ip_counts_per_second.items():
# #                     ip_repetition_frequency[ip] = count / 1.0  # Repetitions per second

# #                 # Append the maximum IP repetition frequency of the second
# #                 if ip_repetition_frequency:
# #                     max_ip_repetition = max(ip_repetition_frequency.values())
# #                     ip_repetition_history.append(max_ip_repetition)
# #                 else:
# #                     ip_repetition_history.append(0)

# #                 # Check for threshold breaches or spike patterns
# #                 if packet_size_deviation > PACKET_SIZE_THRESHOLD or max_ip_repetition > MAX_IP_REPETITION_THRESHOLD:
# #                     if not malicious_activity_detected:
# #                         malicious_activity_detected = True
# #                         malicious_activity_start_time = time.time()
# #                         print("Malicious activity detected: Threshold exceeded!")

# #                 # Check for specific spike pattern (high-low-high)
# #                 if size_history[-1] > SPIKE_THRESHOLD and size_history[-2] < SPIKE_THRESHOLD and size_history[-3] > SPIKE_THRESHOLD:
# #                     print("Spike pattern detected, triggering malicious alert!")
# #                     threading.Thread(target=show_alert).start()  # Show alert in a separate thread

# #                 # Check for alert duration
# #                 if malicious_activity_detected:
# #                     if time.time() - malicious_activity_start_time >= ALERT_DURATION:
# #                         # Reset malicious activity state
# #                         print("Alert duration exceeded, reset malicious activity state.")
# #                         malicious_activity_detected = False
# #                         malicious_activity_start_time = 0

# #                 # Reset for the next second
# #                 packet_count = 0
# #                 ip_counts_per_second.clear()
# #                 start_time = time.time()

# # # Start the server to receive packets
# # def start_monitoring():
# #     threading.Thread(target=handle_client, daemon=True).start()

# # # Run the monitoring system
# # if __name__ == "__main__":
# #     start_monitoring()





# import socket
# import threading
# import time
# from collections import deque, defaultdict
# import tkinter as tk
# from tkinter import messagebox

# # Configuration
# BUFFER_SIZE = 33000
# IP_ADDRESS = '192.168.1.6'
# PORT = 12345

# # Thresholds
# PACKET_SIZE_THRESHOLD = 5000  # Set your packet size deviation threshold
# MAX_IP_REPETITION_THRESHOLD = 10  # Set your max IP repetition threshold
# SPIKE_THRESHOLD = 8000  # Spike threshold to detect major deviations
# ALERT_DURATION = 5  # Duration in seconds to monitor thresholds
# ALERT_INTERVAL = 3  # Interval in seconds to show alerts

# # Packet data tracking history
# history_length = 20  # Increased length to better show dynamic changes
# packet_history = deque([0] * history_length, maxlen=history_length)
# size_history = deque([0] * history_length, maxlen=history_length)
# ip_repetition_history = deque([0] * history_length, maxlen=history_length)

# # Metrics
# lock = threading.Lock()
# packet_size_deviation = 0
# ip_repetition_frequency = defaultdict(float)

# # Malicious activity tracking
# malicious_activity_detected = False
# malicious_activity_start_time = 0
# last_alert_time = 0  # Time when the last alert was shown

# # Function to display malicious activity alert in a dialog box
# def show_alert():
#     root = tk.Tk()
#     root.withdraw()  # Hide the root window
#     messagebox.showwarning("Malicious Traffic Detected", "A major deviation pattern was detected, indicating potential malicious traffic!")
#     root.destroy()

# # Function to handle incoming packets
# def handle_client():
#     global packet_size_deviation, malicious_activity_detected, malicious_activity_start_time, last_alert_time
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind((IP_ADDRESS, PORT))
#     print(f"Receiver started at {IP_ADDRESS}:{PORT}")

#     packet_count = 0
#     start_time = time.time()
#     last_packet_size = 0
#     ip_counts_per_second = defaultdict(int)

#     while True:
#         data, addr = sock.recvfrom(BUFFER_SIZE)
#         packet_count += 1
#         packet_size = len(data)
#         ip_counts_per_second[addr[0]] += 1

#         # Calculate packet size deviation
#         packet_size_deviation = abs(packet_size - last_packet_size)
#         last_packet_size = packet_size

#         # Update packet count and reset every second
#         if time.time() - start_time >= 1:
#             with lock:
#                 # Update packets per second
#                 packet_history.append(packet_count)

#                 # Update packet size deviation history
#                 size_history.append(packet_size_deviation)

#                 # Update IP repetition frequency history
#                 ip_repetition_frequency.clear()
#                 for ip, count in ip_counts_per_second.items():
#                     ip_repetition_frequency[ip] = count / 1.0  # Repetitions per second

#                 # Append the maximum IP repetition frequency of the second
#                 if ip_repetition_frequency:
#                     max_ip_repetition = max(ip_repetition_frequency.values())
#                     ip_repetition_history.append(max_ip_repetition)
#                 else:
#                     ip_repetition_history.append(0)

#                 # Check for threshold breaches or spike patterns
#                 if packet_size_deviation > PACKET_SIZE_THRESHOLD or max_ip_repetition > MAX_IP_REPETITION_THRESHOLD:
#                     if not malicious_activity_detected:
#                         malicious_activity_detected = True
#                         malicious_activity_start_time = time.time()
#                         print("Malicious activity detected: Threshold exceeded!")

#                 # Check for specific spike pattern (high-low-high)
#                 if size_history[-1] > SPIKE_THRESHOLD and size_history[-2] < SPIKE_THRESHOLD and size_history[-3] > SPIKE_THRESHOLD:
#                     current_time = time.time()
#                     # Show alert every 3 seconds if malicious activity is detected
#                     if malicious_activity_detected and (current_time - last_alert_time) >= ALERT_INTERVAL:
#                         print("Spike pattern detected, triggering malicious alert!")
#                         threading.Thread(target=show_alert).start()  # Show alert in a separate thread
#                         last_alert_time = current_time  # Update last alert time

#                 # Check for alert duration
#                 if malicious_activity_detected:
#                     if time.time() - malicious_activity_start_time >= ALERT_DURATION:
#                         # Reset malicious activity state
#                         print("Alert duration exceeded, reset malicious activity state.")
#                         malicious_activity_detected = False
#                         malicious_activity_start_time = 0

#                 # Reset for the next second
#                 packet_count = 0
#                 ip_counts_per_second.clear()
#                 start_time = time.time()

# # Start the server to receive packets
# def start_monitoring():
#     threading.Thread(target=handle_client, daemon=True).start()

# # Run the monitoring system
# if __name__ == "__main__":
#     start_monitoring()


import socket
import threading
import time
from collections import deque, defaultdict
import tkinter as tk
from tkinter import messagebox
import vonage  # Import Vonage

# Configuration
BUFFER_SIZE = 33000
IP_ADDRESS = '192.168.1.6'
PORT = 12345

# Thresholds
PACKET_SIZE_THRESHOLD = 5000  # Set your packet size deviation threshold
MAX_IP_REPETITION_THRESHOLD = 10  # Set your max IP repetition threshold
SPIKE_THRESHOLD = 8000  # Spike threshold to detect major deviations
ALERT_DURATION = 5  # Duration in seconds to monitor thresholds
ALERT_INTERVAL = 3  # Interval in seconds to show alerts

# Packet data tracking history
history_length = 20  # Increased length to better show dynamic changes
packet_history = deque([0] * history_length, maxlen=history_length)
size_history = deque([0] * history_length, maxlen=history_length)
ip_repetition_history = deque([0] * history_length, maxlen=history_length)

# Metrics
lock = threading.Lock()
packet_size_deviation = 0
ip_repetition_frequency = defaultdict(float)

# Malicious activity tracking
malicious_activity_detected = False
malicious_activity_start_time = 0
last_alert_time = 0  # Time when the last alert was shown

# Initialize Vonage client
client = vonage.Client(key="4b83c384", secret="Br4SyKCIqYp8XvjC")
sms = vonage.Sms(client)

# Function to send SMS notification
def send_sms_alert():
    responseData = sms.send_message(
        {
            "from": "Cloud Shield AI",
            "to": "916379152566",  # Replace with the actual recipient number
            "text": "Cloud shield detected malicious traffic in your network",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

# Function to display malicious activity alert in a dialog box
def show_alert():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showwarning("Malicious Traffic Detected", "A major deviation pattern was detected, indicating potential malicious traffic!")
    root.destroy()
    send_sms_alert()  # Send SMS alert when the dialog appears

# Function to handle incoming packets
def handle_client():
    global packet_size_deviation, malicious_activity_detected, malicious_activity_start_time, last_alert_time
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP_ADDRESS, PORT))
    print(f"Receiver started at {IP_ADDRESS}:{PORT}")

    packet_count = 0
    start_time = time.time()
    last_packet_size = 0
    ip_counts_per_second = defaultdict(int)

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        packet_count += 1
        packet_size = len(data)
        ip_counts_per_second[addr[0]] += 1

        # Calculate packet size deviation
        packet_size_deviation = abs(packet_size - last_packet_size)
        last_packet_size = packet_size

        # Update packet count and reset every second
        if time.time() - start_time >= 1:
            with lock:
                # Update packets per second
                packet_history.append(packet_count)

                # Update packet size deviation history
                size_history.append(packet_size_deviation)

                # Update IP repetition frequency history
                ip_repetition_frequency.clear()
                for ip, count in ip_counts_per_second.items():
                    ip_repetition_frequency[ip] = count / 1.0  # Repetitions per second

                # Append the maximum IP repetition frequency of the second
                if ip_repetition_frequency:
                    max_ip_repetition = max(ip_repetition_frequency.values())
                    ip_repetition_history.append(max_ip_repetition)
                else:
                    ip_repetition_history.append(0)

                # Check for threshold breaches or spike patterns
                if packet_size_deviation > PACKET_SIZE_THRESHOLD or max_ip_repetition > MAX_IP_REPETITION_THRESHOLD:
                    if not malicious_activity_detected:
                        malicious_activity_detected = True
                        malicious_activity_start_time = time.time()
                        print("Malicious activity detected: Threshold exceeded!")

                # Check for specific spike pattern (high-low-high)
                if size_history[-1] > SPIKE_THRESHOLD and size_history[-2] < SPIKE_THRESHOLD and size_history[-3] > SPIKE_THRESHOLD:
                    current_time = time.time()
                    # Show alert every 3 seconds if malicious activity is detected
                    if malicious_activity_detected and (current_time - last_alert_time) >= ALERT_INTERVAL:
                        print("Spike pattern detected, triggering malicious alert!")
                        threading.Thread(target=show_alert).start()  # Show alert in a separate thread
                        last_alert_time = current_time  # Update last alert time

                # Check for alert duration
                if malicious_activity_detected:
                    if time.time() - malicious_activity_start_time >= ALERT_DURATION:
                        # Reset malicious activity state
                        print("Alert duration exceeded, reset malicious activity state.")
                        malicious_activity_detected = False
                        malicious_activity_start_time = 0

                # Reset for the next second
                packet_count = 0
                ip_counts_per_second.clear()
                start_time = time.time()

# Start the server to receive packets
def start_monitoring():
    threading.Thread(target=handle_client, daemon=True).start()

# Run the monitoring system
if __name__ == "__main__":
    start_monitoring()
