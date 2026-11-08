"""
Script Blender 3D: Dựng Bản Đồ Làng Mở Rộng Hoàn Thiện Theo Phác Họa 'modelyeucau/map2/1.jpg'
Tuân thủ nghiêm ngặt Antigravity Procedural & Sketch-to-3D Pipeline:
- Sử dụng Thư Viện Procedural Chuẩn 'tools/blender_kit.py'.
- Bắt buộc trải UV tự động (unwrap_mesh) cho MỌI mesh (cấm mất UV bệt màu).
- Gán vật liệu liên kết Texture Seamless (thớ gỗ, thớ đá, bạt sọc, vân đất, ngói đỏ, ngói teal).
- Chi tiết 4 phòng nội thất chuẩn Diorama cắt vách:
  * Nhà Rèn: Lò rèn vòm đá gạch đỏ lửa, đe sắt lớn trên bục tròn, rương thép vụn, rương than củi, bể nước tôi nguội, giá vũ khí gắn kiếm/khiên/giáp treo tường, bàn thợ nguội kìm búa.
  * Nhà Giả Kim: Vạc đồng ma thuật phát quang cyan bốc khói, bàn thí nghiệm sách mở, tủ sách cổ ma thuật kịch trần, kệ chai lọ độc dược đủ màu, chùm thảo mộc khô treo trần.
  * Quán Ăn / Nhà Bếp: Lò nướng bánh mì gạch vòm đỏ than hồng, bàn nhào bột cán bột và bánh mì baguette, bàn ăn dài kèm 2 ghế băng gỗ, kệ bát đĩa gốm sứ, xâu xúc xích treo trần, thùng rượu gỗ.
  * Nhà Dân Cư: Giường ngủ gỗ nệm đỏ gối trắng ấm cúng, tủ áo 2 cánh cao lớn, thảm sàn thổ cẩm sọc kẻ, bàn con cửa sổ rèm xanh.
- 8 Model 3D NPC Stylized dựng tại các vị trí đặc thù:
  * Thợ Rèn (Vulcan): búa tạ yếm da nâu, râu quai nón, cơ bắp cuồn cuộn.
  * Nhà Giả Kim (Aria): áo choàng tím có mũ trùm, 2 bình thuốc phát quang cyan & pink.
  * Đầu Bếp (Gusteau): mũ trắng cao, tạp dề trắng, bánh mì baguette nướng vàng.
  * Nông Dân (George): nón lá, áo nâu, cuốc làm vườn & bó lúa vàng.
  * Ngư Dân (Finn): nón bucket, cần câu tre dài, giỏ nan cá tươi tại cầu cảng.
  * Thợ Mỏ (Brock): mũ bảo hộ vàng có đèn soi, đồ bảo hộ cam, cuốc chim tại mỏ đá.
  * Tiều Phu (Grover): mũ len đỏ, áo kẻ caro, rìu bổ củi to tại xưởng gỗ.
  * 2 Lính Canh (Aegis & Phalanx): mũ giáp sắt, áo giáp kim loại, giáo dài & khiên tròn gác cổng.
- Kỹ thuật: bmesh + Bevel 2-3 segments + Solidify + Shade Auto Smooth + Human Reference Scale (Người 1.8m, Cửa 2.3-2.6m, Tường 3.5-4.5m).
- Tự động sinh collider '-col' trên các vật cản.
- Xuất GLB 'Assets/Models/village_map.glb' và lưu 'Assets/Blender_Source/village_map.blend'.
- Render ảnh mắt thần đa góc đối chiếu 'Assets/Models/_preview_render.png'.
"""

import sys
import os
import bpy
import math

# Thiết lập đường dẫn workspace
cur_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.abspath(os.path.join(cur_dir, ".."))
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from tools.blender_kit import (
    clean_scene,
    create_material,
    unwrap_mesh,
    create_beveled_box,
    create_beveled_cylinder,
    build_chamfered_rock,
    build_stylized_tree,
    build_detailed_roof_gabled,
    setup_preview_render
)

