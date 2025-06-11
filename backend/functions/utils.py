from passlib.hash import bcrypt
import csv
from datetime import datetime
from pathlib import Path
from config import LOG_FOLDER_PATH

def hash_password(plain_password: str) -> str:
    return bcrypt.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

def log_event(level: str, event_type: str, username: str, message: str):
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_file_path = Path(LOG_FOLDER_PATH+"/"+today+"_event_log.csv")
    log_file_path.touch(exist_ok=True) # Create file if it doesn't exist

    with open(log_file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            level.upper(),
            event_type,
            username,
            message
        ])