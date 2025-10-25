import requests, xml.etree.ElementTree as ET, os, json

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
LAST_FILE = "last_videos.txt"

CHANNELS = [
    "UCQvyoMyqYs9hcajVbZHIJxQ",
    "UC0ohl1eKTtlJNqbD-HWRQVg"
]

def get_video(channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    r = requests.get(url)
    if r.status_code != 200:
        return None, None
    root = ET.fromstring(r.content)
    entry = root.find("{http://www.w3.org/2005/Atom}entry")
    if entry is None:
        return None, None
    title = entry.find("{http://www.w3.org/2005/Atom}title").text
    link = entry.find("{http://www.w3.org/2005/Atom}link").attrib["href"]
    return title, link

def send_discord(title, link):
    data = {"content": f"🎬 **{title}**\n{link}"}
    requests.post(WEBHOOK_URL, json=data)

def load_last():
    if not os.path.exists(LAST_FILE):
        return {}
    try:
        with open(LAST_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_last(data):
    with open(LAST_FILE, "w") as f:
        json.dump(data, f)

def main():
    last = load_last()
    for c in CHANNELS:
        title, link = get_video(c)
        if not link:
            continue
        if last.get(c) != link:
            print("New video:", title)
            send_discord(title, link)
            last[c] = link
    save_last(last)

if __name__ == "__main__":
    main()
