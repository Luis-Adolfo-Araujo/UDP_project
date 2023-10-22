import socket as s
import time
import random

def checksum(data):
    byte_count = len(data)
    print(f"N. bytes: {byte_count}")

def simulate_packet_corruption(data, error_probability):
    if random.random() < error_probability:
        print("Simulating packet corruption")
        data = data.replace(b' ', b'X')  # Substitui espaço por 'X' para simular corrupção
    return data

def simulate_packet_loss(loss_probability):
    return random.random() > loss_probability

def send_packet(seq_num, data, addr, client_socket, error_probability, loss_probability):
    data = simulate_packet_corruption(data, error_probability)
    if not simulate_packet_loss(loss_probability):
        packet = str(seq_num).encode() + b"|" + data
        checksum(packet)
        client_socket.sendto(packet, addr)

if __name__ == "__main__":
    HOST = s.gethostbyname(s.gethostname())
    PORT = 8080
    client = s.socket(s.AF_INET, s.SOCK_DGRAM)
    addr = (HOST, PORT)
    window_size = 5  # Tamanho da janela
    next_seq_num = 0
    base_seq_num = 0
    unacked_packets = {}

    while True:
        while next_seq_num < base_seq_num + window_size:
            data = input("Enter a word (or 'exit' to quit): ")
            if data.lower() == 'exit':
                client.close()
                exit()
            data = data.encode("utf-8")
            send_packet(next_seq_num, data, addr, client)
            unacked_packets[next_seq_num] = data
            next_seq_num += 1

        try:
            data, addr = client.recvfrom(1024)
            seq_num = int(data.decode())
            print(f"Received acknowledgment for seq_num {seq_num}")
            while base_seq_num <= seq_num:
                del unacked_packets[base_seq_num]
                base_seq_num += 1
        except s.timeout:
            print("Timeout, retransmitting unacknowledged packets...")
            for seq_num, data in unacked_packets.items():
                send_packet(seq_num, data, addr, client)
