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

## Phiên làm việc: 2026-11-06 (Chiều - Sub-agent blender-helper: Mở Rộng Đài Cao Tầng 2, Xóa Đường Kẻ Ô Vuông Nền Cỏ & Dọn Bớt Núi Nón Tím)
- **Mở rộng đài cao (Tier 2 Terrace / Pavers) & Lan can hàng rào gỗ**:
  - Khảo sát hình học thực tế: Trước đây `SM_Tier2_Pavers` chỉ có kích thước 0.94m x 0.97m (~0.91 m²) rất chật hẹp, hàng rào gỗ cũ chắn ngang ngay trước mặt nhân vật tại Y=7.50m.
  - Tái thiết kế & mở rộng `SM_Tier2_Pavers`:
    * Chiều rộng mới theo trục X: từ 4.80m đến 7.40m (**Rộng 2.60m**, gấp ~2.76 lần).
    * Chiều dài mới theo trục Y: từ 6.99m đến 9.40m (**Dài 2.41m**, gấp ~2.48 lần).
    * Độ dày Z: từ 2.10m đến 2.52m (**Dày 0.42m** dạng khối 3D đặc monolithic vững chắc, móng cắm sâu vào địa hình).
    * Diện tích mặt sàn đài cao mới: **6.27 m²** (gấp ~6.8 lần diện tích cũ 0.91 m²), tạo thành một đài vọng cảnh/ban công tầng 2 rộng rãi, thoáng đãng.
    * Điểm tiếp giáp đỉnh thang: Bắt đầu tại Y = 6.990m đè nhẹ 1.4cm lên đỉnh cầu thang `SM_Staircase_02` (kết thúc ở Y = 7.004m), đảm bảo **0 gap**, kín khít tuyệt đối không có khe hở cho nhân vật rơi.
  - Tái thiết kế hàng rào gỗ `SM_Fence_Wood_Overlook`:
    * Gồm 9 cột gỗ (tiết diện 0.12x0.12m, cao 0.78m kèm chóp nhọn pyramid 0.10m) và các thanh ray đôi chạy quanh 3 mặt mép đài cao (Tây: X=4.88m, Bắc: Y=9.32m, Đông: X=7.32m).
    * Chừa lối thông thoáng rộng 1.24m tại mép Nam (X in [5.08, 6.32] tại Y=7.06m) thông thẳng từ đầu cầu thang bước lên đài vọng cảnh, không còn vật cản trước mặt nhân vật.
  - Tinh chỉnh bố cục: Xóa miếng dán decal `SM_Overlook_Dirt_Pad` để đài cao là thảm cỏ xanh liền mạch; dời biển báo `SM_Signpost_Overlook` về góc đẹp Tây Bắc (5.25, 8.85).
- **Xóa triệt để các đường kẻ ô vuông trên nền cỏ (Clean Organic Grass Texture)**:
  - Viết script Python tạo texture cỏ mới `tex_grass_clean.png` (512x512):
    * Màu xanh tươi mát tự nhiên chuẩn `#529934` (sRGB RGB: 0.322, 0.600, 0.204), Roughness 0.85.
    * Thảm cỏ mềm mịn hữu cơ (multi-octave value noise + vi sợi organic), tuần hoàn seamless 100%.
    * **TUYỆT ĐỐI KHÔNG CÓ CÁC ĐƯỜNG KẺ Ô VUÔNG, LƯỚI GRID HAY CHECKERBOARD BÀN CỜ**.
  - Triển khai và đồng bộ:
    * Đặt file texture tại `Assets/Blender_Source/textures/tex_grass_clean.png`, `Assets/Blender_Source/tex_grass_clean.png`, và `Assets/Models_Exported/tex_grass_clean.png`.
    * Đồng bộ ghi đè toàn bộ các file `tex_grass_grid.png` cũ để triệt tiêu vĩnh viễn tàn dư ô lưới.
    * Cập nhật `Mat_Grass` trong `map_25d_fixed.blend` và `Mat_Grass_Plain` trong `map_surroundings.blend`, đóng gói (pack) trực tiếp vào file `.blend`.
    * Cập nhật `MapAutoCollision.cs`: `GrassTexturePath = "res://Assets/Models_Exported/tex_grass_clean.png"`.
