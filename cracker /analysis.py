import math
import re

def _format_time(seconds: float) -> str:
    if seconds <= 0:
        return "N/A"
    if seconds < 1:
        return "< 1 second"

    units = [
        ("seconds", 60),
        ("minutes", 60),
        ("hours", 24),
        ("days", 365),
        ("years", 100),
    ]

    value = float(seconds)
    name = "seconds"

    for name, factor in units:
        if value < factor:
            break
        value /= factor

    return f"{value:.2f} {name}"

def analyze_password(password: str):
    length = len(password)
    uses_lower = any(c.islower() for c in password)
    uses_upper = any(c.isupper() for c in password)
    uses_digits = any(c.isdigit() for c in password)
    uses_symbols = any(not c.isalnum() for c in password)

    charset_size = 0
    if uses_lower:
        charset_size += 26
    if uses_upper:
        charset_size += 26
    if uses_digits:
        charset_size += 10
    if uses_symbols:
        charset_size += 32  # rough estimate of printable symbols

    if charset_size > 0:
        entropy_bits = round(length * math.log2(charset_size), 2)
    else:
        entropy_bits = 0.0

    if entropy_bits < 28:
        strength = "Very Weak"
    elif entropy_bits < 36:
        strength = "Weak"
    elif entropy_bits < 60:
        strength = "Reasonable"
    elif entropy_bits < 80:
        strength = "Strong"
    else:
        strength = "Very Strong"

    guesses = (charset_size ** length) if charset_size > 0 else 0

    cpu_rate = 10**7   # 10M guesses/sec
    gpu_rate = 10**10  # 10B guesses/sec

    cpu_time = _format_time(guesses / cpu_rate) if guesses else "N/A"
    gpu_time = _format_time(guesses / gpu_rate) if guesses else "N/A"

    patterns = []
    if re.search(r"(123|1234|12345)$", password):
        patterns.append("Ends with common number pattern (123, 1234, ...)")
    if re.search(r"(19|20)\d{2}", password):
        patterns.append("Contains a year-like pattern (19xx or 20xx)")
    if password.lower() in ["password", "admin", "qwerty", "letmein"]:
        patterns.append("Matches a very common leaked password")
    if password.isalpha():
        patterns.append("Uses only letters (no digits or symbols)")
    if password.isdigit():
        patterns.append("Uses only digits")
    if len(set(password)) <= 3:
        patterns.append("Very low character variety")

    return {
        "length": length,
        "entropy": entropy_bits,
        "strength": strength,
        "cpu_time": cpu_time,
        "gpu_time": gpu_time,
        "uses_lower": uses_lower,
        "uses_upper": uses_upper,
        "uses_digits": uses_digits,
        "uses_symbols": uses_symbols,
        "patterns": patterns,
    }
