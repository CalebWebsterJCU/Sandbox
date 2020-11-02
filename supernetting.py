def convert_addresses_to_binary(a):
    binary_addresses = []
    for address in a:
        binary_addresses.append([f"{int(str(bin(int(octet)))[2:]):08}" for octet in address])
    return binary_addresses


def find_common_bits(octets):
    c_bits = ""
    for x in range(8):
        bits_set = {octet[x] for octet in octets}
        if len(bits_set) == 1:
            c_bits += bits_set.pop()
    return c_bits


def find_dissimilar_index(addresses):
    for x in range(4):
        for a in addresses:
            for a_to_compare in addresses:
                if a[x] != a_to_compare[x]:
                    return x


addresses = [
    ['100', '100', '12', '0'],
    ['100', '100', '13', '0'],
    ['100', '100', '14', '0'],
    ['100', '100', '15', '0'],
]
supernet_address_parts = []

# convert addresses to binary
binary_addresses = convert_addresses_to_binary(addresses)
# find index of the dissimilar octet
dissimilar_index = find_dissimilar_index(binary_addresses)
# find common bits of dissimilar octet
common_bits = find_common_bits([a[dissimilar_index] for a in binary_addresses])
# find common octet by converting common bits
common_octet = str(int(common_bits))
# find total number of common bits for subnet mask
total_common_bits = sum([8 for _ in binary_addresses[:dissimilar_index]]) + len(common_bits)
# build supernet address
for octet in addresses[0]:
    if addresses[0].index(octet) < dissimilar_index:
        supernet_address_parts.append(octet)
supernet_address_parts.append(common_octet)
# add zeros where needed
while len(supernet_address_parts) < 4:
    supernet_address_parts.append('0')
supernet_address = '.'.join(supernet_address_parts) + f'/{total_common_bits}'
print(supernet_address)