- **Xóa bớt các ngọn núi nón tím chen chúc (`SM_Mountains_Background`)**:
  - Khảo sát: Cụm núi tím cũ có 7 peaks chen chúc, trong đó Peak 4 và Peak 5 nằm sát sàn sạt ngay sau đài cao (Y in [6, 13]) che kín toàn bộ bầu trời.
  - Xóa bỏ 5 chóp núi nón chật chội: Peak 0, Peak 2, Peak 4, Peak 5, Peak 6.
  - Giữ lại đúng 2 ngọn núi nền phía xa tạo điểm nhấn thanh thoát: Peak 1 (ngọn núi chính cao nhất 9.8m ở xa Y=[9.15, 16.81]) và Peak 3 (núi xa phía Đông). Mở toang không gian bầu trời xanh ProceduralSky và mây hoạt hình phía sau đài cao.
- **Quy tắc bảo toàn Blender**:
  - File gốc `map_25d.blend` và `character_25d.blend` được bảo tồn nguyên vẹn 100% (không ghi đè).
  - Lưu trữ an toàn cập nhật vào `Assets/Blender_Source/map_25d_fixed.blend` và `Assets/Blender_Source/map_surroundings.blend`.
  - Xuất mô hình `Assets/Models_Exported/map_25d.glb` và `Assets/Models_Exported/map_surroundings.glb` chuẩn Godot (-Z forward, Y up, `export_yup=True`).
- **Kiểm định chất lượng & Tự động hóa**:
  - Mở rộng kịch bản kiểm thử `test_suite.gd` lên 128 bài test (kiểm tra kích thước đài cao, hàng rào, texture cỏ sạch không ô vuông, núi thoáng đãng).
  - Kết quả Godot Headless `test_suite.gd`: **128 / 128 Test cases Passed (100% Pass, 0 Fail)**.
  - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.

## Phiên làm việc: 2026-11-06 (Chiều muộn - Sub-agent csharp-coder: Khóa Nhân Vật Đứng Im Khi Bật Free Cam & Đồng Bộ Mã Nguồn Cỏ Không Ô Vuông)
- **Khóa nhân vật đứng im hoàn toàn trong Chế độ Camera Tự Do (Free Cam)**:
  - Khắc phục triệt để hiện tượng khi bật Free Cam 6-DOF, phím WASD / cần gạt Gamepad vừa điều khiển camera bay vừa làm Player chạy và xoay mặt theo.
  - Cập nhật `Scripts/Core/CameraFollow.cs` (140 dòng):
    * Khai báo static accessor chuẩn mực: `public static CameraFollow? Instance { get; private set; }`.
    * Đăng ký `Instance = this;` trong `_Ready()` và hủy `Instance = null;` an toàn bộ nhớ trong `_ExitTree()`.
  - Nâng cấp `Scripts/Player/PlayerMovement.cs` (167 dòng):
    * Bổ sung kiểm tra Guard Clause `IsFreeCamActive()` (`CameraFollow.Instance?.IsFreeCamActive == true`).
    * Khi FreeCam đang bật: Triệt tiêu hoàn toàn vận tốc ngang `StopHorizontalMovement()` (`Velocity = new Vector3(0, Velocity.Y, 0)`), bỏ qua việc đọc input di chuyển `_inputVector`, bỏ qua xử lý nhảy `HandleJump()`, không cập nhật gia tốc ngang `ApplyMovement()` và dừng quay mặt `ApplyRotation()`. Vẫn giữ trọng lực và snap sàn `MoveAndSlide()` để nhân vật tiếp đất ổn định, không bị kẹt hay rơi xuyên map.
    * Khi tắt FreeCam quay về Isometric: Nhân vật lập tức nhận lại toàn bộ điều khiển di chuyển bình thường mượt mà.
  - Nâng cấp `Scripts/Player/PlayerAnimation.cs` (174 dòng):
    * Bổ sung hàm `PlayIdleState(float delta)`: Khi FreeCam đang bật, giữ nguyên clip hoạt ảnh `Idle` (hoặc model ở tư thế chuẩn) và gọi `ResetProcedural(delta)` để triệt tiêu toàn bộ hiệu ứng nghiêng mình (lean) và nhấp nhô (bobbing) thủ tục.
- **Đồng bộ mã nguồn vật liệu cỏ không đường kẻ ô vuông (`MapAutoCollision.cs`)**:
  - Cập nhật `GrassTexturePath = "res://Assets/Models_Exported/tex_grass_clean.png"`.
  - Cải tiến `LoadGrassTexture()` quét danh sách các ứng viên texture cỏ mịn sạch (`tex_grass_clean.png` tại `Assets/Models_Exported/` và `Assets/Blender_Source/textures/`).
  - Trong `GetOrCreatePaverMaterial()`: Tạo fallback vật liệu `StandardMaterial3D` chuẩn màu xanh cỏ tươi mịn tự nhiên `#529934` (`AlbedoColor = new Color(0.32f, 0.60f, 0.20f, 1.0f)`, `Roughness = 0.85f`), đảm bảo tuyệt đối không còn đường kẻ ô vuông nào xuất hiện trên toàn bộ bản đồ.
