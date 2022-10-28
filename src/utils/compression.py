import zlib

# Compress string with zlib
def compress(data:bytes) -> bytes:
    return zlib.compress(data, 9)


# Decompress string with zlib
def decompress(data:bytes) -> bytes:
    return zlib.decompress(data)

if __name__ == '__main__':
    message = b'fd390000920101f200001e55311adcbda4d0308f04000000000000000000000000000000803f000000000000000000000000000000000000000000000000a83acd8c24dc49'
    print(message.decode())
    compressed = compress(message)
    print(len(compressed))
    decompressed = decompress(compressed)
    print(len(decompressed))