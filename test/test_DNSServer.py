import unittest
from dns_server import DNSServer


class TestDNSServer(unittest.TestCase):
    def ips_equal_wout_end(self, first, second):
        sections_first = first.split(".")[:-1]
        sections_second = second.split(".")[:-1]
        return sections_first == sections_second

    def test_find_ip_address_vk(self):
        url = "vk.com"
        server = DNSServer(url)
        expected = "87.240.132.78"
        actual = server.find_ip_address()
        self.assertTrue(self.ips_equal_wout_end(expected, actual))


if __name__ == '__main__':
    unittest.main()
