# QCVN 06:2022/BXD – Tra cứu An toàn cháy PCCC

Công cụ tra cứu **QCVN 06:2022/BXD** tích hợp **Sửa đổi 1:2023** (TT 09/2023/TT-BXD), kết hợp tra cứu **QCVN 10:2025/BCA**, **TCVN 7336:2021** và **NĐ 105/2025/NĐ-CP**.

**Tác giả:** Võ Đỗ Hùng

**[Dùng ngay trên trình duyệt](https://hvdo42.github.io/qcvn06-tra-cuu/)**

---

## Tuyên bố miễn trách nhiệm

> Công cụ này chỉ phục vụ mục đích **tra cứu nhanh và tham khảo cá nhân**.
>
> - **Không thể thay thế** văn bản pháp luật chính thức.
> - **Không sử dụng làm căn cứ** khi thẩm định hồ sơ phòng cháy chữa cháy.
> - Luôn đối chiếu với văn bản gốc do cơ quan có thẩm quyền ban hành.

---

## Tính năng

### Tab 1 — Tra cứu theo dự án

Nhập thông số nhà (nhóm F1÷F5, chiều cao PCCC, số tầng, diện tích...) → app tính và hiển thị đồng thời:

| Kết quả | Căn cứ |
|---------|--------|
| Yêu cầu kiến trúc PCCC (thang máy CC, buồng thang, lối ra thoát nạn, bậc chịu lửa...) | QCVN 06:2022/BXD + SĐ1:2023 |
| Trang bị phương tiện PCCC bắt buộc (báo cháy, chữa cháy, hút khói, ĐBBX...) | QCVN 10:2025/BCA |
| Thông số thiết kế hệ thống Sprinkler (nhóm nguy cơ, cường độ phun, lưu lượng...) | TCVN 7336:2021 |
| Tư vấn đánh đổi thiết kế (thay thế báo cháy, rút gọn phạm vi Sprinkler...) | QCVN 10:2025 + TCVN 7336:2021 |
| Phạm vi thẩm định thiết kế PCCC + cơ quan có thẩm quyền | NĐ 105/2025/NĐ-CP |
| Bảo hiểm cháy, nổ bắt buộc + mức phí tối thiểu | NĐ 105/2025 + NĐ 67/2023 |

### Tab 2 — Hành trình pháp lý

Sơ đồ 7 bước tuân thủ PCCC trong vòng đời dự án đầu tư xây dựng, kèm ma trận 4 văn bản pháp lý theo từng giai đoạn.

### Tab 3 — Thư viện thẩm duyệt

Danh mục nội dung cần đối chiếu khi thẩm duyệt PCCC, theo từng loại công trình (43 bộ kiến trúc, 36 bộ hệ thống).

### Tab 4 — Tìm kiếm tự do

Full-text search toàn bộ QCVN 06:2022/BXD, lọc theo Phần 1–7 và Phụ lục A–I, đánh dấu `[SĐ1]`.

---

## Cách dùng

**Dùng online:** Truy cập link ở trên (điện thoại / máy tính đều được).

**Dùng offline (không cần mạng):** Tải file `local/index.html` từ repo về máy → mở bằng Chrome/Edge/Firefox — hoạt động 100% standalone.

---

## Góp ý và báo lỗi

- **Báo lỗi nội dung / chính tả:** Tạo Issue mới, ghi rõ số điều khoản, nội dung hiện tại, nội dung đúng
- **Đề xuất tính năng:** Tạo Issue mới

---

## Tính năng

| Tab | Chức năng |
|-----|-----------|
| **Tra cứu theo dự án** | Nhập thông số nhà → hiển thị yêu cầu PCCC áp dụng (thang máy CC, CCTN, buồng thang, lối ra thoát nạn...) |
| **Tìm kiếm tự do** | Full-text search toàn bộ QCVN 06, lọc theo Phần 1–7 và Phụ lục A–I, đánh dấu `[SĐ1]` |
| **Thư viện thẩm duyệt** | Danh mục nội dung cần đối chiếu khi thẩm duyệt PCCC, theo loại công trình |

---

## Cách dùng

**Dùng online:** Truy cập link ở trên (điện thoại / máy tính đều được).

**Dùng offline (không cần mạng):** Tải file `local/index.html` từ repo về máy → mở bằng Chrome/Edge/Firefox — hoạt động 100% standalone.

---

## Góp ý và báo lỗi

- **Báo lỗi nội dung / chính tả:** Tạo Issue mới, ghi rõ số điều khoản, nội dung hiện tại, nội dung đúng
- **Đề xuất tính năng:** Tạo Issue mới

---

## Nguồn pháp lý

| Văn bản | Hiệu lực |
|---------|----------|
| QCVN 06:2022/BXD (TT 06/2022/TT-BXD) | 16/01/2023 |
| Sửa đổi 1:2023 (TT 09/2023/TT-BXD) | 01/12/2023 |
| QCVN 10:2025/BCA (TT 103/2025/TT-BCA) | 01/7/2025 |
| TCVN 7336:2021 | Hiện hành |
| NĐ 105/2025/NĐ-CP | 01/7/2025 |

---

## Files trong repo GitHub Pages

| File | Mục đích | Kích thước |
|------|----------|-----------|
| `index.html` | App web — cần kèm `app_data.json` | ~121 KB |
| `app_data.json` | Dữ liệu QCVN 06 — browser cache sau lần đầu | ~6.4 MB |
| `local/index.html` | Bản offline standalone — tải về dùng không cần mạng | ~6.5 MB |
