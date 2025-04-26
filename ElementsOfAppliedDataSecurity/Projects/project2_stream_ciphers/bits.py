class Bits:
    """A mutable sequence of bits."""

    def __init__(self, value, length=None):
        if isinstance(value, int):
            if length is None:
                length = value.bit_length() or 1
            self.bits = [((value >> i) & 1) == 1 for i in reversed(range(length))]
        elif isinstance(value, (bytes, bytearray)):
            self.bits = [((byte >> i) & 1) == 1 for byte in value for i in reversed(range(8))]
        else:  # assume iterable of booleans
            self.bits = list(value)

    def __len__(self):
        return len(self.bits)

    def __getitem__(self, index):
        return self.bits[index]

    def __setitem__(self, index, value):
        self.bits[index] = bool(value)

    def __str__(self):
        return ''.join('1' if bit else '0' for bit in self.bits)

    def __repr__(self):
        return f"Bits('{str(self)}')"

    def append(self, bit):
        self.bits.append(bool(bit))

    def pop(self, index=-1):
        return self.bits.pop(index)

    def parity_bit(self):
        return sum(self.bits) % 2 == 1

    def __xor__(self, other):
        if len(self) != len(other):
            raise ValueError("Bit sequences must be of the same length for XOR.")
        return Bits([a ^ b for a, b in zip(self.bits, other.bits)])

    def __and__(self, other):
        if len(self) != len(other):
            raise ValueError("Bit sequences must be of the same length for AND.")
        return Bits([a & b for a, b in zip(self.bits, other.bits)])

    def __add__(self, other):
        return Bits(self.bits + other.bits)

    def __mul__(self, scalar):
        return Bits(self.bits * scalar)

    def to_bytes(self):
        # Pad bits to make full bytes
        padded = self.bits[:]
        while len(padded) % 8 != 0:
            padded.insert(0, False)
        byte_array = bytearray()
        for i in range(0, len(padded), 8):
            byte = 0
            for bit in padded[i:i+8]:
                byte = (byte << 1) | int(bit)
            byte_array.append(byte)
        return bytes(byte_array)
