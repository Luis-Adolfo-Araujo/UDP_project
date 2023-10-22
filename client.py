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


if __name__ == "__main__":
    HOST = s.gethostbyname(s.gethostname())
    PORT = 8080
    client = s.socket(s.AF_INET, s.SOCK_DGRAM)
    addr = (HOST, PORT)

    while True:
        data = input("Enter a word: ")
        data = data.encode("utf-8")

        send_mode = input("Send mode (isolated/batch): ")

        if send_mode == "isolated":
            checksum_value = checksum(data)
            checksum_bytes = checksum_value.to_bytes(2, byteorder="big")
            client.sendto(checksum_bytes, addr)
            client.sendto(data, addr)
        elif send_mode == "batch":
            packets = []

            while True:
                data = input("Enter a word (or empty line to finish): ")
                data = data.encode("utf-8")

                if not data:
                    break

                checksum_value = checksum(data)
                checksum_bytes = checksum_value.to_bytes(2, byteorder="big")
                packets.append((checksum_bytes, data))

            for checksum_bytes, data in packets:
                client.sendto(checksum_bytes, addr)
                client.sendto(data, addr)

        data, addr = client.recvfrom(1024)
        data = data.decode("utf-8")

        if data == "ERRO":
            print("Falha de integridade")
        else:
            print(len(data))
