"""
Workflow: Lập trình C# và Rà soát Clean Code tự động (Hierarchical 3-Tier Gate)
Thực thi tuần tự:
- Thợ C# (@csharp-coder) lập trình
- Giám sát C# (@csharp-inspector) chạy tools/supervisor_gate.py duyệt/ép sửa tại chỗ
- Giám sát tổng quản (@chief-supervisor) kiểm định thực tế Windowed Playtest & Vision 4 ảnh
"""

task_description = args.get("task", "Thực hiện nhiệm vụ lập trình gameplay C# cho game Godot")

# -------------------------------------------------------------
# PHASE 1: C# CODE IMPLEMENTATION
# -------------------------------------------------------------
phase("Tầng 1: Lập trình C# Gameplay")
coder = agent(
    prompt=(
        f"Bạn là Sub-agent csharp-coder.\n"
        f"Nhiệm vụ: {task_description}\n"
        f"Quy trình bắt buộc:\n"
        f"1. Đọc docs/PROJECT_STATE.md, docs/TASKS.md và docs/CODING_STANDARDS.md.\n"
        f"2. Nếu cần gán vật liệu/texture cho mesh, tra cứu Assets/Textures/TEXTURE_CATALOG.md và nạp từ Assets/Materials_Shared/.\n"
        f"3. Viết code C# theo Clean Code: mỗi hàm < 25 dòng, mỗi file < 200 dòng, Guard Clauses, XML tiếng Việt, hủy -= trong _ExitTree().\n"
        f"4. Chạy 'dotnet build' đảm bảo 0 lỗi 0 cảnh báo.\n"
        f"5. Bàn giao cho @csharp-inspector nghiệm thu."
    ),
    role="C# Programmer",
    type_name="self",
    schema={"type": "string"}
)
coder_result = await coder(task_description, {"type": "string"})
log(f"[Coder]: {coder_result}")

# -------------------------------------------------------------
# PHASE 2: 1-ON-1 C# INSPECTION GATEKEEPER
# -------------------------------------------------------------
phase("Tầng 1: Giám Sát C# Riêng 1-Kèm-1 (@csharp-inspector)")
inspector = agent(
    prompt=(
        "Bạn là Sub-agent csharp-inspector.\n"
        "Quy trình kiểm định cứng:\n"
        "1. Chạy python tools/supervisor_gate.py\n"
        "2. Kiểm tra hàm < 25 dòng, file < 200 dòng, an toàn bộ nhớ, Input Action trong project.godot và dotnet build 0 lỗi.\n"
        "3. Nếu vi phạm bất kỳ tiêu chí nào -> Bắt @csharp-coder sửa lại tại chỗ.\n"
        "4. Chỉ khi exit code là 0 mới ký duyệt PASS và bàn giao lên @chief-supervisor."
    ),
    role="C# Inspector Gatekeeper",
    type_name="self",
    schema={"type": "string"}
)
inspect_result = await inspector("Rà soát các file code vừa tạo/sửa", {"type": "string"})
log(f"[C# Inspector]: {inspect_result}")

# -------------------------------------------------------------
# PHASE 3: CHIEF SUPERVISOR PLAYTEST & WHOLE-GAME QA
# -------------------------------------------------------------
phase("Tầng 2: Giám Sát Tổng Quản Độc Lập (@chief-supervisor)")
chief = agent(
    prompt=(
        "Bạn là Sub-agent chief-supervisor.\n"
        "Quy trình bắt buộc:\n"
        "1. Nhận bàn giao khi @csharp-inspector đã ký duyệt PASS.\n"
        "2. Chạy test_suite.gd bằng Godot Mono Console (không dùng cờ --headless) để render và chụp 4 ảnh màn hình vào docs/test_screenshots/ (1_map_overview.png, 2_interior_view.png, 3_npc_ui.png, 4_devtools_ui.png).\n"
        "3. Kiểm tra Timestamp 4 ảnh mới hơn code.\n"
        "4. Dùng công cụ đọc ảnh Vision soi từng bức ảnh (kiểm tra ánh sáng, che khuất góc nhìn, lún đất, vỡ UI).\n"
        "5. Nếu phát hiện lỗi thị giác -> Thực hiện Reverse Loop trả về cặp Coder-Inspector sửa tiếp đến khi hoàn hảo.\n"
        "6. Cập nhật kết quả vào docs/PROJECT_STATE.md, docs/TASKS.md, docs/SESSION_HISTORY.md và kết thúc."
    ),
    role="Chief Supervisor",
    type_name="self",
    schema={"type": "string"}
)
chief_result = await chief("Thực hiện kiểm định tích hợp và nghiệm thu thị giác toàn game", {"type": "string"})
log(f"[Chief Supervisor]: {chief_result}")

print(f"=== KẾT QUẢ WORKFLOW ===\n{coder_result}\n\n[Đánh giá Gatekeeper]:\n{inspect_result}\n\n[Chief Supervisor]:\n{chief_result}")
