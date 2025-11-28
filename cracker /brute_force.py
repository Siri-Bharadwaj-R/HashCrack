from itertools import product
from .hashing import compute_hash

# Charset: enough for typical short tests (lowercase + digits)
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789"

def brute_force_attack(target_hash: str, algo: str, max_len: int = 4):
    """
    Bruteforce attack for very short passwords (1..max_len).
    Tries all combinations from CHARSET.
    """
    for length in range(1, max_len + 1):
        for combo in product(CHARSET, repeat=length):
            word = "".join(combo)
            if compute_hash(word, algo) == target_hash:
                return word
    return None
