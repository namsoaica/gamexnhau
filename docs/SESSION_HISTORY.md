# LỊCH SỬ PHIÊN LÀM VIỆC (SESSION HISTORY)

## Phiên làm việc: 2026-11-05
- **Khởi tạo nhân vật**: Viết `PlayerMovement.cs` và `PlayerAnimation.cs` theo Clean Code.
- **Tích hợp bản đồ**: Đưa `map_25d.glb` vào `Assets/Models_Exported/`, viết `MapAutoCollision.cs`, `CameraFollow.cs`.
- **Sửa lỗi UID**: Đồng bộ toàn bộ mã UID giữa `Player.tscn`, `WorldMap.tscn`, `TestLevel.tscn` để lưu Scene 100% không bị lỗi đỏ.
- **Khởi tạo tài liệu**: Tạo `docs/PROJECT_STATE.md`, `docs/TASKS.md`, `docs/SESSION_HISTORY.md`.

## Phiên làm việc: 2026-11-06 (Sáng - Chiều)
- **Thiết lập hệ thống Sub-agent tự động (.agents/)**:
  - Chuẩn hóa 5 kỹ năng Sub-agent tại `.agents/skills/`: `csharp-coder`, `code-reviewer`, `producer`, `blender-helper`, `checkpoint`.
  - Thiết lập quy tắc trong `AGENTS.md` & `GEMINI.md`: Luồng chính chỉ điều phối (Orchestrator).
  - Xây dựng 2 kịch bản workflow tự động tại `.agents/workflows/`: `dev_and_review.py` và `checkpoint_and_reset.py`.
- **Mở rộng thế giới 2.5D Isometric (`map_surroundings.glb`)**:
  - Dùng Blender 5.4 CLI tạo `Assets/Blender_Source/map_surroundings.blend` và xuất `Assets/Models_Exported/map_surroundings.glb` (cánh đồng 84x84m, 4 dãy núi bao quanh, 45 tảng đá, 70 cây, 90 cụm hoa).
  - Cập nhật `MapAutoCollision.cs` tự động tạo va chạm cho núi đá và cánh đồng.
  - Tích hợp vào `WorldMap.tscn`, kiểm thử vật lý di chuyển và va chạm trơn tru.
- **Chuẩn hóa hạ tầng cộng tác nhóm & Thiết lập tài liệu (Multi-developer Setup)**:
  - Hoàn thiện `.gitignore`, `.gitattributes`, `.editorconfig`.
  - Tạo `README.md` chuyên nghiệp tại thư mục gốc và tạo hardlink đồng bộ sang dự án Godot.
  - Xây dựng `docs/CONTRIBUTING.md` và mục 4 "Quy Trình Cộng Tác Nhóm" trong `README.md`.

## Phiên làm việc: 2026-11-06 (Tối - Rà soát Code Review & Sáp nhập nhánh dev của AiichaN)
- **Rà soát mã nguồn (Code Review) nhánh `origin/dev`**:
  - Rà soát các tính năng mới: Giao diện tương tác `IInteractable`, vùng va chạm `InteractableArea`, NPC lời thoại billboard 3D `SimpleNpc`, vùng rơi vực tự hồi sinh `VoidKillZone`, bộ dò tương tác `PlayerInteractor`, Coyote Time & Jump Buffer trong `PlayerMovement`, và Procedural Animation trong `PlayerAnimation`.
  - **Phát hiện & Sửa lỗi rò rỉ bộ nhớ (Memory Leaks)**:
    1. `SimpleNpc.cs`: Không hủy delegate timer cũ khi bấm nói chuyện liên tục và thiếu `_ExitTree()` hủy delegate `_hideTimer.Timeout`. Đã refactor triệt tiêu 100%.
    2. `VoidKillZone.cs`: Đăng ký `BodyEntered += OnBodyEntered` nhưng thiếu `_ExitTree()` hủy đăng ký. Đã bổ sung `BodyEntered -= OnBodyEntered`.
    3. `PlayerInteractor.cs`: Đăng ký `AreaEntered` và `AreaExited` nhưng thiếu `_ExitTree()` hủy đăng ký. Đã bổ sung hủy đăng ký sạch sẽ.
- **Sáp nhập Git (Merge) vào nhánh `main`**:
  - Hợp nhất thành công `origin/dev` vào `main` (commit `e324f53`).
  - Xử lý xung đột `WorldMap.tscn`: Bảo tồn trọn vẹn Instance mở rộng `Map_Surroundings` đồng thời tích hợp thêm `NPC` và `VoidKillZone`.
  - Xử lý xung đột `.gitignore` & `PlayerAnimation.cs`.
  - Khôi phục `nuget.config` cho môi trường máy chủ.
- **Kiểm thử & Xác thực**:
  - Chạy `test_suite.gd` trên Godot Headless: **32/32 Passed (100%)**.
  - `dotnet build`: **0 Warning(s), 0 Error(s)**.
