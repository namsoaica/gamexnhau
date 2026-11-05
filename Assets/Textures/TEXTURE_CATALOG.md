# DANH MỤC TEXTURE & MATERIAL DÙNG CHUNG (TEXTURE CATALOG)

> **QUY TẮC BẮT BUỘC CHO AI**: Luôn đọc file này TRƯỚC KHI tạo model, tạo Scene hoặc viết script sinh tài nguyên. Nếu dùng lại hoặc tạo mới bất kỳ file nào, PHẢI cập nhật vào bảng dưới đây.
> 
> **Nguyên tắc tiết kiệm VRAM**:
> 1. **Dùng lại 100%**: Ưu tiên gắn file `.tres` sẵn có trong `Assets/Materials_Shared/`.
> 2. **Tạo vật liệu mới từ ảnh cũ (chỉ 1KB)**: Sử dụng các ảnh trong `Grayscale_Masks/` kết hợp đổi `albedo_color` trong file `.tres` mới.
> 3. **Tạo ảnh mới**: Khi bắt buộc, phải tạo ảnh chuẩn lũy thừa 2 (64x64, 256x256, 512x512) và Seamless tuần hoàn.

---

## 1. Bảng Màu & Vân Xám Đổi Màu (Palettes & Grayscale Masks - Ưu tiên số 1)
*Độ tương phản cao [0.25 - 1.0], nhân trực tiếp với `albedo_color` trong Godot để tạo vô số biến thể màu mà không tốn dung lượng ảnh mới.*

| Tên File | Đường dẫn Godot (`res://`) | Độ phân giải | Đặc điểm & Cách tái sử dụng |
| :--- | :--- | :--- | :--- |
| `palette_standard_stylized.png` | `res://Assets/Textures/Palettes/palette_standard_stylized.png` | 256x64 | Bảng màu Stylized chuẩn gồm 16 dải màu chuyển sắc (Cỏ, Rừng, Đất mòn, Đất sét, Đá xám, Núi đá tím, Gỗ sồi, Gỗ sáng, Sắt thép, Vàng đồng, Tông da, Vải đỏ, Vải lam, Mặt nước bọt sóng, Mây trời, Hoa văn ma pháp). Dùng cho kỹ thuật Palette UV Mapping. |
| `mask_grass_detail.png` | `res://Assets/Textures/Grayscale_Masks/mask_grass_detail.png` | 512x512 | Mặt nạ cụm cỏ cách điệu trắng đen. Pha với `albedo_color` xanh để làm cỏ non, vàng úa làm cỏ khô, tím/xanh ngọc cho thảo nguyên huyền ảo. |
| `mask_dirt_detail.png` | `res://Assets/Textures/Grayscale_Masks/mask_dirt_detail.png` | 512x512 | Mặt nạ lấm tấm sỏi đất hữu cơ. Pha với màu nâu nhạt làm đường cát, đỏ nâu làm đất bazan, xám tối làm bùn lầy. |
| `mask_rock_detail.png` | `res://Assets/Textures/Grayscale_Masks/mask_rock_detail.png` | 512x512 | Mặt nạ vách đá nứt rạn góc cạnh Stylized. Pha màu tím tạo núi tím viễn cảnh (`M_Rock_Mountain_Purple`), pha xám tạo tảng đá sỏi, pha vàng đất làm sa thạch. |
| `mask_wood_grain.png` | `res://Assets/Textures/Grayscale_Masks/mask_wood_grain.png` | 512x512 | Mặt nạ thớ sợi vân gỗ uốn lượn tự nhiên. Pha màu nâu ấm làm gỗ sồi, màu be nhạt làm gỗ thông, màu đỏ sẫm làm gỗ lim. |
| `mask_metal_surface.png` | `res://Assets/Textures/Grayscale_Masks/mask_metal_surface.png` | 512x512 | Mặt nạ xước phay kim loại ánh bạc. Pha xám đen làm sắt rèn thô, pha vàng kim làm đồng thau/vàng ròng, pha xanh lam làm thép cường lực. |

---

## 2. Texture Lặp Lại Không Đường Nối (Seamless / Tileable Textures)
*100% Seamless chu kỳ, lặp tuần hoàn không lộ mối nối biên (Seamless UV Wrap), phong cách Stylized trong trẻo.*

