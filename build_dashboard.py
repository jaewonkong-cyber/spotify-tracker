import csv, json, os

# --- 청취자 데이터 (기존) ---
data = []
with open('data.csv', 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        try:
            m = int(float(row.get('monthly_listeners') or 0))
        except:
            m = 0
        if m > 0:
            data.append({"d": row['date'].strip(), "l": row['label'].strip(), "a": row['artist'].strip(), "m": m})
print(len(data), "datapoints")

# --- 이벤트 데이터 (신규) ---
events = []
DATE_OK = ('YYYY-MM-DD 또는 YYYY-Qn (분기 TBD)')
def valid_date(s):
    import re
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', s) or re.match(r'^\d{4}-Q[1-4]$', s))

if os.path.exists('events.csv'):
    with open('events.csv', 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            date = (row.get('date') or '').strip()
            artist = (row.get('artist') or '').strip()
            etype = (row.get('type') or '').strip().lower()
            title = (row.get('title') or '').strip()
            note = (row.get('note') or '').strip()
            if date and artist and etype:
                if not valid_date(date):
                    print(f"  WARN: bad date '{date}' for {artist} '{title}' (expect {DATE_OK})")
                events.append({"d": date, "a": artist, "t": etype, "ti": title, "n": note})
    print(len(events), "events")
else:
    print("events.csv not found, skipping")

j = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
ej = json.dumps(events, ensure_ascii=False, separators=(',', ':'))

with open('template.html', 'r', encoding='utf-8') as f:
    h = f.read()
h = h.replace('/*DATA_PLACEHOLDER*/[]', j)
h = h.replace('/*EV_DATA_PLACEHOLDER*/[]', ej)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(h)
# GitHub Pages용 index.html도 같이 생성
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print("done!", len(h), "bytes")
