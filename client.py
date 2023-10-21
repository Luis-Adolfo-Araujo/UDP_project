import socket as s

def checksum(data):
    byte_count = len(data)
    print(f"N. bytes: {byte_count}")
    return

def ping(host, port):
    client = s.socket(s.AF_INET, s.SOCK_DGRAM)
    addr = (host, port)
    data = b"ping"
    client.sendto(data, addr)
    data, addr = client.recvfrom(1024)
    if data == b"pong":
        print(f"{host} is up!")
    else:
        print(f"{host} is down!")

if __name__ == "__main__":
    HOST = s.gethostbyname(s.gethostname())
    PORT = 8080
    ping(HOST, PORT)