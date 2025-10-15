import os

def test_read_log_file():
    with open("logs/log.asc", "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("//"):
                continue
            parts = line.split()

            # (Step1) Check whether the file format is correct or not
            '''
            index   context         description
            0       0.00000         Timestamp (unit: sec)
            1       1               CAN channel (CAN1, CAN2...) 
            2       7DF             CAN ID
            3       RX/TX           Receive or Transmit
            4       d               data frame
            5       8               DLC (Data length, 0~8 byte, HSCAN)
            6~      02 10 03...     Real data byte  
            '''
            assert len(parts) >= 7, f"Invalid format: {line}"

            # (Step2) Check wheater the direction is correct or not
            assert parts[3] in ["Rx", "Tx"], f"Missing direction: {line}"

