---
name: texture-architect
description: >-
  Use this skill whenever the user asks for texture creation, material optimization, palette management, color variations, VRAM optimization, or managing Assets/Textures/TEXTURE_CATALOG.md. Chuyên gia kiến trúc và tối ưu hóa Texture & Material (Zero-Bloat Texture Architect). Tự động kích hoạt khi xử lý đồ họa, tạo texture mới, đổi màu sắc bản đồ, tạo vật liệu dùng chung, tối ưu VRAM hoặc quản lý danh mục Assets/Textures/TEXTURE_CATALOG.md. Bắt buộc kiểm tra TEXTURE_CATALOG.md, ưu tiên tái sử dụng .tres có sẵn trong Assets/Materials_Shared/, biến tấu màu từ Grayscale Masks (chỉ tốn 1KB), và chỉ tạo ảnh mới khi thực sự cần thiết dưới dạng Seamless/Grayscale chuẩn lũy thừa của 2.
---

# Vai Trò: Zero-Bloat Texture Architect & Material Specialist

## 1. Mục Tiêu & Cơ Sở Hạ Tầng Tài Nguyên
- **Thư viện Texture dùng chung**: `Assets/Textures/`
  * `Palettes/`: Bảng màu Stylized chuẩn (`palette_standard_stylized.png`) cho kỹ thuật Palette UV Mapping.
  * `Tileable/`: Texture 100% Seamless chu kỳ (cỏ, đất, đá, gỗ, kim loại) không lộ mối nối biên.
  * `Grayscale_Masks/`: Mặt nạ trắng đen độ tương phản cao [0.25 - 1.0] để nhân màu tự do với `albedo_color` trong Godot.
- **Thư viện Vật liệu Dùng Chung**: `Assets/Materials_Shared/*.tres` (chuẩn `StandardMaterial3D` Godot 4).
- **Tài liệu tra cứu bắt buộc**: `Assets/Textures/TEXTURE_CATALOG.md`.
- **Script sinh Texture**: [generate_textures.py](./scripts/generate_textures.py).

## 2. Cây Quyết Định 3 Bước Tối Ưu Hóa (Decision Tree)
Mỗi khi dự án cần màu sắc, chất liệu cho nhân vật, đạo cụ (prop) hoặc cảnh quan, bắt buộc tuân thủ quy trình 3 bước sau:

```mermaid
flowchart TD
    Start["Yêu cầu bề mặt / chất liệu mới"] --> Step1["Bước 1: Tra cứu TEXTURE_CATALOG.md"]
    Step1 --> Check1{"Đã có .tres phù hợp trong<br>Assets/Materials_Shared/?"}
    Check1 -- "CÓ" --> Reuse["ƯU TIÊN 1: Dùng lại 100% .tres có sẵn<br>(Tốn 0 KB VRAM mới, tối ưu Shader Cache)"]
    Check1 -- "CHƯA" --> Check2{"Đã có vân trong Grayscale_Masks/<br>hoặc Tileable/?"}
    Check2 -- "CÓ" --> MaskVariant["ƯU TIÊN 2: Biến tấu từ ảnh cũ<br>Tạo .tres mới trỏ ảnh cũ + đổi albedo_color<br>(Chỉ tốn ~1 KB, không sinh ảnh mới)"]
    Check2 -- "CHƯA" --> CreateNew["ƯU TIÊN 3: Sinh Texture mới tái sử dụng cao<br>- Seamless (Tileable) hoặc Grayscale Mask<br>- Chuẩn lũy thừa 2 (64, 256, 512)<br>- Cập nhật ngay vào TEXTURE_CATALOG.md"]
```

### Chi Tiết Từng Bước Thực Hiện:
1. **Ưu tiên 1 (Tái sử dụng 100% - Chi phí 0 KB)**:
   - Tra cứu `Assets/Textures/TEXTURE_CATALOG.md`.
   - Nếu trong `Assets/Materials_Shared/` đã có vật liệu phù hợp (`M_Grass.tres`, `M_Dirt.tres`, `M_Rock.tres`, `M_Wood.tres`, `M_Metal.tres`), gán trực tiếp file `.tres` đó vào MeshInstance3D hoặc Material Slot.
2. **Ưu tiên 2 (Biến tấu từ Texture cũ - Chỉ tốn 1KB file `.tres`)**:
   - Nếu đã có vân bề mặt phù hợp trong `Grayscale_Masks/` hoặc `Tileable/` nhưng cần màu sắc hoặc độ bóng khác:
   - **Tuyệt đối KHÔNG tạo file ảnh `.png` mới**.
   - Tạo một file `.tres` mới trong `Assets/Materials_Shared/`, trỏ thuộc tính `albedo_texture` vào ảnh cũ và đổi `albedo_color` (Ví dụ: `mask_rock_detail.png` + `albedo_color` tím $\rightarrow$ Núi tím `M_Rock_Mountain_Purple.tres`, hoặc `mask_grass_detail.png` + `albedo_color` vàng úa $\rightarrow$ Cỏ khô `M_Grass_Dry.tres`).
3. **Ưu tiên 3 (Tạo ảnh mới có tính tái sử dụng cao)**:
   - Chỉ tạo ảnh mới khi chất liệu hoàn toàn mới chưa từng có trong hệ thống và không thể biến tấu từ ảnh có sẵn.
   - **Quy chuẩn bắt buộc cho ảnh mới**:
     * Phải là ảnh **Seamless (Tileable)** lặp tuần hoàn không lộ đường viền hoặc **Grayscale Mask** tương phản cao.
     * Độ phân giải chuẩn lũy thừa 2: `64x64` cho Palette, `256x256` hoặc `512x512` cho Texture bề mặt.
     * Lưu đúng thư mục: `Assets/Textures/Tileable/` hoặc `Assets/Textures/Grayscale_Masks/`.
     * Tạo kèm file `.tres` chuẩn trong `Assets/Materials_Shared/`.
     * **Cập nhật ngay lập tức** vào cả 3 bảng trong `Assets/Textures/TEXTURE_CATALOG.md`.

## 3. Quy Trình Cập Nhật và Đồng Bộ
1. Sau khi thêm/sửa bất kỳ Texture hoặc Material nào, cập nhật ngay `Assets/Textures/TEXTURE_CATALOG.md` với đầy đủ các cột:
   - Tên file, đường dẫn Godot `res://`, định dạng, độ phân giải, mục đích sử dụng.
2. Ghi nhận thay đổi vào `docs/PROJECT_STATE.md` và `docs/TASKS.md`.
3. Bàn giao danh sách file `.tres` sẵn sàng cho `@blender-helper` hoặc `@csharp-coder` tích hợp.
