import socket as s

def checksum(data):
    byte_count = len(data)
    print(f"N. bytes: {byte_count}")
    
    if byte_count % 2 == 1:
        data += b'\x00'
        byte_count += 1

    checksum_value = 0

    for i in range(0, byte_count, 2):
        w = (data[i] << 8) + data[i + 1]
        checksum_value += w
        checksum_value = (checksum_value >> 16) + (checksum_value & 0xFFFF)

    checksum_value = ~checksum_value & 0xFFFF

    return checksum_value

def ping(host, port):
    client = s.socket(s.AF_INET, s.SOCK_DGRAM)
    addr = (host, port)
    data = b"ping"
    client.sendto(data, addr)
    data, addr = client.recvfrom(1024)
    if data == b"ping":
        print(f"{host} is up!")
    else:
        print(f"{host} is down!")


if __name__ == "__main__":
    HOST = s.gethostbyname(s.gethostname())
    PORT = 8080
    client = s.socket(s.AF_INET, s.SOCK_DGRAM)
    addr = (HOST, PORT)
    
    client.settimeout(1)

    while True:
        ping(HOST, PORT)
        data = input("Enter a word: ")
        data = data.encode("utf-8")
        checksum_value = checksum(data)
        checksum_bytes = checksum_value.to_bytes(2, byteorder="big")
        client.sendto(checksum_bytes, addr)
        client.sendto(data, addr)
        data, addr = client.recvfrom(1024)
        data = data.decode("utf-8")
        if data == "ERRO":
            print("Falha de integridade")
        else:
            print("pacote sem falha de integridade")
