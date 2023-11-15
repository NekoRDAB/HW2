class DNSAnswerParser:
    def __init__(self, answer):
        self.answer = answer
        self.pointer = 0

    def parse_answer(self):
        question = self.parse_question()
        qtype = self.next_byte() + self.next_byte()
        qclass = self.next_byte() + self.next_byte()
        name = self.parse_name()
        atype = self.next_byte() + self.next_byte()
        aclass = self.next_byte() + self.next_byte()
        ttl = (self.next_byte() + self.next_byte()
               + self.next_byte() + self.next_byte())
        rdlength = self.next_byte() + self.next_byte()
        rddata = self.parse_rddata(rdlength)
        return DNSAnswerByte(question, qtype, qclass,
                             name, atype, aclass, ttl, rdlength, rddata)

    def parse_question(self):
        id = self.next_byte() + self.next_byte()
        flags = self.next_byte() + self.next_byte()
        qdcount = self.next_byte() + self.next_byte()
        ancount = self.next_byte() + self.next_byte()
        nscount = self.next_byte() + self.next_byte()
        arcount = self.next_byte() + self.next_byte()
        header = (id + flags + qdcount
                  + ancount + nscount + arcount)
        qname = self.parse_qname()
        return header, qname

    def parse_name(self):
        hex_offset = self.next_byte() + self.next_byte()
        binary_offset = bin(int(hex_offset, base=16))[4:]
        index = 2 * int(binary_offset, base=2)
        sections = []
        length = int(self.byte_at(index), base=16)
        index += 2
        while length > 0:
            section = ""
            for i in range(length):
                symbol_code = int(self.byte_at(index), base=16)
                index += 2
                section += chr(symbol_code)
            sections.append(section)
            length = int(self.byte_at(index), base=16)
            index += 2
        return ".".join(sections)

    def parse_qname(self):
        sections = []
        length = int(self.next_byte(), base=16)
        while length > 0:
            section = ""
            for i in range(length):
                symbol_code = int(self.next_byte(), base=16)
                section += chr(symbol_code)
            sections.append(section)
            length = int(self.next_byte(), base=16)
        return ".".join(sections)

    def parse_rddata(self, rdlength):
        length = int(rdlength, base=16)
        rddata = ""
        for i in range(length):
            rddata += self.next_byte()
        return rddata

    def next_byte(self):
        result = self.answer[self.pointer: self.pointer + 2]
        self.pointer += 2
        return result

    def byte_at(self, index):
        return self.answer[index: index + 2]


class DNSAnswerByte:
    def __init__(self, question, qtype, qclass,
                 name, atype, aclass, ttl, rdlength, rddata):
        self.question = question
        self.qtype = qtype
        self.qclass = qclass
        self.name = name
        self.atype = atype
        self.aclass = aclass
        self.ttl = ttl
        self.rdlength = rdlength
        self.rddata = rddata


class DNSAnswer:
    ATYPES = {1: "A", 2: "NS"}

    def __init__(self, name, atype, aclass, ttl, data):
        self.name = name
        self.atype = atype
        self.aclass = aclass
        self.ttl = ttl
        self.data = data

    @staticmethod
    def parse_from_bytes(byte_answer: DNSAnswerByte):
        name = byte_answer.name
        atype = DNSAnswer.ATYPES[byte_answer.atype]
        aclass = "IN"
        ttl = int(byte_answer.ttl, base=16)
        data = DNSAnswer.parse_data(byte_answer.rddata)

    @staticmethod
    def parse_data(rddata: str):

