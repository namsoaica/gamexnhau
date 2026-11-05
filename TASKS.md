# BẢNG PHÂN CHIA CÔNG VIỆC (TASKS TRACKER)

## 📌 Đã Hoàn Thành (Done)
- [x] **[HUMAN]** Dựng model nhân vật `character_25d.blend` và xuất sang `character_25d.glb`.
- [x] **[HUMAN]** Dựng bản đồ thế giới `map_25d.blend` và xuất sang `map_25d.glb`.
- [x] **[AI - csharp-coder]** Viết `PlayerMovement.cs` (điều khiển vận tốc, gia tốc, nhảy, xoay mặt theo góc camera Isometric).
- [x] **[AI - csharp-coder]** Viết `PlayerAnimation.cs` (tự động phát hoạt ảnh `Idle`, `Walk`, `Jump`).
- [x] **[AI - csharp-coder]** Viết `MapAutoCollision.cs` (tự động tạo va chạm cho địa hình và cầu thang Blender).
- [x] **[AI - csharp-coder]** Viết `CameraFollow.cs` (camera trượt mượt mà theo nhân vật chuẩn góc Isometric).
- [x] **[AI - csharp-coder]** Tạo Scene hoàn chỉnh `Player.tscn` và `WorldMap.tscn`, đồng bộ mã UID và cấu hình Main Scene.
- [x] **[AI - blender-helper]** Mở rộng thế giới 2.5D (84m x 84m): Cánh đồng, 4 dãy núi ranh giới, 45 tảng đá, 70 cây phong/thông, 90 bụi cỏ/hoa cúc (`map_surroundings.glb`).
- [x] **[AI - code-reviewer]** Rà soát toàn diện dự án: 100% Clean Code, Guard Clauses, XML tiếng Việt, kiểm tra rò rỉ bộ nhớ, build 0 lỗi 0 cảnh báo.
- [x] **[AI - producer]** Chuẩn hóa Git & Môi trường cộng tác: Cập nhật `.gitignore`, `.gitattributes`, `.editorconfig` (Allman style, LF/CRLF, binary 3D).
- [x] **[AI - producer]** Dọn dẹp kho Git: Xóa file thừa/lỗi font `1.gitinore.txt`, untrack và dọn các file backup `*.blend1`.
- [x] **[AI - producer]** Thiết lập tài liệu `README.md` chuyên nghiệp tại thư mục gốc và tạo hardlink đồng bộ sang dự án Godot.
- [x] **[AI - producer]** Xây dựng tài liệu `docs/CONTRIBUTING.md` hướng dẫn quy trình cộng tác, branching strategy, PR template và giải quyết xung đột Scene Godot.
- [x] **[AI - producer]** Nâng cấp mục 4 "Quy Trình Cộng Tác Nhóm" trong `README.md`: Hướng dẫn phân quyền cho Trưởng nhóm (Collaborators, bảo vệ nhánh `main`), quy trình thực hành 7 bước kèm khối lệnh bash cho thành viên, và sơ đồ Mermaid trực quan.
- [x] **[HUMAN - AiichaN]** Đóng góp hệ thống tương tác NPC (`IInteractable`, `InteractableArea`, `SimpleNpc`), chống rơi vực (`VoidKillZone`), bộ dò tương tác (`PlayerInteractor`), Coyote Time, Jump Buffer, Anti-moonwalk, Procedural Animation, kịch bản test `test_suite.gd`.
- [x] **[AI - code-reviewer]** Rà soát chất lượng mã nguồn nhánh `origin/dev`: phát hiện và sửa triệt để 3 nguy cơ rò rỉ bộ nhớ (memory leaks) trong `_ExitTree()`.
- [x] **[AI - code-reviewer]** Sáp nhập (Merge) nhánh `origin/dev` vào `main`, giải quyết xung đột `WorldMap.tscn`, `.gitignore`, `PlayerAnimation.cs`, bảo tồn trọn vẹn mở rộng `Map_Surroundings`.
- [x] **[AI - code-reviewer]** Chạy kiểm thử tự động Godot Headless `test_suite.gd` (32/32 tests Pass) và biên dịch `dotnet build` đạt 0 Warning 0 Error.
- [x] **[AI - blender-helper]** Cải tạo bản đồ 3D: chỉ giữ lại 1 dãy núi phía Bắc hùng vĩ, xóa 3 dãy núi che tầm nhìn, đổi màu xanh cỏ cho nền gạch và làm phẳng kết nối đảo trung tâm.
- [x] **[AI - code-reviewer]** Rà soát toàn bộ 9 file C# trong `Scripts/`: 100% hàm <= 19 dòng (< 25 dòng), file < 195 dòng (< 200 dòng), Guard Clauses, XML tiếng Việt, an toàn bộ nhớ trong `_ExitTree()`.
- [x] **[AI - code-reviewer]** Kiểm định tự động chất lượng cao: Biên dịch `dotnet build` đạt 0 Warning 0 Error và chạy Godot Headless `test_suite.gd` đạt 53/53 test cases Passed (100%).
- [x] **[AI - blender-helper]** Cải tạo mô hình 3D bản đồ: Gán vật liệu Mat_Grass kèm texture tex_grass_grid.png và UV phẳng cho SM_Tier2_Pavers, mở rộng mép tiếp giáp về Y=6.99m đóng kín khe hở bậc thềm 3.6cm, extrude độ dày 0.42m thành khối 3D đặc chống xuyên vật lý, xuất map_25d.glb và lưu an toàn map_25d_fixed.blend. (Test suite: 66/66 Pass).
- [x] **[AI - csharp-coder]** Bổ sung tính năng Zoom Camera bằng con lăn chuột (`CameraFollow.cs`), đưa NPC xuống mặt đất và hoàn thiện hội thoại (`SimpleNpc.cs`, `WorldMap.tscn`).
- [x] **[AI - csharp-coder]** Xây dựng Chế Độ Dev (Dev Mode / Debug Overlay HUD - `DevOverlay.cs`, `DevPlayerTab.cs`, `DevNpcTab.cs`): phím tắt `F1`/`~`/`F3`, tinh chỉnh `MoveSpeed`, `JumpVelocity`, `Gravity`, `InfiniteJump`, dịch chuyển tức thời `TeleportTo`, Live Dialogue Editor sửa câu thoại NPC trực tiếp khi chơi, slider zoom camera, hiển thị FPS & tọa độ Player theo thời gian thực. (Build 0 lỗi 0 cảnh báo, 66/66 test cases Pass).
- [x] **[AI - csharp-coder]** Tái thiết ánh sáng môi trường (ACES Tonemap, ProceduralSky dịu mát, SSAO, bóng đổ PSSM) và xây dựng hệ thống dốc va chạm phẳng `StairRampBuilder` (`ConvexPolygonShape3D`) + `FloorMaxAngle >= 58°` giúp leo cầu thang trơn tru. (Build 0 lỗi 0 cảnh báo, 91/91 test cases Pass).
- [x] **[AI - blender-helper]** Khắc phục lỗi đất xung quanh trắng xóa: Gán vật liệu cỏ xanh `Mat_Grass_Plain` (#529934) kèm texture `tex_grass_grid.png` đóng gói và UV mapping planar projection `(x/4, y/4)` cho `Terrain_Plains_Mesh` trong `map_surroundings.blend`, xuất `map_surroundings.glb`; đo đạc chính xác AABB, bước bậc và độ dốc (51.11° & 57.12°) của 2 cầu thang `SM_Staircase_01` & `SM_Staircase_02` trong `map_25d_fixed.blend`. (Build 0 lỗi 0 cảnh báo, 91/91 test cases Pass).
- [x] **[AI - blender-helper]** Loại bỏ phông nền trắng khổng lồ: Xóa object `SM_Sky_Backdrop_Plane` và vật liệu `Mat_Sky_Gradient` khỏi `map_25d_fixed.blend`, xuất `map_25d.glb` chuẩn Godot, bảo tồn nguyên vẹn 100% file gốc `map_25d.blend` và các thành phần khác, giải phóng tầm nhìn thông thoáng cho bầu trời Procedural Sky. (Build 0 lỗi 0 cảnh báo, 92/92 test cases Pass).
- [x] **[AI - blender-helper]** Mở rộng đài cao tầng 2 gấp 6.8x diện tích (**2.60m x 2.41m**), khép kín 0 gap với đỉnh thang `SM_Staircase_02`, tái thiết hàng rào gỗ 9 cột quanh 3 mặt Tây-Bắc-Đông chừa lối vào thang rộng 1.24m; tạo texture cỏ mịn tự nhiên không vết kẻ ô vuông `tex_grass_clean.png` (#529934) đồng bộ toàn bản đồ; xóa bỏ 5 chóp núi nón tím chen chúc chắn tầm nhìn đài cao, giải phóng bầu trời thoáng đãng. (Build 0 lỗi 0 cảnh báo, 128/128 test cases Pass).
- [x] **[AI - csharp-coder]** Triển khai Chế Độ Camera Tự Do (Free Cam 6-DOF - `FreeCameraController.cs`, `CameraFollow.cs`, `DevWorldTab.cs`), tích hợp cơ chế Freeze Player khóa nhân vật đứng im hoàn toàn khi đang bay Free Cam, tích hợp tay cầm Gamepad toàn diện cho gameplay và Dev HUD. (Build 0 lỗi 0 cảnh báo, 131/131 test cases Pass).
- [x] **[AI - producer]** Viết lại toàn diện tài liệu `README.md` chuyên nghiệp, trực quan, cập nhật đầy đủ bảng điều khiển Controls Matrix (Bàn phím & Chuột vs. Gamepad), Dev Mode HUD toàn năng, đài vọng cảnh tầng 2 (6.27 m²), thảm cỏ tự nhiên không ô vuông (#529934), bậc thang leo êm ái, cơ chế Freeze Player, và đồng bộ cả 2 thư mục dự án.

---

## 🎯 Việc Cần Làm Tiếp Theo (Backlog / Next Steps)

### Phân Nhóm 1: Gameplay & Lập Trình (AI / Developer)
- [ ] **[AI - csharp-coder]** Lập trình hệ thống đòn đánh / tấn công cơ bản (`PlayerCombat.cs`) sử dụng animation `Attack` có sẵn trong model `character_25d.glb`.
- [ ] **[AI - csharp-coder]** Lập trình thanh máu, thể lực hoặc giao diện UI cơ bản (`Scripts/UI/`).
- [ ] **[AI - csharp-coder]** Lập trình AI cho quái vật tuần tra và tấn công (`Scripts/Enemies/`).
- [ ] **[AI - code-reviewer]** Rà soát Clean Code và kiểm tra build `dotnet build` sau mỗi tính năng mới.

### Phân Nhóm 2: Đồ Họa, Âm Thanh & Cấp Độ (Human / 3D Artist)
- [ ] **[HUMAN]** Dựng model quái vật / kẻ địch mới trong Blender (ví dụ: Slime, Goblin) và xuất sang `Assets/Models_Exported/`.
- [ ] **[HUMAN]** Thiết kế thêm chướng ngại vật / rương báu / cổng dịch chuyển vào map trong Blender.
- [ ] **[HUMAN]** Tìm kiếm hoặc thiết kế âm thanh hiệu ứng (SFX bước chân, SFX chém, BGM nền) đưa vào `Assets/Audio/`.
- [ ] **[HUMAN]** Tinh chỉnh góc camera hoặc ánh sáng DirectionalLight trong Inspector Godot theo sở thích thẩm mỹ.
