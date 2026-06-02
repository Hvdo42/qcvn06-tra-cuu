# Hướng dẫn bổ sung nội dung còn thiếu
> Sau khi nhập xong từng bảng, chạy `python rebuild.py` để cập nhật app.

---

## Cách nhập bảng vào QCVN06_Content.md

Mở `QCVN06_Content.md`, tìm đến tiêu đề bảng tương ứng (ví dụ `**Bảng H.1**`), rồi thêm dữ liệu bảng ngay bên dưới theo định dạng Markdown:

```
**Bảng H.1 - Nhà ở và ký túc xá kiểu căn hộ**

| Bậc chịu lửa | Cấp nguy hiểm cháy KC | Chiều cao PCCC tối đa (m) | Diện tích khoang cháy tối đa (m²) |
|---|---|---|---|
| I   | S0, S1 | Không hạn chế | Không hạn chế |
| II  | S0, S1 | 75            | 2500          |
| III | S0, S1 | 28            | 1200          |
...
```

---

## NHÓM A – Bảng số liệu (ưu tiên cao nhất)

### A1. Bảng 4 – Giới hạn chịu lửa tối thiểu theo bậc chịu lửa
**Vị trí trong Content.md:** Tìm `Bảng 4 - Sự phù hợp giữa bậc chịu lửa`
**Nguồn:** File Word gốc `QCVN 06.2022.BXD.doc` → Phần 2 → Bảng 4 [SĐ1]
**Cần nhập:** Bảng gồm 5 bậc (I–V) × các cấu kiện (cột, dầm, sàn, tường chịu lực, tường ngoài, mái)
**Trạng thái:** 🔲 Chưa có

---

### A2. Bảng H.1 – Nhà ở và ký túc xá kiểu căn hộ (F1.3)
**Vị trí:** Phụ lục H → H.1
**Nguồn:** Word → Phụ lục H → Bảng H.1
**Cần nhập:** Bậc chịu lửa | Cấp KC | Chiều cao PCCC max (m) | Diện tích khoang cháy max (m²)
**Trạng thái:** 🔲 Chưa có

---

### A3. Bảng H.2 – Nhà công cộng tổng hợp
**Vị trí:** Phụ lục H → H.2.1
**Nguồn:** Word → Phụ lục H → Bảng H.2
**Cần nhập:** Như H.1
**Trạng thái:** 🔲 Chưa có

---

### A4. Bảng H.3 → H.14 – Từng loại nhà công cộng
**Cần nhập:** Tương tự H.1/H.2
**Nguồn:** Word → Phụ lục H

| Bảng | Nhóm nhà | Trạng thái |
|------|----------|-----------|
| H.3  | Cơ sở dịch vụ F3.5 | 🔲 |
| H.4  | Cơ sở thương mại F3.1 | 🔲 |
| H.5  | Nhà trẻ, mầm non | 🔲 |
| H.6  | Trường học F4.1 | 🔲 |
| H.7  | Bệnh viện, dưỡng lão F1.1 | 🔲 |
| H.8  | Nhà hát, rạp F2.1 | 🔲 |
| H.9  | Văn phòng F4.3 | 🔲 |
| H.10 | Nhà sản xuất F5.1 | 🔲 |
| H.11 | Nhà kho F5.2 | 🔲 |

---

### A5. Bảng G.1–G.9 – Khoảng cách và chiều rộng thoát nạn
**Vị trí:** Phụ lục G
**Nguồn:** Word → Phụ lục G
**Cần nhập:** Các bảng G.1–G.9 (khoảng cách theo loại nhà, số người, bậc CLF...)

| Bảng | Nội dung | Trạng thái |
|------|----------|-----------|
| G.1  | Khoảng cách thoát nạn – nhà ở F1.2/F1.3 | 🔲 |
| G.2a | Khoảng cách – công trình CC (theo loại) | 🔲 |
| G.2b | Khoảng cách – gian phòng CC không ghế cố định | 🔲 |
| G.3  | Khoảng cách – nhà sản xuất F5 (theo thể tích, hạng) | 🔲 |
| G.4  | Khoảng cách – gian phòng SX diện tích ≤1000m² | 🔲 |
| G.9  | Chiều rộng lối ra thoát nạn (theo số người) | 🔲 |

---

