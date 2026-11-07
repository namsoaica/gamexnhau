# DANH MỤC TEXTURE & MATERIAL DÙNG CHUNG (TEXTURE CATALOG)

> **QUY TẮC BẮT BUỘC CHO AI AGENTS (@texture-architect, @blender-helper, @csharp-coder)**:
> 1. **Tra cứu trước khi làm**: Luôn đọc file này TRƯỚC KHI tạo model, chỉnh sửa vật liệu, tạo Scene hoặc viết script sinh tài nguyên.
> 2. **Nguyên tắc tiết kiệm VRAM & Chống phình dung lượng (Zero-Bloat Asset Pipeline)**:
>    - **Ưu tiên 1 (Dùng lại 100%)**: Luôn tìm kiếm và gắn file `.tres` sẵn có trong `Assets/Materials_Shared/` (tốn 0 KB).
>    - **Ưu tiên 2 (Tạo vật liệu mới từ ảnh cũ - chỉ tốn ~1KB)**: Sử dụng các ảnh trong `Grayscale_Masks/` hoặc `Tileable/` kết hợp đổi `albedo_color` trong file `.tres` mới. Tuyệt đối không tạo ảnh `.png` mới nếu có thể dùng mask.
>    - **Ưu tiên 3 (Tạo ảnh mới)**: Khi bắt buộc phải tạo ảnh mới, phải tạo ảnh chuẩn lũy thừa 2 (`64x64`, `256x256`, `512x512`), hỗ trợ lặp Seamless hoặc Grayscale Mask để có thể tái sử dụng cho nhiều đối tượng khác nhau.
> 3. **Cập nhật danh mục**: Mỗi khi tạo mới hoặc thay đổi bất kỳ Texture hay Material nào, PHẢI cập nhật ngay vào bảng tương ứng bên dưới.

---

## 1. Bảng Màu & Mặt Nạ Xám Đổi Màu (Palettes & Grayscale Masks - Ưu Tiên Số 1)
*Mặt nạ độ tương phản cao [0.25 - 1.0], nhân trực tiếp với `albedo_color` trong Godot để tạo vô số biến thể màu mà không tốn dung lượng ảnh mới.*

| Tên File | Đường Dẫn Godot (`res://`) | Định Dạng (Format) | Độ Phân Giải | Mục Đích & Hướng Dẫn Tái Sử Dụng |
| :--- | :--- | :--- | :--- | :--- |
| `palette_standard_stylized.png` | `res://Assets/Textures/Palettes/palette_standard_stylized.png` | PNG (RGBA8) | 256x64 | **Bảng màu Stylized chuẩn** gồm 16 dải màu chuyển sắc (Cỏ, Rừng, Đất mòn, Đất sét, Đá xám, Núi đá tím, Gỗ sồi, Gỗ sáng, Sắt thép, Vàng đồng, Tông da, Vải đỏ, Vải lam, Mặt nước bọt sóng, Mây trời, Hoa văn ma pháp). Dùng cho kỹ thuật Palette UV Mapping trong Blender/Godot. |
| `mask_grass_detail.png` | `res://Assets/Textures/Grayscale_Masks/mask_grass_detail.png` | PNG (Grayscale/RGBA8) | 512x512 | **Mặt nạ vân cỏ cách điệu trắng đen**. Pha với `albedo_color` xanh làm cỏ non (`M_Grass`), vàng úa làm cỏ khô thu (`M_Grass_Dry`), tím/xanh ngọc cho thảo nguyên ma thuật. |
| `mask_dirt_detail.png` | `res://Assets/Textures/Grayscale_Masks/mask_dirt_detail.png` | PNG (Grayscale/RGBA8) | 512x512 | **Mặt nạ sỏi đất hữu cơ**. Pha với màu nâu nhạt làm đường cát, đỏ nâu làm đất bazan mỏ đất sét (`M_Dirt_RedClay`), xám tối làm bùn lầy. |
| `mask_rock_detail.png` | `res://Assets/Textures/Grayscale_Masks/mask_rock_detail.png` | PNG (Grayscale/RGBA8) | 512x512 | **Mặt nạ vách đá nứt rạn Stylized**. Pha màu tím tạo núi tím viễn cảnh (`M_Rock_Mountain_Purple`), pha xám tạo tảng đá tự nhiên, pha đỏ cam tạo ngói nhà (`M_Roof_Tiles_Red`), pha xanh ngọc tạo ngói giả kim (`M_Roof_Tiles_Teal`). |
| `mask_wood_grain.png` | `res://Assets/Textures/Grayscale_Masks/mask_wood_grain.png` | PNG (Grayscale/RGBA8) | 512x512 | **Mặt nạ thớ sợi vân gỗ tự nhiên**. Pha màu nâu ấm làm gỗ sồi, màu be nhạt làm gỗ thông, màu đỏ sẫm làm gỗ lim. |
| `mask_metal_surface.png` | `res://Assets/Textures/Grayscale_Masks/mask_metal_surface.png` | PNG (Grayscale/RGBA8) | 512x512 | **Mặt nạ xước phay kim loại ánh bạc**. Pha xám đen làm sắt rèn thô (`M_Metal_DarkIron`), pha vàng kim làm đồng thau/vàng ròng, pha xanh lam làm thép cường lực. |

