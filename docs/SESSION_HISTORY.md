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

## Phiên làm việc: 2026-11-06 (Sáng - Sub-agent csharp-coder: Tái Thiết Ánh Sáng Môi Trường & Hệ Thống Dốc Cầu Thang)
- **Cải tạo ánh sáng, bóng đổ và bầu trời (`WorldMap.tscn`)**:
  - Khắc phục lỗi "1 màu trắng xóa" do ánh sáng chói lóa (ambient 0.8 + light 1.6 = 2.4, không có tonemap khiến màn hình clipping 100% white).
  - Cấu hình lại `WorldEnvironment`: `background_mode = 2` (Sky), `Sky` với `ProceduralSkyMaterial` (bầu trời xanh dịu mát: sky_top Color(0.35, 0.62, 0.95), sky_horizon Color(0.70, 0.82, 0.95), ground_bottom Color(0.22, 0.38, 0.22), ground_horizon Color(0.55, 0.72, 0.60)).
  - Bật ánh sáng môi trường dịu nhẹ `ambient_light_source = 3` (Sky), `ambient_light_energy = 0.45`.
  - Bắt buộc kích hoạt Tonemap `tonemap_mode = 3` (ACES), `tonemap_exposure = 1.0` giúp khử hiện tượng cháy sáng, tăng độ tương phản và màu sắc tự nhiên.
  - Bật `ssao_enabled = true` tạo bóng tiếp xúc chân thực dưới chân vách đá, cầu thang, cây cối.
  - Cấu hình lại `DirectionalLight3D`: `light_color = Color(1.0, 0.97, 0.91)`, `light_energy = 1.15`, `shadow_enabled = true`, `shadow_bias = 0.04`, `shadow_blur = 1.6`, `directional_shadow_mode = 2` (PSSM 4 splits), `directional_shadow_max_distance = 70.0`.
- **Khắc phục triệt để lỗi không leo được cầu thang (`SM_Staircase_01`, `SM_Staircase_02`)**:
  - `PlayerMovement.cs`: Nâng `FloorMaxAngle` lên 58 độ (`Mathf.DegToRad(58.0f)`), tinh chỉnh `FloorSnapLength = 0.40f` khi ở trên sàn giúp bám chặt mặt dốc thang không bị nảy.
  - Tạo mới `Scripts/Core/StairRampBuilder.cs`: Tự động phân tích hình học mesh cầu thang, tạo dốc va chạm phẳng `ConvexPolygonShape3D` dạng hình nêm lăng trụ (wedge) bao phủ từ chân thang lên đỉnh thang, mở rộng 5cm kết nối êm ái với sàn dưới và thềm trên.
  - Nâng cấp `Scripts/Core/MapAutoCollision.cs`: Điều phối gọi `StairRampBuilder.BuildStairRamp` cho các mesh cầu thang, đồng thời tự động áp dụng vật liệu cỏ xanh `GetOrCreatePaverMaterial()` cho cả `Terrain_Plains_Mesh` (và các mesh chứa `plains`) loại bỏ hoàn toàn màu trắng xung quanh đảo.
- **Kiểm định chất lượng**:
  - Tuân thủ 100% `CODING_STANDARDS.md`: File < 200 dòng, mỗi hàm < 25 dòng, Guard Clauses, XML tiếng Việt, an toàn bộ nhớ trong `_ExitTree()`.
  - `dotnet build`: **0 Warning(s), 0 Error(s)**.
  - Godot Headless `test_suite.gd`: Bổ sung 3 test suites (`test_lighting_and_sky`, `test_staircase_ramp_collision`, `test_plains_recolor`), **91 / 91 Test cases Passed (100% Pass, 0 Fail)**.

