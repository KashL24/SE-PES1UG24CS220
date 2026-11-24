import re


def sender_domain(email):
    """Return the lowercase domain, or an empty string for invalid input."""
    if not isinstance(email, str) or email.count('@') != 1:
        return ''
    local, domain = email.strip().split('@')
    if not local or not domain or any(c.isspace() for c in local + domain):
        return ''
    return domain.lower()


def first_link(text):
    """Return the first HTTP(S) token, or an empty string."""
    if not isinstance(text, str):
        return ''
    match = re.search(r'https?://[^\s]+', text)
    return match.group(0) if match else ''


def shout_ratio(text):
    """Return the fraction of alphabetic characters that are uppercase."""
    if not isinstance(text, str):
        return 0.0
    letters = [c for c in text if c.isalpha()]
    return sum(c.isupper() for c in letters) / len(letters) if letters else 0.0


def main():
    print("==== Running sender_domain ====")
    user_input = input("Enter a sender email (e.g. offers@Deals.com): ")
    result = sender_domain(user_input)
    print("Sender Domain:", result)

    print("\n==== Running first_link ====")
    user_input = input("Enter a message containing a link: ")
    result = first_link(user_input)
    print("First Link:", result)

    print("\n==== Running shout_ratio ====")
    user_input = input("Enter a message (e.g. FREE prize NOW): ")
    result = shout_ratio(user_input)
    print("Uppercase Ratio:", result)

if __name__ == "__main__":
    main()
