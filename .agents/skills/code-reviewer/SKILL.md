---
name: code-reviewer
description: >-
  Use this skill whenever the user asks to review, audit, lint, or check C# code quality in Godot 4, verify Clean Code standards, inspect method length (< 25 lines) and file length (< 200 lines), check memory leaks (event unsubscription -= in _ExitTree), or verify dotnet build results. Chuyên gia rà soát chất lượng mã nguồn C# Godot 4 (.NET 8). Bắt buộc tuân thủ CODING_STANDARDS.md và kiểm tra dotnet build 0 lỗi 0 cảnh báo.
---

# Vai Trò: Clean Code Reviewer & QA (Kiểm Định Chất Lượng C#)

## 1. Mục Tiêu & Phạm Vi Rà Soát
- **Quy chuẩn mã nguồn bắt buộc**: `docs/CODING_STANDARDS.md`
- **File dự án**: `Dự án Trò chơi Mới.csproj`
- **Thư mục mã nguồn cần quét**: `Scripts/` (và các file `.cs` mới được thêm/sửa)

## 2. Tiêu Chí Đánh Giá Nghiêm Ngặt (Rà Soát Tự Động)
1. **Độ dài file & hàm (Giới hạn cứng)**:
   - **Mỗi hàm (Method) < 25 dòng**: Nếu hàm $\ge$ 25 dòng $\rightarrow$ Bắt buộc refactor, tách thành các private helper methods có tên gợi tả rõ hành động.
   - **Mỗi file `.cs` < 200 dòng**: Nếu file $\ge$ 200 dòng $\rightarrow$ Tách nhỏ file thành các class đơn nhiệm theo Single Responsibility Principle.
2. **Cấu trúc & Tính dễ đọc**:
   - **Guard Clauses**: Ưu tiên kiểm tra sớm ở đầu hàm để thoát sớm (`if (!condition) return;`).
   - **Lồng ghép**: Không chấp nhận `if/else/switch/for` lồng ghép quá 2 cấp.
   - **Toán tử 3 ngôi**: Cấm dùng toán tử 3 ngôi lồng nhau (`a ? b : (c ? d : e)`).
   - **Kiểu dữ liệu tường minh**: Cấm dùng `var` khi kiểu dữ liệu bên phải không hiển nhiên.
   - **Không magic numbers**: Mọi tham số phải là `[Export]` hoặc `private const`.
3. **An toàn bộ nhớ Godot & C# (Bắt buộc kiểm tra rò rỉ)**:
   - Mọi sự kiện đăng ký bằng toán tử `+=` (như `BodyEntered += ...`, `ValueChanged += ...`, `Button.Pressed += ...`) **BẮT BUỘC** phải có lệnh hủy `-=` tương ứng trong `_ExitTree()`.
   - Kiểm tra việc dọn dẹp các Timer, Tween, hoặc Thread khi Node bị giải phóng hoặc rời SceneTree.
4. **Tái sử dụng tài nguyên (Zero-Bloat)**:
   - Đảm bảo code không tự khởi tạo `new StandardMaterial3D()` động trong runtime.
   - Nạp vật liệu dùng chung từ `res://Assets/Materials_Shared/*.tres` theo danh mục `Assets/Textures/TEXTURE_CATALOG.md`.
5. **Chú thích XML**:
   - Đảm bảo có chú thích XML `/// <summary>` bằng tiếng Việt trên các Class, Signal và Phương thức quan trọng.

## 3. Quy Trình Thực Hiện & Báo Cáo
1. **Quét mã nguồn**: Đếm số dòng từng file trong `Scripts/` và kiểm tra độ dài từng hàm.
2. **Kiểm tra biên dịch**: Chạy lệnh `dotnet build "Dự án Trò chơi Mới.csproj"` và xác nhận:
   - `0 Warning(s)`
   - `0 Error(s)`
3. **Kiểm tra hồi quy tự động**: Chạy kiểm thử tự động Godot Headless nếu có thay đổi liên quan đến gameplay (`test_suite.gd`).
4. **Cập nhật tài liệu**: Ghi nhận kết quả rà soát chất lượng vào `docs/PROJECT_STATE.md` và `docs/SESSION_HISTORY.md`.
5. **Báo cáo kết quả**: Xuất bảng tóm tắt súc tích:
   - Danh sách file đã quét kèm số dòng.
   - Trạng thái hàm < 25 dòng (Đạt/Cần sửa).
   - Trạng thái hủy sự kiện `-=` trong `_ExitTree()` (Đạt/Thiếu sót).
   - Kết quả `dotnet build` (0 lỗi, 0 cảnh báo).
