"""
Supernetting
2/11/2020
This program determines the supernet for a group of subnet addresses.
"""

ADDRESS_FILE = 'addresses.txt'


def main():
    """
    Determine supernet of addresses.
    Step 1: read addresses from address file
    Step 2: find the dissimilar octet index
    Step 3: find common bits between dissimilar octets
    Step 4: convert common bits to binary to form common octet
    Step 5: find total common bits between all addresses
    Step 6: build supernet address from parts
    """
    addresses = read_addresses(ADDRESS_FILE)
    # find index of the dissimilar octet
    dissimilar_index = find_dissimilar_index(addresses)
    # find dissimilar octets of all addresses
    dissimilar_octets = [a[dissimilar_index] for a in addresses]
    # find common bits of dissimilar octet
    common_bits = find_common_bits([conv_num_to_bin_octet(octet) for octet in dissimilar_octets])
    # find common octet by converting common bits
    super_octet = conv_bin_to_octet(common_bits)
    # find total number of common bits for subnet mask
    total_common_bits = 8 * dissimilar_index + len(common_bits)
    # build supernet address
    supernet_address, supernet_mask = build_supernet_address(addresses[0], dissimilar_index, super_octet, total_common_bits)
    print('Subnet Addresses:')
    for address in addresses:
        print('.'.join(address))
    print('\nD.O | Binary')
    for octet in dissimilar_octets:
        print(f'{octet:3} | {conv_num_to_bin_octet(octet)}')
    print('\nCommon Bits  |  Octet')
    print(f'{common_bits + "(" + "0" * (8 - len(common_bits)) + ")":11}  |  {super_octet}')
    print(f'\nMask: {8 * dissimilar_index} + {len(common_bits)} = /{total_common_bits}')
    print(f'\nSupernet Address:')
    print(f'{supernet_address}{supernet_mask}')


def read_addresses(filename):
    """
    Read addresses from file and only return valid ones.
    :param filename: name of file to read from
    :return: list of valid addresses
    """
    addresses = []
    with open(filename, 'r') as address_file:
        for line in address_file:
            address = line.strip().split('.')
            if max(int(part) for part in address) <= 255 and min(int(part) for part in address) >= 0:
                addresses.append(address)
    return addresses


def find_common_bits(binary_numbers):
    """
    Find common bits between multiple binary numbers.
    :param binary_numbers: list of binary numbers to compare
    :return: binary string of common bits
    """
    c_bits = ""
    x = 0
    bits = [number[x] for number in binary_numbers]
    while items_are_equal(bits):
        c_bits += bits[0]
        x += 1
        bits = [number[x] for number in binary_numbers]
    # for x in range(8):
    #     bits = [number[x] for number in binary_numbers]
    #     if items_are_equal(bits):
    #         c_bits += bits[0]
    #     else:
    #         break
    return c_bits


def find_dissimilar_index(addresses):
    """
    Iterate through list of addresses and return the dissimilar octet index.
    :param addresses: list of addresses to compare
    :return: index of the octet where the addresses start to change
    """
    for x in range(4):
        for a in addresses:
            for a_to_compare in addresses:
                if a[x] != a_to_compare[x]:
                    return x


def items_are_equal(the_list):
    """
    Compare two lists and return True if all items are the same, False if they are not.
    :param the_list: list of items to compare
    :return: True or False
    """
    for item in the_list:
        for item_to_compare in the_list:
            if item != item_to_compare:
                return False
    return True


def conv_num_to_bin_octet(number):
    """
    Given a integer, convert it to a binary octet.
    :param number: number to convert
    :return: string of binary number with length 8
    """
    binary_octet = bin(int(number))[2:]
    while len(binary_octet) != 8:
        if len(binary_octet) < 8:
            binary_octet = "0" + binary_octet
        else:
            binary_octet = binary_octet[:-1]
    return binary_octet


def conv_bin_to_octet(bits):
    """
    Given a binary octet, convert it to an integer.
    If binary string length is not 8, zeros will be added
    or removed from the right until the length is 8.
    :param bits: string of binary octet
    :return: converted integer
    """
    while len(bits) != 8:
        if len(bits) < 8:
            bits += "0"
        else:
            bits = bits[:-1]
    return str(int(bits, 2))


def build_supernet_address(first_address, d_index, super_octet, total_common_bits):
    """
    Construct a supernet address from all parts passed in.
    :param first_address: first address from subnet address list
    :param d_index: index of dissimilar octet
    :param super_octet: number formed from common bits between dissimilar octet
    :param total_common_bits: total number of common bits between all subnet addresses
    :return: string of supernet address, string of supernet mask in slash notation
    """
    parts = [octet for index, octet in enumerate(first_address) if index < d_index]
    parts.append(super_octet)
    while len(parts) < 4:
        parts.append('0')
    supernet_address = '.'.join(parts)
    supernet_mask = f'/{total_common_bits}'
    return supernet_address, supernet_mask


main()
