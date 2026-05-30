"""
build_app.py – Tạo QCVN06_TraCuu.html từ qcvn06_data.json
Tách RULES metadata (Python dict -> JSON) khỏi check functions (JS code)
để tránh lỗi escape chuỗi đa dòng.
"""
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

JSON_PATH = r'd:\Cowork\khoi luong\QC06\qcvn06_data_full.json'
OUT_PATH  = r'd:\Cowork\khoi luong\QC06\QCVN06_TraCuu.html'

with open(JSON_PATH, encoding='utf-8') as f:
    qcvn_data = json.load(f)

# ===== RULES METADATA (Python dict -> JSON-serialized, chuỗi được escape đúng) =====
RULES_META = [
    {
        'block': '🚶 Thoát nạn (Phần 3)',
        'id': 'r_loi_ra_so',
        'title': 'Số lối ra thoát nạn tối thiểu',
        'clause': '3.2.5 [SĐ1]',
        'sd1': True,
        'detail': (
            'Phải có tối thiểu 2 lối ra thoát nạn từ:\n'
            'a) Gian phòng có ≥50 người;\n'
            'b) Gian phòng tầng hầm/nửa hầm có >15 người [SĐ1];\n'
            'c) Gian phòng hạng A và B có ≥5 người; hạng C có ≥25 người;\n'
            'd) Gian phòng tầng ≥2 có diện tích >1.000 m² hoặc >50 người.\n\n'
            'Khoảng cách tối thiểu giữa 2 lối ra ≥7 m (3.2.8 [SĐ1]).\n'
            'Cửa trên lối thoát nạn phải mở theo hướng thoát nạn, trừ gian phòng ≤15 người, nhà F1.4, buồng thang bộ (3.2.10).'
        ),
    },
    {
        'block': '🚶 Thoát nạn (Phần 3)',
        'id': 'r_ban_thang',
        'title': 'Chiều rộng bản thang bộ tối thiểu',
        'clause': '3.4.1 [SĐ1]',
        'sd1': True,
        'detail': (
            'Chiều rộng bản thang tối thiểu:\n'
            '• ≥1,2 m – nhà F1.1 có >15 người thoát nạn qua thang/tầng\n'
            '• ≥1,0 m – nhà F1.1 có ≤15 người/tầng [SĐ1]\n'
            '• ≥1,2 m – nhà F1.2, F1.3, F2÷F4 có PCCC >28 m\n'
            '• ≥0,9 m – nhà F1.2, F1.3, F2÷F4 còn lại\n'
            '• ≥0,7 m – nhà PCCC ≤15 m và ≤15 người/tầng [SĐ1]\n\n'
            'Cho phép dùng tài liệu chuẩn để tính toán thoát nạn khi không đảm bảo kích thước trên [SĐ1].\n'
            'Góc nghiêng bản thang ≤1:2 (~26°) với nhà F1.1; F1.2, F1.3, F2, F3, F4 PCCC >28 m.\n'
            'Chiều cao bậc ≤190 mm; chiều rộng mặt bậc ≥250 mm (3.4.2).'
        ),
    },
    {
        'block': '🚶 Thoát nạn (Phần 3)',
        'id': 'r_hanh_lang',
        'title': 'Chiều rộng hành lang thoát nạn',
        'clause': '3.3.3',
        'sd1': False,
        'detail': (
            'Chiều rộng thông thủy hành lang tối thiểu:\n'
            '• 1,2 m – nhà F1.1, F1.2, F1.3, F2, F3, F4.1 có PCCC >28 m\n'
            '• 1,0 m – nhà F1÷F4 còn lại\n'
            '• 0,9 m – các trường hợp khác\n\n'
            'Hành lang không được là đường đi thông qua giữa hai cầu thang bộ (3.3.4).\n'
            'Hành lang trong phải được ngăn cách với gian phòng tiếp giáp bằng vách ngăn cháy loại 2 (3.3.5 [SĐ1]).'
        ),
    },
    {
        'block': '🚶 Thoát nạn (Phần 3)',
        'id': 'r_buong_thang',
        'title': 'Loại buồng thang bộ – Chống khói',
        'clause': '2.4.3 / 3.4.13',
        'sd1': False,
        'detail': (
            'Phân loại buồng thang bộ:\n'
            'Thông thường: L1 (chiếu sáng qua tường ngoài); L2 (qua khoang mái); L3 (không có lỗ mở)\n'
            'Không nhiễm khói: H1 (hành lang bên ngoài / áp suất dương); H2 (khoang đệm + không khí dương); H3 (khoang đệm + nước mưa)\n\n'
            'Nhà có PCCC >28 m → BẮT BUỘC dùng buồng thang không nhiễm khói H1, H2 hoặc H3.\n'
            'Buồng thang L3 phải có lỗ thoát khói trên tum thang tổng diện tích ≥10% diện tích phủ bì sàn buồng thang (3.4.8 [SĐ1]).'
        ),
    },
    {
        'block': '🚶 Thoát nạn (Phần 3)',
        'id': 'r_tang_lanh_nan',
        'title': 'Tầng lánh nạn',
        'clause': '1.4.58',
        'sd1': False,
        'detail': (
            'Tầng lánh nạn là tầng dùng để sơ tán tạm thời, bố trí trong nhà có PCCC >100 m.\n'
            'Có bố trí một hoặc nhiều gian lánh nạn.\n\n'
            'Xem thêm yêu cầu chi tiết về gian lánh nạn và điều kiện kết cấu tại Phụ lục H.'
        ),
    },
    {
        'block': '🔥 Ngăn chặn cháy lan (Phần 4)',
        'id': 'r_ngan_cach_f13',
        'title': 'Ngăn cách nhà F1.3 với công năng khác',
        'clause': '4.5 [SĐ1]',
        'sd1': True,
        'detail': (
            'Nhà F1.3 (chung cư) phải được ngăn cách với các công năng khác bằng bộ phận ngăn cháy:\n'
            '• GHCL tối thiểu EI 45 – nhà bậc I÷III\n'
            '• GHCL tối thiểu EI 15 – nhà bậc IV\n\n'
            'Không yêu cầu ngăn cháy với: gian phòng F5 hạng C4, E; gian phòng kỹ thuật nước;\n'
            'gian phòng ẩm ướt hoặc nguy cơ cháy thấp [SĐ1].\n\n'
            'CHÚ THÍCH: Tường và vách ngăn giữa các đơn nguyên; tường và vách ngăn\n'
            'giữa hành lang chung và các phòng khác: GHCL ≥EI 45.'
        ),
    },
    {
        'block': '🔥 Ngăn chặn cháy lan (Phần 4)',
        'id': 'r_dai_ngan_chay',
        'title': 'Đai ngăn cháy phương đứng – Mặt ngoài nhà',
        'clause': '4.32.1 / 4.32.2 [SĐ1]',
        'sd1': True,
        'detail': (
            'Mặt ngoài nhà phải có đai ngăn cháy theo phương đứng (băng tường/bê tông không cháy)\n'
            'giữa các tầng:\n'
            '• Chiều cao ≥1,2 m – nhà bậc I, II\n'
            '• Chiều cao ≥0,9 m – nhà bậc III\n\n'
            '4.32.2 [SĐ1]: Cho phép không áp dụng 4.32.1 nếu nhà được trang bị chữa cháy tự động.'
        ),
    },
    {
        'block': '🔥 Ngăn chặn cháy lan (Phần 4)',
        'id': 'r_dai_ngang',
        'title': 'Dải ngăn cháy phương ngang – Mặt ngoài nhà',
        'clause': '4.33 / 4.33.4 [SĐ1]',
        'sd1': True,
        'detail': (
            'Mặt ngoài nhà phải có dải ngăn cháy theo phương ngang giữa khoang cháy hoặc giữa\n'
            'các bộ phận nhà có yêu cầu GHCL khác nhau:\n'
            '• Chiều cao ≥1,0 m – bậc I, II\n'
            '• Chiều cao ≥0,8 m – bậc III\n\n'
            '4.33.4 [SĐ1]: Cho phép không áp dụng 4.33 đối với:\n'
            '• Nhà ≤3 tầng hoặc PCCC <15 m\n'
            '• Ga ra để xe nổi dạng hở\n'
            '• Nhà được trang bị chữa cháy tự động'
        ),
    },
    {
        'block': '💧 Cấp nước chữa cháy (Phần 5)',
        'id': 'r_hong_nuoc',
        'title': 'Hệ thống họng nước chữa cháy trong nhà',
        'clause': '5.2.1, Bảng 11',
        'sd1': False,
        'detail': (
            'Điều kiện BẮT BUỘC trang bị hệ thống họng nước chữa cháy trong nhà (Bảng 11):\n'
            '• Nhà F1.3 cao >6 tầng\n'
            '• Nhà F1.1, F1.2 cao >2 tầng hoặc diện tích >500 m²\n'
            '• Nhà công cộng F2, F3, F4 cao >2 tầng hoặc có tầng hầm >500 m²\n'
            '• Nhà sản xuất và kho F5 hạng A, B, C diện tích >300 m²/tầng\n'
            '• Nhà dưỡng lão, Nhà hỗn hợp\n'
            '• Nhà có PCCC >15 m\n\n'
            'Áp suất tối đa tại họng: 0,6 MPa [SĐ1]; tối thiểu tại lăng phun: 0,45 MPa [SĐ1].'
        ),
    },
    {
        'block': '💧 Cấp nước chữa cháy (Phần 5)',
        'id': 'r_cctn',
        'title': 'Hệ thống chữa cháy tự động (Sprinkler)',
        'clause': '5.3, Bảng 12',
        'sd1': True,
        'detail': (
            'Điều kiện BẮT BUỘC trang bị chữa cháy tự động (Bảng 12):\n'
            '• Nhà F1.1÷F1.3 có PCCC >28 m\n'
            '• Nhà F2, F3 có PCCC >28 m hoặc diện tích >3.500 m²\n'
            '• Nhà F4 có PCCC >28 m\n'
            '• Một số trường hợp đặc biệt khác theo Bảng 12\n\n'
            'Hệ thống CCTN cũng được dùng để miễn giảm một số yêu cầu khác (4.32.2, 4.33.4).'
        ),
    },
    {
        'block': '🚒 Chữa cháy và cứu nạn (Phần 6)',
        'id': 'r_thang_may_cc',
        'title': 'Thang máy chữa cháy',
        'clause': '6.5',
        'sd1': False,
        'detail': (
            'BẮT BUỘC trang bị thang máy chữa cháy trong nhà có PCCC >28 m.\n\n'
            'Thang máy chữa cháy phải có:\n'
            '• Tải trọng ≥630 kg\n'
            '• Kích thước cabin ≥1,1 m × 2,1 m\n'
            '• Tốc độ đủ để đến tầng cao nhất ≤60 giây\n'
            '• Nguồn điện dự phòng\n'
            '• Bảo vệ bởi sảnh thang ngăn cháy (vách ngăn cháy loại 1 – 6.8)\n\n'
            'Kết cấu bao che giếng: GHCL ≥REI 60; cửa giếng thang: EI 30 (6.11).'
        ),
    },
    {
        'block': '🚒 Chữa cháy và cứu nạn (Phần 6)',
        'id': 'r_bai_do_xe',
        'title': 'Đường và bãi đỗ xe chữa cháy',
        'clause': '6.2 [SĐ1]',
        'sd1': True,
        'detail': (
            '• F1÷F4 có PCCC ≤15 m: không yêu cầu bãi đỗ, chỉ cần đường tiếp cận ≤60 m.\n'
            '• PCCC >15 m: cần bố trí bãi đỗ xe chữa cháy (kích thước theo Bảng 14).\n'
            '• F1.3 PCCC >15 m: đường cho xe ≤18 m từ điểm cuối đến lối vào khoang đệm thang máy/buồng thang.\n\n'
            'CHÚ THÍCH [SĐ1]: Không yêu cầu bãi đỗ với F1÷F4 có ≤50 người/tầng và\n'
            'khoảng cách từ đường xe đến họng tiếp nước phù hợp.\n\n'
            'Chiều cao thông thủy trên đường/bãi đỗ ≥4,5 m (6.2.1.3).'
        ),
    },
    {
        'block': '🚒 Chữa cháy và cứu nạn (Phần 6)',
        'id': 'r_loi_vao_cao',
        'title': 'Lối vào từ trên cao (6.3)',
        'clause': '6.3 [SĐ1]',
        'sd1': True,
        'detail': (
            'Tại các mặt nhà có bãi đỗ xe chữa cháy:\n'
            '• Cứ mỗi 20 m chiều dài nhà phải có ≥1 lỗ cửa (≥0,75 m × 1,5 m) hoặc cửa ban công\n'
            '• Chiều cao từ sàn tầng đến mép dưới lỗ cửa ≤1,2 m\n\n'
            'CHÚ THÍCH [SĐ1 – MỚI]: Không quy định về cách bố trí các lối vào từ trên cao\n'
            'khi có phương án phù hợp khác để lực lượng chữa cháy tiếp cận (6.3.5).'
        ),
    },
    {
        'block': '🚒 Chữa cháy và cứu nạn (Phần 6)',
        'id': 'r_khe_hor',
        'title': 'Khe hở về thang',
        'clause': '6.12 [SĐ1]',
        'sd1': True,
        'detail': (
            '6.12 [SĐ1] – Khe hở về thang:\n'
            'Ngưỡng chiều cao PCCC đã được Sửa đổi 1:2023 thay đổi từ 100 m xuống 75 m.\n\n'
            'Khi PCCC >75 m, nhà phải đáp ứng các yêu cầu về khe hở vế thang theo 6.12.\n'
            'Xem chi tiết tại điều 6.12 trong văn bản hợp nhất.'
        ),
    },
]

