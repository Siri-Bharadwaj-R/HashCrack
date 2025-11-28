# HashCrack  
### A Modern Password Security Toolkit built with Python & Flask

HashCrack is a lightweight yet advanced cybersecurity toolkit that provides:

- Password hash cracking (MD5, SHA-1, SHA-256, SHA-512)  
- Automatic hash type detection  
- Password strength auditing  
- Instant hash generation  
- A clean neon-themed Flask UI  

---

## Features

### Hash Cracking Engine
Supports multiple attack strategies:
- Dictionary Attack  
- Rules-Based Attack  
- Smart Hybrid Attack (patterns, years, substitutions)  
- Brute Force (short passwords)

### Hash Type Analyzer
Identifies hash algorithms based on:
- Length  
- Hex signature  
- Structural patterns  

### Password Strength Audit
Provides:
- Entropy calculations  
- Character-set breakdown  
- Estimated crack time  
- Detection of weak or predictable patterns  

### Hash Generator
Generates:
- MD5  
- SHA-1  
- SHA-256  
- SHA-512  
for any input string.

---

## Project Structure

```
HashCrack/
│  app.py
│  requirements.txt
│  README.md
│
├── cracker/                  # Attack engines and utilities
│     ├── hashing.py
│     ├── dictionary_attack.py
│     ├── brute_force.py
│     ├── rules_attack.py
│     ├── smart_attack.py
│     └── __init__.py
│
├── templates/                # Frontend HTML (UI)
│     ├── dashboard.html
│     ├── crack.html
│     ├── analyze.html
│     ├── audit.html
│     └── generator.html
│
└── static/                   # Styling and assets
      └── style.css
```


---

## Running the Application

### Install dependencies:
pip install -r requirements.txt


### Start the Flask server:
python app.py


### Open in browser:
http://127.0.0.1:5000

---

## Responsible Use
This project is intended for learning, research, and authorized security testing only.  
Do not use it on systems or data without explicit permission.
