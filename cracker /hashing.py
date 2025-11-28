import hashlib

def compute_hash(word: str, algo: str) -> str:
    """
    Compute the hash of `word` using the selected algorithm.
    Supported: md5, sha1, sha256, sha512.
    """
    word = word.strip()

    if algo == "md5":
        return hashlib.md5(word.encode()).hexdigest()

    elif algo == "sha1":
        return hashlib.sha1(word.encode()).hexdigest()

    elif algo == "sha256":
        return hashlib.sha256(word.encode()).hexdigest()

    elif algo == "sha512":
        return hashlib.sha512(word.encode()).hexdigest()

    else:
        # If this ever happens, something is wrong with the form value
        raise ValueError(f"Invalid hash algo: {algo}")
