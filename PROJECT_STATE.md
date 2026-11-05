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
| `Scripts/Player/PlayerMovement.cs` | `uid://bat3uly7f4c8o` | Vật lý di chuyển, gia tốc, trọng lực, Coyote Time (0.15s), Jump Buffer (0.15s), xoay mặt theo góc nhìn Camera Isometric chuẩn hóa `Input.GetVector`, chống moonwalk, dịch chuyển tức thời `TeleportTo`. |
| `Scripts/Player/PlayerAnimation.cs` | `uid://dic3neyglppy0` | Đồng bộ hoạt ảnh (`Idle`, `Walk`, `Jump`); tự động nhận diện track AnimationPlayer, tự chuyển sang Procedural Lean/Bobbing khi chưa có clip. |
| `Scripts/Player/PlayerInteractor.cs` | `uid://cwt2g2l1041b` | Quản lý việc dò tìm và tương tác với các thực thể `IInteractable` gần nhất trong bán kính `ScanRadius`, phát signal cho UI, an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Core/IInteractable.cs` | `uid://cb38i1wmsj35b` | Interface chuẩn định nghĩa thực thể tương tác (`PromptText`, `CanInteract()`, `Interact()`, `OnFocusGained()`, `OnFocusLost()`). |
| `Scripts/Core/InteractableArea.cs` | `uid://b45c22501e5v` | Area3D dùng chung cho tương tác, tự động sinh hình cầu va chạm `SphereShape3D`, chuyển tiếp tương tác cho node cha. |
| `Scripts/Core/SimpleNpc.cs` | `uid://cqj18q3f63k1` | Điều khiển NPC mẫu: hiển thị `Label3D` billboard thoại trên đầu khi tương tác, tự ẩn sau 4 giây, xoay vòng câu thoại, an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Core/VoidKillZone.cs` | `uid://dwpklcl7pp863` | Area3D vực sâu bao phủ bản đồ, tự ghi nhớ vị trí ban đầu và hồi sinh Player khi rơi ra ngoài, triệt tiêu vận tốc rơi, an toàn bộ nhớ trong `_ExitTree`. |
| `Scripts/Core/CameraFollow.cs` | `uid://c7kqoh0ntwdus` | Camera bám theo Player mượt mà và tự động `LookAt` vào Player chuẩn góc Isometric. |
| `Scripts/Core/MapAutoCollision.cs` | `uid://7j1cd1f4exa7` | Tự động tạo `Trimesh Collision` cho các mesh địa hình (`Terrain`, `Staircase`, `Path`, `Paver`), chướng ngại vật (`Rock`, `Fence`) và ranh giới núi (`Mountain`, `Cliff`). |

### B. Scenes (`Scenes/`)
| File Scene | UID | Cấu Trúc Node Chính |
| :--- | :--- | :--- |
| `Scenes/Characters/Player.tscn` | `uid://ciy0uaygbkns3` | `CharacterBody3D` (PlayerMovement) -> `CollisionShape3D` (Capsule 0.4x1.8m) -> `CharacterModel` (`character_25d.glb`) -> `PlayerAnimation` -> `PlayerInteractor` (Area3D). |
| `Scenes/Characters/NPC.tscn` | (PackedScene) | `Node3D` (SimpleNpc) -> `CharacterModel` (`character_25d.glb`) -> `InteractableArea` (Area3D). |
| `Scenes/Levels/WorldMap.tscn` | `uid://bu1mkq5a5sqce` | `WorldMap` (Node3D) -> `WorldEnvironment` -> `DirectionalLight3D` -> `MapAutoCollision` -> `Map_25D` (`map_25d.glb`) -> `Map_Surroundings` (`map_surroundings.glb`) -> `Player` -> `IsometricCamera` (CameraFollow) -> `NPC` -> `VoidKillZone` (Area3D). |
| `Scenes/Levels/TestLevel.tscn` | `uid://c66126flaj42w` | Level kiểm thử mặt sàn phẳng ban đầu. |

### C. 3D Models & Assets
- **Player Model**: `Assets/Models_Exported/character_25d.glb` (Animations: `Idle`, `Walk`, `Jump`, `Attack`).
- **Map Model**: `Assets/Models_Exported/map_25d.glb` (chứa `Terrain_Mesh`, `Staircase_1_Mesh`, `Staircase_2_Mesh`, `Dirt_Path_Main_Mesh`, cây cối, hoa cỏ, mây).
- **Surroundings Model**: `Assets/Models_Exported/map_surroundings.glb` (UID `uid://sdy3ykn64aus` - Cánh đồng `Terrain_Plains_Mesh`, 4 dãy núi bao quanh `Mountain_Mesh_*`, 45 tảng đá `Rock_Mesh_*`, 70 cây thông/phong `Tree_Mesh_*`, thảm hoa cỏ).
- **Blender Sources**: `Assets/Blender_Source/` (Vùng cấm ghi đè: `character_25d.blend`, `map_25d.blend`; File nguồn mới: `map_surroundings.blend`).

---

## 3. Hệ Thống Điều Khiển & Physics Layers (Input & Layers)
- **Di chuyển**: Phím `W / A / S / D` hoặc phím mũi tên `↑ / ← / ↓ / →` (chuẩn hóa `Input.GetVector`, tính toán tương đối theo góc nhìn Camera Isometric).
- **Nhảy**: Phím `Space` (có hỗ trợ Coyote Time 0.15s và Jump Buffer 0.15s).
- **Tương tác**: Phím `E` (Action name `"interact"`).
- **3D Physics Layers**:
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
