name: Update news feed

on:
  schedule:
    - cron: "0 * * * *" # every hour
  workflow_dispatch:

permissions:
  contents: write   # 👈 allows commit/push from Actions

jobs:
  fetch:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout main branch
        uses: actions/checkout@v4
        with:
          ref: main
          persist-credentials: false

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: pip install feedparser requests

      - name: Generate latest.json
        run: |
          echo "import json, feedparser, datetime
          feeds = {
              'detik.com': 'https://news.detik.com/berita/rss',
              'antaranews.com': 'https://www.antaranews.com/rss/top-news',
              'kompas.com': 'https://rss.kompas.com/api/feed/social?apikey=bc58c81819dff4b8d5c53540a2fc7ffd83e6314a',
              'tempo.co': 'http://rss.tempo.co/nasional',
              'cnnindonesia.com': 'https://www.cnnindonesia.com/nasional/rss',
          }

          results = []
          for source, url in feeds.items():
              try:
                  d = feedparser.parse(url)
                  if d.entries:
                      title = d.entries[0].title
                      results.append({'source': source, 'title': title})
              except Exception as e:
                  print('Failed to fetch', source, e)

          data = {
              'updated': datetime.datetime.utcnow().isoformat() + 'Z',
              'feeds': results
          }

          with open('latest.json', 'w', encoding='utf-8') as f:
              json.dump(data, f, ensure_ascii=False, indent=2)
          " > update_feeds.py

          python update_feeds.py

      - name: Commit and push changes
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add latest.json
          git commit -m "Update news feed" || echo "No changes to commit"
          git push origin main
