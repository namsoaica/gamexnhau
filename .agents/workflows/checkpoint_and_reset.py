"""
Workflow: Đóng gói trạng thái phiên làm việc (Checkpoint)
Thu thập toàn bộ thay đổi và cập nhật vào docs/PROJECT_STATE.md và docs/SESSION_HISTORY.md
"""

phase("Đóng gói trạng thái dự án")
checkpoint_agent = agent(
    prompt=(
        "Bạn là Sub-agent checkpoint.\n"
        "Quy trình:\n"
        "1. Quét toàn bộ thay đổi code C#, Scene và Asset vừa thực hiện.\n"
        "2. Cập nhật đầy đủ vào docs/PROJECT_STATE.md để một AI mới tinh đọc vào hiểu 100%.\n"
        "3. Ghi nhật ký tóm tắt phiên làm việc vào docs/SESSION_HISTORY.md.\n"
        "4. Gọi finish() với đúng 1 dòng thông điệp bàn giao ngắn gọn."
    ),
    role="Context Manager",
    type_name="self",
    schema={"type": "string"}
)
result = await checkpoint_agent("Đóng gói trạng thái hiện tại", {"type": "string"})
log(f"[Checkpoint]: {result}")
print(f"=== ĐÃ ĐÓNG GÓI TRẠNG THÁI ===\n{result}")
