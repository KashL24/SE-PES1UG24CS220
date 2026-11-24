# Lab 7 — Spam Scoring Filter
Install dependencies: `python -m pip install -r requirements.txt`.
Run the fixed application: `python spam_scoring.py`.
Run the required Hypothesis suite: `python -m pytest test_spam_scoring.py`.
Hypothesis could not be installed in the execution environment (network/DNS failure). The included screenshots show actual pytest fallback runs, not Hypothesis runs. To complete the required evidence locally, install dependencies and run the Hypothesis suite against the original and fixed versions (use a temporary directory with the original renamed to spam_scoring.py and a copy of test_spam_scoring.py). Capture both outputs.
Fallback: `python -m pytest test_edge_cases.py`. Three tests passed on the fixed version; three failed on the original. The fallback uses 300 seeded random strings plus nine explicit inputs per function, and additional assertions. The original file is included for reproduction.
Return conventions: invalid email or missing link returns an empty string; undefined uppercase ratio returns 0.0. Email validation is basic, not full RFC validation; links are HTTP(S) tokens, not fully validated URLs.
