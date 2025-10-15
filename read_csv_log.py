import csv

log_path = "logs/log.csv"

with open(log_path, "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
    print("Run csv import")