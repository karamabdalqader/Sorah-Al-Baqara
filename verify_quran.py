import json
import urllib.request
import unicodedata

# Source 1: AlQuran.cloud (currently used in generate.py)
url1 = "https://api.alquran.cloud/v1/surah/2/quran-uthmani"
req1 = urllib.request.Request(url1, headers={'User-Agent': 'Mozilla/5.0'})
print("Fetching from AlQuran.cloud...")
with urllib.request.urlopen(req1) as response:
    data1 = json.loads(response.read().decode())
ayahs1 = data1['data']['ayahs']

# Source 2: Quran.com API (Tanzil based)
url2 = "https://api.quran.com/api/v4/quran/verses/uthmani?chapter_number=2"
req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
print("Fetching from Quran.com...")
with urllib.request.urlopen(req2) as response:
    data2 = json.loads(response.read().decode())
ayahs2 = data2['verses']

if len(ayahs1) != len(ayahs2):
    print("Verse count mismatch!!")

def normalize_arabic(text):
    # Normalize unicode to canonical composition to avoid hidden byte differences
    # for the exact same character combination
    return unicodedata.normalize('NFC', text.strip())

differences = 0
for i in range(286):
    text1 = ayahs1[i]['text']
    
    # AlQuran cloud appends Bismillah to verse 1, Quran.com does not typically.
    bismillah = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ "
    if i == 0 and text1.startswith(bismillah):
        text1 = text1[len(bismillah):]
        
    text1_norm = normalize_arabic(text1)
    text2_norm = normalize_arabic(ayahs2[i]['text_uthmani'])
    
    if text1_norm != text2_norm:
        # Check if the difference is just Waqf marks or something trivial
        # For full safety, we print exact differences if they exist.
        print(f"Difference found in Ayah {i+1}:")
        print(f"AlQuran.cloud: {text1_norm}")
        print(f"Quran.com:     {text2_norm}")
        print("-" * 40)
        differences += 1

if differences == 0:
    print("\n[VERIFIED] Verification complete: EXACT MATCH between AlQuran.cloud and Quran.com for all 286 verses!")
else:
    print(f"\nFound {differences} unicode/text differences overall.")
