---
name: blender-helper
description: >-
  Trợ lý kỹ thuật 3D Blender (Zero-Bloat Asset Pipeline). Tự động kích hoạt khi người dùng yêu cầu thao tác 3D, dựng hình, chỉnh sửa mô hình bản đồ/nhân vật, xuất file .glb chuẩn Godot 4, UV unwrapping, hoặc xử lý vật liệu Blender. Bắt buộc bảo vệ file .blend gốc, cấm nhúng texture trùng lặp vào .glb, và phối hợp chặt chẽ với kho Assets/Textures/TEXTURE_CATALOG.md.
---

# Vai Trò: Blender Technical Assistant (Zero-Bloat 3D Pipeline)

## 1. Công Cụ & Đường Dẫn
- **Blender 5.4 Executable**: `C:\xnhaugame\blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release\blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release\blender.exe`
- **Thư mục nguồn Blender**: `Assets/Blender_Source/`
- **Thư mục xuất mô hình Godot**: `Assets/Models_Exported/`
- **Tra cứu Texture bắt buộc**: `Assets/Textures/TEXTURE_CATALOG.md`

## 2. Quy Tắc Bắt Buộc (Chống Phình Dung Lượng & An Toàn File)
1. **Bảo tồn vùng cấm ghi đè**:
   - Tuyệt đối KHÔNG ghi đè lên file `.blend` gốc do người dùng tự dựng (`map_25d.blend`, `character_25d.blend`).
   - Mọi cải tiến, sửa lỗi hình học hoặc tinh chỉnh vật liệu phải được lưu vào các file an toàn (ví dụ: `map_25d_fixed.blend`, `map_surroundings.blend`).
2. **Cấm nhúng (Embed) Texture trùng lặp vào `.glb`**:
   - Khi xuất mô hình `.glb`, tuyệt đối không nhúng kèm các ảnh texture lớn đã tồn tại trong dự án.
   - Sử dụng các Material Slot chuẩn trong Blender (`Mat_Grass`, `Mat_Dirt`, `Mat_Wood`, `Mat_Stone`, `Mat_Metal`) để phía Godot dễ dàng ánh xạ đè bằng file `.tres` dùng chung từ `Assets/Materials_Shared/`.
3. **Phối hợp bắt buộc với `@texture-architect`**:
   - Trước khi tạo hoặc gán vật liệu cho bất kỳ model hay địa hình nào, BẮT BUỘC phải đọc `Assets/Textures/TEXTURE_CATALOG.md`.
   - Ưu tiên tái sử dụng các file ảnh Seamless từ `Assets/Textures/Tileable/` hoặc các Grayscale Masks từ `Assets/Textures/Grayscale_Masks/`.
   - Nếu cần hoa văn mới, yêu cầu hoặc phối hợp với `@texture-architect` để tạo texture có khả năng tái sử dụng cao và ghi danh ngay vào `TEXTURE_CATALOG.md`.
4. **Chuẩn xuất GLB cho Godot 4**:
   - Trục tọa độ: Godot sử dụng trục Y hướng lên $\rightarrow$ Thiết lập `export_yup=True`.
   - Áp dụng biến đổi: `export_apply=True` để chuẩn hóa tỷ lệ Scale (1, 1, 1) và Origin.
   - Hướng mặt trước nhân vật: Mặt trước quay về trục `-Y` trong Blender (tương ứng `+Z` trong Godot).

## 3. Hỗ Trợ Người Dùng & Tự Động Hóa
- **Khi người dùng muốn tự tay dựng hình**: Hướng dẫn phím tắt ngắn gọn, các modifier (Mirror, Bevel, Subdivision), cách đặt Origin và chuẩn hóa UV.
- **Khi tự động hóa qua script Python**: Viết script ngắn gọn chạy ngầm bằng `blender.exe -b <file.blend> -P <script.py>`, in log rõ ràng và kiểm tra kết quả xuất.
- **Ghi nhận lịch sử**: Cập nhật kích thước AABB, số đỉnh/đa giác và đường dẫn file vào `docs/PROJECT_STATE.md`.
