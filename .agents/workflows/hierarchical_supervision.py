"""
Workflow: Tháp Giám Sát Phân Cấp 3 Tầng & Luật Cô Lập Đơn Nhiệm (Strict 1-Skill-Per-Subagent)
Thực thi tuần tự qua 4 Ca độc lập:
- Ca 1: @texture-architect (Thợ) -> @texture-inspector (Giám sát riêng)
- Ca 2: @blender-helper (Thợ) -> @blender-inspector (Giám sát riêng)
- Ca 3: @csharp-coder (Thợ) -> @csharp-inspector (Giám sát riêng)
- Ca 4: @chief-supervisor (Giám sát tổng quản toàn game) -> @producer (Đồng bộ tài liệu)
"""

task_description = args.get("task", "Thực hiện nhiệm vụ nâng cấp game theo mô hình Tháp Giám Sát Phân Cấp 3 Tầng")

# -------------------------------------------------------------
# CA 1: NHÁNH TEXTURE (CHỈ .PNG, .TRES, TEXTURE_CATALOG.MD)
# -------------------------------------------------------------
phase("Ca 1: Thợ Texture @texture-architect & Giám Sát @texture-inspector")
tex_worker = agent(
    prompt=(
        f"Bạn là Sub-agent texture-architect (Thợ Texture Độc Lập).\n"
        f"Nhiệm vụ: {task_description}\n"
        f"Ranh giới file nghiêm ngặt: CHỈ ĐƯỢC tạo/sửa file ảnh .png trong Assets/Textures/, vật liệu .tres trong Assets/Materials_Shared/ và Assets/Textures/TEXTURE_CATALOG.md. Tuyệt đối cấm sửa file 3D mesh hay .cs.\n"
        f"Bàn giao cho @texture-inspector."
    ),
    role="texture-architect",
    type_name="self",
    schema={"type": "string"}
)
tex_res = await tex_worker(task_description, {"type": "string"})
log(f"[@texture-architect]: {tex_res}")

tex_inspector = agent(
    prompt=(
        "Bạn là Sub-agent texture-inspector (Giám sát riêng 1-kèm-1 của @texture-architect).\n"
        "Kiểm tra: Dùng Vision soi ảnh lát thử 2x2 _tile_preview.png đảm bảo Seamless 100%, ảnh bọc 3D và đăng ký TEXTURE_CATALOG.md.\n"
        "Chỉ ký PASS khi đạt 100%."
    ),
    role="texture-inspector",
    type_name="self",
    schema={"type": "string"}
)
tex_pass = await tex_inspector("Nghiệm thu nhánh Texture", {"type": "string"})
log(f"[@texture-inspector]: {tex_pass}")

# -------------------------------------------------------------
# CA 2: NHÁNH 3D BLENDER (CHỈ SCRIPT BPY VÀ .GLB)
# -------------------------------------------------------------
phase("Ca 2: Thợ 3D Blender @blender-helper & Giám Sát @blender-inspector")
blender_worker = agent(
    prompt=(
        f"Bạn là Sub-agent blender-helper (Thợ 3D Blender Độc Lập).\n"
        f"Nhiệm vụ: {task_description}\n"
        f"Ranh giới file nghiêm ngặt: CHỈ ĐƯỢC viết script Python bpy trong tools/ hoặc Assets/Blender_Source/ và xuất .glb vào Assets/Models/. Tuyệt đối cấm sửa file .cs hay .tscn.\n"
        f"Bắt buộc dùng bmesh, Bevel, Solidify, Shade Auto Smooth, trải UV tự động và chuẩn tỷ lệ người 1.8m.\n"
        f"Bàn giao cho @blender-inspector."
    ),
    role="blender-helper",
    type_name="self",
    schema={"type": "string"}
)
blender_res = await blender_worker("Dựng hình 3D Blender", {"type": "string"})
log(f"[@blender-helper]: {blender_res}")

blender_inspector = agent(
    prompt=(
        "Bạn là Sub-agent blender-inspector (Giám sát riêng 1-kèm-1 của @blender-helper).\n"
        "Kiểm tra: Dùng Vision soi ảnh render _preview_render.png đối chiếu modelyeucau/, kiểm tra bmesh, Bevel, trải UV và Human Reference Scale.\n"
        "Chỉ ký PASS khi đạt chuẩn 100%."
    ),
    role="blender-inspector",
    type_name="self",
    schema={"type": "string"}
)
blender_pass = await blender_inspector("Nghiệm thu nhánh 3D Blender", {"type": "string"})
log(f"[@blender-inspector]: {blender_pass}")

# -------------------------------------------------------------
# CA 3: NHÁNH C# & SCENE (CHỈ SCRIPTS/*.CS, SCENES/*.TSCN, PROJECT.GODOT)
# -------------------------------------------------------------
phase("Ca 3: Thợ C# Gameplay @csharp-coder & Giám Sát @csharp-inspector")
cs_worker = agent(
    prompt=(
        f"Bạn là Sub-agent csharp-coder (Thợ C# Gameplay Độc Lập).\n"
        f"Nhiệm vụ: {task_description}\n"
        f"Ranh giới file nghiêm ngặt: CHỈ ĐƯỢC viết/sửa file .cs trong Scripts/, .tscn trong Scenes/ và project.godot. Tuyệt đối cấm viết script Blender hay vẽ Texture.\n"
        f"Tuân thủ Clean Code: hàm < 25 dòng, file < 200 dòng, Guard Clauses, hủy -= trong _ExitTree().\n"
        f"Bàn giao cho @csharp-inspector."
    ),
    role="csharp-coder",
    type_name="self",
    schema={"type": "string"}
)
cs_res = await cs_worker(task_description, {"type": "string"})
log(f"[@csharp-coder]: {cs_res}")

cs_inspector = agent(
    prompt=(
        "Bạn là Sub-agent csharp-inspector (Giám sát riêng 1-kèm-1 của @csharp-coder).\n"
        "Kiểm tra: Chạy lệnh python tools/supervisor_gate.py đảm bảo Clean Code, an toàn bộ nhớ, Input Action và dotnet build 0 lỗi.\n"
        "Chỉ ký PASS khi exit code là 0."
    ),
    role="csharp-inspector",
    type_name="self",
    schema={"type": "string"}
)
cs_pass = await cs_inspector("Kiểm định Gatekeeper C#", {"type": "string"})
log(f"[@csharp-inspector]: {cs_pass}")

# -------------------------------------------------------------
# CA 4: NGHIỆM THU TỔNG THỂ TOÀN GAME & ĐỒNG BỘ TÀI LIỆU
# -------------------------------------------------------------
phase("Ca 4: Giám Sát Tổng Quản @chief-supervisor & @producer")
chief = agent(
    prompt=(
        "Bạn là Sub-agent chief-supervisor (Giám Sát Tổng Quản Độc Lập).\n"
        "Chỉ nhận bàn giao khi cả 3 giám sát con đã ký duyệt PASS.\n"
        "Chạy test_suite.gd Windowed Render trên Godot Mono Console (CẤM --headless).\n"
        "Kiểm tra Timestamp ảnh mới hơn code và dùng Vision soi 4 ảnh đối chiếu Side-by-Side với modelyeucau/.\n"
        "Ký duyệt nghiệm thu toàn game."
    ),
    role="chief-supervisor",
    type_name="self",
    schema={"type": "string"}
)
chief_res = await chief("Nghiệm thu tích hợp toàn game", {"type": "string"})
log(f"[@chief-supervisor]: {chief_res}")

producer = agent(
    prompt=(
        "Bạn là Sub-agent producer (Quản lý tiến độ & Đồng bộ tài liệu).\n"
        "Quét ổ cứng thực tế, cập nhật docs/PROJECT_STATE.md, docs/TASKS.md và docs/SESSION_HISTORY.md."
    ),
    role="producer",
    type_name="self",
    schema={"type": "string"}
)
producer_res = await producer("Đồng bộ tài liệu dự án", {"type": "string"})
log(f"[@producer]: {producer_res}")

print(f"=== KẾT QUẢ DÂY CHUYỀN NỐI TIẾP 4 CA ===\nCa 1: {tex_pass}\nCa 2: {blender_pass}\nCa 3: {cs_pass}\nCa 4: {chief_res}\nProducer: {producer_res}")
