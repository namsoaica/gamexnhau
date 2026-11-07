# KẾ HOẠCH & TIẾN ĐỘ DỰ ÁN (PROJECT TASKS)

Tài liệu này quản lý toàn bộ các đầu việc trong dự án, phân định rõ ràng giữa phần việc của **Người dùng (Human)** và các **Sub-agent AI**.

---

## 📋 Trạng Thái Tiến Độ Hiện Tại

- [x] **[AI - csharp-coder]** Khởi tạo nhân vật Player 2.5D dạng khối hộp (`CharacterBody3D`) với chuyển động 8 hướng mượt mà, quán tính gia tốc / giảm tốc, nhảy và trọng lực (`PlayerMovement.cs`).
- [x] **[AI - csharp-coder]** Hoạt họa nhân vật Player bằng `AnimationPlayer` và `Sprite3D` (Idle, Walk, Jump, Fall) xoay hướng theo chiều di chuyển (`PlayerAnimation.cs`).
- [x] **[AI - csharp-coder]** Camera Isometric 2.5D bám theo Player mượt mà qua hàm `Lerp`, có góc nghiêng chuẩn 45° và độ trễ êm ái (`CameraFollow.cs`).
- [x] **[AI - csharp-coder]** Xây dựng hệ thống NPC tương tác (`IInteractable`, `InteractableArea.cs`, `SimpleNpc.cs`), phạm vi kích hoạt tương tác khi Player đến gần và nhấn phím tương tác.
- [x] **[AI - csharp-coder]** Hiển thị bóng thoại / nhãn 3D billboard trên đầu NPC với nội dung hội thoại, tự động xoay theo camera và biến mất sau khoảng thời gian cấu hình.
- [x] **[AI - csharp-coder]** Hệ thống Dev Mode HUD toàn năng (`F1`, phím `~` hoặc phím `Select` trên Gamepad):
  - Tab 1: **Nhân vật (Player Tweaks)** - Tinh chỉnh trực tiếp tốc độ, lực nhảy, trọng lực, gia tốc, tự động hồi sinh.
  - Tab 2: **Hội thoại (Dialogue Editor)** - Chỉnh sửa lời thoại NPC trực tiếp khi đang chạy game, thêm câu thoại mới, phát thử câu thoại.
  - Tab 3: **Thế giới & Camera (World & Camera)** - Chuyển đổi qua lại giữa camera Isometric và **Camera Tự Do 6-DOF (Free Cam)**, đóng băng chuyển động nhân vật (**Freeze Player**), tinh chỉnh trường nhìn (FOV), tốc độ bay, bật/tắt lưới tọa độ.