- **Đảm bảo va chạm kín khít cho đài cao tầng 2 và cầu thang**:
  - Xác nhận `MapAutoCollision.cs` và `StairRampBuilder.cs` tự động tính toán kích thước AABB thực tế khi đài cao tầng 2 (`SM_Tier2_Pavers`, `SM_Terrain_Chunk`, `SM_Fence_Wood_Overlook`) được mở rộng.
  - Tạo khối dốc phẳng `ConvexPolygonShape3D` và kích hoạt `BackfaceCollision = true` cho mọi bề mặt `ConcavePolygonShape3D`, đảm bảo chuyển tiếp bậc thang êm ru, kín khít, 0 khe hở.
- **Kiểm định chất lượng, Clean Code & Tự động hóa**:
  - Tuân thủ 100% `CODING_STANDARDS.md`: Tất cả 15 file C# đều < 175 dòng (< 200 dòng), 100% hàm <= 16 dòng (< 25 dòng), Guard Clauses, XML tiếng Việt, dọn dẹp bộ nhớ sạch sẽ trong `_ExitTree()`.
  - Mở rộng kịch bản kiểm thử `test_suite.gd` lên 131 bài test (bổ sung bài kiểm tra nhân vật đứng im khi FreeCam bật và di chuyển bình thường khi FreeCam tắt).
  - Kết quả Godot Headless `test_suite.gd`: **131 / 131 Test cases Passed (100% Pass, 0 Fail)**.
  - Biên dịch `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.

## Phiên làm việc: 2026-11-06 (Đêm - Sub-agent texture-architect: Khởi Tạo Hệ Thống Texture & Shared Material Nền Tảng)
- **Khởi tạo bộ Texture nền tảng Stylized chuẩn lũy thừa 2 (Power-of-Two 512x512)**:
  - Viết thuật toán tạo ảnh chu kỳ tuần hoàn (Periodic Harvester & Worley Toroidal Distance) sinh texture seamless 100% không mối nối tại `.agents/skills/texture-architect/scripts/generate_textures.py`.
  - Bộ Seamless Tileable (`Assets/Textures/Tileable/`):
    * `tex_grass_seamless.png`: Cỏ xanh Stylized `#529934` mềm mại, không kẻ ô.
    * `tex_dirt_seamless.png`: Đất nâu hữu cơ `#8A5C35` rải sỏi nhỏ.
    * `tex_rock_seamless.png`: Vách đá xám phiến nứt rạn Stylized.
    * `tex_wood_seamless.png`: Thớ sợi vân gỗ sồi ấm áp `#A8764A`.
    * `tex_metal_seamless.png`: Mặt kim loại phay xước nhẹ Stylized ánh bạc xám.
  - Bộ Grayscale Masks (`Assets/Textures/Grayscale_Masks/`):
    * `mask_grass_detail.png`, `mask_dirt_detail.png`, `mask_rock_detail.png`, `mask_wood_grain.png`, `mask_metal_surface.png`: Tương phản cao [0.25 - 1.0], sẵn sàng nhân với `albedo_color` trong Godot để tạo vô số biến thể màu mà không tốn dung lượng VRAM.
  - Bộ Palette (`Assets/Textures/Palettes/`):
    * `palette_standard_stylized.png`: 256x64 px gồm 16 dải màu chuẩn (Cỏ, Rừng, Đất, Đất sét, Đá, Núi tím, Gỗ sồi, Gỗ sáng, Thép, Vàng đồng, Da, Vải đỏ, Vải lam, Nước, Mây, Ma thuật).
- **Khởi tạo 11 file vật liệu dùng chung `Assets/Materials_Shared/*.tres` (StandardMaterial3D Godot 4)**:
  - `M_Grass.tres`, `M_Dirt.tres`, `M_Rock.tres`, `M_Wood.tres`, `M_Metal.tres`, `M_Palette_Stylized.tres`.
  - `M_Wood_Fence.tres` (Gỗ rào rustic sẫm màu).
  - `M_Rock_Mountain_Purple.tres` (Đá núi tím viễn cảnh pha từ `mask_rock_detail.png` + `Color(0.72, 0.58, 0.84, 1.0)`).
  - `M_Grass_Dry.tres` (Cỏ úa), `M_Dirt_RedClay.tres` (Đất đỏ), `M_Metal_DarkIron.tres` (Sắt rèn đen).
