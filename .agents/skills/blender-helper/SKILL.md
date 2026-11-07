---
name: blender-helper
description: >-
  Use this skill whenever the user asks to manipulate 3D models, edit Blender geometry, unwrap UVs, configure materials, or export .glb assets for Godot 4. Trợ lý kỹ thuật 3D Blender (Zero-Bloat Asset Pipeline). Tự động kích hoạt khi thao tác 3D, chỉnh sửa mô hình bản đồ/nhân vật, xuất file .glb chuẩn Godot 4. Bắt buộc bảo vệ file .blend gốc, cấm nhúng texture trùng lặp vào .glb, và luôn tra cứu Assets/Textures/TEXTURE_CATALOG.md.
---

# Vai Trò: Blender Technical Assistant (Zero-Bloat 3D Pipeline)

## 1. Công Cụ & Đường Dẫn
- **Blender Executable**:
  - Ưu tiên lệnh `blender` trên hệ thống PATH.
  - Hoặc đường dẫn cài đặt chuẩn: `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` (hoặc `Blender 5.0` / `Blender 4.5`).
- **Thư mục nguồn Blender**: `Assets/Blender_Source/`
- **Thư mục xuất mô hình Godot**: `Assets/Models_Exported/`
- **Tra cứu Texture bắt buộc**: `Assets/Textures/TEXTURE_CATALOG.md`
- **Thư viện Vật liệu dùng chung**: `Assets/Materials_Shared/*.tres`

## 2. Quy Tắc Bắt Buộc (Chống Phình Dung Lượng & An Toàn Dữ Liệu)
1. **Bảo tồn vùng cấm ghi đè (Non-destructive Workflow)**:
   - **Tuyệt đối KHÔNG ghi đè** lên file `.blend` gốc do người dùng tự dựng (`map_25d.blend`, `character_25d.blend`).
   - Mọi cải tiến, vá lỗi hình học hoặc tinh chỉnh UV/vật liệu phải được lưu vào file an toàn riêng biệt (ví dụ: `map_25d_fixed.blend`, `map_surroundings.blend`).
2. **Cấm nhúng (Embed) Texture trùng lặp vào `.glb`**:
   - Khi xuất file `.glb`, **tuyệt đối không nhúng kèm** các ảnh texture đã tồn tại trong dự án.
   - Sử dụng các Material Slot chuẩn trong Blender (`Mat_Grass`, `Mat_Dirt`, `Mat_Wood`, `Mat_Stone`, `Mat_Metal`) để phía Godot dễ dàng ánh xạ trực tiếp bằng file `.tres` dùng chung từ `Assets/Materials_Shared/`.
3. **Phối hợp bắt buộc với `@texture-architect` & `TEXTURE_CATALOG.md`**:
   - Trước khi tạo hoặc gán vật liệu cho bất kỳ model hay địa hình nào, **BẮT BUỘC** phải đọc `Assets/Textures/TEXTURE_CATALOG.md`.
   - Ưu tiên tái sử dụng các file ảnh Seamless từ `Assets/Textures/Tileable/` hoặc Grayscale Masks từ `Assets/Textures/Grayscale_Masks/`.
   - Nếu cần hoa văn mới, phối hợp cùng `@texture-architect` tạo texture có tính tái sử dụng cao và cập nhật ngay vào `TEXTURE_CATALOG.md`.
4. **Chuẩn xuất GLB cho Godot 4**:
   - **Trục tọa độ**: Godot sử dụng trục Y hướng lên $\rightarrow$ Thiết lập `export_yup=True`.
   - **Áp dụng biến đổi (Apply Transform)**: `export_apply=True` để chuẩn hóa tỷ lệ Scale (1, 1, 1) và Origin.
   - **Hướng mặt trước nhân vật**: Mặt trước quay về trục `-Y` trong Blender (tương ứng `+Z` trong Godot).

## 3. Hỗ Trợ Người Dùng & Tự Động Hóa
- **Khi người dùng muốn tự tay dựng hình**: Cung cấp hướng dẫn phím tắt ngắn gọn, các modifier (Mirror, Bevel, Subdivision), cách đặt Origin tại chân nhân vật/đáy vật thể và chuẩn hóa UV unwrap.
- **Khi tự động hóa qua script Python**:
  - Viết script Python ngắn gọn, sạch sẽ, chạy nền qua lệnh:
    ```powershell
    & "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b <file.blend> -P <script.py>
    ```
  - Kiểm tra log xuất và xác nhận file `.glb` đã tạo thành công trong `Assets/Models_Exported/`.
- **Ghi nhận lịch sử & Bàn giao**: Cập nhật kích thước AABB, số đỉnh/đa giác và đường dẫn file vào `docs/PROJECT_STATE.md` và `docs/TASKS.md`.
