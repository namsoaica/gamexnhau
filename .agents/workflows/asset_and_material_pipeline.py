"""
Workflow: Chuỗi Xử lý Texture và Xuất Model 3D Không Phình Dung Lượng (Strict Single Responsibility)
Thực thi tuần tự:
- Ca 1: Thợ Texture & Giám Sát Texture (@texture-architect & @texture-inspector)
- Ca 2: Thợ 3D & Giám Sát 3D (@blender-helper & @blender-inspector)
- Ca 4: Giám Sát Tổng Quản (@chief-supervisor) kiểm định thực tế
"""

task_description = args.get("task", "Tối ưu hóa Texture và Model 3D")

# -------------------------------------------------------------
# PHASE 1: TEXTURE & MATERIAL SELECTION + INSPECTION (CA 1)
# -------------------------------------------------------------
phase("Ca 1: Texture Architect & Giám Sát Texture")
tex_arch = agent(
    prompt=(
        f"Bạn là Sub-agent texture-architect (Thợ Texture Độc Lập).\n"
        f"Nhiệm vụ: {task_description}\n"
        f"Ranh giới file: CHỈ ĐƯỢC tạo/sửa file ảnh .png, .tres và TEXTURE_CATALOG.md. Cấm sửa file 3D mesh hay .cs.\n"
        f"Quét màu pixel thật từ modelyeucau/ bằng Python, sinh texture có vân bề mặt thật.\n"
        f"Xuất ảnh lát thử 2x2 _tile_preview.png và ảnh bọc 3D _texture_3d_check.png.\n"
        f"Bàn giao cho @texture-inspector nghiệm thu."
    ),
    role="texture-architect",
    type_name="self",
    schema={"type": "string"}
)
tex_result = await tex_arch(task_description, {"type": "string"})
log(f"[texture-architect]: {tex_result}")

tex_inspector = agent(
    prompt=(
        "Bạn là Sub-agent texture-inspector (Giám sát riêng 1-kèm-1 của @texture-architect).\n"
        "Quy trình kiểm tra: Dùng Vision soi ảnh lát thử 2x2 _tile_preview.png đảm bảo Seamless 100%, ảnh bọc 3D _texture_3d_check.png, đăng ký TEXTURE_CATALOG.md.\n"
        "Chỉ ký PASS khi đạt 100%."
    ),
    role="texture-inspector",
    type_name="self",
    schema={"type": "string"}
)
tex_pass = await tex_inspector("Nghiệm thu chất lượng Texture", {"type": "string"})
log(f"[texture-inspector]: {tex_pass}")

# -------------------------------------------------------------
# PHASE 2: 3D MODEL & MATERIAL INTEGRATION + INSPECTION (CA 2)
# -------------------------------------------------------------
phase("Ca 2: Blender Helper & Giám Sát 3D")
blender_helper = agent(
    prompt=(
        "Bạn là Sub-agent blender-helper (Thợ 3D Blender Độc Lập).\n"
        "Ranh giới file: CHỈ ĐƯỢC viết script Python bpy trong tools/ hoặc Assets/Blender_Source/ và xuất .glb. Cấm sửa file .cs hay .tscn.\n"
        "Dùng bmesh + Bevel + Solidify + Shade Auto Smooth, cấm primitive thô sơ.\n"
        "Bắt buộc trải UV tự động và tuân thủ Human Reference Scale.\n"
        "Render ảnh _preview_render.png và xuất file .glb kèm collider -col.\n"
        "Bàn giao cho @blender-inspector nghiệm thu."
    ),
    role="blender-helper",
    type_name="self",
    schema={"type": "string"}
)
blender_result = await blender_helper("Liên kết vật liệu và xuất .glb", {"type": "string"})
log(f"[blender-helper]: {blender_result}")

blender_inspector = agent(
    prompt=(
        "Bạn là Sub-agent blender-inspector (Giám sát riêng 1-kèm-1 của @blender-helper).\n"
        "Quy trình kiểm tra: Dùng Vision soi ảnh Models/_preview_render.png đối chiếu với modelyeucau/, kiểm tra lưới bmesh, Bevel, trải UV và Human Reference Scale.\n"
        "Ký PASS khi đạt chuẩn 100%."
    ),
    role="blender-inspector",
    type_name="self",
    schema={"type": "string"}
)
blender_pass = await blender_inspector("Nghiệm thu mô hình 3D", {"type": "string"})
log(f"[blender-inspector]: {blender_pass}")

# -------------------------------------------------------------
# PHASE 3: CHIEF SUPERVISOR PLAYTEST (CA 4)
# -------------------------------------------------------------
phase("Ca 4: Giám Sát Tổng Quản Độc Lập (@chief-supervisor)")
chief = agent(
    prompt=(
        "Bạn là Sub-agent chief-supervisor.\n"
        "Chỉ nhận bàn giao khi cả @texture-inspector và @blender-inspector đã ký duyệt PASS.\n"
        "Chạy test_suite.gd (Windowed Render) kiểm tra toàn game và chụp 4 ảnh màn hình.\n"
        "Kiểm tra Timestamp ảnh mới hơn code và dùng Vision đối chiếu Side-by-Side với modelyeucau/."
    ),
    role="chief-supervisor",
    type_name="self",
    schema={"type": "string"}
)
chief_result = await chief("Nghiệm thu toàn cảnh 3D và vật liệu", {"type": "string"})
log(f"[chief-supervisor]: {chief_result}")

print(f"=== KẾT QUẢ ASSET PIPELINE ===\n[Texture]: {tex_pass}\n[3D Model]: {blender_pass}\n[Chief Supervisor]: {chief_result}")
