import datetime

def add_log_entry(session_state, log_message: str):
    """
    Adds a timestamped entry to the session state cleaning audit log.
    """
    if "cleaning_log" not in session_state:
        session_state["cleaning_log"] = []
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_log = f"[{timestamp}] {log_message}"
    session_state["cleaning_log"].append(formatted_log)
    return formatted_log

def clear_logs(session_state):
    """Clears all audit logs in session state."""
    session_state["cleaning_log"] = []