from config import PROJECT_NAME, VERSION, DEVELOPER
from security_tools import check_password_strength
from system_info import display_system_info


def show_banner():
    print("=" * 50)
    print(f"🛡️ {PROJECT_NAME}")
    print(f"📦 Version: {VERSION}")
    print(f"👨‍💻 Developer: {DEVELOPER}")
    print("=" * 50)


def password_checker():
    print("\n🔐 فحص قوة كلمة المرور")
    password = input("أدخل كلمة مرور تجريبية: ")

    result = check_password_strength(password)

    print(f"\nنتيجة الفحص: {result}")


def main_menu():
    while True:
        print("\nاختر عملية:")
        print("1 - فحص قوة كلمة المرور")
        print("2 - معلومات النظام")
        print("0 - خروج")

        choice = input("\nاختيارك: ")

        if choice == "1":
            password_checker()

        elif choice == "2":
            display_system_info()

        elif choice == "0":
            print("تم إغلاق CyberForge Security Lab.")
            break

        else:
            print("❌ اختيار غير صحيح.")


def main():
    show_banner()
    main_menu()


if __name__ == "__main__":
    main()
