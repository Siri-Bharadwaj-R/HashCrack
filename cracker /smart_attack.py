from .hashing import compute_hash
from .builtin_wordlist import COMMON_WORDS


LEET_MAP = {"a": "@", "i": "1", "e": "3", "o": "0", "s": "$"}
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025"]
SUFFIXES = ["1", "12", "123", "1234", "!", "@123", "007"] + YEARS

def generate_variants(word: str):
    """
    Generate smarter variants for a base word:
    - base / reverse / capitalize / UPPER
    - appended suffixes (years, 123, 007, etc.)
    - leet versions + suffixes
    - doubled word
    """
    word = word.strip()
    base = word.lower()

    variants = set()
    if not base:
        return []

    # Base forms
    variants.add(base)
    variants.add(base[::-1])
    variants.add(base.capitalize())
    variants.add(base.upper())

    # Append suffixes
    for suf in SUFFIXES:
        variants.add(base + suf)
        variants.add(base.capitalize() + suf)

    # Leet versions
    leet = "".join(LEET_MAP.get(c, c) for c in base)
    variants.add(leet)
    for suf in SUFFIXES:
        variants.add(leet + suf)

    # Double word
    variants.add(base + base)

    return list(variants)

def smart_attack(target_hash: str, algo: str, wordlist=None, base_word=None):
    """
    Smart attack:
    - Use built-in COMMON_WORDS (or uploaded wordlist)
    - Plus an optional user-provided base word
    - Generate many variants for each base word and test them
    """
    candidates = []

    # Built-in / file wordlist
    if wordlist:
        candidates.extend(wordlist)
    else:
        candidates.extend(COMMON_WORDS)

    # User base word at the end
    if base_word:
        candidates.append(base_word.strip())

    # Unique base words
    seen = set()
    base_words = []
    for w in candidates:
        w = w.strip()
        if w and w not in seen:
            seen.add(w)
            base_words.append(w)

    # Try all variants
    for word in base_words:
        for variant in generate_variants(word):
            if compute_hash(variant, algo) == target_hash:
                return variant

    return None
