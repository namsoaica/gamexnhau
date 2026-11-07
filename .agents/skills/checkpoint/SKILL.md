---
name: checkpoint
description: >-
  Use this skill whenever wrapping up a major work session, saving project state, packing context, or preparing for context reset. Chuyên viên đóng gói bối cảnh và lịch sử dự án (Context & State Checkpoint Specialist). Tự động kích hoạt khi kết thúc một chuỗi công việc lớn, khi người dùng yêu cầu lưu trạng thái, đóng gói phiên làm việc, chuẩn bị reset token hoặc chuyển giao phiên mới. Thu thập toàn bộ thay đổi và ghi nhận vào docs/PROJECT_STATE.md và docs/SESSION_HISTORY.md.
---

# Vai Trò: Context & History Manager (Đóng Gói Bối Cảnh)

## 1. Nhiệm Vụ Khi Được Kích Hoạt
Khi được kích hoạt hoặc khi kết thúc phiên làm việc:
1. **Quét toàn bộ thay đổi**:
   - Mã nguồn C# (`Scripts/*.cs`).
   - Scene Godot (`Scenes/**/*.tscn`).
   - Tài nguyên 3D (`Assets/Blender_Source/*.blend`, `Assets/Models_Exported/*.glb`).
   - Texture & Vật liệu (`Assets/Textures/`, `Assets/Materials_Shared/*.tres`, `Assets/Textures/TEXTURE_CATALOG.md`).
2. **Cập nhật bối cảnh dự án (`docs/PROJECT_STATE.md`)**:
   - Ghi nhận chi tiết mọi thay đổi, kiến trúc hệ thống, danh mục tài nguyên UID, trạng thái phím điều khiển và kết quả kiểm thử.
   - Đảm bảo một AI Agent mới đọc file này sẽ hiểu 100% bối cảnh dự án trong 3 giây mà không cần lịch sử chat cũ.
3. **Ghi nhật ký phiên làm việc (`docs/SESSION_HISTORY.md`)**:
   - Ghi nhật ký tóm tắt phiên làm việc: mục tiêu, các file đã thay đổi, kết quả build/test, các quyết định kỹ thuật quan trọng.
4. **Cập nhật danh sách công việc (`docs/TASKS.md`)**:
   - Đánh dấu `[x]` các đầu việc đã hoàn thành và bổ sung các việc cần làm tiếp theo (Backlog).
   - Đồng bộ sang file root `TASKS.md` và `PROJECT_STATE.md`.
5. **Báo cáo bàn giao**: Cung cấp báo cáo 1 dòng trạng thái sẵn sàng để người dùng tiếp tục làm việc.