# Serialize metadata to JSON (handles all string escaping automatically)
rules_meta_js = json.dumps(RULES_META, ensure_ascii=False)
qcvn_data_js  = json.dumps(qcvn_data,  ensure_ascii=False, separators=(',', ':'))

# ===== CHECK FUNCTIONS (JavaScript code, không có chuỗi đa dòng) =====
CHECK_FUNCTIONS_JS = """
function nhomPrefix(nhom){return nhom ? nhom.substring(0,2) : '';}

const CHECKS = {
  r_loi_ra_so: function(inp){
    var warns=[];
    if(inp.so_nguoi>=50) warns.push('Gian phong co >=50 nguoi -> toi thieu 2 loi ra thoat nan');
    if(inp.tang_ham>0 && inp.so_nguoi>15) warns.push('Gian phong tang ham co >15 nguoi -> toi thieu 2 loi ra [SD1]');
    if(inp.dien_tich>1000 && inp.so_tang>=2) warns.push('Tang >=2 dien tich >1000 m2 hoac >50 nguoi -> toi thieu 2 loi ra');
    if(warns.length) return {type:'req', msg: warns.join('; ')};
    if(inp.so_nguoi>=25) return {type:'warn', msg:'25-49 nguoi/tang - kiem tra dieu kien 1 loi ra (3.2.6)'};
    return {type:'ok', msg:'Chua vuot nguong bat buoc 2 loi ra thoat nan'};
  },
  r_ban_thang: function(inp){
    var cc=inp.chieu_cao, nn=inp.so_nguoi, nhom=inp.nhom, p=nhomPrefix(nhom), msgs=[];
    if(nhom==='F1.1'){
      msgs.push(nn>15 ? 'F1.1 >15 nguoi/tang -> Ban thang >= 1,2 m' : 'F1.1 <=15 nguoi/tang -> Ban thang >= 1,0 m [SD1]');
    } else if(['F1.2','F1.3'].indexOf(nhom)>=0 || p==='F2' || p==='F3' || p==='F4'){
      if(cc>28) msgs.push('PCCC >28 m -> Ban thang >= 1,2 m');
      else if(cc<=15 && nn<=15) msgs.push('PCCC <=15 m va <=15 nguoi/tang -> Ban thang >= 0,7 m [SD1]');
      else msgs.push('Ban thang >= 0,9 m (truong hop con lai)');
    }
    if(msgs.length) return {type:'info', msg: msgs.join('; ')};
    return {type:'info', msg:'Chieu rong ban thang: xem 3.4.1 theo nhom nha va chieu cao PCCC'};
  },
  r_hanh_lang: function(inp){
    var cc=inp.chieu_cao, nhom=inp.nhom, p=nhomPrefix(nhom);
    var nhomF4 = (nhom==='F4.1');
    var isF123 = (nhom==='F1.1'||nhom==='F1.2'||nhom==='F1.3');
    var isF23  = (p==='F2'||p==='F3');
    if(cc>28 && (isF123||isF23||nhomF4))
      return {type:'info', msg:'PCCC >28 m -> Hanh lang >= 1,2 m'};
    if(p==='F1'||p==='F2'||p==='F3'||p==='F4')
      return {type:'info', msg:'Nhom F1-F4 (PCCC <=28 m) -> Hanh lang >= 1,0 m'};
    return {type:'info', msg:'Chieu rong hanh lang toi thieu 0,9 m (truong hop con lai)'};
  },
  r_buong_thang: function(inp){
    if(inp.chieu_cao>28)
      return {type:'req', msg:'PCCC >28 m -> Bat buoc dung buong thang khong nhiem khoi (H1 hoac H2 hoac H3)'};
    return {type:'info', msg:'PCCC <=28 m - co the dung buong thang thong thuong (L1, L2, L3)'};
  },
  r_tang_lanh_nan: function(inp){
    if(inp.chieu_cao>100)
      return {type:'req', msg:'PCCC >100 m -> Can bo tri tang lanh nan (gian lanh nan)'};
    return {type:'ok', msg:'PCCC <=100 m - khong bat buoc tang lanh nan'};
  },
  r_ngan_cach_f13: function(inp){
    if(inp.nhom!=='F1.3') return null;
    var bac=inp.bac;
    if(bac==='I'||bac==='II'||bac==='III')
      return {type:'req', msg:'Nha F1.3, bac I-III -> Ngan cach GHCL >= EI 45'};
    if(bac==='IV')
      return {type:'req', msg:'Nha F1.3, bac IV -> Ngan cach GHCL >= EI 15'};
    return {type:'req', msg:'Nha F1.3 -> Phai ngan cach voi cac cong nang khac (GHCL theo bac chiu lua - dieu 4.5)'};
  },
  r_dai_ngan_chay: function(inp){
    if(inp.cctn==='co')
      return {type:'ok', msg:'Co chua chay tu dong -> Duoc mien dai ngan chay phuong dung (4.32.2 [SD1])'};
    return {type:'req', msg:'Khong co CCTN -> Mat ngoai nha phai co dai ngan chay phuong dung >= 1,2 m (bac I,II) hoac >= 0,9 m (bac III)'};
  },
  r_dai_ngang: function(inp){
    if(inp.cctn==='co')
      return {type:'ok', msg:'Co chua chay tu dong -> Duoc mien dai ngan chay ngang (4.33.4 [SD1])'};
    if(inp.so_tang<=3 || inp.chieu_cao<15)
      return {type:'ok', msg:'Nha <=3 tang hoac PCCC <15 m -> Duoc mien dai ngan chay ngang (4.33.4 [SD1])'};
    return {type:'req', msg:'Mat ngoai nha phai co dai ngan chay ngang >= 1,0 m (bac I,II) hoac >= 0,8 m (bac III) giua cac khoang chay'};
  },
  r_hong_nuoc: function(inp){
    var nhom=inp.nhom, p=nhomPrefix(nhom), cc=inp.chieu_cao, st=inp.so_tang, dt=inp.dien_tich;
    var warns=[];
    if(nhom==='F1.3' && st>6) warns.push('F1.3 cao >6 tang');
    if((nhom==='F1.1'||nhom==='F1.2') && (st>2||dt>500)) warns.push('F1.1/F1.2 cao >2 tang hoac DT >500 m2');
    if((p==='F2'||p==='F3'||p==='F4') && (st>2||(inp.tang_ham>0&&dt>500))) warns.push('F2/F3/F4 cao >2 tang hoac tang ham DT >500 m2');
    if(p==='F5' && dt>300) warns.push('F5 hang A,B,C DT >300 m2/tang');
    if(cc>15) warns.push('PCCC >15 m');
    if(warns.length) return {type:'req', msg:'Bat buoc trang bi he thong hong nuoc chua chay trong nha: '+warns.join('; ')};
    return {type:'ok', msg:'Chua xac dinh yeu cau hong nuoc trong nha tu thong tin da nhap - kiem tra day du Bang 11'};
  },
  r_cctn: function(inp){
    var nhom=inp.nhom, p=nhomPrefix(nhom), cc=inp.chieu_cao, dt=inp.dien_tich;
    var warns=[];
    if(cc>28 && (p==='F1'||p==='F2'||p==='F3'||p==='F4')) warns.push('PCCC >28 m, nhom '+p);
    if((p==='F2'||p==='F3') && dt>3500) warns.push('F2/F3 DT >3500 m2');
    if(warns.length){
      if(inp.cctn==='co')   return {type:'ok',   msg:'Da co CCTN - dap ung yeu cau ('+warns.join('; ')+')'};
      if(inp.cctn==='khong') return {type:'req',  msg:'BAT BUOC chua chay tu dong: '+warns.join('; ')+'. Hien chua co!'};
      return                        {type:'warn', msg:'Co the bat buoc CCTN: '+warns.join('; ')+' - can xac nhan'};
    }
    if(inp.cctn==='co') return {type:'ok', msg:'Da co CCTN (khong bat buoc theo thong tin da nhap)'};
    return {type:'info', msg:'Chua xac dinh bat buoc CCTN - kiem tra day du Bang 12'};
  },
  r_thang_may_cc: function(inp){
    if(inp.chieu_cao>28)
      return {type:'req', msg:'PCCC >28 m -> BAT BUOC trang bi thang may chua chay'};
    return {type:'ok', msg:'PCCC <=28 m - khong bat buoc thang may chua chay'};
  },
  r_bai_do_xe: function(inp){
    var cc=inp.chieu_cao, p=nhomPrefix(inp.nhom);
    if(cc<=15 && (p==='F1'||p==='F2'||p==='F3'||p==='F4'))
      return {type:'info', msg:'F1-F4, PCCC <=15 m - Chi can duong tiep can den diem bat ky <=60 m'};
    if(cc>15)
      return {type:'req', msg:'PCCC >15 m -> Can bo tri bai do xe chua chay theo yeu cau 6.2 (kich thuoc theo Bang 14)'};
    return {type:'info', msg:'Kiem tra yeu cau duong/bai do xe chua chay theo 6.2 va Bang 14'};
  },
  r_loi_vao_cao: function(inp){
    if(inp.chieu_cao>15)
      return {type:'req', msg:'Can bo tri loi vao tu tren cao: cu moi 20 m chieu dai nha >= 1 lo cua (>=0,75 m x 1,5 m)'};
    return {type:'info', msg:'Kiem tra yeu cau loi vao tu tren cao theo 6.3 neu co bai do xe chua chay'};
  },
  r_khe_hor: function(inp){
    if(inp.chieu_cao>75)
      return {type:'req', msg:'PCCC >75 m -> Ap dung quy dinh ve khe ho ve thang (6.12 [SD1], nguong giam tu 100 m xuong 75 m)'};
    return {type:'ok', msg:'PCCC <=75 m - khong ap dung quy dinh khe ho ve thang'};
  }
};
"""

