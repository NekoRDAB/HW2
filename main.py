import argparse
import socket
from dns_server import DNSServer
from server import Server


HOST = "127.0.0.1"
PORT = 65432


def main():
    parser = argparse.ArgumentParser(description="dns server")
    parser.add_argument(
        "url", type=str,
        help="URL you wish to get ip address of"
    )
    args = parser.parse_args()
    url = args.url
    dns_server = DNSServer(url)
    ip = dns_server.find_ip_address()
    print(f"IP address for domain {url}: {ip}")


if __name__ == "__main__":
    main()
