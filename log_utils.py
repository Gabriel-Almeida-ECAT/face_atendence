import os
import datetime


def scan_log(log_path: str, msg: str) -> None:
    with open(log_path, 'a') as log_file:
        try:
            log_file.write(msg)
        except:
            print("Error writing in log file")


def main() -> None:
    pass

if __name__ == '__main__':
    main()