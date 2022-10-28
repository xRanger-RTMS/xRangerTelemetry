# split mavlink packages from a long binary string
def split_packages(data: bytes) -> [bytes]:
    packages = []
    i = 0
    while i < len(data):
        if data[i] == 0xfd:
            length = data[i + 1]
            packages.append(data[i:i + length + 12])
            i += length + 12
    return packages


def merge_packages(packages: [bytes]) -> bytes:
    return b''.join(packages)


if __name__ == '__main__':
    mavlink_packets = [
        b"\xfd\x32\x00\x00\xdd\x01\x01\x7c\x00\x00\x30\x33\xb6\x32\x27\x00"
        b"\x00\x00\x1d\x55\x31\x1a\xbd\xbd\xa4\xd0\x72\x84\x04\x00\x00\x00"
        b"\x00\x00\x37\x00\x46\x00\x00\x00\xbc\x02\x06\x1a\x00\x60\x86\x71"
        b"\xf7\x03\x00\x14\x00\x00\x00\x1c\x00\x00\x00\xe6\x12\xab",
        b"\xfd\x05\x00\x00\x64\x01\x01\x7d\x00\x00\xd7\x12\x59\x13\x05\xd4\xfb",
        b"\xfd\x10\x00\x00\x26\x03\x01\x74\x00\x00\x49\xc0\x61\x01\x0b\x00" 
        b"\xb5\x00\x95\xfc\x30\x00\x36\x00\xb1\xff\xc2\x55"
    ]

    merged = merge_packages(mavlink_packets)

    print(merged)

    split = split_packages(merged)

    print(split)
