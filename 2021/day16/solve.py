from operator import mul
from functools import reduce


def toBinary(hexDigit):
    value = int(hexDigit, 16)
    ret = bin(value)[2:]
    while len(ret) < 4:
        ret = '0' + ret
    return ret


def main():
    hexInputData = input().strip()
    binaryData = ''.join(toBinary(hexDigit) for hexDigit in hexInputData)

    def value(l, r):
        return int(binaryData[l : r], 2)

    def readSinglePacket(i):
        packetType = value(i + 3, i + 6)
        i += 6
        if packetType == 4:
            # Literal number, read hex digits
            ret = 0
            while i < len(binaryData):
                cont = value(i, i + 1)
                val = value(i + 1, i + 5)
                i += 5
                ret = 16 * ret + val
                if cont == 0:
                    break

            return (i, ret)
        else:
            # operator packet.
            encType = value(i, i + 1)
            i += 1
            next_i = i + 11
            sub_packets = []
            if encType == 0:
                # no. of bits to read.
                start, next_i = i + 15, i + 15
                numBits = value(i, i + 15)
                while next_i < start + numBits:
                    next_i, sub = readSinglePacket(next_i)
                    sub_packets.append(sub)
            else:
                # no. of packets to read.
                numPackets = value(i, i + 11)
                next_i = i + 11
                for _ in range(numPackets):
                    next_i, sub = readSinglePacket(next_i)
                    sub_packets.append(sub)

            # 0 - sum, 1 - prod, 2 - min, 3 - max, 4 - literal, 5 - greater
            # 6 - lesser, 7 - equal
            ret = 0
            if packetType == 0:
                ret = sum(sub_packets)
            elif packetType == 1:
                ret = reduce(mul, sub_packets)
            elif packetType == 2:
                ret = min(sub_packets)
            elif packetType == 3:
                ret = max(sub_packets)
            elif packetType == 5:
                ret = int(sub_packets[0] > sub_packets[1])
            elif packetType == 6:
                ret = int(sub_packets[0] < sub_packets[1])
            else:
                ret = int(sub_packets[0] == sub_packets[1])
            return (next_i, ret)


    _, ret = readSinglePacket(0)
    print(ret)


if __name__  == '__main__':
    main()
