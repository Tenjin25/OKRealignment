import csv

# Read the problematic file
with open('data/Election_Data/02gov-aligned.csv', 'r') as f:
    lines = f.readlines()

print("=" * 60)
print("Testing CSV parsing for 02gov-aligned.csv")
print("=" * 60)

# Test line 3 (first data row)
test_line = lines[2].strip()
print(f"\nRaw line 3:\n{repr(test_line)}")

# Parse with csv.reader
parsed = list(csv.reader([test_line]))[0]
print(f"\nParsed with csv.reader: {len(parsed)} fields")
for i, field in enumerate(parsed[:6]):
    print(f"  Field {i}: {repr(field)}")

# Try with skipinitialspace=True
parsed2 = list(csv.reader([test_line], skipinitialspace=True))[0]
print(f"\nParsed with skipinitialspace=True: {len(parsed2)} fields")
for i, field in enumerate(parsed2[:6]):
    print(f"  Field {i}: {repr(field)}")