HTML = (
    '<!DOCTYPE html>\n'
    '<html lang="vi">\n'
    '<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '<title>QCVN 06:2022/BXD – Tra cứu an toàn cháy</title>\n'
    '<style>\n'
    '*{box-sizing:border-box;margin:0;padding:0}\n'
    "body{font-family:'Segoe UI',Arial,sans-serif;font-size:14px;background:#f0f2f5;color:#222}\n"
    'header{background:#1565C0;color:#fff;padding:12px 20px;display:flex;align-items:center;gap:12px}\n'
    'header h1{font-size:18px;font-weight:700;line-height:1.3}\n'
    'header p{font-size:12px;opacity:.8;margin-top:2px}\n'
    '.tabs{display:flex;background:#1976D2;padding:0 20px}\n'
    '.tab-btn{padding:10px 20px;color:#fff;border:none;background:none;cursor:pointer;font-size:14px;border-bottom:3px solid transparent;opacity:.75;font-weight:500}\n'
    '.tab-btn.active{opacity:1;border-bottom-color:#fff}\n'
    '.tab-content{display:none;padding:16px 20px;max-width:1200px;margin:0 auto}\n'
    '.tab-content.active{display:block}\n'
    '.form-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;background:#fff;border-radius:8px;padding:16px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.1)}\n'
    '.form-group label{display:block;font-size:12px;color:#555;margin-bottom:4px;font-weight:600}\n'
    '.form-group input,.form-group select{width:100%;border:1px solid #ccc;border-radius:4px;padding:7px 10px;font-size:14px;outline:none}\n'
    '.form-group input:focus,.form-group select:focus{border-color:#1565C0}\n'
    '.radio-group{display:flex;gap:16px;margin-top:4px}\n'
    '.radio-group label{font-size:14px;font-weight:normal;color:#222;cursor:pointer;display:flex;align-items:center;gap:4px}\n'
    '.btn-check{background:#1565C0;color:#fff;border:none;padding:10px 24px;border-radius:6px;cursor:pointer;font-size:15px;font-weight:600;margin-bottom:16px}\n'
    '.btn-check:hover{background:#1976D2}\n'
    '.btn-reset{background:#757575;color:#fff;border:none;padding:10px 16px;border-radius:6px;cursor:pointer;font-size:14px;margin-left:8px}\n'
    '#results-empty{color:#888;text-align:center;padding:32px;background:#fff;border-radius:8px}\n'
    '.results-wrapper{display:flex;flex-direction:column;gap:10px}\n'
    '.block-title{font-size:15px;font-weight:700;color:#1565C0;padding:8px 0 4px;border-bottom:2px solid #1565C0;margin-top:8px}\n'
    '.rule-card{background:#fff;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.1);overflow:hidden}\n'
    '.rule-card-header{display:flex;align-items:flex-start;gap:10px;padding:12px 14px;cursor:pointer;user-select:none}\n'
    '.rule-card-header:hover{background:#f5f7ff}\n'
    '.badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:700;white-space:nowrap;flex-shrink:0;margin-top:1px}\n'
    '.badge-ok{background:#E8F5E9;color:#2E7D32}\n'
    '.badge-info{background:#E3F2FD;color:#1565C0}\n'
    '.badge-warn{background:#FFF3E0;color:#E65100}\n'
    '.badge-req{background:#FFEBEE;color:#B71C1C}\n'
    '.rule-title{font-weight:600;font-size:14px;flex:1}\n'
    '.rule-clause{font-size:11px;color:#888;flex-shrink:0;margin-top:2px;white-space:nowrap}\n'
    '.rule-detail{padding:10px 14px 12px;font-size:13px;color:#444;line-height:1.7;display:none;border-top:1px solid #eee;white-space:pre-wrap}\n'
    '.rule-detail.open{display:block}\n'
    '.sd1-tag{background:#FFF8E1;color:#F57F17;font-size:11px;font-weight:700;border-radius:3px;padding:1px 5px;margin-left:6px}\n'
    '.rule-msg{font-weight:600;color:#333;margin-bottom:4px;font-size:13px}\n'
    '.rule-msg.ok{color:#2E7D32}\n'
    '.rule-msg.warn{color:#E65100}\n'
    '.rule-msg.req{color:#B71C1C}\n'
    '.rule-msg.info{color:#1565C0}\n'
    '.search-bar{display:flex;gap:8px;background:#fff;border-radius:8px;padding:12px;margin-bottom:12px;box-shadow:0 1px 4px rgba(0,0,0,.1);flex-wrap:wrap}\n'
    '.search-bar input{flex:1;min-width:200px;border:1px solid #ccc;border-radius:4px;padding:8px 12px;font-size:14px;outline:none}\n'
    '.search-bar input:focus{border-color:#1565C0}\n'
    '.filter-group{display:flex;gap:6px;flex-wrap:wrap;align-items:center}\n'
    '.filter-group span{font-size:12px;color:#666;font-weight:600}\n'
    '.chip{padding:4px 10px;border:1px solid #ccc;border-radius:14px;font-size:12px;cursor:pointer;background:#fff;user-select:none}\n'
    '.chip.active{background:#1565C0;color:#fff;border-color:#1565C0}\n'
    '.search-stats{font-size:12px;color:#888;padding:0 0 8px 2px}\n'
    '.entry-card{background:#fff;border-radius:6px;padding:10px 14px;margin-bottom:8px;box-shadow:0 1px 3px rgba(0,0,0,.08);line-height:1.6}\n'
    '.entry-card .ec-meta{font-size:11px;color:#888;margin-bottom:4px;display:flex;gap:8px;flex-wrap:wrap}\n'
    '.entry-card .ec-clause{font-weight:700;color:#1565C0}\n'
    '.ec-text{color:#333}\n'
    '.entry-card.is-heading{background:#E3F2FD}\n'
    '.entry-card.is-heading .ec-text{font-weight:700;color:#1565C0}\n'
    'mark{background:#FFF176;padding:0 2px;border-radius:2px}\n'
    '.no-results{text-align:center;padding:32px;color:#888;background:#fff;border-radius:8px}\n'
    '.disclaimer{background:#FFF3CD;border-left:4px solid #FFC107;padding:10px 16px;font-size:12px;color:#664D03;line-height:1.5}\n'
    '.disclaimer strong{color:#B45309}\n'
    'footer{background:#37474F;color:#CFD8DC;text-align:center;padding:14px 20px;font-size:12px;margin-top:24px}\n'
    'footer a{color:#80CBC4;text-decoration:none}\n'
    '@media(max-width:600px){.form-grid{grid-template-columns:1fr 1fr}header h1{font-size:15px}.tab-btn{padding:8px 12px;font-size:13px}}\n'
    '</style>\n'
    '</head>\n'
    '<body>\n'
    '<header>\n'
    '  <div style="font-size:32px;line-height:1">&#128293;</div>\n'
    '  <div>\n'
    '    <h1>QCVN 06:2022/BXD – An toàn cháy cho nhà và công trình</h1>\n'
    '    <p>Văn bản hợp nhất: Thông tư 06/2022/TT-BXD + Sửa đổi 1:2023 (TT 09/2023/TT-BXD)</p>\n'
    '  </div>\n'
    '</header>\n'
    '<div class="disclaimer">\n'
    '  <strong>&#9888; Lưu ý quan trọng:</strong> Công cụ này chỉ phục vụ mục đích <strong>tra cứu nhanh và tham khảo</strong>.\n'
    '  Nội dung không thể thay thế các văn bản pháp luật chính thức.\n'
    '  <strong>Không sử dụng làm căn cứ khi thẩm định hồ sơ phòng cháy chữa cháy.</strong>\n'
    '  Luôn đối chiếu với văn bản gốc do cơ quan có thẩm quyền ban hành.\n'
    '</div>\n'
    '<div class="tabs">\n'
    "  <button class=\"tab-btn active\" onclick=\"showTab('tab1',this)\">&#128203; Tra cứu theo dự án</button>\n"
    "  <button class=\"tab-btn\" onclick=\"showTab('tab2',this)\">&#128269; Tìm kiếm tự do</button>\n"
    '</div>\n'
    '<div id="tab1" class="tab-content active">\n'
    '  <div style="padding:12px 0 8px;font-size:13px;color:#555">Nhập thông tin nhà để tra cứu các yêu cầu PCCC áp dụng.</div>\n'
    '  <div class="form-grid">\n'
    '    <div class="form-group">\n'
    '      <label>Nhóm công năng</label>\n'
    '      <select id="f-nhom">\n'
    '        <option value="">-- Chọn nhóm --</option>\n'
    '        <optgroup label="F1 – Nhà ở">\n'
    '          <option value="F1.1">F1.1 – Nhà trẻ, mầm non; Bệnh viện, dưỡng lão</option>\n'
    '          <option value="F1.2">F1.2 – Khách sạn, nhà nghỉ, ký túc xá</option>\n'
    '          <option value="F1.3">F1.3 – Chung cư, nhà ở tập thể</option>\n'
    '          <option value="F1.4">F1.4 – Nhà ở riêng lẻ (1–2 gia đình)</option>\n'
    '        </optgroup>\n'
    '        <optgroup label="F2 – Giải trí, thể thao">\n'
    '          <option value="F2.1">F2.1 – Rạp chiếu phim, nhà hát</option>\n'
    '          <option value="F2.2">F2.2 – Vũ trường, cơ sở giải trí</option>\n'
    '          <option value="F2.3">F2.3 – Sân thể thao có mái che</option>\n'
    '          <option value="F2.4">F2.4 – Bảo tàng, triển lãm</option>\n'
    '        </optgroup>\n'
    '        <optgroup label="F3 – Dịch vụ, thương mại">\n'
    '          <option value="F3.1">F3.1 – Cửa hàng bán lẻ</option>\n'
    '          <option value="F3.2">F3.2 – Nhà hàng, ăn uống</option>\n'
    '          <option value="F3.3">F3.3 – Nhà ga, sân bay, bến cảng</option>\n'
    '          <option value="F3.4">F3.4 – Phòng khám, cơ sở y tế ngoại trú</option>\n'
    '          <option value="F3.5">F3.5 – Dịch vụ tiêu dùng</option>\n'
    '          <option value="F3.6">F3.6 – Khu liên hợp thể thao</option>\n'
    '        </optgroup>\n'
    '        <optgroup label="F4 – Giáo dục, văn phòng">\n'
    '          <option value="F4.1">F4.1 – Trường học các cấp</option>\n'
    '          <option value="F4.2">F4.2 – Đại học, cao đẳng, học viện</option>\n'
    '          <option value="F4.3">F4.3 – Văn phòng, cơ quan, ngân hàng</option>\n'
    '          <option value="F4.4">F4.4 – Trạm chữa cháy và cứu nạn</option>\n'
    '        </optgroup>\n'
    '        <optgroup label="F5 – Sản xuất, kho">\n'
    '          <option value="F5.1">F5.1 – Nhà sản xuất, xưởng</option>\n'
    '          <option value="F5.2">F5.2 – Nhà kho, ga ra</option>\n'
    '          <option value="F5.3">F5.3 – Nhà nông nghiệp</option>\n'
    '        </optgroup>\n'
    '      </select>\n'
    '    </div>\n'
    '    <div class="form-group"><label>Chiều cao PCCC (m)</label>'
    '<input type="number" id="f-chieu-cao" min="0" max="500" step="0.5" placeholder="Ví dụ: 25.5"></div>\n'
    '    <div class="form-group"><label>Số tầng nổi</label>'
    '<input type="number" id="f-so-tang" min="1" max="100" step="1" placeholder="Ví dụ: 10"></div>\n'
    '    <div class="form-group"><label>Số tầng hầm</label>'
    '<select id="f-tang-ham"><option value="0">0</option><option value="1">1</option>'
    '<option value="2">2</option><option value="3">3</option></select></div>\n'
    '    <div class="form-group"><label>Bậc chịu lửa</label>'
    '<select id="f-bac"><option value="">-- Chọn bậc --</option>'
    '<option value="I">Bậc I</option><option value="II">Bậc II</option>'
    '<option value="III">Bậc III</option><option value="IV">Bậc IV</option>'
    '<option value="V">Bậc V</option></select></div>\n'
    '    <div class="form-group"><label>Diện tích một tầng (m²)</label>'
    '<input type="number" id="f-dien-tich" min="0" step="1" placeholder="Ví dụ: 1500"></div>\n'
    '    <div class="form-group"><label>Số người tối đa / tầng</label>'
    '<input type="number" id="f-so-nguoi" min="0" step="1" placeholder="Ví dụ: 80"></div>\n'
    '    <div class="form-group" style="grid-column:1/-1">\n'
    '      <label>Có hệ thống chữa cháy tự động?</label>\n'
    '      <div class="radio-group">\n'
    '        <label><input type="radio" name="cctn" value="co"> Có</label>\n'
    '        <label><input type="radio" name="cctn" value="khong" checked> Không</label>\n'
    '        <label><input type="radio" name="cctn" value="chua_biet"> Chưa xác định</label>\n'
    '      </div>\n'
    '    </div>\n'
    '  </div>\n'
    '  <button class="btn-check" onclick="runCheck()">&#10004; Tra cứu</button>\n'
    '  <button class="btn-reset" onclick="resetForm()">&#8635; Xóa</button>\n'
    '  <div id="results-area" style="margin-top:12px">\n'
    '    <div id="results-empty" style="display:none;color:#888;text-align:center;padding:32px;background:#fff;border-radius:8px">'
    'Nhập thông tin nhà và nhấn <strong>Tra cứu</strong> để xem yêu cầu PCCC.</div>\n'
    '    <div id="results-wrapper" class="results-wrapper"></div>\n'
    '  </div>\n'
    '</div>\n'
    '<div id="tab2" class="tab-content">\n'
    '  <div class="search-bar">\n'
    '    <input type="text" id="s-query" placeholder="Tìm theo từ khóa: tầng hầm, thang máy, lối ra..." oninput="runSearch()">\n'
    '    <div class="filter-group"><span>Phần:</span>\n'
    '      <span class="chip active" data-sec="all" onclick="setSecFilter(this)">Tất cả</span>\n'
    '      <span class="chip" data-sec="1" onclick="setSecFilter(this)">1</span>\n'
    '      <span class="chip" data-sec="2" onclick="setSecFilter(this)">2</span>\n'
    '      <span class="chip" data-sec="3" onclick="setSecFilter(this)">3</span>\n'
    '      <span class="chip" data-sec="4" onclick="setSecFilter(this)">4</span>\n'
    '      <span class="chip" data-sec="5" onclick="setSecFilter(this)">5</span>\n'
    '      <span class="chip" data-sec="6" onclick="setSecFilter(this)">6</span>\n'
    '      <span class="chip" data-sec="7" onclick="setSecFilter(this)">7</span>\n'
    '    </div>\n'
    '    <div class="filter-group"><span>Phụ lục:</span>\n'
    '      <span class="chip" data-sec="A" onclick="setSecFilter(this)">A</span>\n'
    '      <span class="chip" data-sec="B" onclick="setSecFilter(this)">B</span>\n'
    '      <span class="chip" data-sec="C" onclick="setSecFilter(this)">C</span>\n'
    '      <span class="chip" data-sec="D" onclick="setSecFilter(this)">D</span>\n'
    '      <span class="chip" data-sec="E" onclick="setSecFilter(this)">E</span>\n'
    '      <span class="chip" data-sec="H" onclick="setSecFilter(this)">H</span>\n'
    '    </div>\n'
    '    <div class="filter-group">\n'
    '      <label style="font-size:12px;cursor:pointer">'
    '<input type="checkbox" id="s-sd1only" onchange="runSearch()"> Chỉ [SĐ1]</label>\n'
    '    </div>\n'
    '  </div>\n'
    '  <div class="search-stats" id="s-stats"></div>\n'
    '  <div id="s-results"></div>\n'
    '</div>\n'
    '<script>\n'
    'var QCVN_DATA = ' + qcvn_data_js + ';\n'
    'var RULES_META = ' + rules_meta_js + ';\n'
    + CHECK_FUNCTIONS_JS +
    """
// Gop metadata + check functions thanh RULES array
var RULES = RULES_META.map(function(m){
  var rule = Object.assign({}, m);
  rule.check = CHECKS[m.id] || function(){ return null; };
  return rule;
});

// ===== FORM INPUT =====
function getVal(id){ return document.getElementById(id).value.trim(); }
function getNum(id){ var v=parseFloat(getVal(id)); return isNaN(v)?0:v; }
function getInt(id){ var v=parseInt(getVal(id));   return isNaN(v)?0:v; }
function getCctn(){
  var r=document.querySelector('input[name="cctn"]:checked');
  return r ? r.value : 'khong';
}

// ===== CHAY KIEM TRA =====
function runCheck(){
  var nhom = getVal('f-nhom');
  if(!nhom){ alert('Vui long chon Nhom cong nang.'); return; }

  var inp = {
    nhom:      nhom,
    chieu_cao: getNum('f-chieu-cao'),
    so_tang:   Math.max(1, getInt('f-so-tang')),
    tang_ham:  parseInt(getVal('f-tang-ham'))||0,
    bac:       getVal('f-bac'),
    dien_tich: getNum('f-dien-tich'),
    so_nguoi:  getNum('f-so-nguoi'),
    cctn:      getCctn()
  };

  var wrapper = document.getElementById('results-wrapper');
  wrapper.innerHTML = '';
  document.getElementById('results-empty').style.display = 'none';

  var lastBlock = '';
  for(var i=0; i<RULES.length; i++){
    var rule   = RULES[i];
    var result = rule.check(inp);
    if(result === null) continue;

    if(rule.block !== lastBlock){
      var bt = document.createElement('div');
      bt.className = 'block-title';
      bt.textContent = rule.block;
      wrapper.appendChild(bt);
      lastBlock = rule.block;
    }

    var badgeClass = {ok:'badge-ok', info:'badge-info', warn:'badge-warn', req:'badge-req'}[result.type] || 'badge-info';
    var badgeText  = {ok:'&#10003; Khong yeu cau', info:'&#8505; Thong tin', warn:'&#9888; Chu y', req:'&#10007; Bat buoc'}[result.type] || '&#8505;';
    var sd1html = rule.sd1 ? '<span class="sd1-tag">SD1</span>' : '';
    var detailHtml = escapeHtml(rule.detail || '');

    var card = document.createElement('div');
    card.className = 'rule-card';

    var header = document.createElement('div');
    header.className = 'rule-card-header';
    header.onclick = function(){ toggleDetail(this); };
    header.innerHTML =
      '<span class="badge ' + badgeClass + '">' + badgeText + '</span>' +
      '<div style="flex:1">' +
        '<div class="rule-title">' + escapeHtml(rule.title) + sd1html + '</div>' +
        '<div class="rule-msg ' + result.type + '">' + escapeHtml(result.msg) + '</div>' +
      '</div>' +
      '<span class="rule-clause">' + escapeHtml(rule.clause) + '</span>';

    var detail = document.createElement('div');
    detail.className = 'rule-detail';
    detail.innerHTML = detailHtml;

    card.appendChild(header);
    card.appendChild(detail);

    wrapper.appendChild(card);
  }

  // Ghi chu cuoi
  var note = document.createElement('div');
  note.style.cssText = 'background:#FFF8E1;border-radius:8px;padding:12px 16px;font-size:13px;color:#5D4037;margin-top:8px;line-height:1.6';
  note.innerHTML = '<strong>Luu y:</strong> Ket qua mang tinh dinh huong. Mot so yeu cau phu thuoc hang nguy hiem chay (A/B/C/D/E) chua nhap va cac dieu kien cu the trong Phu luc H. Luon kiem tra van ban goc QCVN 06:2022/BXD truoc khi ap dung.';
  wrapper.appendChild(note);
}

function toggleDetail(headerEl){
  var detail = headerEl.nextElementSibling;
  if(detail) detail.classList.toggle('open');
}

function resetForm(){
  document.getElementById('f-nhom').value = '';
  document.getElementById('f-chieu-cao').value = '';
  document.getElementById('f-so-tang').value = '';
  document.getElementById('f-tang-ham').value = '0';
  document.getElementById('f-bac').value = '';
  document.getElementById('f-dien-tich').value = '';
  document.getElementById('f-so-nguoi').value = '';
  document.querySelector('input[name="cctn"][value="khong"]').checked = true;
  document.getElementById('results-wrapper').innerHTML = '';
  document.getElementById('results-empty').style.display = 'block';
}

// ===== TAB 2 – TIM KIEM =====
var secFilter = 'all';

function setSecFilter(el){
  document.querySelectorAll('.chip').forEach(function(c){ c.classList.remove('active'); });
  el.classList.add('active');
  secFilter = el.dataset.sec;
  runSearch();
}

function escapeHtml(s){
  if(!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function highlight(text, query){
  if(!query) return escapeHtml(text);
  var lower = text.toLowerCase(), qlen = query.length;
  var result = '', i = 0, pos;
  while((pos = lower.indexOf(query, i)) >= 0){
    result += escapeHtml(text.substring(i, pos));
    result += '<mark>' + escapeHtml(text.substring(pos, pos+qlen)) + '</mark>';
    i = pos + qlen;
  }
  result += escapeHtml(text.substring(i));
  return result;
}

function runSearch(){
  var query = (document.getElementById('s-query').value || '').trim().toLowerCase();
  var sd1only = document.getElementById('s-sd1only').checked;
  var entries = QCVN_DATA.entries;

  var results = entries.filter(function(e){
    if(sd1only && !e.sd1) return false;
    if(secFilter !== 'all'){
      if(e.section_type === 'phan' && String(e.section_key) !== secFilter) return false;
      if(e.section_type === 'phu_luc' && e.section_key !== secFilter) return false;
      if(e.section_type !== 'phan' && e.section_type !== 'phu_luc') return false;
    }
    if(query && e.text.toLowerCase().indexOf(query) < 0) return false;
    return true;
  });

  var MAX = 200;
  var total = results.length;
  results = results.slice(0, MAX);

  var stats = document.getElementById('s-stats');
  stats.textContent = total === 0 ? 'Khong tim thay ket qua.' :
    'Hien thi ' + results.length + ' / ' + total + ' ket qua' + (query ? ' cho "' + query + '"' : '') + '.';

  var container = document.getElementById('s-results');
  if(total === 0){
    container.innerHTML = '<div class="no-results">Khong tim thay. Thu tu khoa khac hoac bo bo loc.</div>';
    return;
  }

  container.innerHTML = results.map(function(e){
    var sd1span    = e.sd1 ? '<span class="sd1-tag">SD1</span>' : '';
    var clauseSpan = e.clause ? '<span class="ec-clause">&#167; ' + escapeHtml(e.clause) + '</span>' : '';
    var secSpan    = '<span class="ec-sec">' + escapeHtml(e.section_label.substring(0,30)) + '</span>';
    var hClass     = e.is_heading ? 'is-heading' : '';
    var textHtml   = highlight(e.text, query);
    return '<div class="entry-card ' + hClass + '">' +
             '<div class="ec-meta">' + clauseSpan + secSpan + sd1span + '</div>' +
             '<div class="ec-text">' + textHtml + '</div>' +
           '</div>';
  }).join('');
}

// ===== TABS =====
function showTab(id, btn){
  document.querySelectorAll('.tab-content').forEach(function(t){ t.classList.remove('active'); });
  document.querySelectorAll('.tab-btn').forEach(function(b){ b.classList.remove('active'); });
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
  if(id === 'tab2'){ runSearch(); }
}

// Khoi dong
document.getElementById('results-empty').style.display = 'block';
</script>
<footer>
  <p>&#128293; <strong>QCVN 06:2022/BXD Tra cứu</strong> &nbsp;|&nbsp; Tác giả: <strong>Võ Đỗ Hùng</strong></p>
  <p style="margin-top:6px;opacity:.8">
    Công cụ tra cứu nhanh, tham khảo. Không thay thế văn bản pháp luật chính thức.
    Không dùng làm căn cứ thẩm định hồ sơ PCCC.
  </p>
  <p style="margin-top:4px;opacity:.6;font-size:11px">
    Nguồn: Thông tư 06/2022/TT-BXD &amp; Thông tư 09/2023/TT-BXD (BXD) &nbsp;|&nbsp;
    Phiên bản nội dung có thể chưa cập nhật đầy đủ mọi sửa đổi.
  </p>
</footer>
</body>
</html>
"""
)

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(HTML)

# Cũng ghi index.html (dùng cho GitHub Pages)
INDEX_PATH = os.path.join(os.path.dirname(OUT_PATH), 'index.html')
with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(HTML)

size = os.path.getsize(OUT_PATH)
print('OK -> ' + OUT_PATH)
print('   -> ' + INDEX_PATH)
print('File size: ' + str(round(size/1024)) + ' KB')
