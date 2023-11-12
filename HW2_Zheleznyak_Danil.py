import binascii
import socket


class DNSMessage:
    message_id = 0

    @staticmethod
    def build_query_message(url):
        header = DNSMessage.build_header("0000")
        question = DNSMessage.build_question(url)
        return header + question

    @staticmethod
    def build_header(flags):
        hex_id = DNSMessage.bin_to_hex(f"{DNSMessage.message_id:0>16b}")
        qdcount = "0001"
        ancount = "0000"
        nscount = "0000"
        arcount = "0000"
        header = hex_id+flags+qdcount+ancount+nscount+arcount
        return header

    @staticmethod
    def build_question(url):
        qname = DNSMessage.build_qname(url)
        qtype = "0001"
        qclass = "0001"
        question = qname + qtype + qclass
        return question

    @staticmethod
    def build_qname(url):
        sections = url.split('.')
        qname = ""
        for section in sections:
            qname += DNSMessage.build_label(section)
        return qname + "00"

    @staticmethod
    def build_label(section):
        length = f"{len(section):0>8b}"
        label = f"{DNSMessage.bin_to_hex(length)}"
        for symbol in section:
            binary_code = f"{ord(symbol):0>8b}"
            hex = DNSMessage.bin_to_hex(binary_code)
            label += hex
        return label

    @staticmethod
    def bin_to_hex(binary):
        hex = ""
        for i in range(0, len(binary), 4):
            quartet = binary[i:i+4]
            hex += str(format(int(quartet, 2), 'x'))
        return hex


def send_udp_message(message, address, port):
    """send_udp_message sends a message to UDP server

    message should be a hexadecimal encoded string
    """
    server_address = (address, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")


def format_hex(hex):
    """format_hex returns a pretty version of a hex string"""
    octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
    pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
    return "\n".join(pairs)


message = DNSMessage.build_query_message("vk.com")
print(format_hex(send_udp_message(message, "198.41.0.4", 53)))