- **Hoàn thiện tài liệu `Assets/Textures/TEXTURE_CATALOG.md`**:
  - Biên soạn danh mục 3 bảng trực quan với đường dẫn `res://`, độ phân giải, đặc tính và hướng dẫn tái sử dụng bắt buộc.
- **Kiểm định Godot Engine**:
  - Quét nạp Godot 4.7.2 Headless Editor hoàn tất không có lỗi, tự sinh UID chuẩn cho toàn bộ 11 textures và 11 materials.

## Phiên làm việc: 2026-11-06 (Sáng sớm - Sub-agent csharp-coder: Chuẩn Hóa Vật Liệu Player & Áp Dụng Shared Materials Map)
- **Chuẩn hóa vật liệu cho Player (`M_Character_Body.tres`, `M_Character_Face.tres`)**:
  - Tạo `Assets/Materials_Shared/M_Character_Body.tres` (`StandardMaterial3D`, liên kết `character_box_texture.png`, Roughness = 0.60).
  - Tạo `Assets/Materials_Shared/M_Character_Face.tres` (`StandardMaterial3D`, liên kết `character_face.png`, Roughness = 0.60).
  - Bổ sung cả 2 vật liệu vào bảng 3 của `Assets/Textures/TEXTURE_CATALOG.md`.
- **Refactor `Scripts/Core/MapAutoCollision.cs` tải và gán Shared Materials**:
  - Tải trước bộ tài nguyên dùng chung trong `Assets/Materials_Shared/`: `M_Grass.tres`, `M_Dirt.tres`, `M_Rock.tres`, `M_Wood_Fence.tres`, `M_Rock_Mountain_Purple.tres`.
  - Phân loại và gán tự động khi quét mesh:
    * `SM_Tier2_Pavers`, `Terrain_Plains_Mesh` -> gán `M_Grass.tres`.
    * `SM_Dirt_Path_Main`, `SM_Dirt_Path_Tier1` -> gán `M_Dirt.tres`.
    * `SM_Fence_Wood_Overlook` -> gán `M_Wood_Fence.tres`.
    * `SM_Mountains_Background` -> gán `M_Rock_Mountain_Purple.tres`.
    * `SM_Rock_Boulder_*`, `Rock_Mesh_*` -> gán `M_Rock.tres`.
  - Giữ vững toàn vẹn cơ chế tự động xóa phông nền trời `SM_Sky_Backdrop_Plane`, dốc phẳng cho cầu thang qua `StairRampBuilder`, và bật `BackfaceCollision = true` cho Trimesh.
  - Tuân thủ 100% `CODING_STANDARDS.md`: File 168 dòng (< 200 dòng), 11 hàm (mỗi hàm < 15 dòng, đạt chuẩn < 25 dòng), Guard Clauses, giải phóng an toàn biến tham chiếu trong `_ExitTree()`.
- **Mở rộng kịch bản kiểm thử tự động `test_suite.gd`**:
  - Thêm test nạp toàn bộ 13 file `.tres` trong `Assets/Materials_Shared/`.
  - Thêm test tính hợp lệ và thông số của `M_Character_Body.tres` & `M_Character_Face.tres`.
  - Thêm test gán đúng shared materials trên từng loại mesh của bản đồ.
