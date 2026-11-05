"""
Workflow: Lập trình C# và Rà soát Clean Code tự động
Thực thi tuần tự: Coder viết code -> Reviewer rà soát Clean Code -> Cập nhật docs/PROJECT_STATE.md & docs/TASKS.md
"""

task_description = args.get("task", "Thực hiện nhiệm vụ lập trình gameplay C# cho game Godot")

# -------------------------------------------------------------
# PHASE 1: C# CODE IMPLEMENTATION
# -------------------------------------------------------------
phase("Lập trình C# Gameplay")
coder = agent(
    prompt=(
        f"Bạn là Sub-agent csharp-coder.\n"
        f"Nhiệm vụ: {task_description}\n"
        f"Quy trình bắt buộc:\n"
        f"1. Đọc docs/PROJECT_STATE.md, docs/TASKS.md và docs/CODING_STANDARDS.md.\n"
        f"2. Nếu cần gán vật liệu/texture cho mesh, tra cứu Assets/Textures/TEXTURE_CATALOG.md và nạp từ Assets/Materials_Shared/.\n"
        f"3. Viết code C# theo Clean Code: mỗi hàm < 25 dòng, mỗi file < 200 dòng, Guard Clauses, XML tiếng Việt, [Export] Inspector.\n"
        f"4. Chạy 'dotnet build' đảm bảo 0 lỗi 0 cảnh báo.\n"
        f"5. Cập nhật thay đổi vào docs/PROJECT_STATE.md, docs/TASKS.md và docs/SESSION_HISTORY.md.\n"
        f"6. Gọi finish() trả về tóm tắt ngắn gọn dưới 10 dòng."
    ),
    role="C# Programmer",
    type_name="self",
    schema={"type": "string"}
)
coder_result = await coder(task_description, {"type": "string"})
log(f"[Coder]: {coder_result}")

# -------------------------------------------------------------
# PHASE 2: CLEAN CODE REVIEW & QA
# -------------------------------------------------------------
phase("Rà soát Clean Code & QA")
reviewer = agent(
    prompt=(
        "Bạn là Sub-agent code-reviewer.\n"
        "Quy trình bắt buộc:\n"
        "1. Đọc docs/CODING_STANDARDS.md.\n"
        "2. Rà soát toàn bộ các file C# vừa được tạo/sửa trong Scripts/.\n"
        "3. Nếu có hàm >= 25 dòng hoặc file >= 200 dòng -> Tách nhỏ và refactor ngay.\n"
        "4. Kiểm tra an toàn bộ nhớ: hủy sự kiện -= trong _ExitTree().\n"
        "5. Chạy 'dotnet build' kiểm tra 0 lỗi 0 cảnh báo.\n"
        "6. Cập nhật kết quả vào docs/SESSION_HISTORY.md và gọi finish() trả về tóm tắt dưới 5 dòng."
    ),
    role="Code Reviewer",
    type_name="self",
    schema={"type": "string"}
)
review_result = await reviewer("Rà soát các file code vừa tạo/sửa", {"type": "string"})
log(f"[Reviewer]: {review_result}")

print(f"=== KẾT QUẢ WORKFLOW ===\n{coder_result}\n\n[Đánh giá QA]:\n{review_result}")
