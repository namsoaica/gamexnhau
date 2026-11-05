"""
Workflow: Chuỗi Xử lý Texture và Xuất Model 3D Không Phình Dung Lượng
Thực thi tuần tự: Texture Architect tra cứu/tối ưu texture -> Blender Helper liên kết/xuất .glb -> Cập nhật trạng thái
"""

task_description = args.get("task", "Tối ưu hóa Texture và Model 3D")

# -------------------------------------------------------------
# PHASE 1: TEXTURE & MATERIAL SELECTION / GENERATION
# -------------------------------------------------------------
phase("Tối ưu hóa Texture & Material")
tex_arch = agent(
    prompt=(
        f"Bạn là Sub-agent texture-architect.\n"
        f"Nhiệm vụ: {task_description}\n"
        f"Quy trình bắt buộc:\n"
        f"1. Đọc Assets/Textures/TEXTURE_CATALOG.md.\n"
        f"2. Áp dụng cây quyết định 3 bước: Ưu tiên dùng lại .tres sẵn có -> Biến tấu từ Grayscale Masks -> Sinh ảnh mới Seamless/Grayscale lũy thừa 2.\n"
        f"3. Cập nhật mọi tài nguyên mới vào Assets/Textures/TEXTURE_CATALOG.md.\n"
        f"4. Gọi finish() trả về danh sách vật liệu sẵn sàng sử dụng."
    ),
    role="Texture Architect",
    type_name="self",
    schema={"type": "string"}
)
tex_result = await tex_arch(task_description, {"type": "string"})
log(f"[Texture Architect]: {tex_result}")

# -------------------------------------------------------------
# PHASE 2: 3D MODEL & MATERIAL INTEGRATION IN BLENDER
# -------------------------------------------------------------
phase("Tích hợp Model 3D Blender & Xuất GLB")
blender_helper = agent(
    prompt=(
        "Bạn là Sub-agent blender-helper.\n"
        "Quy trình bắt buộc:\n"
        "1. Bảo vệ tuyệt đối file .blend gốc, làm việc trên file an toàn.\n"
        "2. Không nhúng texture trùng lặp vào .glb. Đặt tên Material Slot chuẩn khớp với Assets/Materials_Shared/.\n"
        "3. Xuất file .glb chuẩn Godot 4 (export_yup=True, export_apply=True).\n"
        "4. Cập nhật thay đổi vào docs/PROJECT_STATE.md và docs/TASKS.md.\n"
        "5. Gọi finish() với tóm tắt ngắn gọn."
    ),
    role="Blender Assistant",
    type_name="self",
    schema={"type": "string"}
)
blender_result = await blender_helper("Liên kết vật liệu và xuất .glb", {"type": "string"})
log(f"[Blender Helper]: {blender_result}")

print(f"=== KẾT QUẢ ASSET PIPELINE ===\n{tex_result}\n\n[3D Export]:\n{blender_result}")
