# -*- coding: utf-8 -*-

import os
import json
import socket
import platform
import threading
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8080

EVENT_FILE = "cyberforge_events.json"

events = []


# =========================
# أدوات النظام
# =========================

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "غير متاح"


def get_system_info():
    return {
        "hostname": platform.node() or "غير معروف",
        "system": platform.system() or "غير معروف",
        "release": platform.release() or "غير معروف",
        "machine": platform.machine() or "غير معروف",
        "python": platform.python_version(),
        "ip": get_ip(),
        "folder": os.getcwd()
    }


# =========================
# الأحداث
# =========================

def save_events():
    try:
        with open(EVENT_FILE, "w", encoding="utf-8") as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def load_events():
    global events

    try:
        with open(EVENT_FILE, "r", encoding="utf-8") as f:
            events = json.load(f)
    except Exception:
        events = []

    if not events:
        add_event(
            "INFO",
            "تم تشغيل CyberForge Security Monitor"
        )


def add_event(level, message):

    event = {
        "level": level,
        "message": message,
        "time": now()
    }

    events.insert(0, event)

    if len(events) > 100:
        del events[100:]

    save_events()


# =========================
# حماية النصوص
# =========================

def escape(text):

    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# =========================
# HTML
# =========================

def dashboard():

    info = get_system_info()

    alerts = 0
    warnings = 0

    for event in events:

        if event["level"] == "ALERT":
            alerts += 1

        elif event["level"] == "WARNING":
            warnings += 1

    rows = ""

    for event in events[:20]:

        level = event["level"]

        if level == "ALERT":
            badge = "red"

        elif level == "WARNING":
            badge = "orange"

        else:
            badge = "green"

        rows += f"""
        <tr>

            <td>
                <span class="badge {badge}">
                    {escape(level)}
                </span>
            </td>

            <td>
                {escape(event["message"])}
            </td>

            <td>
                {escape(event["time"])}
            </td>

        </tr>
        """

    return f"""
<!DOCTYPE html>

<html lang="ar" dir="rtl">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,initial-scale=1">

<meta http-equiv="refresh" content="30">

<title>
CyberForge Security Monitor
</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    background:
    #070b12;

    color: #f2f5f8;

    font-family:
    Arial, sans-serif;

}}

.container {{

    max-width:
    1150px;

    margin:
    auto;

    padding:
    20px;

}}

.header {{

    background:
    linear-gradient(
        135deg,
        #111b2b,
        #0b111c
    );

    border:
    1px solid #27364d;

    border-radius:
    22px;

    padding:
    25px;

    margin-bottom:
    18px;

}}

.header h1 {{

    margin:
    0 0 10px;

    font-size:
    28px;

}}

.subtitle {{

    color:
    #9aa8bc;

    line-height:
    1.8;

}}

.grid {{

    display:
    grid;

    grid-template-columns:
    repeat(
        auto-fit,
        minmax(
            210px,
            1fr
        )
    );

    gap:
    14px;

}}

.card {{

    background:
    #101826;

    border:
    1px solid #26354a;

    border-radius:
    17px;

    padding:
    20px;

}}

.label {{

    color:
    #8d9bb0;

    font-size:
    14px;

    margin-bottom:
    9px;

}}

.value {{

    font-size:
    22px;

    font-weight:
    bold;

}}

.small {{

    font-size:
    15px;

    word-break:
    break-all;

}}

.green {{

    color:
    #52e28b;

}}

.orange {{

    color:
    #ffc15b;

}}

.red {{

    color:
    #ff6b6b;

}}

.buttons {{

    display:
    flex;

    flex-wrap:
    wrap;

    gap:
    10px;

    margin:
    20px 0;

}}

button {{

    border:
    0;

    border-radius:
    12px;

    padding:
    13px 17px;

    color:
    white;

    background:
    #1976ff;

    font-size:
    14px;

}}

.alert-button {{

    background:
    #d63e4a;

}}

.warning-button {{

    background:
    #ad7400;

}}

.dark-button {{

    background:
    #263449;

}}

table {{

    width:
    100%;

    border-collapse:
    collapse;

    background:
    #101826;

    border:
    1px solid #26354a;

    border-radius:
    16px;

    overflow:
    hidden;

}}

th,
td {{

    padding:
    13px;

    text-align:
    right;

    border-bottom:
    1px solid #202b3c;

}}

th {{

    color:
    #9aa8bc;

}}

.badge {{

    display:
    inline-block;

    padding:
    5px 9px;

    border-radius:
    20px;

    font-size:
    12px;

}}

.badge.green {{

    background:
    #123b27;

}}

.badge.orange {{

    background:
    #493617;

}}

.badge.red {{

    background:
    #491e24;

}}

.footer {{

    text-align:
    center;

    color:
    #68758a;

    margin-top:
    25px;

    line-height:
    1.8;

}}

</style>

</head>


<body>


<div class="container">


<div class="header">

<h1>
🛡️ CyberForge Security Monitor
</h1>

<div class="subtitle">

مختبر المهندس عبدالكريم أحمد صالح علبهادي

<br>

منصة مراقبة أمنية — النسخة التجريبية الأولى

</div>

</div>


<!-- الإحصائيات -->

<div class="grid">


<div class="card">

<div class="label">
حالة النظام
</div>

<div class="value green">
🟢 يعمل
</div>

</div>


<div class="card">

<div class="label">
المراقبة
</div>

<div class="value green">
🟢 مفعلة
</div>

</div>


<div class="card">

<div class="label">
الأحداث
</div>

<div class="value">
{len(events)}
</div>

</div>


<div class="card">

<div class="label">
التنبيهات
</div>

<div class="value red">
{alerts}
</div>

</div>


</div>


<br>


<!-- معلومات الجهاز -->

<h2>
🖥️ الجهاز المراقب
</h2>


<div class="grid">


<div class="card">

<div class="label">
اسم الجهاز
</div>

<div class="value small">
{escape(info["hostname"])}
</div>

</div>


<div class="card">

<div class="label">
نظام التشغيل
</div>

<div class="value small">

{escape(info["system"])}

<br>

{escape(info["release"])}

</div>

</div>


<div class="card">

<div class="label">
المعمارية
</div>

<div class="value small">
{escape(info["machine"])}
</div>

</div>


<div class="card">

<div class="label">
Python
</div>

<div class="value small">
{escape(info["python"])}
</div>

</div>


<div class="card">

<div class="label">
عنوان الشبكة المحلي
</div>

<div class="value small">
{escape(info["ip"])}
</div>

</div>


</div>


<!-- الأزرار -->

<div class="buttons">


<form method="post"
action="/alert">

<button class="alert-button">

🚨 تنبيه تجريبي

</button>

</form>


<form method="post"
action="/warning">

<button class="warning-button">

⚠️ تحذير تجريبي

</button>

</form>


<form method="post"
action="/scan">

<button>

🔍 فحص النظام

</button>

</form>


<form method="post"
action="/clear">

<button class="dark-button">

🧹 مسح السجل

</button>

</form>


<form method="get"
action="/">

<button>

🔄 تحديث

</button>

</form>


</div>


<!-- الأحداث -->

<h2>
📋 سجل الأحداث الأمنية
</h2>


<table>

<thead>

<tr>

<th>
المستوى
</th>

<th>
الحدث
</th>

<th>
الوقت
</th>

</tr>

</thead>


<tbody>

{rows}

</tbody>

</table>


<!-- معلومات -->

<div class="card"
style="margin-top:18px">


<div class="label">
حالة المشروع
</div>

<div>

🟢 الواجهة تعمل

<br>

🟢 تسجيل الأحداث يعمل

<br>

🟢 حفظ السجل يعمل

<br>

🟡 المراقبة المتقدمة قيد التطوير

</div>


</div>


<div class="footer">

CyberForge77

<br>

المهندس عبدالكريم أحمد صالح علبهادي

<br>

نسخة تجريبية تعليمية تعمل محليًا

</div>


</div>


</body>

</html>
"""