## Phiên làm việc: 2026-11-06 (Sáng - Sub-agent blender-helper: Đồng bộ Model Môi Trường Cỏ Xanh & Đo đạc Cầu Thang)
- **Khắc phục lỗi đất xung quanh trắng xóa trong `map_surroundings.blend`**:
  - Mở file `Assets/Blender_Source/map_surroundings.blend` bằng Blender 5.4 CLI.
  - Mesh `Terrain_Plains_Mesh` được gán vật liệu cỏ xanh `Mat_Grass_Plain` với Base Color tươi mát `#529934` (Color(0.32, 0.60, 0.20, 1.0)), Roughness = 0.85.
  - Tải và đóng gói (pack) trực tiếp texture `Assets/Blender_Source/tex_grass_grid.png` vào file blend, kết nối Image Texture `Color` -> Principled BSDF `Base Color`.
  - Cập nhật UV mapping dạng planar projection chiếu đứng `(u, v) = (x/4, y/4)` cho toàn bộ 1,896 mặt của `Terrain_Plains_Mesh`, hoa văn cỏ phủ đều tuyệt đối trên diện tích 84m x 84m.
  - Bảo tồn nguyên vẹn vị trí, xoay và vật liệu của toàn bộ 63 cây, 45 tảng đá, 36 hoa cúc và dãy núi phía Bắc `Mountain_Mesh_North`.
  - Lưu an toàn file blend vào `Assets/Blender_Source/map_surroundings.blend`.
  - Xuất mô hình sang `Assets/Models_Exported/map_surroundings.glb` chuẩn Godot (`export_yup=True`, `export_materials='EXPORT'`). Re-import tự động trích xuất texture vào Godot.
- **Đo đạc hình học chi tiết Cầu Thang trong `map_25d_fixed.blend`**:
  - `SM_Staircase_01`:
    - Kích thước AABB: X=[3.9250, 5.0750] (Rộng 1.15m), Y=[3.1960, 4.0040] (Dài 0.808m), Z=[0.0000, 1.2500] (Cao 1.25m).
    - Độ dốc (Rise/Run): 1.25 / 0.808 = 1.5470 -> Góc nghiêng: **57.12°**.
    - Bước bậc: 5 bậc, mỗi bậc cao (Rise) = **0.2500m** (25cm), sâu (Tread run) = **0.1600m** (16cm), góc nghiêng từng bước = **57.38°**.
  - `SM_Staircase_02`:
    - Kích thước AABB: X=[5.1500, 6.2500] (Rộng 1.10m), Y=[5.9958, 7.0042] (Dài 1.0083m), Z=[1.2500, 2.5000] (Cao 1.25m).
    - Độ dốc (Rise/Run): 1.25 / 1.0083 = 1.2397 -> Góc nghiêng: **51.11°**.
    - Bước bậc: 6 bậc, mỗi bậc cao (Rise) = **0.2083m** (~20.8cm), sâu (Tread run) = **0.1667m** (~16.7cm), góc nghiêng từng bước = **51.34°**.
  - Đã đối chiếu và xác nhận giải pháp collision ramp của `StairRampBuilder` (`ConvexPolygonShape3D`) kết hợp `FloorMaxAngle >= 58.0°` trong `PlayerMovement.cs` khớp hoàn hảo với thông số thực tế của mesh.
- **Kiểm định tự động**:
  - `dotnet build`: **0 Warning(s), 0 Error(s)**.
  - Godot Headless `test_suite.gd`: **91 / 91 Test cases Passed (100% Pass, 0 Fail)**.

## Phiên làm việc: 2026-11-06 (Sáng - Sub-agent blender-helper: Loại Bỏ Phông Nền Trắng Sky Backdrop)
- **Loại bỏ triệt để tấm phông nền trắng `SM_Sky_Backdrop_Plane`**:
  - Mở file `Assets/Blender_Source/map_25d_fixed.blend` bằng Blender 5.4 CLI.
  - Xác định và xóa sạch object `SM_Sky_Backdrop_Plane` (tấm plane 54x45m ở (13, 13, 7.5)), orphan mesh `Plane` và orphan material `Mat_Sky_Gradient` (vốn gây hiện tượng bức tường trắng xóa che khuất bầu trời ProceduralSky phía sau dãy núi).
  - Giữ nguyên vẹn 100% tất cả các đối tượng địa hình, cầu thang, nền gạch dày 0.42m thảm cỏ, dãy núi, mây và cây cỏ khác.
  - Tuân thủ quy tắc bảo toàn: Giữ nguyên vẹn 100% file gốc `map_25d.blend`.
  - Lưu file blend cập nhật an toàn vào `Assets/Blender_Source/map_25d_fixed.blend`.
