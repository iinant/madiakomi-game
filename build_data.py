import csv, json, re, sys

src, dst = sys.argv[1], sys.argv[2]

rows = []
with open(src, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for r in reader:
        link = (r.get('ссылка') or '').strip()
        price_raw = (r.get('цена') or '').strip()
        photos = []
        for k in ('фото 1', 'фото 2 ', 'фото 3', 'фото 4', 'фото 5'):
            p = (r.get(k) or '').strip()
            if p.startswith('http'):
                photos.append(p)
        price = re.sub(r'[\s\xa0 ]', '', price_raw)
        if not price.isdigit():
            continue
        price = int(price)
        # Активные объявления = есть и ссылка, и хотя бы 2 фото, и адекватная цена
        if not link.startswith('http') or len(photos) < 2 or price < 20000:
            continue
        rows.append({
            'link': link,
            'photos': photos,
            'price': price,
            'desc': (r.get('описание') or '').strip(),
            'street': (r.get('цлица') or '').strip(),
        })

with open(dst, 'w', encoding='utf-8') as f:
    f.write('window.GAME_DATA = ')
    json.dump(rows, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';')

print('kept:', len(rows))
for r in rows:
    print(r['price'], r['desc'][:40], r['street'], len(r['photos']))