- **Biên dịch & Kiểm định tự động 100%**:
  - `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
  - Chạy Godot Headless `test_suite.gd`: **193 / 193 Test cases Passed (100% Pass, 0 Fail)**.

## Phiên làm việc: 2026-11-06 (Sáng sớm - Sub-agent blender-helper: Áp Dụng Bộ Texture Nền Tảng Mới Vào Map & Xuất GLB)
- **Áp dụng bộ Texture chuẩn vào `map_25d_fixed.blend`**:
  - Bảo tồn tuyệt đối 100% file gốc `map_25d.blend`.
  - Mở `Assets/Blender_Source/map_25d_fixed.blend` bằng Blender 5.4 CLI:
    * Cập nhật `Mat_Grass` -> liên kết texture `tex_grass_seamless.png`.
    * Cập nhật `Mat_Cliff_Dirt` & `Mat_Dirt_Path` -> liên kết texture `tex_dirt_seamless.png`.
    * Cập nhật `Mat_Wood` (`SM_Fence_Wood_Overlook`, biển báo) -> liên kết texture `tex_wood_seamless.png`.
    * Cập nhật `Mat_Stone` (`SM_Rock_Boulder_*`, đá bước, cầu thang) & `Mat_Cliff_Rock` -> liên kết texture `tex_rock_seamless.png`.
  - Bổ sung và chuẩn hóa UV mapping:
    * `SM_Dirt_Path_Main` & `SM_Dirt_Path_Tier1`: Tạo lớp planar `UVMap` chu kỳ 2.0m.
    * `SM_Staircase_01`, `SM_Staircase_02`, `SM_Signpost_Overlook`, `SM_Signpost_Tier1`: Tự động Unwrap Smart UV Project.
    * `SM_Tier2_Pavers` & `SM_Fence_Wood_Overlook`: Đổi tên lớp UV `Float2` thành chuẩn `UVMap`.
  - Đóng gói toàn bộ textures vào file blend và lưu an toàn vào `map_25d_fixed.blend`.
  - Xuất mô hình sang `Assets/Models_Exported/map_25d.glb` (`export_yup=True`, `export_materials='EXPORT'`).
- **Áp dụng bộ Texture chuẩn vào `map_surroundings.blend`**:
  - Mở `Assets/Blender_Source/map_surroundings.blend`:
    * Cập nhật cánh đồng cỏ `Terrain_Plains_Mesh` (`Mat_Grass_Plain`) -> liên kết `tex_grass_seamless.png`.
    * Cập nhật toàn bộ 45 tảng đá `Rock_Mesh_*` (`Mat_Stone`) -> liên kết `tex_rock_seamless.png`.
  - Đóng gói textures vào file blend và lưu an toàn vào `map_surroundings.blend`.
  - Xuất mô hình sang `Assets/Models_Exported/map_surroundings.glb` (`export_yup=True`, `export_materials='EXPORT'`).
- **Re-import vào Godot & Mở rộng bộ kiểm thử tự động**:
  - Chạy Godot Headless import cập nhật toàn bộ tài nguyên cho `.blend` và `.glb`.
  - Bổ sung test case `test_blender_exported_models_and_textures()` vào `test_suite.gd`.
  - Biên dịch `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
  - Godot Headless `test_suite.gd`: **203 / 203 Test cases Passed (100% Pass, 0 Fail)**.

## Phiên làm việc: 2026-11-06 (Sáng - Chuẩn Hóa Toàn Diện Workspace Antigravity CLI & Tự Động Kích Hoạt 5 Kỹ Năng)
- **Chuẩn hóa thư mục kỹ năng theo Antigravity Workspace (`.agents/skills/{skill_name}/SKILL.md`)**:
  - Di chuyển và hoàn thiện 5 kỹ năng chính:
    1. `csharp-coder`: Viết mã C# gameplay Godot 4 (.NET 8), Clean Code, XML tiếng Việt, `[Export]` Inspector, `dotnet build` 0 lỗi 0 cảnh báo.
    2. `code-reviewer`: Rà soát code, kiểm tra giới hạn hàm < 25 dòng, file < 200 dòng, bắt rò rỉ bộ nhớ trong `_ExitTree()`.
    3. `producer`: Quản lý tiến độ `TASKS.md`, `PROJECT_STATE.md`, phân chia việc giữa Human và AI.
    4. `blender-helper`: Hỗ trợ 3D Blender, xuất `.glb` chuẩn Godot, cấm nhúng texture trùng lặp, bảo vệ file `.blend` gốc.
    5. `texture-architect`: Kiến trúc Texture/Material, cây quyết định 3 bước chống phình VRAM, quản lý `TEXTURE_CATALOG.md`.
    (Kèm kỹ năng bổ trợ `checkpoint` để đóng gói trạng thái phiên làm việc).
  - Dọn dẹp thư mục cũ `.gemini/skills/` trong nhánh dự án con.
- **Thiết lập kho tài nguyên dùng chung & Junction thư mục gốc**:
  - Tạo Junction `C:\xnhaugame\Assets` liên kết trực tiếp tới `C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới\Assets`, giúp đường dẫn `Assets/Textures/TEXTURE_CATALOG.md` và `Assets/Materials_Shared/` truy cập thông suốt ở cả thư mục gốc lẫn dự án con.
