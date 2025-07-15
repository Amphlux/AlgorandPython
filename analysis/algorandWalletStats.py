from algosdk import account, mnemonic
from collections import defaultdict

def analyze_first_character():
    print("Analyzing first character of Algorand addresses...")
    print("Checking 100,000 addresses")
    
    # Track first characters
    first_chars = defaultdict(int)
    total = 100_000
    
    for i in range(total):
        _, address = account.generate_account()
        first_char = address[0]
        first_chars[first_char] += 1
    
    # Print sorted results
    print("\nFirst character frequencies:")
    print("-" * 50)
    for char, count in sorted(first_chars.items(), key=lambda x: x[1], reverse=True):
        percentage = (count/total) * 100
        print(f"{char}: {count} times ({percentage:.2f}%)")
    
    # Print summary
    print("\nSummary:")
    print("-" * 50)
    print(f"Total characters found: {len(first_chars)}")
    print(f"Expected count per character if uniform: {total/32:.1f}")
    print("\nFound characters:", ", ".join(sorted(first_chars.keys())))
    
    # Check if any valid characters are never seen
    all_valid = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
    missing = all_valid - set(first_chars.keys())
    if missing:
        print("\nMissing characters:", ", ".join(sorted(missing)))
    else:
        print("\nAll valid characters (A-Z, 2-7) appear as first characters")
    
    # Calculate deviation from expected uniform distribution
    expected = total/32
    max_deviation = max(abs(count - expected) for count in first_chars.values())
    print(f"\nMaximum deviation from expected: {max_deviation:.1f} ({(max_deviation/expected)*100:.1f}%)")

if __name__ == "__main__":
    analyze_first_character()
