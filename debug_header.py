import csv

with open('data/Election_Data/02gov-aligned.csv', 'r') as f:
    csv_reader = csv.reader(f, skipinitialspace=True)
    header = next(csv_reader)
    
    print("Header row:")
    for i, field in enumerate(header):
        print(f"  [{i}]: {repr(field)}")
    
    print("\nExtracting candidate info:")
    for i in range(1, len(header)):
        if header[i] and 'TOTAL' not in header[i].upper():
            text = header[i].replace('\n', ' ').replace('\r', ' ').strip()
            text = ' '.join(text.split())
            print(f"  Field {i}: {repr(text)}")
            
            # Try to extract candidate and party
            import re
            match = re.search(r'([A-Za-z\s\.\']+)\(([A-Z])\)', text)
            if match:
                name = match.group(1).strip()
                party = match.group(2)
                print(f"    -> Name: {name}, Party: {party}")
            else:
                print(f"    -> NO MATCH")
