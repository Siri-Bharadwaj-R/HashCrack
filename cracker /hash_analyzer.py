import re

HEX_RE = re.compile(r"^[0-9a-fA-F]+$")

def detect_hash_type(hash_value: str):
    """
    Very simple hash type fingerprinting based on length and prefix.
    Not perfect, but good enough for a student/offsec tool.
    """
    h = hash_value.strip()

    info = {
        "likely_type": "Unknown",
        "category": "Unknown",
        "length": len(h),
        "details": [],
        "recommended_attack": "Dictionary + Smart",
        "difficulty": "Unknown",
    }

    # bcrypt: $2a$, $2b$, $2y$...
    if h.startswith(("$2a$", "$2b$", "$2y$", "$2x$")):
        info["likely_type"] = "bcrypt"
        info["category"] = "Slow, salted password hash"
        info["difficulty"] = "Very hard (designed to resist cracking)"
        info["details"].append("bcrypt format detected (salt + cost factor included).")
        info["recommended_attack"] = "Targeted wordlist; offline cracking with GPU tools (e.g. hashcat)."
        return info

    # Argon2: $argon2id$, $argon2i$, $argon2d$
    if h.startswith(("$argon2id$", "$argon2i$", "$argon2d$")):
        info["likely_type"] = "Argon2"
        info["category"] = "Modern slow, salted hash"
        info["difficulty"] = "Very hard (state of the art)"
        info["details"].append("Argon2 format detected (memory-hard password hash).")
        info["recommended_attack"] = "Specialized GPU tools; not feasible with naive Python code."
        return info

    # PBKDF2 (common encodings, e.g. Django-style or hex)
    if "pbkdf2" in h.lower():
        info["likely_type"] = "PBKDF2"
        info["category"] = "Slow, salted key derivation"
        info["difficulty"] = "Hard"
        info["details"].append("PBKDF2 marker found (likely salted with many iterations).")
        info["recommended_attack"] = "Dictionary + rule-based attacks with GPU tools."
        return info

    # now heuristic by length & hex-ness
    length = len(h)
    is_hex = bool(HEX_RE.match(h))

    info["length"] = length

    if is_hex:
        if length == 32:
            info["likely_type"] = "MD5"
            info["category"] = "Fast, unsalted"
            info["difficulty"] = "Easy to moderate"
            info["details"].append("32 hex chars → typical MD5.")
            info["recommended_attack"] = "Dictionary + Smart + Rules. Brute-force for short passwords."
        elif length == 40:
            info["likely_type"] = "SHA-1"
            info["category"] = "Fast, unsalted"
            info["difficulty"] = "Moderate"
            info["details"].append("40 hex chars → typical SHA-1.")
            info["recommended_attack"] = "Dictionary + Smart with large wordlists."
        elif length == 64:
            info["likely_type"] = "SHA-256"
            info["category"] = "Fast, unsalted"
            info["difficulty"] = "Hard for brute-force"
            info["details"].append("64 hex chars → typical SHA-256.")
            info["recommended_attack"] = "Large curated wordlists + rules; smart attack."
        elif length == 128:
            info["likely_type"] = "SHA-512"
            info["category"] = "Fast, unsalted"
            info["difficulty"] = "Very hard for brute-force"
            info["details"].append("128 hex chars → typical SHA-512.")
            info["recommended_attack"] = "Only realistic with huge wordlists & rules."
        else:
            info["likely_type"] = "Unknown hex hash"
            info["category"] = "Unknown (hex)"
            info["difficulty"] = "Unknown"
            info["details"].append(f"Hex hash with length {length}. Could be custom or salted.")
    else:
        info["details"].append("Non-hex / custom structured hash (may be salted, encoded, or application-specific).")
        info["difficulty"] = "Unknown / structure-dependent"

    return info
