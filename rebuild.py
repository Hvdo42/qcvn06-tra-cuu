"""
rebuild.py – Đọc QCVN06_Content.md → tạo lại JSON và HTML app

Cách dùng:
  python rebuild.py          # Rebuild từ QCVN06_Content.md
  python rebuild.py --check  # Chỉ kiểm tra parse, không ghi file

Cú pháp QCVN06_Content.md:
  # TIÊU ĐỀ               → Section heading (# ở đầu)
  ## Sub-heading           → Sub-heading (## ở đầu, không tạo entry riêng)
  3.2.5 Nội dung...        → Entry có số điều khoản
  [SĐ1] Nội dung...        → Entry có marker sửa đổi
  Nội dung bình thường     → Entry không có số điều khoản
  ---                      → Bỏ qua (separator)
  > Ghi chú...             → Bỏ qua (blockquote)
"""
import json, re, sys, os, subprocess, argparse
sys.stdout.reconfigure(encoding='utf-8')

MD_PATH   = r'd:\Cowork\khoi luong\QC06\QCVN06_Content.md'
JSON_PATH = r'd:\Cowork\khoi luong\QC06\qcvn06_data_full.json'
HTML_PATH = r'd:\Cowork\khoi luong\QC06\QCVN06_TraCuu.html'
BUILD_PY  = r'd:\Cowork\khoi luong\QC06\build_app.py'

# Pattern nhận diện
CLAUSE_RE = re.compile(
    r'^(\d+\.\d+(?:\.\d+)*[a-z]?'
    r'|[A-I]\.\d+(?:\.\d+)*'
    r'|B[aả]ng\s+\d+'
    r'|\d+\.\d+[÷-]\d+\.\d+)',
    re.IGNORECASE
)
SD1_RE    = re.compile(r'\[S[DĐ]1\]?', re.IGNORECASE)

# Map section label → (type, key)
SECTION_MAP = {
    'PHẦN 1': ('phan', 1), 'PHẦN 2': ('phan', 2), 'PHẦN 3': ('phan', 3),
    'PHẦN 4': ('phan', 4), 'PHẦN 5': ('phan', 5), 'PHẦN 6': ('phan', 6),
    'PHẦN 7': ('phan', 7),
}
for k in 'ABCDEFGHI':
    SECTION_MAP[f'PHỤ LỤC {k}'] = ('phu_luc', k)

def detect_section(heading_text):
    """Tìm section type/key từ heading text."""
    t = heading_text.strip().upper()
    for key, val in SECTION_MAP.items():
        if key in t:
            return val[0], val[1], heading_text.strip()
    return 'khac', 0, heading_text.strip()

def parse_md(md_path):
    with open(md_path, encoding='utf-8') as f:
        raw_lines = f.readlines()

    entries = []
    current_section = {'type': 'header', 'key': 0, 'label': 'Phần mở đầu'}
    entry_id = 0

    for raw in raw_lines:
        line = raw.rstrip('\n').rstrip('\r')

        # Bỏ qua dòng trống, separator, blockquote, title chính
        if not line.strip():
            continue
        if line.startswith('---') or line.startswith('>'):
            continue

        # Section heading (# )
        if line.startswith('# ') and not line.startswith('## '):
            heading = line[2:].strip()
            if 'QCVN 06' in heading:
                continue  # Skip title line
            sec_type, sec_key, label = detect_section(heading)
            current_section = {'type': sec_type, 'key': sec_key, 'label': label}
            continue

        # Sub-heading (## )
        if line.startswith('## '):
            text = line[3:].strip()
            # Phát hiện clause id trong sub-heading
            m = CLAUSE_RE.match(text)
            clause = m.group(1).strip() if m else None
            sd1 = bool(SD1_RE.search(text))
            entries.append({
                'id': f'e_{entry_id}',
                'clause': clause,
                'text': text,
                'section_type': current_section['type'],
                'section_key': current_section['key'],
                'section_label': current_section['label'],
                'sd1': sd1,
                'is_heading': True,
                'page': None,
            })
            entry_id += 1
            continue

        # Entry thong thuong
        text = line.strip()
        if not text:
            continue

        sd1 = bool(SD1_RE.search(text))
        # Xoa [SĐ1] prefix khoi text neu co
        clean_text = SD1_RE.sub('', text).strip()

        m = CLAUSE_RE.match(clean_text)
        clause = m.group(1).strip() if m else None

        upper_ratio = sum(1 for c in clean_text if c.isupper()) / max(len(clean_text), 1)
        is_heading = (clause is None and upper_ratio > 0.6 and len(clean_text) < 60)

        entries.append({
            'id': f'e_{entry_id}',
            'clause': clause,
            'text': clean_text,
            'section_type': current_section['type'],
            'section_key': current_section['key'],
            'section_label': current_section['label'],
            'sd1': sd1,
            'is_heading': is_heading,
            'page': None,
        })
        entry_id += 1

    return entries

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Chỉ parse, không ghi file')
    args = parser.parse_args()

    if not os.path.exists(MD_PATH):
        print(f'Không tìm thấy {MD_PATH}')
        print('Chạy python export_md.py trước để tạo file.')
        return

    print(f'Đọc {MD_PATH}...')
    entries = parse_md(MD_PATH)
    print(f'Parsed {len(entries)} entries')

    # Thống kê
    sections = {}
    for e in entries:
        k = e['section_label'][:40]
        sections[k] = sections.get(k, 0) + 1
    for k, v in sorted(sections.items(), key=lambda x: -x[1])[:12]:
        print(f'  {v:4d}  {k}')

    if args.check:
        print('--check mode: không ghi file')
        return

    # Ghi JSON
    data = {
        'meta': {
            'title': 'QCVN 06:2022/BXD – An toàn cháy cho nhà và công trình',
            'hop_nhat': 'QCVN 06:2022/BXD + Sửa đổi 1:2023 (TT 09/2023/TT-BXD)',
            'source': f'Từ {os.path.basename(MD_PATH)}',
            'total_entries': len(entries),
        },
        'entries': entries,
    }
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    size = os.path.getsize(JSON_PATH) / 1024
    print(f'Đã ghi {JSON_PATH} ({size:.0f} KB)')

    # Rebuild HTML
    print('Đang rebuild HTML...')
    result = subprocess.run(
        [sys.executable, BUILD_PY],
        capture_output=True, text=True, encoding='utf-8'
    )
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print('LỖI khi build HTML:')
        print(result.stderr)

    print()
    print('Hoàn thành! Mở QCVN06_TraCuu.html để kiểm tra.')

if __name__ == '__main__':
    main()
