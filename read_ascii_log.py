import csv

log_path = "logs/log.asc"

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("//"):
            continue

        parts = line.split() # Split based on blank
        timestamp = float(parts[0])
        can_id = parts[2]
        direction = parts[3]
        dlc = int(parts[5])
        data_bytes = parts[6:6+dlc] # Slice the data by the number of data bytes

        print(timestamp, can_id, direction, data_bytes)