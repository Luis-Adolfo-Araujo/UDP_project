import socket as s

def checksum(data):
    byte_count = len(data)
    print(f"N. bytes: {byte_count}")

if __name__ == "__main__":
    HOST = s.gethostbyname(s.gethostname())
    PORT = 8080
    server = s.socket(s.AF_INET, s.SOCK_DGRAM)
    server.bind((HOST, PORT))
    expected_seq_num = 0

    while True:
        data, addr = server.recvfrom(1024)
        seq_num, data = data.split(b"|", 1)
        seq_num = int(seq_num)
        data = data.decode("utf-8")

        if seq_num == expected_seq_num:
            print(f"Received from Client: {data}")
            data = data.upper()
            data = data.encode("utf-8")
            checksum(data)
            server.sendto(data, addr)
            expected_seq_num += 1
        else:
            print(f"Received out-of-order packet with seq_num {seq_num}. Ignoring.")
