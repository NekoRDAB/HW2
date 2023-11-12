from dns_query import DNSQuery
from message_sender import MessageSender


class DNSServer:
    def __init__(self, url):
        self.url = url

    def find_ip_address(self):
        query = DNSQuery.build_query_message(self.url)
        server = "198.41.0.4"
        port = 53
        response = MessageSender.send_udp_message(query, server, port)
        
