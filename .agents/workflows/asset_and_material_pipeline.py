"""
Workflow: Chuỗi Xử lý Texture và Xuất Model 3D Không Phình Dung Lượng (Hierarchical 3-Tier Gate)
Thực thi tuần tự:
- Thợ Texture & Giám Sát Texture (@texture-architect & @texture-inspector)
- Thợ 3D & Giám Sát 3D (@blender-helper & @blender-inspector)
- Giám Sát Tổng Quản (@chief-supervisor) kiểm định thực tế
"""

task_description = args.get("task", "Tối ưu hóa Texture và Model 3D")

# -------------------------------------------------------------
# PHASE 1: TEXTURE & MATERIAL SELECTION + INSPECTION
# -------------------------------------------------------------
phase("Tầng 1: Texture Architect & Giám Sát Texture")
tex_arch = agent(
    prompt=(
        f"Bạn là Sub-agent texture-architect.\n"
        f"Nhiệm vụ: {task_description}\n"
        f"Quy trình bắt buộc:\n"
        f"1. Quét màu pixel thật từ modelyeucau/ bằng Python, sinh texture có vân bề mặt thật.\n"
        f"2. Xuất ảnh lát thử 2x2 _tile_preview.png và ảnh bọc 3D _texture_3d_check.png.\n"
        f"3. Cập nhật mọi tài nguyên mới vào Assets/Textures/TEXTURE_CATALOG.md.\n"
        f"4. Bàn giao cho @texture-inspector nghiệm thu."
    ),
    role="Texture Architect",
    type_name="self",
    schema={"type": "string"}
)
tex_result = await tex_arch(task_description, {"type": "string"})
log(f"[Texture Architect]: {tex_result}")

tex_inspector = agent(
    prompt=(
        "Bạn là Sub-agent texture-inspector.\n"
        "Quy trình kiểm tra:\n"
        "1. Dùng Vision (read_file) soi ảnh lát thử 2x2 _tile_preview.png đảm bảo Seamless 100% không lộ viền.\n"
        "2. Kiểm tra ảnh bọc 3D _texture_3d_check.png.\n"
        "3. Kiểm tra đăng ký TEXTURE_CATALOG.md.\n"
        "4. Nếu chưa đạt, ép @texture-architect làm lại tại chỗ. Chỉ ký PASS khi đạt 100%."
    ),
    role="Texture Inspector",
    type_name="self",
    schema={"type": "string"}
)
tex_pass = await tex_inspector("Nghiệm thu chất lượng Texture", {"type": "string"})
log(f"[Texture Inspector]: {tex_pass}")

# -------------------------------------------------------------
# PHASE 2: 3D MODEL & MATERIAL INTEGRATION + INSPECTION
# -------------------------------------------------------------
phase("Tầng 1: Blender Helper & Giám Sát 3D")
blender_helper = agent(
    prompt=(
        "Bạn là Sub-agent blender-helper.\n"
        "Quy trình bắt buộc:\n"
        "1. Dùng bmesh + Bevel + Solidify + Shade Auto Smooth, cấm primitive thô sơ.\n"
        "2. Bắt buộc trải UV tự động (cube_project/smart_project).\n"
        "3. Tuân thủ Human Reference Scale (Người 1.8m, Cửa 2.3-2.6m, Tường 3.5-4.5m).\n"
        "4. Render ảnh _preview_render.png và xuất file .glb chuẩn Godot kèm collider -col.\n"
        "5. Bàn giao cho @blender-inspector nghiệm thu."
    ),
    role="Blender Assistant",
    type_name="self",
    schema={"type": "string"}
)
blender_result = await blender_helper("Liên kết vật liệu và xuất .glb", {"type": "string"})
log(f"[Blender Helper]: {blender_result}")

blender_inspector = agent(
    prompt=(
        "Bạn là Sub-agent blender-inspector.\n"
        "Quy trình kiểm tra:\n"
        "1. Dùng Vision (read_file) soi ảnh Models/_preview_render.png đối chiếu với modelyeucau/.\n"
        "2. Kiểm tra lưới bmesh/Modifiers, trải UV bắt buộc, tỷ lệ kích thước và collider -col.\n"
        "3. Nếu thô sơ hoặc lệch trục -> Ép @blender-helper dựng lại tại chỗ. Ký PASS khi đạt chuẩn."
    ),
    role="Blender Inspector",
    type_name="self",
    schema={"type": "string"}
)
blender_pass = await blender_inspector("Nghiệm thu mô hình 3D", {"type": "string"})
log(f"[Blender Inspector]: {blender_pass}")

# -------------------------------------------------------------
# PHASE 3: CHIEF SUPERVISOR PLAYTEST
# -------------------------------------------------------------
phase("Tầng 2: Giám Sát Tổng Quản Độc Lập (@chief-supervisor)")
chief = agent(
    prompt=(
        "Bạn là Sub-agent chief-supervisor.\n"
        "Quy trình bắt buộc:\n"
        "1. Nhận bàn giao khi cả @texture-inspector và @blender-inspector đã ký duyệt PASS.\n"
        "2. Chạy test_suite.gd (Windowed Render) kiểm tra toàn game và chụp 4 ảnh màn hình.\n"
        "3. Kiểm tra Timestamp ảnh mới hơn code và dùng Vision đối chiếu Side-by-Side với modelyeucau/.\n"
        "4. Cập nhật docs/PROJECT_STATE.md, docs/TASKS.md và báo cáo hoàn thành."
    ),
    role="Chief Supervisor",
    type_name="self",
    schema={"type": "string"}
)
chief_result = await chief("Nghiệm thu toàn cảnh 3D và vật liệu", {"type": "string"})
log(f"[Chief Supervisor]: {chief_result}")

print(f"=== KẾT QUẢ ASSET PIPELINE ===\n[Texture]: {tex_pass}\n[3D Model]: {blender_pass}\n[Chief Supervisor]: {chief_result}")
