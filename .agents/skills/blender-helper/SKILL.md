---
name: blender-helper
description: >-
  Trợ lý kỹ thuật 3D Blender (Zero-Bloat Asset, Sketch-to-3D Pipeline & Procedural Modeling Kit). Tự động kích hoạt khi người dùng yêu cầu thao tác 3D, dựng map/model từ ảnh phác họa trong modelyeucau/, chỉnh sửa mô hình bản đồ/nhân vật, xuất file .glb chuẩn Godot 4, UV unwrapping, hoặc xử lý vật liệu Blender. Bắt buộc: (1) Cấm dùng primitive thô sơ (dùng bmesh + Bevel 2-3 segments + Solidify + Auto Smooth), (2) Sử dụng thư viện chuẩn tools/blender_kit.py với căn chỉnh AABB, (3) Mắt Thần Tự Kiểm Tra render _preview_render.png và đọc ảnh đối chiếu, (4) Vòng lặp chất lượng đến khi đạt thẩm mỹ chuẩn.
---

# Vai Trò: Blender Technical Assistant (Zero-Bloat, Sketch-to-3D & Procedural Pipeline)

Kỹ năng này chịu trách nhiệm tối cao về việc thiết kế, dựng hình 3D, tối ưu hóa hình học, tự động hóa bằng script `bpy` và bảo đảm thẩm mỹ chuẩn mực cho toàn bộ mô hình trong dự án.

---

## 1. Công Cụ & Thư Viện Chuẩn
- **Trình chạy Blender 5.4 CLI**:
  `C:/xnhaugame/blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release/blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release/blender.exe`
- **Thư viện Procedural chuẩn dùng chung**: `tools/blender_kit.py`
- **Thư mục ảnh phác họa người dùng**: `modelyeucau/`
- **Thư mục xuất mô hình Godot**: `Assets/Models/` (và `Assets/Models_Exported/`)
- **Thư mục nguồn Blender**: `Assets/Blender_Source/`
- **Ảnh render kiểm tra thị giác (Mắt Thần)**: `Assets/Models/_preview_render.png`
- **Tra cứu Texture bắt buộc**: `Assets/Textures/TEXTURE_CATALOG.md`
- **Thư viện Vật liệu dùng chung**: `Assets/Materials_Shared/*.tres`

---

## 2. 4 Quy Tắc Bắt Buộc Dựng Model Blender (Chống Model Thô Kệch)

### Quy Tắc 1: CẤM DỰNG KHỐI THÔ SƠ (No Raw Primitives)
- **Tuyệt đối cấm** việc chỉ ghép các khối Cube/Cylinder/Sphere nguyên bản thô cứng mà không qua xử lý cạnh và bề mặt.
- Mọi script Python (`bpy`) bắt buộc phải áp dụng:
  - **`bmesh` operations**: Extrude, Inset, Bevel, Subdivide, và Vertex Displace để tạo độ cong, gờ cạnh và độ nhấp nhô tự nhiên.
  - **Blender Modifiers**:
    - `Bevel Modifier` (từ 2 - 3 segments, width 0.02 - 0.04m, limit by Angle 30°) để bo viền bắt sáng (edge highlight), giúp vật thể có chiều sâu thị giác.
    - `Solidify Modifier` (thickness 0.15m) cho các vách tường, mái hiên, tấm ván nhằm tạo độ dày vật lý thực tế.
    - `Displace / Noise` cho đá núi, địa hình, tán lá để triệt tiêu cảm giác đa giác sắc nhọn nhân tạo.
    - Bật `Shade Auto Smooth` (góc 35° - 45°) trên toàn bộ bề mặt cong và trụ tròn.

### Quy Tắc 2: XÂY DỰNG & TÁI SỬ DỤNG THƯ VIỆN PROCEDURAL CHUẨN (`tools/blender_kit.py`)
- Mọi script dựng hình bắt buộc phải `import` từ thư viện dùng chung `tools/blender_kit.py`.
- Thư viện cung cấp sẵn các module tham số hóa cao cấp:
  - `create_beveled_box(...)`: Khối hộp có vát cạnh bắt sáng tự động.
  - `create_beveled_cylinder(...)`: Khối trụ bo viền trên dưới.
  - `build_chamfered_rock(...)`: Tảng đá Low-Poly vát cạnh tự nhiên ngẫu hóa bằng hạt nhân (seed).
  - `build_stylized_tree(...)`: Cây cách điệu thân thon, đa tầng tán lá hữu cơ không trùng lặp.
  - `build_detailed_roof_gabled(...)`: Mái nhà có riềm chìa ra ngoài (overhang) và độ dày thực tế.
  - **Hàm tự động căn chỉnh AABB**:
    - `snap_to_ground(obj, ground_z)`: Chống tuyệt đối hiện tượng vật thể bay lơ lửng trên không trung.
    - `stack_on_top(child_obj, base_obj)`: Đặt vật thể con nằm khít hoàn hảo trên đỉnh vật thể cha, không đâm xuyên (interpenetration).
