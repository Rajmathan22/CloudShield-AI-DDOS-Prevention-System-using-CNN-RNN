import socket
import threading
import tkinter as tk
import time
import random

# Configuration
SERVER_IP = '192.168.1.6'  # IP of the server laptop
SERVER_PORT = 12345  # Port the server is listening on
BUFFER_SIZE = 33000  # Packet size
running = False
is_ddos = False  # To track if DDoS is currently running

# Function to generate a random IP address (simulating different source IPs)
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Function to send packets (normal or DDoS)
def send_packets(normal=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while running:
        if normal:
            # Simulate traffic with varying IPs and normal data size
            data = b"Normal request"  # Normal packet size
            packet_type = "Normal packet"
            rate = 0.5  # Slower rate for normal traffic
            src_ip = generate_random_ip()  # Random IP for each normal packet
        else:
            # Simulate a DDoS attack with larger, variable data sizes and repetitive IPs
            data_size = random.randint(500, 1500)  # Variable packet sizes for DDoS
            data = b"DDoS attack packet" * data_size  # Larger payload for DDoS
            packet_type = f"DDoS packet of size {len(data)}"
            rate = random.uniform(0.005, 0.02)  # Faster sending rate
            src_ip = random.choice([generate_random_ip() for _ in range(5)])  # Some repetition in source IPs

        # Simulate sending the packet to the server
        sock.sendto(data, (SERVER_IP, SERVER_PORT))

        print(f"Sending {packet_type} from {src_ip} to {SERVER_IP}:{SERVER_PORT}")  # Log message
        time.sleep(rate)

    sock.close()

# Functions for button commands
def start_normal_traffic():
    global running, is_ddos
    running = True
    is_ddos = False
    threading.Thread(target=send_packets, args=(True,), daemon=True).start()  # Simulates normal traffic
    print("Normal traffic started!")  # Log message

def start_ddos():
    global running, is_ddos
    running = True
    is_ddos = True
    threading.Thread(target=send_packets, args=(False,), daemon=True).start()  # Simulates DDoS
    print("DDoS attack started!")  # Log message

def stop_ddos():
    global running, is_ddos
    running = False
    print("DDoS attack ended!")  # Log message
    time.sleep(1)  # Wait a moment before starting normal traffic again
    start_normal_traffic()  # Start normal traffic again after stopping DDoS
    print("Normal traffic resumed!")  # Log message

# Create a simple GUI using Tkinter
root = tk.Tk()
root.title("DDoS Attack Simulator")

tk.Label(root, text="Choose traffic type:").pack(pady=10)

# Buttons to activate normal traffic, DDoS, or stop DDoS
start_button = tk.Button(root, text="Start Normal Traffic", command=start_normal_traffic)
start_button.pack(pady=5)

ddos_button = tk.Button(root, text="DDoS Init", command=start_ddos)
ddos_button.pack(pady=5)

stop_ddos_button = tk.Button(root, text="Stop DDoS", command=stop_ddos)
stop_ddos_button.pack(pady=5)

root.mainloop()
