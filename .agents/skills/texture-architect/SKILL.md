---
name: texture-architect
description: Chuyên gia quản lý và tối ưu hóa Texture/Material, tự động tái sử dụng tài nguyên cũ hoặc sinh Texture mới có tính tái sử dụng cao (Seamless, Grayscale, Palette).
---
# Vai trò: Smart Texture & Material Optimization Architect

## Quy trình ra quyết định tự động (Bắt buộc)
Mỗi khi dự án cần màu sắc, bề mặt vật liệu cho nhân vật, đạo cụ (prop) hoặc bản đồ (map):

### Bước 1: Kiểm tra kho (`Assets/Textures/TEXTURE_CATALOG.md`)
- Đọc `Assets/Textures/TEXTURE_CATALOG.md` để xem các Texture và Material `.tres` hiện có.

### Bước 2: Đánh giá Tái sử dụng hay Tạo mới
1. **DÙNG LẠI NGAY (Reuse 100%)**: Nếu trong `Assets/Materials_Shared/` đã có sẵn vật liệu phù hợp (ví dụ: cỏ, đất, gỗ, kim loại), gắn trực tiếp file `.tres` đó vào Mesh/Node.
2. **BIẾN TẤU NHẸ (Reuse Texture + Tạo `.tres` mới 1KB)**: Nếu đã có vân bề mặt phù hợp trong `Grayscale_Masks/` hoặc `Tileable/` nhưng cần màu sắc khác hoặc độ nhám (`roughness`)/tỷ lệ lặp (`uv1_scale`) khác -> **KHÔNG tạo file ảnh `.png` mới**. Hãy tạo một file `.tres` (`StandardMaterial3D`) mới trong `Assets/Materials_Shared/`, trỏ vào file ảnh cũ và đổi thông số `albedo_color` / `uv1_scale`.
3. **TẠO MỚI CHỦ ĐỘNG (Create New Reusable Asset)**: Khi và chỉ khi bề mặt yêu cầu có họa tiết/chất liệu hoàn toàn khác biệt không thể dùng lại đồ cũ (ví dụ: cần vân gạch mới, mặt nước, vỏ cây, bảng màu mới):
   - Tự động viết script Python (dùng `PIL`/`numpy` hoặc Blender procedural) để sinh file ảnh `.png` mới.
   - **Thiết kế để tái sử dụng lâu dài**:
     * Ưu tiên tạo ảnh **Seamless (Tileable)** để lát được trên mọi diện tích.
     * Hoặc tạo ảnh **Grayscale (Trắng đen độ tương phản tốt)** lưu vào `Assets/Textures/Grayscale_Masks/` để sau này có thể pha ra hàng chục màu khác nhau bằng `albedo_color` trong Godot.
     * Độ phân giải chuẩn lũy thừa của 2 (`64x64` cho Palette, `256x256` hoặc `512x512` cho vân bề mặt) để nhẹ dung lượng và tối ưu VRAM.
   - Tạo kèm file `.tres` chuẩn trong `Assets/Materials_Shared/`.
   - **Cập nhật ngay lập tức** thông tin file ảnh và `.tres` vừa tạo vào `Assets/Textures/TEXTURE_CATALOG.md`.
