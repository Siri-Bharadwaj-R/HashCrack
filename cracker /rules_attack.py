from .hashing import compute_hash
from .builtin_wordlist import COMMON_WORDS


def expand(word: str):
    """
    Generate rule-based variants of a base word:
    - case variants
    - reversed
    - appended suffixes (123, 2024, etc.)
    - basic leet substitutions
    - some special cases for very common words like 'password'
    """
    word = word.strip()
    base = word.lower()
    variants = set()

    if not base:
        return []

    # Basic forms
    variants.add(base)
    variants.add(base.capitalize())
    variants.add(base.upper())

    # Reverse
    variants.add(base[::-1])

    # Suffixes
    suffixes = ["1", "12", "123", "1234", "2024", "2025", "!", "@123", "007"]
    for suf in suffixes:
        variants.add(base + suf)
        variants.add(base.capitalize() + suf)

    # Leet substitutions
    leet_map = {"a": "@", "s": "$", "i": "1", "e": "3", "o": "0"}
    leet = "".join(leet_map.get(c, c) for c in base)
    variants.add(leet)

    for suf in suffixes:
        variants.add(leet + suf)

    # Special handling for the super-common 'password'
    if base == "password":
        # These are classic weak variants
        variants.add("p@ssword")
        variants.add("pa$$word")
        variants.add("p@$$word")

    return list(variants)

def rules_attack(target_hash: str, algo: str, wordlist=None):
    """
    Rules-based attack:
    Expand each base word (COMMON_WORDS or uploaded list) using expand().
    """
    if not wordlist:
        wordlist = COMMON_WORDS

    for word in wordlist:
        for variant in expand(word):
            if compute_hash(variant, algo) == target_hash:
                return variant

    return None
