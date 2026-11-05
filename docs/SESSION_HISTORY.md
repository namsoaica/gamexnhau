# LỊCH SỬ PHIÊN LÀM VIỆC (SESSION HISTORY)

## Phiên làm việc: 2026-11-05
- **Khởi tạo nhân vật**: Viết `PlayerMovement.cs` và `PlayerAnimation.cs` theo Clean Code.
- **Tích hợp bản đồ**: Đưa `map_25d.glb` vào `Assets/Models_Exported/`, viết `MapAutoCollision.cs`, `CameraFollow.cs`.
- **Sửa lỗi UID**: Đồng bộ toàn bộ mã UID giữa `Player.tscn`, `WorldMap.tscn`, `TestLevel.tscn` để lưu Scene 100% không bị lỗi đỏ.
- **Khởi tạo tài liệu**: Tạo `docs/PROJECT_STATE.md`, `docs/TASKS.md`, `docs/SESSION_HISTORY.md`.

## Phiên làm việc: 2026-11-06
- **Thiết lập hệ thống Sub-agent tự động (.agents/)**:
  - Chuẩn hóa 5 kỹ năng Sub-agent tại `.agents/skills/`: `csharp-coder`, `code-reviewer`, `producer`, `blender-helper`, `checkpoint`.
  - Thiết lập quy tắc trong `AGENTS.md` & `GEMINI.md`: Luồng chính chỉ điều phối (Orchestrator), cấm tự đọc code/build làm loãng token. Mọi việc đều ủy thác cho Sub-agent con tự đọc `docs/PROJECT_STATE.md`, tự build, tự ghi nhật ký và tự đóng tiến trình để giải phóng 100% token nháp.
  - Xây dựng 2 kịch bản workflow tự động tại `.agents/workflows/`: `dev_and_review.py` và `checkpoint_and_reset.py`.
  - Liên kết không gian làm việc kép giữa `C:\xnhaugame` và `dự-án-trò-chơi-mới`, đảm bảo quy tắc luôn tự động kích hoạt dù mở AGY CLI ở bất kỳ thư mục nào.
  - Định nghĩa sẵn sàng 5 Sub-agent types qua `define_subagent` để luồng chính có thể điều phối tức thì qua `invoke_subagent`.
- **Mở rộng thế giới 2.5D Isometric (`map_surroundings.glb`)**:
  - Dùng Blender 5.4 CLI tạo `Assets/Blender_Source/map_surroundings.blend` và xuất `Assets/Models_Exported/map_surroundings.glb` (cánh đồng 84x84m, 4 dãy núi bao quanh, 45 tảng đá, 70 cây, 90 cụm hoa). Tuyệt đối không ghi đè model gốc.
  - Cập nhật `MapAutoCollision.cs` tự động tạo va chạm cho núi đá và cánh đồng.
  - Tích hợp vào `WorldMap.tscn`, kiểm thử vật lý di chuyển và va chạm trơn tru.
- **Rà soát chất lượng toàn diện (QA Code Review)**:
  - 100% file C# < 200 dòng, 100% hàm < 25 dòng, áp dụng Guard Clauses, không lồng if quá 2 cấp.
  - Bổ sung chú thích XML tiếng Việt cho toàn bộ hàm vòng đời Godot.
  - Kiểm tra an toàn bộ nhớ (không có delegate/event listener treo).
  - Khớp 100% UID tài nguyên giữa scenes và assets.
  - Kiểm tra `dotnet build`: Đạt 0 Warning(s), 0 Error(s).
- **Chuẩn hóa hạ tầng cộng tác nhóm & Thiết lập tài liệu (Multi-developer Setup)**:
  - Hoàn thiện `.gitignore` đầy đủ cho Godot 4 C# (.NET 8), Visual Studio, VSCode, Rider, Blender backup `*.blend*`, OS artifacts.
  - Xóa file lỗi font thừa `1.gitinore.txt`, untrack và xóa các file backup `character_25d.blend1` khỏi Git tracking.
  - Chuẩn hóa `.gitattributes`: thiết lập `* text=auto eol=lf`, `*.cs text diff=csharp eol=crlf`, phân định file text diff cho Godot và đánh dấu nhị phân `binary` cho tài nguyên 3D/hình ảnh/âm thanh.
  - Hoàn thiện `.editorconfig`: thống nhất định dạng Allman style, thụt lề 4 space, kiểm soát var và quy chuẩn `_camelCase`.
  - Tạo `README.md` chuyên nghiệp tại thư mục gốc và tạo hardlink đồng bộ sang thư mục dự án Godot.
  - Xây dựng `docs/CONTRIBUTING.md` hướng dẫn chi tiết quy trình nhận việc, branching strategy, Conventional Commits, chiến lược chống xung đột Scene trong Godot và mẫu PR Template.
  - Bổ sung hướng dẫn chi tiết cộng tác nhóm trên GitHub vào mục 4 của `README.md`: Thiết lập quyền Trưởng nhóm (Collaborators, bảo vệ nhánh `main`), quy trình 7 bước thực hành với lệnh bash copy-paste trực tiếp, sơ đồ Mermaid luồng phối hợp nhóm.
  - Kiểm tra biên dịch `dotnet build`: Đạt 0 Warning(s), 0 Error(s).


