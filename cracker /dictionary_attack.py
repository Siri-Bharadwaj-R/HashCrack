from .hashing import compute_hash
from .builtin_wordlist import COMMON_WORDS

def dictionary_attack(target_hash: str, algo: str, wordlist=None):
    """
    Dictionary attack.
    Falls back to built-in COMMON_WORDS when:
    - no file uploaded
    - empty file
    - file with only blank lines
    """
    if (
        wordlist is None or
        len(wordlist) == 0 or
        (len(wordlist) == 1 and not wordlist[0].strip())
    ):
        wordlist = COMMON_WORDS

    for word in wordlist:
        w = word.strip()
        if not w:
            continue
        if compute_hash(w, algo) == target_hash:
            return w

    return None
