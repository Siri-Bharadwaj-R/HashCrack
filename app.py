from flask import Flask, render_template, request
import time
import hashlib

from cracker.dictionary_attack import dictionary_attack
from cracker.brute_force import brute_force_attack
from cracker.rules_attack import rules_attack
from cracker.smart_attack import smart_attack
from cracker.analysis import analyze_password
from cracker.normalize import normalize_string
from cracker.hash_analyzer import detect_hash_type

app = Flask(__name__)

# -------------------------
# DASHBOARD
# -------------------------
@app.route("/dashboard")
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# -------------------------
# CRACK A HASH
# -------------------------
@app.route("/crack", methods=["GET", "POST"])
def crack():
    if request.method == "POST":

        raw_hash = request.form["hash"]
        algo = request.form["algo"]
        attack_type = request.form["attack"]
        base_word_raw = request.form.get("base_word", "")

        raw_hash = raw_hash.strip()
        base_word_raw = base_word_raw.strip()

        # Normalize
        hash_value, hash_warnings = normalize_string(raw_hash)
        base_word, base_warnings = normalize_string(base_word_raw)

        # Wordlist (optional)
        wordlist_file = request.files.get("wordlist")
        wordlist = None

        if wordlist_file and wordlist_file.filename:
            text = wordlist_file.read().decode(errors="ignore")
            lines = text.splitlines()
            wordlist = []
            for w in lines:
                norm, warn = normalize_string(w)
                wordlist.append(norm)

        # Start attack timer
        start = time.time()

        if attack_type == "dictionary":
            result = dictionary_attack(hash_value, algo, wordlist)
        elif attack_type == "bruteforce":
            result = brute_force_attack(hash_value, algo)
        elif attack_type == "rules":
            result = rules_attack(hash_value, algo, wordlist)
        elif attack_type == "smart":
            result = smart_attack(hash_value, algo, wordlist, base_word)
        else:
            result = None

        end = time.time()
        time_taken = round(end - start, 4)

        # Password analysis (only if found)
        analysis = None
        if isinstance(result, str) and result:
            analysis = analyze_password(result)

        all_warnings = hash_warnings + base_warnings

        return render_template(
            "result.html",
            result=result,
            time=time_taken,
            analysis=analysis,
            warnings=all_warnings,
        )

    return render_template("crack.html")


# -------------------------
# HASH ANALYZER (HashID-style)
# -------------------------
@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        raw_hash = request.form["hash_to_analyze"].strip()
        normalized, warnings = normalize_string(raw_hash)
        info = detect_hash_type(normalized)

        return render_template(
            "analyze.html",
            hash_value=normalized,
            info=info,
            warnings=warnings,
        )

    return render_template("analyze.html", hash_value=None, info=None, warnings=[])


# -------------------------
# PASSWORD STRENGTH AUDIT
# -------------------------
@app.route("/audit", methods=["GET", "POST"])
def audit():
    if request.method == "POST":
        password = request.form["password"]
        analysis = analyze_password(password)
        return render_template("audit.html", password=password, analysis=analysis)

    return render_template("audit.html", password=None, analysis=None)


# -------------------------
# HASH GENERATOR (NEW)
# -------------------------
@app.route("/generator", methods=["GET", "POST"])
def generator():
    hashes = None
    text = ""
    warnings = []

    if request.method == "POST":
        text_raw = request.form.get("text_input", "")
        text, norm_warn = normalize_string(text_raw)
        warnings.extend(norm_warn)

        if text:
            hashes = {
                "MD5": hashlib.md5(text.encode()).hexdigest(),
                "SHA1": hashlib.sha1(text.encode()).hexdigest(),
                "SHA256": hashlib.sha256(text.encode()).hexdigest(),
                "SHA512": hashlib.sha512(text.encode()).hexdigest(),
            }

    return render_template("generator.html", hashes=hashes, text=text, warnings=warnings)


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
