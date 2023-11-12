import socket, binascii


class MessageSender:
    @staticmethod
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
