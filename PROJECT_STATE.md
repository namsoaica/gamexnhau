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
| `Scripts/Player/PlayerInteractor.cs` | `uid://cwt2g2l1041b` | Quản lý việc dò tìm và tương tác với các thực thể `IInteractable` gần nhất trong bán kính `ScanRadius`, phát signal cho UI, an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Core/IInteractable.cs` | `uid://cb38i1wmsj35b` | Interface chuẩn định nghĩa thực thể tương tác (`PromptText`, `CanInteract()`, `Interact()`, `OnFocusGained()`, `OnFocusLost()`). |
| `Scripts/Core/InteractableArea.cs` | `uid://b45c22501e5v` | Area3D dùng chung cho tương tác, tự động sinh hình cầu va chạm `SphereShape3D`, chuyển tiếp tương tác cho node cha. |
| `Scripts/Core/SimpleNpc.cs` | `uid://cqj18q3f63k1` | Điều khiển NPC mẫu: hiển thị `Label3D` billboard thoại nổi (`NoDepthTest = true`, `FontSize = 36`, `OutlineSize = 8`) rõ ràng trên đầu khi tương tác, tự ẩn sau 4 giây, xoay vòng câu thoại, an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Core/VoidKillZone.cs` | `uid://dwpklcl7pp863` | Area3D vực sâu bao phủ bản đồ, tự ghi nhớ vị trí ban đầu và hồi sinh Player khi rơi ra ngoài, triệt tiêu vận tốc rơi, an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Core/CameraFollow.cs` | `uid://c7kqoh0ntwdus` | Camera điều khiển góc nhìn Isometric bám theo Player và hỗ trợ Chế Độ Tự Do (Free Cam 6-DOF), cung cấp static singleton `Instance`, tự chuyển đổi `Perspective`/`Orthogonal`, hỗ trợ thu phóng con lăn chuột mượt mà và zoom bằng cần gạt phải tay cầm (`MinZoomSize = 8`, `MaxZoomSize = 35`, `ZoomSpeed = 1.5`, `ZoomSmoothness = 10`), cung cấp `SetFreeCamActive()` và `ResetToPlayer()`, an toàn bộ nhớ trong `_ExitTree()`. |
| `Scripts/Core/FreeCameraController.cs` | (C# Script) | Bộ điều khiển Camera Tự Do (6-DOF Fly Cam) độc lập, hỗ trợ bàn phím WASD / Space / Ctrl / EQ, xoay góc nhìn chuột phải + Mouse Motion hoặc Right Stick cần phải, nâng/hạ độ cao bằng cò L2/R2 hoặc LB/RB, cuộn chuột điều chỉnh tốc độ bay (5.0 - 50.0). |
| `Scripts/Core/MapAutoCollision.cs` | `uid://7j1cd1f4exa7` | Tự động tải và tái sử dụng bộ vật liệu dùng chung `res://Assets/Materials_Shared/` (`M_Grass.tres`, `M_Dirt.tres`, `M_Rock.tres`, `M_Wood_Fence.tres`, `M_Rock_Mountain_Purple.tres`), tự động gán vật liệu chuẩn cho nền gạch, cánh đồng, lối mòn đất, hàng rào gỗ, vách núi tím viễn cảnh và đá tảng; loại bỏ các tấm phông nền trắng `sky_backdrop`/`sky_plane` để lộ bầu trời xanh ProceduralSky; tự động tạo `Trimesh Collision` kèm `BackfaceCollision = true` cho địa hình và điều phối tạo Ramp cho cầu thang qua `StairRampBuilder`. Tuân thủ Clean Code 168 dòng, mỗi hàm < 15 dòng, dọn dẹp biến trong `_ExitTree()`. |
| `Scripts/Core/StairRampBuilder.cs` | (C# Script) | Tự động phân tích hình học đỉnh và hướng dốc của mesh cầu thang (`stair`/`staircase`), tạo khối dốc nghiêng phẳng `ConvexPolygonShape3D` che phủ bậc thang giúp nhân vật bước lên êm ru không vướng góc 90°. |
| `Scripts/UI/DevOverlay.cs` | (C# Script) | Bảng điều khiển HUD Chế Độ Dev (Dev Mode): Bật/tắt linh hoạt bằng phím `F1`/`~`/`F3` hoặc tay cầm Gamepad (`Back`/`Select`, `Start`, `RightStick`), chuyển đổi các tab bằng nút vai `LB`/`RB`, mở khóa chuột, điều phối các tab con. |
| `Scripts/UI/DevPlayerTab.cs` | (C# Script) | Tab tinh chỉnh nhân vật: Sliders `MoveSpeed`, `JumpVelocity`, `Gravity`, Checkbox `InfiniteJump` (nhảy vô hạn/bất tử), Nút `TeleportTo` về điểm xuất phát. |
| `Scripts/UI/DevNpcTab.cs` | (C# Script) | Tab Live Dialogue Editor: Hiển thị tên NPC, danh sách thoại trong `ItemList`, ô nhập `LineEdit`, nút thêm thoại mới, phát thoại ngay, xoay vòng thoại, xóa câu thoại. |
| `Scripts/UI/DevWorldTab.cs` | (C# Script) | Tab Môi trường & Camera: Slider Zoom Isometric, CheckBox kích hoạt `[🎥 Free Cam]`, Slider tốc độ bay Free Cam (5.0 - 50.0), Nút `[🔄 Quay về góc nhìn Player]`, hiển thị nhãn trạng thái camera thời gian thực, FPS, Player Pos, và nút Reload màn chơi. An toàn bộ nhớ trong `_ExitTree()`. |

### B. Scenes (`Scenes/`)
| File Scene | UID | Cấu Trúc Node Chính |
| :--- | :--- | :--- |
| `Scenes/Characters/Player.tscn` | `uid://ciy0uaygbkns3` | `CharacterBody3D` (PlayerMovement) -> `CollisionShape3D` (Capsule 0.4x1.8m) -> `CharacterModel` (`character_25d.glb`) -> `PlayerAnimation` -> `PlayerInteractor` (Area3D). |
| `Scenes/Characters/NPC.tscn` | (PackedScene) | `Node3D` (SimpleNpc) -> `CharacterModel` (`character_25d.glb`) -> `InteractableArea` (Area3D). |
| `Scenes/UI/DevOverlay.tscn` | `uid://b8d2y01devhud` | `CanvasLayer` (DevOverlay, layer 100) -> `PanelContainer` (StyleBoxFlat bán trong suốt bo góc) -> `VBoxContainer` -> HeaderBar -> `TabContainer` (`DevPlayerTab`, `DevNpcTab`, `DevWorldTab`). |
| `Scenes/Levels/WorldMap.tscn` | `uid://bu1mkq5a5sqce` | `WorldMap` (Node3D) -> `WorldEnvironment` -> `DirectionalLight3D` -> `MapAutoCollision` -> `Map_25D` (`map_25d.glb`) -> `Map_Surroundings` (`map_surroundings.glb`) -> `Player` -> `IsometricCamera` (CameraFollow) -> `NPC` -> `VoidKillZone` (Area3D) -> `DevOverlay` (CanvasLayer). |
| `Scenes/Levels/TestLevel.tscn` | `uid://c66126flaj42w` | Level kiểm thử mặt sàn phẳng ban đầu. |

### C. 3D Models & Assets
- **Player Model**: `Assets/Models_Exported/character_25d.glb` (Animations: `Idle`, `Walk`, `Jump`, `Attack`).
- **Map Model**: `Assets/Models_Exported/map_25d.glb` (chứa `Terrain_Mesh`, `Staircase_1_Mesh`, `Staircase_2_Mesh`, `Dirt_Path_Main_Mesh`, cây cối, hoa cỏ, mây; nền gạch `SM_Tier2_Pavers` đã mở rộng diện tích gấp 6.8x thành **2.60m x 2.41m x 0.42m** khối đặc monolithic Z=[2.10, 2.52], mép tiếp giáp bắt đầu tại Y=6.99m đè nhẹ 1.4cm lên đỉnh `SM_Staircase_02` đóng kín hoàn toàn khe hở 0 gap; hàng rào gỗ `SM_Fence_Wood_Overlook` gồm 9 cột bao quanh 3 mặt Tây, Bắc, Đông và chừa lối thang Nam rộng 1.24m thông thoáng; cụm núi tím `SM_Mountains_Background` đã xóa 5 chóp chen chúc, chỉ giữ 2 ngọn núi xa thoáng đãng; đã liên kết bộ texture seamless mới: `tex_grass_seamless.png` (`Mat_Grass`), `tex_dirt_seamless.png` (`Mat_Cliff_Dirt`, `Mat_Dirt_Path`), `tex_wood_seamless.png` (`Mat_Wood`), `tex_rock_seamless.png` (`Mat_Stone`, `Mat_Cliff_Rock`); toàn bộ texture được pack trực tiếp vào file blend an toàn `map_25d_fixed.blend` và xuất sang `.glb` chuẩn Godot `export_yup=True`, `export_materials='EXPORT'`).
- **Surroundings Model**: `Assets/Models_Exported/map_surroundings.glb` (UID `uid://sdy3ykn64aus` - Cánh đồng phẳng `Terrain_Plains_Mesh` 84m x 84m được gán vật liệu cỏ xanh tươi mát `Mat_Grass_Plain` liên kết texture chuẩn `tex_grass_seamless.png`, thiết lập chuẩn UV mapping planar projection chiếu đứng `(u, v) = (x/4, y/4)` phủ đều sắc nét; toàn bộ 45 tảng đá `Rock_Mesh_*` được gán vật liệu `Mat_Stone` liên kết texture `tex_rock_seamless.png`; toàn bộ texture được pack trực tiếp vào `map_surroundings.blend` và xuất sang `.glb` chuẩn Godot; bảo tồn nguyên vẹn 63 cây, 45 tảng đá, 36 hoa cúc và duy nhất dãy núi phía Bắc `Mountain_Mesh_North` làm phông nền background xa hùng vĩ).
- **Blender Sources**: `Assets/Blender_Source/` (Vùng cấm ghi đè: `character_25d.blend`, `map_25d.blend` - tuân thủ nguyên vẹn tuyệt đối; File lưu an toàn cải tiến: `map_25d_fixed.blend`; File nguồn môi trường: `map_surroundings.blend`).

### D. Hệ Thống Texture & Vật Liệu Dùng Chung (`Assets/Textures/` & `Assets/Materials_Shared/`)
- **Tra cứu bắt buộc trước khi tạo Model / Scene**: `Assets/Textures/TEXTURE_CATALOG.md`.
- **Tileable Textures (512x512 Seamless 100%)**:
  * `tex_grass_seamless.png` (`uid://drvty0xy4e6jc`): Thảm cỏ xanh mát Stylized `#529934`.
  * `tex_dirt_seamless.png` (`uid://cj7r7nm3t4kwv`): Đất/đường mòn nâu tự nhiên hữu cơ `#8A5C35`.
  * `tex_rock_seamless.png` (`uid://u5lhns2a7ofk`): Vách đá xám phiến Stylized, vết nứt sắc nét.
  * `tex_wood_seamless.png` (`uid://cylrbgem14pnb`): Thớ vân gỗ sồi ấm áp tự nhiên `#A8764A`.
  * `tex_metal_seamless.png` (`uid://bkow053hg3twe`): Mặt kim loại phay xước nhẹ Stylized ánh bạc xám.
- **Grayscale Masks (512x512 Tương phản cao [0.25 - 1.0] để đổi màu tự do bằng `albedo_color`)**:
  * `mask_grass_detail.png` (`uid://dl88hu1ndt3py`): Mặt nạ cụm vi sợi cỏ cách điệu.
  * `mask_dirt_detail.png` (`uid://ctmnogu3s05aq`): Mặt nạ lấm tấm sỏi đất hữu cơ.
  * `mask_rock_detail.png` (`uid://6q8pf6plns63`): Mặt nạ vách đá nứt rạn góc cạnh.
  * `mask_wood_grain.png` (`uid://2smk488wwfdu`): Mặt nạ thớ sợi vân gỗ uốn lượn tự nhiên.
  * `mask_metal_surface.png` (`uid://cn7gdogjuc8ir`): Mặt nạ phay xước kim loại.
- **Palettes (Bảng màu Stylized chuẩn)**:
  * `palette_standard_stylized.png` (`uid://dukjgixx0vrrb`): Bảng màu 256x64 px gồm 16 dải màu chuyển sắc (Cỏ, Rừng, Đất mòn, Đất sét, Đá xám, Núi đá tím, Gỗ sồi, Gỗ sáng, Sắt thép, Vàng đồng, Tông da, Vải đỏ, Vải lam, Mặt nước bọt sóng, Mây trời, Hoa văn ma pháp) cho UV Palette Mapping.
- **Shared Materials (`Assets/Materials_Shared/*.tres` - StandardMaterial3D Godot 4)**:
  * `M_Grass.tres`, `M_Dirt.tres`, `M_Rock.tres`, `M_Wood.tres`, `M_Metal.tres`: Vật liệu cơ bản theo texture seamless.
  * `M_Palette_Stylized.tres`: Vật liệu dùng chung cho toàn bộ model dùng kỹ thuật UV Color Palette.
  * `M_Wood_Fence.tres`: Gỗ sồi tối màu rustic cho hàng rào.
  * `M_Rock_Mountain_Purple.tres`: Núi tím huyền ảo viễn cảnh (biến tấu từ `mask_rock_detail.png` + `Color(0.72, 0.58, 0.84, 1.0)`).
  * `M_Grass_Dry.tres`: Cỏ khô vàng úa mùa thu.
  * `M_Dirt_RedClay.tres`: Đất đỏ bazan / mỏ đất sét.
  * `M_Metal_DarkIron.tres`: Sắt đen rèn thô.
  * `M_Character_Body.tres`: Chuẩn vật liệu thân nhân vật Player / NPC Box (`character_box_texture.png`, Roughness = 0.60).
  * `M_Character_Face.tres`: Chuẩn vật liệu khuôn mặt nhân vật Player (`character_face.png`, Roughness = 0.60).


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


### [2026-11-08] - Triển Khai Hệ Thống Tấn Công Cơ Bản (PlayerCombat & IDamageable) (Sub-agent csharp-coder)
1. **Thiết kế kiến trúc chiến đấu chuẩn Clean Code**:
   - `Scripts/Core/IDamageable.cs` (29 dòng): Giao diện chuẩn cho các thực thể nhận sát thương (`CurrentHealth`, `MaxHealth`, `IsAlive`, `TakeDamage()`).
   - `Scripts/Core/DummyTarget.cs` (56 dòng): Thực thể bia tập đánh triển khai `IDamageable` với hiệu ứng co giãn trúng đòn (`Tween`), trừ máu và tự động hồi máu phục hồi sau thời gian chờ.
   - `Scripts/Player/PlayerCombat.cs` (168 dòng): Điều phối đòn đánh, cấu hình phím tấn công (Chuột trái / Phím J / Nút X Gamepad), kích hoạt `AttackArea` hình cầu phía trước nhân vật, liên kết chặt chẽ với `PlayerAnimation`.
   - `Scripts/Player/PlayerAnimation.cs`: Refactor gọn gàng (144 dòng < 200 dòng), đồng bộ cờ `IsAttacking` để ưu tiên phát animation `Attack` (51 channel tracks) từ `character_25d.glb` và triệt tiêu lean/bobbing thủ tục trong lúc vung kiếm.
2. **An toàn bộ nhớ & Scene Setup**:
   - `AttackArea` được cấu hình trực tiếp trong `Scenes/Characters/Player.tscn` với `SphereShape3D` bán kính 0.9m.
   - Toàn bộ sự kiện `BodyEntered` và `AreaEntered` đều được hủy kết nối `-=` an toàn trong `PlayerCombat._ExitTree()`.
3. **Mở rộng bộ kiểm thử tự động `test_suite.gd`**:
   - Thêm `test_player_combat_system()`: Kiểm tra toàn diện thuộc tính combat mặc định, kích hoạt đòn đánh, trạng thái hitbox, khả năng gây 25 sát thương chuẩn lên `DummyTarget` và hoàn tất đòn đánh.
4. **Biên dịch & Xác thực chất lượng**:
   - `dotnet build`: **Build succeeded. 0 Warning(s), 0 Error(s)**.
   - Godot Headless `test_suite.gd`: **223 / 223 Test cases Passed (100% Pass, 0 Fail)**.