---

## 2. Texture Lặp Lại Không Đường Nối (Seamless / Tileable Textures)
*100% Seamless chu kỳ, lặp tuần hoàn không lộ mối nối biên (Seamless UV Wrap), phong cách Stylized trong trẻo.*

| Tên File | Đường Dẫn Godot (`res://`) | Định Dạng (Format) | Độ Phân Giải | Mục Đích Sử Dụng & Bề Mặt Áp Dụng |
| :--- | :--- | :--- | :--- | :--- |
| `tex_grass_seamless.png` | `res://Assets/Textures/Tileable/tex_grass_seamless.png` | PNG (RGBA8) | 512x512 | **Thảm cỏ xanh mướt mát mắt** (`#529934`), mượt mà mềm mại, không sọc ô vuông; dùng phủ toàn bộ mặt đất chính và đài cao tầng 2. |
| `tex_dirt_seamless.png` | `res://Assets/Textures/Tileable/tex_dirt_seamless.png` | PNG (RGBA8) | 512x512 | **Đất/đường mòn nâu tự nhiên** (`#8A5C35`) kèm hạt sỏi lấm tấm hữu cơ; dùng cho đường đi chính, taluy bờ vực. |
| `tex_rock_seamless.png` | `res://Assets/Textures/Tileable/tex_rock_seamless.png` | PNG (RGBA8) | 512x512 | **Vách đá phiến xám Stylized** có vết nứt và khối mảng bóng râm tự nhiên; dùng cho vách đá dựng đứng, đá tảng lớn quanh map. |
| `tex_wood_seamless.png` | `res://Assets/Textures/Tileable/tex_wood_seamless.png` | PNG (RGBA8) | 512x512 | **Vân gỗ sồi tự nhiên** (`#A8764A`); dùng lát sàn gỗ, thùng hàng, xe ngựa, hàng rào đài cao, nhịp cầu gỗ. |
| `tex_metal_seamless.png` | `res://Assets/Textures/Tileable/tex_metal_seamless.png` | PNG (RGBA8) | 512x512 | **Mặt kim loại phay xước nhẹ Stylized ánh bạc**; dùng cho chấn song, đường ray, rương báu kim loại, máy móc. |
| `tex_canopy_striped.png` | `res://Assets/Textures/Tileable/tex_canopy_striped.png` | PNG (RGBA8) | 128x128 | **Bạt sọc đỏ-trắng Stylized** (`#DA3028` và trắng kem); dùng cho mái che lều sạp chợ, xe hàng. |
| `tex_roof_tiles_red.png` | `res://Assets/Textures/Tileable/tex_roof_tiles_red.png` | PNG (RGB8) | 256x256 | **Mái ngói vảy đỏ cam Stylized** (`#A83828`), viền vát bắt sáng và bóng rãnh; dùng cho mái nhà rèn, quán ăn, nhà dân. |
| `tex_roof_tiles_teal.png` | `res://Assets/Textures/Tileable/tex_roof_tiles_teal.png` | PNG (RGB8) | 256x256 | **Mái ngói vảy xanh ngọc teal** (`#268C82`); dùng cho mái nhà giả kim huyền bí. |
| `tex_stone_cobble.png` | `res://Assets/Textures/Tileable/tex_stone_cobble.png` | PNG (RGB8) | 256x256 | **Đá cuội gạch xây Stylized** (`#686C70`); dùng cho lò rèn, ống khói, giếng nước, lò nướng bánh. |

---

## 3. Vật Liệu Godot Dùng Chung (`Assets/Materials_Shared/*.tres`)
*Vật liệu `StandardMaterial3D` chuẩn Godot 4, sẵn sàng kéo thả trực tiếp vào MeshInstance3D hoặc gán vào Scene.*

