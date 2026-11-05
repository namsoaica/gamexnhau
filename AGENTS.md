# NỘI QUY DỰ ÁN GAME (HUMAN-LED CO-OP STUDIO)

Dự án này do **Người dùng (Lead Developer & 3D Artist)** trực tiếp chỉ đạo và cùng tham gia phát triển với các AI Agent cục bộ trong `.gemini/skills/`.

## 1. Vùng Bảo Vệ (Protected Zones - Cấm AI tự ý ghi đè)
- **`Assets/Blender_Source/`**: Chứa file `.blend` do người dùng tự dựng. AI tuyệt đối không chỉnh sửa hoặc xóa.
- **Cây thư mục gốc**: Đã được người dùng quy hoạch cố định. AI chỉ tạo file đúng vào các thư mục con hiện có trong `Scripts/` và `Scenes/`.
- **Các file `.tscn` do người dùng tạo**: Khi người dùng đã tự sắp xếp Node trong Godot Editor, AI chỉ được đọc để lấy đường dẫn Node hoặc gắn script `.cs`, không tự ý xóa Node của người dùng.

## 2. Luật Bắt Buộc Khi Viết Code C#
- **Đọc `docs/CODING_STANDARDS.md` trước khi viết bất kỳ dòng code nào.**
- Code phải sạch, dễ đọc như người viết, chia hàm nhỏ dưới 25 dòng, file dưới 200 dòng, có chú thích `/// <summary>` bằng tiếng Việt.
- Luôn chạy `dotnet build` để kiểm tra biên dịch 0 lỗi sau khi viết code.
