import feedparser, json, datetime

# List of RSS feeds
feeds = {
    "detik.com": "https://news.detik.com/berita/rss",
    "antaranews.com": "https://www.antaranews.com/rss/top-news",
    "kompas.com": "https://rss.kompas.com/api/feed/social?apikey=bc58c81819dff4b8d5c53540a2fc7ffd83e6314a",
    "tempo.co": "http://rss.tempo.co/nasional",
    "cnnindonesia.com": "https://www.cnnindonesia.com/nasional/rss"
}

results = []
for name, url in feeds.items():
    d = feedparser.parse(url)
    if d.entries:
        latest = d.entries[0]
        title = latest.title.replace("\n", " ").strip()
        results.append({"source": name, "title": title})

data = {
    "updated": datetime.datetime.utcnow().isoformat() + "Z",
    "feeds": results
}

# ←←← ONLY THIS LINE CHANGED ←←←
with open("data/latest.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("latest.json updated successfully inside /data folder!")
