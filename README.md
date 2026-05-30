# 🔥 QCVN 06:2022/BXD – Tra cứu An toàn cháy

Công cụ tra cứu nhanh **QCVN 06:2022/BXD** tích hợp **Sửa đổi 1:2023** (TT 09/2023/TT-BXD).

**Tác giả:** Võ Đỗ Hùng

👉 **[Dùng ngay trên trình duyệt](https://vodohhung.github.io/qcvn06/)** _(cập nhật link sau khi deploy)_

---

## ⚠️ Tuyên bố miễn trách nhiệm

> Công cụ này chỉ phục vụ mục đích **tra cứu nhanh và tham khảo cá nhân**.
>
> - **Không thể thay thế** văn bản pháp luật chính thức.
> - **Không sử dụng làm căn cứ** khi thẩm định hồ sơ phòng cháy chữa cháy.
> - Luôn đối chiếu với văn bản gốc do cơ quan có thẩm quyền ban hành.
> - Nội dung có thể chưa cập nhật đầy đủ mọi sửa đổi.

---

## Tính năng

| Tab | Chức năng |
|-----|-----------|
| 📋 **Tra cứu theo dự án** | Nhập thông số nhà → hiển thị yêu cầu PCCC áp dụng (thang máy CC, CCTN, buồng thang, lối ra thoát nạn...) |
| 🔍 **Tìm kiếm tự do** | Full-text search toàn bộ QCVN 06, lọc theo Phần 1–7 và Phụ lục A–I, đánh dấu `[SĐ1]` |

Hoạt động **100% offline** sau khi tải về — không cần internet, không server.

---

## Cách dùng

**Dùng online:** Truy cập link ở trên (điện thoại / máy tính đều được).

**Dùng offline:** Tải file `index.html` → mở bằng Chrome/Edge/Firefox.

---

## Góp ý và báo lỗi

Nội dung còn nhiều lỗi chính tả từ quá trình xử lý tự động. Rất mong nhận được góp ý!

- 🐛 **Báo lỗi nội dung / chính tả:** [Tạo Issue mới](../../issues/new?template=bao-loi-noi-dung.md&labels=noi-dung)
- 💡 **Đề xuất tính năng:** [Tạo Issue mới](../../issues/new?template=de-xuat-tinh-nang.md&labels=enhancement)
- ✏️ **Sửa trực tiếp:** Fork repo → sửa `QCVN06_Content.md` → gửi Pull Request

**Cách báo lỗi nội dung nhanh nhất:**
1. Nhấn tab **Issues** ở trên
2. Nhấn **New Issue**
3. Ghi rõ: số điều khoản, nội dung hiện tại, nội dung đúng

---

## Nguồn pháp lý

- **QCVN 06:2022/BXD** – Thông tư 06/2022/TT-BXD ngày 30/11/2022, hiệu lực 16/01/2023
- **Sửa đổi 1:2023** – Thông tư 09/2023/TT-BXD ngày 16/10/2023, hiệu lực 01/12/2023

---

## Files trong repo

| File | Mục đích |
|------|----------|
| `index.html` | App tra cứu — **tải về và dùng ngay** |
| `QCVN06_Content.md` | Nội dung QCVN 06 — chỉnh sửa để đóng góp |
| `rebuild.py` | Rebuild `index.html` từ `QCVN06_Content.md` |
| `build_app.py` | Build engine |

---

*Phiên bản nội dung: QCVN 06:2022/BXD + Sửa đổi 1:2023*
