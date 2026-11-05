# BẢNG PHÂN CHIA CÔNG VIỆC (TASKS TRACKER)

## 📌 Đã Hoàn Thành (Done)
- [x] **[HUMAN]** Dựng model nhân vật `character_25d.blend` và xuất sang `character_25d.glb`.
- [x] **[HUMAN]** Dựng bản đồ thế giới `map_25d.blend` và xuất sang `map_25d.glb`.
- [x] **[AI - csharp-coder]** Viết `PlayerMovement.cs` (điều khiển vận tốc, gia tốc, nhảy, xoay mặt theo góc camera Isometric).
- [x] **[AI - csharp-coder]** Viết `PlayerAnimation.cs` (tự động phát hoạt ảnh `Idle`, `Walk`, `Jump`).
- [x] **[AI - csharp-coder]** Viết `MapAutoCollision.cs` (tự động tạo va chạm cho địa hình và cầu thang Blender).
- [x] **[AI - csharp-coder]** Viết `CameraFollow.cs` (camera trượt mượt mà theo nhân vật chuẩn góc Isometric).
- [x] **[AI - csharp-coder]** Tạo Scene hoàn chỉnh `Player.tscn` và `WorldMap.tscn`, đồng bộ mã UID và cấu hình Main Scene.
- [x] **[AI - blender-helper]** Mở rộng thế giới 2.5D (84m x 84m): Cánh đồng, 4 dãy núi ranh giới, 45 tảng đá, 70 cây phong/thông, 90 bụi cỏ/hoa cúc (`map_surroundings.glb`).
- [x] **[AI - code-reviewer]** Rà soát toàn diện dự án: 100% Clean Code, Guard Clauses, XML tiếng Việt, kiểm tra rò rỉ bộ nhớ, build 0 lỗi 0 cảnh báo.
- [x] **[AI - producer]** Chuẩn hóa Git & Môi trường cộng tác: Cập nhật `.gitignore`, `.gitattributes`, `.editorconfig` (Allman style, LF/CRLF, binary 3D).
- [x] **[AI - producer]** Dọn dẹp kho Git: Xóa file thừa/lỗi font `1.gitinore.txt`, untrack và dọn các file backup `*.blend1`.
- [x] **[AI - producer]** Thiết lập tài liệu `README.md` chuyên nghiệp tại thư mục gốc và tạo hardlink đồng bộ sang dự án Godot.
- [x] **[AI - producer]** Xây dựng tài liệu `docs/CONTRIBUTING.md` hướng dẫn quy trình cộng tác, branching strategy, PR template và giải quyết xung đột Scene Godot.
- [x] **[AI - producer]** Nâng cấp mục 4 "Quy Trình Cộng Tác Nhóm" trong `README.md`: Hướng dẫn phân quyền cho Trưởng nhóm (Collaborators, bảo vệ nhánh `main`), quy trình thực hành 7 bước kèm khối lệnh bash cho thành viên, và sơ đồ Mermaid trực quan.

---

## 🎯 Việc Cần Làm Tiếp Theo (Backlog / Next Steps)

### Phân Nhóm 1: Gameplay & Lập Trình (AI / Developer)
- [ ] **[AI - csharp-coder]** Lập trình hệ thống đòn đánh / tấn công cơ bản (`PlayerCombat.cs`) sử dụng animation `Attack` có sẵn trong model `character_25d.glb`.
- [ ] **[AI - csharp-coder]** Lập trình thanh máu, thể lực hoặc giao diện UI cơ bản (`Scripts/UI/`).
- [ ] **[AI - csharp-coder]** Lập trình AI cho quái vật tuần tra và tấn công (`Scripts/Enemies/`).
- [ ] **[AI - code-reviewer]** Rà soát Clean Code và kiểm tra build `dotnet build` sau mỗi tính năng mới.

### Phân Nhóm 2: Đồ Họa, Âm Thanh & Cấp Độ (Human / 3D Artist)
- [ ] **[HUMAN]** Dựng model quái vật / kẻ địch mới trong Blender (ví dụ: Slime, Goblin) và xuất sang `Assets/Models_Exported/`.
- [ ] **[HUMAN]** Thiết kế thêm chướng ngại vật / rương báu / cổng dịch chuyển vào map trong Blender.
- [ ] **[HUMAN]** Tìm kiếm hoặc thiết kế âm thanh hiệu ứng (SFX bước chân, SFX chém, BGM nền) đưa vào `Assets/Audio/`.
- [ ] **[HUMAN]** Tinh chỉnh góc camera hoặc ánh sáng DirectionalLight trong Inspector Godot theo sở thích thẩm mỹ.
