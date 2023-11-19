import argparse
import socket
from dns_server import DNSServer
from server import Server


HOST = "127.0.0.1"
PORT = 65432


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024).decode().replace("\n", "").split()
            url = data[-1]
            dns_server = DNSServer(url)
            ip = dns_server.find_ip_address()
            conn.sendall(ip.encode())

    # parser = argparse.ArgumentParser(description="dns server")
    # parser.add_argument(
    #     "url", type=str,
    #     help="URL you wish to get ip address of"
    # )
    # args = parser.parse_args()
    # url = args.url
    # dns_server = DNSServer(url)
    # ip = dns_server.find_ip_address()
    # print(f"IP address for domain {url}: {ip}")


if __name__ == "__main__":
    main()
