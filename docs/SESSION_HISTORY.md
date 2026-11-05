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

## Phiên làm việc: 2026-11-06 (Rạng sáng - Sửa Hướng Quay Mặt, Chống Xuyên Mép, Zoom Camera, Tương Tác NPC)
- **Sửa hướng quay mặt nhân vật (`PlayerMovement.cs`)**:
  - Xóa bỏ dấu âm làm ngược 180 độ; sửa công thức tính góc quay `Mathf.Atan2(horizontalVelocity.X, horizontalVelocity.Y)` khớp chuẩn với model `character_25d.glb` (mặt hướng +Z). Nhân vật nhìn thẳng về phía trước theo hướng di chuyển.
- **Chống lọt mép & xuyên rìa bậc thềm (`PlayerMovement.cs` & `MapAutoCollision.cs`)**:
  - `PlayerMovement.cs`: Thêm cấu hình `SafeMargin = 0.08f;`, `MaxSlides = 6;`, `WallMinSlideAngle = Mathf.DegToRad(15.0f);`.
  - `MapAutoCollision.cs`: Kích hoạt `concave.BackfaceCollision = true;` cho mọi `ConcavePolygonShape3D` của mesh địa hình, triệt tiêu lỗi xuyên mép bậc thang.
- **Đồng bộ nền gạch sang họa tiết & màu cỏ (`MapAutoCollision.cs`)**:
  - Sử dụng texture cỏ `tex_grass_grid.png` với `AlbedoColor = Colors.White` và `TextureFilter = BaseMaterial3D.TextureFilterEnum.LinearWithMipmaps`.
- **Thêm tính năng Zoom Camera bằng con lăn chuột (`CameraFollow.cs`)**:
  - Bắt sự kiện `MouseButton.WheelUp` (Zoom In) và `MouseButton.WheelDown` (Zoom Out), giới hạn từ 8.0 đến 30.0, nội suy Lerp mượt mà theo từng frame trong `_Process`.
- **Đưa NPC xuống mặt đất & hoàn thiện hội thoại (`WorldMap.tscn`, `SimpleNpc.cs`)**:
  - Đưa NPC từ `(3, 2.5, -6)` xuống `(5.0, 0.5, -4.0)` trên mặt đất đảo trung tâm.
  - Bật `NoDepthTest = true;`, tăng `FontSize = 36;`, `OutlineSize = 8;` cho `Label3D` trên đầu NPC giúp lời thoại hiển thị rõ ràng, không bị chìm hay che khuất.
- **Kiểm định tự động**:
  - `dotnet build`: **0 Warning(s), 0 Error(s)**.
  - Godot Headless `test_suite.gd`: **Passed: 63 / Failed: 0 (100% Pass)**.

## Phiên làm việc: 2026-11-06 (Sáng sớm - Sub-agent blender-helper: Cải tạo mô hình 3D bản đồ)
- **Đồng bộ thảm cỏ nền gạch `SM_Tier2_Pavers`**:
  - Gán vật liệu `Mat_Grass` kèm texture `Tex_Grass_Grid` (`tex_grass_grid.png`).
  - Cấu hình UV mapping phẳng (planar projection) chiếu đứng `(u, v) = (x, y)` cho mặt trên, họa tiết lưới cỏ ăn khớp 1:1 với địa hình đảo trung tâm.
- **Khắc phục triệt để khe hở bậc thềm & chống xuyên mép**:
  - Đo đạc thực tế: Cầu thang kết thúc ở Y = 7.004m, nền gạch cũ bắt đầu ở Y = 7.040m (hở 3.6cm, chỉ dày 2.5cm).
  - Mở rộng mép tiếp giáp của `SM_Tier2_Pavers` về `Y = 6.99m`, đè lên bậc thang 1.4cm đóng kín 100% khe hở.
  - Kéo đùn (extrude) độ dày sâu xuống đất thêm 0.40m (`Z` từ 2.10m đến 2.52m), kèm khối móng đặc liên kết tạo thành khối 3D đặc vững chắc chống xuyên mép/rìa.
- **Quy tắc bảo toàn Blender**:
  - File gốc `map_25d.blend` được bảo tồn nguyên vẹn 100%.
  - Lưu an toàn file cập nhật vào `Assets/Blender_Source/map_25d_fixed.blend`.
  - Xuất mô hình `Assets/Models_Exported/map_25d.glb` chuẩn Godot (-Z forward, Y up).
- **Kiểm định tự động**:
  - Bổ sung test case `test_paver_stair_gap_and_thickness` vào `test_suite.gd`.
  - Godot Headless `test_suite.gd`: **Passed: 66 / Failed: 0 (100% Pass)**.
  - `dotnet build`: **0 Warning(s), 0 Error(s)**.

## Phiên làm việc: 2026-11-06 (Sáng sớm - Sub-agent csharp-coder: Xây Dựng Chế Độ Dev Mode / Debug Overlay HUD)
- **Hệ thống phím tắt Toggle & Quản lý chuột (`DevOverlay.cs`)**:
  - Hỗ trợ phím tắt `F1`, `~` (QuoteLeft / Tilde) và `F3` để bật/tắt HUD trên cùng (`CanvasLayer` layer 100).
  - Tự động mở khóa chuột (`Input.MouseMode = Visible`) khi mở bảng điều khiển.
  - Tự động dò tìm các node `PlayerMovement`, `CameraFollow`, `SimpleNpc` trong scene tree.
- **Tab 1: Nhân Vật (`DevPlayerTab.cs`)**:
  - Tinh chỉnh tốc độ chạy (`MoveSpeed`: 2.0 -> 25.0), lực nhảy (`JumpVelocity`: 5.0 -> 25.0), trọng lực (`Gravity`: 5.0 -> 40.0) với nhãn hiển thị số thực trực tiếp.
  - Bật/tắt chế độ Nhảy Vô Hạn / Bất Tử (`InfiniteJump`) cho phép nhảy liên tục trên không.
  - Nút dịch chuyển tức thời về điểm xuất phát ban đầu (`TeleportTo(SpawnPosition)`).
- **Tab 2: Trình Chỉnh Sửa Hội Thoại Trực Tiếp (`DevNpcTab.cs`)**:
  - Hiển thị tên NPC, danh sách câu thoại dạng `ItemList`.
  - Ô nhập `LineEdit` và nút Thêm Thoại (ghi trực tiếp vào mảng `DialogueLines`).
  - Nút Nói Ngay (`DisplayMessage`) và Xoay Vòng Thoại (`SpeakNextLine`).
  - Nút Xóa Thoại đã chọn.
- **Tab 3: Camera & Môi Trường (`DevWorldTab`)**:
  - Thanh trượt Zoom Camera (8.0 -> 35.0) đồng bộ trực tiếp với `CameraFollow.TargetZoomSize`.
  - Hiển thị thông số thời gian thực: FPS và tọa độ `Player Pos: (X, Y, Z)`.
  - Nút Tải lại màn chơi (`ReloadCurrentScene`).
- **Tích hợp Scene (`Scenes/UI/DevOverlay.tscn` & `Scenes/Levels/WorldMap.tscn`)**:
  - Giao diện PanelContainer bán trong suốt, bo góc, tích hợp sẵn vào `WorldMap.tscn`.
- **Kiểm định Clean Code & Biên dịch**:
  - 100% file < 200 dòng, mọi hàm < 20 dòng (< 25 dòng), an toàn bộ nhớ hủy sự kiện trong `_ExitTree()`.
  - `dotnet build`: **0 Warning(s), 0 Error(s)**.

