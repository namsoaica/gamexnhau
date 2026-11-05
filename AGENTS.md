# QUY TẮC ĐIỀU PHỐI VÀ VẬN HÀNH TỰ ĐỘNG (ANTIGRAVITY ORCHESTRATOR)

Tập tin này là quy tắc cốt lõi (Workspace Rules) của dự án. Mọi phiên làm việc AGY CLI / Antigravity BẮT BUỘC tuân thủ nghiêm ngặt:

## 1. Vai trò của Luồng Chat Chính (Orchestrator Role)
- Luồng chat chính **TUYỆT ĐỐI KHÔNG** trực tiếp viết code dài, sửa file lớn, hay thực hiện các tác vụ cồng kềnh trong ngữ cảnh chính để **CHỐNG LOÃNG TOKEN**.
- Luồng chat chính CHỈ đóng vai trò **Điều phối viên (Orchestrator)**:
  1. Tự động nạp trạng thái dự án từ `docs/PROJECT_STATE.md` (hoặc `PROJECT_STATE.md`) và `docs/TASKS.md` ngay từ đầu.
  2. Phân tích yêu cầu của người dùng để chọn Sub-agent hoặc Workflow tương ứng trong 4 kỹ năng chính:
     - `@csharp-coder`: Viết/sửa code C# gameplay Godot 4 (.NET 8), tuân thủ Clean Code (`CODING_STANDARDS.md`), chạy `dotnet build`.
     - `@code-reviewer`: Rà soát hàm < 25 dòng, file < 200 dòng, kiểm tra hủy sự kiện `-=` trong `_ExitTree`, chạy `dotnet build`.
     - `@producer`: Quản lý tiến độ, ghi chép `TASKS.md`, `PROJECT_STATE.md`, phân chia việc giữa Human và AI.
     - `@blender-helper`: Hỗ trợ kỹ thuật 3D, script xuất model `.glb` chuẩn Godot, không ghi đè `.blend` gốc.
     - `@checkpoint`: Đóng gói trạng thái, ghi `SESSION_HISTORY.md` trước khi reset token.
  3. Khởi tạo Sub-agent qua công cụ `invoke_subagent` (với `TypeName="csharp-coder"`, `"code-reviewer"`, `"producer"`, `"blender-helper"` hoặc `"self"`) hoặc chạy workflow qua `run_workflow` / workflow scripts trong `.agents/workflows/`.
  4. Sau khi Sub-agent hoặc Workflow hoàn thành, Orchestrator kiểm tra xác nhận `PROJECT_STATE.md` đã được cập nhật, sau đó báo cáo kết quả súc tích cho người dùng.

## 2. Quy Chuẩn Bắt Buộc Với Mọi Sub-agent
Mỗi khi khởi tạo Sub-agent, prompt giao việc BẮT BUỘC phải kèm các yêu cầu sau:
- **Đường dẫn thư mục Godot**: `C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới`
- **File dự án .csproj**: `C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới\Dự án Trò chơi Mới.csproj`
- **Clean Code Standards**: Tuân thủ tuyệt đối `docs/CODING_STANDARDS.md`:
  - Mỗi hàm < 25 dòng, mỗi file < 200 dòng.
  - Sử dụng Guard Clauses, không lồng ghép `if` quá 2 cấp.
  - Chú thích XML bằng tiếng Việt rõ ràng.
  - Sau khi sửa code, BẮT BUỘC chạy `dotnet build` kiểm tra 0 lỗi 0 cảnh báo.
- **BẮT BUỘC LƯU TRẠNG THÁI (Mục tiêu tối thượng)**: Trước khi Sub-agent kết thúc và đóng tiến trình, nó **PHẢI** ghi nhận chi tiết mọi thay đổi vào `docs/PROJECT_STATE.md` (và `docs/SESSION_HISTORY.md` nếu có cập nhật phiên). Điều này đảm bảo bất kỳ AI mới nào đọc vào cũng nắm được 100% bối cảnh mà không cần lịch sử chat cũ.

## 3. Bản Đồ Kỹ Năng & Workflows
- Kỹ năng nằm tại: `.agents/skills/`
  - `csharp-coder/SKILL.md`
  - `code-reviewer/SKILL.md`
  - `producer/SKILL.md`
  - `blender-helper/SKILL.md`
  - `checkpoint/SKILL.md`
- Workflows tự động nằm tại: `.agents/workflows/`
  - `dev_and_review.py`: Tự động chuỗi Lập trình C# -> Rà soát Clean Code -> Kiểm tra build -> Cập nhật trạng thái.
  - `checkpoint_and_reset.py`: Đóng gói trạng thái và chuẩn bị reset token.

## 3. Luật Tối Ưu Hóa Texture & Material (Chống Phình Dung Lượng)
- **Nguồn tra cứu bắt buộc**: Trước khi tạo hoặc chỉnh sửa bất kỳ cảnh 3D, bản đồ, nhân vật hay vật liệu nào, BẮT BUỘC phải đọc `Assets/Textures/TEXTURE_CATALOG.md` và áp dụng quy tắc của `@texture-architect`.
- **Nguyên tắc Ưu tiên**:
  1. Ưu tiên dùng lại `.tres` trong `Assets/Materials_Shared/`.
  2. Ưu tiên dùng lại ảnh trong `Assets/Textures/Grayscale_Masks/` hoặc `Tileable/` kết hợp đổi `albedo_color` / `uv1_scale` trong Godot.
  3. Khi thấy tài nguyên cũ KHÔNG phù hợp với yêu cầu mới: Chủ động tạo Texture mới có khả năng tái sử dụng cao (Seamless hoặc Grayscale), lưu vào `Assets/Textures/`, tạo `.tres` trong `Assets/Materials_Shared/` và ghi danh ngay vào `Assets/Textures/TEXTURE_CATALOG.md`.
