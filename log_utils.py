import os
import datetime

os.makedirs(r'./logs/', exist_ok=True)
scan_log_path = './logs/scan_log.txt'
register_log_path = './logs/register_log.txt'

def scan_log(msg: str) -> None:
    with open(scan_log_path, 'a') as log_file:
        try:
            log_file.write(msg)
        except:
            print("Error writing in log file")


def register_log(msg: str) -> None:
    with open(register_log_path, 'a') as log_file:
        try:
            log_file.write(msg)
        except:
            print("Error writing in log file")


def main() -> None:
    pass

if __name__ == '__main__':
    main()