#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

host = input("Enter host: ").strip()
scan_type = input("Scan type? (port/common/all): ").strip().lower()


def port_scan(host, port):
    try:
        with socket.create_connection((host, port), timeout=2) as sock:
            print(f"[OPEN] Port {port}")

            # Only send HTTP requests to HTTP services
            if port == 80:
                request = (
                    "HEAD / HTTP/1.0\r\n"
                    f"Host: {host}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                ).encode("utf-8")

                sock.sendall(request)

                sock.settimeout(2)
                response = sock.recv(1024)

                print(response.decode("utf-8", errors="replace"))

    except socket.timeout:
        print(f"[TIMEOUT] Port {port} (possibly filtered)")

    except ConnectionRefusedError:
        print(f"[CLOSED] Port {port}")

    except OSError as e:
        print(f"[ERROR] Port {port}: {e}")


if scan_type == "port":
    try:
        port = int(input("Enter port: "))
        if not 1 <= port <= 65535:
            print("Port must be between 1 and 65535.")
        else:
            port_scan(host, port)
    except ValueError:
        print("Please enter a valid integer.")

elif scan_type == "common":

    common_ports = [
        21, 22, 23, 25, 53, 80, 110,
        143, 443, 445, 1433, 3306, 3389
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(port_scan, repeat(host), common_ports))

elif scan_type == "all":

    with ThreadPoolExecutor(max_workers=6) as executor:
        list(executor.map(port_scan, repeat(host), range(1, 65536)))

else:
    print("Invalid scan type.")


# In[ ]:




