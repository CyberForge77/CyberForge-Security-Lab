import platform
import socket


def get_system_info():
    return {
        "نظام التشغيل": platform.system(),
        "إصدار النظام": platform.release(),
        "اسم الجهاز": socket.gethostname(),
        "إصدار Python": platform.python_version(),
    }


def display_system_info():
    print("\n🖥️ معلومات النظام")
    print("-" * 35)

    info = get_system_info()

    for name, value in info.items():
        print(f"{name}: {value}")
