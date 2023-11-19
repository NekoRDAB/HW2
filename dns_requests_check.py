import binascii
import socket


def send_udp_message(message, address, port):
    """send_udp_message sends a message to UDP server

    message should be a hexadecimal encoded string
    """
    message = message.replace(" ", "").replace("\n", "")
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


# message_recursive = "AA AA 01 00 00 01 00 00 00 00 00 00 " \
#     "02 76 6B 03 63 6f 6d 00 00 01 00 01"
# response_recursive = send_udp_message(message_recursive, "198.41.0.4", 53)
# print(format_hex(response_recursive))
# print("////")

# message_iterative = "AA AA 00 00 00 01 00 00 00 00 00 00 " \
#     "02 76 6B 03 63 6f 6d 00 00 02 00 01"
# response_iterative = send_udp_message(message_iterative, "198.41.0.4", 53)
# print(format_hex(response_iterative))
# print("////")

# message_recursive_for_gltd_servers = "AA AA 01 00 00 01 00 00 00 00 00 00 " \
#     "01 65 0c 67 74 6C 64 2D 73 65 72 76 65 72 73 03 6E 65 74 00 00 01 00 01"
# response_recursive_for_gltd_servers = send_udp_message(message_recursive_for_gltd_servers, "8.8.8.8", 53)
# print(format_hex(response_recursive_for_gltd_servers))
# print("////")
#
# message_iterative_for_ns2_google_com = "AA AA 00 00 00 01 00 00 00 00 00 00 " \
#     "03 6E 73 32 06 67 6F 6F 67 6C 65 03 63 6F 6D 00 00 01 00 01"
# response_iterative_for_ns2_google_com = send_udp_message(message_iterative_for_ns2_google_com, "198.41.0.4", 53)
# print(format_hex(response_iterative_for_ns2_google_com))
