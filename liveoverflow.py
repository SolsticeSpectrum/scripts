def decode_varint(data):
    result = 0
    shift = 0
    index = 0
    while True:
        byte = data[index]
        result |= (byte & 0x7F) << shift
        shift += 7
        index += 1
        if not byte & 0x80:
            break
    return result, index

packet_data = bytes([0x00, 0x00, 0x01, 0x1f, 0x00, 0x00, 0x00, 0xb9])
decoded_result = decode_varint(packet_data)
print(f"Decoded Value: {decoded_result[0]}")
print(f"Consumed Bytes: {decoded_result[1]}")
