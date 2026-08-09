from datetime import datetime


LOG_FILE = "security_scan.log"


def save_scan(scan_type, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"[{timestamp}] {scan_type}: {result}\n"
        )


def show_logs():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            logs = file.read()

        if not logs:
            print("\nلا توجد فحوصات مسجلة.")

        else:
            print("\n📋 سجل الفحوصات")
            print("-" * 40)
            print(logs)

    except FileNotFoundError:
        print("\n📋 لا يوجد سجل فحوصات حتى الآن.")
