from read_ascii_log import read_asc

# (Step1) Log file validity check
def test_log_file_is_not_empty():
    frames = read_asc("logs/log.asc")
    assert len(frames) > 0, "File may be empty or all skipped"

# (Step2) Check Session Control $10
def test_check_session_control():
    pass

# (Step3) Check Security Access $27
def test_check_security_access():
    pass

# (Step4) Check ReadByDataIdentifier $22
def test_check_readByIdentifier():
    pass

# (Step5) Check WriteByDataIdentifier $2E
def test_check_writeByIdentifier():
    pass

# (Step6) Check Routine Control $31
def test_check_routine_control():
    pass

# (Step7) Check Communication Control $28
def test_check_communication_control():
    pass

# (Step8) Check Clear DTC $14
def test_check_clear_dtc():
    pass

# (Step9) Check Read DTC $19
def test_check_read_dtc():
    pass

