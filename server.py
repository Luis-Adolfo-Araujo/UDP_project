import socket as s
import time

def checksum(data):
    byte_count = len(data)
    print(f"N. bytes: {byte_count}")
    
def handle_packet(data, seq_num, addr, server_socket, error_probability):
    # Verifique a integridade do pacote (exemplo simples)
    if b'X' in data:  # Simula erro de corrupção
        print("Received a corrupted packet, ignoring.")
        return

if __name__ == "__main__":
    HOST = s.gethostbyname(s.gethostname())
    PORT = 8080
    server = s.socket(s.AF_INET, s.SOCK_DGRAM)
    server.bind((HOST, PORT))
    server.settimeout(5)  # Tempo limite para receber reconhecimentos
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
            server.sendto(str(seq_num).encode(), addr)  # Envia o reconhecimento
            expected_seq_num += 1
        else:
            print(f"Received out-of-order packet with seq_num {seq_num}. Sending NACK.")
            server.sendto(str(expected_seq_num - 1).encode(), addr)  # Envia NACK