- **Cấu hình tự động kích hoạt dây chuyền (`AGENTS.md` & `GEMINI.md`)**:
  - Viết lại quy tắc Orchestrator: Tự động phân tích câu lệnh bất kỳ của người dùng và kích hoạt dây chuyền kỹ năng tương ứng (không cần người dùng phải gõ `@tên-skill`).
  - Ép buộc cách ly tiến trình qua Sub-agent (`invoke_subagent` / `run_workflow`) để toàn bộ việc đọc/viết mã dài chạy trong tiến trình con, giải phóng 100% token nháp khi hoàn thành.
  - Cập nhật workflow scripts: `dev_and_review.py`, `asset_and_material_pipeline.py`, `checkpoint_and_reset.py`.
- **Kiểm định chất lượng**:
  - `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
  - Godot Headless `test_suite.gd`: **203 / 203 Test cases Passed (100% Pass, 0 Fail)**.

## Phiên làm việc: 2026-11-08 (Sáng - Tích Hợp Quy Trình Sketch-to-3D Pipeline Vào blender-helper & Workspace Rules)
- **Cập nhật kỹ năng `.agents/skills/blender-helper/SKILL.md`**:
  - Tích hợp quy trình 4 bước chuẩn "Đọc Ảnh Phác Họa Tạo Model 3D (Sketch-to-3D Pipeline)".
  - Quy định thư mục ảnh người dùng tại `modelyeucau/`.
  - Bắt buộc phân tích thị giác bằng công cụ đọc file (`read_file`) để giải mã bố cục 2D (tọa độ X, Z), màu sắc, tỷ lệ kích thước trước khi viết code.
  - Phối hợp `@texture-architect` tra cứu `Assets/Textures/TEXTURE_CATALOG.md` để tái sử dụng hoặc tạo vật liệu phù hợp.
  - Tự động hóa qua Blender CLI (`C:/xnhaugame/blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release/blender.exe --background --python ...`): dựng Mesh 3D, sinh Collision va chạm tự động, xuất file `.glb` vào `Assets/Models/` và gắn vào Scene `.tscn` của Godot 4.
- **Cập nhật quy tắc dự án `AGENTS.md` và `GEMINI.md`**:
  - Bổ sung sơ đồ Mermaid và quy chuẩn chi tiết cho quy trình Sketch-to-3D vào Mục 2.
  - Cập nhật vai trò kỹ năng `@blender-helper` trong Mục 1 và Mục 5.
- **Tạo thư mục chuẩn**: Khởi tạo thư mục đích `Assets/Models/` để tiếp nhận các model xuất từ Blender.









## Phiên làm việc: 2026-11-07 (Tối - Cấu Hình Toàn Diện Workspace Antigravity CLI Theo Chuẩn Local Scope)
- **Thực thi nguyên tắc Strict Local Scope**:
  - Giữ toàn bộ rules, skills, agents, workflows và manifest trong nội bộ workspace `gamexnhau`. Không truy cập hay sửa đổi bất kỳ tài nguyên toàn cục nào (`~/.gemini/`).
- **Nâng cấp và Chuẩn hóa 5 Kỹ Năng Chính + Kỹ Năng Phụ Trợ (`.agents/skills/`)**:
  - `csharp-coder`: Bổ sung mô tả kích hoạt tự nhiên song ngữ (Anh/Việt), chuyển sang đường dẫn tương đối dự án, ràng buộc Clean Code theo `docs/CODING_STANDARDS.md` (< 25 dòng/hàm, < 200 dòng/file, hủy `-=` trong `_ExitTree()`, `dotnet build` 0 lỗi 0 cảnh báo).
  - `code-reviewer`: Rà soát chất lượng code, kiểm định độ dài hàm/file, an toàn bộ nhớ và lệnh biên dịch.
  - `producer`: Quản lý tiến độ, phân chia việc giữa Human và AI, đồng bộ hóa `docs/TASKS.md` và `docs/PROJECT_STATE.md`.
  - `blender-helper`: Tự động tìm `blender.exe` linh hoạt (PATH / Program Files Blender 5.2), cấm nhúng texture trùng lặp vào `.glb`, bảo vệ tuyệt đối `.blend` gốc.
  - `texture-architect`: Cây quyết định 3 bước tối ưu VRAM, chuẩn ảnh lũy thừa 2, quản lý `TEXTURE_CATALOG.md`.
  - `checkpoint`: Tự động quét và đóng gói trạng thái phiên làm việc.
- **Nâng cấp Danh mục Tài nguyên Dùng chung (`Assets/Textures/TEXTURE_CATALOG.md`)**:
  - Bổ sung định dạng (PNG RGBA8, Godot StandardMaterial3D .tres), mục đích sử dụng và hướng dẫn chi tiết cho từng tài nguyên Palettes, Grayscale Masks, Tileable Seamless và Shared Materials.
  - Tích hợp nguyên tắc bắt buộc: `@texture-architect` và `@blender-helper` phải tra cứu catalog trước khi thao tác và cập nhật ngay khi tài nguyên thay đổi.
- **Đồng bộ hóa Quy tắc Workspace (`AGENTS.md` & `GEMINI.md`)**:
  - Thống nhất quy tắc Orchestrator, luồng điều phối tự động theo yêu cầu tự nhiên, và quy chuẩn kỹ thuật cho Sub-agents.
- **Kiểm định chất lượng & Hồi quy**:
  - `dotnet build "Dự án Trò chơi Mới.csproj"`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
  - Godot 4.7.2 Headless `test_suite.gd`: **203 / 203 Test cases Passed (100% Pass, 0 Fail)**.

## Phiên làm việc: 2026-11-08 (Rạng sáng - Triển Khai Hệ Thống Tấn Công Cơ Bản PlayerCombat)
- **Triển khai Hệ thống Tấn công & Hitbox**:
  - Tạo `Scripts/Core/IDamageable.cs` và `Scripts/Core/DummyTarget.cs`.
  - Tạo `Scripts/Player/PlayerCombat.cs` và cập nhật `Scripts/Player/PlayerAnimation.cs`.
  - Bổ sung node `AttackArea` và `PlayerCombat` vào `Scenes/Characters/Player.tscn`.
  - Thêm hành động `attack` vào `project.godot` (Chuột trái / Phím J / Gamepad X).
- **Tuân thủ Clean Code & Memory Safety**:
  - Toàn bộ các file `.cs` đều dưới 170 dòng (< 200 dòng), các hàm < 25 dòng.
  - Hủy đăng ký sự kiện `-=` trong `PlayerCombat._ExitTree()`.
- **Kiểm định chất lượng & Test Suite**:
  - `dotnet build "Dự án Trò chơi Mới.csproj"`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
  - Chạy `test_suite.gd`: **223 / 223 Test cases Passed (100% Pass, 0 Fail)**.

## Phiên làm việc: 2026-11-08 (Sáng - Lập Trình Trọn Gói 4 Phân Hệ Gameplay Bản Đồ Làng Mới)
- **Phân hệ 1: Chuyển Đổi Nội Thất Liền Mạch (Seamless Interior Transition)**:
  - Tạo `Scripts/Core/InteriorZone.cs` (133 dòng): Điều khiển ẩn/hiện mái nhà (`Roof_*`) và tường trước (`Wall_Front_*`), ngắt bật collider, bật đèn ấm nội thất `OmniLight3D`, kích hoạt zoom cận cảnh camera.
  - Nâng cấp `Scripts/Core/CameraFollow.cs` (181 dòng): Bổ sung `SetInteriorFocus` và `ResetInteriorFocus` lerp mượt mà không gián đoạn gameplay.
- **Phân hệ 2: Hệ Thống AI NPC & Tương Tác Chuyên Biệt 8 Dân Làng**:
  - Tạo `Scripts/NPC/NpcProfession.cs` (54 dòng), `Scripts/NPC/NpcState.cs` (12 dòng).
  - Tạo `Scripts/NPC/NpcSpecialActionManager.cs` (101 dòng): Cung cấp bộ tùy chọn đặc biệt cho 8 nghề (Thợ Rèn, Giả Kim, Đầu Bếp, Nông Dân, Ngư Dân, Thợ Mỏ, Tiều Phu, Lính Canh).
  - Tạo `Scripts/NPC/NpcBehavior.cs` (179 dòng): AI State Machine (Idle, Working, Patrolling, Interacting), chuyển động nhấp nhô thủ tục (procedural working), tuần tra waypoint, xoay mặt nhìn Player khi tương tác.
  - Tạo `Scripts/UI/NpcInteractionDialog.cs` (139 dòng) & `Scenes/UI/NpcInteractionDialog.tscn`: Giao diện Popup Dialog chuyên nghiệp, tự động sinh nút bấm theo nghề, mở khóa chuột và đóng sạch sẽ.
  - Tạo `Scenes/Characters/VillageNpc.tscn`: Scene mẫu dân làng gồm `CharacterBody3D`, `CollisionShape3D`, `VisualModel`, `InteractableArea`, `OverheadLabel` billboard.
- **Phân hệ 3: Cài Đặt Hiển Thị & Khung Hình (DisplaySettingsManager)**:
  - Tạo `Scripts/Core/DisplaySettingsManager.cs` (118 dòng): Singleton quản lý độ phân giải (720p đến 4K), chế độ màn hình (Windowed, Borderless, Fullscreen), Target FPS (30 - Unlimited), VSync, lưu bền vững vào `user://settings.cfg`.
