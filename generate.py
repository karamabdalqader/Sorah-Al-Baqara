import json
import urllib.request
import re

url = "https://api.alquran.cloud/v1/surah/2/quran-uthmani"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
except Exception as e:
    print("Error fetching from API:", e)
    exit(1)

ayahs = data['data']['ayahs']

pages = {}
for ayah in ayahs:
    page = ayah['page']
    if page not in pages:
        pages[page] = []
    pages[page].append(ayah)

def to_arabic_numerals(num):
    arabic_map = {'0':'٠', '1':'١', '2':'٢', '3':'٣', '4':'٤', '5':'٥', '6':'٦', '7':'٧', '8':'٨', '9':'٩'}
    return ''.join(arabic_map.get(d, d) for d in str(num))

html_template = """<!DOCTYPE html>
<html lang="en" class="">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Surah Al-Baqarah - Reading View</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Amiri+Quran&amp;family=Lora:ital,wght@0,400..700;1,400..700&amp;display=swap" rel="stylesheet"/>
    <style>
        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Lora', serif;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        .quran-text {
            font-family: 'Amiri Quran', serif;
            font-size: 56px; 
            line-height: 2.8; 
            direction: rtl;
            text-align: justify;
            text-justify: inter-word;
            transition: font-size 0.3s ease, color 0.3s ease;
        }

        .ayah-marker {
            color: #D4AF37; 
            font-size: 0.5em; /* relative to font-size */
            margin: 0 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            position: relative;
            user-select: none;
        }



        .content-container {
            max-width: 700px; 
            width: 100%;
            margin: 0 auto;
            padding: 240px 32px 200px 32px; 
        }

        #progress-container {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 6px; 
            background: rgba(212, 175, 55, 0.1);
            z-index: 110;
        }
        
        html.dark #progress-container {
            background: rgba(212, 175, 55, 0.2);
        }

        #progress-bar {
            height: 100%;
            width: 0%;
            background: #D4AF37;
            opacity: 1;
            transition: width 0.1s ease-out;
        }

        #sticky-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 140px; 
            backdrop-filter: blur(16px);
            z-index: 105;
            border-bottom: 2px solid #D4AF37;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, background-color 0.3s ease;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 0 2rem;
        }
        
        html.dark #sticky-header {
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        #autosave-text {
            transition: opacity 0.5s ease;
            opacity: 0;
        }

        #autosave-text.show {
            opacity: 1;
        }
    
        .page-marker {
            position: absolute;
            right: -160px;
            top: 0.2em;
            font-family: 'Amiri Quran', serif;
            font-size: 1.14em; /* relative to font-size */
            color: #D4AF37; 
            user-select: none;
            pointer-events: none;
            opacity: 0.6; 
            direction: rtl;
            white-space: nowrap;
        }

        .quran-text {
            position: relative;
        }

        .verse-segment {
            position: relative;
            display: block;
        }

        .arabic-stats {
            font-family: 'Amiri Quran', serif;
            direction: rtl;
        }
    </style>
    <script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            colors: {
              "primary": "#eec02b",
              "background-light": "#f8f8f6",
              "background-dark": "#121212",
              "text-main": "#2A2626",
              "text-ui": "#59514A",
              "accent": "#D4AF37",
              "surface": "#F4EFE6",
              "muted": "#BDB3A6"
            },
            fontFamily: {
              "display": ["Newsreader", "serif"],
              "arabic": ["'Amiri Quran'", "serif"],
              "ui": ["Lora", "serif"]
            },
            borderRadius: {"DEFAULT": "0.125rem", "lg": "0.25rem", "xl": "0.5rem", "full": "0.75rem"},
          },
        },
      }
    </script>
</head>
<body class="bg-[#FBF8F1] dark:bg-background-dark text-text-main dark:text-[#e0e0e0] min-h-screen flex flex-col items-center overflow-x-hidden selection:bg-surface selection:text-text-main relative transition-colors duration-300">

<header id="sticky-header" class="bg-[#FBF8F1]/98 dark:bg-[#1a1a1a]/98 transition-colors duration-300">
    <div class="max-w-4xl mx-auto w-full flex justify-between items-center">
        <div class="flex flex-col">
            <h2 class="text-[12px] uppercase tracking-[0.4em] font-extrabold text-accent mb-2">سورة البقرة</h2>
            <div class="flex items-center gap-12 arabic-stats text-text-main dark:text-gray-200 transition-colors">
                <span class="text-3xl font-bold" id="verse-progress-ar">الآية ١ من ٢٨٦</span>
                <div class="w-2 h-2 rounded-full bg-accent/40"></div>
                <span class="text-3xl font-bold" id="page-progress-ar">الصفحة ٢ من ٤٩</span>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <div id="autosave-text" class="hidden sm:flex items-center gap-1 text-accent/80 text-[10px] font-bold tracking-wider mr-2">
                <span class="material-symbols-outlined text-[14px]">check_circle</span>
                <span>تلقائي</span>
            </div>
            <button aria-label="Increase Font Size" title="Font Size" class="p-2 rounded-full hover:bg-accent/10 dark:hover:bg-accent/20 text-text-ui dark:text-gray-300 transition-colors" onclick="changeFontSize()">
                <span class="material-symbols-outlined text-[24px] hover:scale-110 transition-transform">format_size</span>
            </button>
            <button aria-label="Toggle Theme" title="Toggle Theme" class="p-2 rounded-full hover:bg-accent/10 dark:hover:bg-accent/20 text-text-ui dark:text-gray-300 transition-colors" onclick="toggleNightMode()">
                <span class="material-symbols-outlined text-[24px] hover:scale-110 transition-transform" id="theme-icon">dark_mode</span>
            </button>
            <button aria-label="Restart Recitation" title="Restart Recitation" class="p-2 rounded-full hover:bg-accent/10 dark:hover:bg-accent/20 text-text-ui dark:text-gray-300 transition-colors" onclick="restartRecitation()">
                <span class="material-symbols-outlined text-[24px] hover:scale-110 transition-transform">restart_alt</span>
            </button>
        </div>
    </div>
    <div id="progress-container">
        <div id="progress-bar"></div>
    </div>
</header>

<!-- Removed overlay save indicator -->

<main class="content-container flex flex-col items-center">
    <div class="mb-24 text-center w-full" dir="rtl">
        <h1 class="font-arabic text-[42px] text-text-ui dark:text-gray-400 tracking-wide opacity-80 transition-colors duration-300">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</h1>
    </div>

    <article class="quran-text w-full">
{CONTENT}
    </article>

    <div class="mt-32 flex flex-col items-center opacity-30 dark:opacity-50 select-none text-text-main dark:text-gray-300 transition-colors">
        <span class="material-symbols-outlined animate-bounce">keyboard_double_arrow_down</span>
        <span class="font-ui text-xs uppercase tracking-[0.2em] mt-2">Continue Scrolling</span>
    </div>
</main>



<script>
    const progressBar = document.getElementById('progress-bar');
    const autosaveText = document.getElementById('autosave-text');
    const verseTextAr = document.getElementById('verse-progress-ar');
    const pageTextAr = document.getElementById('page-progress-ar');
    const segments = document.querySelectorAll('.verse-segment');
    const ayahMarkers = document.querySelectorAll('.ayah-marker');

    let scrollTimeout;
    let saveTimeout;
    let currentFontSize = 56;

    const toArabicNumerals = (num) => {
        const arabicMap = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
        return String(num).replace(/[0-9]/g, (d) => arabicMap[d]);
    };

    const pages = new Set();
    segments.forEach(s => pages.add(parseInt(s.dataset.page)));
    const minPage = Math.min(...pages);
    const maxPage = Math.max(...pages);
    const totalPages = maxPage - minPage + 1; 

    // Handle initial state restore
    window.addEventListener('load', () => {
        const isDark = localStorage.getItem('alBaqarahDarkMode') === 'true';
        if (isDark) {
            document.documentElement.classList.add('dark');
            updateThemeIcon(true);
        }

        const savedFontSize = localStorage.getItem('alBaqarahFontSize');
        if (savedFontSize) {
            currentFontSize = parseInt(savedFontSize, 10);
            document.querySelector('.quran-text').style.fontSize = currentFontSize + 'px';
        }

        const savedScroll = localStorage.getItem('alBaqarahScrollPos');
        if (savedScroll) {
            window.scrollTo({
                top: parseInt(savedScroll, 10),
                behavior: 'auto'
            });
        }
        updateProgressText();
    });

    // Theme Toggle
    function toggleNightMode() {
        document.documentElement.classList.toggle('dark');
        const isDark = document.documentElement.classList.contains('dark');
        localStorage.setItem('alBaqarahDarkMode', isDark);
        updateThemeIcon(isDark);
        showSaveIndicator(isDark ? "الوضع الليلي: مفعل" : "الوضع الليلي: معطل");
    }

    function updateThemeIcon(isDark) {
        const icon = document.getElementById('theme-icon');
        if (isDark) {
            icon.textContent = 'light_mode';
        } else {
            icon.textContent = 'dark_mode';
        }
    }

    // Font Size Toggle
    function changeFontSize() {
        const textContainer = document.querySelector('.quran-text');
        currentFontSize += 8;
        if (currentFontSize > 80) currentFontSize = 40; 
        textContainer.style.fontSize = currentFontSize + 'px';
        localStorage.setItem('alBaqarahFontSize', currentFontSize);
        
        let sizeName = "متوسط";
        if (currentFontSize <= 48) sizeName = "صغير";
        if (currentFontSize >= 64) sizeName = "كبير";
        if (currentFontSize >= 72) sizeName = "كبير جداً";
        
        showSaveIndicator("حجم الخط: " + sizeName);
        
        // Minor readjustment tracking due to layout shift
        setTimeout(updateProgressText, 300);
    }

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        document.body.classList.add('scrolling');
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function() {
            document.body.classList.remove('scrolling');
            savePosition(scrollTop);
        }, 1500);

        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (height > 0) ? (scrollTop / height) * 100 : 0;
        progressBar.style.width = scrolled + "%";

        updateProgressText();
    });

    function savePosition(pos) {
        localStorage.setItem('alBaqarahScrollPos', pos);
    }

    function restartRecitation() {
        localStorage.removeItem('alBaqarahScrollPos');
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        showSaveIndicator("تم مسح التقدم");
    }

    function updateProgressText() {
        let currentPage = minPage;
        let currentVerse = 1;

        let foundPage = false;
        segments.forEach(segment => {
            if (!foundPage) {
                const rect = segment.getBoundingClientRect();
                if (rect.bottom > 150) {
                    currentPage = segment.dataset.page;
                    foundPage = true;
                }
            }
        });

        let foundVerse = false;
        ayahMarkers.forEach(marker => {
            if (!foundVerse) {
                const rect = marker.getBoundingClientRect();
                // 150px threshold perfectly clears the sticky header (140px)
                if (rect.bottom > 150) {
                    currentVerse = marker.dataset.verse;
                    foundVerse = true;
                }
            }
        });

        const totalVersesAr = toArabicNumerals(286);
        const currentVerseAr = toArabicNumerals(currentVerse);
        const maxPageAr = toArabicNumerals(maxPage);
        
        const currentPageAr = toArabicNumerals(currentPage);

        verseTextAr.textContent = `الآية ${currentVerseAr} من ${totalVersesAr}`;
        pageTextAr.textContent = `الصفحة ${currentPageAr} من ${maxPageAr}`;
    }

    function showSaveIndicator(customText) {
        if (!autosaveText) return;
        if (customText) {
            autosaveText.children[1].textContent = customText;
        } else {
            autosaveText.children[1].textContent = "تلقائي";
        }
        autosaveText.classList.add('show');
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            autosaveText.classList.remove('show');
        }, 1500);
    }
</script>
</body>
</html>"""

content = ""
for page, page_ayahs in sorted(pages.items()):
    start_verse = page_ayahs[0]['numberInSurah']
    page_arabic = to_arabic_numerals(page)
    content += f'        <div class="verse-segment" data-page="{page}" data-start-verse="{start_verse}">\n'
    content += f'            <span class="page-marker">{page_arabic}</span>\n'
    
    for ayah in page_ayahs:
        text = ayah['text']
        
        bismillah = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ "
        if ayah['numberInSurah'] == 1 and text.startswith(bismillah):
            text = text[len(bismillah):]
            
        verse_num = to_arabic_numerals(ayah['numberInSurah'])
        content += f'            {text} <span class="ayah-marker" data-verse="{ayah["numberInSurah"]}">﴿{verse_num}﴾</span>\n'
        
    content += '        </div>\n'

html_output = html_template.replace('{CONTENT}', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("Generated index.html successfully.")
