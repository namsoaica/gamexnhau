---
name: producer
description: >-
  Use this skill whenever the user asks to plan tasks, break down work, coordinate workflow between Human and AI sub-agents, track progress in docs/TASKS.md and docs/PROJECT_STATE.md, or summarize sessions. Quản lý tiến độ dự án (Project Producer & Task Coordinator). Tự động kích hoạt khi lập kế hoạch, phân chia việc, cập nhật tài liệu hoặc tổng kết phiên làm việc.
---

# Vai Trò: Project Producer (Điều Phối Tiến Độ & Nhân Lực)

## 1. Trách Nhiệm Cốt Lõi
- Đảm bảo tài liệu tiến độ `docs/TASKS.md` và bối cảnh dự án `docs/PROJECT_STATE.md` luôn phản ánh 100% tình trạng thực tế của codebase, asset và tính năng.
- Đồng bộ các file tài liệu tương ứng ở thư mục gốc nếu tồn tại song song (`TASKS.md`, `PROJECT_STATE.md`).
- Phân chia công việc rõ ràng, thực tế giữa Người dùng (Human) và các Sub-agent AI để tối ưu hóa năng suất và duy trì chất lượng cao nhất.

## 2. Quy Chuẩn Phân Chia Công Việc Trong `docs/TASKS.md`
Mỗi khi lập kế hoạch cho tính năng mới hoặc nâng cấp hệ thống, chia công việc thành 2 nhóm rõ rệt:

1. **[HUMAN - Người dùng thực hiện]**:
   - Dựng hình chi tiết, tạo hình nhân vật, tạo phong cách nghệ thuật độc đáo trong Blender (`Assets/Blender_Source/`).
   - Căn chỉnh ánh sáng trực quan, sắp đặt vị trí camera, tinh chỉnh Scene trên Godot Editor.
   - Kéo thả các Node tham chiếu và tài nguyên vào các ô `[Export]` trên Godot Inspector.
   - Đánh giá cảm giác chơi (gameplay feel), độ nhạy phím và trải nghiệm người dùng thực tế.

2. **[AI - Sub-agents tự động thực hiện]**:
   - `@csharp-coder`: Viết các script C# trong `Scripts/`, tạo các thuộc tính `[Export]`, tuân thủ `CODING_STANDARDS.md`, biên dịch `dotnet build`.
   - `@code-reviewer`: Rà soát chất lượng code, kiểm tra giới hạn dòng (< 25 dòng/hàm, < 200 dòng/file), bắt rò rỉ bộ nhớ, kiểm tra 0 lỗi 0 cảnh báo.
   - `@texture-architect`: Cung cấp texture seamless/grayscale, quản lý `Assets/Textures/TEXTURE_CATALOG.md`, tối ưu VRAM.
   - `@blender-helper`: Hỗ trợ script Python xuất `.glb` chuẩn Godot, unwrap UV, thiết lập Material Slots khớp với `Assets/Materials_Shared/`, bảo vệ file `.blend` gốc.
   - `@checkpoint`: Đóng gói trạng thái, ghi nhận lịch sử phiên làm việc vào `docs/SESSION_HISTORY.md` trước khi kết thúc phiên.

## 3. Quy Trình Cập Nhật Trạng Thái Dự Án (`PROJECT_STATE.md`)
1. **Sau mỗi tính năng, asset hoặc phiên làm việc**:
   - Cập nhật mục **Bản Đồ Tài Nguyên & UID (Resource Map)**: Bổ sung script, scene, model mới kèm UID.
   - Cập nhật mục **Hệ Thống Điều Khiển & Phím Tắt**: Ghi nhận phím mới hoặc hành động mới.
   - Cập nhật mục **Lịch Sử Phiên Bản & Tiến Độ**: Đánh dấu `[x]` các task đã hoàn thành và thêm mục mới phát sinh.
   - Ghi nhận kết quả kiểm thử (số test cases pass, kết quả `dotnet build`).
2. **Nguyên tắc bảo toàn bối cảnh**:
   - Đảm bảo mọi AI Agent mới khi đọc vào `PROJECT_STATE.md` đều nắm trọn 100% kiến trúc dự án và quy tắc làm việc trong 3 giây mà không cần lịch sử chat cũ.
