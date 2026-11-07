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
