from dns_answer_parser import DNSAnswer
import unittest


class TestDNSAnswerParser(unittest.TestCase):
    def test_parse_ip(self):
        rddata = "5db8d822"
        expected = "93.184.216.34"
        actual = DNSAnswer.parse_ip(rddata)
        self.assertEqual(expected, actual)

        rddata = "c0a80001"
        expected = "192.168.0.1"
        actual = DNSAnswer.parse_ip(rddata)
        self.assertEqual(expected, actual)

    def test_parse_domain_name(self):
        rddata = "01650c67746c642d73657276657273036e657400"
        expected = "e.gtld-servers.net"
        actual = DNSAnswer.parse_domain_name(rddata)
        self.assertEqual(expected, actual)

    def test_parse_data(self):
        rddata = "5db8d822"
        expected = "93.184.216.34"
        actual = DNSAnswer.parse_data("A", rddata)
        self.assertEqual(expected, actual)

        rddata = "01650c67746c642d73657276657273036e657400"
        expected = "e.gtld-servers.net"
        actual = DNSAnswer.parse_data("NS", rddata)
        self.assertEqual(expected, actual)

    def test_parse_compressed_label(self):
        DNSAnswer.answer ="0000820000010000000d000b07796f757475626503636f6d0000010001c014000200010002a300001401650c67746c642d73657276657273036e657400c01400"
        offset = bin(int("c014", base=16))[2:]
        expected = "com"
        actual = DNSAnswer.parse_compressed_label(offset)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
