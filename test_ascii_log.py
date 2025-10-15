from read_ascii_log import read_asc

def test_log_file_is_not_empty():
    frames = read_asc("logs/log.asc")
    assert len(frames) > 0, "File may be empty or all skipped"