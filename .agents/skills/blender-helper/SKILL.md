---
name: blender-helper
description: >-
  Trợ lý kỹ thuật 3D Blender (Zero-Bloat Asset & Sketch-to-3D Pipeline). Tự động kích hoạt khi người dùng yêu cầu thao tác 3D, dựng map/model từ ảnh phác họa trong modelyeucau/, chỉnh sửa mô hình bản đồ/nhân vật, xuất file .glb chuẩn Godot 4, UV unwrapping, hoặc xử lý vật liệu Blender. Bắt buộc đọc ảnh phân tích trước khi viết script bpy, bảo vệ file .blend gốc, cấm nhúng texture trùng lặp vào .glb, và phối hợp chặt chẽ với kho Assets/Textures/TEXTURE_CATALOG.md.
---

# Vai Trò: Blender Technical Assistant (Zero-Bloat & Sketch-to-3D Pipeline)

## 1. Công Cụ & Đường Dẫn
- **Blender 5.4 Executable**:
  - `C:/xnhaugame/blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release/blender.exe` (hoặc đường dẫn đầy đủ: `C:\xnhaugame\blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release\blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release\blender.exe`)
- **Thư mục ảnh phác họa người dùng**: `modelyeucau/` (chứa các folder ảnh concept/sketch như `modelyeucau/map/`, `modelyeucau/map2/`, `modelyeucau/charater1/`)
- **Thư mục xuất mô hình Godot**: `Assets/Models/` (và `Assets/Models_Exported/`)
- **Thư mục nguồn Blender**: `Assets/Blender_Source/`
- **Tra cứu Texture bắt buộc**: `Assets/Textures/TEXTURE_CATALOG.md`
- **Thư viện Vật liệu dùng chung**: `Assets/Materials_Shared/*.tres`

---

## 2. Quy Trình "Đọc Ảnh Phác Họa Tạo Model 3D" (Sketch-to-3D Pipeline)

Khi người dùng yêu cầu tạo bản đồ, công trình, đạo cụ hoặc nhân vật 3D dựa trên ảnh trong thư mục `modelyeucau/` (ví dụ: `modelyeucau/map2/1.jpg` hoặc `1.png`), AI **BẮT BUỘC** tuân thủ nghiêm ngặt 4 bước sau:

### Bước 1: Xác định nguồn ảnh phác họa
- Định vị chính xác đường dẫn ảnh trong `modelyeucau/` theo yêu cầu của người dùng.
- Kiểm tra danh mục tài nguyên có sẵn trong thư mục đó (ảnh sketch, texture nháp, script mẫu).

### Bước 2: Đọc ảnh & Phân tích thị giác (Vision Analysis)
- **Bắt buộc dùng công cụ đọc ảnh (`read_file`)** để trực tiếp nạp và phân tích ảnh phác họa trước khi viết bất kỳ dòng mã nào.
- Trích xuất chi tiết các thông số không gian:
  1. **Bố cục 2D & Tọa độ tương đối**: Xác định mặt bằng lưới (Grid), phân bố tọa độ (X, Z) của từng vật thể (vùng đất chính, lối đi, ao hồ, cây cối, đá, tường rào, công trình...).
  2. **Độ cao & Tỷ lệ (Y / Scale)**: Ước lượng chiều cao của các tầng địa hình, gờ đất dốc (cliff/ramps), kích thước AABB (dài, rộng, cao).
  3. **Màu sắc & Phân vùng thẩm mỹ**: Nhận diện bảng màu chủ đạo (màu cỏ, đất, đá, nước, gỗ, kim loại) để phân định các Material Slot.

### Bước 3: Phối hợp vật liệu với `@texture-architect`
- Đọc và đối chiếu với `Assets/Textures/TEXTURE_CATALOG.md`.
- **Ưu tiên 1**: Sử dụng lại các Material `.tres` đã có trong `Assets/Materials_Shared/`.
- **Ưu tiên 2**: Tái sử dụng các texture Seamless (`Assets/Textures/Tileable/`) hoặc Grayscale Masks (`Assets/Textures/Grayscale_Masks/`) kết hợp gán màu tương ứng trong ảnh phác họa.
- Thiết lập tên Material Slot trong Blender chuẩn hóa (`Mat_Grass`, `Mat_Cliff`, `Mat_Water`, `Mat_Wood`, `Mat_Stone`, `Mat_Path`) để Godot tự động ánh xạ hoặc ghi đè mà không làm phình VRAM.