### A6. Bảng F.1–F.7 – GHCL danh định cấu kiện
**Vị trí:** Phụ lục F
**Nguồn:** Word → Phụ lục F
**Cần nhập:** Chiều dày lớp bảo vệ / kích thước tiết diện → GHCL đạt được

| Bảng | Cấu kiện | Trạng thái |
|------|----------|-----------|
| F.1  | Tường xây hoặc bê tông (chiều dày → GHCL) | 🔲 |
| F.2  | Tường ngoài không chịu lực | 🔲 |
| F.3  | Dầm BTCT (a_min, b_min → GHCL) | 🔲 |
| F.4  | Dầm BTCT ứng suất trước | 🔲 |
| F.5  | Cột BTCT 4 mặt tiếp xúc lửa | 🔲 |
| F.6  | Cột BTCT 1 mặt tiếp xúc lửa | 🔲 |
| F.7  | Cột thép bọc bảo vệ | 🔲 |

---

### A7. Bảng 11 – Điều kiện trang bị họng nước chữa cháy trong nhà
**Vị trí:** Phần 5 → 5.2 → Bảng 11
**Nguồn:** Word → Phần 5 → Bảng 11
**Cần nhập:** Nhóm nhà | Số tầng | Diện tích | Yêu cầu họng nước
**Trạng thái:** 🔲

---

### A8. Bảng 12 – Điều kiện trang bị chữa cháy tự động
**Vị trí:** Phần 5 → 5.3 → Bảng 12
**Nguồn:** Word → Phần 5 → Bảng 12
**Cần nhập:** Nhóm nhà | Điều kiện (chiều cao, diện tích) → bắt buộc CCTN
**Trạng thái:** 🔲

---

## NHÓM B – Điều khoản [SĐ1] cần cập nhật text

Các điều khoản sau đang hiển thị text gốc từ TT 06/2022. Cần thay bằng text mới từ TT 09/2023.

**Nguồn:** File `QCVN_06_2022_BXD_Hop_Nhat.docx` (đã có sẵn trong thư mục)

| Điều khoản | Nội dung sửa đổi | Trạng thái |
|-----------|-----------------|-----------|
| 1.1.2     | Phạm vi áp dụng – bổ sung nhà ở riêng lẻ | 🔲 |
| 1.1.11    | Điều khoản MỚI: địa phương ban hành QCKT địa phương | 🔲 |
| 3.2.5b    | Ngưỡng tầng hầm: >5 người → >15 người | 🔲 |
| 3.4.1     | Thêm trường hợp bản thang ≥0,7m (nhà ≤15m, ≤15 người) | 🔲 |
| 3.5.10    | Sửa toàn diện yêu cầu vật liệu hoàn thiện | 🔲 |
| 4.5       | Ngăn cách F1.3: EI 45 (bậc I–III) / EI 15 (bậc IV) | 🔲 |
| 5.1.5.9   | Bán kính phục vụ họng nước: 200m → 400m | 🔲 |
| 6.12      | Khe hở vế thang: ngưỡng >100m → >75m | 🔲 |
| H.2.9.1   | Bệnh viện PCCC >28m: điều kiện bổ sung | 🔲 |
| H.7       | Bổ sung MỚI: yêu cầu bổ sung một số trường hợp khác | 🔲 |
| A.3.2.2   | Bổ sung MỚI: vùng an toàn loại 1–4 | 🔲 |

---

## NHÓM C – Nội dung thiếu hoàn toàn

| Phụ lục / Bảng | Nội dung | Mức độ ưu tiên |
|----------------|----------|---------------|
| Bảng B.6       | Yêu cầu vật liệu hoàn thiện theo nhóm nhà + bậc CLF | Trung bình |
| Bảng C.1–C.3   | Hạng nguy hiểm cháy A/B/C/D/E theo loại vật liệu/sản phẩm | Thấp |
| Bảng E.1–E.2   | Khoảng cách phòng cháy giữa các nhà (theo bậc chịu lửa) | Trung bình |

---

## Khi bạn cập nhật xong một bảng

1. Mở `QCVN06_Content.md` bằng VS Code
2. Tìm đến tiêu đề bảng (Ctrl+F → "Bảng H.1")
3. Thêm dữ liệu bảng theo định dạng Markdown table bên dưới tiêu đề
4. Đánh dấu `✅` vào file này
5. Chạy `python rebuild.py` để cập nhật app
