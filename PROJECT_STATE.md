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
| `Scripts/Player/PlayerMovement.cs` | `uid://bat3uly7f4c8o` | Vật lý di chuyển, gia tốc, trọng lực, nhảy, xoay mặt theo góc nhìn Camera Isometric. |
| `Scripts/Player/PlayerAnimation.cs` | `uid://dic3neyglppy0` | Đồng bộ hoạt ảnh (`Idle`, `Walk`, `Jump`) theo trạng thái sàn và vận tốc của Player. |
| `Scripts/Core/CameraFollow.cs` | `uid://c7kqoh0ntwdus` | Camera bám theo Player mượt mà và tự động `LookAt` vào Player chuẩn góc Isometric. |
| `Scripts/Core/MapAutoCollision.cs` | `uid://7j1cd1f4exa7` | Tự động tạo `Trimesh Collision` cho các mesh địa hình (`Terrain`, `Staircase`, `Path`, `Paver`), chướng ngại vật (`Rock`, `Fence`) và ranh giới núi (`Mountain`, `Cliff`). |

### B. Scenes (`Scenes/`)
| File Scene | UID | Cấu Trúc Node Chính |
| :--- | :--- | :--- |
| `Scenes/Characters/Player.tscn` | `uid://ciy0uaygbkns3` | `CharacterBody3D` (PlayerMovement) -> `CollisionShape3D` (Capsule 0.4x1.8m) -> `CharacterModel` (`character_25d.glb`) -> `PlayerAnimation`. |
| `Scenes/Levels/WorldMap.tscn` | `uid://bu1mkq5a5sqce` | `WorldMap` (Node3D) -> `WorldEnvironment` (Sky hoạt hình) -> `DirectionalLight3D` (Mặt trời) -> `MapAutoCollision` -> `Map_25D` (`map_25d.glb`) -> `Map_Surroundings` (`map_surroundings.glb`) -> `Player` -> `IsometricCamera` (CameraFollow). |
| `Scenes/Levels/TestLevel.tscn` | `uid://c66126flaj42w` | Level kiểm thử mặt sàn phẳng ban đầu. |

### C. 3D Models & Assets
- **Player Model**: `Assets/Models_Exported/character_25d.glb` (Animations: `Idle`, `Walk`, `Jump`, `Attack`).
- **Map Model**: `Assets/Models_Exported/map_25d.glb` (chứa `Terrain_Mesh`, `Staircase_1_Mesh`, `Staircase_2_Mesh`, `Dirt_Path_Main_Mesh`, cây cối, hoa cỏ, mây).
- **Surroundings Model**: `Assets/Models_Exported/map_surroundings.glb` (UID `uid://sdy3ykn64aus` - Cánh đồng `Terrain_Plains_Mesh`, 4 dãy núi bao quanh `Mountain_Mesh_*`, 45 tảng đá `Rock_Mesh_*`, 70 cây thông/phong `Tree_Mesh_*`, thảm hoa cỏ).
- **Blender Sources**: `Assets/Blender_Source/` (Vùng cấm ghi đè: `character_25d.blend`, `map_25d.blend`; File nguồn mới: `map_surroundings.blend`).

---

## 3. Hệ Thống Điều Khiển (Input Controls)
- **Di chuyển**: Phím `W / A / S / D` hoặc phím mũi tên `↑ / ← / ↓ / →` (được tính toán di chuyển tương đối theo góc nhìn màn hình Camera Isometric).
- **Nhảy**: Phím `Space`.

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
   - Luồng chat chính đóng vai trò Orchestrator: tự động nạp trạng thái, phân tích nhiệm vụ, ủy thác cho Sub-agent/Workflow tương ứng và xác nhận lưu trạng thái vào `PROJECT_STATE.md` sau mỗi lượt.

### [2026-11-06] - Mở Rộng Thế Giới Xung Quanh (Surrounding Environment 2.5D)
1. **Thiết kế & Xuất Mô Hình Blender (`map_surroundings.glb`)**:
   - Chạy script Python (`generate_surroundings.py`) ngầm với Blender 5.4 CLI, tuyệt đối không ghi đè file nguồn `map_25d.blend`.
   - Tạo file nguồn Blender mới `Assets/Blender_Source/map_surroundings.blend` và xuất `Assets/Models_Exported/map_surroundings.glb` chuẩn tọa độ Godot (-Z forward, Y up).
   - Quy mô mở rộng thế giới 84m x 84m:
     + Cánh đồng cỏ bát ngát `Terrain_Plains_Mesh` khoét lỗ khít khao tại cao độ Z=0 với mép đảo trung tâm, tích hợp chân đế skirt chống hở đáy.
     + 4 Dãy núi low-poly hùng vĩ bao quanh 4 viền ngoài (`Mountain_Mesh_North`, `Mountain_Mesh_South`, `Mountain_Mesh_West`, `Mountain_Mesh_East`) cao 8-15m làm ranh giới tự nhiên bao trọn bản đồ.
     + 45 Khối đá tảng `Rock_Mesh_*` rải rác tạo điểm nhấn phong cảnh.
     + 70 Cây cối stylized (`Tree_Mesh_Pine_*`, `Tree_Mesh_Deciduous_*`) và 90 cụm hoa cúc, thảm cỏ (`Grass_Clump_Mesh_*`, `Daisy_Mesh_*`).
     + Đồng bộ 100% bảng màu và vật liệu với map gốc: `Mat_Grass`, `Mat_Stone`, `Mat_Mountain_Purple`, `Mat_Mountain_Dark`.
