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

## Phiên làm việc: 2026-11-06 (Khuya - Sửa Lỗi Vật Lý & Hệ Thống Tương Tác / Hội Thoại)
- **Sửa lỗi Hội thoại & Tương tác**:
  - Khắc phục lỗi lệch Physics Layer: Chuyển `InteractableArea.cs` sang `CollisionLayer = (1 << 2) | (1 << 3)` (Layer 3 NPC & Layer 4 Interactable) và `CollisionMask = 0`, giúp `PlayerInteractor` nhận diện NPC ngay lập tức.
  - Khắc phục trải nghiệm hội thoại trong `SimpleNpc.cs`: Quản lý cờ `_isFocused`, sau khi hết 4 giây ẩn thoại thì chuyển nhãn hiển thị về `[Tên NPC]\n(Ấn E để tiếp tục trò chuyện)` thay vì biến mất hoàn toàn.
  - Cải tiến bắt phím E trong `PlayerInteractor.cs`: Kiểm tra `Input.IsActionJustPressed(ActionName)` ngay trong `_PhysicsProcess` kèm cơ chế chống kích hoạt kép theo `Engine.GetProcessFrames()`.
- **Sửa lỗi Vật lý & Môi trường**:
  - Khắc phục lỗi FloorSnap kéo giật nhân vật dính sàn khi nhảy trong `PlayerMovement.cs`: Đặt `FloorSnapLength = 0.0f` khi nhảy hoặc ở trên không, chỉ phục hồi `DefaultFloorSnap` (0.35m) khi tiếp đất ổn định; bổ sung `FloorStopOnSlope` và `FloorBlockOnWall`.
  - Tự động đổi màu nền gạch sang màu xanh cỏ trong `MapAutoCollision.cs`: Nhận diện mesh `paver` / `Tier2_Pavers` và áp dụng `StandardMaterial3D` xanh cỏ đồng bộ màu sắc cảnh quan.
- **Kiểm thử & Clean Code**:
  - Tuân thủ 100% `CODING_STANDARDS.md`: Mọi hàm < 25 dòng, mọi file < 200 dòng.
  - Mở rộng kịch bản kiểm thử `test_suite.gd`: Nâng tổng số bài test lên 47. Kết quả Godot Headless: **47/47 Passed (100%)**.
  - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.

## Phiên làm việc: 2026-11-06 (Đêm - Kiểm Định Toàn Diện Chất Lượng Code & QA Audit)
- **Rà soát Clean Code toàn bộ 9 file C# trong `Scripts/`**:
  - Đo lường số dòng: Tất cả các file đều < 195 dòng (nằm trong chuẩn 150 - 200 dòng).
  - Đo lường độ dài hàm: 100% hàm <= 19 dòng (đạt chỉ tiêu < 25 dòng).
  - Cấu trúc: 100% tuân thủ Guard Clauses, không lồng ghép `if` quá 2 cấp, không dùng số ma thuật, comment XML tiếng Việt chuẩn chỉnh.
- **Tối ưu hóa và làm gọn (Refactoring Buffer)**:
  - Tinh gọn nhẹ `PlayerInteractor.cs` từ 198 dòng xuống 189 dòng để giữ vùng đệm an toàn.
  - Tinh gọn nhẹ `PlayerAnimation.cs` từ 195 dòng xuống 193 dòng.
- **Kiểm định rò rỉ bộ nhớ (Memory Safety Check)**:
  - Xác nhận 100% các sự kiện `+=` đều có hủy `-=` trong `_ExitTree()` (`VoidKillZone.cs`, `SimpleNpc.cs`, `PlayerInteractor.cs`).
- **Kiểm định tự động**:
  - `dotnet build`: **0 Warning(s), 0 Error(s)**.
  - Godot Headless `test_suite.gd`: **Passed: 53 / Failed: 0 (100% Pass)**.