- **Xuất mô hình ra Godot**:
  - Xuất sang `Assets/Models_Exported/map_25d.glb` (`export_yup=True`, `export_materials='EXPORT'`).
  - Kiểm tra import GLB: Số lượng objects giảm từ 232 xuống 231, không còn `SM_Sky_Backdrop_Plane` hay mesh `Plane`.
  - Re-import tài nguyên thành công trong Godot Editor Headless.
- **Kiểm định chất lượng**:
  - Bổ sung kiểm thử `assert_true(sky_plane == null, "SM_Sky_Backdrop_Plane removed (sky is clear and unobstructed)")` vào `test_suite.gd`.
  - Chạy Godot Headless `test_suite.gd`: **92 / 92 Test cases Passed (100% Pass, 0 Fail)**.
  - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.

## Phiên làm việc: 2026-11-06 (Trưa - Sub-agent csharp-coder: Chế Độ Camera Tự Do, Gamepad Toàn Diện & Khử Vùng Trắng Bầu Trời)
- **Xóa bỏ triệt để phông trắng trong mã nguồn (`MapAutoCollision.cs`)**:
  - Bổ sung hàm nhận diện `IsSkyBackdrop(string nodeName)`: quét các node chứa `sky_backdrop`, `backdrop`, `sky_plane`.
  - Tự động ẩn và giải phóng (`Visible = false; QueueFree();`), bảo đảm không có phông trắng nào che lấp bầu trời `ProceduralSky`.
- **Triển khai Chế độ Camera Tự Do (Free Cam Mode 6-DOF)**:
  - Tạo `Scripts/Core/FreeCameraController.cs` (156 dòng): Điều khiển bay 6 bậc tự do (WASD/LeftStick, Space/Ctrl/EQ/Triggers L2/R2, cuộn chuột/L3 đổi tốc độ 5-50 m/s, Right Click rê chuột hoặc RightStick xoay 360° Pitch/Yaw).
  - Nâng cấp `Scripts/Core/CameraFollow.cs` (155 dòng): Hỗ trợ `SetFreeCamActive(bool)` chuyển đổi linh hoạt Perspective/Orthogonal, `ResetToPlayer()` đưa góc nhìn về nhân vật, Zoom Isometric bằng cần gạt phải Gamepad.
  - Tách `Scripts/UI/DevWorldTab.cs` (161 dòng) & Nâng cấp `DevOverlay.tscn`: CheckBox bật/tắt FreeCam, Slider tốc độ, Nút quay về Player, hiển thị trạng thái camera, dọn dẹp sạch sẽ trong `_ExitTree()`.
- **Hỗ trợ kết nối Tay Cầm Gamepad toàn diện**:
  - Cấu hình `project.godot`: Bổ sung Joypad events cho `move_left`, `move_right`, `move_forward`, `move_backward`, `jump`, `interact`.
  - Nâng cấp `DevOverlay.cs` (153 dòng): Bật/tắt HUD bằng nút `Back`/`Select`, `Start` hoặc `R3`; chuyển đổi qua lại giữa các tab bằng nút vai `LB`/`RB`.
- **Kiểm định chất lượng & Clean Code**:
  - 100% file C# < 195 dòng (< 200 dòng), 100% hàm < 20 dòng (< 25 dòng), Guard Clauses, XML tiếng Việt.
  - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.
  - Mở rộng `test_suite.gd`: **117 / 117 Test cases Passed (100% Pass, 0 Fail)**.



