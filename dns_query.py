import binascii
import socket


class DNSQuery:
    message_id = 0

    @staticmethod
    def build_query_message(url):
        header = DNSQuery.build_header("0000")
        question = DNSQuery.build_question(url)
        return header + question

    @staticmethod
    def build_header(flags):
        hex_id = DNSQuery.bin_to_hex(f"{DNSQuery.message_id:0>16b}")
        DNSQuery.message_id = (DNSQuery.message_id + 1) % 2**16
        qdcount = "0001"
        ancount = "0000"
        nscount = "0000"
        arcount = "0000"
        header = hex_id+flags+qdcount+ancount+nscount+arcount
        return header

    @staticmethod
    def build_question(url):
        qname = DNSQuery.build_qname(url)
        qtype = "0001"
        qclass = "0001"
        question = qname + qtype + qclass
        return question

    @staticmethod
    def build_qname(url):
        sections = url.split('.')
        qname = ""
        for section in sections:
            qname += DNSQuery.build_label(section)
        return qname + "00"

    @staticmethod
    def build_label(section):
        length = f"{len(section):0>8b}"
        label = f"{DNSQuery.bin_to_hex(length)}"
        for symbol in section:
            binary_code = f"{ord(symbol):0>8b}"
            hex = DNSQuery.bin_to_hex(binary_code)
            label += hex
        return label

    @staticmethod
    def bin_to_hex(binary):
        hex = ""
        for i in range(0, len(binary), 4):
            quartet = binary[i:i+4]
            hex += str(format(int(quartet, 2), 'x'))
        return hex

    @staticmethod
    def build_query_mesage(url):
        header = DNSQuery.build_header("0100")
        question = DNSQuery.build_question(url)
        return header + question


def format_hex(hex):
    """format_hex returns a pretty version of a hex string"""
    octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
    pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
    return "\n".join(pairs)
