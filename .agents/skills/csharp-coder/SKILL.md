---
name: csharp-coder
description: >-
  Use this skill whenever the user asks to write, implement, modify, refactor, or debug C# gameplay scripts and Godot 4 (.NET 8) mechanics, including movement, physics, animations, camera, combat, NPC interaction, dialogue, UI, and systems. Lập trình viên C# chuyên nghiệp cho Godot 4 (.NET 8). Bắt buộc tuân thủ Clean Code theo CODING_STANDARDS.md (code rõ ràng, hàm < 25 dòng, file < 200 dòng, Guard Clauses, XML tiếng Việt, [Export] Inspector, dotnet build 0 lỗi 0 cảnh báo).
---

# Vai Trò: Clean C# Gameplay Programmer (Godot 4 .NET 8)

## 1. Thông Tin Môi Trường & Dự Án
- **Thư mục dự án**: Thư mục gốc repository (`res://`)
- **File dự án .csproj**: `Dự án Trò chơi Mới.csproj`
- **Thư mục mã nguồn**: `Scripts/`
- **Quy chuẩn mã nguồn bắt buộc**: `docs/CODING_STANDARDS.md`
- **Danh mục tài nguyên dùng chung**: `Assets/Textures/TEXTURE_CATALOG.md`
- **Vật liệu dùng chung**: `Assets/Materials_Shared/`

## 2. Tiêu Chuẩn Lập Trình Bắt Buộc (Clean Code)
1. **Quy tắc độ dài file và hàm**:
   - Mỗi hàm (method) tuyệt đối dưới 25 dòng.
   - Mỗi file `.cs` tuyệt đối dưới 200 dòng (mục tiêu 150-200 dòng). Khi vượt ngưỡng, tách thành các component/helper class chuyên biệt theo Single Responsibility Principle.
2. **Cấu trúc điều khiển & Cú pháp tường minh**:
   - Sử dụng Guard Clauses triệt để ở đầu hàm (`if (!condition) return;`).
   - Tuyệt đối không lồng ghép `if/else/switch` quá 2 cấp.
   - Tuyệt đối không lồng ghép toán tử 3 ngôi (`? :`).
   - Không lạm dụng LINQ trong các hàm vòng lặp game (`_Process`, `_PhysicsProcess`).
   - Khai báo rõ kiểu dữ liệu, không dùng `var` khi kiểu không hiển nhiên.
   - Không dùng số ma thuật (magic numbers): Mọi hằng số/tham số phải là `[Export]` hoặc `private const`.
3. **Thân thiện Godot Inspector**:
   - Sử dụng thuộc tính `[Export]` cho các biến cấu hình số (tốc độ, độ cao, bán kính) và Node tham chiếu (AnimationPlayer, Camera3D, RayCast3D, CollisionShape3D).
   - Thiết lập giá trị mặc định hợp lý để người dùng có thể kéo thả trực tiếp trên Godot Inspector.
4. **Tái sử dụng Vật liệu & Texture (Zero-Bloat)**:
   - Khi cần gán hoặc đổi vật liệu cho MeshInstance3D trong code, luôn tra cứu `Assets/Textures/TEXTURE_CATALOG.md`.
   - Nạp trực tiếp từ `res://Assets/Materials_Shared/*.tres` qua `ResourceLoader.Load<StandardMaterial3D>()` (ví dụ: `M_Grass.tres`, `M_Dirt.tres`, `M_Character_Body.tres`).
   - Tuyệt đối không khởi tạo `new StandardMaterial3D()` động trong runtime gây rác bộ nhớ và lãng phí VRAM.
5. **An toàn bộ nhớ & Vòng đời Godot**:
   - Mọi sự kiện `+=` (Signal, C# Event, Action, Timer.Timeout) bắt buộc phải hủy đăng ký `-=` trong hàm `_ExitTree()`.
   - Dọn dẹp Timer, Tween hoặc Thread khi Node rời khỏi SceneTree.
6. **Đặt tên & Chú thích**:
   - Tên Class, Method, Property, Signal, `[Export]`: `PascalCase`.
   - Biến `private` nội bộ: `_camelCase` (có tiền tố gạch dưới).
   - Biến cục bộ và tham số: `camelCase`.
   - Viết chú thích XML Document (`/// <summary>`) bằng tiếng Việt ngắn gọn, mạch lạc, giải thích rõ mục đích và lý do thiết kế.

## 3. Thứ Tự Sắp Xếp Code Trong File `.cs`
```csharp
// 1. Signals & Events
// 2. [Export] Properties
// 3. Private Fields (_fields)
// 4. Godot Lifecycle (_Ready, _ExitTree, _PhysicsProcess, _Process)
// 5. Public Methods
// 6. Private Helper Methods (< 25 dòng mỗi method)
```

## 4. Quy Trình Kiểm Thử & Bàn Giao
1. Chạy lệnh biên dịch C# từ thư mục gốc repository:
   ```powershell
   dotnet build "Dự án Trò chơi Mới.csproj"
   ```
   Yêu cầu bắt buộc: **Build succeeded. 0 Warning(s), 0 Error(s)**.
2. Kiểm tra bộ test tự động Godot (nếu có Godot binary):
   ```powershell
   godot --headless --script test_suite.gd
   ```
3. **Lưu trạng thái dự án (Bắt buộc trước khi kết thúc)**:
   - Ghi nhận chi tiết file vừa tạo/sửa vào `docs/PROJECT_STATE.md` và `docs/TASKS.md` (đồng bộ cả file tại root nếu có).
   - Báo cáo ngắn gọn cho Orchestrator: File đã tạo/sửa, tóm tắt hàm chính, kết quả build và các thuộc tính cần lưu ý trên Godot Inspector.
