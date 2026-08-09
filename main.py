from datetime import datetime
import re


PROJECT_NAME = "CyberForge Security Lab"
VERSION = "1.0.0"


def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1

    if score <= 2:
        return "ضعيفة"
    elif score <= 4:
        return "متوسطة"
    else:
        return "قوية"


def show_status():
    print("=" * 40)
    print(f"🛡️ {PROJECT_NAME}")
    print(f"📦 Version: {VERSION}")
    print(f"🕒 Time: {datetime.now()}")
    print("🔐 Security Lab: READY")
    print("=" * 40)


def main():
    show_status()

    print("\n🔐 Password Security Check")
    password = input("أدخل كلمة مرور للاختبار: ")

    result = check_password_strength(password)

    print(f"\nنتيجة الفحص: {result}")


if __name__ == "__main__":
    main()
