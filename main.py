from datetime import datetime


PROJECT_NAME = "CyberForge Security Lab"
VERSION = "1.0.0"


def show_status():
    print("=" * 40)
    print(f"🛡️ {PROJECT_NAME}")
    print(f"📦 Version: {VERSION}")
    print(f"🕒 Time: {datetime.now()}")
    print("🔐 Security Lab: READY")
    print("=" * 40)


def main():
    show_status()


if __name__ == "__main__":
    main()
