from bits import Bits

class LFSR:
    """Linear Feedback Shift Register (LFSR) implementation."""

    def __init__(self, poly, state=None):
        self.poly = set(poly)
        self.length = max(self.poly)
        if state is None:
            self.state = Bits([True] * self.length)
        else:
            self.state = Bits(state)
            if len(self.state) < self.length:
                # If the state was shorter, we put zeros
                padding = [False] * (self.length - len(self.state))
                self.state = Bits(padding + self.state.bits)
        self.output = self.state[0]
        self.feedback = False

    def __iter__(self):
        return self

    def __str__(self):
        return f"LFSR(poly={self.poly}, state={self.state})"

    def __next__(self):
        # Save the current output
        self.output = self.state[0]
        
        # Calculate feedback bit
        feedback_bit = self.state[0]
        for i in range(1, self.length):
            if (self.length - i) in self.poly:
                feedback_bit ^= self.state[i]
        
        # Shift
        for i in range(self.length - 1):
            self.state[i] = self.state[i + 1]
        
        self.state[-1] = feedback_bit
        self.feedback = feedback_bit
        
        return self.output

    def run_steps(self, N=1, state=None):
        if state is not None:
            self.state = Bits(state)
            if len(self.state) < self.length:
                padding = [False] * (self.length - len(self.state))
                self.state = Bits(padding + self.state.bits)
        output_bits = []
        for _ in range(N):
            output_bits.append(next(self))
        return Bits(output_bits)

    def cycle(self, state=None):
        if state is not None:
            saved_state = self.state
            self.state = Bits(state)
        else:
            saved_state = Bits(self.state.bits)  # Copy from state

        seen_states = set()
        output_bits = []
        while True:
            state_tuple = tuple(self.state.bits)
            if state_tuple in seen_states:
                break
            seen_states.add(state_tuple)
            output_bits.append(next(self))

        # Returning initial state
        self.state = saved_state
        return Bits(output_bits)

def berlekamp_massey(bits):
    """
    Implementation of the Berlekamp-Massey algorithm.
    Input: bits (Bits) - observed bit sequence
    Output: poly (set) - set of degrees of the shortest LFSR polynomial
    """
    n = len(bits)
    c = [0] * n  # connection polynomial coefficients
    b = [0] * n
    c[0] = 1
    b[0] = 1
    l = 0  # current LFSR length
    m = -1  # last update position

    for i in range(n):
        # Compute discrepancy
        d = bits[i]
        for j in range(1, l + 1):
            d ^= (c[j] & bits[i - j])

        if d == 1:
            t = c.copy()
            for j in range(i - m, n):
                c[j] ^= b[j - (i - m)]
            if 2 * l <= i:
                l = i + 1 - l
                m = i
                b = t

    # Build the set of degrees from c
    poly = set()
    for i, coeff in enumerate(c[:l+1]):
        if coeff:
            poly.add(l - i)

    return poly
