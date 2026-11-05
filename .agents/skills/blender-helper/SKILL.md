---
name: blender-helper
description: Hỗ trợ xuất model 3D từ Blender sang .glb không nhúng trùng lặp texture, đồng bộ với kho Assets/Textures và Assets/Materials_Shared.
---
# Vai trò: Blender Technical Assistant (Zero-Bloat Pipeline)

1. **Cấm nhúng (Embed) Texture trùng lặp vào `.glb`**:
   - Khi xuất file `.glb` bằng script Python (`bpy.ops.export_scene.gltf`), nếu dùng texture chung, hãy đặt `export_materials='PLACEHOLDER'` hoặc gán Material chuẩn từ `Assets/Materials_Shared/*.tres` ở phía Godot để 10 file `.glb` không tự nhân bản 10 bức ảnh giống hệt nhau.
2. **Phối hợp chặt với `@texture-architect`**:
   - Trước khi tạo vật liệu cho model hay map, luôn đọc `Assets/Textures/TEXTURE_CATALOG.md`.
   - Đặt tên Material Slot trong Blender trùng khớp ý nghĩa (ví dụ: `Mat_Wood`, `Mat_Stone`, `Mat_Foliage`) để dễ dàng ánh xạ với các file `.tres` trong `Assets/Materials_Shared/`.
3. **Bảo vệ file gốc**: Không tự ý ghi đè lên file `.blend` do người dùng tự dựng.
