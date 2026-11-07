# QUY CHUẨN VIẾT CODE C# DỄ ĐỌC (HUMAN-READABLE CLEAN CODE)

Mọi đoạn code C# do AI viết trong dự án này PHẢI giúp lập trình viên con người đọc hiểu trong 5 giây và tự sửa được dễ dàng:

## 1. Quy tắc chia nhỏ File và Hàm (Chống Spaghetti Code)
- **Mỗi file `.cs` tối đa 150 - 200 dòng**: Mỗi class chỉ đảm nhận ĐÚNG 1 TRÁCH NHIỆM (Single Responsibility).
  - *Sai*: Nhét cả di chuyển, nhảy, chém, máu vào `Player.cs`.
  - *Đúng*: Tách thành `PlayerMovement.cs`, `PlayerCombat.cs`, `HealthComponent.cs`.
- **Mỗi hàm (Method) tối đa 25 dòng**: Nếu một hàm dài hơn, hãy tách các bước xử lý thành các hàm phụ có tên gợi tả rõ hành động (ví dụ: `CalculateJumpVelocity()`, `ApplyGravity(float delta)`).
- **Không lồng ghép quá 2 cấp (Max 2 Nesting Levels)**: Không viết `if` lồng trong `for` rồi lại lồng `if` bên trong. Hãy dùng câu lệnh kiểm tra sớm (**Guard Clauses** - `if (!IsOnFloor()) return;`) ở ngay đầu hàm.

## 2. Quy tắc Cú pháp Tường minh (Chống "Code Thông Minh Giả Tạo")
- **CẤM dùng toán tử 3 ngôi lồng nhau**: Tuyệt đối không viết `a ? b : (c ? d : e)`. Hãy viết `if - else` rõ ràng.
- **CẤM viết chuỗi LINQ phức tạp trong vòng lặp Game**: Trong `_Process` và `_PhysicsProcess`, dùng vòng lặp `foreach` hoặc `for` truyền thống để dễ đọc, dễ đặt Breakpoint debug và không gây rác bộ nhớ (GC).
- **CẤM dùng kiểu `var` khi kiểu dữ liệu không hiển nhiên**:
  - *Sai*: `var target = GetClosestEnemy();` (Người đọc không biết `target` thuộc kiểu gì).
  - *Đúng*: `EnemyController target = GetClosestEnemy();`
- **CẤM số ma thuật (No Magic Numbers)**: Mọi thông số (tốc độ, sát thương, thời gian hồi chiêu) phải khai báo thành biến `[Export]` hoặc hằng số `private const float` có tên rõ nghĩa.

## 3. Quy ước Đặt tên & Cấu trúc trong 1 File `.cs`
- Biến `[Export]` và `public`: Dùng `PascalCase` (ví dụ: `[Export] public float MoveSpeed { get; set; } = 5.0f;`).
- Biến `private` nội bộ: Có dấu gạch dưới ở đầu `_camelCase` (ví dụ: `private float _currentStamina;`).
- Tên hàm: Phải bắt đầu bằng Động từ (`UpdateMovement`, `TakeDamage`, `TryExecuteDash`).
- **Thứ tự sắp xếp trong mọi file `.cs` phải thống nhất từ trên xuống dưới**:
  1. `[Signal]` / `event` (Sự kiện)
  2. `[Export]` Properties (Thông số tinh chỉnh trên Godot Inspector)
  3. Biến `private` nội bộ (`_fields`)
  4. Hàm vòng đời Godot (`_Ready`, `_ExitTree`, `_PhysicsProcess`)
  5. Các hàm `public` (Giao tiếp với bên ngoài)
  6. Các hàm `private` (Xử lý chi tiết bên trong)

## 4. Quy tắc Chú thích (Comments) cho Người Đọc
- Mọi Class và Hàm quan trọng đều phải có chú thích XML `/// <summary>` ngắn gọn bằng **tiếng Việt** giải thích mục đích của hàm.
- Không chú thích những điều hiển nhiên (như `// Tăng i lên 1`), chỉ chú thích **lý do tại sao** hoặc giải thích công thức toán học/vật lý 3D.