- **Phân hệ 4: Mở Rộng Bảng Điều Khiển Dev Mode HUD (6 Tab Toàn Năng)**:
  - Tạo `Scripts/UI/DevTeleportTab.cs` (71 dòng): Dịch chuyển nhanh tới 8 phân khu và 4 nội thất phòng.
  - Tạo `Scripts/UI/DevNpcSystemTab.cs` (144 dòng): Giám sát 8 NPC, triệu hồi NPC, dịch chuyển đến NPC, ép đổi trạng thái AI.
  - Tạo `Scripts/UI/DevGraphicsTab.cs` (174 dòng): Tinh chỉnh đồ họa, độ phân giải, FPS, VSync ngay trong HUD kèm nút lưu.
  - Cập nhật `Scripts/UI/DevOverlay.cs` (152 dòng) và `Scenes/UI/DevOverlay.tscn`: Đồng bộ 6 tabs mượt mà với chuột và Gamepad (LB/RB).
- **Phân hệ 5: Scene Bản Đồ Làng Hoàn Chỉnh & Kiểm Thử Toàn Diện**:
  - Tạo `Scenes/Levels/VillageMap.tscn`: Tích hợp toàn diện `village_map.glb`, `Player`, `IsometricCamera`, 4 `InteriorZone`, 8 NPC dân làng, `DisplaySettingsManager`, `VoidKillZone`, `DevOverlay`, `NpcInteractionDialog`.
  - Khắc phục lỗi disconnect trong `DevNpcTab.cs` khi `_npc == null`.
  - **Chuẩn Clean Code**: 100% file C# < 200 dòng, method < 25 dòng, Guard Clauses, hủy `-=` trong `_ExitTree()`.
  - **Biên dịch C#**: `dotnet build` $\rightarrow$ **Build succeeded. 0 Warning(s), 0 Error(s)**.
  - **Godot Headless verification**: `test_suite.gd` $\rightarrow$ **279 / 279 Test cases Passed (100% Pass, 0 Fail)**.

