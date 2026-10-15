# Lab 5: Static Code Analysis

## Issues Identified and Fixed

| Issue | Type | Original Finding | Fix Applied |
|---|---|---|---|
| Binding to all network interfaces | Security | Bandit B104 | Changed `0.0.0.0` to `127.0.0.1` for local-only access. |
| Hardcoded moderator password | Security | Bandit B105 | Replaced the hardcoded password with an environment variable. |
| Standard pseudo-random selection | Security review | Bandit B311 | Used `secrets.choice()` for secure random selection. |
| Weak MD5 hash | Security | Bandit B324 | Replaced MD5 with SHA-256. |
| Missing docstrings | Code quality | Pylint C0114, C0116 | Added module and function docstrings. |
| Naming convention violations | Code quality | Pylint C0103 | Converted names to `snake_case`. |
| Unnecessary else after return | Code quality | Pylint R1705 | Removed the unnecessary else block. |
| Global statement | Code quality | Pylint W0603 | Removed global variable mutation. |
| Loop style | Code quality | Pylint C0200 | Used `enumerate()`. |
| Spacing and final newline | Formatting | Flake8 | Fixed whitespace and added the final newline. |

## Final Results

- Pylint: 10.00/10
- Bandit: No issues identified.
- Flake8: No violations reported.