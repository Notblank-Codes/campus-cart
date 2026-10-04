from datetime import datetime
from functools import wraps

transaction_logs = []


def log_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{timestamp}] Starting: {func.__name__}")

        try:
            result = func(*args, **kwargs)

            log_entry = {
                "function": func.__name__,
                "timestamp": timestamp,
                "status": "completed"
            }

            transaction_logs.append(log_entry)

            print(f"[{timestamp}] Completed: {func.__name__}")

            return result

        except Exception as error:
            log_entry = {
                "function": func.__name__,
                "timestamp": timestamp,
                "status": "failed",
                "error": str(error)
            }

            transaction_logs.append(log_entry)

            print(f"[{timestamp}] Failed: {func.__name__}")

            raise

    return wrapper

def get_audit_summary(logs):
    completed = list(filter(lambda log: log["status"] == "completed", logs))
    failed = list(filter(lambda log: log["status"] == "failed", logs))

    return {
        "total_transactions": len(logs),
        "completed": len(completed),
        "failed": len(failed)
    }