# =========================
# فحص تجريبي
# =========================

def local_scan():

    info = get_system_info()

    add_event(
        "INFO",
        "بدأ فحص النظام المحلي"
    )

    add_event(
        "INFO",
        f"نظام التشغيل: {info['system']} {info['release']}"
    )

    add_event(
        "INFO",
        f"عنوان الشبكة المحلي: {info['ip']}"
    )

    add_event(
        "INFO",
        "انتهى الفحص المحلي بنجاح"
    )


# =========================
# الخادم
# =========================

class SecurityServer(BaseHTTPRequestHandler):


    def log_message(self, format, *args):
        pass


    def send_page(self):

        data = dashboard().encode(
            "utf-8"
        )

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(data))
        )

        self.end_headers()

        self.wfile.write(data)


    def redirect_home(self):

        self.send_response(303)

        self.send_header(
            "Location",
            "/"
        )

        self.end_headers()


    def do_GET(self):

        if self.path == "/":

            self.send_page()

        else:

            self.send_response(404)

            self.end_headers()


    def do_POST(self):

        if self.path == "/alert":

            add_event(
                "ALERT",
                "تم اكتشاف نشاط أمني تجريبي"
            )

            self.redirect_home()


        elif self.path == "/warning":

            add_event(
                "WARNING",
                "تم تسجيل تحذير أمني تجريبي"
            )

            self.redirect_home()


        elif self.path == "/scan":

            local_scan()

            self.redirect_home()


        elif self.path == "/clear":

            events.clear()

            add_event(
                "INFO",
                "تم تنظيف سجل الأحداث"
            )

            self.redirect_home()


        else:

            self.send_response(404)

            self.end_headers()


# =========================
# التشغيل
# =========================

def open_browser():

    try:

        webbrowser.open(
            f"http://{HOST}:{PORT}"
        )

    except Exception:

        pass


def main():

    load_events()

    print()
    print("=" * 60)

    print(
        "🛡️ CYBERFORGE SECURITY MONITOR"
    )

    print(
        "مختبر المهندس عبدالكريم أحمد صالح علبهادي"
    )

    print("=" * 60)

    print()

    print(
        f"🟢 النظام يعمل على:"
    )

    print(
        f"http://{HOST}:{PORT}"
    )

    print()

    print(
        "🌐 افتح الرابط في المتصفح"
    )

    print()

    print(
        "🛑 لإيقاف البرنامج استخدم Ctrl+C"
    )

    print()


    server = ThreadingHTTPServer(
        (HOST, PORT),
        SecurityServer
    )


    threading.Timer(
        1.0,
        open_browser
    ).start()


    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print()
        print(
            "🛑 تم إيقاف النظام."
        )

    finally:

        server.server_close()


# =========================
# البداية
# =========================

if __name__ == "__main__":

    main()
