import json
import urllib.request

editions = ['quran-uthmani', 'quran-uthmani-min', 'quran-simple', 'quran-simple-clean', 'quran-simple-enhanced']
for ed in editions:
    url = f"https://api.alquran.cloud/v1/ayah/2:124/{ed}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            text = data['data']['text']
            print(f"{ed:25} : {text}")
    except Exception as e:
        print(f"Error {ed}: {e}")

