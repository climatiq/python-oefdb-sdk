import csv

rows = [];

with open("oefdb-copy.csv", newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

with open("oefdb-formatted.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
