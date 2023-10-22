import socket as s
import random

def verify_checksum(data, checksum):
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

    return checksum_value == checksum

if __name__ == "__main__":
    
    HOST = s.gethostbyname(s.gethostname())
    PORT = 8080
    server = s.socket(s.AF_INET, s.SOCK_DGRAM)
    server.bind((HOST, PORT))

    while True:
        checksum_bytes, addr = server.recvfrom(1024)
        checksum = int.from_bytes(checksum_bytes, byteorder="big")
        data, addr = server.recvfrom(1024)
        data = data.decode("utf-8")

        print("Client: {data}")

        #random simulation check for the packet integrity
        integrity_error = random.randint(0, 100)
        if integrity_error <= 25:
            print("Pacote contém erro de integridade.")
            server.sendto(b"ERRO", addr)
        else:
            if verify_checksum(data.encode("utf-8"), checksum):
                print("Checksum is valid.")
            else:
                print("Checksum is invalid.")

        data = data.upper()
        data = data.encode("utf-8")
        server.sendto(data, addr)