2. **Nâng Cấp Vật Lý Va Chạm (`MapAutoCollision.cs`)**:
   - Cập nhật hàm `IsWalkableSurface` nhận diện thêm `rock`, `mountain`, `cliff`.
   - Tự động sinh `Trimesh Collision` (ConcavePolygonShape3D) cho cánh đồng phẳng và các vật cản núi/đá để Player không rơi khỏi map và không đi xuyên vật thể.
   - Tuân thủ 100% `CODING_STANDARDS.md` (hàm < 25 dòng, file < 200 dòng, build 0 lỗi 0 cảnh báo).
3. **Tích hợp Scene `WorldMap.tscn`**:
   - Thêm Instance `Map_Surroundings` (`map_surroundings.glb`, UID `uid://sdy3ykn64aus`).
   - Kiểm thử thực tế trong Godot Engine: toàn bộ mesh địa hình, đá tảng và dãy núi đều được tự động sinh va chạm vật lý hoàn chỉnh.

### [2026-11-06] - Đánh Giá & Kiểm Định Chất Lượng Toàn Diện (QA Review)
1. **Kiểm tra Chuẩn Code (Clean Code & Coding Standards)**:
   - Toàn bộ 4 file C# trong `Scripts/` đều tuân thủ tuyệt đối quy định:
     + `CameraFollow.cs`: 40 dòng (< 200 dòng), hàm dài nhất 11 dòng (< 25 dòng).
     + `MapAutoCollision.cs`: 82 dòng (< 200 dòng), hàm dài nhất 14 dòng (< 25 dòng).
     + `PlayerAnimation.cs`: 96 dòng (< 200 dòng), hàm dài nhất 19 dòng (< 25 dòng).
     + `PlayerMovement.cs`: 167 dòng (< 200 dòng), hàm dài nhất 18 dòng (< 25 dòng).
   - Kiểm tra lồng ghép: 100% không vượt quá 2 cấp độ lồng, áp dụng triệt để Guard Clauses.
   - Bổ sung và đồng bộ 100% chú thích XML `/// <summary>` bằng tiếng Việt cho toàn bộ các hàm vòng đời Godot (`_Ready`, `_PhysicsProcess`, `_Process`).
2. **Kiểm tra An toàn Bộ nhớ & Vòng đời**:
   - Rà soát toàn bộ các sự kiện `+=`, không phát hiện listener treo hoặc rò rỉ bộ nhớ sự kiện C#.
3. **Kiểm tra Tính toàn vẹn Tài nguyên & Build**:
   - Khớp 100% các mã định danh UID giữa các Scene (`Player.tscn`, `WorldMap.tscn`, `TestLevel.tscn`) và các tài nguyên mô hình 3D/Scripts.
   - Chạy lệnh `dotnet build`: Đạt 0 Warning(s), 0 Error(s).

### [2026-11-06] - Chuẩn Hóa Hạ Tầng Cộng Tác Nhóm & Tài Liệu (Multi-developer Setup)
1. **Chuẩn hóa Git & Môi trường Đa Lập Trình Viên**:
   - **Cập nhật `.gitignore`**: Bỏ qua toàn bộ cache Godot (`.godot/`, `.mono/`), bản build xuất ra (`build/`, `*.pck`, `*.apk`), artifact C# (`bin/`, `obj/`, `*.suo`, `*.user`), thư mục IDE (`.vs/`, `.vscode/`, `.idea/`), file backup Blender (`*.blend1`, `*.blend2`, v.v.), và file rác hệ điều hành (`Thumbs.db`, `.DS_Store`).
   - **Xóa & Untrack file thừa**: Xóa file lỗi font `1.gitinore.txt`, untrack và xóa các file backup `*.blend1` khỏi kho lưu trữ Git.
   - **Cập nhật `.gitattributes`**: Chuẩn hóa `* text=auto eol=lf`, `*.cs text diff=csharp eol=crlf`, phân loại rõ file text diff Godot (`.tscn`, `.tres`, `.godot`) và đánh dấu nhị phân `binary` cho toàn bộ asset 3D/hình ảnh/âm thanh (`.blend`, `.glb`, `.png`, `.wav`).
   - **Cập nhật `.editorconfig`**: Định dạng Allman Style cho C#, 4 spaces indent, quy chuẩn đặt tên biến `_camelCase` và giới hạn dùng `var`.
2. **Xây dựng Tài liệu Hướng dẫn Chuyên Nghiệp**:
   - **Tạo `README.md`**: Tổng quan kiến trúc game 2.5D Isometric, hướng dẫn cài đặt Quick Start (.NET 8 SDK, Godot Mono), quy trình Git phân nhánh (`main`, `develop`, `feature/*`), Conventional Commits, chiến lược chống xung đột Scene trong Godot, và giới thiệu hệ thống AI Orchestrator.
   - **Nâng cấp mục 4 `README.md` (Quy Trình Cộng Tác Nhóm)**: Bổ sung liên kết repository chính thức `https://github.com/namsoaica/gamexnhau`, hướng dẫn thiết lập phân quyền cho Repo Owner (thêm Collaborators, bật Branch Protection cho nhánh `main`), quy trình 7 bước thực hành chuẩn cho thành viên với đầy đủ khối lệnh bash copy-paste, và sơ đồ Mermaid trực quan luồng phối hợp nhóm.
   - **Tạo `docs/CONTRIBUTING.md`**: Hướng dẫn chi tiết từng bước cho thành viên mới, checklist kiểm thử trước khi commit, quy chuẩn đóng góp 3D/Audio, và mẫu Pull Request Template.
   - **Đồng bộ liên kết**: Tạo hardlink đồng bộ `README.md`, `.gitignore`, `.gitattributes`, `.editorconfig` giữa thư mục gốc và thư mục dự án Godot.
3. **Xác thực Hệ Thống**:
   - Kiểm tra biên dịch `dotnet build`: Đạt 0 Warning(s), 0 Error(s).



