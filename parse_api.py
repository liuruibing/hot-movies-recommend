import json
import urllib.request
import sys

def fetch_data(t):
    url = f"https://cj.lziapi.com/api.php/provide/vod/?ac=detail&t={t}&pg=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))

        movies = data.get('list', [])[:4]
        results = []
        for movie in movies:
            play_urls_raw = movie.get('vod_play_url', '')
            play_urls = []

            # vod_play_url may contain multiple sources separated by '$$$'
            sources = play_urls_raw.split('$$$')
            m3u8_source = ""
            for source in sources:
                if 'm3u8' in source:
                    m3u8_source = source
                    break
            if not m3u8_source and sources:
                m3u8_source = sources[0]

            # Parse episodes
            episodes = m3u8_source.split('#')
            first_ep_url = ""
            if episodes:
                parts = episodes[0].split('$')
                if len(parts) > 1:
                    first_ep_url = parts[1]

            results.append({
                'id': movie.get('vod_id'),
                'name': movie.get('vod_name'),
                'pic': movie.get('vod_pic'),
                'remarks': movie.get('vod_remarks'),
                'blurb': movie.get('vod_blurb', '')[:50] + '...' if movie.get('vod_blurb') else '',
                'score': movie.get('vod_score', 'N/A'),
                'class': movie.get('vod_class', ''),
                'play_url': first_ep_url
            })

        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    t = sys.argv[1]
    fetch_data(t)
