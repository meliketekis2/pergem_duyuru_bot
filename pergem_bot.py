import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.tarimorman.gov.tr/PERGEM/Sayfalar/Detay.aspx?Liste=Duyuru"
STATE_FILE = "last_pergem_duyuru.txt"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def fetch_announcements():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    items = soup.select("div.divList ul li")
    announcements = []
    for li in items:
        title = li.get_text(" ", strip=True)
        announcements.append(title)
    return announcements

def load_last():
    if os.path.exists(STATE_FILE):
        return open(STATE_FILE, "r", encoding="utf-8").read().strip()
    return ""

def save_last(v):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(v)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg,
        "disable_web_page_preview": False
    })
    resp.raise_for_status()

def main():
    ann = fetch_announcements()
    if not ann:
        msg = "Duyuru listesi bulunamadı."
        send_telegram(msg)
        print(msg)
        return
    latest = ann[0]
    if latest != load_last():
        msg = f"Yeni PERGEM duyurusu:\n{latest}\n{URL}"
        send_telegram(msg)
        print("Yeni duyuru bildirildi:", latest)
        save_last(latest)
    else:
        msg = "Yeni PERGEM duyurusu yok."
        send_telegram(msg)
        print(msg)

if __name__ == "__main__":
    main()