- Mọi khi phát triển chi tiết mới (cầu thang, xe hàng, giếng nước), phải đóng gói ngược lại vào `tools/blender_kit.py` để tái sử dụng vĩnh viễn.

### Quy Tắc 3: CƠ CHẾ MẮT THẦN TỰ KIỂM TRA (Visual Self-Correction Loop)
- Cuối mỗi script dựng hình Blender, bắt buộc phải tự động gọi hàm:
  `blender_kit.setup_preview_render(output_path="Assets/Models/_preview_render.png")`
- Thiết lập Camera Isometric + Sun Light cường độ cao, bật Cavity Shading (đổ bóng khe kẽ sắc nét) và render nhanh bằng `BLENDER_WORKBENCH` ra file ảnh `Assets/Models/_preview_render.png`.
- Sau khi chạy lệnh `blender.exe --background`, AI **bắt buộc** phải dùng công cụ đọc ảnh (`read_file`) để trực tiếp xem file ảnh `_preview_render.png`, đối chiếu với yêu cầu và ảnh phác họa trong `modelyeucau/`.

### Quy Tắc 4: VÒNG LẶP CHẤT LƯỢNG (Self-Correction & Refinement)
- Nếu sau khi đọc ảnh `_preview_render.png` phát hiện:
  - Model còn thô sơ, cạnh quá bén, thiếu độ bo tròn.
  - Tỷ lệ các chi tiết bị lệch (nhà quá bé, cửa quá nhỏ so với người cao 1.8m, cây cối trơ trọi).
  - Vật thể bị bay lơ lửng hoặc đâm xuyên lệch vị trí.
- AI **TUYỆT ĐỐI KHÔNG ĐƯỢC DỪNG LẠI** hoặc bàn giao cho người dùng. Bắt buộc phải tự chỉnh sửa lại tham số trong script Python, render lại `_preview_render.png` và tự đánh giá lại liên tục cho đến khi hình dáng 3D sắc nét, thẩm mỹ, hài hòa mới được xuất file `.glb` vào Godot.

---

## 3. Quy Trình "Sketch-to-3D Pipeline" Đầy Đủ
```mermaid
flowchart TD
    Sketch["1. Đọc ảnh phác họa trong modelyeucau/<br>(Phân tích tọa độ X, Z, tỷ lệ, màu sắc)"] --> Tex["2. Tra cứu Assets/Textures/TEXTURE_CATALOG.md<br>(Lấy Shared .tres / Seamless / Mask)"]
    Tex --> Script["3. Soạn script bpy dùng tools/blender_kit.py<br>(bmesh, Bevel Modifier, AABB snap)"]
    Script --> Exec["4. Chạy Blender CLI Headless<br>& Render _preview_render.png"]
    Exec --> Eye{"5. Mắt Thần Tự Kiểm Tra<br>(Dùng read_file đọc _preview_render.png)"}
    Eye -- "Thô / Lệch / Xấu" --> Script
    Eye -- "Sắc nét, Đúng tỷ lệ, Đẹp" --> Export["6. Xuất Assets/Models/*.glb (export_yup=True)<br>Lưu file .blend an toàn"]
    Export --> GodotScene["7. Gắn vào Scene .tscn Godot 4<br>& Chạy Playtest Loop test_suite.gd"]
```

---

## 4. Quy Chuẩn Xuất File & An Toàn Bộ Nhớ
1. **Bảo vệ file gốc**: Tuyệt đối không ghi đè `.blend` gốc (`map_25d.blend`, `character_25d.blend`). Mọi file mới lưu vào `Assets/Blender_Source/<tên>_fixed.blend`.
2. **Cấm nhúng trùng lặp Texture**: Đặt Material Slot chuẩn (`Mat_Grass`, `Mat_Dirt`, `Mat_Stone`, `Mat_Wood`, `Mat_Roof_Red`, `Mat_Roof_Teal`, `Mat_Canopy_Striped`, `Mat_Mystic_Cyan`, `Mat_Lava_Fire`) để Godot tự động ánh xạ bằng file `.tres` dùng chung trong `Assets/Materials_Shared/`.
3. **Chuẩn tọa độ Godot**:
   - Vị trí: `blender_pos = (godot_x, -godot_z, godot_y)`
   - Kích thước: `blender_size = (godot_sx, godot_sz, godot_sy)`
   - Cờ xuất glTF: `export_yup=True`, `export_apply=True`, `export_materials='EXPORT'`.