| Tên File | Đường dẫn Godot (`res://`) | Độ phân giải | Dùng cho bề mặt nào |
| :--- | :--- | :--- | :--- |
| `tex_grass_seamless.png` | `res://Assets/Textures/Tileable/tex_grass_seamless.png` | 512x512 | Thảm cỏ xanh mướt mát mắt (`#529934`), mượt mà mềm mại, không sọc ô vuông; dùng phủ toàn bộ mặt đất chính. |
| `tex_dirt_seamless.png` | `res://Assets/Textures/Tileable/tex_dirt_seamless.png` | 512x512 | Đất/đường mòn nâu tự nhiên (`#8A5C35`) kèm các hạt sỏi lấm tấm hữu cơ; dùng cho đường đi, bờ vực taluy. |
| `tex_rock_seamless.png` | `res://Assets/Textures/Tileable/tex_rock_seamless.png` | 512x512 | Vách đá xám phiến Stylized có vết nứt và mảng bóng râm tự nhiên; dùng cho vách đá dựng đứng, đá tảng lớn. |
| `tex_wood_seamless.png` | `res://Assets/Textures/Tileable/tex_wood_seamless.png` | 512x512 | Vân gỗ sồi ấm áp tự nhiên (`#A8764A`); dùng lát sàn gỗ, thùng hàng, xe ngựa, hàng rào, nhịp cầu gỗ. |
| `tex_metal_seamless.png` | `res://Assets/Textures/Tileable/tex_metal_seamless.png` | 512x512 | Mặt kim loại phay xước nhẹ Stylized ánh bạc xám; dùng cho chấn song, đường ray, rương báu kim loại, máy móc. |

---

## 3. Vật Liệu Godot Dùng Chung (`Assets/Materials_Shared/*.tres`)
*Vật liệu `StandardMaterial3D` chuẩn Godot 4, sẵn sàng kéo thả trực tiếp vào MeshInstance3D hoặc gán vào Scene.*

| Tên Material | Đường dẫn (`res://`) | Texture gốc sử dụng | Màu sắc / Thuộc tính (`Albedo`, `Roughness`, `UV Scale`) |
| :--- | :--- | :--- | :--- |
| `M_Grass.tres` | `res://Assets/Materials_Shared/M_Grass.tres` | `tex_grass_seamless.png` | Albedo Color trắng thuần, Roughness 0.85. Chuẩn mặc định cho mặt sàn cỏ map. |
| `M_Dirt.tres` | `res://Assets/Materials_Shared/M_Dirt.tres` | `tex_dirt_seamless.png` | Albedo Color trắng thuần, Roughness 0.90. Chuẩn cho các lối mòn đất. |
| `M_Rock.tres` | `res://Assets/Materials_Shared/M_Rock.tres` | `tex_rock_seamless.png` | Albedo Color trắng thuần, Roughness 0.80. Dùng cho vách đá tự nhiên. |
| `M_Wood.tres` | `res://Assets/Materials_Shared/M_Wood.tres` | `tex_wood_seamless.png` | Albedo Color trắng thuần, Roughness 0.70. Dùng cho thùng gỗ, sàn gỗ. |
| `M_Metal.tres` | `res://Assets/Materials_Shared/M_Metal.tres` | `tex_metal_seamless.png` | Metallic 0.85, Roughness 0.35. Dùng cho bề mặt kim loại sáng bóng. |
| `M_Palette_Stylized.tres` | `res://Assets/Materials_Shared/M_Palette_Stylized.tres` | `palette_standard_stylized.png` | Roughness 0.60. Chuẩn dùng chung cho toàn bộ Model Blender UV Palette. |
| `M_Wood_Fence.tres` | `res://Assets/Materials_Shared/M_Wood_Fence.tres` | `tex_wood_seamless.png` | Albedo Color `Color(0.65, 0.48, 0.32, 1)`, Roughness 0.75. Tối màu hơn cho hàng rào gỗ rustic. |
| `M_Rock_Mountain_Purple.tres`| `res://Assets/Materials_Shared/M_Rock_Mountain_Purple.tres`| `mask_rock_detail.png` | Albedo Color `Color(0.72, 0.58, 0.84, 1)`, Roughness 0.85. Biến tấu từ mask đá thành núi tím huyền ảo. |
| `M_Grass_Dry.tres` | `res://Assets/Materials_Shared/M_Grass_Dry.tres` | `mask_grass_detail.png` | Albedo Color `Color(0.85, 0.76, 0.42, 1)`, Roughness 0.90. Cỏ úa màu thu. |
| `M_Dirt_RedClay.tres` | `res://Assets/Materials_Shared/M_Dirt_RedClay.tres` | `mask_dirt_detail.png` | Albedo Color `Color(0.78, 0.42, 0.28, 1)`, Roughness 0.90. Đất đỏ bazan / mỏ đất nung. |
| `M_Metal_DarkIron.tres` | `res://Assets/Materials_Shared/M_Metal_DarkIron.tres` | `mask_metal_surface.png` | Albedo Color `Color(0.35, 0.38, 0.42, 1)`, Metallic 0.90, Roughness 0.40. Sắt đen rèn thô. |
| `M_Character_Body.tres` | `res://Assets/Materials_Shared/M_Character_Body.tres` | `character_box_texture.png` | Roughness 0.60. Chuẩn vật liệu thân nhân vật Player / NPC Box. |
| `M_Character_Face.tres` | `res://Assets/Materials_Shared/M_Character_Face.tres` | `character_face.png` | Roughness 0.60. Chuẩn vật liệu khuôn mặt nhân vật Player. |

