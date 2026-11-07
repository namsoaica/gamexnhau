"""
Workflow: Tháp Giám Sát Phân Cấp 3 Tầng (Hierarchical 3-Tier Supervision Pipeline)
Thực thi tuần tự:
- Tầng 1: Thợ (@texture-architect, @blender-helper, @csharp-coder) làm việc
          -> Giám sát riêng (@texture-inspector, @blender-inspector, @csharp-inspector) duyệt/ép sửa tại chỗ
- Tầng 2: Giám Sát Tổng Quản (@chief-supervisor) kiểm định thực tế toàn game
          (chạy test_suite.gd Windowed, soi 4 ảnh màn hình, kiểm tra Timestamp)
- Tầng 3: Lead Orchestrator cập nhật docs/PROJECT_STATE.md và báo cáo kết quả
"""

task_description = args.get("task", "Thực hiện nhiệm vụ nâng cấp game theo mô hình Tháp Giám Sát Phân Cấp 3 Tầng")

# -------------------------------------------------------------
# PHASE 1: C# & GAMEPLAY IMPLEMENTATION + 1-ON-1 SUPERVISION
# -------------------------------------------------------------
phase("Tầng 1: Thợ Lập Trình & Giám Sát C# Riêng")
coder = agent(
    prompt=(
        f"Bạn là Sub-agent csharp-coder.\n"
        f"Nhiệm vụ: {task_description}\n"
        f"Quy trình bắt buộc:\n"
        f"1. Đọc docs/PROJECT_STATE.md, docs/TASKS.md và docs/CODING_STANDARDS.md.\n"
        f"2. Viết code C# theo Clean Code: mỗi hàm < 25 dòng, mỗi file < 200 dòng, Guard Clauses, hủy sự kiện -= trong _ExitTree().\n"
        f"3. Khớp AABB CollisionShape3D với Mesh, kiểm tra Input Action trong project.godot.\n"
        f"4. Chạy 'dotnet build' đảm bảo 0 lỗi 0 cảnh báo.\n"
        f"5. Bàn giao kết quả cho @csharp-inspector nghiệm thu."
    ),
    role="C# Programmer",
    type_name="self",
    schema={"type": "string"}
)
coder_result = await coder(task_description, {"type": "string"})
log(f"[Coder]: {coder_result}")

# Giám sát viên 1-kèm-1 của C#
cs_inspector = agent(
    prompt=(
        "Bạn là Sub-agent csharp-inspector (Giám sát riêng 1-kèm-1 của @csharp-coder).\n"
        "Quy trình kiểm soát cứng:\n"
        "1. Chạy lệnh: python tools/supervisor_gate.py\n"
        "2. Kiểm tra 100% hàm < 25 dòng, file < 200 dòng, an toàn bộ nhớ, Input Action và dotnet build.\n"
        "3. Nếu có vi phạm -> Ép @csharp-coder refactor lại ngay lập tức tại chỗ.\n"
        "4. Chỉ khi exit code là 0 mới ký duyệt PASS và bàn giao lên @chief-supervisor."
    ),
    role="C# Inspector Gatekeeper",
    type_name="self",
    schema={"type": "string"}
)
cs_pass = await cs_inspector("Kiểm định Clean Code và chất lượng mã nguồn", {"type": "string"})
log(f"[C# Inspector Gatekeeper]: {cs_pass}")

# -------------------------------------------------------------
# PHASE 2: CHIEF SUPERVISOR PLAYTEST & WHOLE-GAME INTEGRATION
# -------------------------------------------------------------
phase("Tầng 2: Giám Sát Tổng Quản Độc Lập (@chief-supervisor)")
chief = agent(
    prompt=(
        "Bạn là Sub-agent chief-supervisor (Giám Sát Tổng Quản Độc Lập).\n"
        "Quy trình nghiệm thu bắt buộc:\n"
        "1. Xác nhận các giám sát con đã ký duyệt PASS.\n"
        "2. Chạy test_suite.gd ở chế độ Windowed Rendering bằng Godot Mono Console (CẤM dùng --headless):\n"
        "   & \"C:\\xnhaugame\\Godot_v4.7.2-stable_mono_win64\\Godot_v4.7.2-stable_mono_win64\\Godot_v4.7.2-stable_mono_win64_console.exe\" --script test_suite.gd\n"
        "3. Kiểm tra Timestamp 4 ảnh trong docs/test_screenshots/ đảm bảo mới hơn code.\n"
        "4. Dùng Vision (read_file) mở trực tiếp 4 ảnh (1_map_overview.png, 2_interior_view.png, 3_npc_ui.png, 4_devtools_ui.png) đối chiếu song song với modelyeucau/.\n"
        "5. Nếu có lỗi ghép nối -> Điều phối trả ngược task về cặp Thợ-Giám sát con sửa tiếp (Reverse Loop).\n"
        "6. Khi đạt 100% PASS và ảnh thẩm mỹ hoàn hảo -> Quét ổ cứng thực tế, cập nhật docs/PROJECT_STATE.md, docs/TASKS.md, docs/SESSION_HISTORY.md và báo cáo hoàn thành."
    ),
    role="Chief Supervisor",
    type_name="self",
    schema={"type": "string"}
)
chief_result = await chief("Thực hiện kiểm định tích hợp và nghiệm thu thị giác toàn game", {"type": "string"})
log(f"[Chief Supervisor]: {chief_result}")

print(f"=== KẾT QUẢ THÁP GIÁM SÁT 3 TẦNG ===\n[Coder]: {coder_result}\n[C# Gatekeeper]: {cs_pass}\n[Chief Supervisor]: {chief_result}")
