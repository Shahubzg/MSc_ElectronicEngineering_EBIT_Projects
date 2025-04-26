from lfsr import LFSR
from bits import Bits

class AlternatingStep:
    """Alternating-Step Generator using three LFSRs."""

    def __init__(self, seed=None, polyC=None, poly0=None, poly1=None):
        # If default polynomials aren't given
        if polyC is None:
            polyC = {5, 2, 0}  # x^5 + x^2 + 1
        if poly0 is None:
            poly0 = {3, 1, 0}  # x^3 + x + 1
        if poly1 is None:
            poly1 = {4, 1, 0}  # x^4 + x + 1

        # Calculating total length for seed
        lenC = max(polyC)
        len0 = max(poly0)
        len1 = max(poly1)
        total_len = lenC + len0 + len1

        if seed is None:
            seed_bits = Bits([True] * total_len)
        else:
            seed_bits = Bits(seed)
            if len(seed_bits) < total_len:
                padding = [False] * (total_len - len(seed_bits))
                seed_bits = Bits(padding + seed_bits.bits)

        # Dividing the seed between three LSFRs
        idx1 = lenC
        idx2 = lenC + len0
        self.lfsrC = LFSR(polyC, seed_bits.bits[:idx1])
        self.lfsr0 = LFSR(poly0, seed_bits.bits[idx1:idx2])
        self.lfsr1 = LFSR(poly1, seed_bits.bits[idx2:])

        self.output = False  # Initial Value

    def __iter__(self):
        return self

    def __next__(self):
        control_bit = next(self.lfsrC)
        if control_bit == 0:
            bit0 = next(self.lfsr0)
            bit1 = self.lfsr1.output  # Previous
        else:
            bit0 = self.lfsr0.output  # Previous
            bit1 = next(self.lfsr1)
        self.output = bit0 ^ bit1
        return self.output
