log_path = "logs/log.txt"

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip() #\n remove
        if not line:
            continue #ingnore blank line

        parts = line.split(",") #distinguish by ","
        print(parts)
    print("Run txt import")