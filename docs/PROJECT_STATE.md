# TRẠNG THÁI DỰ ÁN & LỊCH SỬ PHÁT TRIỂN (PROJECT STATE & HISTORY)

> **Mục đích**: File này lưu trữ toàn bộ bối cảnh kiến trúc, danh sách tài nguyên và tiến độ dự án để AI Agent đọc hiểu ngay trong 3 giây ở mỗi phiên làm việc tiếp theo, không tốn thời gian và token quét lại từ đầu.

---

## 1. Thông Tin Tổng Quan Dự Án
- **Tên dự án**: Dự án Trò chơi Mới
- **Engine**: Godot 4.7.2 .NET (C# .NET 8.0)
- **Physics Engine**: Jolt Physics 3D
- **Thể loại Game**: 2.5D Isometric Action / Adventure
- **Góc nhìn (Camera)**: Orthographic Isometric 45° (Offset `(-28, 23, 28)`, Size `17.5`, bám theo Player và ngắm bằng `LookAt`)
- **Màn chơi khởi động mặc định**: `res://Scenes/Levels/WorldMap.tscn`

---

## 2. Bản Đồ Tài Nguyên & UID (Resource Map)

### A. Scripts (`Scripts/`)
| File Script | UID | Trách Nhiệm (Single Responsibility) |
| :--- | :--- | :--- |
| `Scripts/Player/PlayerMovement.cs` | `uid://bat3uly7f4c8o` | Vật lý di chuyển, gia tốc, trọng lực, Coyote Time (0.15s), Jump Buffer (0.15s), xoay mặt theo góc nhìn Camera Isometric chuẩn hóa `Input.GetVector`, mặt quay chuẩn hướng di chuyển `+Z` với `Mathf.Atan2(horizontalVelocity.X, horizontalVelocity.Y)`, cấu hình `SafeMargin = 0.08f`, `MaxSlides = 6`, `WallMinSlideAngle = 15°` chống kẹt mép dốc, `FloorMaxAngle = 58°` hỗ trợ leo dốc/thang, `FloorSnapLength = 0.40f` bám dốc chống nảy, dịch chuyển tức thời `TeleportTo`, **tự động khóa đứng im hoàn toàn khi Chế Độ Camera Tự Do (Free Cam) đang bật**. |
| `Scripts/Player/PlayerAnimation.cs` | `uid://dic3neyglppy0` | Đồng bộ hoạt ảnh (`Idle`, `Walk`, `Jump`); tự động nhận diện track AnimationPlayer, tự chuyển sang Procedural Lean/Bobbing khi chưa có clip, **giữ nguyên trạng thái `Idle` và triệt tiêu lean/bobbing khi Free Cam đang bật**. |
| `Scripts/Player/PlayerCombat.cs` | `uid://bm2xb2wbrsbx4` | Quản lý hệ thống tấn công cơ bản của người chơi: kích hoạt hoạt ảnh Attack, Area3D hitbox gây sát thương lên các thực thể `IDamageable`, xử lý cooldown và an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Player/PlayerInteractor.cs` | `uid://dyarx2jkxgfyv` | Quản lý việc dò tìm và tương tác với các thực thể `IInteractable` gần nhất trong bán kính `ScanRadius`, phát signal cho UI, an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Core/IInteractable.cs` | `uid://d03msuxc00sqo` | Interface chuẩn định nghĩa thực thể tương tác (`PromptText`, `CanInteract()`, `Interact()`, `OnFocusGained()`, `OnFocusLost()`). |
| `Scripts/Core/IDamageable.cs` | `uid://3c56iiu05mhv` | Interface định nghĩa thực thể nhận sát thương (`TakeDamage(float amount, Vector3 knockbackDirection)`). |
| `Scripts/Core/DummyTarget.cs` | `uid://btf3mj7gtyjw3` | Bù nhìn rơm kiểm thử sát thương: triển khai `IDamageable`, hiệu ứng nảy màu và trừ máu khi bị tấn công. |
| `Scripts/Core/InteractableArea.cs` | `uid://ccohjcxq5sdqv` | Area3D dùng chung cho tương tác, tự động sinh hình cầu va chạm `SphereShape3D`, chuyển tiếp tương tác cho node cha. |
| `Scripts/Core/SimpleNpc.cs` | `uid://d0s4mcsx0coa8` | Điều khiển NPC mẫu: hiển thị `Label3D` billboard thoại nổi (`NoDepthTest = true`, `FontSize = 36`, `OutlineSize = 8`) rõ ràng trên đầu khi tương tác, tự ẩn sau 4 giây, xoay vòng câu thoại, an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Core/VoidKillZone.cs` | `uid://dwpklcl7pp863` | Area3D vực sâu bao phủ bản đồ, tự ghi nhớ vị trí ban đầu và hồi sinh Player khi rơi ra ngoài, triệt tiêu vận tốc rơi, an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Core/CameraFollow.cs` | `uid://c7kqoh0ntwdus` | Camera điều khiển góc nhìn Isometric bám theo Player và hỗ trợ Chế Độ Tự Do (Free Cam 6-DOF), hỗ trợ chuyển đổi tâm nhìn và zoom cho chuyển đổi nội thất (`SetInteriorFocus`, `ResetInteriorFocus`), cung cấp static singleton `Instance`, tự chuyển đổi `Perspective`/`Orthogonal`, hỗ trợ thu phóng con lăn chuột mượt mà và zoom bằng cần gạt phải tay cầm (`MinZoomSize = 8`, `MaxZoomSize = 35`, `ZoomSpeed = 1.5`, `ZoomSmoothness = 10`), an toàn bộ nhớ trong `_ExitTree()`. |
| `Scripts/Core/FreeCameraController.cs` | `uid://lkkgtwutvfgt` | Bộ điều khiển bay tự do 6-DOF cho camera chế độ debug/dev, điều khiển chuột xoay góc nhìn 360 độ và bàn phím bay tự do. |
| `Scripts/Core/InteriorZone.cs` | `uid://hxqpxcpfv4oe` | Vùng chuyển đổi nội thất liền mạch (Seamless Interior Transition): Tự động ẩn mái nhà, tường trước và collider khi Player bước vào trong nhà, bật đèn ấm nội thất `OmniLight3D`, kích hoạt zoom gần và tâm ngắm của camera nội thất. |
| `Scripts/Core/BuildingInteriorArea.cs` | `uid://dkubunity3oji` | Vùng chuyển đổi nội thất cho từng công trình trong làng, kế thừa `InteriorZone`, cung cấp zoom 9.5f và góc nhìn diorama cắt vách không bị che khuất. |
| `Scripts/Core/BuildingInteriorManager.cs` | `uid://f4kh13ki1vav` | Quản lý tập trung hệ thống chuyển đổi góc nhìn nội thất liền mạch trong làng, quản lý và thông báo sự kiện chuyển đổi. |
| `Scripts/Core/DisplaySettingsManager.cs` | `uid://bf6cpcl5snmh6` | Singleton quản lý cấu hình hiển thị, độ phân giải đa màn hình (720p đến 4K), chế độ cửa sổ (Windowed, Borderless, Fullscreen), Target FPS (30, 60, 120, 144, Unlimited), VSync, lưu trữ bền vững tại `user://settings.cfg`. |
| `Scripts/Core/MapAutoCollision.cs` | `uid://7j1cd1f4exa7` | Tự động phát hiện mesh địa hình, sinh `Trimesh Collision` hai mặt (`BackfaceCollision = true`), tự động gán vật liệu từ danh mục `TEXTURE_CATALOG.md` cho các phân khu bản đồ. |
| `Scripts/Core/MaterialCatalogHelper.cs` | `uid://ban5idixs5g1w` | Hỗ trợ phân loại và ánh xạ tài nguyên vật liệu `.tres` dùng chung dựa trên tên mesh (`foliage`, `cobble`, `roof`, `wood`, `dirt`...). |
| `Scripts/Core/StairRampBuilder.cs` | `uid://l15hdn2c0a10` | Tự động sinh dốc nghiêng ConvexPolygonShape3D vô hình phủ trên các bậc thang để Player di chuyển êm ái không bị nảy hoặc kẹt góc vuông 90°. |
| `Scripts/NPC/NpcProfession.cs` | `uid://cqw6i27ut5pfk` | Enum định nghĩa 8 nghề nghiệp dân làng (`Blacksmith`, `Alchemist`, `Chef`, `Farmer`, `Fisherman`, `Miner`, `Lumberjack`, `Guard`) kèm các hàm mở rộng tiêu đề tiếng Việt và câu chào mặc định. |
| `Scripts/NPC/NpcState.cs` | `uid://4kna0gmpmq6l` | Enum định nghĩa 4 trạng thái AI State Machine (`Idle`, `Working`, `Patrolling`, `Interacting`). |
| `Scripts/NPC/NpcSpecialActionManager.cs` | `uid://v7xlf537deee` | Quản lý danh mục tùy chọn tương tác đặc biệt cho 8 nghề nghiệp (cường hóa vũ khí, mua potion hồi máu/tăng tốc, thưởng thức bánh mì, đổi khoáng sản...). |
| `Scripts/NPC/NpcBehavior.cs` | `uid://m4ifh1va3jib` | Bộ điều khiển AI State Machine và tương tác chuyên biệt cho dân làng, kế thừa `CharacterBody3D`, implement `IInteractable`, procedural working animation, tuần tra waypoints, xoay mặt nhìn Player khi tương tác. |
| `Scripts/NPC/NpcVisualHelper.cs` | `uid://cn1rdl4qfree0` | Nạp an toàn Sprite 2.5D và Avatar chân dung cho từng nghề nghiệp, thiết lập Billboard và bóng đổ cho `Sprite3D`. |
| `Scripts/UI/NpcInteractionDialog.cs` | `uid://m37pk4j735kh` | Giao diện Popup Dialog cho 8 dân làng: Hiển thị avatar/nghề nghiệp, lời chào, danh sách các nút hành động đặc biệt sinh động, mở khóa chuột và đóng sạch sẽ. |
| `Scripts/UI/SettingsMenu.cs` | `uid://g33yaavqqvle` | Giao diện Menu Cài Đặt Game mở bằng phím ESC hoặc nút HUD "⚙ Cài Đặt (ESC)", điều chỉnh đa độ phân giải (720p - 4K), chế độ cửa sổ (Windowed, Borderless, Fullscreen), FPS (30 - Unlimited), VSync, tự động lưu/nạp từ `user://settings.cfg`. |
| `Scripts/UI/SettingsMenuBinder.cs` | `uid://d2nvf1fkycuhn` | Module liên kết logic sự kiện UI cho `SettingsMenu`, đảm bảo chuẩn Clean Code (<25 dòng/hàm, <200 dòng/file) và an toàn bộ nhớ trong `_ExitTree()`. |
| `Scripts/UI/DevTeleportTab.cs` | `uid://b750qvvb04pd` | Tab dịch chuyển tức thời (Teleport) tới 8 phân khu làng và 4 phòng nội thất trên bản đồ. |
| `Scripts/UI/DevNpcSystemTab.cs` | `uid://cohvs8t3kexqv` | Tab giám sát và điều khiển trạng thái 8 NPC trong làng: xem tọa độ/state, dịch chuyển đến cạnh NPC, triệu hồi NPC tới Player, ép đổi state AI. |
| `Scripts/UI/DevGraphicsTab.cs` | `uid://qc2k7227vri3` | Tab tinh chỉnh cấu hình đồ họa, độ phân giải, FPS và VSync trực tiếp trên Dev HUD kèm nút lưu cấu hình. |
| `Scripts/UI/DevOverlay.cs` | `uid://cphjqrulbwgi1` | Bảng điều khiển HUD Chế Độ Dev (Dev Mode) mở rộng 6 tab: Bật/tắt bằng phím `F1`/`~`/`F3` hoặc Gamepad, điều phối các tab con. |
| `Scripts/UI/DevPlayerTab.cs` | `uid://bjytjrdnp1ufc` | Tab tinh chỉnh nhân vật: Sliders `MoveSpeed`, `JumpVelocity`, `Gravity`, Checkbox `InfiniteJump` (nhảy vô hạn/bất tử), Nút `TeleportTo` về điểm xuất phát. |
| `Scripts/UI/DevNpcTab.cs` | `uid://crv11rj4g6vdi` | Tab Live Dialogue Editor: Hiển thị tên NPC, danh sách thoại trong `ItemList`, ô nhập `LineEdit`, nút thêm thoại mới, phát thoại ngay, xoay vòng thoại, xóa câu thoại. |
| `Scripts/UI/DevWorldTab.cs` | `uid://bbphgkev6ohgl` | Tab Môi trường & Camera: Slider Zoom Isometric, CheckBox kích hoạt `[🎥 Free Cam]`, Slider tốc độ bay Free Cam (5.0 - 50.0), Nút `[🔄 Quay về góc nhìn Player]`, hiển thị nhãn trạng thái camera thời gian thực, FPS, Player Pos, và nút Reload màn chơi. An toàn bộ nhớ trong `_ExitTree()`. |

### B. Scenes (`Scenes/`)
| File Scene | UID | Cấu Trúc Node Chính |
| :--- | :--- | :--- |
| `Scenes/Characters/Player.tscn` | `uid://ciy0uaygbkns3` | `CharacterBody3D` (PlayerMovement) -> `CollisionShape3D` (Capsule 0.4x1.8m) -> `CharacterModel` (`character_25d.glb`) -> `PlayerAnimation` -> `PlayerInteractor` (Area3D). |
| `Scenes/Characters/NPC.tscn` | (PackedScene) | `Node3D` (SimpleNpc) -> `CharacterModel` (`character_25d.glb`) -> `InteractableArea` (Area3D). |
| `Scenes/UI/DevOverlay.tscn` | `uid://b8d2y01devhud` | `CanvasLayer` (DevOverlay, layer 100) -> `PanelContainer` (StyleBoxFlat bán trong suốt bo góc) -> `VBoxContainer` -> HeaderBar -> `TabContainer` (`DevPlayerTab`, `DevNpcTab`, `DevWorldTab`, `DevTeleportTab`, `DevNpcSystemTab`, `DevGraphicsTab`). |
| `Scenes/Characters/VillageNpc.tscn` | `uid://b2v8npcbehav1` | `CharacterBody3D` (NpcBehavior) -> `CollisionShape3D` (Capsule 0.4x1.8m) -> `VisualModel` (`character_25d.glb`) -> `InteractableArea` -> `OverheadLabel` (Label3D billboard). |
| `Scenes/UI/NpcInteractionDialog.tscn` | `uid://c3q8npcdialog1` | `CanvasLayer` (NpcInteractionDialog, layer 90) -> `PanelContainer` -> VBox (Header Tên/Nghề -> MessageLabel -> Scroll/ActionsList -> CloseButton). |
| `Scenes/UI/SettingsMenu.tscn` | `uid://cb5setmenu801` | `CanvasLayer` (SettingsMenu, layer 95) -> HudSettingsButton (nút bánh răng) & PanelContainer (chỉnh độ phân giải 720p - 4K, Window Mode, FPS 30-144-Unlimited, VSync, Nút Lưu và Nút Đóng ESC). |
| `Scenes/Levels/WorldMap.tscn` | `uid://bu1mkq5a5sqce` | **Màn chơi thế giới mở duy nhất kết nối liền mạch (Seamless Connected World)**: Chứa toàn bộ Đảo Đá gốc (`map_25d.glb`), Cánh đồng cỏ bao quanh (`map_surroundings.glb`), Bản Đồ Làng Mới (`village_map.glb`) nối liền trực tiếp qua con đường đất từ chân dốc đảo đá vào Cổng Làng (`Z=0.2` tới `Z=45`), `Player` spawn tại giao lộ kết nối `(3.8, 0.5, 4.0)`, `IsometricCamera`, 4 vùng chuyển đổi nội thất `InteriorZone_*`, cụm 8 dân làng `Village_NPCs`, `VoidKillZone`, `DevOverlay`, `NpcInteractionDialog`, `DisplaySettingsManager`. |
| `Scenes/Levels/VillageMap.tscn` | `uid://c8vlgmap72001` | **Bản sao đồng bộ hoàn hảo của WorldMap**: Chứa trọn vẹn 2 map nối liền nhau để khi mở tab trong Godot Editor hoặc ấn F6 đều hiển thị thế giới liền mạch, triệt tiêu 100% lỗi khối trắng chắn màn hình. |
| `Scenes/Levels/Village/VillageMap.tscn` | `uid://c9vlgmap72002` | **Bản sao đồng bộ đường dẫn thư mục phụ**: Đảm bảo mở từ bất kỳ đường dẫn nào trong project đều tải được scene thế giới liền mạch hoàn chỉnh. |
| `Scenes/Levels/TestLevel.tscn` | `uid://c66126flaj42w` | Level kiểm thử mặt sàn phẳng ban đầu. |

### C. 3D Models & Assets
- **Player Model**: `Assets/Models_Exported/character_25d.glb` (Animations: `Idle`, `Walk`, `Jump`, `Attack`).
- **Map Model**: `Assets/Models_Exported/map_25d.glb` (chứa `Terrain_Mesh`, `Staircase_1_Mesh`, `Staircase_2_Mesh`, `Dirt_Path_Main_Mesh`, cây cối, hoa cỏ, mây; nền gạch `SM_Tier2_Pavers` đã mở rộng diện tích gấp 6.8x thành **2.60m x 2.41m x 0.42m** khối đặc monolithic Z=[2.10, 2.52], mép tiếp giáp bắt đầu tại Y=6.99m đè nhẹ 1.4cm lên đỉnh `SM_Staircase_02` đóng kín hoàn toàn khe hở 0 gap; hàng rào gỗ `SM_Fence_Wood_Overlook` gồm 9 cột bao quanh 3 mặt Tây, Bắc, Đông và chừa lối thang Nam rộng 1.24m thông thoáng; cụm núi tím `SM_Mountains_Background` đã xóa 5 chóp chen chúc, chỉ giữ 2 ngọn núi xa thoáng đãng; đã liên kết bộ texture seamless mới: `tex_grass_seamless.png` (`Mat_Grass`), `tex_dirt_seamless.png` (`Mat_Cliff_Dirt`, `Mat_Dirt_Path`), `tex_wood_seamless.png` (`Mat_Wood`), `tex_rock_seamless.png` (`Mat_Stone`, `Mat_Cliff_Rock`); toàn bộ texture được pack trực tiếp vào file blend an toàn `map_25d_fixed.blend` và xuất sang `.glb` chuẩn Godot `export_yup=True`, `export_materials='EXPORT'`).
- **Surroundings Model**: `Assets/Models_Exported/map_surroundings.glb` (UID `uid://sdy3ykn64aus` - Cánh đồng phẳng `Terrain_Plains_Mesh` 84m x 84m được gán vật liệu cỏ xanh tươi mát `Mat_Grass_Plain` liên kết texture chuẩn `tex_grass_seamless.png`, thiết lập chuẩn UV mapping planar projection chiếu đứng `(u, v) = (x/4, y/4)` phủ đều sắc nét; toàn bộ 45 tảng đá `Rock_Mesh_*` được gán vật liệu `Mat_Stone` liên kết texture `tex_rock_seamless.png`; toàn bộ texture được pack trực tiếp vào `map_surroundings.blend` và xuất sang `.glb` chuẩn Godot; bảo tồn nguyên vẹn 63 cây, 45 tảng đá, 36 hoa cúc và duy nhất dãy núi phía Bắc `Mountain_Mesh_North` làm phông nền background xa hùng vĩ).
- **Village Map Model**: `Assets/Models/village_map.glb` (Kích thước 1.88 MB, địa hình 48m x 48m, 7 phân khu: Lâm Nghiệp, Nhà Rèn, Chợ Trung Tâm, Nhà Giả Kim, Mỏ Đá, Bến Cảng Ngư Dân với mặt nước & cầu cảng & thuyền gỗ, Cổng Làng 2 Lính Canh & 2 Thửa Ruộng Rau; hoàn thiện nội thất 4 phòng chi tiết theo modelyeucau/map2/1.jpg gồm giá vũ khí, đe, rương than, rương sắt vụn, vạc ma thuật phát sáng, kệ sách ma thuật, chai lọ độc dược, lò nướng bánh, bàn ăn dài, giỏ bánh mì, giường gối trắng nệm đỏ, tủ áo; 8 cụm phụ kiện đạo cụ đặc trưng cho 8 NPC; tách riêng các bộ phận mái `Roof_*` và tường trước `Wall_Front_*` cho cơ chế Seamless Interior Transition).
- **NPC 3D Low-Poly Models (`Assets/Models/NPCs/`)**: Bộ 8 mô hình 3D cho 8 nghề nghiệp dân làng phục vụ hiển thị 3D và đối chiếu hình học:
  * `npc_blacksmith.glb`, `npc_alchemist.glb`, `npc_chef.glb`, `npc_farmer.glb`, `npc_fisherman.glb`, `npc_miner.glb`, `npc_lumberjack.glb`, `npc_guard.glb`.
- **NPC 2.5D Stylized Sprites & Avatars (`Assets/Textures/NPCs/`)**: Trích xuất trực tiếp từ bản vẽ concept `modelyeucau/map2/1.jpg`, tách nền Alpha sạch sẽ 100%, tích hợp `Sprite3D` Y-billboard bóng đổ hai mặt và hiển thị Avatar chân dung trong hộp thoại `NpcInteractionDialog`:
  * `sprite_blacksmith.png` + `avatar_blacksmith.png` (Thợ Rèn Vulcan)
  * `sprite_alchemist.png` + `avatar_alchemist.png` (Nhà Giả Kim Aria)
  * `sprite_chef.png` + `avatar_chef.png` (Đầu Bếp Gusteau)
  * `sprite_farmer.png` + `avatar_farmer.png` (Nông Dân George)
  * `sprite_fisherman.png` + `avatar_fisherman.png` (Ngư Dân Finn tại Bến Cảng)
  * `sprite_miner.png` + `avatar_miner.png` (Thợ Mỏ Brock)
  * `sprite_lumberjack.png` + `avatar_lumberjack.png` (Tiều Phu Grover)
  * `sprite_guard.png` + `avatar_guard.png` (Lính Canh Aegis & Phalanx)
- **Blender Sources**: `Assets/Blender_Source/` (Vùng cấm ghi đè: `character_25d.blend`, `map_25d.blend` - tuân thủ nguyên vẹn tuyệt đối; File lưu an toàn cải tiến: `map_25d_fixed.blend`; File nguồn môi trường: `map_surroundings.blend`; File nguồn làng: `village_map.blend`, script sinh tự động: `build_village_map.py` tuân thủ tools/blender_kit.py và unwrap_mesh tự động 100%).

### D. Hệ Thống Texture & Vật Liệu Dùng Chung (`Assets/Textures/` & `Assets/Materials_Shared/`)
- **Tra cứu bắt buộc trước khi tạo Model / Scene**: `Assets/Textures/TEXTURE_CATALOG.md`.
- **Tileable Textures (Seamless 100%)**:
  * `tex_grass_seamless.png` (`uid://drvty0xy4e6jc`): Thảm cỏ xanh mát Stylized `#529934`.
  * `tex_dirt_seamless.png` (`uid://cj7r7nm3t4kwv`): Đất/đường mòn nâu tự nhiên hữu cơ `#8A5C35`.
  * `tex_rock_seamless.png` (`uid://u5lhns2a7ofk`): Vách đá xám phiến Stylized, vết nứt sắc nét.
  * `tex_wood_seamless.png` (`uid://cylrbgem14pnb`): Thớ vân gỗ sồi ấm áp tự nhiên `#A8764A`.
  * `tex_forge_brick.png`: Gạch nung đỏ lò rèn Stylized `#B64430` bo viền 3D.
  * `tex_anvil_iron.png`: Kim loại đe sắt đúc rèn thô `#3E4148` ánh bạc xước ngang.
  * `tex_carpet_tribal.png`: Thảm dệt thổ cẩm hoa văn hình học len.
  * `tex_canopy_striped.png` (`uid://c4vb0n6seik18`): Bạt sọc đỏ trắng cho sạp chợ.
  * `tex_magic_cloak_purple.png`: Vải nhung tím ma thuật `#6C2A80` điểm tinh thể vàng kim.
  * `tex_bread_crust.png`: Vỏ bánh mì baguette nướng vàng giòn `#C88032`.
  * `tex_roof_tiles_red.png` (`uid://b8e78ukphvtme`): Ngói vảy đỏ cam cho nhà rèn, quán ăn, nhà dân.
  * `tex_roof_tiles_teal.png` (`uid://d08e7du43tohb`): Ngói vảy xanh ngọc teal cho nhà giả kim.
  * `tex_stone_cobble.png` (`uid://bkw3f617222ku`): Đá cuội xây lò rèn, ống khói, giếng nước.
  * `tex_metal_seamless.png` (`uid://bkow053hg3twe`): Mặt kim loại phay xước nhẹ Stylized ánh bạc xám.
- **Grayscale Masks (512x512 Tương phản cao [0.25 - 1.0] để đổi màu tự do bằng `albedo_color`)**:
  * `mask_grass_detail.png` (`uid://dl88hu1ndt3py`): Mặt nạ cụm vi sợi cỏ cách điệu.
  * `mask_dirt_detail.png` (`uid://ctmnogu3s05aq`): Mặt nạ lấm tấm sỏi đất hữu cơ.
  * `mask_rock_detail.png` (`uid://6q8pf6plns63`): Mặt nạ vách đá nứt rạn góc cạnh.
  * `mask_wood_grain.png` (`uid://2smk488wwfdu`): Mặt nạ thớ sợi vân gỗ uốn lượn tự nhiên.
  * `mask_forge_brick.png`: Mặt nạ gạch nung bo viền và rãnh vữa lò rèn.
  * `mask_anvil_metal.png`: Mặt nạ xước búa rèn đe sắt (peening dimples).
  * `mask_carpet_tribal.png`: Mặt nạ dệt thổ cẩm hình học (diamonds & stripes).
  * `mask_canopy_striped.png`: Mặt nạ vòm cong bóng râm sọc bạt lều chợ.
  * `mask_purple_cloak.png`: Mặt nạ vải nhung mềm & vân ma pháp.
  * `mask_bread_crust.png`: Mặt nạ vỏ bánh mì nướng giòn & khía rãnh.
  * `mask_metal_surface.png` (`uid://cn7gdogjuc8ir`): Mặt nạ phay xước kim loại.
- **Palettes (Bảng màu Stylized chuẩn)**:
  * `palette_standard_stylized.png` (`uid://dukjgixx0vrrb`): Bảng màu 256x64 px gồm 16 dải màu chuyển sắc cho UV Palette Mapping.
- **Shared Materials (`Assets/Materials_Shared/*.tres` - StandardMaterial3D Godot 4)**:
  * `M_Grass.tres`, `M_Dirt.tres`, `M_Rock.tres`, `M_Wood.tres` (`uid://mat_m_wood`), `M_Metal.tres`: Vật liệu cơ bản theo texture seamless.
  * `M_Palette_Stylized.tres`: Vật liệu dùng chung cho toàn bộ model dùng kỹ thuật UV Color Palette.
  * `M_Wood_Fence.tres`: Gỗ sồi tối màu rustic cho hàng rào.
  * `M_Rock_Mountain_Purple.tres`: Núi tím huyền ảo viễn cảnh (biến tấu từ `mask_rock_detail.png` + `Color(0.72, 0.58, 0.84, 1.0)`).
  * `M_Grass_Dry.tres`: Cỏ khô vàng úa mùa thu.
  * `M_Dirt_RedClay.tres`: Đất đỏ bazan / mỏ đất sét.
  * `M_Metal_DarkIron.tres`: Sắt đen rèn thô.
  * `M_Forge_Brick.tres` (`uid://mat_m_forge_brick`): Gạch nung đỏ lò rèn Vulcan, ống khói, lò nướng bánh Gusteau.
  * `M_Anvil_Iron.tres` (`uid://mat_m_anvil_iron`): Sắt đen rèn thô, đe sắt nặng, búa tạ.
  * `M_Carpet_Tribal.tres` (`uid://mat_m_carpet_tribal`): Thảm hoa văn thổ cẩm phòng Nhà Giả Kim và Nhà Dân.
  * `M_Canopy_Striped.tres` (`uid://mat_m_canopy_striped`): Mái bạt sọc đỏ trắng kem lều sạp chợ.
  * `M_Magic_Cloak_Purple.tres` (`uid://mat_m_magic_cloak_purple`): Vải nhung tím ma thuật áo choàng Aria, rèm ma pháp.
  * `M_Bread_Crust.tres` (`uid://mat_m_bread_crust`): Vỏ bánh mì baguette nướng vàng giòn thơm của Gusteau.
  * `M_Roof_Tiles_Red.tres`: Mái ngói đỏ cam nhà rèn & nhà dân.
  * `M_Roof_Tiles_Teal.tres`: Mái ngói xanh ngọc teal nhà giả kim.
  * `M_Stone_Cobble.tres`: Đá cuội xây lò rèn, ống khói, giếng nước, lò nướng bánh.
  * `M_Mystic_Cyan.tres`: Dung dịch & khói ma thuật cyan phát sáng emission.
  * `M_Lava_Fire.tres`: Lửa lò rèn & lò luyện nung phát sáng emission vàng cam.
  * `M_Character_Body.tres`: Chuẩn vật liệu thân nhân vật Player / NPC Box (`character_box_texture.png`, Roughness = 0.60).
  * `M_Character_Face.tres`: Chuẩn vật liệu khuôn mặt nhân vật Player (`character_face.png`, Roughness = 0.60).

### E. Quy Trình Sketch-to-3D Pipeline (`modelyeucau/` -> Blender -> Godot)
- **Thư mục ảnh phác họa**: `modelyeucau/` (chứa các concept, sketch như `modelyeucau/charater1/`, `modelyeucau/map/`, `modelyeucau/map2/`).
- **Quy trình chuẩn hóa 4 bước**:
  1. **Nguồn ảnh**: Xác định đường dẫn file trong `modelyeucau/`.
  2. **Phân tích thị giác**: Bắt buộc dùng công cụ đọc file (`read_file`) đọc ảnh phác họa, giải mã bố cục 2D (tọa độ lưới X, Z), tỷ lệ kích thước AABB và bảng màu chủ đạo trước khi sinh mã.
  3. **Phối hợp Texture**: Đối chiếu `Assets/Textures/TEXTURE_CATALOG.md`, gán Material Slot chuẩn kết nối với `.tres` dùng chung hoặc masks đổi màu.
  4. **Dựng 3D & Xuất Godot Scene**: Soạn script Python (`bpy`), gọi Blender CLI tại `C:/xnhaugame/blender-5.4.0-alpha+main.4f97ee24309d-windows.amd64-release/blender.exe --background --python ...` để sinh Mesh đúng tọa độ, tạo va chạm (Collision `-col`/`-colonly`), xuất `.glb` vào `Assets/Models/`, sau đó tạo và liên kết vào Scene `.tscn` của Godot 4.
  5. **Bản đồ Làng đã hoàn thành**: Đã hiện thực hóa `modelyeucau/map2/1.jpg` thành `Assets/Models/village_map.glb` (884 KB, 428 mesh, 117 colliders, 6 phân khu ngoại thất và nội thất 4 phòng kèm cơ chế tách mái `Roof_*` và tường trước `Wall_Front_*`).


---

## 3. Hệ Thống Điều Khiển & Physics Layers (Input & Layers)

### A. Chế Độ Chơi Mặc Định (Isometric Gameplay)
| Hành Động | Bàn Phím & Chuột | Tay Cầm Gamepad / Joypad |
| :--- | :--- | :--- |
| **Di chuyển** | `W / A / S / D` hoặc phím mũi tên `↑ / ← / ↓ / →` (chuẩn hóa `Input.GetVector` theo hướng camera) | Cần gạt trái (Left Stick: Axis 0 & 1) hoặc D-Pad (`↑ / ← / ↓ / →`) |
| **Nhảy** | Phím `Space` (Coyote Time 0.15s, Jump Buffer 0.15s) | Nút `A` (Xbox) / Nút `✕` (PlayStation) - `JoyButton.A` |
| **Tương tác** | Phím `E` (Action name `"interact"`) | Nút `X` / `Y` (Xbox) hoặc `□` / `△` (PlayStation) - `JoyButton.X / Y` |
| **Thu phóng Camera (Zoom)** | Cuộn con lăn chuột (`WheelUp`: phóng to, `WheelDown`: thu nhỏ) | Cần gạt phải (Right Stick: Axis 3 đẩy lên/xuống) |
| **Bật/Tắt Chế Độ Dev** | Phím `F1`, `~` (QuoteLeft / Tilde) hoặc `F3` | Nút `Back` / `Select` (`JoyButton.Back`), `Start` hoặc nhấn cần phải `R3` (`JoyButton.RightStick`) |
| **Chuyển Tab Dev Mode** | Nhấp chuột chọn Tab | Nút vai `LB` (Tab trước) / `RB` (Tab kế tiếp) |

### B. Chế Độ Camera Tự Do (Free Cam Mode - 6-DOF Fly Cam)
| Hành Động | Bàn Phím & Chuột | Tay Cầm Gamepad / Joypad |
| :--- | :--- | :--- |
| **Bay Ngang / Tiến Lùi** | Phím `W / A / S / D` theo hướng nhìn camera | Cần gạt trái (Left Stick: Axis 0 & 1) |
| **Nâng Độ Cao (Bay lên)** | Phím `Space` hoặc `E` | Nút vai phải `RB` (`JoyButton.RightShoulder`) hoặc Cò phải `R2` (`JoyAxis.TriggerRight`) |
| **Hạ Độ Cao (Bay xuống)** | Phím `Ctrl` hoặc `Q` | Nút vai trái `LB` (`JoyButton.LeftShoulder`) hoặc Cò trái `L2` (`JoyAxis.TriggerLeft`) |
| **Xoay Góc Nhìn (Pitch & Yaw 360°)** | Giữ Chuột Phải (Right Click) + rê chuột | Cần gạt phải (Right Stick: Axis 2 & 3 xoay 360°) |
| **Tăng/Giảm Tốc Độ Bay** | Cuộn con lăn chuột lên / xuống (5.0 - 50.0 m/s) | Nhấn cần gạt trái `L3` (`JoyButton.LeftStick`) |
| **Quay Về Góc Nhìn Isometric** | Bấm nút `[🔄 Quay Về Góc Nhìn Player]` trên Dev HUD | Bấm Reset trên HUD hoặc tắt Dev Mode |

### C. 3D Physics Layers
- Layer 1: `World` (Mặt sàn, địa hình, vật cản tĩnh)
- Layer 2: `Player` (Nhân vật người chơi)
- Layer 3: `NPC` (Nhân vật NPC)
- Layer 4: `Interactable` (Vùng tương tác)
- Layer 5: `Hazard/KillZone` (Vực thẳm, bẫy nguy hiểm)

---

## 4. Nhật Ký Tiến Độ (Development Changelog)

### [2026-11-05] - Khởi tạo & Tích hợp Map 2.5D Isometric
1. **Lập trình chuyển động nhân vật**:
   - Viết `PlayerMovement.cs` và `PlayerAnimation.cs` tuân thủ 100% `CODING_STANDARDS.md` (Clean Code, tách hàm < 25 dòng, file < 200 dòng, Guard Clauses, XML tiếng Việt).
   - Tạo Scene `Player.tscn` tích hợp model `character_25d.glb`.
2. **Tích hợp bản đồ `map_25d`**:
   - Chuyển `map_25d.glb` và texture vào `Assets/Models_Exported/`.
   - Viết `MapAutoCollision.cs` tự động sinh va chạm vật lý cho địa hình và bậc thang, không cần vẽ tay.
   - Viết `CameraFollow.cs` tạo góc nhìn Isometric mượt mà khóa ngắm vào nhân vật.
   - Tạo Scene chính `WorldMap.tscn` hoàn chỉnh với ánh sáng, bóng đổ, bầu trời hoạt hình.
   - Sửa lỗi lệch UID giữa các Scene để lưu Scene an toàn tuyệt đối.

### [2026-11-06] - Thiết lập Hệ Thống Sub-agent & Workflow Tự Động (.agents/)
1. **Kiến trúc Sub-agent độc lập**:
   - Đặt tại `.agents/skills/`: gồm `csharp-coder`, `code-reviewer`, `producer`, `blender-helper`, `checkpoint`.
   - Cơ chế tự giải phóng token: Mỗi Sub-agent khi được spawn sẽ tự đọc state -> code/review -> ghi nhật ký vào `docs/PROJECT_STATE.md` & `docs/SESSION_HISTORY.md` -> tự đóng tiến trình (giải phóng 100% token nháp).
   - Đã định nghĩa chuẩn hóa các Sub-agent types sẵn sàng gọi qua `invoke_subagent`.
2. **Workflows tự động (`.agents/workflows/`)**:
   - `dev_and_review.py`: Tự động hóa chuỗi Lập trình C# -> QA Review -> Build kiểm tra.
   - `checkpoint_and_reset.py`: Tự động hóa việc đóng gói trạng thái và dọn dẹp ngữ cảnh.
3. **Đồng bộ hóa Không gian làm việc (Workspace Orchestration)**:
   - Đồng bộ liên kết `AGENTS.md`, `GEMINI.md`, `.agents/`, `docs/`, `PROJECT_STATE.md`, `TASKS.md`, `CODING_STANDARDS.md` tại cả `C:\xnhaugame` và thư mục dự án con `dự-án-trò-chơi-mới`.

### [2026-11-06] - Mở Rộng Thế Giới Xung Quanh (Surrounding Environment 2.5D)
1. **Thiết kế & Xuất Mô Hình Blender (`map_surroundings.glb`)**:
   - Chạy script Python (`generate_surroundings.py`) ngầm với Blender 5.4 CLI, tạo `Assets/Blender_Source/map_surroundings.blend` và xuất `Assets/Models_Exported/map_surroundings.glb`.
   - Cánh đồng 84m x 84m, 4 dãy núi bao quanh cao 8-15m, 45 tảng đá, 70 cây, 90 cụm hoa cỏ.
2. **Nâng Cấp Vật Lý Va Chạm (`MapAutoCollision.cs`)**:
   - Tự động sinh `Trimesh Collision` cho núi đá và cánh đồng.
3. **Tích hợp Scene `WorldMap.tscn`**:
   - Thêm Instance `Map_Surroundings` (`map_surroundings.glb`, UID `uid://sdy3ykn64aus`).

### [2026-11-06] - Chuẩn Hóa Hạ Tầng Cộng Tác Nhóm & Tài Liệu (Multi-developer Setup)
1. **Chuẩn hóa Git & Môi trường**: Cập nhật `.gitignore`, `.gitattributes`, `.editorconfig` (Allman style, LF/CRLF, binary 3D). Xóa file thừa `1.gitinore.txt` và untrack `*.blend1`.
2. **Xây dựng Tài liệu Hướng dẫn**: Tạo `README.md`, `docs/CONTRIBUTING.md`, bổ sung mục 4 Quy trình Cộng tác nhóm với lệnh bash và sơ đồ Mermaid.

### [2026-11-06] - Rà Soát Mã Nguồn & Sáp Nhập Nhánh `origin/dev` (AiichaN - Thành viên Hùng)
1. **Đánh Giá Chất Lượng Mã Nguồn (Code Review) Nhánh `dev`**:
   - `IInteractable.cs`: 35 dòng, chuẩn Single Responsibility, XML comment tiếng Việt đầy đủ. Đạt xuất sắc.
   - `InteractableArea.cs`: 96 dòng, tự động tạo collision shape, ủy quyền tương tác cho cha. Đạt xuất sắc.
   - `SimpleNpc.cs`: 171 dòng, hiển thị lời thoại billboard 3D, hẹn giờ tự ẩn sau 4 giây. **Đã phát hiện & refactor chống rò rỉ bộ nhớ**: hủy delegate `_hideTimer.Timeout` trước khi tạo timer mới và trong `_ExitTree`.
   - `VoidKillZone.cs`: 129 dòng, bảo vệ Player rơi vực, tự động ghi nhớ điểm hồi sinh ban đầu và `TeleportTo`. **Đã phát hiện & refactor chống rò rỉ bộ nhớ**: bổ sung `_ExitTree()` hủy sự kiện `BodyEntered -= OnBodyEntered`.
   - `PlayerInteractor.cs`: 185 dòng, quét mục tiêu tương tác gần nhất trong bán kính `ScanRadius`, phát signal UI. **Đã phát hiện & refactor chống rò rỉ bộ nhớ**: bổ sung `_ExitTree()` hủy sự kiện `AreaEntered` và `AreaExited`.
   - `PlayerMovement.cs`: 189 dòng, nâng cấp Coyote Time (0.15s), Jump Buffer (0.15s), `Input.GetVector` isometric chuẩn hóa, `TeleportTo`, xoay mặt nhân vật chống moonwalk. 100% hàm < 20 dòng (< 25 dòng). Đạt xuất sắc.
   - `PlayerAnimation.cs`: 194 dòng (< 200 dòng), tự nhận diện animation clip, tự fallback procedural lean/bobbing. Đạt chuẩn.
2. **Sáp Nhập (Merge) & Giải Quyết Xung Đột (Conflict Resolution)**:
   - Sáp nhập thành công commit `08bcde2` vào nhánh `main` (commit `e324f53`).
   - Xung đột `.gitignore`: Giữ toàn bộ quy chuẩn nghiêm ngặt của `main` và bổ sung rule `test_rot.gd`.
   - Xung đột `WorldMap.tscn`: Giữ trọn vẹn Instance mở rộng `Map_Surroundings` đồng thời tích hợp thêm `NPC` và `VoidKillZone`.
   - Xung đột `PlayerAnimation.cs`: Hợp nhất định nghĩa `_Process(double delta) => UpdateAnimation((float)delta)` ngắn gọn, sạch sẽ.
   - `nuget.config`: Khôi phục đường dẫn gói GodotPackages cục bộ chuẩn môi trường máy.
3. **Xác Thực Hệ Thống & Kiểm Thử Tự Động**:
   - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.
   - Chạy kịch bản kiểm thử Godot Headless `test_suite.gd`: **Passed: 32 / Failed: 0** (100% Pass).

### [2026-11-06] - Khắc Phục Triệt Để Lỗi Vật Lý & Hệ Thống Tương Tác / Hội Thoại
1. **Khắc phục Lỗi Hội Thoại & Tương Tác**:
   - `InteractableArea.cs`: Sửa `CollisionLayer = (1 << 2) | (1 << 3)` (Layer 3 NPC & Layer 4 Interactable), `CollisionMask = 0`, khắc phục hoàn toàn lỗi lệch physics layer khiến Player không dò thấy NPC.
   - `SimpleNpc.cs`: Quản lý cờ `_isFocused`. Khi hết 4 giây ẩn thoại (`OnDialogueTimeout`), nếu người chơi vẫn ở gần NPC thì chuyển nhãn hiển thị về `[Tên NPC]\n(Ấn E để tiếp tục trò chuyện)` thay vì ẩn mất hoàn toàn.
   - `PlayerInteractor.cs`: Bổ sung kiểm tra `Input.IsActionJustPressed(ActionName)` trong `_PhysicsProcess` để bắt phím E tức thì không bị nuốt, tích hợp cơ chế chống kích hoạt kép theo `Engine.GetProcessFrames()`.
2. **Khắc phục Lỗi Vật Lý & Chuyển Động**:
   - `PlayerMovement.cs`: Triệt tiêu lỗi FloorSnap kéo giật nhân vật dính sàn khi nhảy bằng cách đặt `FloorSnapLength = 0.0f` khi nhảy hoặc ở trên không (`!IsOnFloor()`), chỉ phục hồi `DefaultFloorSnap` (0.35m) khi đã tiếp đất ổn định. Thêm `FloorStopOnSlope` và `FloorBlockOnWall` chống trôi dốc.
   - `MapAutoCollision.cs`: Bổ sung tính năng tự động nhận diện mesh nền gạch (`paver` / `Tier2_Pavers`) và phủ `StandardMaterial3D` màu xanh cỏ tươi mát (`AlbedoColor = (0.35, 0.65, 0.25)`), đồng bộ hóa màu sắc cảnh quan theo yêu cầu.
3. **Kiểm Thử & Chuẩn Hóa Mã Nguồn**:
   - Tuân thủ 100% `CODING_STANDARDS.md`: Tất cả hàm < 25 dòng, tất cả file < 200 dòng (`PlayerMovement.cs`: 176 dòng, `PlayerInteractor.cs`: 198 dòng, `SimpleNpc.cs`: 185 dòng, `MapAutoCollision.cs`: 128 dòng, `InteractableArea.cs`: 97 dòng).
   - Mở rộng kịch bản kiểm thử tự động `test_suite.gd`: Bổ sung các test cases kiểm tra layer tương tác, trải nghiệm hội thoại, vật lý FloorSnap và đổi màu nền gạch.
   - Chạy Godot Headless: **Passed: 47 / Failed: 0** (100% Pass).
   - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.

### [2026-11-06] - Cải Tạo Môi Trường Bản Đồ 3D (Sub-agent blender-helper)
1. **Tinh Gọn Dãy Núi & Mở Rộng Tầm Nhìn Isometric**:
   - Camera Isometric đặt ở `(-28, 23, 28)` nhìn về phía Player (hướng `+X, -Z`).
   - Xóa bỏ hoàn toàn 3 dãy núi chắn tầm nhìn và chặn lối đi: `Mountain_Mesh_South`, `Mountain_Mesh_West`, `Mountain_Mesh_East`.
   - **CHỈ GIỮ LẠI DUY NHẤT 1 DÃY NÚI PHÍA BẮC**: `Mountain_Mesh_North` (trải rộng X: [-39.3, 51.4], Y: [24.0, 47.7], cao 16.5m) làm phông nền background xa hùng vĩ, thoáng đãng, tráng lệ.
2. **Đồng Bộ Màu Xanh Cỏ Cho Nền Gạch (`SM_Tier2_Pavers`)**:
   - Tuân thủ nghiêm ngặt quy tắc vùng cấm ghi đè: Đọc `map_25d.blend` vào bộ nhớ RAM qua Blender CLI mà không ghi đè file gốc.
   - Gán vật liệu xanh cỏ `Mat_Grass_Pavers` kèm UV mapping chiếu phẳng cho `SM_Tier2_Pavers`, hòa quyện tuyệt đối với địa hình cỏ của đảo.
   - Xuất lại model `Assets/Models_Exported/map_25d.glb` chuẩn Godot (-Z forward, Y up).
   - Kết hợp cấu hình 2 tầng cùng `MapAutoCollision.cs` (`MaterialOverride`), đảm bảo nền gạch hiển thị màu xanh cỏ đồng nhất trên mọi nền tảng.
3. **Ổn Định Bản Đồ (Map Stability) & Dọn Sạch Tiền Cảnh**:
   - Định hình lại bề mặt `Terrain_Plains_Mesh`: Thiết lập vùng đệm quanh đảo trung tâm (`[-4, 16] x [-4, 16]`) phẳng lì tuyệt đối ở độ cao `Z = 0.000m`, kết nối không vết nối và không nhấp nhô với đảo trung tâm.
   - Thảo nguyên phía Nam, Tây, Đông phẳng phiu êm dịu, không gờ dốc cản trở; chân núi phía Bắc dốc nhẹ từ 0.0m lên 4.2m tiếp giáp êm ái với `Mountain_Mesh_North`.
   - Dọn sạch 7 cây cối và tảng đá tiền cảnh che khuất đường nhìn từ Camera Isometric đến Player/NPC, di chuyển và snap khít 100% tài sản phụ trợ (cây, đá, hoa cỏ) lên bề mặt mới của cánh đồng.
4. **Kiểm Thử Toàn Diện**:
   - Đã re-import tài nguyên trong Godot Editor headless.
   - Mở rộng `test_suite.gd` với bài kiểm tra xác thực dãy núi duy nhất và các núi che khuất đã bị loại bỏ.
   - Kết quả kiểm thử Godot Headless: **Passed: 53 / Failed: 0** (100% Pass).
   - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.

### [2026-11-06] - Rà Soát Toàn Diện Mã Nguồn & Đảm Bảo Chất Lượng (Code Review & QA Audit)
1. **Kiểm Định Chuẩn Clean Code (`CODING_STANDARDS.md`) Toàn Bộ Scripts C#**:
   - `Scripts/Core/CameraFollow.cs`: 46 dòng, 2 hàm (11-12 dòng), Guard Clauses, XML tiếng Việt. (Đạt 100%)
   - `Scripts/Core/IInteractable.cs`: 35 dòng, interface chuẩn mực, Single Responsibility. (Đạt 100%)
   - `Scripts/Core/InteractableArea.cs`: 98 dòng, 6 hàm (< 18 dòng), tự động tạo collision shape, ủy quyền tương tác. (Đạt 100%)
   - `Scripts/Core/MapAutoCollision.cs`: 127 dòng, 8 hàm (< 16 dòng), tự động tạo Trimesh Collision & phủ vật liệu xanh cỏ. (Đạt 100%)
   - `Scripts/Core/VoidKillZone.cs`: 129 dòng, 8 hàm (< 15 dòng), an toàn bộ nhớ trong `_ExitTree()` với `BodyEntered -= OnBodyEntered`. (Đạt 100%)
   - `Scripts/Player/PlayerMovement.cs`: 175 dòng, 12 hàm (< 13 dòng), FloorSnap chống giật dính sàn, trôi dốc, xoay mặt chống moonwalk. (Đạt 100%)
   - `Scripts/Core/SimpleNpc.cs`: 183 dòng, 11 hàm (< 16 dòng), an toàn bộ nhớ trong `_ExitTree()` với `_hideTimer.Timeout -= OnDialogueTimeout`. (Đạt 100%)
   - `Scripts/Player/PlayerInteractor.cs`: 189 dòng, 15 hàm (< 19 dòng), an toàn bộ nhớ trong `_ExitTree()` với `AreaEntered` và `AreaExited`. (Đạt 100%)
   - `Scripts/Player/PlayerAnimation.cs`: 193 dòng, 13 hàm (< 19 dòng), tự động nhận diện clip hoặc procedural lean/bobbing. (Đạt 100%)
   - **Đánh giá tổng quát**: 100% file C# < 195 dòng (nằm trong giới hạn 150-200 dòng), 100% hàm <= 19 dòng (dưới mức trần 25 dòng), không lồng if quá 2 cấp, Guard Clauses nhất quán, đầy đủ XML comments tiếng Việt.
2. **Kiểm Tra An Toàn Bộ Nhớ (Memory Safety)**:
   - Mọi sự kiện đăng ký (`+=`) trong `VoidKillZone.cs`, `SimpleNpc.cs`, `PlayerInteractor.cs` đều đã có lệnh hủy (`-=`) tương ứng trong `_ExitTree()`. Hoàn toàn không rò rỉ bộ nhớ.
3. **Kiểm Tra Biên Dịch & Chạy Bộ Kiểm Thử Tự Động**:
   - Biên dịch `dotnet build "C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới\Dự án Trò chơi Mới.csproj"`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Chạy kiểm thử tự động Godot Headless `test_suite.gd`: **53 / 53 Test cases Passed (100% Pass, 0 Fail)**.

### [2026-11-06] - Sửa Hướng Quay Nhân Vật, Chống Xuyên Mép Bậc Thềm, Thu Phóng Camera & Đồng Bộ Nền Gạch
1. **Sửa Hướng Quay Mặt Nhân Vật Chuẩn Xác (`PlayerMovement.cs`)**:
   - Model `character_25d.glb` có mặt hướng chuẩn theo trục `+Z`.
   - Loại bỏ dấu âm gây hiện tượng moonwalk (đi giật lùi), sửa công thức xoay chuẩn: `float targetAngle = Mathf.Atan2(horizontalVelocity.X, horizontalVelocity.Y);`.
   - Nhân vật quay mặt nhìn thẳng chính xác 100% theo hướng chuyển động thực tế.
2. **Chống Xuyên Qua Mép / Rìa Bậc Thềm (`PlayerMovement.cs` & `MapAutoCollision.cs`)**:
   - `PlayerMovement.cs`: Trong `_Ready()`, cấu hình `SafeMargin = 0.08f;`, `MaxSlides = 6;`, `WallMinSlideAngle = Mathf.DegToRad(15.0f);` chống lọt mép góc nhọn bậc thềm và trôi dốc.
   - `MapAutoCollision.cs`: Duyệt tìm `ConcavePolygonShape3D` của các mesh địa hình sau khi gọi `CreateTrimeshCollision()`, tự động kích hoạt `concave.BackfaceCollision = true;` để các bề mặt tam giác có va chạm hai mặt, triệt tiêu hoàn toàn lỗi rơi xuyên mép bậc thang.
3. **Đồng Bộ Nền Gạch Sang Màu & Texture Cỏ (`MapAutoCollision.cs`)**:
   - Gán `StandardMaterial3D` với texture `tex_grass_grid.png` (fallback `map_25d_Tex_Grass_Grid.png`), `AlbedoColor = Colors.White` và `TextureFilter = BaseMaterial3D.TextureFilterEnum.LinearWithMipmaps`.
   - Giúp bề mặt nền gạch `SM_Tier2_Pavers` đồng nhất tuyệt đối về họa tiết ô cỏ và sắc độ với thảm cỏ xung quanh.
4. **Bổ Sung Tính Năng Phóng To / Thu Nhỏ Camera Bằng Con Lăn Chuột (`CameraFollow.cs`)**:
   - Bắt sự kiện `MouseButton.WheelUp` (phóng to, giảm Orthographic Size) và `MouseButton.WheelDown` (thu nhỏ, tăng Orthographic Size).
   - Tham số: `MinZoomSize = 8.0f;`, `MaxZoomSize = 30.0f;`, `ZoomSpeed = 1.5f;`, `ZoomSmoothness = 10.0f;`.
   - Nội suy mượt mà trong `_Process`: `Size = Mathf.Lerp(Size, _targetZoomSize, ZoomSmoothness * (float)delta);`.
5. **Đưa NPC Xuống Mặt Đất & Hoàn Thiện Tương Tác Hội Thoại**:
   - Cập nhật Scene `WorldMap.tscn`: Chuyển vị trí NPC từ sườn đồi `(3, 2.5, -6)` xuống mặt đất bằng phẳng đảo trung tâm `(5.0, 0.5, -4.0)` gần lối đi chính của Player.
   - Nâng cấp `SimpleNpc.cs`: Cấu hình nhãn `Label3D` với `NoDepthTest = true;`, `FontSize = 36;`, `OutlineSize = 8;` để chữ luôn hiển thị rõ nét, không bị che khuất. Nhấn E đổi câu thoại mượt mà xoay vòng.
6. **Kiểm Định & Biên Dịch**:
   - Tuân thủ 100% `CODING_STANDARDS.md`: Mọi hàm < 20 dòng (< 25 dòng), mọi file < 195 dòng (< 200 dòng).
   - `dotnet build "C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới\Dự án Trò chơi Mới.csproj"`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Godot Headless `test_suite.gd`: **63 / 63 Test cases Passed (100% Pass, 0 Fail)**.

### [2026-11-06] - Cải Tạo Mô Hình 3D Bản Đồ: Đóng Kín Khe Hở Bậc Thềm & Đồng Bộ Nền Gạch Cỏ Xanh (Sub-agent blender-helper)
1. **Đồng Bộ Nền Gạch `SM_Tier2_Pavers` Thành Thảm Cỏ Tự Nhiên**:
   - Gán vật liệu `Mat_Grass` trực tiếp vào mesh trong Blender, kết nối texture `Tex_Grass_Grid` (`tex_grass_grid.png`).
   - Thiết lập UV mapping phẳng (planar projection) chuẩn 1:1 `(u, v) = (x, y)` cho các mặt trên của `SM_Tier2_Pavers`, đồng bộ hoàn hảo họa tiết ô lưới và sắc thái màu xanh cỏ với mặt sàn `SM_Terrain_Chunk` của đảo trung tâm.
2. **Khắc Phục Triệt Để Khe Hở Rìa Bậc Thềm (`SM_Staircase_02` & `SM_Tier2_Pavers`)**:
   - Khắc phục khe hở 3.6cm trước đây (bậc thang kết thúc ở Y = 7.004m, nền gạch cũ bắt đầu ở Y = 7.040m).
   - Mở rộng mép tiếp giáp của `SM_Tier2_Pavers` về `Y = 6.99m`, đè nhẹ lên bậc thang 1.4cm (`7.0042m - 6.9900m`), đóng kín 100% khoảng trống chuyển tiếp giữa cầu thang và thềm paver.
   - Kéo đùn (extrude) độ dày của `SM_Tier2_Pavers` sâu xuống đất thêm 0.40m (`Z` từ 2.10m đến 2.52m), đồng thời tạo khối móng đặc monolithic liên kết toàn bộ chân đế bên dưới từ Z=2.10m đến Z=2.50m. Tạo thành một khối 3D đặc vững chắc, loại bỏ hoàn toàn hiện tượng xuyên mép, lọt kẽ vật lý.
3. **Quy Tắc Bảo Toàn & Pipeline Blender CLI**:
   - Chạy script Python ngầm qua Blender CLI 5.4.
   - Tuyệt đối tuân thủ quy tắc bảo tồn tài nguyên gốc: File nguồn gốc `map_25d.blend` được giữ nguyên vẹn 100%.
   - Lưu trữ bản cải tiến an toàn vào `Assets/Blender_Source/map_25d_fixed.blend`.
   - Xuất model `Assets/Models_Exported/map_25d.glb` chuẩn tọa độ Godot (-Z forward, Y up, `export_yup=True`).
4. **Kiểm Định & Xác Thực Hệ Thống**:
   - Bổ sung bài kiểm tra `test_paver_stair_gap_and_thickness` trong `test_suite.gd` đo đạc trực tiếp AABB: độ dày paver Y >= 0.40m và độ phủ mép tiếp giáp Z paver >= Z stair (0 gap).
   - Biên dịch `dotnet build "C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới\Dự án Trò chơi Mới.csproj"`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Chạy kiểm thử tự động Godot Headless `test_suite.gd`: **66 / 66 Test cases Passed (100% Pass, 0 Fail)**.

### [2026-11-06] - Xây Dựng Chế Độ Dev (Dev Mode / Debug Overlay HUD & Live Dialogue Editor)
1. **Kiến Trúc & Phím Tắt Dev Mode (`Scripts/UI/DevOverlay.cs`)**:
   - Phím tắt bật/tắt: Hỗ trợ linh hoạt `F1`, `~` (QuoteLeft / Tilde) và `F3`.
   - Tự động mở khóa chuột (`Input.MouseMode = Visible`) khi mở bảng HUD và ẩn bảng khi tắt hoặc ấn nút '✕'.
   - Tự động dò tìm các node trong Scene Tree: `PlayerMovement`, `CameraFollow`, `SimpleNpc`.
2. **Tab 1: 🎮 Nhân Vật (Player Tweaks - `Scripts/UI/DevPlayerTab.cs`)**:
   - Thanh trượt (Slider) tinh chỉnh `MoveSpeed` (2.0 đến 25.0) hiển thị số thực trực tiếp.
   - Thanh trượt `JumpVelocity` (5.0 đến 25.0) hiển thị số thực.
   - Thanh trượt `Gravity` (5.0 đến 40.0) hiển thị số thực.
   - CheckBox `Nhảy Vô Hạn / Bất Tử (Infinite Jump)`: Người chơi có thể nhảy liên tục trên không trung.
   - Nút `Hồi sinh / Về điểm xuất phát`: Dịch chuyển tức thời Player về vị trí xuất phát ban đầu `SpawnPosition` qua `TeleportTo`.
3. **Tab 2: 💬 Hội Thoại NPC (NPC Dialogue Live Editor - `Scripts/UI/DevNpcTab.cs`)**:
   - Hiển thị thông tin tên NPC hiện tại (`NpcName`).
   - Hiển thị danh sách câu thoại trong `ItemList` trực quan.
   - Ô nhập `LineEdit` cho phép gõ câu thoại mới.
   - Nút `Thêm Thoại`: Cập nhật trực tiếp vào mảng `DialogueLines` của NPC trong thời gian thực.
   - Nút `Nói Ngay`: Kích hoạt NPC phát câu thoại vừa nhập lập tức qua `DisplayMessage`.
   - Nút `Xoay Vòng Thoại`: Gọi `SpeakNextLine()` để chuyển sang câu tiếp theo.
   - Nút `Xóa Thoại`: Xóa câu thoại đang chọn hoặc câu cuối cùng.
4. **Tab 3: 📷 Camera & Môi Trường (World & Stats)**:
   - Thanh trượt `Camera Zoom`: Đồng bộ trực tiếp `TargetZoomSize` của `CameraFollow` (từ 8.0 đến 35.0).
   - Hiển thị thông số thời gian thực: `FPS` và tọa độ `Player Pos: (X, Y, Z)`.
   - Nút `Tải Lại Màn Chơi`: Gọi `GetTree().ReloadCurrentScene()`.
5. **Thiết Kế Giao Diện UI & Tích Hợp Scene (`Scenes/UI/DevOverlay.tscn`)**:
   - Bảng `PanelContainer` hiện đại, tông màu tối bán trong suốt (semi-transparent dark theme, bo góc 10px).
   - Gắn `DevOverlay.tscn` vào `Scenes/Levels/WorldMap.tscn`.
6. **Chuẩn Clean Code & An Toàn Bộ Nhớ**:
   - Tuân thủ 100% `CODING_STANDARDS.md`: `DevOverlay.cs` (178 dòng), `DevNpcTab.cs` (164 dòng), `DevPlayerTab.cs` (127 dòng), mọi hàm < 20 dòng (< 25 dòng), Guard Clauses, XML tiếng Việt.
   - 100% sự kiện kết nối đều được hủy (`-=`) sạch sẽ trong `_ExitTree()`.
   - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.

### [2026-11-06] - Cải Tạo Toàn Diện Ánh Sáng Môi Trường, Tonemap, Bóng Đổ & Hệ Thống Dốc Cầu Thang Tự Động (Sub-agent csharp-coder)
1. **Tái Thiết Hiệu Ứng Ánh Sáng, Bầu Trời & Tonemap (Lighting, Shadows & Environment)**:
   - Khắc phục triệt để lỗi "1 màu trắng xóa" do quá sáng clipping (ambient 0.8 + light 1.6 = 2.4 không có tonemap):
   - Cấu hình lại `WorldEnvironment` trong `WorldMap.tscn`:
     * `background_mode = 2` (Sky).
     * Tạo `Sky` với `ProceduralSkyMaterial`: `sky_top_color = Color(0.35, 0.62, 0.95)`, `sky_horizon_color = Color(0.70, 0.82, 0.95)`, `ground_bottom_color = Color(0.22, 0.38, 0.22)`, `ground_horizon_color = Color(0.55, 0.72, 0.60)`.
     * `ambient_light_source = 3` (Sky), `ambient_light_energy = 0.45` (ánh sáng môi trường dịu nhẹ, cân bằng).
     * Kích hoạt Tonemap chuẩn điện ảnh: `tonemap_mode = 3` (ACES), `tonemap_exposure = 1.0` giúp khử hoàn toàn cháy sáng trắng, màu sắc cảnh vật rực rỡ và có chiều sâu.
     * Bật `ssao_enabled = true` (Screen Space Ambient Occlusion) tạo bóng tiếp xúc tự nhiên dưới chân cây cối, tảng đá và cầu thang.
   - Cấu hình lại `DirectionalLight3D`:
     * `light_color = Color(1.0, 0.97, 0.91)` (ánh nắng ấm áp tự nhiên).
     * `light_energy = 1.15` (cường độ cân bằng, hài hòa).
     * `shadow_enabled = true`, `shadow_bias = 0.04`, `shadow_blur = 1.6` (bóng đổ mềm mại).
     * `directional_shadow_mode = 2` (PSSM 4 splits), `directional_shadow_max_distance = 70.0` (bóng đổ sắc nét toàn cảnh đảo).
2. **Khắc Phục Lỗi Leo Cầu Thang (`SM_Staircase_01`, `SM_Staircase_02`)**:
   - Phân tích nguyên nhân: Mặt đứng bậc thang 90° cản trở capsule (`FloorBlockOnWall = true`) và góc dốc của thang ~51°-57.1° vượt quá `FloorMaxAngle = 50°`.
   - Nâng cấp `PlayerMovement.cs`:
     * Tăng `DefaultMaxFloorAngle = 58.0f` (`Mathf.DegToRad(58.0f)`), cho phép leo dốc/thang lên tới 58 độ mà không bị trượt hay coi là tường.
     * Tinh chỉnh `DefaultFloorSnap = 0.40f`, giữ chân nhân vật luôn bám dính mặt dốc mượt mà khi di chuyển.
   - Tạo `Scripts/Core/StairRampBuilder.cs`:
     * Tự động phân tích hình học đỉnh và xác định hướng leo dốc của mesh cầu thang (`stair`/`staircase`).
     * Tạo mặt dốc va chạm phẳng dạng `ConvexPolygonShape3D` (lăng trụ tam giác / hình nêm wedge) trùm kín từ chân đến đỉnh bậc, mở rộng nhẹ 5cm để tiếp giáp trơn tru với sàn dưới và thềm trên.
   - Nâng cấp `Scripts/Core/MapAutoCollision.cs`:
     * Tích hợp `StairRampBuilder.BuildStairRamp` cho các mesh cầu thang thay vì sinh trimesh 90°.
     * Mở rộng `ShouldRecolorToGrass` đồng bộ vật liệu cỏ xanh texture `tex_grass_grid.png` cho cả cánh đồng `Terrain_Plains_Mesh`, đảm bảo 100% không gian đất xung quanh có màu xanh cỏ tươi mát.
3. **Kiểm Định Tự Động & Tiêu Chuẩn Clean Code**:
   - Tuân thủ 100% `CODING_STANDARDS.md`: `PlayerMovement.cs` (183 dòng), `MapAutoCollision.cs` (179 dòng), `StairRampBuilder.cs` (137 dòng), mọi hàm < 25 dòng, Guard Clauses, XML tiếng Việt, an toàn bộ nhớ trong `_ExitTree()`.
   - Biên dịch `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Mở rộng kịch bản kiểm thử `test_suite.gd` lên 91 bài test: **91 / 91 Test cases Passed (100% Pass, 0 Fail)**.

### [2026-11-06] - Khắc Phục Lỗi Trắng Xóa Bản Đồ Môi Trường & Đo Đạc Thông Số Cầu Thang (Sub-agent blender-helper)
1. **Khắc Phục Lỗi Nền Đất Xung Quanh Trắng Xóa (`map_surroundings.blend`)**:
   - Khảo sát nguyên nhân gốc rễ trong Blender 5.4: Mesh `Terrain_Plains_Mesh` dùng vật liệu `Mat_Grass` nhưng texture `Tex_Grass_Grid` chưa được pack vào file blend (`has_data: False`), và Base Color là màu xám trắng. Khi xuất GLB, glTF exporter không nhúng được ảnh nên gán màu trắng xóa.
   - Nâng cấp mô hình trong `Assets/Blender_Source/map_surroundings.blend`:
     * Tạo và gán vật liệu `Mat_Grass_Plain` với Base Color chuẩn xanh cỏ tươi `#529934` (Color(0.32, 0.60, 0.20, 1.0)), Roughness = 0.85.
     * Tải và đóng gói (pack) trực tiếp texture cỏ `Assets/Blender_Source/tex_grass_grid.png` vào file blend.
     * Liên kết Image Texture node -> Principled BSDF `Base Color` -> Material Output.
     * Tái lập trình UV mapping cho toàn bộ 1,896 mặt đa giác theo planar projection chiếu đứng `(u, v) = (x/4, y/4)`, đảm bảo hoa văn ô cỏ phủ đều và sắc nét trên toàn bộ cánh đồng 84m x 84m.
     * Bảo tồn nguyên vẹn 100% vị trí và vật liệu của 63 cây, 45 tảng đá, 36 hoa cúc và dãy núi phía Bắc `Mountain_Mesh_North`.
     * Lưu file cập nhật an toàn vào `Assets/Blender_Source/map_surroundings.blend`.
     * Xuất mô hình ra `Assets/Models_Exported/map_surroundings.glb` chuẩn Godot (`export_yup=True`, `export_materials='EXPORT'`).
     * Re-import vào Godot Headless: Texture `map_surroundings_tex_grass_grid.png` được tự động trích xuất và liên kết hoàn hảo.
2. **Khảo Sát & Đo Đạc Thông Số Hình Học Cầu Thang (`map_25d_fixed.blend`)**:
   - `SM_Staircase_01`:
     * AABB: X: [3.9250, 5.0750] (Rộng: 1.1500m), Y: [3.1960, 4.0040] (Dài/Run: 0.8080m), Z: [0.0000, 1.2500] (Cao/Rise: 1.2500m).
     * Độ dốc tổng thể (Rise/Run): 1.2500 / 0.8080 = 1.5470 -> Góc nghiêng: **57.12°**.
     * Cấu trúc: 5 bậc thang. Chiều cao mỗi bậc (Rise) = **0.2500m** (25cm), độ sâu mặt bậc (Tread run) = **0.1600m** (16cm). Góc nghiêng từng bậc = **57.38°**.
   - `SM_Staircase_02`:
     * AABB: X: [5.1500, 6.2500] (Rộng: 1.1000m), Y: [5.9958, 7.0042] (Dài/Run: 1.0083m), Z: [1.2500, 2.5000] (Cao/Rise: 1.2500m).
     * Độ dốc tổng thể (Rise/Run): 1.2500 / 1.0083 = 1.2397 -> Góc nghiêng: **51.11°**.
     * Cấu trúc: 6 bậc thang. Chiều cao mỗi bậc (Rise) = **0.2083m** (~20.8cm), độ sâu mặt bậc (Tread run) = **0.1667m** (~16.7cm). Góc nghiêng từng bậc = **51.34°**.
   - Khuyến nghị vật lý cho `csharp-coder`: Do độ dốc cầu thang thực tế (51.11° và 57.12°) vượt quá góc leo dốc tối đa mặc định (45°), giải pháp kết hợp dốc va chạm lăng trụ phẳng `ConvexPolygonShape3D` của `StairRampBuilder` cùng cấu hình `FloorMaxAngle >= 58.0°` trong `PlayerMovement.cs` đảm bảo nhân vật đi lên mượt mà tuyệt đối.
3. **Kiểm Định & Biên Dịch**:
   - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.
   - Godot Headless `test_suite.gd`: **91 / 91 Test cases Passed (100% Pass, 0 Fail)**.

### [2026-11-06] - Loại Bỏ Hoàn Toàn Tấm Phông Nền Trắng Sky Backdrop (Sub-agent blender-helper)
1. **Loại Bỏ `SM_Sky_Backdrop_Plane` Khỏi `map_25d_fixed.blend`**:
   - Sử dụng Blender 5.4 CLI: Xác định tấm plane 54m x 45m tại tọa độ (13, 13, 7.5) mang vật liệu `Mat_Sky_Gradient` che khuất bầu trời Procedural Sky và dãy núi background phía Bắc.
   - Xóa bỏ triệt để object `SM_Sky_Backdrop_Plane`, orphan mesh `Plane` và orphan material `Mat_Sky_Gradient`.
   - Bảo tồn 100% nguyên vẹn toàn bộ các thực thể khác: `SM_Terrain_Chunk`, `SM_Staircase_01`, `SM_Staircase_02`, `SM_Tier2_Pavers`, `SM_Mountains_Background`, 17 cây thông & phong, 7 tảng đá lớn, các phiến đá bước, 4 đám mây hoạt hình `SM_Cloud_*` và toàn bộ hoa cúc, bụi cỏ.
   - Tuân thủ quy tắc bảo toàn tài nguyên gốc: Tuyệt đối không ghi đè `map_25d.blend`.
   - Lưu trữ an toàn cập nhật vào `Assets/Blender_Source/map_25d_fixed.blend`.
2. **Xuất Model `.glb` Chuẩn Godot & Re-import**:
   - Xuất mô hình sang `Assets/Models_Exported/map_25d.glb` (`export_yup=True`, `export_materials='EXPORT'`).
   - Kiểm tra import GLB: Số lượng objects giảm chính xác từ 232 xuống 231 (xác nhận `SM_Sky_Backdrop_Plane` và mesh `Plane` đã bị xóa hoàn toàn).
   - Re-import tài nguyên thành công trong Godot Editor Headless.
3. **Kiểm Định & Biên Dịch Tự Động**:
   - Bổ sung bài kiểm tra `assert_true(sky_plane == null, "SM_Sky_Backdrop_Plane removed (sky is clear and unobstructed)")` vào `test_suite.gd`.
   - Godot Headless `test_suite.gd`: **92 / 92 Test cases Passed (100% Pass, 0 Fail)**.
   - Biên dịch `dotnet build`: **0 Warning(s), 0 Error(s)**.

### [2026-11-06] - Triển Khai Chế Độ Camera Tự Do (Free Cam), Tích Hợp Gamepad Controller Toàn Diện & Xóa Triệt Để Vùng Trắng Bầu Trời (Sub-agent csharp-coder)
1. **Bộ Lọc Xóa Bỏ Phông Nền Trắng Trong Mã Nguồn (`MapAutoCollision.cs`)**:
   - Bổ sung hàm nhận diện `IsSkyBackdrop`: Quét các node mesh chứa từ khóa `sky_backdrop`, `backdrop`, `sky_plane`.
   - Tự động ẩn và giải phóng (`meshInstance.Visible = false; meshInstance.QueueFree();`), không tạo va chạm và ngăn chặn hoàn toàn việc che lấp bầu trời `ProceduralSky` tự nhiên.
2. **Chế Độ Camera Tự Do (Free Camera Mode 6-DOF) & Nâng Cấp Dev Mode**:
   - Xây dựng component `Scripts/Core/FreeCameraController.cs` (156 dòng):
     * Điều khiển bay 6 bậc tự do: Phím `W/A/S/D` hoặc Cần gạt trái Gamepad theo hướng camera (`Transform.Basis`).
     * Nâng/hạ độ cao: Phím `Space/E` (bay lên), `Ctrl/Q` (bay xuống); Cò phải `R2` hoặc `RB` (bay lên), Cò trái `L2` hoặc `LB` (bay xuống).
     * Xoay góc nhìn Pitch & Yaw 360°: Giữ Chuột Phải rê chuột (Mouse Motion) hoặc Cần gạt phải Gamepad (Right Stick).
     * Tinh chỉnh tốc độ bay: Cuộn con lăn chuột hoặc bấm cần gạt trái `L3` (5.0 - 50.0 m/s).
   - Nâng cấp `Scripts/Core/CameraFollow.cs` (155 dòng):
     * Tích hợp `SetFreeCamActive(bool active)`: Chuyển đổi linh hoạt giữa góc nhìn Isometric (Orthogonal) và FreeCam (Perspective FOV 75°).
     * Tích hợp `ResetToPlayer()`: Tự động đưa Camera quay về khóa ngắm nhân vật chính.
     * Hỗ trợ thu phóng mượt mà bằng Cần gạt phải Gamepad (Right Stick) trong chế độ Isometric.
   - Tạo `Scripts/UI/DevWorldTab.cs` (161 dòng) & Nâng cấp `Scenes/UI/DevOverlay.tscn`:
     * CheckBox `[🎥 Bật/Tắt Camera Tự Do (Free Cam)]` đồng bộ trực tiếp camera.
     * Slider `Tốc độ FreeCam` (5.0 đến 50.0) tinh chỉnh tức thời.
     * Nút `[🔄 Quay Về Góc Nhìn Player (Isometric)]` khôi phục camera ngay lập tức.
     * Nhãn hiển thị trạng thái camera thời gian thực (`🎥 Free Cam 6-DOF` / `🎯 Khóa góc nhìn Isometric`).
     * Đảm bảo an toàn bộ nhớ 100% trong `_ExitTree()` hủy đăng ký mọi sự kiện UI.
3. **Tích Hợp Tay Cầm (Gamepad / Joypad Controller) Toàn Diện**:
   - Cấu hình `project.godot` `[input]`: Bổ sung toàn diện các sự kiện Joypad cho `move_left`, `move_right`, `move_forward`, `move_backward`, `jump` (JoyButton.A), `interact` (JoyButton.X / Y).
   - Bảng điều khiển Dev Mode (`DevOverlay.cs`):
     * Phím tắt bật/tắt bằng tay cầm: Nút `Back` / `Select` (`JoyButton.Back`), `Start` hoặc ấn cần phải `R3` (`JoyButton.RightStick`).
     * Chuyển đổi qua lại giữa các tab Dev Mode mượt mà bằng 2 nút vai `LB` / `RB`.
4. **Kiểm Định Chất Lượng & Clean Code Standards**:
   - Tuân thủ 100% `CODING_STANDARDS.md`: Tất cả 15 files C# đều < 195 dòng (< 200 dòng), 100% hàm < 20 dòng (< 25 dòng), Guard Clauses, XML tiếng Việt.
   - Biên dịch `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Mở rộng kịch bản kiểm thử `test_suite.gd` lên 117 bài test: **117 / 117 Test cases Passed (100% Pass, 0 Fail)**.

### [2026-11-06] - Mở Rộng Đài Cao Tầng 2, Xóa Sạch Đường Kẻ Ô Vuông Nền Cỏ & Dọn Bớt Núi Nón Tím (Sub-agent blender-helper)
1. **Mở Rộng Đài Cao (Tier 2 Terrace / Pavers) & Lan Can Hàng Rào Gỗ**:
   - Tái thiết kế `SM_Tier2_Pavers`: Mở rộng từ diện tích cũ 0.94m x 0.97m (~0.91 m²) lên kích thước mới **2.60m x 2.41m** (Diện tích: **6.27 m²**, gấp gần 7 lần cũ, gấp 2.76x chiều rộng và 2.48x chiều dài).
   - Tiếp giáp kín khít đỉnh thang: Bắt đầu tại Y = 6.990m đè nhẹ 1.4cm lên đỉnh `SM_Staircase_02` (Y = 7.004m), đảm bảo **0 gap**, không có khe hở cho nhân vật lọt.
   - Độ dày móng: Z=[2.10, 2.52], dày 0.42m dạng khối monolithic đặc vững chắc.
   - Tái thiết kế hàng rào `SM_Fence_Wood_Overlook`: Gồm 9 cột gỗ (tiết diện 0.12x0.12m cao 0.78m kèm chóp nhọn 0.10m) và thanh ray ngang đôi chạy quanh 3 mặt Tây (X=4.88), Bắc (Y=9.32), Đông (X=7.32).
   - Chừa lối vào thang thoáng đãng rộng 1.24m tại mép Nam (X in [5.08, 6.32] tại Y=7.06m) thông thẳng từ cầu thang bước lên, không còn vật cản trước mặt người chơi.
   - Xóa bỏ `SM_Overlook_Dirt_Pad` để nền đài cao là thảm cỏ xanh liền mạch; dời biển báo `SM_Signpost_Overlook` về góc Tây Bắc (5.25, 8.85).
2. **Xóa Triệt Để Đường Kẻ Ô Vuông Nền Cỏ (Clean Organic Grass Texture)**:
   - Tạo texture cỏ mới `tex_grass_clean.png` (512x512) qua Blender Python: Màu xanh tươi mát chuẩn `#529934` (sRGB RGB: 0.322, 0.600, 0.204), thảm cỏ mềm mịn tự nhiên hữu cơ, tuần hoàn seamless 100%, **tuyệt đối không có các đường kẻ ô vuông / lưới grid / bàn cờ**.
   - Cập nhật và đóng gói trực tiếp vào `map_25d_fixed.blend` (`Mat_Grass`) và `map_surroundings.blend` (`Mat_Grass_Plain`).
   - Cập nhật `MapAutoCollision.cs` sử dụng `GrassTexturePath = "res://Assets/Models_Exported/tex_grass_clean.png"`.
3. **Xóa Bớt Các Ngọn Núi Nón Tím Chen Chúc (`SM_Mountains_Background`)**:
   - Xóa bỏ 5 chóp núi nón chật chội chắn ngay sau đài cao: Peak 0, Peak 2, Peak 4, Peak 5, Peak 6.
   - Giữ lại 2 ngọn núi nền phía xa tạo điểm nhấn thanh thoát: Peak 1 (ngọn núi chính cao nhất 9.8m ở xa Y=[9.15, 16.81]) và Peak 3 (núi xa phía Đông).
   - Giải phóng tầm nhìn bầu trời ProceduralSky và mây hoạt hình thông thoáng, khoáng đạt.
4. **Quy Tắc Bảo Toàn Tài Nguyên & Kiểm Định Tự Động**:
   - Bảo tồn 100% nguyên vẹn file gốc `map_25d.blend` và `character_25d.blend`.
   - Lưu trữ an toàn cập nhật vào `map_25d_fixed.blend` và `map_surroundings.blend`.
   - Xuất mô hình `Assets/Models_Exported/map_25d.glb` và `map_surroundings.glb` chuẩn Godot.
   - Mở rộng bộ kiểm thử `test_suite.gd` lên 128 bài test: **128 / 128 Test cases Passed (100% Pass, 0 Fail)**.
   - Biên dịch `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.

### [2026-11-06] - Khóa Nhân Vật Đứng Im Khi Bật Camera Tự Do & Đồng Bộ Mã Nguồn Cỏ Không Ô Vuông (Sub-agent csharp-coder)
1. **Khóa Nhân Vật Đứng Im Hoàn Toàn Trong Chế Độ Camera Tự Do (Free Cam)**:
   - Khắc phục triệt để hiện tượng khi bật Free Cam 6-DOF trong Dev Mode, phím WASD và cần gạt Gamepad vừa di chuyển Camera vừa làm Nhân vật chạy và quay mặt theo.
   - Nâng cấp `CameraFollow.cs` (140 dòng): Khai báo `public static CameraFollow? Instance { get; private set; }`, gán `Instance = this;` trong `_Ready()`, dọn dẹp `Instance = null;` trong `_ExitTree()`.
   - Nâng cấp `PlayerMovement.cs` (167 dòng):
     * Kiểm tra Guard Clause `IsFreeCamActive()` (`CameraFollow.Instance?.IsFreeCamActive == true`).
     * Khi FreeCam bật: Triệt tiêu toàn bộ vận tốc ngang `StopHorizontalMovement()` (`Velocity = new Vector3(0, Velocity.Y, 0)`), bỏ qua việc đọc input di chuyển `_inputVector`, bỏ qua xử lý nhảy `HandleJump()`, không cập nhật gia tốc ngang `ApplyMovement()` và dừng quay mặt `ApplyRotation()`.
     * Vẫn duy trì trọng lực và snap sàn `MoveAndSlide()` để nhân vật tiếp đất ổn định, không bị kẹt hay rơi xuyên map nếu người chơi bật FreeCam khi đang trên không.
     * Khi tắt FreeCam: Nhân vật lập tức nhận lại quyền điều khiển di chuyển bình thường, trơn tru.
   - Nâng cấp `PlayerAnimation.cs` (174 dòng):
     * Bổ sung `PlayIdleState(float delta)`: Khi FreeCam đang bật, giữ nguyên hoạt ảnh `Idle` (hoặc tư thế chuẩn của model) và gọi `ResetProcedural(delta)` để triệt tiêu toàn bộ hiệu ứng nghiêng mình (lean) và nhấp nhô (bobbing) thủ tục.
2. **Đồng Bộ Mã Nguồn Vật Liệu Cỏ Không Ô Vuông (`MapAutoCollision.cs`)**:
   - Cập nhật `GrassTexturePath = "res://Assets/Models_Exported/tex_grass_clean.png"`.
   - Cải tiến `LoadGrassTexture()` quét tìm các file texture cỏ sạch không có ô vuông (`tex_grass_clean.png` tại `Assets/Models_Exported/` và `Assets/Blender_Source/textures/`).
   - Trong `GetOrCreatePaverMaterial()`: Tạo fallback vật liệu `StandardMaterial3D` chuẩn màu xanh cỏ tươi mịn tự nhiên `#529934` (`AlbedoColor = new Color(0.32f, 0.60f, 0.20f, 1.0f)`, `Roughness = 0.85f`), đảm bảo tuyệt đối không còn đường kẻ ô vuông nào xuất hiện trên toàn bộ bản đồ.
3. **Đảm Bảo Va Chạm Kín Khít Cho Đài Cao Tầng 2 & Cầu Thang**:
   - Đảm bảo `MapAutoCollision.cs` và `StairRampBuilder.cs` tự động tính toán kích thước AABB thực tế khi đài cao tầng 2 (`SM_Tier2_Pavers`, `SM_Terrain_Chunk`, `SM_Fence_Wood_Overlook`) được mở rộng.
   - Tạo khối dốc phẳng `ConvexPolygonShape3D` và kích hoạt `BackfaceCollision = true` cho mọi bề mặt `ConcavePolygonShape3D`, đảm bảo chuyển tiếp bậc thang êm ru, kín khít, 0 khe hở.
4. **Kiểm Định Clean Code & Tự Động Hóa**:
   - Tuân thủ 100% `CODING_STANDARDS.md`: Tất cả 15 files C# đều < 175 dòng (< 200 dòng), 100% hàm <= 16 dòng (< 25 dòng), Guard Clauses, XML tiếng Việt, dọn dẹp bộ nhớ sạch sẽ trong `_ExitTree()`.
   - Bổ sung bài kiểm tra vào `test_suite.gd`: Xác thực nhân vật đứng im khi `CameraFollow.IsFreeCamActive = true` và di chuyển bình thường khi `CameraFollow.IsFreeCamActive = false`.
   - Biên dịch `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Chạy kiểm thử tự động Godot Headless `test_suite.gd`: **131 / 131 Test cases Passed (100% Pass, 0 Fail)**.





### [2026-11-06] - Viết Lại Toàn Diện Tài Liệu README.md & Đồng Bộ Toàn Bộ Dự Án (Sub-agent producer)
1. **Tái Thiết Kế & Nâng Cấp Toàn Diện Tài Liệu README.md**:
   - Cập nhật bộ Badges chuyên nghiệp: Godot 4.7.2 Mono, C# .NET 8.0, Jolt Physics 3D, Blender 5.4, Clean Code Allman, Antigravity Sub-Agents, **131/131 Tests Passed (100% Pass)**.
   - Trình bày trực quan và chi tiết các tính năng gameplay & môi trường mới nhất:
     * **Đài Vọng Cảnh Tầng 2 Mở Rộng (6.27 m²)**: Rộng 2.60m x 2.41m (gấp ~7 lần diện tích cũ), móng khối 3D đặc monolithic Z=[2.10, 2.52] dày 0.42m, hệ hàng rào gỗ 3 mặt 9 cột tinh xảo, lối vào thang thông thoáng 1.24m nối thẳng đỉnh thang SM_Staircase_02, 0 gap kín khít.
     * **Thảm Cỏ Tự Nhiên Không Ô Vuông (Clean Organic Grass)**: Xóa 100% đường kẻ ô vuông / bàn cờ, thay bằng thảm cỏ seamless xanh mướt tự nhiên #529934 liền mạch trên toàn bộ bản đồ và cánh đồng 84x84m.
     * **Không Gian Bầu Trời & Dãy Núi Thoáng Đãng**: Xóa bỏ 5 chóp núi nón chật chội, chỉ giữ lại 2 ngọn núi xa làm điểm nhấn thanh thoát, loại bỏ phông che trắng SM_Sky_Backdrop_Plane, mở rộng bầu trời ProceduralSky và mây bồng bềnh.
     * **Cầu Thang Leo Mượt Mà (Stair Ramp Builder)**: Tự động phân tích hình học đỉnh và tạo khối dốc phẳng ConvexPolygonShape3D che phủ bậc thang 90°, kết hợp FloorMaxAngle = 58° và FloorSnapLength = 0.40f.
     * **Vực Sâu Tự Hồi Sinh (VoidKillZone)**: Tự động cứu sinh khi rơi khỏi đảo, triệt tiêu gia tốc rơi và đưa Player an toàn về điểm xuất phát.
     * **NPC Tương Tác & Thoại Nổi 3D Billboard**: Nhấn phím E / nút tay cầm để mở lời thoại, nhãn Label3D hiển thị rõ nét trên đầu NPC (NoDepthTest=true, FontSize=36, OutlineSize=8), tự ẩn sau 4s.
2. **Bảng Điều Khiển Toàn Diện (Controls Matrix)**:
   - Xây dựng bảng ma trận điều khiển đối chiếu trực quan 1:1 giữa **Bàn phím & Chuột** vs. **Tay cầm Gamepad** (Xbox / PlayStation) cho cả chế độ Isometric và Chế độ Camera Tự Do 6-DOF (Free Cam).
3. **Bộ Công Cụ Dev Mode HUD Toàn Năng (F1 / ~ / Select)**:
   - Mô tả chi tiết 3 Tab: Tab Nhân Vật (Player Tweaks), Tab Live Dialogue Editor (soạn thảo, thêm, phát, xoay vòng thoại), Tab Thế Giới & Camera.
   - Nêu bật **Cơ chế Freeze Player Độc Quyền**: Khi bật Free Cam, nhân vật tự động đứng im hoàn toàn để người chơi/dev tự do bay lượn ngắm cảnh, chuyển động phục hồi trơn tru ngay khi tắt.
4. **Đồng Bộ Hóa Đa Thư Mục & Kiểm Thử Xác Thực**:
   - Đồng bộ tự động giữa C:\xnhaugame\README.md và C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới\README.md qua HardLink.
   - Xác nhận biên dịch dotnet build: **0 Warning(s), 0 Error(s)**.
   - Xác nhận kiểm thử tự động Godot Headless: **131 / 131 Test cases Passed (100% Pass, 0 Fail)**.

### [2026-11-06] - Khởi Tạo Hệ Thống Texture Nền Tảng & Shared Materials (Sub-agent texture-architect)
1. **Khảo sát & Tối ưu hóa kho tài nguyên**:
   - Khảo sát các tài nguyên ảnh trong `Assets/Blender_Source/` và `Assets/Models_Exported/`.
   - Thiết lập nguyên tắc tái sử dụng tài nguyên (Luật Tối Ưu Hóa Texture & Material): Không tạo ảnh `.png` trùng lặp, dùng chung `.tres` hoặc biến tấu nhẹ bằng Grayscale Mask kết hợp `albedo_color`.
2. **Sinh bộ Texture nền tảng chuẩn Stylized & Lũy thừa 2 (512x512)**:
   - Viết kịch bản Python tự động tạo texture chu kỳ tuần hoàn (Seamless UV Wrap 100% không mối nối) tại `.agents/skills/texture-architect/scripts/generate_textures.py`.
   - **`Assets/Textures/Tileable/` (512x512 Seamless)**:
     * `tex_grass_seamless.png`: Thảm cỏ xanh mướt mát mắt `#529934`, mịn màng không ô vuông.
     * `tex_dirt_seamless.png`: Đất/đường mòn nâu tự nhiên `#8A5C35` rải sỏi nhỏ hữu cơ.
     * `tex_rock_seamless.png`: Vách đá/sỏi xám phiến Stylized góc cạnh có vết nứt tự nhiên.
     * `tex_wood_seamless.png`: Thớ vân gỗ sồi ấm áp tự nhiên `#A8764A`.
     * `tex_metal_seamless.png`: Mặt kim loại phay xước nhẹ Stylized ánh bạc xám.
   - **`Assets/Textures/Grayscale_Masks/` (512x512 Trắng đen tương phản cao [0.25 - 1.0])**:
     * `mask_grass_detail.png`: Mặt nạ vi sợi cụm cỏ cách điệu.
     * `mask_dirt_detail.png`: Mặt nạ lấm tấm sỏi đất hữu cơ.
     * `mask_rock_detail.png`: Mặt nạ vách đá nứt rạn góc cạnh Stylized.
     * `mask_wood_grain.png`: Mặt nạ thớ sợi vân gỗ uốn lượn tự nhiên.
     * `mask_metal_surface.png`: Mặt nạ phay xước bóng kim loại.
   - **`Assets/Textures/Palettes/` (Bảng màu chuẩn Stylized)**:
     * `palette_standard_stylized.png`: Bảng màu 256x64 px gồm 16 dải màu chuyển sắc mượt mà (Cỏ, Rừng, Đất mòn, Đất sét, Đá xám, Núi đá tím, Gỗ sồi, Gỗ sáng, Sắt thép, Vàng đồng, Tông da, Vải đỏ, Vải lam, Mặt nước bọt sóng, Mây trời, Hoa văn ma pháp) cho kỹ thuật Palette UV Mapping.
3. **Tạo 11 vật liệu dùng chung `Assets/Materials_Shared/*.tres` (StandardMaterial3D Godot 4)**:
   - `M_Grass.tres`: Albedo texture = `tex_grass_seamless.png`, Roughness = 0.85.
   - `M_Dirt.tres`: Albedo texture = `tex_dirt_seamless.png`, Roughness = 0.90.
   - `M_Rock.tres`: Albedo texture = `tex_rock_seamless.png`, Roughness = 0.80.
   - `M_Wood.tres`: Albedo texture = `tex_wood_seamless.png`, Roughness = 0.70.
   - `M_Metal.tres`: Albedo texture = `tex_metal_seamless.png`, Metallic = 0.85, Roughness = 0.35.
   - `M_Palette_Stylized.tres`: Albedo texture = `palette_standard_stylized.png`, Roughness = 0.60.
   - `M_Wood_Fence.tres`: `tex_wood_seamless.png` + `albedo_color = Color(0.65, 0.48, 0.32, 1.0)`, Roughness = 0.75.
   - `M_Rock_Mountain_Purple.tres`: `mask_rock_detail.png` + `albedo_color = Color(0.72, 0.58, 0.84, 1.0)`, Roughness = 0.85.
   - `M_Grass_Dry.tres`: `mask_grass_detail.png` + `albedo_color = Color(0.85, 0.76, 0.42, 1.0)`, Roughness = 0.90.
   - `M_Dirt_RedClay.tres`: `mask_dirt_detail.png` + `albedo_color = Color(0.78, 0.42, 0.28, 1.0)`, Roughness = 0.90.
   - `M_Metal_DarkIron.tres`: `mask_metal_surface.png` + `albedo_color = Color(0.35, 0.38, 0.42, 1.0)`, Metallic = 0.90, Roughness = 0.40.
4. **Cập nhật tài liệu tra cứu bắt buộc `Assets/Textures/TEXTURE_CATALOG.md`**:
   - Trình bày 3 bảng danh mục toàn diện với đường dẫn `res://`, độ phân giải, đặc tính và hướng dẫn tái sử dụng.
   - Quét nạp Godot Engine 4.7.2 Headless thành công, tự động gán UID hợp lệ cho toàn bộ tài nguyên mới.

### [2026-11-06] - Áp Dụng Bộ Material Dùng Chung Vào Map Và Player (Sub-agent csharp-coder)
1. **Chuẩn hóa vật liệu cho Player & Nhân vật**:
   - Tạo `Assets/Materials_Shared/M_Character_Body.tres` (`StandardMaterial3D`, Roughness = 0.60, liên kết texture `character_box_texture.png`, UID `uid://bp6j51qtlw6fp`).
   - Tạo `Assets/Materials_Shared/M_Character_Face.tres` (`StandardMaterial3D`, Roughness = 0.60, liên kết texture `character_face.png`, UID `uid://b2v12hdnjeipu`).
   - Bổ sung cả 2 vật liệu vào bảng 3 của `Assets/Textures/TEXTURE_CATALOG.md`.
2. **Refactor `Scripts/Core/MapAutoCollision.cs`**:
   - Tải sẵn và tái sử dụng bộ vật liệu `.tres` trong `res://Assets/Materials_Shared/`:
     * Nền gạch `SM_Tier2_Pavers` và cánh đồng `Terrain_Plains_Mesh` -> gán `M_Grass.tres`.
     * Đường đất `SM_Dirt_Path_Main`, `SM_Dirt_Path_Tier1` -> gán `M_Dirt.tres`.
     * Hàng rào gỗ `SM_Fence_Wood_Overlook` -> gán `M_Wood_Fence.tres`.
     * Vách núi viễn cảnh `SM_Mountains_Background` -> gán `M_Rock_Mountain_Purple.tres`.
     * Toàn bộ tảng đá `SM_Rock_Boulder_*` và `Rock_Mesh_*` -> gán `M_Rock.tres`.
   - Giữ nguyên cơ chế tự động xóa phông nền trời `SM_Sky_Backdrop_Plane`, tạo `BackfaceCollision = true` cho Trimesh và điều phối dốc phẳng cho cầu thang qua `StairRampBuilder`.
   - Đảm bảo 100% Clean Code: 168 dòng (< 200 dòng), 11 hàm (mỗi hàm < 15 dòng, đạt chuẩn < 25 dòng), Guard Clauses, giải phóng tham chiếu an toàn trong `_ExitTree()`.
3. **Mở rộng kịch bản kiểm định tự động `test_suite.gd`**:
   - Thêm `test_shared_materials_loading()`: Kiểm tra toàn bộ 13 file `.tres` trong `Assets/Materials_Shared/` tồn tại, nạp thành công và đúng kiểu `StandardMaterial3D`.
   - Thêm `test_character_shared_materials()`: Kiểm tra `M_Character_Body.tres` và `M_Character_Face.tres` hợp lệ, có texture gán kèm và Roughness = 0.60.
   - Thêm `test_map_shared_materials_applied()`: Kiểm tra toàn diện các mesh trên bản đồ được tự động gán đúng các file vật liệu `.tres` tương ứng.
4. **Biên dịch & Xác thực chất lượng**:
   - `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Godot Headless `test_suite.gd`: **193 / 193 Test cases Passed (100% Pass, 0 Fail)**.

### [2026-11-06] - Áp Dụng Bộ Texture Nền Tảng Mới Vào Map Trong Blender & Xuất GLB Chuẩn Godot (Sub-agent blender-helper)
1. **Áp Dụng Bộ Texture Chuẩn Vào `map_25d_fixed.blend`**:
   - Tuân thủ nguyên tắc Vùng cấm ghi đè: Tuyệt đối không chạm vào `map_25d.blend`.
   - Mở file an toàn `Assets/Blender_Source/map_25d_fixed.blend`:
     * Vật liệu cỏ `Mat_Grass` -> liên kết trực tiếp với `Assets/Textures/Tileable/tex_grass_seamless.png`.
     * Vật liệu vách đất `Mat_Cliff_Dirt` & đường mòn `Mat_Dirt_Path` -> liên kết trực tiếp với `Assets/Textures/Tileable/tex_dirt_seamless.png`.
     * Vật liệu gỗ hàng rào & biển báo `Mat_Wood` -> liên kết trực tiếp với `Assets/Textures/Tileable/tex_wood_seamless.png`.
     * Vật liệu đá `Mat_Stone` & vách đá `Mat_Cliff_Rock` -> liên kết trực tiếp với `Assets/Textures/Tileable/tex_rock_seamless.png`.
   - Sinh chuẩn UV mapping cho các đối tượng trước đây chưa có UV layer:
     * `SM_Dirt_Path_Main` & `SM_Dirt_Path_Tier1`: Tạo lớp planar `UVMap` theo tọa độ X, Y lặp chu kỳ 2.0m.
     * `SM_Staircase_01`, `SM_Staircase_02`, `SM_Signpost_Overlook`, `SM_Signpost_Tier1`: Tự động Unwrap Smart UV Project sắc nét.
     * `SM_Tier2_Pavers` & `SM_Fence_Wood_Overlook`: Chuẩn hóa tên lớp UV từ `Float2` thành `UVMap`.
   - Đóng gói toàn bộ 5 textures vào file blend qua `bpy.ops.file.pack_all()`.
   - Lưu an toàn vào `Assets/Blender_Source/map_25d_fixed.blend`.
   - Xuất mô hình sang `Assets/Models_Exported/map_25d.glb` (`export_yup=True`, `export_materials='EXPORT'`, `export_apply=True`, `export_texcoords=True`).
2. **Áp Dụng Bộ Texture Chuẩn Vào `map_surroundings.blend`**:
   - Mở file `Assets/Blender_Source/map_surroundings.blend`:
     * Cánh đồng cỏ `Mat_Grass_Plain` -> liên kết với `tex_grass_seamless.png`.
     * Toàn bộ 45 tảng đá `Rock_Mesh_*` (`Mat_Stone`) -> liên kết với `tex_rock_seamless.png`.
   - Đóng gói texture qua `bpy.ops.file.pack_all()`.
   - Lưu an toàn vào `Assets/Blender_Source/map_surroundings.blend`.
   - Xuất mô hình sang `Assets/Models_Exported/map_surroundings.glb` (`export_yup=True`, `export_materials='EXPORT'`, `export_apply=True`, `export_texcoords=True`).
3. **Re-import Headless Vào Godot & Mở Rộng Bộ Kiểm Thử**:
   - Chạy Godot Console Headless re-import cập nhật toàn diện tài nguyên cho cả 2 file `.blend` và `.glb`.
   - Thêm phương thức kiểm định `test_blender_exported_models_and_textures()` vào `test_suite.gd`:
     * Kiểm tra `map_25d.glb` và `map_surroundings.glb` nạp hợp lệ dưới dạng `PackedScene`.
     * Xác nhận bảo toàn nguyên vẹn `map_25d.blend` gốc cùng sự hiện diện của `map_25d_fixed.blend` và `map_surroundings.blend`.
     * Xác nhận sự tồn tại và tính hợp lệ của toàn bộ 5 textures trong `Assets/Textures/Tileable/`.
4. **Biên Dịch & Kết Quả Kiểm Định**:
   - `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Godot Headless `test_suite.gd`: **203 / 203 Test cases Passed (100% Pass, 0 Fail)**.



### [2026-11-07] - Cấu Hình Toàn Diện Workspace Antigravity CLI Theo Chuẩn Local Scope (Lead Orchestrator)
1. **Thực thi nguyên tắc Strict Local Scope**:
   - Toàn bộ cấu hình, rules, skills, workflows và tài nguyên chỉ hoạt động trong phạm vi cục bộ của repository `gamexnhau`.
   - Tuyệt đối không can thiệp, không tạo và không sửa đổi bất kỳ file nào thuộc phạm vi toàn cục (`~/.gemini/`).
2. **Nâng cấp và Chuẩn hóa Toàn bộ 5 Kỹ Năng Chính + Kỹ Năng Phụ Trợ**:
   - `.agents/skills/csharp-coder/SKILL.md`: Chuẩn hóa vai trò Clean C# Gameplay Programmer, chuyển đổi toàn bộ đường dẫn thành tương đối (`Dự án Trò chơi Mới.csproj`, `Scripts/`), bổ sung mô tả kích hoạt tự nhiên song ngữ (Anh - Việt), ràng buộc Clean Code (< 25 dòng/hàm, < 200 dòng/file, Guard Clauses, hủy `-=` trong `_ExitTree()`).
   - `.agents/skills/code-reviewer/SKILL.md`: Chuẩn hóa vai trò Clean Code Reviewer & QA, quy trình rà soát tự động 5 bước, kiểm định an toàn bộ nhớ và lệnh `dotnet build` 0 lỗi 0 cảnh báo.
   - `.agents/skills/producer/SKILL.md`: Chuẩn hóa vai trò Project Producer & Task Coordinator, phân chia nhiệm vụ mạch lạc `[HUMAN]` vs `[AI]`, đồng bộ hóa tài liệu giữa `docs/` và root.
   - `.agents/skills/blender-helper/SKILL.md`: Chuẩn hóa vai trò Blender Technical Assistant, cơ chế tự động tìm `blender.exe` linh hoạt (PATH hoặc `C:\Program Files\Blender Foundation\Blender 5.2`), quy tắc bất khả xâm phạm bảo vệ `.blend` gốc và cấm nhúng texture trùng vào `.glb`.
   - `.agents/skills/texture-architect/SKILL.md`: Hoàn thiện kỹ năng kiến trúc Texture/Material, cây quyết định 3 bước tối ưu hóa VRAM, quy chuẩn ảnh lũy thừa 2 và quản lý danh mục `Assets/Textures/TEXTURE_CATALOG.md`.
   - `.agents/skills/checkpoint/SKILL.md`: Chuẩn hóa vai trò Context & History Manager, tự động quét thay đổi và đóng gói bối cảnh dự án.
3. **Nâng cấp Danh Mục Tài Nguyên Dùng Chung `Assets/Textures/TEXTURE_CATALOG.md`**:
   - Bổ sung cột Định dạng (Format: PNG RGBA8, StandardMaterial3D .tres), Mục đích sử dụng chi tiết và Hướng dẫn tái sử dụng cụ thể cho từng danh mục: Palettes, Grayscale Masks, Tileable Seamless Textures và Shared Materials.
   - Thiết lập nguyên tắc bắt buộc: `@texture-architect` và `@blender-helper` phải tra cứu catalog trước khi thao tác và cập nhật ngay khi tài nguyên thay đổi.
4. **Đồng Bộ Hóa Quy Tắc Workspace `AGENTS.md` & `GEMINI.md`**:
   - Đồng bộ hóa 100% nội dung giữa `AGENTS.md` và `GEMINI.md`, xác lập rõ ràng sơ đồ luồng điều phối tự nhiên theo từng nhóm nhiệm vụ.
5. **Kiểm Định Chất Lượng Toàn Diện**:
   - Biên dịch C#: `dotnet build "Dự án Trò chơi Mới.csproj"` $\rightarrow$ **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Kiểm thử Godot Headless: Chạy `test_suite.gd` trên Godot 4.7.2 Mono $\rightarrow$ **203 / 203 Test cases Passed (100% Pass, 0 Fail)**.


### [2026-11-08] - Lập Trình Trọn Gói 4 Phân Hệ Gameplay Bản Đồ Làng Mới (Village Map) (Sub-agent csharp-coder & code-reviewer)
1. **Phân Hệ 1: Cơ Chế Chuyển Đổi Nội Thất Liền Mạch (Seamless Interior Transition)**:
   - `Scripts/Core/InteriorZone.cs` (133 dòng): Quản lý vùng nội thất Area3D cho 4 ngôi nhà (Nhà Rèn, Nhà Giả Kim, Quán Ăn, Nhà Dân), tự động ẩn/hiện mái nhà (`Roof_*`) và tường trước (`Wall_Front_*`), ngắt/bật collider va chạm, điều khiển đèn ấm nội thất `OmniLight3D`.
   - `Scripts/Core/CameraFollow.cs` (181 dòng): Bổ sung phương thức `SetInteriorFocus(Vector3? roomCenter, float? interiorZoom)` cùng overload cho GDScript/C#, lerp tâm ngắm và mức zoom phù hợp với không gian bên trong nhà mà không làm gián đoạn gameplay.
2. **Phân Hệ 2: Hệ Thống Hành Vi NPC (NPC Behavior System) & Tương Tác Đặc Biệt 8 Dân Làng**:
   - `Scripts/NPC/NpcProfession.cs` (54 dòng): Enum 8 nghề nghiệp (`Blacksmith`, `Alchemist`, `Chef`, `Farmer`, `Fisherman`, `Miner`, `Lumberjack`, `Guard`) kèm danh xưng tiếng Việt và câu chào cá nhân hóa.
   - `Scripts/NPC/NpcState.cs` (12 dòng): Enum 4 trạng thái AI State Machine (`Idle`, `Working`, `Patrolling`, `Interacting`).
   - `Scripts/NPC/NpcSpecialActionManager.cs` (101 dòng): Cung cấp bộ 2-3 tùy chọn tương tác đặc biệt cho từng nghề (cường hóa vũ khí, sửa trang bị, mua potion máu/tốc, thưởng thức bánh mì, đổi khoáng sản...).
   - `Scripts/NPC/NpcBehavior.cs` (179 dòng): Bộ não AI State Machine kế thừa `CharacterBody3D`, implement `IInteractable`, chuyển động nhấp nhô công việc thủ tục (procedural working motion), tuần tra các Waypoints, tự động xoay người đối thoại với Player khi ấn E.
   - `Scripts/UI/NpcInteractionDialog.cs` (139 dòng) & `Scenes/UI/NpcInteractionDialog.tscn`: Giao diện Popup Dialog chuẩn UX, hiển thị avatar, nghề nghiệp, danh sách nút hành động sinh động, giải phóng chuột và đóng sạch sẽ.
   - `Scenes/Characters/VillageNpc.tscn`: Scene NPC dân làng hoàn chỉnh gắn `NpcBehavior`, `CollisionShape3D`, `VisualModel` và `OverheadLabel` billboard 3D.
3. **Phân Hệ 3: Cài Đặt Hiển Thị & Khung Hình (DisplaySettingsManager)**:
   - `Scripts/Core/DisplaySettingsManager.cs` (118 dòng): Singleton quản lý cấu hình hiển thị đa độ phân giải (720p, 900p, 1080p, 1440p, 4K), chế độ cửa sổ (Windowed, Borderless, Fullscreen), Target FPS (30, 60, 120, 144, Unlimited), VSync, lưu và đọc bền vững từ `user://settings.cfg`.
4. **Phân Hệ 4: Nâng Cấp Bảng Điều Khiển Dev Mode (Dev Overlay HUD)**:
   - `Scripts/UI/DevTeleportTab.cs` (71 dòng): Tab dịch chuyển nhanh tới 8 phân khu làng và 4 phòng nội thất.
   - `Scripts/UI/DevNpcSystemTab.cs` (144 dòng): Tab giám sát 8 NPC (xem state/tọa độ, dịch chuyển tới NPC, triệu hồi NPC tới Player, ép đổi trạng thái AI).
   - `Scripts/UI/DevGraphicsTab.cs` (174 dòng): Tab tinh chỉnh độ phân giải, FPS, VSync và lưu cấu hình ngay trong game.
   - `Scripts/UI/DevOverlay.cs` (152 dòng) & `Scenes/UI/DevOverlay.tscn`: Nâng cấp giao diện 6 tab hoàn chỉnh.
5. **Phân Hệ 5: Tích Hợp Scene & Kiểm Định Chất Lượng Toàn Diện**:
   - `Scenes/Levels/WorldMap.tscn`: Kết nối liền mạch toàn diện giữa Đảo Đá và Làng Mới (Seamless Connected World), loại bỏ Scene rời `VillageMap.tscn`.
   - **Đạt chuẩn Clean Code**: 100% file C# < 200 dòng, 100% method < 25 dòng, Guard Clauses, hủy `-=` trong `_ExitTree()`.
   - **Biên dịch C#**: `dotnet build` $\rightarrow$ **Build succeeded. 0 Warning(s), 0 Error(s)**.


### [2026-11-08] - Thiết Lập Requirement-Driven Auto-Playtest Loop & Nâng Cấp Procedural Blender Kit (Sub-agent code-reviewer & blender-helper)
1. **Cơ Chế Kiểm Thử Nghiệm Thu Thực Tế (Requirement-Driven Auto-Playtest Loop)**:
   - Nâng cấp `.agents/skills/code-reviewer/SKILL.md`, `AGENTS.md`, `GEMINI.md` và `.agents/workflows/dev_and_review.py` với 4 quy tắc sống còn: Cấm chỉ chạy `dotnet build`; chuyển hóa 100% yêu cầu thành Playtest Assertions trong `test_suite.gd`; chạy Godot Headless đọc full log; Self-Healing Loop sửa lỗi liên tục đến khi 100% Pass.
   - Mở rộng `test_suite.gd`: Giả lập bước vào/ra 4 ngôi nhà (kiểm tra Seamless Interior Transition, ẩn mái/tường trước, đổi camera, bật đèn); kiểm tra chống xuyên tường/sàn cho toàn bộ mesh; giả lập tương tác 8 NPC (State 3 Interacting, hiển thị danh xưng tiếng Việt, sinh đủ nút hành động); kiểm tra Dev Tool 6 Tabs và Teleport; kiểm tra DisplaySettingsManager thay đổi 720p/1080p, FPS 60/144, VSync.
   - **Kết quả kiểm thử**: Chạy Godot Headless $\rightarrow$ **368 / 368 Test Cases PASSED (100% Tuyệt Đối, 0 Fail, 0 Error)**.
2. **Nâng Cấp Toàn Diện Kỹ Năng Blender Với 4 Quy Tắc Bắt Buộc**:
   - `.agents/skills/blender-helper/SKILL.md`, `AGENTS.md`, `GEMINI.md`: Thiết lập 4 quy tắc: (1) Cấm khối thô sơ, dùng bmesh + Modifiers (Bevel 2-3 segments, Solidify, Shade Auto Smooth); (2) Xây dựng thư viện procedural chuẩn `tools/blender_kit.py` tham số hóa, tự động căn chỉnh AABB (`snap_to_ground`, `stack_on_top`); (3) Cơ chế Mắt Thần Tự Kiểm Tra (Visual Self-Correction Loop) render `Assets/Models/_preview_render.png` bằng Workbench Cavity Shading; (4) Vòng lặp chất lượng đối chiếu trực quan với `modelyeucau/` trước khi xuất sang Godot.
   - Thư viện `tools/blender_kit.py`: Cung cấp bộ công cụ chuyển đổi tọa độ Godot-Blender, căn chỉnh AABB, vật liệu Workbench + PBR, Bevel/Solidify Modifiers, Procedural Mesh Builders (hộp beveled, trụ, đá đa giác ngẫu hóa, cây tán tầng hữu cơ, mái nhà riềm chìa), và Render Preview tự động.
   - Refactor toàn bộ `Assets/Blender_Source/build_village_map.py` theo `tools/blender_kit.py`, xuất ra `Assets/Models/village_map.glb`, render và kiểm tra trực quan thành công `Assets/Models/_preview_render.png`.


### [2026-11-08] - Thiết Lập Cơ Chế Kiểm Thử Thị Giác Thực Tế & Soi Ảnh Chụp Màn Hình (Visual Playtest & Screenshot Inspection Loop)
1. **Xóa Bỏ Kiểm Thử Mù Trong Bóng Tối (`--headless`)**:
   - Nâng cấp `.agents/skills/code-reviewer/SKILL.md`, `AGENTS.md`, `GEMINI.md`, `.agents/workflows/dev_and_review.py` và `test_suite.gd`.
   - Chạy `test_suite.gd` trực tiếp ở chế độ dựng hình thực tế (Windowed rendering qua D3D12 / Vulkan Forward+ trên Godot Mono Console) không dùng cờ `--headless`.
   - Tự động điều khiển nhân vật chạy thử nghiệm các tính năng và chụp 4 bức ảnh thực tế lưu vào `docs/test_screenshots/`:
     * `docs/test_screenshots/1_map_overview.png`: Ngoài trời toàn cảnh làng, đường đất, cổng làng, chợ, NPC.
     * `docs/test_screenshots/2_interior_view.png`: Bên trong nhà với Seamless Interior Transition (mái và tường South/West ẩn đi, đèn sáng, nhân vật và nội thất rõ ràng không bị che khuất).
     * `docs/test_screenshots/3_npc_ui.png`: Tương tác với NPC dân làng, hộp thoại popup không tràn viền, text tiếng Việt chuẩn.
     * `docs/test_screenshots/4_devtools_ui.png`: Dev Mode HUD 6 tabs và điều chỉnh đồ họa đa độ phân giải.
2. **Mắt Thần Tự Soi Ảnh & Sửa Lỗi Thị Giác (Visual Self-Healing Loop)**:
   - Dùng công cụ đọc ảnh (Vision) mở từng bức ảnh lên tự kiểm tra bằng mắt.
   - **Phát hiện & khắc phục lỗi thị giác nghiêm trọng**: Phát hiện 65 đạo cụ xung quanh (`Map_Surroundings`) mọc xuyên vào sàn nhà rèn và đường làng; đã tạo `MaterialCatalogHelper.cs` và nâng cấp `MapAutoCollision.cs` tự động dọn dẹp sạch sẽ các node xung đột.
   - **Tối ưu góc nhìn Seamless Interior Transition**: Bổ sung `Wall_South_*` và `Wall_West_*` vào danh sách ẩn khi vào nhà trong `WorldMap.tscn`, điều chỉnh `InteriorCameraZoom = 9.5`, di chuyển cây cối phía sau nhà rèn ra xa sightline camera, giúp không gian nội thất mở ra như mô hình diorama trong suốt tuyệt đẹp.
3. **Kiểm Định Toàn Diện**:
   - `dotnet build`: Build succeeded. 0 Warning(s), 0 Error(s).
   - Kiểm thử thực tế Windowed: **372 / 372 Test cases PASSED (100% Tuyệt Đối, 0 Fail, 0 Error)**.
   - Soi ảnh thực tế: 100% 4 bức ảnh đạt chuẩn thẩm mỹ cao, ánh sáng cân đối, không lún đất, không che khuất, không vỡ UI.


### [2026-11-08] - Tinh Chỉnh Điểm Spawn Giao Lộ 2 Map & Đồng Bộ Scene Editor (Sub-agent csharp-coder & producer)
1. **Giải Quyết Triệt Để Lỗi Spawn Khuất Núi Trong `WorldMap.tscn`**:
   - Di dời vị trí xuất phát mặc định của Player từ tọa độ cũ khuất sau núi `(6.0, 2.5, -6.0)` sang vị trí giao lộ đắc địa `(3.8, 0.5, 4.0)`.
   - Vị trí này nằm ngay chân bậc thang đá Đảo Đá (`SM_Staircase_01`) và trên con đường mòn đất `Path_Connector_Island` nối thẳng vào Cổng Làng (`Z=8.5`).
   - Cập nhật vị trí ban đầu của `IsometricCamera` khớp tọa độ `(-24.2, 23.5, 32.0)` để khi vừa vào game (F5), góc nhìn bao quát toàn bộ 2 Map liền kề: Phía sau là Đảo Đá bậc thang, phía trước là Cổng Làng, vườn rau, Nông dân George, Lính canh Aegis, sạp chợ và các cửa tiệm.
2. **Khởi Tạo Đồng Bộ `VillageMap.tscn` Khắc Phục Lỗi Tab Editor Cũ**:
   - Tạo đồng bộ `Scenes/Levels/VillageMap.tscn` và `Scenes/Levels/Village/VillageMap.tscn` chứa trọn vẹn 100% cấu trúc hợp nhất từ `WorldMap.tscn`.
   - Giúp Godot Editor khi reload tab `VillageMap.tscn` cũ của người dùng sẽ hiển thị ngay thế giới liền mạch, triệt tiêu hoàn toàn khối trắng chắn màn hình.
3. **Cập Nhật Vực Sâu & Biên Dịch An Toàn**:
   - `Scripts/Core/VoidKillZone.cs`: Cập nhật `DefaultSpawnPosition = new Vector3(3.8f, 0.5f, 4.0f)`.
   - `dotnet build`: **0 Warning(s), 0 Error(s)**.
4. **Kiểm Định Thị Giác Thực Tế Windowed**:
   - Chạy `test_suite.gd` trên Godot Mono Console: **372 / 372 Test cases PASSED (100% Tuyệt Đối)**.
   - Đọc ảnh kiểm tra trực quan `read_file`:
     * `docs/test_screenshots/1_map_overview.png`: Hiển thị rõ ràng giao lộ 2 map, đường đất kết nối Đảo Đá với Cổng Làng, vườn rau, NPC, không có vật thể che chắn tầm nhìn.
     * `docs/test_screenshots/2_interior_view.png`, `3_npc_ui.png`, `4_devtools_ui.png`: 100% đạt chuẩn chất lượng cao.


### [2026-11-08] - Thiết Lập 4 Quy Tắc Kỹ Thuật Chống Bọc Texture Mù & Character Rigging Pipeline (Sub-agent texture-architect & blender-helper)
1. **Nâng Cấp `.agents/skills/texture-architect/SKILL.md`**:
   - Quy tắc 1: Trích xuất bảng màu & họa tiết thật từ ảnh mẫu (`Pixel Color & Pattern Sampling`) bằng script Python (`PIL`/`numpy`) quét trực tiếp file trong `modelyeucau/` để lấy mã Hex/RGB thật và sinh Texture `.png` có vân bề mặt (vân gỗ, thớ đá, gân lá, gạch lát, bạt sọc).
   - Quy tắc 2: Bắt buộc trải UV tự động (`bpy.ops.uv.cube_project` / `smart_project`) cho mọi Mesh trong Blender và kích hoạt `uv1_triplanar = true` / `uv1_scale` trong Godot `.tres`.
   - Quy tắc 3: Kiểm tra bọc Texture lên khối 3D thực tế (`docs/test_screenshots/_texture_3d_check.png`) trước khi đưa vào game.
   - Quy tắc 4: Đối chiếu song song với ảnh gốc (`Side-by-Side Visual Diff`) giữa ảnh `modelyeucau/` và ảnh chụp màn hình game để triệt tiêu mọi vật thể bị trơn màu phẳng hoặc mất material.
2. **Nâng Cấp `.agents/skills/blender-helper/SKILL.md`**:
   - Tích hợp 4 quy tắc bọc texture & UV unwrapping cho quy trình Blender.
   - Bổ sung **Quy Chuẩn Dựng Nhân Vật 3D & Animation (Character & Rigging Pipeline)**: Dựng tách bộ phận (`Head`, `Torso`, `Arm_L/R`, `Leg_L/R`, `Weapon_Slot`), căn chỉnh tâm xoay (Pivot/Origin) đúng khớp vai/háng/cổ hoặc tạo hệ xương Armature chuẩn, bo tròn `bmesh`, lấy mẫu màu trang phục/mặt từ ảnh mẫu, tạo sẵn 4 Actions animation cơ bản (`Idle`, `Walk`, `Run`, `Attack`/`Work`), và render ảnh `_char_preview.png` đối chiếu tỷ lệ 1.8m trước khi đưa vào Godot.
3. **Đồng Bộ Hóa Toàn Diện**:
   - Cập nhật đồng bộ vào `AGENTS.md` và `GEMINI.md`.
   - Xác thực `dotnet build` 0 lỗi 0 cảnh báo.


### [2026-11-08] - Hoàn Thiện 4 Phòng Nội Thất Chuẩn Diorama Cắt Vách, Hệ Thống Seamless Interior Transition & Game Settings Menu (Village Interior & NPC System Lead)
1. **Nội Thất 4 Phòng Diorama Cắt Vách Chi Tiết Theo `modelyeucau/map2/1.jpg`**:
   - Nâng cấp `tools/build_village_map.py` và `Assets/Blender_Source/build_village_map.py`:
     * **Nhà Rèn**: Lò rèn vòm đá cao bốc khói rực lửa cam đỏ (`Blacksmith_Forge_Furnace-col`, lửa phát quang), đe sắt lớn (`Anvil_Heavy-col`) đặt trên bục tròn trung tâm, rương sắt chứa phôi thép vụn (`Chest_Scrap_Metal-col`), rương gỗ chứa than củi (`Chest_Charcoal-col`), bể nước làm nguội tôi kim loại (`Quench_Tank-col`), giá vũ khí trên tường đá có kiếm, khiên tròn, áo giáp sắt treo (`Weapon_Rack_Wall-col`), bàn thợ nguội kèm kìm, búa, đe, ê tô (`Blacksmith_Workbench-col`).
     * **Nhà Giả Kim**: Vạc đồng ma thuật phát quang cyan/ngọc bích đang sôi sục khói bốc lên (`Alchemist_Cauldron_Glowing-col`), bàn thí nghiệm mở cuốn sách ma thuật cổ, đèn cầy và ống nghiệm (`Alchemy_Lab_Table-col`), tủ sách cổ ma thuật cao kịch trần đầy sách cổ (`Alchemy_Tall_Bookshelf-col`), kệ chai lọ độc dược đủ sắc màu đỏ tím lục lam (`Potion_Shelves-col`), chùm thảo mộc khô treo lơ lửng từ xà nhà (`Hanging_Herbs-col`).
     * **Quán Ăn / Nhà Bếp**: Lò nướng bánh mì gạch vòm đỏ than hồng (`Bakery_Brick_Oven-col`), bàn nhào bột lớn có cây cán bột, bột mì trắng và các ổ bánh mì baguette vàng ươm (`Bakery_Prep_Table-col`), bàn ăn gỗ dài kèm 2 hàng ghế băng gỗ (`Dining_Table_Long-col`, `Dining_Bench_L-col`, `Dining_Bench_R-col`), kệ để bát đĩa gốm sứ (`Dish_Shelf-col`), xâu xúc xích, giò hun khói treo trần (`Hanging_Sausages-col`), thùng rượu gỗ (`Wine_Barrel_Cask-col`).
     * **Nhà Dân Cư**: Giường ngủ gỗ nệm đỏ gối trắng ấm cúng (`House_Cozy_Bed-col`), tủ quần áo 2 cánh cao lớn (`House_Wardrobe_Tall-col`), tấm thảm sàn dệt thổ cẩm sọc kẻ (`House_Floor_Rug-col`), bàn con bên cửa sổ có rèm vải xanh (`House_Side_Table-col`).
   - Chạy Blender CLI: Xuất lại `Assets/Models/village_map.glb`, lưu file an toàn `Assets/Blender_Source/village_map.blend`, render ảnh mắt thần `Assets/Models/_preview_render.png`.
2. **Hệ Thống Góc Nhìn Camera Seamless Interior Transition**:
   - Xây dựng `Scripts/Core/BuildingInteriorArea.cs` và `Scripts/Core/BuildingInteriorManager.cs`.
   - Khi người chơi bước qua cửa vào nhà: Camera mượt mà zoom cận cảnh (Interior Zoom level ~9.5), góc nghiêng vừa vặn để nhìn rõ toàn cảnh căn phòng lát cắt diorama.
   - Mái nhà và các mảng tường phía trước (South/West) tự động ẩn mượt mà không che khuất góc nhìn. Đèn phòng bên trong bật sáng ấm áp hoặc huyền bí.
   - Khi người chơi bước ra ngoài: Camera mượt mà khôi phục lại toàn cảnh làng (Exterior Zoom level ~17.5), mái và tường hiện lại.
3. **Menu Cài Đặt Game (Game Settings Menu)**:
   - Xây dựng giao diện Menu Cài Đặt hoàn chỉnh: `Scenes/UI/SettingsMenu.tscn` và `Scripts/UI/SettingsMenu.cs`.
   - Mở được bằng phím `ESC` hoặc nút "⚙ Cài Đặt (ESC)" trên màn hình.
   - Chỉnh độ phân giải màn hình: 1280x720, 1600x900, 1920x1080, 2560x1440, 3840x2160.
   - Chế độ cửa sổ: Cửa sổ (Windowed), Không viền (Borderless), Toàn màn hình (Fullscreen).
   - Giới hạn FPS: 30 FPS, 60 FPS, 120 FPS, 144 FPS, Không giới hạn (Unlimited).
   - VSync: Bật / Tắt.
   - Tự động lưu cấu hình và nạp lại từ `user://settings.cfg` qua `DisplaySettingsManager.cs`.
   - Giao diện co giãn tự động bằng Container và Anchor theo Clean Code & UI Standards.
4. **Kiểm Thử & Nghiệm Thu Thị Giác Thực Tế (Visual Playtest & Screenshot Inspection Loop)**:
   - `dotnet build`: Build succeeded. 0 Warning(s), 0 Error(s).
   - Chạy `test_suite.gd` trên Godot Mono Console Windowed (không dùng `--headless`): **463 / 463 Test cases PASSED (100% Tuyệt Đối, 0 Fail, 0 Error)**.
   - Chụp 4 ảnh màn hình thực tế lưu vào `docs/test_screenshots/` và tự soi mắt thần đối chiếu song song với `modelyeucau/map2/1.jpg`:
     * `1_map_overview.png`: Toàn cảnh giao lộ 2 map, Cổng Làng, 8 NPC và các cửa hàng.
     * `2_interior_view.png`: Bên trong phòng Nhà Rèn lát cắt diorama nhìn rõ toàn bộ đe, lò rèn, giá vũ khí, rương than, rương sắt, bể nước, bàn thợ nguội.
     * `3_npc_ui.png`: Hộp thoại tương tác NPC hiển thị Avatar HD của Vulcan và các tùy chọn hành động.
     * `4_devtools_ui.png`: Menu Cài Đặt Game và Dev Overlay hiển thị các tùy chọn phân giải, FPS, VSync.



### [2026-11-08] - Nâng Cấp Toàn Bộ Hệ Thống Sang Mô Hình Tháp Giám Sát Phân Cấp 3 Tầng (Hierarchical 3-Tier Supervision Pyramid)
1. **Thiết Lập 3 Sub-agent Giám Sát Chuyên Biệt 1-Kèm-1 (Tầng 1)**:
   - Tạo `.agents/skills/texture-inspector/SKILL.md`: Giám sát riêng kèm chặt `@texture-architect`, kiểm tra quét mã màu thật từ `modelyeucau/`, soi ảnh lát thử 2x2 Seamless `_tile_preview.png`, ảnh bọc 3D `_texture_3d_check.png` và danh mục `TEXTURE_CATALOG.md`.
   - Tạo `.agents/skills/blender-inspector/SKILL.md`: Giám sát riêng kèm chặt `@blender-helper`, soi ảnh `_preview_render.png` đối chiếu `modelyeucau/`, kiểm tra lưới `bmesh` + Bevel + Solidify + Shade Auto Smooth, trải UV bắt buộc và tỷ lệ Human Reference Scale (Người 1.8m, Cửa 2.3-2.6m, Tường 3.5-4.5m).
   - Tạo `.agents/skills/csharp-inspector/SKILL.md`: Giám sát riêng kèm chặt `@csharp-coder`, chạy công cụ tự động `tools/supervisor_gate.py` (hàm < 25 dòng, file < 200 dòng, an toàn bộ nhớ -= `_ExitTree`, Input Action, `dotnet build` 0 lỗi) và kiểm tra AABB va chạm trong `.tscn`.
2. **Thiết Lập Sub-agent Giám Sát Tổng Quản Độc Lập (Tầng 2)**:
   - Tạo `.agents/skills/chief-supervisor/SKILL.md`: Đứng trên 3 giám sát con, chỉ nhận bàn giao khi cả 3 giám sát con ký PASS, chạy `test_suite.gd` Windowed Rendering (CẤM `--headless`), kiểm tra Timestamp ảnh mới hơn code, dùng Vision soi 4 ảnh Side-by-Side với `modelyeucau/`, và điều phối vòng lặp sửa lỗi ngược (Reverse Loop).
3. **Phát Triển Bộ Công Cụ Tự Động Gatekeeper**:
   - Viết `tools/supervisor_gate.py` (Python) tự động phân tích tĩnh Clean Code C#, kiểm tra sự kiện `+=` có `-=` trong `_ExitTree()`, kiểm tra đăng ký Input Action trong `project.godot` và chạy `dotnet build`.
   - Refactor `MapAutoCollision.cs`, `StairRampBuilder.cs`, `DevGraphicsTab.cs`, `SettingsMenu.cs` (tách `SettingsMenuBinder.cs`) đảm bảo 100% C# codebase tuân thủ Clean Code (<25 dòng/hàm, <200 dòng/file).
4. **Cập Nhật Workflow & Quy Tắc Cốt Lõi**:
   - Tạo mới `.agents/workflows/hierarchical_supervision.py`.
   - Nâng cấp `.agents/workflows/dev_and_review.py` và `.agents/workflows/asset_and_material_pipeline.py`.
   - Cập nhật toàn diện `AGENTS.md` và `GEMINI.md` theo mô hình Tháp Giám Sát Phân Cấp 3 Tầng.


### [2026-11-08] - Ban Hành Luật Cô Lập Đơn Nhiệm & Quy Tắc Cấm Gộp Giám Sát (Strict 1-Skill-Per-Subagent & File-Boundary Isolation)
1. **Cấm Đặt Tên Chung Chung & Cấm Kiêm Nhiệm**:
   - Nghiêm cấm đặt tên Sub-agent dạng "System Lead", "Lead Integrator", "QA Tester" để gom việc.
   - Mỗi Sub-agent bắt buộc gắn 1-1 với 1 kỹ năng cụ thể trong `.agents/skills/`, tên Role phải mang đúng định danh kỹ năng.
2. **Cô Lập Ranh Giới File Tuyệt Đối (File-Type Boundary)**:
   - `@texture-architect`: Chỉ tạo/sửa `.png`, `.tres`, `Assets/Textures/TEXTURE_CATALOG.md`.
   - `@blender-helper`: Chỉ viết script Python `bpy` trong `tools/` / `Assets/Blender_Source/` và xuất `.glb` vào `Assets/Models/`. Cấm sửa `.cs` hoặc `.tscn`.
   - `@csharp-coder`: Chỉ viết/sửa `.cs`, `.tscn` và `project.godot`. Cấm viết script Blender hay vẽ Texture.
3. **Dây Chuyền Nối Tiếp 4 Ca Tách Biệt**:
   - Ca 1: `@texture-architect` + `@texture-inspector` -> Đóng tiến trình.
   - Ca 2: `@blender-helper` + `@blender-inspector` -> Đóng tiến trình.
   - Ca 3: `@csharp-coder` + `@csharp-inspector` -> Đóng tiến trình.
   - Ca 4: `@chief-supervisor` + `@producer` -> Nghiệm thu toàn game và đồng bộ tài liệu.
4. **Cấm Gộp Giám Sát (Strict 1-to-1 Inspector Pairing)**:
   - Mỗi Thợ bắt buộc phải có Giám sát chuyên ngành riêng biệt tương ứng có ID tiến trình độc lập.
5. **Cập Nhật Công Cụ & Quy Tắc**:
   - `tools/supervisor_gate.py`: Thêm kiểm tra tự động luật phân vai đơn nhiệm trong nhật ký phiên làm việc.
   - Cập nhật toàn diện `AGENTS.md`, `GEMINI.md`, workflows và các file `SKILL.md`.


### [2026-11-08] - Hoàn Tất Chu Kỳ Nghiệm Thu 4 Ca Nối Tiếp Theo Mô Hình Tháp Giám Sát Phân Cấp 3 Tầng & Luật Cô Lập Đơn Nhiệm (100% PASS)
1. **Ca 1 (Nhánh Texture - Sub-agent @texture-architect & @texture-inspector)**:
   - Trích xuất bảng màu thật và họa tiết từ `modelyeucau/map2/1.jpg` bằng script Python (PIL/numpy).
   - Tạo bộ 7 Grayscale Masks 512x512 mới: `mask_anvil_metal.png`, `mask_bread_crust.png`, `mask_canopy_striped.png`, `mask_carpet_tribal.png`, `mask_forge_brick.png`, `mask_purple_cloak.png`, `mask_wood_grain.png`.
   - Tạo bộ 9 Tileable Seamless Textures 256x256 mới: `tex_anvil_iron.png`, `tex_bread_crust.png`, `tex_canopy_striped.png`, `tex_carpet_tribal.png`, `tex_forge_brick.png`, `tex_magic_cloak_purple.png`, `tex_metal_seamless.png`, `tex_stone_cobble.png`, `tex_wood_seamless.png`.
   - Tạo 7 StandardMaterial3D `.tres` mới trong `Assets/Materials_Shared/`: `M_Anvil_Iron.tres`, `M_Bread_Crust.tres`, `M_Carpet_Tribal.tres`, `M_Forge_Brick.tres`, `M_Magic_Cloak_Purple.tres`, `M_Canopy_Striped.tres`, `M_Wood.tres` (với `uv1_triplanar = true`).
   - Cập nhật đầy đủ vào `Assets/Textures/TEXTURE_CATALOG.md`.
   - Giám sát `@texture-inspector` đã kiểm tra toàn bộ ảnh lát thử 2x2 Seamless (`_tile_preview_*.png`), ảnh bọc thử 3D `docs/test_screenshots/_texture_3d_check.png` và ký duyệt **100% PASS**.

2. **Ca 2 (Nhánh 3D Blender - Sub-agent @blender-helper & @blender-inspector)**:
   - Nâng cấp `tools/blender_kit.py` với giao thức bắt buộc `unwrap_mesh(obj)` và hỗ trợ gán vật liệu chuẩn.
   - Hoàn thiện mô hình Làng 48m x 48m trong `tools/build_village_map.py` và `Assets/Blender_Source/build_village_map.py`: Nội thất 4 phòng diorama cắt vách (Nhà Rèn có lò rèn than hồng, đe sắt, rương thép; Nhà Giả Kim có vạc ma thuật phát sáng, kệ sách ma thuật; Quán Ăn có lò nướng bánh baguette, bàn ăn dài; Nhà Dân có giường nệm đỏ, tủ áo); 8 cụm đạo cụ đặc trưng; Bến Cảng Ngư Dân và Cổng Làng 2 Lính Canh; xuất mô hình `Assets/Models/village_map.glb` (1.88 MB) và lưu an toàn `Assets/Blender_Source/village_map.blend`.
   - Dựng và xuất 8 model NPC 3D trong `Assets/Models/NPCs/` (`npc_blacksmith.glb`, `npc_alchemist.glb`, `npc_chef.glb`, `npc_farmer.glb`, `npc_fisherman.glb`, `npc_miner.glb`, `npc_lumberjack.glb`, `npc_guard.glb`).
   - Render mắt thần `Assets/Models/_preview_render.png`, `Assets/Models/_char_preview.png`, các ảnh preview nội thất `Assets/Models/_temp_previews/`.
   - Giám sát `@blender-inspector` đã kiểm tra lưới `bmesh` + Bevel + Solidify + Shade Auto Smooth, Human Reference Scale (Người 1.8m, Cửa 2.3-2.6m, Tường 3.5-4.5m), trải UV bắt buộc cho 100% mesh và ký duyệt **100% PASS**.

3. **Ca 3 (Nhánh C# Gameplay & Scene - Sub-agent @csharp-coder & @csharp-inspector)**:
   - C# scripts:
     * `Scripts/Core/BuildingInteriorArea.cs`: Tự động nhận diện và chuyển đổi góc nhìn nội thất diorama.
     * `Scripts/Core/BuildingInteriorManager.cs`: Quản lý tập trung các vùng nội thất.
     * `Scripts/Core/InteriorZone.cs`: Vùng ẩn/hiện mái và tường trước, collider và đèn phòng.
     * `Scripts/NPC/NpcBehavior.cs`: Cập nhật logic hành vi AI State Machine và hiển thị NPC.
     * `Scripts/NPC/NpcVisualHelper.cs`: Nạp an toàn Sprite 2.5D và Avatar chân dung cho từng NPC.
     * `Scripts/UI/SettingsMenuBinder.cs`: Tách từ `SettingsMenu.cs` để giữ mọi hàm < 25 dòng và file < 200 dòng.
   - Scenes:
     * `Scenes/Characters/VillageNpc.tscn`: Gắn `Sprite3D` Y-billboard (chiều cao chuẩn 1.80m, bóng đổ DoubleSided, độ nét cao).
     * `Scenes/Levels/WorldMap.tscn`: Hợp nhất liền mạch Đảo Đá và Làng Mới, cấu hình 4 vùng `InteriorZone` và 8 NPC dân làng.
     * `Scenes/Levels/VillageMap.tscn` & `Scenes/Levels/Village/VillageMap.tscn`: Đồng bộ cấu trúc hợp nhất.
   - Giám sát `@csharp-inspector` chạy `tools/supervisor_gate.py`: 100% hàm < 25 dòng, file < 200 dòng theo `CODING_STANDARDS.md`, an toàn bộ nhớ `-=` trong `_ExitTree()`, Input Action đã đăng ký trong `project.godot`, `dotnet build` đạt 0 lỗi 0 cảnh báo. Ký duyệt **100% PASS**.

4. **Ca 4 (Nghiệm Thu Toàn Cục & Cập Nhật Tài Liệu - Sub-agent @chief-supervisor & @producer)**:
   - `@chief-supervisor`:
     * Tiếp nhận bàn giao khi cả 3 Giám sát con ký PASS.
     * Chạy kịch bản kiểm thử `test_suite.gd` trên Godot Windowed Console (D3D12/Vulkan Forward+ render, CẤM `--headless`): **463 / 463 Test cases PASSED (100% Tuyệt đối, 0 Fail, 0 Error)**.
     * Chụp bộ 4 ảnh màn hình mới nhất vào `docs/test_screenshots/` (`1_map_overview.png`, `2_interior_view.png`, `3_npc_ui.png`, `4_devtools_ui.png`).
     * Dùng Vision soi 4 ảnh Side-by-Side với `modelyeucau/map2/1.jpg`: Ánh sáng cân đối, nội thất diorama cắt vách rõ ràng không bị che khuất, NPC 2.5D hiển thị sắc nét với Avatar chân dung, Dev Overlay HUD 6 tabs và Settings Menu co giãn linh hoạt.
     * Ký duyệt **100% PASS Toàn Cục**.
   - `@producer`:
     * Thực thi Quy tắc Chữa Mù Đồng Bộ Tài Liệu: Quét toàn bộ hệ thống file thực tế trên ổ cứng trong `Scripts/`, `Scenes/`, `Assets/`, `tools/` và `docs/`.
     * Cập nhật đồng bộ toàn diện vào `docs/PROJECT_STATE.md`, `PROJECT_STATE.md`, `docs/TASKS.md`, `TASKS.md` và `docs/SESSION_HISTORY.md`.
     * Báo cáo kết quả hoàn thành cho Lead Orchestrator.
