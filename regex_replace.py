import re
import sys

def unescape(s):
    """Interpret \n, \t, \\ and similar escape sequences."""
    return bytes(s, "utf-8").decode("unicode_escape")

def load_rules(filename):
    rules = []
    with open(filename, encoding="utf-8") as f:
        search = replace = None
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.strip().startswith("#"):
                continue
            if line.startswith("search:"):
                search = line.split("search:", 1)[1].strip()
            elif line.startswith("replace:"):
                replace = line.split("replace: ", 1)[1]
            # Append rule when both keys were seen, even if replace is empty
            if search is not None and replace is not None:
                rules.append((search, replace))
                search = replace = None
    return rules

def apply_rules(text, rules):
    for search, replace in rules:
        text = re.sub(search, replace, text, flags=re.MULTILINE)
    return text

def main():
    if len(sys.argv) != 4:
        print("Usage: python regex_replace.py <rules.txt> <input.txt> <output.txt>")
        sys.exit(1)

    rules_file, input_file, output_file = sys.argv[1:4]
    rules = load_rules(rules_file)

    with open(input_file, encoding="utf-8") as f:
        text = f.read()

    result = apply_rules(text, rules)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"✅ Applied {len(rules)} regex replacements and saved to {output_file}")

if __name__ == "__main__":
    main()
