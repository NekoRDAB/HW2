import argparse
from dns_server import DNSServer


def main():
    parser = argparse.ArgumentParser(description="dns server")
    parser.add_argument(
        "url", type=str,
        help="URL you wish to get ip address of"
    )
    args = parser.parse_args()
    url = args.url


if __name__ == "__main__":
    main()