| Tên Material | Đường Dẫn (`res://`) | Texture Gốc Sử Dụng | Mục Đích & Thuộc Tính (`Albedo`, `Roughness`, `Metallic`) |
| :--- | :--- | :--- | :--- |
| `M_Grass.tres` | `res://Assets/Materials_Shared/M_Grass.tres` | `tex_grass_seamless.png` | Chuẩn mặc định cho mặt sàn cỏ map, đài cao. Albedo trắng thuần, Roughness 0.85. |
| `M_Grass_Dry.tres` | `res://Assets/Materials_Shared/M_Grass_Dry.tres` | `mask_grass_detail.png` | Cỏ úa màu thu. Albedo `Color(0.85, 0.76, 0.42, 1)`, Roughness 0.90. |
| `M_Dirt.tres` | `res://Assets/Materials_Shared/M_Dirt.tres` | `tex_dirt_seamless.png` | Chuẩn cho các lối mòn đất. Albedo trắng thuần, Roughness 0.90. |
| `M_Dirt_RedClay.tres` | `res://Assets/Materials_Shared/M_Dirt_RedClay.tres` | `mask_dirt_detail.png` | Đất đỏ bazan / mỏ đất sét nung. Albedo `Color(0.78, 0.42, 0.28, 1)`, Roughness 0.90. |
| `M_Rock.tres` | `res://Assets/Materials_Shared/M_Rock.tres` | `tex_rock_seamless.png` | Dùng cho vách đá và đá tảng tự nhiên. Albedo trắng thuần, Roughness 0.80. |
| `M_Rock_Mountain_Purple.tres` | `res://Assets/Materials_Shared/M_Rock_Mountain_Purple.tres` | `mask_rock_detail.png` | Núi đá tím huyền ảo viễn cảnh. Albedo `Color(0.72, 0.58, 0.84, 1)`, Roughness 0.85. |
| `M_Wood.tres` | `res://Assets/Materials_Shared/M_Wood.tres` | `tex_wood_seamless.png` | Thùng gỗ, sàn gỗ, đồ nội thất. Albedo trắng thuần, Roughness 0.70. |
| `M_Wood_Fence.tres` | `res://Assets/Materials_Shared/M_Wood_Fence.tres` | `tex_wood_seamless.png` | Hàng rào gỗ rustic bao quanh đài cao. Albedo `Color(0.65, 0.48, 0.32, 1)`, Roughness 0.75. |
| `M_Metal.tres` | `res://Assets/Materials_Shared/M_Metal.tres` | `tex_metal_seamless.png` | Bề mặt kim loại sáng bóng, đường ray. Metallic 0.85, Roughness 0.35. |
| `M_Metal_DarkIron.tres` | `res://Assets/Materials_Shared/M_Metal_DarkIron.tres` | `mask_metal_surface.png` | Sắt đen rèn thô, xích sắt, vũ khí cổ. Albedo `Color(0.35, 0.38, 0.42, 1)`, Metallic 0.90, Roughness 0.40. |
| `M_Palette_Stylized.tres` | `res://Assets/Materials_Shared/M_Palette_Stylized.tres` | `palette_standard_stylized.png` | Chuẩn dùng chung cho toàn bộ Model Blender UV Palette. Roughness 0.60. |
| `M_Character_Body.tres` | `res://Assets/Materials_Shared/M_Character_Body.tres` | `character_box_texture.png` | Chuẩn vật liệu thân nhân vật Player / NPC Box. Roughness 0.60. |
| `M_Character_Face.tres` | `res://Assets/Materials_Shared/M_Character_Face.tres` | `character_face.png` | Chuẩn vật liệu khuôn mặt nhân vật Player. Roughness 0.60. |
| `M_Roof_Tiles_Red.tres` | `res://Assets/Materials_Shared/M_Roof_Tiles_Red.tres` | `tex_roof_tiles_red.png` | Mái ngói đỏ cam nhà rèn & nhà dân. Triplanar UV, Albedo trắng thuần, Roughness 0.75. |
| `M_Roof_Tiles_Teal.tres` | `res://Assets/Materials_Shared/M_Roof_Tiles_Teal.tres` | `tex_roof_tiles_teal.png` | Mái ngói xanh ngọc teal nhà giả kim. Triplanar UV, Albedo trắng thuần, Roughness 0.75. |
| `M_Stone_Cobble.tres` | `res://Assets/Materials_Shared/M_Stone_Cobble.tres` | `tex_stone_cobble.png` | Đá cuội lò rèn, ống khói, giếng đá, lò nướng. Triplanar UV, Roughness 0.80. |
| `M_Canopy_Striped.tres` | `res://Assets/Materials_Shared/M_Canopy_Striped.tres` | `tex_canopy_striped.png` | Mái bạt sọc đỏ trắng sạp chợ. Roughness 0.85. |
| `M_Mystic_Cyan.tres` | `res://Assets/Materials_Shared/M_Mystic_Cyan.tres` | N/A (Emission) | Vạc ma thuật, khói phép thuật. Albedo `Color(0.2, 0.85, 0.8, 0.85)`, Emission x2.0 cyan. |
| `M_Lava_Fire.tres` | `res://Assets/Materials_Shared/M_Lava_Fire.tres` | N/A (Emission) | Lửa lò rèn, lò nướng bánh, lò luyện quặng. Albedo `Color(1.0, 0.45, 0.05, 1)`, Emission x2.5 vàng cam. |
