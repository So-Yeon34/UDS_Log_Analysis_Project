from dataclasses import dataclass
from typing import Optional, List
import re

SKIP_PREFIXES = {
    "//", "date", "Date", "base", "Base",
    "Begin", "End", "Warning", "ERROR", "Error",
}

HEX_ID_RE = re.compile(r"^[0-9A-Fa-f]{3,8}$")

@dataclass
class AscFrame:
    t_ms: int
    can_id: str
    direction: str # Rx, Tx
    dlc: int
    data_hex: str # Real Data

def _is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

def _find_can_id(parts: List[str]) -> Optional[str]:
    # It is normally contained in parts[2], but search for Hex format
    for p in parts[:8]: # Check only for front side data
        if HEX_ID_RE.match(p):
            return p.upper()
    return None

def parse_asc_line(line: str) -> Optional[AscFrame]:
    raw = line.strip()
    if not raw:
        return None
    if any(raw.startswith(pref) for pref in SKIP_PREFIXES):
        return None

    parts = raw.split()
    # Check minimum token (timestamp, channel, ID, data format)
    if len(parts)<4:
        return None

    # (Step1) Timestamp
    try:
        t_s = float(parts[0])
    except ValueError:
        return None
    t_ms = int(round(t_s*1000))

    # (Step2) CAN ID
    can_id = _find_can_id(parts)
    if not can_id:
        return None

    # (Step3) Direction
    direction = ""
    for tok in parts:
        if tok in ("Rx", "Tx"):
            direction = tok
            break

    # (Step4) Frame Type & DLC
    # It has the pattern "...Rx d 8 <data>". the integer number behind 'd' or 'r' means DLC
    dlc = None
    data_start_idx = None

    for i, tok in enumerate(parts):
        if tok in ("d", "r", "D", "R"):
            if i+1 < len(parts) and _is_int(parts[i+1]):
                candidate = int(parts[i+1])
                if 0<= candidate <=8:
                    dlc = candidate
                    data_start_idx = i+2
                    break
    if dlc is None:
        # In case that dlc comes out without 'd'
        for i in range(4, min(len(parts), 10)):
            if _is_init(parts[i]):
                candidate = int(parts[i])
                if 0<= candidate <=8:
                    dlc = candidate
                    data_start_idx = i+1
                    break
    if dlc is None:
        return None

    # (Step5) Gathering the data bytes
    if data_start_idx is None or data_start_idx + dlc > len(parts):
        return None

    data_bytes = parts[data_start_idx:data_start_idx + dlc]

    #Data byte normal has 2 characters, but add protective code just in case
    norm = []
    for b in data_bytes:
        b2 = b.strip().upper()
        if not re.match(r"^[0-9A-F]{1,2}$", b2):
            return None
        if len(b2)==1:
            b2 = "0" + b2
        norm.append(b2)
    data_hex = "".join(norm)

    return AscFrame(t_ms=t_ms, can_id=can_id, direction=direction, dlc=dlc, data_hex=data_hex)

def read_asc(path: str) -> List[AscFrame]:
    out: List[AscFrame] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            fr = parse_asc_line(line)
            if fr:
                out.append(fr)
    out.sort(key=lambda x: x.t_ms)
    return out

frames = read_asc("logs/log.asc")
for fr in frames:
    print(fr.t_ms, fr.can_id, fr.direction, fr.dlc, fr.data_hex)