def build_village():
    print("=== BẮT ĐẦU DỰNG BẢN ĐỒ LÀNG MỞ RỘNG (PROCEDURAL & SKETCH PIPELINE) ===")
    clean_scene()

    tex_dir = os.path.join(workspace_dir, "Assets", "Textures", "Tileable")
    p_wood = os.path.join(tex_dir, "tex_wood_seamless.png")
    p_rock = os.path.join(tex_dir, "tex_rock_seamless.png")
    p_cobble = os.path.join(tex_dir, "tex_stone_cobble.png")
    p_dirt = os.path.join(tex_dir, "tex_dirt_seamless.png")
    p_metal = os.path.join(tex_dir, "tex_metal_seamless.png")
    p_roof_red = os.path.join(tex_dir, "tex_roof_tiles_red.png")
    p_roof_teal = os.path.join(tex_dir, "tex_roof_tiles_teal.png")
    p_canopy = os.path.join(tex_dir, "tex_canopy_striped.png")
    p_grass = os.path.join(tex_dir, "tex_grass_seamless.png")

    # =========================================================================
    # 1. BẢNG VẬT LIỆU TEXTURE SEAMLESS & SHADING
    # =========================================================================
    mat_dirt = create_material("Mat_Dirt", (0.54, 0.36, 0.21), roughness=0.90, texture_path=p_dirt)
    mat_stone = create_material("Mat_Stone", (0.42, 0.44, 0.46), roughness=0.80, texture_path=p_rock)
    mat_cobble = create_material("Mat_Cobble", (0.41, 0.42, 0.44), roughness=0.80, texture_path=p_cobble)
    mat_wood = create_material("Mat_Wood", (0.55, 0.35, 0.20), roughness=0.75, texture_path=p_wood)
    mat_wood_fence = create_material("Mat_Wood_Fence", (0.36, 0.23, 0.13), roughness=0.80, texture_path=p_wood)
    mat_metal = create_material("Mat_Metal", (0.58, 0.60, 0.64), roughness=0.35, metallic=0.85, texture_path=p_metal)
    mat_metal_silver = create_material("Mat_Metal_Silver", (0.78, 0.80, 0.84), roughness=0.25, metallic=0.90, texture_path=p_metal)
    mat_metal_gold = create_material("Mat_Metal_Gold", (0.92, 0.75, 0.22), roughness=0.30, metallic=0.85)
    mat_roof_red = create_material("Mat_Roof_Red", (0.66, 0.22, 0.16), roughness=0.75, texture_path=p_roof_red)
    mat_roof_teal = create_material("Mat_Roof_Teal", (0.15, 0.55, 0.51), roughness=0.75, texture_path=p_roof_teal)
    mat_canopy_striped = create_material("Mat_Canopy_Striped", (0.88, 0.23, 0.23), roughness=0.85, texture_path=p_canopy)
    mat_mystic_cyan = create_material("Mat_Mystic_Cyan", (0.20, 0.88, 0.82), roughness=0.20, emission_color=(0.20, 0.88, 0.82), emission_strength=3.5)
    mat_mystic_purple = create_material("Mat_Mystic_Purple", (0.65, 0.22, 0.85), roughness=0.25, emission_color=(0.65, 0.22, 0.85), emission_strength=2.6)
    mat_mystic_pink = create_material("Mat_Mystic_Pink", (0.90, 0.25, 0.75), roughness=0.20, emission_color=(0.90, 0.25, 0.75), emission_strength=3.0)
    mat_lava_fire = create_material("Mat_Lava_Fire", (1.00, 0.45, 0.05), roughness=0.40, emission_color=(1.00, 0.45, 0.05), emission_strength=3.8)
    mat_foliage = create_material("Mat_Foliage", (0.22, 0.52, 0.20), roughness=0.85, texture_path=p_grass)
    mat_vegetable = create_material("Mat_Vegetable", (0.30, 0.69, 0.24), roughness=0.80)
    mat_wheat = create_material("Mat_Wheat", (0.90, 0.75, 0.29), roughness=0.85)
    mat_bread = create_material("Mat_Bread", (0.83, 0.58, 0.29), roughness=0.70)
    mat_wall = create_material("Mat_Wall_Stone", (0.82, 0.80, 0.76), roughness=0.85)
    mat_water = create_material("Mat_Water", (0.18, 0.65, 0.72), roughness=0.15, emission_color=(0.18, 0.65, 0.72), emission_strength=0.9)
    mat_sausage = create_material("Mat_Sausage", (0.72, 0.24, 0.18), roughness=0.60)

    # Vật liệu cho 8 Stylized NPC
    mat_skin_tan = create_material("Mat_NPC_Skin_Tan", (0.74, 0.54, 0.42), roughness=0.60)
    mat_skin_fair = create_material("Mat_NPC_Skin_Fair", (0.86, 0.68, 0.54), roughness=0.60)
    mat_npc_black = create_material("Mat_NPC_Black", (0.10, 0.10, 0.10), roughness=0.40)
    mat_npc_white = create_material("Mat_NPC_White", (0.95, 0.95, 0.95), roughness=0.70)
    mat_apron_brown = create_material("Mat_NPC_Apron_Brown", (0.42, 0.26, 0.16), roughness=0.80)
    mat_pants_dark = create_material("Mat_NPC_Pants_Dark", (0.28, 0.30, 0.34), roughness=0.80)
    mat_pants_blue = create_material("Mat_NPC_Pants_Blue", (0.24, 0.36, 0.54), roughness=0.80)
    mat_hard_hat_yellow = create_material("Mat_NPC_HardHat", (0.95, 0.78, 0.12), roughness=0.35)
    mat_miner_suit = create_material("Mat_NPC_MinerSuit", (0.84, 0.58, 0.18), roughness=0.75)
    mat_plaid_red = create_material("Mat_NPC_Plaid", (0.76, 0.18, 0.18), roughness=0.80)
    mat_kaki_shirt = create_material("Mat_NPC_Kaki", (0.76, 0.68, 0.52), roughness=0.80)
    mat_farmer_brown = create_material("Mat_NPC_FarmerBrown", (0.54, 0.36, 0.22), roughness=0.85)

    # =========================================================================
    # HÀM DỰNG NHÂN VẬT STYLIZED 3D CHUẨN CAO 1.8M (HUMAN REFERENCE SCALE)
    # =========================================================================
    def build_stylized_npc_at(prefix, skin_m, shirt_m, pants_m, shoe_m, pos, rot_y=0.0,
                              has_beard=False, beard_m=None, hat_type=None, hat_m=None,
                              tool_type=None):
        gx, gy, gz = pos

        def local_to_world(lx, ly, lz):
            cos_y = math.cos(rot_y)
            sin_y = math.sin(rot_y)
            wx = gx + lx * cos_y + lz * sin_y
            wy = gy + ly
            wz = gz - lx * sin_y + lz * cos_y
            return (wx, wy, wz)

        # 1. Chân & Giày (0.0m - 0.76m)
        create_beveled_box(f"{prefix}_Shoe_L", (0.16, 0.14, 0.22), local_to_world(-0.14, 0.07, 0.03), bevel_width=0.02, rotation=(0, rot_y, 0), material=shoe_m)
        create_beveled_box(f"{prefix}_Shoe_R", (0.16, 0.14, 0.22), local_to_world(0.14, 0.07, 0.03), bevel_width=0.02, rotation=(0, rot_y, 0), material=shoe_m)
        create_beveled_box(f"{prefix}_Leg_L", (0.15, 0.62, 0.16), local_to_world(-0.14, 0.45, 0.0), bevel_width=0.02, rotation=(0, rot_y, 0), material=pants_m)
        create_beveled_box(f"{prefix}_Leg_R", (0.15, 0.62, 0.16), local_to_world(0.14, 0.45, 0.0), bevel_width=0.02, rotation=(0, rot_y, 0), material=pants_m)

        # 2. Thân người (0.76m - 1.34m)
        create_beveled_box(f"{prefix}_Torso", (0.42, 0.58, 0.26), local_to_world(0.0, 1.05, 0.0), bevel_width=0.03, rotation=(0, rot_y, 0), material=shirt_m)

        # 3. Cánh tay & Bàn tay
        create_beveled_box(f"{prefix}_Arm_L", (0.13, 0.50, 0.14), local_to_world(-0.28, 1.02, 0.0), bevel_width=0.02, rotation=(0, rot_y, 0), material=shirt_m)
        create_beveled_box(f"{prefix}_Arm_R", (0.13, 0.50, 0.14), local_to_world(0.28, 1.02, 0.0), bevel_width=0.02, rotation=(0, rot_y, 0), material=shirt_m)
        create_beveled_box(f"{prefix}_Hand_L", (0.11, 0.12, 0.12), local_to_world(-0.28, 0.72, 0.0), bevel_width=0.02, rotation=(0, rot_y, 0), material=skin_m)
        create_beveled_box(f"{prefix}_Hand_R", (0.11, 0.12, 0.12), local_to_world(0.28, 0.72, 0.0), bevel_width=0.02, rotation=(0, rot_y, 0), material=skin_m)

        # 4. Cổ & Đầu (1.34m - 1.76m)
        create_beveled_cylinder(f"{prefix}_Neck", 0.09, 0.12, local_to_world(0.0, 1.36, 0.0), bevel_width=0.015, rotation=(0, rot_y, 0), material=skin_m)
        create_beveled_box(f"{prefix}_Head", (0.34, 0.36, 0.32), local_to_world(0.0, 1.56, 0.0), bevel_width=0.04, rotation=(0, rot_y, 0), material=skin_m)

        # Mắt (Eyes)
        create_beveled_box(f"{prefix}_Eye_L", (0.04, 0.06, 0.02), local_to_world(-0.08, 1.58, 0.17), bevel_width=0.005, rotation=(0, rot_y, 0), material=mat_npc_black)
        create_beveled_box(f"{prefix}_Eye_R", (0.04, 0.06, 0.02), local_to_world(0.08, 1.58, 0.17), bevel_width=0.005, rotation=(0, rot_y, 0), material=mat_npc_black)

        # Râu quai nón
        if has_beard and beard_m:
            create_beveled_box(f"{prefix}_Beard", (0.36, 0.18, 0.18), local_to_world(0.0, 1.45, 0.10), bevel_width=0.02, rotation=(0, rot_y, 0), material=beard_m)

        # 5. Mũ nón chuyên ngành (Hat/Headgear)
        if hat_type == "chef":
            create_beveled_cylinder(f"{prefix}_ChefHat_Base", 0.16, 0.15, local_to_world(0.0, 1.78, 0.0), bevel_width=0.02, rotation=(0, rot_y, 0), material=hat_m)
            create_beveled_cylinder(f"{prefix}_ChefHat_Top", 0.22, 0.20, local_to_world(0.0, 1.92, 0.0), bevel_width=0.04, rotation=(0, rot_y, 0), material=hat_m)
        elif hat_type == "straw_conical":
            create_beveled_cylinder(f"{prefix}_Hat_Rim", 0.36, 0.05, local_to_world(0.0, 1.74, 0.0), bevel_width=0.02, vertices=16, rotation=(0, rot_y, 0), material=hat_m)
            create_beveled_cylinder(f"{prefix}_Hat_Cone", 0.22, 0.18, local_to_world(0.0, 1.84, 0.0), bevel_width=0.03, vertices=16, rotation=(0, rot_y, 0), material=hat_m)
        elif hat_type == "bucket":
            create_beveled_cylinder(f"{prefix}_Hat_Brim", 0.30, 0.04, local_to_world(0.0, 1.74, 0.0), bevel_width=0.015, vertices=16, rotation=(0, rot_y, 0), material=hat_m)
            create_beveled_cylinder(f"{prefix}_Hat_Crown", 0.18, 0.12, local_to_world(0.0, 1.80, 0.0), bevel_width=0.02, vertices=16, rotation=(0, rot_y, 0), material=hat_m)
        elif hat_type == "hard_hat":
            create_beveled_cylinder(f"{prefix}_Hat_Brim", 0.24, 0.05, local_to_world(0.0, 1.74, 0.0), bevel_width=0.02, rotation=(0, rot_y, 0), material=hat_m)
            create_beveled_cylinder(f"{prefix}_Hat_Dome", 0.19, 0.16, local_to_world(0.0, 1.82, 0.0), bevel_width=0.04, rotation=(0, rot_y, 0), material=hat_m)
            create_beveled_box(f"{prefix}_Headlamp", (0.08, 0.07, 0.06), local_to_world(0.0, 1.80, 0.22), bevel_width=0.01, rotation=(0, rot_y, 0), material=mat_lava_fire)
        elif hat_type == "beanie":
            create_beveled_cylinder(f"{prefix}_Beanie_Band", 0.20, 0.08, local_to_world(0.0, 1.72, 0.0), bevel_width=0.02, rotation=(0, rot_y, 0), material=hat_m)
            create_beveled_cylinder(f"{prefix}_Beanie_Top", 0.18, 0.14, local_to_world(0.0, 1.80, -0.02), bevel_width=0.04, rotation=(0, rot_y, 0), material=hat_m)
        elif hat_type == "hood":
            create_beveled_box(f"{prefix}_Hood", (0.40, 0.42, 0.38), local_to_world(0.0, 1.60, -0.02), bevel_width=0.04, rotation=(0, rot_y, 0), material=hat_m)
            create_beveled_box(f"{prefix}_Hood_Tip", (0.15, 0.15, 0.20), local_to_world(0.0, 1.65, -0.22), bevel_width=0.03, rotation=(0, rot_y, 0), material=hat_m)
            create_beveled_box(f"{prefix}_Skirt", (0.46, 0.55, 0.32), local_to_world(0.0, 0.55, 0.0), bevel_width=0.03, rotation=(0, rot_y, 0), material=hat_m)
        elif hat_type == "helmet":
            create_beveled_cylinder(f"{prefix}_Helmet", 0.20, 0.24, local_to_world(0.0, 1.76, 0.0), bevel_width=0.03, rotation=(0, rot_y, 0), material=hat_m)
            create_beveled_box(f"{prefix}_Nasal", (0.04, 0.14, 0.06), local_to_world(0.0, 1.62, 0.19), bevel_width=0.01, rotation=(0, rot_y, 0), material=hat_m)

        # 6. Đạo cụ và công cụ cầm tay đặc trưng
        if tool_type == "blacksmith":
            create_beveled_box(f"{prefix}_Apron", (0.34, 0.52, 0.05), local_to_world(0.0, 0.95, 0.14), bevel_width=0.015, rotation=(0, rot_y, 0), material=mat_apron_brown)
            create_beveled_cylinder(f"{prefix}_Hammer_Handle", 0.03, 0.85, local_to_world(0.38, 0.95, 0.25), bevel_width=0.008, rotation=(0.5, rot_y, 0), material=mat_wood)
            create_beveled_box(f"{prefix}_Hammer_Head", (0.16, 0.14, 0.25), local_to_world(0.38, 1.25, 0.42), bevel_width=0.02, rotation=(0, rot_y, 0), material=mat_metal)
        elif tool_type == "alchemist":
            create_beveled_cylinder(f"{prefix}_Pot_L", 0.06, 0.14, local_to_world(-0.28, 0.82, 0.16), bevel_width=0.015, rotation=(0, rot_y, 0), material=mat_mystic_cyan)
            create_beveled_cylinder(f"{prefix}_Pot_R", 0.06, 0.14, local_to_world(0.28, 0.82, 0.16), bevel_width=0.015, rotation=(0, rot_y, 0), material=mat_mystic_pink)
        elif tool_type == "chef":
            create_beveled_cylinder(f"{prefix}_Baguette", 0.07, 0.65, local_to_world(0.0, 0.92, 0.20), bevel_width=0.02, rotation=(0, rot_y + 1.57, 0.2), material=mat_bread)
        elif tool_type == "farmer":
            create_beveled_cylinder(f"{prefix}_Hoe_Handle", 0.025, 1.10, local_to_world(0.36, 1.15, -0.10), bevel_width=0.008, rotation=(-0.4, rot_y, 0), material=mat_wood)
            create_beveled_box(f"{prefix}_Hoe_Blade", (0.14, 0.18, 0.04), local_to_world(0.36, 1.55, -0.32), bevel_width=0.01, rotation=(0, rot_y, 0), material=mat_metal)
            create_beveled_cylinder(f"{prefix}_Wheat_Bundle", 0.11, 0.45, local_to_world(-0.28, 0.88, 0.16), bevel_width=0.02, rotation=(0.3, rot_y, 0), material=mat_wheat)
        elif tool_type == "fisherman":
            create_beveled_cylinder(f"{prefix}_Rod", 0.02, 2.10, local_to_world(0.32, 1.05, 0.12), bevel_width=0.005, rotation=(-0.1, rot_y, 0), material=mat_wood)
            create_beveled_cylinder(f"{prefix}_Basket", 0.14, 0.24, local_to_world(-0.32, 0.45, 0.08), bevel_width=0.02, rotation=(0, rot_y, 0), material=mat_wheat)
            create_beveled_box(f"{prefix}_Fish_1", (0.06, 0.16, 0.08), local_to_world(-0.32, 0.58, 0.08), bevel_width=0.01, rotation=(0, rot_y, 0), material=mat_water)
        elif tool_type == "miner":
            create_beveled_cylinder(f"{prefix}_Pick_Handle", 0.028, 1.05, local_to_world(0.36, 1.15, -0.10), bevel_width=0.008, rotation=(-0.4, rot_y, 0), material=mat_wood)
            create_beveled_box(f"{prefix}_Pick_Head", (0.10, 0.08, 0.42), local_to_world(0.36, 1.55, -0.32), bevel_width=0.02, rotation=(0, rot_y, 0), material=mat_metal)
        elif tool_type == "lumberjack":
            create_beveled_cylinder(f"{prefix}_Axe_Handle", 0.03, 1.10, local_to_world(0.36, 1.15, -0.10), bevel_width=0.008, rotation=(-0.4, rot_y, 0), material=mat_wood)
            create_beveled_box(f"{prefix}_Axe_Blade", (0.08, 0.26, 0.22), local_to_world(0.36, 1.55, -0.32), bevel_width=0.02, rotation=(0, rot_y, 0), material=mat_metal_silver)
        elif tool_type == "guard":
            create_beveled_cylinder(f"{prefix}_Shield_Rim", 0.30, 0.06, local_to_world(-0.36, 0.95, 0.15), bevel_width=0.02, rotation=(1.57, rot_y, 0), material=mat_metal_gold)
            create_beveled_cylinder(f"{prefix}_Shield_Center", 0.24, 0.07, local_to_world(-0.36, 0.95, 0.15), bevel_width=0.02, rotation=(1.57, rot_y, 0), material=mat_wood)
            create_beveled_cylinder(f"{prefix}_Spear_Shaft", 0.025, 2.30, local_to_world(0.36, 1.15, 0.12), bevel_width=0.005, rotation=(0, rot_y, 0), material=mat_wood)
            create_beveled_box(f"{prefix}_Spear_Tip", (0.05, 0.30, 0.08), local_to_world(0.36, 2.35, 0.12), bevel_width=0.015, rotation=(0, rot_y, 0), material=mat_metal_silver)

    # =========================================================================
    # 2. ĐƯỜNG MÒN ĐẤT NỐI LIỀN TRỰC TIẾP TỪ ĐẢO ĐÁ VÀO LÀNG
    # =========================================================================
    create_beveled_box("Path_Connector_Island", (3.2, 0.04, 4.5), (4.0, 0.02, 2.5), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_Connector_Bend", (3.4, 0.04, 4.5), (2.0, 0.02, 6.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_Village_Main_Gate", (3.6, 0.04, 8.0), (0.0, 0.02, 11.5), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_Village_Main_Avenue", (4.0, 0.04, 12.0), (0.0, 0.02, 20.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_Market_Square", (11.0, 0.04, 9.0), (0.0, 0.02, 29.5), bevel_width=0.02, material=mat_dirt)

    create_beveled_box("Path_To_Farm", (4.5, 0.04, 2.4), (-4.5, 0.02, 8.5), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_To_Chef", (4.5, 0.04, 2.4), (4.5, 0.02, 8.5), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_To_Smith", (6.5, 0.04, 3.0), (-6.0, 0.02, 21.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_To_Alchemist", (6.5, 0.04, 3.0), (6.0, 0.02, 21.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_To_House", (5.0, 0.04, 2.6), (-5.5, 0.02, 28.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_To_Lumber", (2.8, 0.04, 11.0), (-12.0, 0.02, 36.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_To_Mine", (2.8, 0.04, 11.0), (12.0, 0.02, 36.0), bevel_width=0.02, material=mat_dirt)

    # =========================================================================
    # 3. CỔNG LÀNG, VƯỜN RAU CẢI & 2 LÍNH CANH GÁC CỔNG
    # =========================================================================
    gate_z = 8.5
    create_beveled_cylinder("Gate_Post_L", 0.24, 4.0, (-2.0, 2.0, gate_z), bevel_width=0.03, material=mat_wood)
    create_beveled_cylinder("Gate_Post_R", 0.24, 4.0, (2.0, 2.0, gate_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Gate_Beam_Top", (4.6, 0.35, 0.35), (0.0, 3.8, gate_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Gate_Signboard", (2.4, 0.7, 0.12), (0.0, 3.1, gate_z), bevel_width=0.02, material=mat_wood)

    for side in [-1, 1]:
        for i in range(4):
            fx = side * (2.8 + i * 1.5)
            create_beveled_cylinder(f"Fence_Gate_{side}_{i}", 0.11, 1.3, (fx, 0.65, gate_z), bevel_width=0.02, material=mat_wood_fence)
            create_beveled_box(f"Fence_Rail_Top_{side}_{i}", (1.6, 0.08, 0.08), (fx - side * 0.75, 1.0, gate_z), bevel_width=0.015, material=mat_wood_fence)
            create_beveled_box(f"Fence_Rail_Bot_{side}_{i}", (1.6, 0.08, 0.08), (fx - side * 0.75, 0.5, gate_z), bevel_width=0.015, material=mat_wood_fence)

    # 3.A 2 LÍNH CANH GÁC CỔNG (AEGIS & PHALANX)
    build_stylized_npc_at("NPC_Aegis", mat_skin_fair, mat_metal_silver, mat_pants_dark, mat_metal_silver,
                          pos=(-0.8, 0.0, gate_z), rot_y=0.0, hat_type="helmet", hat_m=mat_metal_silver, tool_type="guard")
    build_stylized_npc_at("NPC_Guard_2", mat_skin_fair, mat_metal_silver, mat_pants_dark, mat_metal_silver,
                          pos=(0.8, 0.0, gate_z), rot_y=0.0, hat_type="helmet", hat_m=mat_metal_silver, tool_type="guard")

    # 3.B VƯỜN RAU CẢI & NÔNG DÂN GEORGE
    for row in range(3):
        rz = 7.5 + row * 1.1
        create_beveled_box(f"Crop_Soil_L_{row}", (4.2, 0.1, 0.8), (-5.2, 0.05, rz), bevel_width=0.02, material=mat_dirt)
        for col in range(4):
            cx = -6.5 + col * 0.9
            build_chamfered_rock(f"Cabbage_L_{row}_{col}", (0.52, 0.44, 0.52), (cx, 0.22, rz), material=mat_vegetable, seed_val=row*10+col)

    for row in range(3):
        rz = 7.5 + row * 1.1
        create_beveled_box(f"Crop_Soil_R_{row}", (3.6, 0.1, 0.8), (4.8, 0.05, rz), bevel_width=0.02, material=mat_dirt)
        for col in range(3):
            cx = 3.9 + col * 0.9
            build_chamfered_rock(f"Cabbage_R_{row}_{col}", (0.50, 0.42, 0.50), (cx, 0.22, rz), material=mat_vegetable, seed_val=100+row*10+col)

    build_stylized_npc_at("NPC_George", mat_skin_tan, mat_farmer_brown, mat_farmer_brown, mat_apron_brown,
                          pos=(-5.2, 0.0, 8.5), rot_y=1.57, hat_type="straw_conical", hat_m=mat_wheat, tool_type="farmer")

    # =========================================================================
    # 4. QUÁN ĂN / TAVERN CỦA ĐẦU BẾP GUSTEAU (ĐÔNG: X = 8.0, Z = 7.5)
    # =========================================================================
    cf_cx, cf_cz = 8.0, 7.5
    cf_w, cf_l, cf_h = 6.2, 5.4, 3.6
    create_beveled_box("Floor_Chef", (cf_w, 0.15, cf_l), (cf_cx, 0.08, cf_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_Chef", (cf_w, cf_h, 0.3), (cf_cx, cf_h/2, cf_cz - cf_l/2 + 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_Chef", (cf_w, cf_h, 0.3), (cf_cx, cf_h/2, cf_cz + cf_l/2 - 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_East_Chef", (0.3, cf_h, cf_l - 0.6), (cf_cx + cf_w/2 - 0.15, cf_h/2, cf_cz), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Chef_L", (0.3, cf_h, 1.8), (cf_cx - cf_w/2 + 0.15, cf_h/2, cf_cz - 1.5), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Chef_R", (0.3, cf_h, 1.8), (cf_cx - cf_w/2 + 0.15, cf_h/2, cf_cz + 1.5), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Chef_Top", (0.3, 1.1, 1.8), (cf_cx - cf_w/2 + 0.15, cf_h - 0.55, cf_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Chef", cf_w, cf_l, 1.8, (cf_cx, cf_h, cf_cz), overhang=0.35, ridge_along_x=False, material=mat_roof_red)

    # 4.A NỘI THẤT QUÁN ĂN / NHÀ BẾP (DIORAMA CẮT VÁCH CHUẨN ẢNH 1.JPG)
    # Lò nướng bánh mì gạch vòm đỏ than hồng (Bakery_Brick_Oven-col)
    create_beveled_cylinder("Bakery_Brick_Oven-col", 0.95, 1.8, (cf_cx + cf_w/2 - 1.2, 0.90, cf_cz - cf_l/2 + 1.2), bevel_width=0.04, vertices=16, material=mat_cobble)
    build_chamfered_rock("Bakery_Brick_Oven_Fire", (0.80, 0.55, 0.70), (cf_cx + cf_w/2 - 1.2, 0.55, cf_cz - cf_l/2 + 1.2), material=mat_lava_fire, seed_val=666)
    create_beveled_cylinder("Bakery_Oven_Flue", 0.28, 1.8, (cf_cx + cf_w/2 - 1.2, 2.3, cf_cz - cf_l/2 + 1.2), bevel_width=0.02, material=mat_cobble)

    # Bàn nhào bột lớn có cây cán bột, bột mì trắng và các ổ bánh mì baguette (Bakery_Prep_Table-col)
    create_beveled_box("Bakery_Prep_Table-col", (1.2, 0.88, 2.4), (cf_cx - 1.3, 0.44, cf_cz - 0.9), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Bakery_Flour_Dust", (0.7, 0.02, 1.1), (cf_cx - 1.3, 0.89, cf_cz - 0.9), bevel_width=0.01, material=mat_wall)
    create_beveled_cylinder("Bakery_Rolling_Pin", 0.04, 0.55, (cf_cx - 1.3, 0.93, cf_cz - 0.6), bevel_width=0.01, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_cylinder("Bakery_Baguette_1", 0.08, 0.65, (cf_cx - 1.3, 0.95, cf_cz - 1.3), bevel_width=0.02, rotation=(0.3, 0, 0.4), material=mat_bread)
    create_beveled_cylinder("Bakery_Baguette_2", 0.08, 0.65, (cf_cx - 1.3, 0.95, cf_cz - 1.0), bevel_width=0.02, rotation=(-0.2, 0, 0.3), material=mat_bread)
    create_beveled_cylinder("Bakery_Dough_Loaf", 0.16, 0.14, (cf_cx - 1.3, 0.95, cf_cz - 0.2), bevel_width=0.02, material=mat_bread)

    # Bàn ăn gỗ dài kèm 2 hàng ghế băng (Dining_Table_Long-col, Dining_Bench_L-col, Dining_Bench_R-col)
    create_beveled_box("Dining_Table_Long-col", (1.2, 0.85, 2.6), (cf_cx + 0.4, 0.42, cf_cz + 0.8), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Dining_Bench_L-col", (0.35, 0.45, 2.6), (cf_cx - 0.5, 0.22, cf_cz + 0.8), bevel_width=0.02, material=mat_wood)
    create_beveled_box("Dining_Bench_R-col", (0.35, 0.45, 2.6), (cf_cx + 1.3, 0.22, cf_cz + 0.8), bevel_width=0.02, material=mat_wood)

    # Kệ để bát đĩa gốm sứ (Dish_Shelf-col)
    create_beveled_box("Dish_Shelf-col", (2.4, 0.85, 0.30), (cf_cx - 0.4, 1.85, cf_cz - cf_l/2 + 0.35), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Dish_Plate_1", 0.18, 0.04, (cf_cx - 1.0, 1.88, cf_cz - cf_l/2 + 0.42), bevel_width=0.01, vertices=12, material=mat_wall)
    create_beveled_cylinder("Dish_Plate_2", 0.18, 0.04, (cf_cx - 0.5, 1.88, cf_cz - cf_l/2 + 0.42), bevel_width=0.01, vertices=12, material=mat_wall)
    create_beveled_cylinder("Dish_Bowl_1", 0.14, 0.10, (cf_cx + 0.1, 1.90, cf_cz - cf_l/2 + 0.42), bevel_width=0.01, vertices=12, material=mat_wall)
    create_beveled_cylinder("Dish_Bowl_2", 0.14, 0.10, (cf_cx + 0.6, 1.90, cf_cz - cf_l/2 + 0.42), bevel_width=0.01, vertices=12, material=mat_wall)

    # Xâu xúc xích treo trần (Sausages treo lơ lửng)
    create_beveled_box("Sausage_Rafter", (cf_w - 0.8, 0.16, 0.16), (cf_cx, 2.85, cf_cz), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Sausage_String_1", 0.08, 0.55, (cf_cx - 1.0, 2.45, cf_cz), bevel_width=0.02, rotation=(0.1, 0, 0.2), material=mat_sausage)
    create_beveled_cylinder("Sausage_String_2", 0.08, 0.55, (cf_cx, 2.48, cf_cz), bevel_width=0.02, rotation=(-0.1, 0, 0.1), material=mat_sausage)
    create_beveled_cylinder("Sausage_String_3", 0.08, 0.55, (cf_cx + 1.0, 2.42, cf_cz), bevel_width=0.02, rotation=(0.2, 0, -0.1), material=mat_sausage)

    # Thùng rượu gỗ (Wine_Cask_Big-col, Wine_Cask_Small-col)
    create_beveled_cylinder("Wine_Cask_Big-col", 0.48, 1.1, (cf_cx + cf_w/2 - 0.8, 0.55, cf_cz + cf_l/2 - 0.8), bevel_width=0.04, vertices=14, material=mat_wood_fence)
    create_beveled_cylinder("Wine_Cask_Small-col", 0.38, 0.85, (cf_cx + cf_w/2 - 1.6, 0.42, cf_cz + cf_l/2 - 0.8), bevel_width=0.03, vertices=12, material=mat_wood_fence)

    # 4.B ĐẦU BẾP GUSTEAU TẠI QUÁN ĂN (5.5, 0, 7.5)
    build_stylized_npc_at("NPC_Gusteau", mat_skin_fair, mat_npc_white, mat_pants_dark, mat_npc_black,
                          pos=(5.5, 0.0, 7.5), rot_y=-1.57, hat_type="chef", hat_m=mat_npc_white, tool_type="chef")

    # =========================================================================
    # 5. BẾN CẢNG NGƯ DÂN & NGƯ DÂN FINN (ĐÔNG: X = 13.5, Z = 7.5)
    # =========================================================================
    dk_cx, dk_cz = 13.5, 7.5
    create_beveled_box("Pier_Dock_Planks", (3.6, 0.2, 6.0), (dk_cx, 0.18, dk_cz), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Pier_Post_1", 0.16, 2.0, (dk_cx - 1.6, 0.0, dk_cz - 2.8), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Pier_Post_2", 0.16, 2.0, (dk_cx + 1.6, 0.0, dk_cz - 2.8), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Pier_Post_3", 0.16, 2.0, (dk_cx - 1.6, 0.0, dk_cz + 2.8), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Pier_Post_4", 0.16, 2.0, (dk_cx + 1.6, 0.0, dk_cz + 2.8), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("River_Water_Plane", (14.0, 0.02, 16.0), (dk_cx + 4.5, -0.05, dk_cz), bevel_width=0.01, material=mat_water)

    # Ngư Dân Finn tại bến cảng
    build_stylized_npc_at("NPC_Finn", mat_skin_tan, mat_kaki_shirt, mat_pants_blue, mat_apron_brown,
                          pos=(dk_cx, 0.18, dk_cz), rot_y=0.0, hat_type="bucket", hat_m=mat_kaki_shirt, tool_type="fisherman")

    # =========================================================================
    # 6. CHỢ TRUNG TÂM & GIẾNG NƯỚC (Z in [16, 31])
    # =========================================================================
    well_x, well_z = 0.0, 16.5
    create_beveled_cylinder("Well_Base_Cobble", 1.3, 1.0, (well_x, 0.5, well_z), bevel_width=0.04, vertices=16, material=mat_cobble)
    create_beveled_cylinder("Well_Water_Deep", 1.0, 0.1, (well_x, 0.7, well_z), bevel_width=0.01, material=mat_water)
    create_beveled_cylinder("Well_Post_L", 0.12, 2.4, (well_x - 1.1, 1.4, well_z), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Well_Post_R", 0.12, 2.4, (well_x + 1.1, 1.4, well_z), bevel_width=0.02, material=mat_wood)
    build_detailed_roof_gabled("Well_Roof", 2.6, 1.8, 0.8, (well_x, 2.5, well_z), overhang=0.2, ridge_along_x=True, material=mat_roof_red)

    ms_x = 0.0
    for i, sz in enumerate([24.0, 27.5]):
        create_beveled_box(f"Market_Stall_Table_{i+1}", (2.8, 0.85, 1.4), (ms_x, 0.42, sz), bevel_width=0.03, material=mat_wood)
        create_beveled_box(f"Market_Stall_Canopy_{i+1}", (3.2, 0.2, 1.8), (ms_x, 2.1, sz), bevel_width=0.04, material=mat_canopy_striped)
        create_beveled_box(f"Market_Produce_Box_{i+1}", (0.8, 0.3, 0.6), (ms_x - 0.6, 0.95, sz), bevel_width=0.02, material=mat_wood_fence)
        create_beveled_cylinder(f"Market_Barrel_{i+1}", 0.35, 0.75, (ms_x + 1.8, 0.38, sz), bevel_width=0.03, vertices=12, material=mat_wood_fence)

    cart_x, cart_z = -2.6, 18.8
    create_beveled_box("Cart_Body", (1.6, 0.5, 1.8), (cart_x, 0.55, cart_z), bevel_width=0.03, material=mat_wood)
    create_beveled_cylinder("Cart_Wheel_L", 0.42, 0.12, (cart_x - 0.9, 0.42, cart_z), bevel_width=0.03, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_cylinder("Cart_Wheel_R", 0.42, 0.12, (cart_x + 0.9, 0.42, cart_z), bevel_width=0.03, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_box("Cart_Crate_1", (0.6, 0.5, 0.6), (cart_x - 0.3, 0.9, cart_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Cart_Crate_2", (0.5, 0.4, 0.5), (cart_x + 0.3, 0.85, cart_z), bevel_width=0.03, material=mat_wood)

    # =========================================================================
    # 7. NHÀ RÈN CỦA THỢ RÈN VULCAN (TÂY: X = -11.0, Z = 21.0)
    # =========================================================================
    sm_cx, sm_cz = -11.0, 21.0
    sm_w, sm_l, sm_h = 6.6, 5.8, 3.8
    create_beveled_box("Floor_Smith", (sm_w, 0.15, sm_l), (sm_cx, 0.08, sm_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_Smith", (sm_w, sm_h, 0.3), (sm_cx, sm_h/2, sm_cz - sm_l/2 + 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_Smith", (sm_w, sm_h, 0.3), (sm_cx, sm_h/2, sm_cz + sm_l/2 - 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_West_Smith", (0.3, sm_h, sm_l - 0.6), (sm_cx - sm_w/2 + 0.15, sm_h/2, sm_cz), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Smith_L", (0.3, sm_h, 1.9), (sm_cx + sm_w/2 - 0.15, sm_h/2, sm_cz - 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Smith_R", (0.3, sm_h, 1.9), (sm_cx + sm_w/2 - 0.15, sm_h/2, sm_cz + 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Smith_Top", (0.3, 1.2, 2.0), (sm_cx + sm_w/2 - 0.15, sm_h - 0.6, sm_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Smith", sm_w, sm_l, 1.8, (sm_cx, sm_h, sm_cz), overhang=0.35, ridge_along_x=False, material=mat_roof_red)

    # Ống khói đá lớn
    create_beveled_box("Chimney_Smith_Base", (1.2, 5.4, 1.2), (sm_cx - sm_w/2 + 0.8, 2.7, sm_cz - sm_l/2 + 0.8), bevel_width=0.04, material=mat_cobble)

    # 7.A NỘI THẤT NHÀ RÈN (DIORAMA CẮT VÁCH CHUẨN ẢNH 1.JPG)
    # Lò rèn vòm đá gạch cao rực lửa cam đỏ (Blacksmith_Forge_Furnace-col, lửa phát quang)
    create_beveled_box("Blacksmith_Forge_Furnace-col", (1.8, 2.4, 1.6), (sm_cx - 1.6, 1.20, sm_cz - 1.5), bevel_width=0.04, material=mat_cobble)
    build_chamfered_rock("Blacksmith_Forge_Fire", (1.2, 0.55, 1.0), (sm_cx - 1.6, 0.90, sm_cz - 1.5), material=mat_lava_fire, seed_val=999)
    create_beveled_cylinder("Forge_Chimney_Flue", 0.35, 1.8, (sm_cx - 1.6, 2.5, sm_cz - 1.5), bevel_width=0.02, material=mat_cobble)

    # Đe sắt lớn (Anvil_Heavy-col) đặt trên bục gỗ tròn trung tâm
    create_beveled_cylinder("Anvil_Block_Center", 0.48, 0.65, (sm_cx, 0.32, sm_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Anvil_Heavy-col", (0.55, 0.35, 0.95), (sm_cx, 0.82, sm_cz), bevel_width=0.03, material=mat_metal)

    # Rương sắt chứa phôi thép vụn (Chest_Scrap_Metal-col)
    create_beveled_box("Chest_Scrap_Metal-col", (0.85, 0.55, 0.65), (sm_cx - 1.8, 0.28, sm_cz + 1.5), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Chest_Scrap_Lumps", (0.65, 0.22, 0.45), (sm_cx - 1.8, 0.60, sm_cz + 1.5), bevel_width=0.02, material=mat_metal_silver)

    # Rương gỗ chứa than củi (Chest_Charcoal-col)
    create_beveled_box("Chest_Charcoal-col", (0.85, 0.55, 0.65), (sm_cx - 0.7, 0.28, sm_cz + 1.5), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Chest_Charcoal_Lumps", (0.65, 0.20, 0.45), (sm_cx - 0.7, 0.58, sm_cz + 1.5), bevel_width=0.02, material=mat_npc_black)

    # Bể nước làm nguội tôi kim loại (Quench_Tank-col)
    create_beveled_box("Quench_Tank-col", (1.6, 0.75, 0.85), (sm_cx + 1.4, 0.38, sm_cz - 1.5), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Quench_Tank_Water", (1.4, 0.12, 0.65), (sm_cx + 1.4, 0.68, sm_cz - 1.5), bevel_width=0.01, material=mat_water)

    # Giá vũ khí trên tường đá có kiếm, khiên tròn, áo giáp sắt treo (Weapon_Rack_Wall-col)
    create_beveled_box("Weapon_Rack_Wall-col", (2.8, 1.00, 0.18), (sm_cx + 0.4, 1.85, sm_cz - sm_l/2 + 0.35), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Weapon_Rack_Sword_1", 0.04, 1.4, (sm_cx - 0.2, 1.85, sm_cz - sm_l/2 + 0.45), bevel_width=0.01, rotation=(0, 0, 0.75), material=mat_metal_silver)
    create_beveled_cylinder("Weapon_Rack_Sword_2", 0.04, 1.4, (sm_cx + 0.3, 1.85, sm_cz - sm_l/2 + 0.45), bevel_width=0.01, rotation=(0, 0, -0.75), material=mat_metal_silver)
    create_beveled_cylinder("Weapon_Rack_Shield", 0.40, 0.06, (sm_cx + 1.1, 1.85, sm_cz - sm_l/2 + 0.45), bevel_width=0.02, rotation=(1.57, 0, 0), vertices=16, material=mat_metal_gold)
    create_beveled_box("Weapon_Rack_Armor_Plate", (0.50, 0.65, 0.12), (sm_cx - 0.7, 1.85, sm_cz - sm_l/2 + 0.45), bevel_width=0.02, material=mat_metal_silver)

    # Bàn thợ nguội và công cụ kìm búa đe (Blacksmith_Workbench-col)
    create_beveled_box("Blacksmith_Workbench-col", (0.9, 0.88, 2.2), (sm_cx + 1.9, 0.44, sm_cz + 0.5), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Smith_Vise_Tool", (0.22, 0.25, 0.25), (sm_cx + 1.9, 0.98, sm_cz - 0.2), bevel_width=0.01, material=mat_metal)
    create_beveled_cylinder("Smith_Bench_Hammer", 0.03, 0.45, (sm_cx + 1.9, 0.90, sm_cz + 0.3), bevel_width=0.01, rotation=(0, 0, 1.57), material=mat_metal)
    create_beveled_cylinder("Smith_Bench_Tongs", 0.025, 0.50, (sm_cx + 1.9, 0.90, sm_cz + 0.8), bevel_width=0.01, rotation=(0, 0, 1.2), material=mat_metal)

    # 7.B ĐẠO CỤ VÀ THỢ RÈN VULCAN NGOÀI HIÊN (-6.8, 0, 20.0)
    out_x, out_z = -6.8, 20.0
    create_beveled_cylinder("Anvil_Outdoor_Log", 0.45, 0.7, (out_x, 0.35, out_z - 0.8), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Anvil_Outdoor_Iron", (0.55, 0.35, 0.9), (out_x, 0.82, out_z - 0.8), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Forge_Outdoor_Base", (1.4, 0.9, 1.2), (out_x - 1.2, 0.45, out_z - 1.8), bevel_width=0.04, material=mat_cobble)
    build_chamfered_rock("Forge_Outdoor_Fire", (1.0, 0.35, 0.8), (out_x - 1.2, 0.95, out_z - 1.8), material=mat_lava_fire, seed_val=888)

    build_stylized_npc_at("NPC_Vulcan", mat_skin_tan, mat_skin_tan, mat_pants_dark, mat_npc_black,
                          pos=(out_x, 0.0, out_z), rot_y=1.57, has_beard=True, beard_m=mat_npc_black, tool_type="blacksmith")

    # =========================================================================
    # 8. NHÀ GIẢ KIM CỦA ARIA (ĐÔNG: X = 11.0, Z = 21.0)
    # =========================================================================
    al_cx, al_cz = 11.0, 21.0
    al_w, al_l, al_h = 6.6, 5.8, 3.8
    create_beveled_box("Floor_Alchemist", (al_w, 0.15, al_l), (al_cx, 0.08, al_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_Alchemist", (al_w, al_h, 0.3), (al_cx, al_h/2, al_cz - al_l/2 + 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_Alchemist", (al_w, al_h, 0.3), (al_cx, al_h/2, al_cz + al_l/2 - 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_East_Alchemist", (0.3, al_h, al_l - 0.6), (al_cx + al_w/2 - 0.15, al_h/2, al_cz), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Alchemist_L", (0.3, al_h, 1.9), (al_cx - al_w/2 + 0.15, al_h/2, al_cz - 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Alchemist_R", (0.3, al_h, 1.9), (al_cx - al_w/2 + 0.15, al_h/2, al_cz + 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Alchemist_Top", (0.3, 1.2, 2.0), (al_cx - al_w/2 + 0.15, al_h - 0.6, al_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Alchemist", al_w, al_l, 1.8, (al_cx, al_h, al_cz), overhang=0.35, ridge_along_x=False, material=mat_roof_teal)

    # Ống khói & Khói ma thuật uốn lượn bay ra
    create_beveled_cylinder("Chimney_Alchemist", 0.38, 4.8, (al_cx + al_w/2 - 0.8, 2.4, al_cz - al_l/2 + 0.8), bevel_width=0.03, material=mat_cobble)
    build_chamfered_rock("Smoke_Alchemist_1", (1.1, 1.1, 1.1), (al_cx + al_w/2 - 0.8, 5.2, al_cz - al_l/2 + 0.8), material=mat_mystic_cyan, seed_val=111)
    build_chamfered_rock("Smoke_Alchemist_2", (1.4, 1.4, 1.4), (al_cx + al_w/2 - 0.5, 6.0, al_cz - al_l/2 + 0.6), material=mat_mystic_cyan, seed_val=222)
    build_chamfered_rock("Smoke_Alchemist_3", (1.8, 1.8, 1.8), (al_cx + al_w/2 - 0.2, 7.0, al_cz - al_l/2 + 0.4), material=mat_mystic_cyan, seed_val=333)

    # 8.A NỘI THẤT NHÀ GIẢ KIM (DIORAMA CẮT VÁCH CHUẨN ẢNH 1.JPG)
    # Vạc đồng ma thuật phát quang cyan bốc khói (Alchemist_Cauldron_Glowing-col)
    create_beveled_cylinder("Cauldron_Hearth_Stand", 0.65, 0.35, (al_cx, 0.18, al_cz), bevel_width=0.03, vertices=16, material=mat_cobble)
    create_beveled_cylinder("Cauldron_Magic_Fire", 0.55, 0.22, (al_cx, 0.12, al_cz), bevel_width=0.02, material=mat_mystic_purple)
    create_beveled_cylinder("Alchemist_Cauldron_Glowing-col", 0.70, 0.85, (al_cx, 0.72, al_cz), bevel_width=0.04, vertices=18, material=mat_metal)
    create_beveled_cylinder("Cauldron_Potion_Liquid", 0.58, 0.08, (al_cx, 1.05, al_cz), bevel_width=0.01, material=mat_mystic_cyan)
    build_chamfered_rock("Cauldron_Smoke_1", (0.42, 0.42, 0.42), (al_cx, 1.35, al_cz), material=mat_mystic_cyan, seed_val=444)
    build_chamfered_rock("Cauldron_Smoke_2", (0.55, 0.55, 0.55), (al_cx + 0.15, 1.70, al_cz - 0.1), material=mat_mystic_cyan, seed_val=555)

    # Bàn thí nghiệm sách mở (Alchemy_Desk_Main-col)
    create_beveled_box("Alchemy_Desk_Main-col", (2.2, 0.88, 1.0), (al_cx - 1.2, 0.44, al_cz - al_l/2 + 0.9), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Alchemy_Open_Book_Base", (0.45, 0.06, 0.35), (al_cx - 1.2, 0.91, al_cz - al_l/2 + 0.9), bevel_width=0.01, material=mat_wood_fence)
    create_beveled_box("Alchemy_Book_Pages", (0.42, 0.05, 0.32), (al_cx - 1.2, 0.94, al_cz - al_l/2 + 0.9), bevel_width=0.01, material=mat_wall)
    create_beveled_cylinder("Alchemy_Flask_Cyan", 0.08, 0.22, (al_cx - 1.8, 1.00, al_cz - al_l/2 + 0.8), bevel_width=0.01, material=mat_mystic_cyan)
    create_beveled_cylinder("Alchemy_Flask_Pink", 0.08, 0.22, (al_cx - 0.6, 1.00, al_cz - al_l/2 + 0.8), bevel_width=0.01, material=mat_mystic_pink)
    create_beveled_cylinder("Alchemy_Flask_Yellow", 0.07, 0.18, (al_cx - 0.8, 0.98, al_cz - al_l/2 + 1.1), bevel_width=0.01, material=mat_wheat)

    # Tủ sách cổ ma thuật kịch trần (Alchemist_Bookshelf_Tall-col)
    create_beveled_box("Alchemist_Bookshelf_Tall-col", (2.2, 2.7, 0.55), (al_cx - al_w/2 + 0.65, 1.35, al_cz), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Book_Row_1", (1.8, 0.45, 0.38), (al_cx - al_w/2 + 0.65, 0.65, al_cz), bevel_width=0.02, material=mat_roof_red)
    create_beveled_box("Book_Row_2", (1.8, 0.45, 0.38), (al_cx - al_w/2 + 0.65, 1.35, al_cz), bevel_width=0.02, material=mat_roof_teal)
    create_beveled_box("Book_Row_3", (1.8, 0.45, 0.38), (al_cx - al_w/2 + 0.65, 2.05, al_cz), bevel_width=0.02, material=mat_mystic_purple)
    create_beveled_cylinder("Scroll_Bundle", 0.14, 0.65, (al_cx - al_w/2 + 0.65, 2.45, al_cz), bevel_width=0.02, rotation=(0, 0, 1.57), material=mat_wall)

    # Kệ chai lọ độc dược đủ màu (Potion_Wall_Shelf-col)
    create_beveled_box("Potion_Wall_Shelf-col", (2.6, 0.80, 0.25), (al_cx + al_w/2 - 0.35, 1.85, al_cz + 1.0), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Potion_Bottle_Red", 0.09, 0.25, (al_cx + al_w/2 - 0.4, 2.05, al_cz + 0.3), bevel_width=0.01, material=mat_roof_red)
    create_beveled_cylinder("Potion_Bottle_Purple", 0.09, 0.25, (al_cx + al_w/2 - 0.4, 2.05, al_cz + 0.7), bevel_width=0.01, material=mat_mystic_purple)
    create_beveled_cylinder("Potion_Bottle_Cyan", 0.09, 0.25, (al_cx + al_w/2 - 0.4, 2.05, al_cz + 1.1), bevel_width=0.01, material=mat_mystic_cyan)
    create_beveled_cylinder("Potion_Bottle_Teal", 0.09, 0.25, (al_cx + al_w/2 - 0.4, 2.05, al_cz + 1.5), bevel_width=0.01, material=mat_roof_teal)

    # Chùm thảo mộc khô treo lơ lửng từ xà nhà (Hanging_Herbs-col)
    create_beveled_box("Hanging_Herbs_Rafter", (al_w - 0.8, 0.16, 0.16), (al_cx, 2.95, al_cz), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Hanging_Herbs-col", 0.18, 0.55, (al_cx - 1.0, 2.45, al_cz), bevel_width=0.02, rotation=(0.1, 0, 0.1), material=mat_vegetable)
    create_beveled_cylinder("Hanging_Herbs_Bundle_2", 0.18, 0.55, (al_cx, 2.48, al_cz), bevel_width=0.02, rotation=(-0.1, 0, 0.1), material=mat_wheat)
    create_beveled_cylinder("Hanging_Herbs_Bundle_3", 0.18, 0.55, (al_cx + 1.0, 2.42, al_cz), bevel_width=0.02, rotation=(0.1, 0, -0.1), material=mat_vegetable)

    # 8.B ĐẠO CỤ VÀ NHÀ GIẢ KIM ARIA TẠI VỊ TRÍ NPC (7.5, 0, 21.0)
    create_beveled_box("Herb_Bed_1", (1.2, 0.35, 3.2), (al_cx - al_w/2 - 0.8, 0.18, al_cz + 1.2), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("Herb_Soil_1", (1.0, 0.10, 3.0), (al_cx - al_w/2 - 0.8, 0.36, al_cz + 1.2), bevel_width=0.02, material=mat_vegetable)

    build_stylized_npc_at("NPC_Aria", mat_skin_fair, mat_mystic_purple, mat_mystic_purple, mat_npc_black,
                          pos=(7.5, 0.0, 21.0), rot_y=-1.57, hat_type="hood", hat_m=mat_mystic_purple, tool_type="alchemist")

    # =========================================================================
    # 9. NHÀ DÂN CƯ (TÂY: X = -10.0, Z = 28.5)
    # =========================================================================
    hs_cx, hs_cz = -10.0, 28.5
    hs_w, hs_l, hs_h = 6.0, 5.4, 3.6
    create_beveled_box("Floor_House", (hs_w, 0.15, hs_l), (hs_cx, 0.08, hs_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Wall_North_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz - hs_l/2 + 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz + hs_l/2 - 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_West_House", (0.3, hs_h, hs_l - 0.6), (hs_cx - hs_w/2 + 0.15, hs_h/2, hs_cz), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_L", (0.3, hs_h, 1.8), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz - 1.5), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_R", (0.3, hs_h, 1.8), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz + 1.5), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_Top", (0.3, 1.1, 1.8), (hs_cx + hs_w/2 - 0.15, hs_h - 0.55, hs_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_House", hs_w, hs_l, 1.8, (hs_cx, hs_h, hs_cz), overhang=0.35, ridge_along_x=False, material=mat_roof_red)

    # 9.A NỘI THẤT NHÀ DÂN (DIORAMA CẮT VÁCH CHUẨN ẢNH 1.JPG)
    # Giường ngủ gỗ nệm đỏ gối trắng ấm cúng (House_Cozy_Bed-col)
    create_beveled_box("House_Cozy_Bed-col", (1.7, 0.55, 2.3), (hs_cx - hs_w/2 + 1.2, 0.28, hs_cz - hs_l/2 + 1.5), bevel_width=0.03, material=mat_wood)
    create_beveled_box("House_Bed_Mattress", (1.5, 0.25, 2.1), (hs_cx - hs_w/2 + 1.2, 0.60, hs_cz - hs_l/2 + 1.5), bevel_width=0.03, material=mat_roof_red)
    create_beveled_box("House_Bed_Pillow", (0.9, 0.16, 0.45), (hs_cx - hs_w/2 + 1.2, 0.76, hs_cz - hs_l/2 + 0.7), bevel_width=0.02, material=mat_wall)

    # Tủ quần áo 2 cánh cao lớn (House_Wardrobe_Tall-col)
    create_beveled_box("House_Wardrobe_Tall-col", (1.4, 2.4, 0.70), (hs_cx - hs_w/2 + 0.90, 1.20, hs_cz + hs_l/2 - 0.7), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("House_Wardrobe_Door_L", (0.60, 2.1, 0.04), (hs_cx - hs_w/2 + 0.58, 1.20, hs_cz + hs_l/2 - 0.33), bevel_width=0.015, material=mat_wood)
    create_beveled_box("House_Wardrobe_Door_R", (0.60, 2.1, 0.04), (hs_cx - hs_w/2 + 1.22, 1.20, hs_cz + hs_l/2 - 0.33), bevel_width=0.015, material=mat_wood)
    create_beveled_cylinder("House_Wardrobe_Handle_L", 0.02, 0.12, (hs_cx - hs_w/2 + 0.85, 1.20, hs_cz + hs_l/2 - 0.30), bevel_width=0.005, material=mat_metal_gold)
    create_beveled_cylinder("House_Wardrobe_Handle_R", 0.02, 0.12, (hs_cx - hs_w/2 + 0.95, 1.20, hs_cz + hs_l/2 - 0.30), bevel_width=0.005, material=mat_metal_gold)

    # Tấm thảm sàn dệt thổ cẩm sọc kẻ (House_Floor_Rug-col)
    create_beveled_box("House_Floor_Rug-col", (2.4, 0.02, 2.2), (hs_cx + 0.4, 0.09, hs_cz), bevel_width=0.01, material=mat_canopy_striped)

    # Bàn con bên cửa sổ có rèm vải xanh (House_Side_Table-col)
    create_beveled_cylinder("House_Side_Table-col", 0.55, 0.80, (hs_cx + 1.4, 0.40, hs_cz + 1.3), bevel_width=0.02, vertices=14, material=mat_wood)
    create_beveled_cylinder("House_Side_Stool", 0.25, 0.48, (hs_cx + 1.4, 0.24, hs_cz + 0.5), bevel_width=0.02, vertices=10, material=mat_wood)
    create_beveled_cylinder("House_Flower_Vase", 0.10, 0.25, (hs_cx + 1.4, 0.92, hs_cz + 1.3), bevel_width=0.01, material=mat_wall)

    # Rèm cửa vải xanh trên tường South
    create_beveled_box("House_Window_Frame", (1.4, 1.2, 0.08), (hs_cx + 1.4, 1.80, hs_cz + hs_l/2 - 0.25), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("House_Window_Curtain_L", (0.4, 1.1, 0.06), (hs_cx + 0.9, 1.80, hs_cz + hs_l/2 - 0.22), bevel_width=0.02, material=mat_roof_teal)
    create_beveled_box("House_Window_Curtain_R", (0.4, 1.1, 0.06), (hs_cx + 1.9, 1.80, hs_cz + hs_l/2 - 0.22), bevel_width=0.02, material=mat_roof_teal)

    # =========================================================================
    # 10. KHU LÂM NGHIỆP CỦA TIỀU PHU GROVER (TÂY BẮC: X = -14.0, Z = 38.0)
    # =========================================================================
    lm_cx, lm_cz = -14.0, 38.0
    create_beveled_cylinder("Lumber_P1", 0.18, 3.2, (lm_cx - 2.5, 1.6, lm_cz - 2.0), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Lumber_P2", 0.18, 3.2, (lm_cx + 2.5, 1.6, lm_cz - 2.0), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Lumber_P3", 0.18, 3.2, (lm_cx - 2.5, 1.6, lm_cz + 2.0), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Lumber_P4", 0.18, 3.2, (lm_cx + 2.5, 1.6, lm_cz + 2.0), bevel_width=0.02, material=mat_wood)
    build_detailed_roof_gabled("Lumber_Shed_Roof", 5.6, 4.6, 1.0, (lm_cx, 3.2, lm_cz), overhang=0.25, ridge_along_x=True, material=mat_wood_fence)

    create_beveled_box("Lumber_Saw_Table", (3.2, 0.85, 1.4), (lm_cx, 0.42, lm_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_cylinder("Lumber_Saw_Blade", 0.45, 0.04, (lm_cx, 0.95, lm_cz), bevel_width=0.01, rotation=(1.57, 0, 0), material=mat_metal)

    for i in range(3):
        create_beveled_cylinder(f"Log_Pile_Bot_{i}", 0.32, 4.0, (lm_cx + 4.0, 0.32, lm_cz - 1.2 + i * 0.75), bevel_width=0.03, rotation=(1.57, 0, 0), material=mat_wood)
    for i in range(2):
        create_beveled_cylinder(f"Log_Pile_Top_{i}", 0.30, 4.0, (lm_cx + 4.0, 0.85, lm_cz - 0.85 + i * 0.75), bevel_width=0.03, rotation=(1.57, 0, 0), material=mat_wood)

    create_beveled_cylinder("NPC_Grover_Chopping_Block", 0.40, 0.60, (-13.5, 0.30, 35.8), bevel_width=0.03, vertices=12, material=mat_wood)

    # Tiều phu Grover tại khu lâm nghiệp
    build_stylized_npc_at("NPC_Grover", mat_skin_tan, mat_plaid_red, mat_pants_blue, mat_npc_black,
                          pos=(-13.5, 0.0, 36.5), rot_y=0.8, has_beard=True, beard_m=mat_farmer_brown, hat_type="beanie", hat_m=mat_roof_red, tool_type="lumberjack")

    build_stylized_tree("Tree_Lumber_1", (lm_cx - 4.5, 0, lm_cz - 3.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Lumber_2", (lm_cx - 4.0, 0, lm_cz + 3.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Lumber_3", (lm_cx, 0, lm_cz + 4.5), scale=1.4, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # =========================================================================
    # 11. KHU MỎ ĐÁ CỦA THỢ MỎ BROCK (ĐÔNG BẮC: X = 14.0, Z = 38.0)
    # =========================================================================
    mn_cx, mn_cz = 14.0, 38.0
    build_chamfered_rock("Mine_Cliff_Main", (13.0, 7.5, 8.0), (mn_cx, 3.75, mn_cz + 3.0), material=mat_stone, seed_val=333)
    build_chamfered_rock("Mine_Cliff_Ledge", (6.5, 5.0, 4.0), (mn_cx - 4.5, 2.5, mn_cz + 0.5), material=mat_stone, seed_val=444)
    create_beveled_box("Mine_Entrance_Void", (2.8, 3.2, 1.2), (mn_cx, 1.6, mn_cz - 0.9), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Mine_Beam_L", (0.35, 3.4, 0.4), (mn_cx - 1.5, 1.7, mn_cz - 0.9), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Mine_Beam_R", (0.35, 3.4, 0.4), (mn_cx + 1.5, 1.7, mn_cz - 0.9), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Mine_Beam_Top", (3.6, 0.35, 0.4), (mn_cx, 3.2, mn_cz - 0.9), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_cylinder("Ore_Furnace", 1.3, 2.6, (mn_cx - 4.2, 1.3, mn_cz - 2.5), bevel_width=0.04, vertices=16, material=mat_cobble)
    create_beveled_box("Ore_Furnace_Fire", (0.8, 0.6, 0.5), (mn_cx - 4.2, 0.6, mn_cz - 1.8), bevel_width=0.02, material=mat_lava_fire)
    create_beveled_box("Rail_L", (0.08, 0.08, 4.5), (mn_cx + 2.0, 0.06, mn_cz - 1.0), bevel_width=0.01, material=mat_metal)
    create_beveled_box("Rail_R", (0.08, 0.08, 4.5), (mn_cx + 2.8, 0.06, mn_cz - 1.0), bevel_width=0.01, material=mat_metal)
    create_beveled_box("Minecart_Body", (1.2, 0.65, 1.6), (mn_cx + 2.4, 0.58, mn_cz - 1.5), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Minecart_Ore", (0.9, 0.3, 1.3), (mn_cx + 2.4, 0.88, mn_cz - 1.5), bevel_width=0.03, material=mat_stone)

    build_chamfered_rock("NPC_Brock_Ore_Cluster", (0.8, 0.5, 0.8), (12.5, 0.25, 37.5), material=mat_stone, seed_val=777)

    # Thợ mỏ Brock tại khu mỏ đá
    build_stylized_npc_at("NPC_Brock", mat_skin_tan, mat_miner_suit, mat_miner_suit, mat_npc_black,
                          pos=(12.5, 0.0, 36.5), rot_y=-0.8, has_beard=True, beard_m=mat_farmer_brown, hat_type="hard_hat", hat_m=mat_hard_hat_yellow, tool_type="miner")

    # =========================================================================
    # 12. CÂY CỐI TRANG TRÍ BAO QUANH LÀNG
    # =========================================================================
    build_stylized_tree("Tree_Gate_L", (-5.0, 0, 5.0), scale=1.1, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Gate_R", (5.5, 0, 4.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Smith_Back", (-18.5, 0, 14.0), scale=1.0, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Alchemist_Back", (16.5, 0, 16.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_House_South", (-17.0, 0, 32.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Mine_East", (18.5, 0, 35.0), scale=1.5, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # =========================================================================
    # 13. RENDER MẮT THẦN ĐA GÓC (VILLAGE OVERVIEW & 4 PHÒNG DIORAMA CẮT VÁCH)
    # =========================================================================
    temp_dir = os.path.join(workspace_dir, "Assets", "Models", "_temp_previews")
    os.makedirs(temp_dir, exist_ok=True)

    # 13.A Render Toàn Cảnh Làng
    p_village = os.path.join(temp_dir, "preview_village.png")
    setup_preview_render(p_village, resolution=(1280, 800), camera_pos=(-26, -34, 22), target_pos=(0, -18, 1), ortho_scale=46.0)

    # 13.B Render 4 Căn Phòng Nội Thất Cắt Vách (Ẩn tạm thời mái nhà để soi nội thất)
    roof_nodes = ["Roof_Smith", "Roof_Alchemist", "Roof_Chef", "Roof_House"]
    wall_front_nodes = [
        "Wall_Front_Smith_L", "Wall_Front_Smith_R", "Wall_Front_Smith_Top", "Wall_South_Smith", "Wall_West_Smith",
        "Wall_Front_Alchemist_L", "Wall_Front_Alchemist_R", "Wall_Front_Alchemist_Top", "Wall_South_Alchemist",
        "Wall_Front_Chef_L", "Wall_Front_Chef_R", "Wall_Front_Chef_Top", "Wall_South_Chef",
        "Wall_Front_House_L", "Wall_Front_House_R", "Wall_Front_House_Top", "Wall_South_House", "Wall_West_House"
    ]

    tree_objs = [obj for obj in bpy.data.objects if 'Tree' in obj.name or 'Foliage' in obj.name]
    for obj in tree_objs:
        obj.hide_render = True
    for name in roof_nodes + wall_front_nodes:
        obj = bpy.data.objects.get(name)
        if obj:
            obj.hide_render = True

    # Render Nội Thất Nhà Rèn
    p_smith = os.path.join(temp_dir, "preview_interior_smith.png")
    setup_preview_render(p_smith, resolution=(640, 480), camera_pos=(-11 - 5.5, -21 - 5.5, 7.2), target_pos=(-11.0, -21.0, 1.3), ortho_scale=7.2)

    # Render Nội Thất Nhà Giả Kim
    p_alchemist = os.path.join(temp_dir, "preview_interior_alchemist.png")
    setup_preview_render(p_alchemist, resolution=(640, 480), camera_pos=(11 - 5.5, -21 - 5.5, 7.2), target_pos=(11.0, -21.0, 1.3), ortho_scale=7.2)

    # Render Nội Thất Quán Ăn / Nhà Bếp
    p_chef = os.path.join(temp_dir, "preview_interior_chef.png")
    setup_preview_render(p_chef, resolution=(640, 480), camera_pos=(8 - 5.5, -7.5 - 5.5, 7.2), target_pos=(8.0, -7.5, 1.3), ortho_scale=7.2)

    # Render Nội Thất Nhà Dân Cư
    p_house = os.path.join(temp_dir, "preview_interior_house.png")
    setup_preview_render(p_house, resolution=(640, 480), camera_pos=(-10 - 5.5, -28.5 - 5.5, 7.2), target_pos=(-10.5, -28.5, 1.3), ortho_scale=7.2)

    # Khôi phục hiển thị mái, vách và cây cối trước khi xuất GLB cho Godot
    for obj in tree_objs:
        obj.hide_render = False
    for name in roof_nodes + wall_front_nodes:
        obj = bpy.data.objects.get(name)
        if obj:
            obj.hide_render = False

    # =========================================================================
    # 14. XUẤT RA GLB & LƯU FILE BLEND AN TOÀN
    # =========================================================================
    out_glb = os.path.join(workspace_dir, "Assets", "Models", "village_map.glb")
    print(f"Xuất mô hình sang: {out_glb}")
    bpy.ops.export_scene.gltf(
        filepath=out_glb,
        export_format='GLB',
        export_yup=True,
        export_apply=True,
        export_materials='EXPORT'
    )
    blend_path = os.path.join(workspace_dir, "Assets", "Blender_Source", "village_map.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Lưu file blend: {blend_path}")

    print("=== DỰNG BẢN ĐỒ LÀNG MỞ RỘNG HOÀN TẤT VỚI CHẤT LƯỢNG CAO ===")

if __name__ == '__main__':
    build_village()