## Phiên làm việc: 2026-11-08 (Trưa - Tinh Chỉnh Điểm Spawn Giao Lộ 2 Map & Triệt Tiêu Lỗi Scene Editor)
- **Cập nhật tọa độ Spawn Player tại Giao Lộ 2 Map (`WorldMap.tscn`)**:
  - Chuyển vị trí spawn của Player sang `(3.8, 0.5, 4.0)` ngay chân bậc thang Đảo Đá (`SM_Staircase_01`) và trên con đường mòn đất `Path_Connector_Island` dẫn thẳng vào Cổng Làng (`Z=8.5`).
  - Cập nhật vị trí `IsometricCamera` về `(-24.2, 23.5, 32.0)` để người chơi vừa bấm F5 là thấy ngay cả 2 Map liền kề: Bậc thang Đảo Đá hùng vĩ sau lưng và toàn cảnh Cổng Làng, vườn rau, sạp chợ, NPC phía trước trong 1 góc nhìn thông thoáng duy nhất.
- **Đồng bộ hóa Scenes (`VillageMap.tscn` và `Village/VillageMap.tscn`)**:
  - Khởi tạo `Scenes/Levels/VillageMap.tscn` và `Scenes/Levels/Village/VillageMap.tscn` mang toàn bộ cấu trúc hợp nhất từ `WorldMap.tscn`.
  - Triệt tiêu triệt để hiện tượng Godot Editor mở tab cũ bị khối trắng che khuất màn hình.
- **Cập nhật `VoidKillZone.cs`**:
  - Thiết lập `DefaultSpawnPosition = new Vector3(3.8f, 0.5f, 4.0f)`.
- **Kiểm định chất lượng toàn diện**:
  - `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
  - Chạy `test_suite.gd` trên Godot Mono Console (Windowed rendering): **372 / 372 Test cases PASSED (100% Pass, 0 Error)**.
  - Mắt thần tự soi 4 ảnh thực tế: 100% đạt chuẩn thẩm mỹ cao.

