import json
import urllib.request
import unicodedata

# Source 1: AlQuran.cloud quran-simple
url1 = "https://api.alquran.cloud/v1/surah/2/quran-simple"
req1 = urllib.request.Request(url1, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req1) as response:
    data1 = json.loads(response.read().decode())
ayahs1 = data1['data']['ayahs']

# Source 2: Quran.com Imlaei script
url2 = "https://api.quran.com/api/v4/quran/verses/imlaei?chapter_number=2"
req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req2) as response:
    data2 = json.loads(response.read().decode())
ayahs2 = data2['verses']

def normalize_arabic(text):
    return unicodedata.normalize('NFC', text.strip())

differences = 0
for i in range(286):
    text1 = ayahs1[i]['text']
    bismillah = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ "
    if i == 0 and text1.startswith(bismillah):
        text1 = text1[len(bismillah):]
        
    t1 = normalize_arabic(text1)
    
    # Quran.com structure: text_imlaei
    t2 = normalize_arabic(ayahs2[i].get('text_imlaei', ''))
    
    if t1 != t2:
        # Ignore minor punctuation (like sajda marks or stop characters) matching between sources
        print(f"Diff Ayah {i+1}:")
        print(f"  AlQuran: {t1}")
        print(f"  Quran.com: {t2}")
        differences += 1

print(f"Total differences: {differences}")
