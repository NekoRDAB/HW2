from dns_answer_parser import DNSAnswerParser, DNSAnswer
from dns_query import DNSQuery
from message_sender import MessageSender
from dns_requests_check import format_hex


class DNSServer:
    def __init__(self, url):
        self.url = url

    def find_ip_address(self):
        query = DNSQuery.build_query_message(self.url)
        server = "192.5.5.241"
        port = 53
        response = MessageSender.send_udp_message(query, server, port)
        dns_answer_byte = DNSAnswerParser(response).parse_answer()
        dns_answer = DNSAnswer.parse_from_bytes(dns_answer_byte)
        while dns_answer.atype != "A":
            server_url = dns_answer.data
            server = DNSServer.get_server_ip(server_url)
            query = DNSQuery.build_query_message(self.url)
            response = MessageSender.send_udp_message(query, server, port)
            dns_answer_byte = DNSAnswerParser(response).parse_answer()
            dns_answer = DNSAnswer.parse_from_bytes(dns_answer_byte)
        return dns_answer.data

    @staticmethod
    def get_server_ip(server_url):
        query = DNSQuery.build_query_mesage(server_url)
        response = MessageSender.send_udp_message(query, "8.8.8.8", 53)
        dns_answer_byte = DNSAnswerParser(response).parse_answer()
        dns_answer = DNSAnswer.parse_from_bytes(dns_answer_byte)
        return dns_answer.data
