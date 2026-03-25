import os

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update .content-container CSS
    content = content.replace(
'''        .content-container {
            max-width: 700px; 
            width: 100%;
            margin: 0 auto;
            padding: 240px 32px 200px 32px; 
        }''',
'''        .content-container {
            max-width: 700px; 
            width: 100%;
            margin: 0 auto;
            padding: 240px 16px 200px 16px; 
        }
        @media (min-width: 640px) {
            .content-container {
                padding: 240px 32px 200px 32px;
            }
        }'''
    )

    # 2. Update .page-marker CSS
    content = content.replace(
'''        .page-marker {
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
        }''',
'''        .page-marker {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            margin: 1.5em 0;
            padding-top: 1em;
            border-top: 1px dashed rgba(212, 175, 55, 0.3);
            font-family: 'Amiri Quran', serif;
            font-size: 0.5em; /* beautifully scaled down */
            color: #D4AF37; 
            user-select: none;
            opacity: 0.7; 
            direction: rtl;
        }'''
    )

    # 3. Update active header HTML
    content = content.replace(
'''        <div class="flex flex-col">
            <h2 class="text-[12px] uppercase tracking-[0.4em] font-extrabold text-accent mb-2">سورة البقرة</h2>
            <div class="flex items-center gap-12 arabic-stats text-text-main dark:text-gray-200 transition-colors">
                <span class="text-3xl font-bold" id="verse-progress-ar">الآية ١ من ٢٨٦</span>
                <div class="w-2 h-2 rounded-full bg-accent/40"></div>
                <span class="text-3xl font-bold" id="page-progress-ar">الصفحة ٢ من ٤٩</span>
            </div>
        </div>''',
'''        <div class="flex flex-col">
            <h2 class="text-[10px] sm:text-[12px] uppercase tracking-[0.4em] font-extrabold text-accent mb-1 sm:mb-2">سورة البقرة</h2>
            <div class="flex items-center gap-4 sm:gap-12 arabic-stats text-text-main dark:text-gray-200 transition-colors">
                <span class="text-xl sm:text-3xl font-bold" id="verse-progress-ar">الآية ١ من ٢٨٦</span>
                <div class="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-accent/40"></div>
                <span class="text-xl sm:text-3xl font-bold" id="page-progress-ar">الصفحة ٢ من ٤٩</span>
            </div>
        </div>'''
    )

    # 4. Update Bismillah HTML
    content = content.replace(
'''    <div class="mb-24 text-center w-full" dir="rtl">
        <h1 class="font-arabic text-[42px] text-text-ui dark:text-gray-400 tracking-wide opacity-80 transition-colors duration-300">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</h1>
    </div>''',
'''    <div class="mb-16 sm:mb-24 text-center w-full" dir="rtl">
        <h1 class="font-arabic text-[32px] sm:text-[42px] text-text-ui dark:text-gray-400 tracking-wide opacity-80 transition-colors duration-300">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</h1>
    </div>'''
    )

    # 5. Update Python loop page span
    content = content.replace(
'''    content += f'        <div class="verse-segment" data-page="{page}" data-start-verse="{start_verse}">\\n'
    content += f'            <span class="page-marker">{page_arabic}</span>\\n' ''',
'''    content += f'        <div class="verse-segment" data-page="{page}" data-start-verse="{start_verse}">\\n'
    content += f'            <div class="page-marker">الصفحة {page_arabic}</div>\\n' '''
    )

    # 6. Update JS FontSize Baseline
    content = content.replace(
        "let currentFontSize = 56;",
        "let currentFontSize = window.innerWidth < 640 ? 40 : 56;"
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Replacements executed successfully.")

update_file('generate.py')
