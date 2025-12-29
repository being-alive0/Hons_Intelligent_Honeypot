import socket
import json
from datetime import datetime, timezone # Updated import
import threading

# USE PORT 9999 for the demo (avoid admin permission issues)
HOST = '0.0.0.0'
PORT = 9999

def log_interaction(data):
    """Saves interaction data to a JSON log file."""
    with open('honeypot_log.json', 'a') as f:
        f.write(json.dumps(data) + '\n')

def handle_client(client, addr):
    print(f"\n[!] INCOMING CONNECTION: {addr[0]}")
    
    # FIX: Use datetime.now(timezone.utc) instead of utcnow()
    interaction_data = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'ip_address': addr[0],
        'port': addr[1],
        'credentials': [],
        'commands': []
    }

    try:
        client.sendall(b'IoT Device Login: ')
        username = client.recv(1024).strip().decode(errors='ignore')
        client.sendall(b'Password: ')
        password = client.recv(1024).strip().decode(errors='ignore')
        
        interaction_data['credentials'].append({'username': username, 'password': password})
        print(f"    -> Capturing Creds: {username}/{password}")

        client.sendall(b'\nroot@iot-device:~# ') 
        while True:
            command = client.recv(1024).strip().decode(errors='ignore')
            if not command or command.lower() in ['exit', 'quit']:
                break
            interaction_data['commands'].append(command)
            print(f"    -> Capturing Command: {command}")
            client.sendall(b'root@iot-device:~# ')
    except:
        pass
    finally:
        log_interaction(interaction_data)
        client.close()

def run_honeypot():
    print(f"[*] HONEYPOT ACTIVE. Listening on {HOST}:{PORT}...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    while True:
        client, addr = server.accept()
        # Use threads so we can handle multiple "bots" at once
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.start()

if __name__ == '__main__':
    run_honeypot()