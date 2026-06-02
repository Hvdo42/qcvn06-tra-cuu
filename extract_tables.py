"""
extract_tables.py – Trích xuất toàn bộ bảng từ QCVN_06_2022_BXD.docx
và cập nhật vào QCVN06_Content.md

Nguyên tắc:
  - Duyệt qua document theo thứ tự (paragraph + table)
  - Khi gặp paragraph có "Bảng X" tiếp theo là table → chèn table vào Content.md
  - Bảng được format dạng Markdown table
"""
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
from docx import Document
from docx.oxml.ns import qn

MAIN_DOCX  = r'd:\Cowork\khoi luong\QC06\QCVN_06_2022_BXD.docx'
CONTENT_MD = r'd:\Cowork\khoi luong\QC06\QCVN06_Content.md'

# ===== ĐỌC DOCUMENT THEO THỨ TỰ (paragraph + table xen kẽ) =====
doc = Document(MAIN_DOCX)
body = doc.element.body

def iter_block_items(body):
    """Yield (type, object) theo thứ tự xuất hiện trong document."""
    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            from docx.text.paragraph import Paragraph
            yield 'para', Paragraph(child, body)
        elif tag == 'tbl':
            from docx.table import Table
            yield 'table', Table(child, body)

# ===== HÀM XỬ LÝ MERGED CELLS =====
def get_cell_text(cell):
    """Lấy text của cell, xử lý merge."""
    return cell.text.strip().replace('\n', ' ')

def table_to_markdown(tbl):
    """Chuyển Table thành Markdown, xử lý merged cells."""
    if not tbl.rows:
        return ''

    rows_data = []
    for row in tbl.rows:
        cells = [get_cell_text(c) for c in row.cells]
        rows_data.append(cells)

    if not rows_data:
        return ''

    # Tìm số cột thực tế (loại bỏ duplicate do merge)
    def dedupe_row(row):
        result = []
        prev = None
        for cell in row:
            if cell != prev or not result:
                result.append(cell)
            prev = cell
        return result

    # Dùng số cột từ hàng đầu tiên có nhiều cột nhất
    max_cols = max(len(set(row)) if len(row) > 1 else len(row) for row in rows_data[:3])

    # Xác định header rows (thường là 2-3 dòng đầu giống nhau do merge ngang)
    # Gộp header rows thành 1 dòng
    header_rows = []
    data_rows = []

    # Heuristic: nếu row[0] == row[1] thì là merged header → bỏ duplicate
    i = 0
    while i < len(rows_data):
        row = rows_data[i]
        deduped = dedupe_row(row)
        # Header row nếu chứa nhiều text dài (tiêu đề cột)
        is_likely_header = (i < 3 and
            sum(1 for c in deduped if len(c) > 5) >= max(1, len(deduped)//2))
        if is_likely_header:
            header_rows.append(deduped)
        else:
            data_rows.append(deduped)
        i += 1

    # Lấy header từ dòng cuối của header_rows (chi tiết nhất)
    if header_rows:
        header = header_rows[-1]
    elif data_rows:
        header = data_rows[0]
        data_rows = data_rows[1:]
    else:
        return ''

    # Đảm bảo tất cả row cùng độ dài
    ncols = len(header)
    def pad_row(row, n):
        if len(row) >= n:
            return row[:n]
        return row + [''] * (n - len(row))

    lines = []
    lines.append('| ' + ' | '.join(header) + ' |')
    lines.append('|' + '---|' * ncols)
    for row in data_rows:
        row = dedupe_row(row)
        row = pad_row(row, ncols)
        # Bỏ qua dòng ghi chú dài (CHÚ THÍCH) trong bảng
        if row[0].startswith('CHÚ THÍCH') and len(set(row)) == 1:
            lines.append(f'> {row[0][:150]}')
            continue
        lines.append('| ' + ' | '.join(str(c) for c in row) + ' |')

    return '\n'.join(lines)

# ===== DUYỆT DOCUMENT, GHÉP PARAGRAPH + TABLE =====
print('Đang đọc document theo thứ tự...')
doc_elements = []  # list of (type, name_or_obj)

current_para_title = None
TABLE_NAME_RE = re.compile(r'B[aả]ng\s+([A-Za-z0-9\.\-]+)', re.IGNORECASE)

for etype, eobj in iter_block_items(body):
    if etype == 'para':
        text = eobj.text.strip()
        if not text:
            continue
        doc_elements.append(('para', text))
        # Phát hiện tiêu đề bảng trong paragraph
        m = TABLE_NAME_RE.search(text)
        if m:
            current_para_title = text
    elif etype == 'table':
        md = table_to_markdown(eobj)
        if md:
            doc_elements.append(('table', md, current_para_title or ''))
        current_para_title = None  # reset sau khi đã dùng

# Thống kê
tables_found = [(t[2], len(t[1].split('\n'))) for t in doc_elements if t[0] == 'table']
print(f'Tìm thấy {len(tables_found)} bảng có dữ liệu')
for title, nrows in tables_found[:15]:
    short_title = (title or 'Bảng không tên')[:60]
    print(f'  {nrows:3d} dòng MD  {short_title}')

# ===== GHÉP VÀO CONTENT.MD =====
print()
print('Đang cập nhật QCVN06_Content.md...')

with open(CONTENT_MD, encoding='utf-8') as f:
    content = f.read()

# Với mỗi bảng tìm được, tìm tiêu đề tương ứng trong Content.md rồi chèn bảng vào
inserted = 0
skipped = 0

for element in doc_elements:
    if element[0] != 'table':
        continue
    _, md_table, para_title = element

    # Tìm tên bảng từ para_title
    if not para_title:
        skipped += 1
        continue

    m = TABLE_NAME_RE.search(para_title)
    if not m:
        skipped += 1
        continue

    table_id = m.group(1)  # e.g. "H.1", "4", "G.2a"

    # Tìm vị trí trong Content.md nơi đề cập đến Bảng này
    # Pattern: "Bảng H.1" hoặc "Bảng 4" trong content
    search_pattern = f'Bảng {table_id}'
    alt_pattern = f'Bảng {table_id.upper()}'

    pos = content.find(search_pattern)
    if pos < 0:
        pos = content.find(alt_pattern)
    if pos < 0:
        skipped += 1
        continue

    # Tìm cuối dòng tại vị trí đó
    end_of_line = content.find('\n', pos)
    if end_of_line < 0:
        end_of_line = len(content)

    # Kiểm tra nếu bảng đã được chèn rồi (dòng sau là | ... |)
    next_content = content[end_of_line+1:end_of_line+10].strip()
    if next_content.startswith('|'):
        skipped += 1
        continue

    # Chèn bảng Markdown sau dòng tiêu đề
    table_block = '\n\n' + md_table + '\n'
    content = content[:end_of_line] + table_block + content[end_of_line:]
    inserted += 1

    # Cần recalculate positions do đã thêm nội dung
    # (Không ảnh hưởng vì tìm từ đầu mỗi lần)

with open(CONTENT_MD, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Đã chèn: {inserted} bảng')
print(f'Bỏ qua:  {skipped} bảng (không tìm thấy vị trí)')
print()
print('Xong! Chạy python rebuild.py để cập nhật HTML.')
