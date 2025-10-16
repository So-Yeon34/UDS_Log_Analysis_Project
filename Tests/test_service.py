from read_ascii_log import read_asc
import pytest
from pathlib import Path

@pytest.fixture(scope="session") #Function, Class, Module, Session (Only one time execute)
def _load_frames():
    log_path = Path(__file__).resolve().parent.parent / "logs" / "log.asc"
    print(f"[_load_frame] using log: {log_path}")

    if not log_path.exists():
        pytest.fail(f"Log file doesn't exist in the directory: {log_path}")

    data = read_asc(str(log_path))
    assert data, "Parsing frame is empty (Empty file or skipped)"
    return data

# (Step1) Check Session Control $10
def test_check_session_control(_load_frames):
    req = []
    res = []

    for fr in _load_frames:
        data = fr.data_hex.replace(" ", "").upper()
        if len(data) < 4:
            continue

        second_byte = data[2:4]
        third_byte = data[4:6]

        if second_byte == "10" and third_byte == "03" and fr.can_id.upper() == "7DF":
            req.append(fr)
        elif second_byte == "50" and third_byte == "03" and fr.can_id.upper() == "7E8":
            res.append(fr)

    assert req, "There is no request for session control (0x10)"
    assert res, "There is no positive response for session control (0x50)"

    for request in req:
        resp_found = any(
            (respond.t_ms > request.t_ms) and ((respond.t_ms - request.t_ms) <= 300)
            for respond in res
        )
        assert resp_found, f"There is no response within 300ms after {request.t_ms}ms"

# (Step2) Check Security Access $27
def test_check_security_access(_load_frames):
    pass

# (Step3) Check ReadByDataIdentifier $22
def test_check_readByIdentifier(_load_frames):
    pass

# (Step4) Check WriteByDataIdentifier $2E
def test_check_writeByIdentifier(_load_frames):
    pass

# (Step5) Check Routine Control $31
def test_check_routine_control(_load_frames):
    pass

# (Step6) Check Communication Control $28
def test_check_communication_control(_load_frames):
    pass

# (Step7) Check Clear DTC $14
def test_check_clear_dtc(_load_frames):
    pass

# (Step8) Check Read DTC $19
def test_check_read_dtc(_load_frames):
    pass

