import socket as s
import os

def checksum(data):
    byte_count = len(data)
    print(f"N. bytes: {byte_count}")
    return

def ping(host, port):
    data = b"pong"
    client = s.socket(s.AF_INET, s.SOCK_DGRAM)
    addr = (host, port)
    client.sendto(data, addr)

def ping_response(host, port):
    data = b"pong"
    client = s.socket(s.AF_INET, s.SOCK_DGRAM)
    addr = (host, port)
    client.sendto(data, addr)

if __name__ == "__main__":
    
    HOST = s.gethostbyname(s.gethostname())
    PORT = 8080
    server = s.socket(s.AF_INET, s.SOCK_DGRAM)
    server.bind((HOST, PORT))

    # Set the timeout to 1 second.
    server.settimeout(1)

    print("Current timeout: " + str(server.getdefaulttimeout()))

    while True:
        try:
            data, addr = server.recvfrom(1024)
            data = data.decode("utf-8")

            print(f"Client: {data}")
            if data == "ping":
                ping_response(addr[0], addr[1])
        except s.timeout as e:
            print(e)