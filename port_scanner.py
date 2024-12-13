import socket
import threading
import time
import os
import webbrowser

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "192.168.1.1"

def ip_range(start_ip):
    # Convert IP to numbers
    start_parts = list(map(int, start_ip.split('.')))
    start_parts[3] = 1
    
    for i in range(1, 255):
        current = list(start_parts)
        current[3] = i
        yield '.'.join(map(str, current))

def check_port(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((str(ip), 5000))
        sock.close()
        if result == 0:
            print(f"Found service on {ip}:5000")
            return str(ip)
    except:
        pass
    return None

def scan_network():
    local_ip = get_local_ip()
    print(f"Local IP: {local_ip}")
    print(f"Scanning network for port 5000...")
    
    threads = []
    found_ips = []
    thread_lock = threading.Lock()
    
    def worker(ip):
        result = check_port(ip)
        if result:
            with thread_lock:
                found_ips.append(result)
    
    # Create threads for scanning
    for ip in ip_range(local_ip):
        while threading.active_count() > 20:  # Limit concurrent threads
            time.sleep(0.1)
        t = threading.Thread(target=worker, args=(ip,))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    if found_ips:
        for ip in found_ips:
            url = f"http://{ip}:5000"
            print(f"Found service at: {url}")
            try:
                webbrowser.open(url)
                print(f"Opened browser to {url}")
            except:
                print(f"Could not open browser. Please manually visit: {url}")
        return True
    return False

if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    print("Port Scanner v1.0")
    print("=================")
    print("This program will scan your local network for services running on port 5000")
    print("Press Ctrl+C to stop the scan at any time")
    print("")
    
    try:
        if not scan_network():
            print("\nNo services found running on port 5000 in the local network.")
    except KeyboardInterrupt:
        print("\nScan stopped by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    print("\nPress Enter to exit...")
    input()
