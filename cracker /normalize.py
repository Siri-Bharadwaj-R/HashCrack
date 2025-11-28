import unicodedata

# Maps full-width Unicode symbols to ASCII equivalents
UNICODE_MAP = {
    "＠": "@",
    "！": "!",
    "＃": "#",
    "＄": "$",
    "％": "%",
    "＾": "^",
    "＆": "&",
    "＊": "*",
    "（": "(",
    "）": ")",
}

def normalize_string(s: str):
    """
    Normalizes password/hash inputs by:
    - converting full-width Unicode characters to ASCII
    - performing Unicode NFKC normalization
    - returning (normalized_string, warnings_list)
    """
    warnings = []

    # Step 1: Replace known full-width forms
    normalized = ""
    for ch in s:
        if ch in UNICODE_MAP:
            warnings.append(f"Converted full-width '{ch}' to '{UNICODE_MAP[ch]}'")
            normalized += UNICODE_MAP[ch]
        else:
            normalized += ch

    # Step 2: Apply universal normalization
    nfkc = unicodedata.normalize("NFKC", normalized)

    if nfkc != s:
        warnings.append("Unicode normalization changed the input.")

    return nfkc, warnings
