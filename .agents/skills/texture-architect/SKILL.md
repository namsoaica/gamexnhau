---
name: texture-architect
description: >-
  Chuyên gia kiến trúc và tối ưu hóa Texture & Material (Zero-Bloat Texture Architect). Tự động kích hoạt khi người dùng yêu cầu xử lý đồ họa, tạo texture mới, đổi màu sắc bản đồ, tạo vật liệu dùng chung, tối ưu VRAM hoặc quản lý danh mục Assets/Textures/TEXTURE_CATALOG.md. Bắt buộc kiểm tra TEXTURE_CATALOG.md, ưu tiên tái sử dụng .tres có sẵn trong Assets/Materials_Shared/, biến tấu màu từ Grayscale Masks (chỉ tốn 1KB), và chỉ tạo ảnh mới khi thực sự cần thiết dưới dạng Seamless/Grayscale chuẩn lũy thừa của 2.
---

# Vai Trò: Smart Texture & Material Optimization Architect

## 1. Mục Tiêu & Cơ Sở Hạ Tầng Tài Nguyên
- **Thư viện Texture**: `Assets/Textures/`
  * `Palettes/`: Bảng màu chuẩn Stylized (`palette_standard_stylized.png`).
  * `Tileable/`: Texture 100% Seamless chu kỳ (cỏ, đất, đá, gỗ, kim loại).
  * `Grayscale_Masks/`: Mặt nạ trắng đen tương phản cao [0.25 - 1.0] để đổi màu tự do bằng `albedo_color` trong Godot.
- **Thư viện Vật liệu Dùng Chung**: `Assets/Materials_Shared/*.tres` (StandardMaterial3D Godot 4).
- **Tài liệu tra cứu bắt buộc**: `Assets/Textures/TEXTURE_CATALOG.md`.

## 2. Quy Trình Ra Quyết Định Tối Ưu Hóa (Cây Quyết Định 3 Bước)
Mỗi khi dự án cần màu sắc, chất liệu cho nhân vật, đạo cụ (prop) hoặc cảnh quan:

```mermaid
flowchart TD
    Start["Yêu cầu bề mặt / chất liệu mới"] --> Step1["Bước 1: Tra cứu TEXTURE_CATALOG.md"]
    Step1 --> Check1{"Đã có .tres phù hợp trong<br>Assets/Materials_Shared/?"}
    Check1 -- "CÓ" --> Reuse["ƯU TIÊN 1: Dùng lại 100% .tres có sẵn<br>(Tốn 0 KB, Shader Cache tối ưu)"]
    Check1 -- "CHƯA" --> Check2{"Đã có vân trong Grayscale_Masks/<br>hoặc Tileable/?"}
    Check2 -- "CÓ" --> MaskVariant["ƯU TIÊN 2: Biến tấu từ ảnh cũ<br>Tạo .tres mới trỏ ảnh cũ + đổi albedo_color<br>(Chỉ tốn ~1 KB, không sinh ảnh mới)"]
    Check2 -- "CHƯA" --> CreateNew["ƯU TIÊN 3: Sinh Texture mới tái sử dụng cao<br>- Seamless (Tileable) hoặc Grayscale Mask<br>- Chuẩn lũy thừa 2 (64, 256, 512)<br>- Cập nhật ngay vào TEXTURE_CATALOG.md"]
```

### Chi Tiết Từng Bước:
1. **Ưu tiên 1 (Tái sử dụng 100% - Không tốn tài nguyên)**:
   - Nếu trong `Assets/Materials_Shared/` đã có sẵn vật liệu phù hợp (`M_Grass.tres`, `M_Dirt.tres`, `M_Rock.tres`, `M_Wood.tres`, `M_Metal.tres`), gắn trực tiếp file `.tres` đó vào Mesh/Node.
2. **Ưu tiên 2 (Biến tấu từ Texture cũ - Chỉ tốn 1KB file `.tres`)**:
   - Nếu đã có vân bề mặt phù hợp trong `Grayscale_Masks/` hoặc `Tileable/` nhưng cần màu sắc khác:
   - **TUYỆT ĐỐI KHÔNG** tạo file ảnh `.png` mới.
   - Hãy tạo một file `.tres` mới trong `Assets/Materials_Shared/`, trỏ vào file ảnh cũ và nhân với `albedo_color` trong Godot (Ví dụ: `mask_rock_detail.png` + `albedo_color` tím $\rightarrow$ Núi tím `M_Rock_Mountain_Purple.tres`).
3. **Ưu tiên 3 (Tạo ảnh mới có tính tái sử dụng cao)**:
   - Khi và chỉ khi chất liệu hoàn toàn mới chưa từng có trong thư viện:
   - Viết script Python (dùng `generate_textures.py` với thư viện `PIL`/`numpy`) để tạo ảnh.
   - **Quy chuẩn bắt buộc cho ảnh mới**:
     * Phải là ảnh **Seamless (Tileable)** lặp tuần hoàn không lộ mối nối hoặc **Grayscale Mask** trắng đen độ tương phản cao.
     * Kích thước chuẩn lũy thừa 2: `64x64` cho bảng màu Palette, `256x256` hoặc `512x512` cho bề mặt vân.
     * Lưu đúng thư mục: `Assets/Textures/Tileable/` hoặc `Assets/Textures/Grayscale_Masks/`.
     * Tạo kèm file `.tres` chuẩn trong `Assets/Materials_Shared/`.
     * **Cập nhật ngay lập tức** vào cả 3 bảng trong `Assets/Textures/TEXTURE_CATALOG.md`.