### Bước 4: Viết Script Blender Python (`bpy`), Dựng Mesh & Xuất GLB
- Soạn thảo script Python tự động hóa:
  - Khởi tạo Mesh sạch (Geometry sạch, chuẩn Quad/Tris, tối ưu Polycount).
  - Đặt các khối và chi tiết đúng vị trí (X, Y, Z) và tỷ lệ theo phân tích từ ảnh phác họa ở Bước 2.
  - **Tự động tạo va chạm (Collision)**:
    - Tạo các Object va chạm đơn giản hóa (Box/Convex Hull) với hậu tố chuẩn Godot như `-col` (tạo StaticBody + CollisionShape) hoặc `-colonly` (chỉ tạo va chạm vô hình).
  - Chuẩn hóa Pivot/Origin (tâm chân vật thể nằm tại Y=0).
- Chạy Blender ở chế độ không giao diện (Headless / Background):
  ```bash
  C:/xnhaugame/blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release/blender.exe --background --python <đường_dẫn_script.py>
  ```
- Xuất file `.glb` vào thư mục `Assets/Models/` với các cờ xuất chuẩn: `export_yup=True`, `export_apply=True`.
- **Gắn vào Scene `.tscn` trong Godot**: Tạo Scene Godot 4 (.tscn) kế thừa hoặc instance model `.glb`, kiểm tra va chạm vật lý và ánh xạ vật liệu hoàn chỉnh.

---

## 3. Quy Tắc Bắt Buộc (Chống Phình Dung Lượng & An Toàn File)
1. **Bảo tồn vùng cấm ghi đè**:
   - Tuyệt đối KHÔNG ghi đè lên file `.blend` gốc do người dùng tự dựng (`map_25d.blend`, `character_25d.blend`).
   - Mọi cải tiến, sửa lỗi hình học hoặc tinh chỉnh vật liệu phải được lưu vào các file an toàn (ví dụ: `map_25d_fixed.blend`, `map2_generated.blend`).
2. **Cấm nhúng (Embed) Texture trùng lặp vào `.glb`**:
   - Khi xuất mô hình `.glb`, tuyệt đối không nhúng kèm các ảnh texture lớn đã tồn tại trong dự án.
   - Sử dụng các Material Slot chuẩn để phía Godot dễ dàng ánh xạ bằng file `.tres` dùng chung từ `Assets/Materials_Shared/`.
3. **Phối hợp bắt buộc với `@texture-architect`**:
   - BẮT BUỘC đọc `Assets/Textures/TEXTURE_CATALOG.md` trước khi gán vật liệu.
4. **Chuẩn xuất GLB cho Godot 4**:
   - Trục tọa độ: Trục Y hướng lên $\rightarrow$ Thiết lập `export_yup=True`.
   - Áp dụng biến đổi: `export_apply=True` để chuẩn hóa tỷ lệ Scale (1, 1, 1) và Origin.
   - Hướng mặt trước nhân vật: Mặt trước quay về trục `-Y` trong Blender (tương ứng `+Z` trong Godot).

---

## 4. Hỗ Trợ Người Dùng & Tự Động Hóa
- **Khi người dùng muốn tự tay dựng hình**: Hướng dẫn phím tắt ngắn gọn, các modifier (Mirror, Bevel, Subdivision), cách đặt Origin và chuẩn hóa UV.
- **Khi tự động hóa qua script Python**: Viết script ngắn gọn, chạy ngầm bằng CLI, in log rõ ràng và kiểm tra kết quả xuất.
- **Ghi nhận lịch sử**: Cập nhật kích thước AABB, số đỉnh/đa giác và đường dẫn file vào `docs/PROJECT_STATE.md` và `docs/TASKS.md`.