- [x] **[AI - csharp-coder]** Tự động phát hiện và gán va chạm địa hình (`MapAutoCollision.cs`), sinh `CollisionShape3D` dạng Trimesh cho toàn bộ bề mặt di chuyển trong Scene `WorldMap.tscn`.
- [x] **[AI - csharp-coder]** Khắc phục triệt để hiện tượng Player bị kẹt / cản trở tại các mép bậc thang vuông góc 90° bằng script `StairRampBuilder.cs`, tự động dựng dốc nghiêng ConvexPolygonShape3D vô hình phủ trên các bậc thang.
- [x] **[AI - csharp-coder]** Vực sâu tự cứu sinh (`VoidKillZone.cs`): Tự động phát hiện khi Player rơi khỏi đảo lơ lửng xuống dưới độ cao an toàn, triệt tiêu gia tốc rơi và đưa Player trở lại điểm xuất phát an toàn.
- [x] **[AI - code-reviewer]** Rà soát toàn bộ codebase theo chuẩn Clean Code: Mỗi hàm dưới 25 dòng, mỗi file dưới 200 dòng, XML comment tiếng Việt, biến `[Export]` tường minh, bảo đảm biên dịch `dotnet build` 0 lỗi 0 cảnh báo.
- [x] **[AI - blender-helper]** Loại bỏ phông nền trắng khổng lồ: Xóa object `SM_Sky_Backdrop_Plane` và vật liệu `Mat_Sky_Gradient` khỏi `map_25d_fixed.blend`, xuất `map_25d.glb` chuẩn Godot, bảo tồn nguyên vẹn 100% file gốc `map_25d.blend` và các thành phần khác, giải phóng tầm nhìn thông thoáng cho bầu trời Procedural Sky. (Build 0 lỗi 0 cảnh báo, 92/92 test cases Pass).
- [x] **[AI - blender-helper]** Mở rộng đài cao tầng 2 gấp 6.8x diện tích (**2.60m x 2.41m**), khép kín 0 gap với đỉnh thang `SM_Staircase_02`, tái thiết hàng rào gỗ 9 cột quanh 3 mặt Tây-Bắc-Đông chừa lối vào thang rộng 1.24m; tạo texture cỏ mịn tự nhiên không vết kẻ ô vuông `tex_grass_clean.png` (#529934) đồng bộ toàn bản đồ; xóa bỏ 5 chóp núi nón tím chen chúc chắn tầm nhìn đài cao, giải phóng bầu trời thoáng đãng. (Build 0 lỗi 0 cảnh báo, 128/128 test cases Pass).
- [x] **[AI - csharp-coder]** Triển khai Chế Độ Camera Tự Do (Free Cam 6-DOF - `FreeCameraController.cs`, `CameraFollow.cs`, `DevWorldTab.cs`), tích hợp cơ chế Freeze Player khóa nhân vật đứng im hoàn toàn khi đang bay Free Cam, tích hợp tay cầm Gamepad toàn diện cho gameplay và Dev HUD. (Build 0 lỗi 0 cảnh báo, 131/131 test cases Pass).
- [x] **[AI - producer]** Viết lại toàn diện tài liệu `README.md` chuyên nghiệp, trực quan, cập nhật đầy đủ bảng điều khiển Controls Matrix (Bàn phím & Chuột vs. Gamepad), Dev Mode HUD toàn năng, đài vọng cảnh tầng 2 (6.27 m²), thảm cỏ tự nhiên không ô vuông (#529934), bậc thang leo êm ái, cơ chế Freeze Player, và đồng bộ cả 2 thư mục dự án.
- [x] **[AI - texture-architect]** Khởi tạo hệ thống Texture & Material dùng chung nền tảng (`Assets/Textures/`, `Assets/Materials_Shared/`, `TEXTURE_CATALOG.md`), tối ưu VRAM và chống phân mảnh tài nguyên.
- [x] **[AI - csharp-coder]** Chuẩn hóa vật liệu Player (`M_Character_Body.tres`, `M_Character_Face.tres`), refactor `MapAutoCollision.cs` tải và gán trực tiếp shared materials cho toàn bộ mesh địa hình/đường đất/rào gỗ/núi tím/đá tảng trên Map, mở rộng `test_suite.gd` đạt 193/193 test cases Passed (100%).
- [x] **[AI - blender-helper]** Áp dụng bộ texture nền tảng mới vào Map trong Blender (cỏ `tex_grass_seamless.png`, đất `tex_dirt_seamless.png`, gỗ `tex_wood_seamless.png`, đá `tex_rock_seamless.png`), sinh planar UV cho đường đất và smart UV cho cầu thang/biển báo, đóng gói vào `map_25d_fixed.blend` và `map_surroundings.blend`, xuất `map_25d.glb` và `map_surroundings.glb` chuẩn Godot, mở rộng `test_suite.gd` đạt 203/203 tests Pass (100%).
- [x] **[AI - agy-customizations & producer]** Hoàn thiện cấu hình Workspace Antigravity CLI theo chuẩn Local Scope: Nâng cấp 5 kỹ năng chính (`.agents/skills/{skill_name}/SKILL.md`) và checkpoint với natural-language triggers song ngữ, làm phong phú `Assets/Textures/TEXTURE_CATALOG.md` với định dạng/mục đích/hướng dẫn tái sử dụng, cập nhật `AGENTS.md` và `GEMINI.md`, loại bỏ đường dẫn tuyệt đối, xác thực `dotnet build` 0 lỗi 0 cảnh báo và 203/203 test cases Passed.
- [x] **[AI - csharp-coder]** Triển khai Hệ Thống Tấn Công Cơ Bản (`PlayerCombat.cs`, `IDamageable.cs`, `DummyTarget.cs`): Kích hoạt hoạt ảnh `Attack` từ `character_25d.glb`, cấu hình phím tấn công (Chuột trái, Phím J, Gamepad X), hitbox `AttackArea` quét đa mục tiêu, hủy sự kiện `-=` trong `_ExitTree()`, mở rộng `test_suite.gd` đạt 223/223 test cases Passed (100%).
- [x] **[AI - agy-customizations & blender-helper]** Thiết lập quy trình "Đọc Ảnh Phác Họa Tạo Model 3D (Sketch-to-3D Pipeline)" trong `.agents/skills/blender-helper/SKILL.md`, `AGENTS.md` và `GEMINI.md`: đọc ảnh từ `modelyeucau/`, phân tích thị giác 2D (tọa độ X, Z, tỷ lệ, màu sắc), phối hợp `@texture-architect` tra cứu `Assets/Textures/TEXTURE_CATALOG.md`, viết script Python `bpy` gọi Blender CLI dựng Mesh và Collision tự động, xuất `.glb` vào `Assets/Models/` và gắn vào scene `.tscn` của Godot 4.
- [x] **[AI - texture-architect]** Chuẩn bị texture bạt sọc đỏ-trắng `tex_canopy_striped.png` (Tileable 128x128) và 5 vật liệu `StandardMaterial3D` dùng chung Godot 4: `M_Roof_Tiles_Red.tres`, `M_Roof_Tiles_Teal.tres`, `M_Canopy_Striped.tres`, `M_Mystic_Cyan.tres` (Emission x2.0), `M_Lava_Fire.tres` (Emission x2.5), đăng ký đầy đủ vào `Assets/Textures/TEXTURE_CATALOG.md`.
- [x] **[AI - blender-helper]** Hiện thực hóa Bản Đồ Làng Mở Rộng và Nội Thất từ ảnh concept `modelyeucau/map2/1.jpg`: Soạn thảo `Assets/Blender_Source/build_village_map.py`, dựng mô hình 3D Stylized Low-Poly Isometric quy mô 48m x 48m gồm 6 phân khu (Lâm Nghiệp, Nhà Rèn, Chợ Trung Tâm, Nhà Giả Kim, Mỏ Đá, Cổng Làng & Vườn Rau) và nội thất 4 phòng (Nhà Rèn, Giả Kim, Quán Ăn, Nhà Dân); tách riêng `Roof_*` và `Wall_Front_*` cho cơ chế Seamless Interior Transition; tự động tạo 117 mesh va chạm `-col`; xuất ra `Assets/Models/village_map.glb` (884 KB) và lưu an toàn `Assets/Blender_Source/village_map.blend`.
- [x] **[AI - csharp-coder & code-reviewer]** Lập trình trọn gói 4 phân hệ gameplay cho Bản Đồ Làng Mới:
  - Phân hệ 1: Chuyển đổi nội thất liền mạch (`InteriorZone.cs`, `CameraFollow.cs` mở rộng `SetInteriorFocus`).
  - Phân hệ 2: Hệ thống hành vi AI NPC và tương tác chuyên biệt 8 dân làng (`NpcProfession.cs`, `NpcState.cs`, `NpcSpecialActionManager.cs`, `NpcBehavior.cs`, `NpcInteractionDialog.cs`, `VillageNpc.tscn`, `NpcInteractionDialog.tscn`).
  - Phân hệ 3: Cài đặt hiển thị và tối ưu hóa khung hình đa cấu hình (`DisplaySettingsManager.cs` lưu `user://settings.cfg`).
  - Phân hệ 4: Mở rộng Dev Mode HUD (`DevTeleportTab.cs`, `DevNpcSystemTab.cs`, `DevGraphicsTab.cs`, `DevOverlay.cs`, `DevOverlay.tscn`).
- [x] **[AI - blender-helper & csharp-coder]** Hợp nhất 2 Map liền nhau hoàn toàn trong `WorldMap.tscn` (Seamless Connected World):
  - Khắc phục triệt để lỗi đảo trục tọa độ Blender Y-Z trong `build_village_map.py`: Chuyển đổi chính xác 100% tọa độ Godot sang Blender, đưa mô hình làng nằm phẳng hoàn toàn trên mặt cỏ cánh đồng, nối thẳng con đường đất từ chân dốc Đảo Đá (`Z=0.2`) qua Cổng Làng (`Z=8.5`) tới Chợ Trung Tâm (`Z=17.0`) và các phân khu.
  - Xóa bỏ scene rời `VillageMap.tscn`, quy về 1 màn chơi duy nhất `WorldMap.tscn`.
  - Cập nhật vị trí 4 vùng nội thất `InteriorZone_*` (Smith, Alchemist, Chef, House) và 8 dân làng `Village_NPCs` khớp với bản đồ thực.
  - Cập nhật tọa độ dịch chuyển trong `DevTeleportTab.cs`.
  - Bổ sung va chạm tự động cho tường, giếng, đe sắt, lò luyện trong `MapAutoCollision.cs`.
  - Xác thực `dotnet build` 0 lỗi 0 cảnh báo, Godot Headless `test_suite.gd` đạt 279/279 test cases Passed (100%).
- [x] **[AI - agy-customizations & code-reviewer]** Thiết lập "Cơ Chế Kiểm Thử Nghiệm Thu Thực Tế Đến Khi Đạt Yêu Cầu (Requirement-Driven Auto-Playtest Loop)" với 4 quy tắc bắt buộc:
  - (1) Cấm kết thúc nhiệm vụ khi mới chỉ chạy `dotnet build` thành công.
  - (2) Chuyển hóa 100% yêu cầu người dùng thành Automated Playtest Assertions trong `test_suite.gd` (giả lập bước vào/ra nhà Seamless Interior Transition, kiểm tra va chạm toàn bộ mesh chống xuyên tường, giả lập tương tác 8 NPC và hội thoại tiếng Việt, kiểm tra Dev HUD 6 Tabs và dịch chuyển tức thời, kiểm tra thay đổi đa độ phân giải và FPS trần).
  - (3) Tự động gọi Godot Headless Mono Console tại `C:/xnhaugame/Godot_v4.7.2-stable_mono_win64/Godot_v4.7.2-stable_mono_win64/Godot_v4.7.2-stable_mono_win64_console.exe` và đọc toàn bộ log.
  - (4) Thiết lập vòng lặp tự chữa lỗi (Self-Healing Loop) phân tích log, sửa code/scene và chạy lại liên tục đến khi 100% Pass tuyệt đối.
  - Đã nâng cấp đồng bộ: `.agents/skills/code-reviewer/SKILL.md`, `AGENTS.md`, `GEMINI.md`, `.agents/workflows/dev_and_review.py`, và `test_suite.gd` đạt **368 / 368 tests Passed (100%)**.
- [x] **[AI - agy-customizations & blender-helper]** Nâng cấp toàn diện kỹ năng Blender với 4 quy tắc bắt buộc nhằm khắc phục triệt để tình trạng dựng model lúc đẹp lúc xấu:
  - (1) CẤM DỰNG KHỐI THÔ SƠ (No Raw Primitives): Dùng bmesh (Extrude, Inset, Bevel, Subdivide, Displace) kết hợp Modifiers (Bevel 2-3 segments bo viền bắt sáng, Solidify, Shade Auto Smooth).
  - (2) XÂY DỰNG THƯ VIỆN PROCEDURAL CHUẨN (`tools/blender_kit.py`): Xây dựng thư viện chứa các hàm dựng sẵn chất lượng cao có tham số hóa (nhà tường-mái-hiên, cây tán tầng hữu cơ, đá vát cạnh ngẫu hóa, đường đất) và tự động căn chỉnh AABB (`snap_to_ground`, `stack_on_top`) chống bay lơ lửng / đâm xuyên.
  - (3) CƠ CHẾ MẮT THẦN TỰ KIỂM TRA (Visual Self-Correction Loop): Tự động render ảnh góc nhìn Isometric với Sun Light xuất ra `Assets/Models/_preview_render.png`, AI dùng công cụ đọc ảnh đối chiếu trực tiếp với concept `modelyeucau/`.
  - (4) VÒNG LẶP CHẤT LƯỢNG: Tự sửa script bpy và render kiểm tra liên tục đến khi mô hình sắc nét, cân đối mới đưa vào Scene Godot.
  - Đã refactor toàn bộ `Assets/Blender_Source/build_village_map.py` theo `tools/blender_kit.py`, xuất lại `Assets/Models/village_map.glb`, lưu `Assets/Blender_Source/village_map.blend`, render kiểm tra trực quan thành công và xác thực 368/368 test cases Pass trên Godot Headless.
- [x] **[AI - agy-customizations & code-reviewer]** Nâng cấp toàn diện cơ chế "Kiểm Thử Thị Giác Thực Tế (Visual Playtest & Screenshot Inspection Loop)", xóa bỏ triệt để tình trạng kiểm thử mù trong bóng tối (`--headless`):
  - (1) Bắt buộc chạy dựng hình thực tế (Windowed rendering) qua Godot Mono Console: Tự động điều khiển nhân vật trải nghiệm các tính năng và chụp 4 bức ảnh màn hình thực tế lưu vào `docs/test_screenshots/` (`1_map_overview.png`, `2_interior_view.png`, `3_npc_ui.png`, `4_devtools_ui.png`).
  - (2) AI BẮT BUỘC dùng công cụ đọc ảnh (Vision) mở từng bức ảnh lên tự kiểm tra bằng mắt (ánh sáng/màu sắc, góc nhìn nội thất không bị che khuất, tiếp xúc mặt đất của nhân vật, bố cục giao diện UI).
  - (3) Phát hiện và loại bỏ triệt để 65 đạo cụ xung quanh (`Map_Surroundings`) mọc xuyên vào làng/nhà dân qua `MaterialCatalogHelper.cs` và `MapAutoCollision.cs`; cấu hình `InteriorZone` ẩn tường South/West cho góc nhìn diorama thông thoáng; điều chỉnh vị trí cây cối bao quanh.
  - (4) Đạt chuẩn 100% cả về logic lẫn hình ảnh: **372 / 372 Test cases PASSED (100% Pass, 0 Error)** và 4/4 ảnh chụp màn hình đạt chuẩn thẩm mỹ cao.
  - Đã cập nhật đồng bộ: `.agents/skills/code-reviewer/SKILL.md`, `AGENTS.md`, `GEMINI.md`, `.agents/workflows/dev_and_review.py`, `test_suite.gd`, và `WorldMap.tscn`.
- [x] **[AI - csharp-coder & producer]** Giải quyết triệt để 2 vấn đề hiển thị trực quan và đồng bộ Scene Editor:
  - (1) Cập nhật vị trí spawn Player trong `WorldMap.tscn` tại giao lộ đắc địa `(3.8, 0.5, 4.0)` ngay chân bậc thang Đảo Đá (`SM_Staircase_01`) và trên con đường mòn đất `Path_Connector_Island` nối thẳng Cổng Làng (`Z=8.5`). Khi vào game (F5), thấy ngay bậc thang đảo đá phía sau và toàn cảnh làng, cổng làng, vườn rau, 8 NPC phía trước trong 1 góc nhìn thông thoáng duy nhất.
  - (2) Khởi tạo đồng bộ `Scenes/Levels/VillageMap.tscn` và `Scenes/Levels/Village/VillageMap.tscn` chứa toàn bộ cấu trúc hợp nhất từ `WorldMap.tscn`, triệt tiêu hoàn toàn khối trắng chắn màn hình khi người dùng mở tab scene trong Godot Editor.
  - (3) Cập nhật `DefaultSpawnPosition` trong `VoidKillZone.cs` thành `(3.8, 0.5, 4.0)`, biên dịch `dotnet build` đạt 0 lỗi 0 cảnh báo.
  - (4) Thực thi Visual Playtest Loop chụp 4 ảnh màn hình mới, soi mắt thần kiểm tra trực quan thành công, 372/372 test cases Passed (100%).
- [x] **[AI - agy-customizations, texture-architect & blender-helper]** Thiết lập 4 quy tắc kỹ thuật bắt buộc xóa bỏ hoàn toàn bọc Texture mù theo `modelyeucau` và Quy chuẩn Dựng Nhân Vật 3D & Animation (Character & Rigging Pipeline):
  - (1) **Trích xuất bảng màu & họa tiết thật từ ảnh mẫu** (Pixel Color & Pattern Sampling): Bắt buộc viết script Python (`PIL`/`numpy`) quét trực tiếp file ảnh trong `modelyeucau/` để lấy mẫu mã màu Hex/RGB thật của từng phân khu và sinh Texture `.png` có vân bề mặt (vân gỗ, thớ đá, gân lá, gạch lát, bạt sọc).
  - (2) **Bắt buộc trải UV tự động trong Blender & Godot** (Mandatory UV Unwrapping & Triplanar): Chạy lệnh `bpy.ops.uv.cube_project(cube_size=1.0)` hoặc `bpy.ops.uv.smart_project()` cho mọi Mesh tạo ra; bật `uv1_triplanar = true` cho bề mặt địa hình/kiến trúc lớn trong Godot.
  - (3) **Kiểm tra bọc Texture lên khối 3D thực tế**: Bắt buộc xuất ảnh bọc thử 3D `docs/test_screenshots/_texture_3d_check.png` trước khi đưa vào game.
  - (4) **Đối chiếu song song với ảnh gốc** (Side-by-Side Visual Diff): Mắt thần mở song song ảnh gốc trong `modelyeucau/` và ảnh chụp màn hình trong game để so sánh màu sắc, hoa văn, triệt tiêu mọi vật thể bị trơn màu phẳng hoặc mất material.
  - (5) **Quy Chuẩn Dựng Nhân Vật 3D & Animation (Character & Rigging Pipeline)**: Dựng tách bộ phận cơ thể (`Head`, `Torso`, `Arm_L/R`, `Leg_L/R`, `Weapon_Slot`), căn chỉnh tâm xoay (Pivot/Origin) đúng khớp vai/háng/cổ, bo tròn `bmesh`, lấy mẫu màu trang phục/mặt từ ảnh mẫu, tạo sẵn 4 Actions animation cơ bản (`Idle`, `Walk`, `Run`, `Attack`/`Work`), và render `_char_preview.png` đối chiếu tỷ lệ 1.8m trước khi đưa vào Godot.
  - Đã cập nhật đồng bộ toàn diện: `.agents/skills/texture-architect/SKILL.md`, `.agents/skills/blender-helper/SKILL.md`, `AGENTS.md`, và `GEMINI.md`.

---

## 🎯 Việc Cần Làm Tiếp Theo (Backlog / Next Steps)

### Phân Nhóm 1: Gameplay & Lập Trình (AI / Developer)
- [ ] **[AI - csharp-coder]** Lập trình thanh máu, thể lực hoặc giao diện UI cơ bản (`Scripts/UI/`).
- [ ] **[AI - csharp-coder]** Lập trình AI cho quái vật tuần tra và tấn công (`Scripts/Enemies/`).
- [ ] **[AI - code-reviewer]** Rà soát Clean Code và kiểm tra build `dotnet build` sau mỗi tính năng mới.

### Phân Nhóm 2: Đồ Họa, Âm Thanh & Cấp Độ (Human / 3D Artist)
- [ ] **[HUMAN]** Dựng model quái vật / kẻ địch mới trong Blender (ví dụ: Slime, Goblin) và xuất sang `Assets/Models_Exported/`.
- [ ] **[HUMAN]** Thiết kế thêm chướng ngại vật / rương báu / cổng dịch chuyển vào map trong Blender.
- [ ] **[HUMAN]** Tìm kiếm hoặc thiết kế âm thanh hiệu ứng (SFX bước chân, SFX chém, BGM nền) đưa vào `Assets/Audio/`.
- [ ] **[HUMAN]** Tinh chỉnh góc camera hoặc ánh sáng DirectionalLight trong Inspector Godot theo sở thích thẩm mỹ.
