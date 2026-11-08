"""
Script Blender 3D: Dựng Bản Đồ Làng Mở Rộng Hoàn Thiện Cực Hạn (tools/build_village_map.py)
Dự án: Trò Chơi Mới - Antigravity Pipeline
Quy chuẩn Kỹ Thuật:
- Khắc phục triệt để lỗi xuyên tường (Anti-Wall Clipping): Mọi vách tường 4 phòng hiện tại và công trình mới
  đều là khối hộp đặc có độ dày >= 0.40m và mang hậu tố '-col' để Godot sinh collider vật lý chuẩn 100%.
- Bổ sung công trình thứ 5: Nhà Trưởng Làng / Nhà Kho Dự Trữ Lương Thực (Elder Hall & Village Storehouse)
  kèm thềm đá, bậc thang, bàn làm việc trưởng làng, cờ hiệu làng, thùng gỗ, bao tải lúa mì, rương ngân khố.
- Dựng hệ thống 10 Trụ Đèn Đường Làng (Street Lanterns) dọc từ Cổng Làng đến Chợ và Bến Cảng với Mat_Lantern_Glow.
- Tăng cường chi tiết cực hạn: Giàn hoa, chậu cây, xe đẩy hàng, thùng rượu, giỏ cá bến cảng, quặng pha lê mỏ đá, củi xẻ tiều phu.
- Trải UV tự động (unwrap_mesh) 100% mesh mới và tuân thủ Human Reference Scale.
- Xuất GLB 'Assets/Models/village_map.glb' và lưu 'Assets/Blender_Source/village_map.blend'.
- Render ảnh mắt thần toàn cảnh và 5 phòng diorama nội thất cắt vách.
"""

import sys
import os
import bpy
import math

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
    print("=== BẮT ĐẦU DỰNG BẢN ĐỒ LÀNG MỞ RỘNG CỰC HẠN (ANTI-WALL CLIPPING & 5 CÔNG TRÌNH) ===")
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
    mat_flower_red = create_material("Mat_Flower_Red", (0.92, 0.18, 0.22), roughness=0.70)
    mat_flower_yellow = create_material("Mat_Flower_Yellow", (0.96, 0.85, 0.18), roughness=0.70)
    mat_wheat = create_material("Mat_Wheat", (0.90, 0.75, 0.29), roughness=0.85)
    mat_bread = create_material("Mat_Bread", (0.83, 0.58, 0.29), roughness=0.70)
    mat_wall = create_material("Mat_Wall_Stone", (0.82, 0.80, 0.76), roughness=0.85)
    mat_water = create_material("Mat_Water", (0.18, 0.65, 0.72), roughness=0.15, emission_color=(0.18, 0.65, 0.72), emission_strength=0.9)
    mat_sausage = create_material("Mat_Sausage", (0.72, 0.24, 0.18), roughness=0.60)
    mat_cheese = create_material("Mat_Cheese", (0.95, 0.82, 0.25), roughness=0.60)
    mat_glass = create_material("Mat_Glass", (0.85, 0.92, 0.95), roughness=0.10)
    mat_leather_book = create_material("Mat_Leather_Book", (0.35, 0.18, 0.12), roughness=0.70)
    mat_brass = create_material("Mat_Brass", (0.85, 0.65, 0.22), roughness=0.35, metallic=0.85)
    mat_fabric_blue = create_material("Mat_Fabric_Blue", (0.20, 0.45, 0.68), roughness=0.85)
    mat_glowing_iron = create_material("Mat_Glowing_Iron", (1.00, 0.35, 0.05), roughness=0.30, emission_color=(1.00, 0.35, 0.05), emission_strength=4.5)

    # Đèn lồng phát quang ấm áp
    mat_lantern_glow = create_material("Mat_Lantern_Glow", (1.00, 0.85, 0.45), roughness=0.20, emission_color=(1.00, 0.85, 0.40), emission_strength=4.5)

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

        create_beveled_box(f"{prefix}_Eye_L", (0.04, 0.06, 0.02), local_to_world(-0.08, 1.58, 0.17), bevel_width=0.005, rotation=(0, rot_y, 0), material=mat_npc_black)
        create_beveled_box(f"{prefix}_Eye_R", (0.04, 0.06, 0.02), local_to_world(0.08, 1.58, 0.17), bevel_width=0.005, rotation=(0, rot_y, 0), material=mat_npc_black)

        if has_beard and beard_m:
            create_beveled_box(f"{prefix}_Beard", (0.36, 0.18, 0.18), local_to_world(0.0, 1.45, 0.10), bevel_width=0.02, rotation=(0, rot_y, 0), material=beard_m)

        # 5. Mũ nón chuyên ngành
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

        # 6. Đạo cụ cầm tay
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
    # HÀM DỰNG TRỤ ĐÈN ĐƯỜNG LÀNG PHÁT QUANG ẤM ÁP (STREET LANTERNS)
    # =========================================================================
    def build_street_lantern(name, location, arm_dir_x=1.0):
        gx, gy, gz = location
        # Chân đế đá
        create_beveled_box(f"{name}_Base-col", (0.42, 0.35, 0.42), (gx, gy + 0.175, gz), bevel_width=0.03, material=mat_cobble)
        # Thân cột đèn
        create_beveled_cylinder(f"{name}_Post-col", 0.09, 3.1, (gx, gy + 1.725, gz), bevel_width=0.015, material=mat_wood_fence)
        # Khuyên đai sắt gia cố cột
        create_beveled_cylinder(f"{name}_Iron_Band_1", 0.105, 0.06, (gx, gy + 1.2, gz), bevel_width=0.008, material=mat_metal)
        create_beveled_cylinder(f"{name}_Iron_Band_2", 0.105, 0.06, (gx, gy + 2.5, gz), bevel_width=0.008, material=mat_metal)
        # Tay xà ngang vươn ra treo đèn
        arm_len = 0.65
        arm_cx = gx + (arm_dir_x * arm_len / 2.0)
        create_beveled_box(f"{name}_Arm", (arm_len, 0.10, 0.10), (arm_cx, gy + 3.25, gz), bevel_width=0.015, material=mat_metal)
        # Móc xích sắt
        lantern_x = gx + (arm_dir_x * (arm_len - 0.08))
        create_beveled_cylinder(f"{name}_Chain", 0.015, 0.18, (lantern_x, gy + 3.12, gz), bevel_width=0.004, material=mat_metal)
        # Khung lồng đèn & nắp chóp kim loại
        create_beveled_cylinder(f"{name}_Cap", 0.22, 0.08, (lantern_x, gy + 3.02, gz), bevel_width=0.02, vertices=8, material=mat_metal)
        create_beveled_cylinder(f"{name}_Bottom", 0.18, 0.06, (lantern_x, gy + 2.62, gz), bevel_width=0.015, vertices=8, material=mat_metal)
        # Lõi đèn phát quang rực rỡ Mat_Lantern_Glow
        build_chamfered_rock(f"{name}_Glow_Core", (0.24, 0.32, 0.24), (lantern_x, gy + 2.82, gz), material=mat_lantern_glow, seed_val=int(abs(gx)*100 + abs(gz)))

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
    create_beveled_box("Path_To_Elder", (3.6, 0.04, 4.0), (0.0, 0.02, 34.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_To_Lumber", (2.8, 0.04, 11.0), (-12.0, 0.02, 36.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_To_Mine", (2.8, 0.04, 11.0), (12.0, 0.02, 36.0), bevel_width=0.02, material=mat_dirt)

    # =========================================================================
    # 3. CỔNG LÀNG, VƯỜN RAU CẢI & 2 LÍNH CANH GÁC CỔNG
    # =========================================================================
    gate_z = 8.5
    create_beveled_cylinder("Gate_Post_L-col", 0.24, 4.0, (-2.0, 2.0, gate_z), bevel_width=0.03, material=mat_wood)
    create_beveled_cylinder("Gate_Post_R-col", 0.24, 4.0, (2.0, 2.0, gate_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Gate_Beam_Top-col", (4.6, 0.35, 0.35), (0.0, 3.8, gate_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Gate_Signboard", (2.4, 0.7, 0.12), (0.0, 3.1, gate_z), bevel_width=0.02, material=mat_wood)

    for side in [-1, 1]:
        for i in range(4):
            fx = side * (2.8 + i * 1.5)
            create_beveled_cylinder(f"Fence_Gate_{side}_{i}-col", 0.11, 1.3, (fx, 0.65, gate_z), bevel_width=0.02, material=mat_wood_fence)
            create_beveled_box(f"Fence_Rail_Top_{side}_{i}-col", (1.6, 0.08, 0.08), (fx - side * 0.75, 1.0, gate_z), bevel_width=0.015, material=mat_wood_fence)
            create_beveled_box(f"Fence_Rail_Bot_{side}_{i}-col", (1.6, 0.08, 0.08), (fx - side * 0.75, 0.5, gate_z), bevel_width=0.015, material=mat_wood_fence)

    # 3.A 2 LÍNH CANH GÁC CỔNG
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
    # TƯỜNG DÀY 0.42M & MANG HẬU TỐ '-col' CHỐNG XUYÊN TƯỜNG TRIỆT ĐỂ
    # =========================================================================
    cf_cx, cf_cz = 8.0, 7.5
    cf_w, cf_l, cf_h = 6.2, 5.4, 3.6
    wall_th = 0.42

    create_beveled_box("Floor_Chef-col", (cf_w, 0.18, cf_l), (cf_cx, 0.09, cf_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_Chef-col", (cf_w, cf_h, wall_th), (cf_cx, cf_h/2, cf_cz - cf_l/2 + wall_th/2), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_Chef-col", (cf_w, cf_h, wall_th), (cf_cx, cf_h/2, cf_cz + cf_l/2 - wall_th/2), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_East_Chef-col", (wall_th, cf_h, cf_l - wall_th*2), (cf_cx + cf_w/2 - wall_th/2, cf_h/2, cf_cz), bevel_width=0.03, material=mat_wall)
    # Cửa vào hướng Tây: Mở rộng cửa 1.8m, tường 2 bên dày 0.42m
    create_beveled_box("Wall_Front_Chef_L-col", (wall_th, cf_h, 1.8), (cf_cx - cf_w/2 + wall_th/2, cf_h/2, cf_cz - 1.5), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Chef_R-col", (wall_th, cf_h, 1.8), (cf_cx - cf_w/2 + wall_th/2, cf_h/2, cf_cz + 1.5), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Chef_Top-col", (wall_th, 1.1, 1.8), (cf_cx - cf_w/2 + wall_th/2, cf_h - 0.55, cf_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Chef", cf_w, cf_l, 1.8, (cf_cx, cf_h, cf_cz), overhang=0.35, ridge_along_x=False, material=mat_roof_red)

    # 4.A NỘI THẤT QUÁN ĂN / NHÀ BẾP
    oven_x = cf_cx + cf_w/2 - 1.25
    oven_z = cf_cz - cf_l/2 + 1.25
    create_beveled_cylinder("Bakery_Brick_Oven-col", 0.95, 1.8, (oven_x, 0.90, oven_z), bevel_width=0.04, vertices=18, material=mat_cobble)
    create_beveled_box("Bakery_Oven_Arch_Trim", (0.22, 0.70, 0.85), (oven_x - 0.85, 0.65, oven_z), bevel_width=0.02, material=mat_roof_red)
    create_beveled_box("Bakery_Oven_Mouth", (0.35, 0.55, 0.65), (oven_x - 0.70, 0.60, oven_z), bevel_width=0.02, material=mat_npc_black)
    build_chamfered_rock("Bakery_Oven_Glowing_Coals", (0.70, 0.35, 0.60), (oven_x - 0.55, 0.45, oven_z), material=mat_lava_fire, seed_val=666)
    create_beveled_box("Bakery_Baking_Loaf_1", (0.18, 0.12, 0.24), (oven_x - 0.55, 0.55, oven_z - 0.15), bevel_width=0.02, material=mat_bread)
    create_beveled_box("Bakery_Baking_Loaf_2", (0.18, 0.12, 0.24), (oven_x - 0.55, 0.55, oven_z + 0.15), bevel_width=0.02, material=mat_bread)
    create_beveled_cylinder("Bakery_Oven_Flue", 0.30, 1.8, (oven_x, 2.3, oven_z), bevel_width=0.02, material=mat_cobble)
    create_beveled_cylinder("Bakery_Bread_Peel_Handle", 0.025, 1.6, (oven_x - 1.0, 0.85, oven_z - 0.75), bevel_width=0.005, rotation=(0.3, 0, 0), material=mat_wood)
    create_beveled_box("Bakery_Bread_Peel_Paddle", (0.04, 0.30, 0.25), (oven_x - 1.0, 0.20, oven_z - 0.95), bevel_width=0.01, material=mat_wood)
    create_beveled_cylinder("Bakery_Stew_Pot", 0.24, 0.28, (oven_x - 0.3, 1.85, oven_z), bevel_width=0.02, material=mat_metal)

    prep_x = cf_cx - 1.3
    prep_z = cf_cz - 0.9
    create_beveled_box("Bakery_Prep_Table-col", (1.2, 0.88, 2.4), (prep_x, 0.44, prep_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Bakery_Flour_Dust", (0.75, 0.02, 1.2), (prep_x, 0.89, prep_z), bevel_width=0.01, material=mat_wall)
    create_beveled_cylinder("Bakery_Rolling_Pin", 0.04, 0.55, (prep_x, 0.93, prep_z - 0.5), bevel_width=0.01, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_box("Bakery_Baguette_Basket", (0.50, 0.22, 0.65), (prep_x, 0.96, prep_z - 0.85), bevel_width=0.02, material=mat_wheat)
    create_beveled_cylinder("Bakery_Baguette_1", 0.07, 0.70, (prep_x - 0.1, 1.12, prep_z - 0.85), bevel_width=0.02, rotation=(0.4, 0, 0.3), material=mat_bread)
    create_beveled_cylinder("Bakery_Baguette_2", 0.07, 0.70, (prep_x + 0.1, 1.10, prep_z - 0.85), bevel_width=0.02, rotation=(-0.3, 0, 0.2), material=mat_bread)
    create_beveled_cylinder("Bakery_Dough_Proofing", 0.18, 0.14, (prep_x, 0.96, prep_z + 0.2), bevel_width=0.03, material=mat_bread)
    create_beveled_cylinder("Bakery_Mixing_Bowl", 0.20, 0.16, (prep_x, 0.97, prep_z + 0.7), bevel_width=0.02, material=mat_wall)

    din_x = cf_cx + 0.4
    din_z = cf_cz + 0.8
    create_beveled_box("Dining_Table_Long-col", (1.2, 0.85, 2.6), (din_x, 0.42, din_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Dining_Bench_L-col", (0.35, 0.45, 2.6), (din_x - 0.75, 0.22, din_z), bevel_width=0.02, material=mat_wood)
    create_beveled_box("Dining_Bench_R-col", (0.35, 0.45, 2.6), (din_x + 0.75, 0.22, din_z), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Dining_Cheese_Plate", 0.22, 0.03, (din_x, 0.87, din_z - 0.7), bevel_width=0.01, material=mat_wood_fence)
    create_beveled_cylinder("Dining_Cheese_Wheel", 0.16, 0.10, (din_x, 0.93, din_z - 0.7), bevel_width=0.015, vertices=12, material=mat_cheese)
    create_beveled_cylinder("Dining_Beer_Mug_1", 0.08, 0.18, (din_x - 0.25, 0.94, din_z - 0.2), bevel_width=0.01, material=mat_wood_fence)
    create_beveled_cylinder("Dining_Beer_Mug_2", 0.08, 0.18, (din_x + 0.25, 0.94, din_z + 0.3), bevel_width=0.01, material=mat_wood_fence)
    create_beveled_cylinder("Dining_Candle_Brass", 0.06, 0.12, (din_x, 0.91, din_z + 0.3), bevel_width=0.01, material=mat_brass)
    create_beveled_cylinder("Dining_Candle_Flame", 0.02, 0.06, (din_x, 0.99, din_z + 0.3), bevel_width=0.005, material=mat_lava_fire)

    dish_z = cf_cz - cf_l/2 + 0.45
    create_beveled_box("Dish_Shelf-col", (2.4, 0.85, 0.30), (cf_cx - 0.4, 1.85, dish_z), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Dish_Plate_1", 0.18, 0.04, (cf_cx - 1.0, 1.88, dish_z + 0.07), bevel_width=0.01, vertices=12, material=mat_wall)
    create_beveled_cylinder("Dish_Bowl_1", 0.14, 0.10, (cf_cx + 0.1, 1.90, dish_z + 0.07), bevel_width=0.01, vertices=12, material=mat_wall)

    create_beveled_box("Kitchen_Rafter_Beam", (cf_w - 0.8, 0.16, 0.16), (cf_cx, 2.85, cf_cz), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Hanging_Sausage_1", 0.08, 0.55, (cf_cx - 1.2, 2.45, cf_cz), bevel_width=0.02, rotation=(0.1, 0, 0.2), material=mat_sausage)
    create_beveled_cylinder("Hanging_Sausage_2", 0.08, 0.55, (cf_cx - 0.5, 2.48, cf_cz), bevel_width=0.02, rotation=(-0.1, 0, 0.1), material=mat_sausage)

    cask_x = cf_cx + cf_w/2 - 0.9
    cask_z = cf_cz + cf_l/2 - 0.9
    create_beveled_cylinder("Wine_Barrel_Cask-col", 0.48, 1.1, (cask_x, 0.55, cask_z), bevel_width=0.04, vertices=16, material=mat_wood_fence)
    create_beveled_cylinder("Wine_Barrel_Small-col", 0.36, 0.82, (cask_x - 0.85, 0.41, cask_z), bevel_width=0.03, vertices=14, material=mat_wood_fence)
    build_chamfered_rock("Flour_Sack_Crumpled-col", (0.60, 0.65, 0.55), (cask_x, 0.32, cask_z - 1.3), material=mat_wall, seed_val=321)

    # 4.B ĐẦU BẾP GUSTEAU
    build_stylized_npc_at("NPC_Gusteau", mat_skin_fair, mat_npc_white, mat_pants_dark, mat_npc_black,
                          pos=(5.5, 0.0, 7.5), rot_y=-1.57, hat_type="chef", hat_m=mat_npc_white, tool_type="chef")

    # =========================================================================
    # 5. BẾN CẢNG NGƯ DÂN & NGƯ DÂN FINN (ĐÔNG: X = 13.5, Z = 7.5)
    # TĂNG CƯỜNG CHI TIẾT CỰC HẠN: Giỏ cá, lưới phơi, thùng ướp muối
    # =========================================================================
    dk_cx, dk_cz = 13.5, 7.5
    create_beveled_box("Pier_Dock_Planks-col", (3.6, 0.25, 6.0), (dk_cx, 0.18, dk_cz), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Pier_Post_1-col", 0.16, 2.0, (dk_cx - 1.6, 0.0, dk_cz - 2.8), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Pier_Post_2-col", 0.16, 2.0, (dk_cx + 1.6, 0.0, dk_cz - 2.8), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Pier_Post_3-col", 0.16, 2.0, (dk_cx - 1.6, 0.0, dk_cz + 2.8), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Pier_Post_4-col", 0.16, 2.0, (dk_cx + 1.6, 0.0, dk_cz + 2.8), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("River_Water_Plane", (14.0, 0.02, 16.0), (dk_cx + 4.5, -0.05, dk_cz), bevel_width=0.01, material=mat_water)

    # Chi tiết cực hạn bến cảng: Giỏ cá đan nan tre, xâu cá khô, giàn phơi lưới
    create_beveled_cylinder("Harbor_Fish_Basket_1-col", 0.26, 0.38, (dk_cx + 1.2, 0.38, dk_cz - 1.5), bevel_width=0.02, vertices=14, material=mat_wheat)
    create_beveled_box("Harbor_Fresh_Fish_1", (0.08, 0.24, 0.10), (dk_cx + 1.2, 0.58, dk_cz - 1.5), bevel_width=0.01, rotation=(0.3, 0, 0), material=mat_water)
    create_beveled_cylinder("Harbor_Fish_Basket_2-col", 0.24, 0.35, (dk_cx + 1.2, 0.36, dk_cz - 0.8), bevel_width=0.02, vertices=14, material=mat_wheat)
    # Giàn phơi lưới cá
    create_beveled_cylinder("Net_Rack_Post_1", 0.06, 1.8, (dk_cx + 1.4, 0.9, dk_cz + 1.2), bevel_width=0.01, material=mat_wood)
    create_beveled_cylinder("Net_Rack_Post_2", 0.06, 1.8, (dk_cx + 1.4, 0.9, dk_cz + 2.4), bevel_width=0.01, material=mat_wood)
    create_beveled_box("Net_Rack_Bar", (0.08, 0.08, 1.4), (dk_cx + 1.4, 1.75, dk_cz + 1.8), bevel_width=0.01, material=mat_wood)
    create_beveled_box("Drying_Fish_Net", (0.10, 0.90, 1.2), (dk_cx + 1.4, 1.30, dk_cz + 1.8), bevel_width=0.02, material=mat_kaki_shirt)

    build_stylized_npc_at("NPC_Finn", mat_skin_tan, mat_kaki_shirt, mat_pants_blue, mat_apron_brown,
                          pos=(dk_cx, 0.18, dk_cz), rot_y=0.0, hat_type="bucket", hat_m=mat_kaki_shirt, tool_type="fisherman")

    # =========================================================================
    # 6. CHỢ TRUNG TÂM & GIẾNG NƯỚC (Z in [16, 31])
    # TĂNG CƯỜNG CHI TIẾT: Xe đẩy thương nhân, chậu hoa, bao tải
    # =========================================================================
    well_x, well_z = 0.0, 16.5
    create_beveled_cylinder("Well_Base_Cobble-col", 1.3, 1.0, (well_x, 0.5, well_z), bevel_width=0.04, vertices=16, material=mat_cobble)
    create_beveled_cylinder("Well_Water_Deep", 1.0, 0.1, (well_x, 0.7, well_z), bevel_width=0.01, material=mat_water)
    create_beveled_cylinder("Well_Post_L-col", 0.12, 2.4, (well_x - 1.1, 1.4, well_z), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Well_Post_R-col", 0.12, 2.4, (well_x + 1.1, 1.4, well_z), bevel_width=0.02, material=mat_wood)
    build_detailed_roof_gabled("Well_Roof", 2.6, 1.8, 0.8, (well_x, 2.5, well_z), overhang=0.2, ridge_along_x=True, material=mat_roof_red)

    ms_x = 0.0
    for i, sz in enumerate([24.0, 27.5]):
        create_beveled_box(f"Market_Stall_Table_{i+1}-col", (2.8, 0.85, 1.4), (ms_x, 0.42, sz), bevel_width=0.03, material=mat_wood)
        create_beveled_box(f"Market_Stall_Canopy_{i+1}", (3.2, 0.2, 1.8), (ms_x, 2.1, sz), bevel_width=0.04, material=mat_canopy_striped)
        create_beveled_box(f"Market_Produce_Box_{i+1}-col", (0.8, 0.3, 0.6), (ms_x - 0.6, 0.95, sz), bevel_width=0.02, material=mat_wood_fence)
        create_beveled_cylinder(f"Market_Barrel_{i+1}-col", 0.35, 0.75, (ms_x + 1.8, 0.38, sz), bevel_width=0.03, vertices=12, material=mat_wood_fence)

    cart_x, cart_z = -2.6, 18.8
    create_beveled_box("Cart_Body-col", (1.6, 0.5, 1.8), (cart_x, 0.55, cart_z), bevel_width=0.03, material=mat_wood)
    create_beveled_cylinder("Cart_Wheel_L-col", 0.42, 0.12, (cart_x - 0.9, 0.42, cart_z), bevel_width=0.03, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_cylinder("Cart_Wheel_R-col", 0.42, 0.12, (cart_x + 0.9, 0.42, cart_z), bevel_width=0.03, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_box("Cart_Crate_1-col", (0.6, 0.5, 0.6), (cart_x - 0.3, 0.9, cart_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Cart_Crate_2-col", (0.5, 0.4, 0.5), (cart_x + 0.3, 0.85, cart_z), bevel_width=0.03, material=mat_wood)

    # =========================================================================
    # 7. NHÀ RÈN CỦA THỢ RÈN VULCAN (TÂY: X = -11.0, Z = 21.0)
    # TƯỜNG DÀY 0.42M & MANG HẬU TỐ '-col' CHỐNG XUYÊN TƯỜNG TRIỆT ĐỂ
    # =========================================================================
    sm_cx, sm_cz = -11.0, 21.0
    sm_w, sm_l, sm_h = 6.6, 5.8, 3.8

    create_beveled_box("Floor_Smith-col", (sm_w, 0.18, sm_l), (sm_cx, 0.09, sm_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_Smith-col", (sm_w, sm_h, wall_th), (sm_cx, sm_h/2, sm_cz - sm_l/2 + wall_th/2), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_Smith-col", (sm_w, sm_h, wall_th), (sm_cx, sm_h/2, sm_cz + sm_l/2 - wall_th/2), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_West_Smith-col", (wall_th, sm_h, sm_l - wall_th*2), (sm_cx - sm_w/2 + wall_th/2, sm_h/2, sm_cz), bevel_width=0.03, material=mat_wall)
    # Cửa vào hướng Đông: Mở rộng cửa 2.0m, tường 2 bên dày 0.42m
    create_beveled_box("Wall_Front_Smith_L-col", (wall_th, sm_h, 1.9), (sm_cx + sm_w/2 - wall_th/2, sm_h/2, sm_cz - 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Smith_R-col", (wall_th, sm_h, 1.9), (sm_cx + sm_w/2 - wall_th/2, sm_h/2, sm_cz + 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Smith_Top-col", (wall_th, 1.2, 2.0), (sm_cx + sm_w/2 - wall_th/2, sm_h - 0.6, sm_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Smith", sm_w, sm_l, 1.8, (sm_cx, sm_h, sm_cz), overhang=0.35, ridge_along_x=False, material=mat_roof_red)

    create_beveled_box("Chimney_Smith_Base-col", (1.2, 5.4, 1.2), (sm_cx - sm_w/2 + 0.8, 2.7, sm_cz - sm_l/2 + 0.8), bevel_width=0.04, material=mat_cobble)

    # 7.A NỘI THẤT NHÀ RÈN
    forge_x = sm_cx - 1.8
    forge_z = sm_cz - 1.5
    create_beveled_box("Blacksmith_Forge_Furnace-col", (2.0, 1.6, 1.8), (forge_x, 0.80, forge_z), bevel_width=0.04, material=mat_cobble)
    create_beveled_box("Forge_Brick_Arch", (1.2, 0.85, 0.25), (forge_x + 0.9, 0.85, forge_z), bevel_width=0.02, material=mat_roof_red)
    create_beveled_box("Forge_Mouth_Void", (0.8, 0.65, 0.35), (forge_x + 0.6, 0.80, forge_z), bevel_width=0.02, material=mat_npc_black)
    build_chamfered_rock("Forge_Coals_Bed", (1.1, 0.38, 1.1), (forge_x + 0.3, 0.55, forge_z), material=mat_lava_fire, seed_val=999)
    build_chamfered_rock("Forge_Rising_Flame", (0.6, 0.45, 0.6), (forge_x + 0.3, 0.85, forge_z), material=mat_lava_fire, seed_val=777)
    create_beveled_cylinder("Forge_Chimney_Flue", 0.42, 2.2, (forge_x, 2.7, forge_z), bevel_width=0.03, material=mat_cobble)

    create_beveled_cylinder("Anvil_Stump_Base-col", 0.50, 0.65, (sm_cx, 0.32, sm_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Anvil_Heavy-col", (0.55, 0.35, 1.05), (sm_cx, 0.82, sm_cz), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Glowing_Hot_Ingot", (0.12, 0.05, 0.45), (sm_cx, 1.02, sm_cz), bevel_width=0.01, material=mat_glowing_iron)

    tank_x = sm_cx + 1.4
    tank_z = sm_cz - 1.5
    create_beveled_box("Quench_Tank-col", (1.6, 0.75, 0.85), (tank_x, 0.38, tank_z), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Quench_Tank_Water", (1.4, 0.12, 0.65), (tank_x, 0.68, tank_z), bevel_width=0.01, material=mat_water)

    rack_z = sm_cz - sm_l/2 + 0.45
    create_beveled_box("Weapon_Rack_Wall-col", (2.8, 1.10, 0.18), (sm_cx + 0.4, 1.85, rack_z), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Weapon_Rack_Sword_1", 0.04, 1.4, (sm_cx - 0.2, 1.85, rack_z + 0.10), bevel_width=0.01, rotation=(0, 0, 0.75), material=mat_metal_silver)
    create_beveled_cylinder("Weapon_Rack_Shield", 0.42, 0.07, (sm_cx + 1.1, 1.85, rack_z + 0.10), bevel_width=0.02, rotation=(1.57, 0, 0), vertices=16, material=mat_metal_gold)

    bench_x = sm_cx + 1.9
    bench_z = sm_cz + 0.5
    create_beveled_box("Blacksmith_Workbench-col", (0.9, 0.88, 2.2), (bench_x, 0.44, bench_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Chest_Scrap_Metal-col", (0.85, 0.55, 0.65), (sm_cx - 1.8, 0.28, sm_cz + 1.6), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Chest_Charcoal-col", (0.85, 0.55, 0.65), (sm_cx - 0.7, 0.28, sm_cz + 1.6), bevel_width=0.03, material=mat_wood_fence)

    # 7.B ĐẠO CỤ VÀ THỢ RÈN VULCAN NGOÀI HIÊN
    out_x, out_z = -6.8, 20.0
    create_beveled_cylinder("Anvil_Outdoor_Log-col", 0.45, 0.7, (out_x, 0.35, out_z - 0.8), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Anvil_Outdoor_Iron-col", (0.55, 0.35, 0.9), (out_x, 0.82, out_z - 0.8), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Forge_Outdoor_Base-col", (1.4, 0.9, 1.2), (out_x - 1.2, 0.45, out_z - 1.8), bevel_width=0.04, material=mat_cobble)
    build_chamfered_rock("Forge_Outdoor_Fire", (1.0, 0.35, 0.8), (out_x - 1.2, 0.95, out_z - 1.8), material=mat_lava_fire, seed_val=888)

    build_stylized_npc_at("NPC_Vulcan", mat_skin_tan, mat_skin_tan, mat_pants_dark, mat_npc_black,
                          pos=(out_x, 0.0, out_z), rot_y=1.57, has_beard=True, beard_m=mat_npc_black, tool_type="blacksmith")

    # =========================================================================
    # 8. NHÀ GIẢ KIM CỦA ARIA (ĐÔNG: X = 11.0, Z = 21.0)
    # TƯỜNG DÀY 0.42M & MANG HẬU TỐ '-col' CHỐNG XUYÊN TƯỜNG TRIỆT ĐỂ
    # =========================================================================
    al_cx, al_cz = 11.0, 21.0
    al_w, al_l, al_h = 6.6, 5.8, 3.8

    create_beveled_box("Floor_Alchemist-col", (al_w, 0.18, al_l), (al_cx, 0.09, al_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_Alchemist-col", (al_w, al_h, wall_th), (al_cx, al_h/2, al_cz - al_l/2 + wall_th/2), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_Alchemist-col", (al_w, al_h, wall_th), (al_cx, al_h/2, al_cz + al_l/2 - wall_th/2), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_East_Alchemist-col", (wall_th, al_h, al_l - wall_th*2), (al_cx + al_w/2 - wall_th/2, al_h/2, al_cz), bevel_width=0.03, material=mat_wall)
    # Cửa vào hướng Tây: Mở rộng cửa 2.0m, tường 2 bên dày 0.42m
    create_beveled_box("Wall_Front_Alchemist_L-col", (wall_th, al_h, 1.9), (al_cx - al_w/2 + wall_th/2, al_h/2, al_cz - 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Alchemist_R-col", (wall_th, al_h, 1.9), (al_cx - al_w/2 + wall_th/2, al_h/2, al_cz + 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Alchemist_Top-col", (wall_th, 1.2, 2.0), (al_cx - al_w/2 + wall_th/2, al_h - 0.6, al_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Alchemist", al_w, al_l, 1.8, (al_cx, al_h, al_cz), overhang=0.35, ridge_along_x=False, material=mat_roof_teal)

    create_beveled_cylinder("Chimney_Alchemist-col", 0.38, 4.8, (al_cx + al_w/2 - 0.8, 2.4, al_cz - al_l/2 + 0.8), bevel_width=0.03, material=mat_cobble)
    build_chamfered_rock("Smoke_Alchemist_1", (1.1, 1.1, 1.1), (al_cx + al_w/2 - 0.8, 5.2, al_cz - al_l/2 + 0.8), material=mat_mystic_cyan, seed_val=111)
    build_chamfered_rock("Smoke_Alchemist_2", (1.4, 1.4, 1.4), (al_cx + al_w/2 - 0.5, 6.0, al_cz - al_l/2 + 0.6), material=mat_mystic_cyan, seed_val=222)

    # 8.A NỘI THẤT NHÀ GIẢ KIM
    create_beveled_cylinder("Cauldron_Hearth_Stand-col", 0.72, 0.35, (al_cx, 0.18, al_cz), bevel_width=0.03, vertices=18, material=mat_cobble)
    create_beveled_cylinder("Alchemist_Cauldron_Glowing-col", 0.72, 0.85, (al_cx, 0.72, al_cz), bevel_width=0.04, vertices=18, material=mat_metal)
    create_beveled_cylinder("Cauldron_Potion_Liquid", 0.65, 0.08, (al_cx, 1.08, al_cz), bevel_width=0.01, material=mat_mystic_cyan)
    build_chamfered_rock("Cauldron_Smoke_1", (0.48, 0.48, 0.48), (al_cx, 1.38, al_cz), material=mat_mystic_cyan, seed_val=444)

    lab_x = al_cx - 1.1
    lab_z = al_cz - al_l/2 + 0.9
    create_beveled_box("Alchemy_Lab_Table-col", (2.4, 0.88, 1.1), (lab_x, 0.44, lab_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Grimoire_Book_Base", (0.48, 0.06, 0.38), (lab_x - 0.1, 0.91, lab_z), bevel_width=0.01, material=mat_leather_book)
    build_chamfered_rock("Alchemy_Crystal_Orb", (0.24, 0.24, 0.24), (lab_x + 0.65, 1.10, lab_z - 0.1), material=mat_mystic_purple, seed_val=888)
    create_beveled_cylinder("Alchemy_Flask_Cyan", 0.08, 0.24, (lab_x - 0.7, 1.00, lab_z - 0.15), bevel_width=0.015, material=mat_mystic_cyan)

    book_x = al_cx + al_w/2 - 0.70
    book_z = al_cz - 0.3
    create_beveled_box("Alchemy_Tall_Bookshelf-col", (0.60, 2.7, 2.4), (book_x, 1.35, book_z), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Potion_Shelves-col", (2.0, 0.90, 0.28), (al_cx + 1.4, 1.85, al_cz - al_l/2 + 0.45), bevel_width=0.02, material=mat_wood_fence)

    # 8.B ĐẠO CỤ VÀ NHÀ GIẢ KIM ARIA TẠI VỊ TRÍ NPC
    create_beveled_box("Herb_Bed_1-col", (1.2, 0.35, 3.2), (al_cx - al_w/2 - 0.8, 0.18, al_cz + 1.2), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("Herb_Soil_1", (1.0, 0.10, 3.0), (al_cx - al_w/2 - 0.8, 0.36, al_cz + 1.2), bevel_width=0.02, material=mat_vegetable)

    build_stylized_npc_at("NPC_Aria", mat_skin_fair, mat_mystic_purple, mat_mystic_purple, mat_npc_black,
                          pos=(7.5, 0.0, 21.0), rot_y=-1.57, hat_type="hood", hat_m=mat_mystic_purple, tool_type="alchemist")

    # =========================================================================
    # 9. NHÀ DÂN CƯ (TÂY: X = -10.0, Z = 28.5)
    # TƯỜNG DÀY 0.42M & MANG HẬU TỐ '-col' CHỐNG XUYÊN TƯỜNG TRIỆT ĐỂ
    # =========================================================================
    hs_cx, hs_cz = -10.0, 28.5
    hs_w, hs_l, hs_h = 6.0, 5.4, 3.6

    create_beveled_box("Floor_House-col", (hs_w, 0.18, hs_l), (hs_cx, 0.09, hs_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Wall_North_House-col", (hs_w, hs_h, wall_th), (hs_cx, hs_h/2, hs_cz - hs_l/2 + wall_th/2), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_House-col", (hs_w, hs_h, wall_th), (hs_cx, hs_h/2, hs_cz + hs_l/2 - wall_th/2), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_West_House-col", (wall_th, hs_h, hs_l - wall_th*2), (hs_cx - hs_w/2 + wall_th/2, hs_h/2, hs_cz), bevel_width=0.03, material=mat_wall)
    # Cửa vào hướng Đông: Mở rộng cửa 1.8m, tường 2 bên dày 0.42m
    create_beveled_box("Wall_Front_House_L-col", (wall_th, hs_h, 1.8), (hs_cx + hs_w/2 - wall_th/2, hs_h/2, hs_cz - 1.5), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_R-col", (wall_th, hs_h, 1.8), (hs_cx + hs_w/2 - wall_th/2, hs_h/2, hs_cz + 1.5), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_Top-col", (wall_th, 1.1, 1.8), (hs_cx + hs_w/2 - wall_th/2, hs_h - 0.55, hs_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_House", hs_w, hs_l, 1.8, (hs_cx, hs_h, hs_cz), overhang=0.35, ridge_along_x=False, material=mat_roof_red)

    # 9.A NỘI THẤT NHÀ DÂN
    bed_x = hs_cx - hs_w/2 + 1.35
    bed_z = hs_cz - hs_l/2 + 1.45
    create_beveled_box("House_Cozy_Bed-col", (1.65, 0.55, 2.3), (bed_x, 0.28, bed_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("House_Bed_Mattress", (1.48, 0.25, 2.1), (bed_x, 0.60, bed_z), bevel_width=0.03, material=mat_roof_red)
    create_beveled_box("House_Bed_Pillow_1", (0.60, 0.16, 0.42), (bed_x - 0.35, 0.76, bed_z - 0.7), bevel_width=0.02, material=mat_wall)

    wardrobe_x = hs_cx - hs_w/2 + 1.05
    wardrobe_z = hs_cz + hs_l/2 - 0.8
    create_beveled_box("House_Wardrobe_Tall-col", (1.5, 2.45, 0.70), (wardrobe_x, 1.23, wardrobe_z), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("House_Floor_Rug-col", (2.5, 0.02, 2.2), (hs_cx + 0.4, 0.09, hs_cz), bevel_width=0.01, material=mat_canopy_striped)
    create_beveled_cylinder("House_Side_Table-col", 0.52, 0.82, (hs_cx + 1.4, 0.41, hs_cz + 1.3), bevel_width=0.02, vertices=16, material=mat_wood)
    create_beveled_box("House_Cozy_Chair-col", (0.52, 0.45, 0.52), (hs_cx + 0.65, 0.23, hs_cz + 1.3), bevel_width=0.02, material=mat_wood)

    # =========================================================================
    # 10. CÔNG TRÌNH THỨ 5: NHÀ TRƯỞNG LÀNG / NHÀ KHO DỰ TRỮ (ELDER HALL)
    # (ĐIỂM CUỐI ĐẠI LỘ CHÍNH: X = 0.0, Z = 38.0) - TƯỜNG DÀY 0.45M CÓ '-col'
    # =========================================================================
    el_cx, el_cz = 0.0, 38.0
    el_w, el_l, el_h = 7.2, 6.4, 4.2
    el_th = 0.45

    create_beveled_box("Floor_Elder-col", (el_w, 0.20, el_l), (el_cx, 0.10, el_cz), bevel_width=0.03, material=mat_cobble)
    # Vách tường sau hướng Bắc:
    create_beveled_box("Wall_North_Elder-col", (el_w, el_h, el_th), (el_cx, el_h/2, el_cz + el_l/2 - el_th/2), bevel_width=0.03, material=mat_wall)
    # Vách tường bên hướng Tây:
    create_beveled_box("Wall_West_Elder-col", (el_th, el_h, el_l - el_th*2), (el_cx - el_w/2 + el_th/2, el_h/2, el_cz), bevel_width=0.03, material=mat_wall)
    # Vách tường bên hướng Đông:
    create_beveled_box("Wall_East_Elder-col", (el_th, el_h, el_l - el_th*2), (el_cx + el_w/2 - el_th/2, el_h/2, el_cz), bevel_width=0.03, material=mat_wall)
    # Cửa vào mặt tiền hướng Nam (nhìn thẳng ra Chợ trung tâm và Cổng Làng): Rộng 2.0m, cao 2.6m
    front_z = el_cz - el_l/2 + el_th/2
    side_w = (el_w - 2.0) / 2.0
    create_beveled_box("Wall_Front_Elder_L-col", (side_w, el_h, el_th), (el_cx - el_w/2 + side_w/2, el_h/2, front_z), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Elder_R-col", (side_w, el_h, el_th), (el_cx + el_w/2 - side_w/2, el_h/2, front_z), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Elder_Top-col", (2.0, el_h - 2.6, el_th), (el_cx, 2.6 + (el_h - 2.6)/2, front_z), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Elder", el_w, el_l, 2.2, (el_cx, el_h, el_cz), overhang=0.40, ridge_along_x=False, material=mat_roof_teal)

    # Thềm đá & bậc thang lối vào Nhà Trưởng Làng (vươn về hướng Nam)
    porch_z = el_cz - el_l/2
    create_beveled_box("Elder_Porch_Step_1-col", (2.8, 0.12, 1.2), (el_cx, 0.06, porch_z - 0.6), bevel_width=0.02, material=mat_stone)
    create_beveled_box("Elder_Porch_Step_2-col", (2.4, 0.12, 0.8), (el_cx, 0.14, porch_z - 0.3), bevel_width=0.02, material=mat_stone)
    create_beveled_cylinder("Elder_Porch_Pillar_L-col", 0.20, 3.4, (el_cx - 1.4, 1.7, porch_z - 0.25), bevel_width=0.03, material=mat_stone)
    create_beveled_cylinder("Elder_Porch_Pillar_R-col", 0.20, 3.4, (el_cx + 1.4, 1.7, porch_z - 0.25), bevel_width=0.03, material=mat_stone)

    # 10.A NỘI THẤT NHÀ TRƯỞNG LÀNG & NHÀ KHO DỰ TRỮ (DIORAMA CẮT VÁCH)
    # 1. Bàn làm việc Trưởng Làng (Elder_Desk-col) & Ghế bành cao cấp
    desk_x = el_cx - 1.2
    desk_z = el_cz + 1.2
    create_beveled_box("Elder_Desk-col", (2.2, 0.90, 1.1), (desk_x, 0.45, desk_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Elder_Map_Scroll", (0.85, 0.03, 0.55), (desk_x - 0.2, 0.92, desk_z), bevel_width=0.008, material=mat_wall)
    create_beveled_box("Elder_Ledger", (0.35, 0.05, 0.45), (desk_x + 0.6, 0.93, desk_z), bevel_width=0.01, material=mat_leather_book)
    create_beveled_cylinder("Elder_Inkwell", 0.05, 0.08, (desk_x + 0.3, 0.94, desk_z + 0.3), bevel_width=0.005, material=mat_brass)
    create_beveled_cylinder("Elder_Candle_Brass", 0.06, 0.15, (desk_x - 0.8, 0.98, desk_z - 0.2), bevel_width=0.01, material=mat_brass)
    create_beveled_cylinder("Elder_Candle_Flame", 0.02, 0.07, (desk_x - 0.8, 1.08, desk_z - 0.2), bevel_width=0.005, material=mat_lava_fire)
    create_beveled_box("Elder_High_Chair-col", (0.65, 0.50, 0.65), (desk_x, 0.25, desk_z + 0.9), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("Elder_Chair_Backrest", (0.65, 0.85, 0.12), (desk_x, 0.92, desk_z + 1.18), bevel_width=0.02, material=mat_canopy_striped)

    # 2. Cờ hiệu & Biểu trưng của Làng (Village Heraldic Banner) trên vách Bắc
    create_beveled_box("Elder_Heraldic_Banner", (2.2, 1.8, 0.06), (el_cx, 2.8, el_cz + el_l/2 - 0.50), bevel_width=0.02, material=mat_canopy_striped)

    # 3. Khu Nhà Kho Lương Thực Dự Trữ (Village Storehouse Section - Phía Đông)
    store_x = el_cx + 1.8
    store_z = el_cz
    # Chồng bao tải lúa mì căng tròn
    build_chamfered_rock("Elder_Grain_Sack_1-col", (0.75, 0.65, 0.70), (store_x - 0.5, 0.35, store_z - 1.2), material=mat_wall, seed_val=101)
    build_chamfered_rock("Elder_Grain_Sack_2-col", (0.75, 0.65, 0.70), (store_x + 0.3, 0.35, store_z - 1.2), material=mat_wall, seed_val=202)
    build_chamfered_rock("Elder_Grain_Sack_3-col", (0.70, 0.60, 0.65), (store_x - 0.1, 0.95, store_z - 1.2), material=mat_wall, seed_val=303)
    # Thùng gỗ lớn dự trữ rượu táo & dầu olive
    create_beveled_cylinder("Elder_Cask_Large_1-col", 0.55, 1.25, (store_x + 0.8, 0.625, store_z + 0.4), bevel_width=0.04, vertices=16, material=mat_wood_fence)
    create_beveled_cylinder("Elder_Cask_Large_2-col", 0.48, 1.10, (store_x + 0.8, 0.55, store_z + 1.6), bevel_width=0.03, vertices=16, material=mat_wood_fence)
    # Kệ để đồ dự trữ (Elder_Supply_Rack-col)
    rack_x = el_cx + el_w/2 - 0.75
    create_beveled_box("Elder_Supply_Rack-col", (0.60, 2.2, 2.4), (rack_x, 1.10, store_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Elder_Supply_Crate_1-col", (0.50, 0.45, 0.65), (rack_x, 0.50, store_z - 0.6), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("Elder_Supply_Crate_2-col", (0.50, 0.45, 0.65), (rack_x, 1.10, store_z - 0.6), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Elder_Cheese_Wheel_1", 0.22, 0.14, (rack_x, 0.55, store_z + 0.5), bevel_width=0.02, vertices=14, material=mat_cheese)
    create_beveled_cylinder("Elder_Cheese_Wheel_2", 0.20, 0.12, (rack_x, 1.12, store_z + 0.5), bevel_width=0.02, vertices=14, material=mat_cheese)
    # Rương ngân khố của Làng
    create_beveled_box("Elder_Treasury_Chest-col", (0.95, 0.65, 0.65), (desk_x - 1.5, 0.325, desk_z), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Elder_Treasury_Band", (1.00, 0.67, 0.12), (desk_x - 1.5, 0.335, desk_z), bevel_width=0.015, material=mat_metal_gold)

    # =========================================================================
    # 11. HỆ THỐNG 10 TRỤ ĐÈN ĐƯỜNG LÀNG PHÁT QUANG ẤM ÁP (STREET LANTERNS)
    # =========================================================================
    build_street_lantern("Lantern_Gate_L", (-2.6, 0.0, 9.5), arm_dir_x=1.0)
    build_street_lantern("Lantern_Gate_R", (2.6, 0.0, 9.5), arm_dir_x=-1.0)
    build_street_lantern("Lantern_Avenue_1", (-2.6, 0.0, 15.0), arm_dir_x=1.0)
    build_street_lantern("Lantern_Avenue_2", (2.6, 0.0, 15.0), arm_dir_x=-1.0)
    build_street_lantern("Lantern_Well_Corner", (2.4, 0.0, 18.5), arm_dir_x=-1.0)
    build_street_lantern("Lantern_Market_W", (-4.8, 0.0, 25.0), arm_dir_x=1.0)
    build_street_lantern("Lantern_Market_E", (4.8, 0.0, 25.0), arm_dir_x=-1.0)
    build_street_lantern("Lantern_Elder_Entrance", (-2.6, 0.0, 33.6), arm_dir_x=1.0)
    build_street_lantern("Lantern_Harbor_Path", (5.6, 0.0, 8.5), arm_dir_x=-1.0)
    build_street_lantern("Lantern_Pier_Entrance", (11.8, 0.0, 7.5), arm_dir_x=1.0)

    # =========================================================================
    # 12. CHI TIẾT CỰC HẠN NGOẠI CẢNH (CHẬU HOA, GIÀN HOA, XE HÀNG)
    # =========================================================================
    # Chậu hoa trước Quán Ăn
    create_beveled_box("Planter_Chef_Porch-col", (1.2, 0.40, 0.45), (cf_cx - cf_w/2 - 0.4, 0.20, cf_cz + 2.2), bevel_width=0.02, material=mat_wood)
    build_chamfered_rock("Flower_Red_Cluster_1", (0.9, 0.30, 0.35), (cf_cx - cf_w/2 - 0.4, 0.48, cf_cz + 2.2), material=mat_flower_red, seed_val=55)

    # Chậu hoa trước Nhà Dân Cư
    create_beveled_box("Planter_House_Porch-col", (1.2, 0.40, 0.45), (hs_cx + hs_w/2 + 0.4, 0.20, hs_cz - 2.0), bevel_width=0.02, material=mat_wood)
    build_chamfered_rock("Flower_Yellow_Cluster_1", (0.9, 0.30, 0.35), (hs_cx + hs_w/2 + 0.4, 0.48, hs_cz - 2.0), material=mat_flower_yellow, seed_val=77)

    # Chậu hoa thềm đá Nhà Trưởng Làng
    create_beveled_cylinder("Elder_Flower_Urn_L-col", 0.32, 0.65, (el_cx - 1.8, 0.325, porch_z - 0.6), bevel_width=0.03, material=mat_stone)
    build_chamfered_rock("Elder_Flowers_Red", (0.48, 0.35, 0.48), (el_cx - 1.8, 0.78, porch_z - 0.6), material=mat_flower_red, seed_val=88)
    create_beveled_cylinder("Elder_Flower_Urn_R-col", 0.32, 0.65, (el_cx + 1.8, 0.325, porch_z - 0.6), bevel_width=0.03, material=mat_stone)
    build_chamfered_rock("Elder_Flowers_Yellow", (0.48, 0.35, 0.48), (el_cx + 1.8, 0.78, porch_z - 0.6), material=mat_flower_yellow, seed_val=99)

    # Xe đẩy hàng thương nhân bổ sung ở góc chợ
    create_beveled_box("Market_Handcart_Body-col", (1.4, 0.45, 1.2), (3.2, 0.50, 24.5), bevel_width=0.03, material=mat_wood)
    create_beveled_cylinder("Market_Handcart_Wheel_L-col", 0.38, 0.10, (2.4, 0.38, 24.5), bevel_width=0.02, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_cylinder("Market_Handcart_Wheel_R-col", 0.38, 0.10, (4.0, 0.38, 24.5), bevel_width=0.02, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_box("Market_Cart_Apples-col", (0.6, 0.35, 0.5), (3.2, 0.85, 24.5), bevel_width=0.02, material=mat_flower_red)

    # Thùng rượu xếp ngoài quán ăn
    create_beveled_cylinder("Tavern_Outdoor_Keg_1-col", 0.38, 0.85, (cf_cx - cf_w/2 - 0.5, 0.425, cf_cz - 2.2), bevel_width=0.03, vertices=14, material=mat_wood_fence)
    create_beveled_cylinder("Tavern_Outdoor_Keg_2-col", 0.38, 0.85, (cf_cx - cf_w/2 - 1.2, 0.425, cf_cz - 2.2), bevel_width=0.03, vertices=14, material=mat_wood_fence)
    create_beveled_cylinder("Tavern_Outdoor_Keg_Top-col", 0.32, 0.75, (cf_cx - cf_w/2 - 0.85, 1.15, cf_cz - 2.2), bevel_width=0.025, vertices=14, material=mat_wood_fence)

    # =========================================================================
    # 13. KHU LÂM NGHIỆP CỦA TIỀU PHU GROVER (TÂY BẮC: X = -14.0, Z = 38.0)
    # TĂNG CƯỜNG CHI TIẾT: Củi xẻ tiều phu, củi chẻ xếp lớp gọn gàng
    # =========================================================================
    lm_cx, lm_cz = -14.0, 38.0
    create_beveled_cylinder("Lumber_P1-col", 0.18, 3.2, (lm_cx - 2.5, 1.6, lm_cz - 2.0), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Lumber_P2-col", 0.18, 3.2, (lm_cx + 2.5, 1.6, lm_cz - 2.0), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Lumber_P3-col", 0.18, 3.2, (lm_cx - 2.5, 1.6, lm_cz + 2.0), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Lumber_P4-col", 0.18, 3.2, (lm_cx + 2.5, 1.6, lm_cz + 2.0), bevel_width=0.02, material=mat_wood)
    build_detailed_roof_gabled("Lumber_Shed_Roof", 5.6, 4.6, 1.0, (lm_cx, 3.2, lm_cz), overhang=0.25, ridge_along_x=True, material=mat_wood_fence)

    create_beveled_box("Lumber_Saw_Table-col", (3.2, 0.85, 1.4), (lm_cx, 0.42, lm_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_cylinder("Lumber_Saw_Blade", 0.45, 0.04, (lm_cx, 0.95, lm_cz), bevel_width=0.01, rotation=(1.57, 0, 0), material=mat_metal)

    for i in range(3):
        create_beveled_cylinder(f"Log_Pile_Bot_{i}-col", 0.32, 4.0, (lm_cx + 4.0, 0.32, lm_cz - 1.2 + i * 0.75), bevel_width=0.03, rotation=(1.57, 0, 0), material=mat_wood)
    for i in range(2):
        create_beveled_cylinder(f"Log_Pile_Top_{i}-col", 0.30, 4.0, (lm_cx + 4.0, 0.85, lm_cz - 0.85 + i * 0.75), bevel_width=0.03, rotation=(1.57, 0, 0), material=mat_wood)

    # Đống củi xẻ chẻ sẵn (Split Firewood Stack)
    create_beveled_box("Firewood_Shelter_Base-col", (2.4, 0.10, 1.2), (lm_cx - 2.8, 0.05, lm_cz + 1.2), bevel_width=0.02, material=mat_wood_fence)
    for layer in range(3):
        ly = 0.22 + layer * 0.22
        for col in range(5):
            lx = (lm_cx - 3.8) + col * 0.45
            create_beveled_box(f"Split_Log_{layer}_{col}-col", (0.38, 0.18, 0.95), (lx, ly, lm_cz + 1.2), bevel_width=0.02, material=mat_wood)

    create_beveled_cylinder("NPC_Grover_Chopping_Block-col", 0.40, 0.60, (-13.5, 0.30, 35.8), bevel_width=0.03, vertices=12, material=mat_wood)

    build_stylized_npc_at("NPC_Grover", mat_skin_tan, mat_plaid_red, mat_pants_blue, mat_npc_black,
                          pos=(-13.5, 0.0, 36.5), rot_y=0.8, has_beard=True, beard_m=mat_farmer_brown, hat_type="beanie", hat_m=mat_roof_red, tool_type="lumberjack")

    build_stylized_tree("Tree_Lumber_1", (lm_cx - 4.5, 0, lm_cz - 3.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Lumber_2", (lm_cx - 4.0, 0, lm_cz + 3.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Lumber_3", (lm_cx, 0, lm_cz + 4.5), scale=1.4, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # =========================================================================
    # 14. KHU MỎ ĐÁ CỦA THỢ MỎ BROCK (ĐÔNG BẮC: X = 14.0, Z = 38.0)
    # TĂNG CƯỜNG CHI TIẾT: Tinh thể quặng pha lê ma thuật phát quang cyan & xe goòng
    # =========================================================================
    mn_cx, mn_cz = 14.0, 38.0
    build_chamfered_rock("Mine_Cliff_Main-col", (13.0, 7.5, 8.0), (mn_cx, 3.75, mn_cz + 3.0), material=mat_stone, seed_val=333)
    build_chamfered_rock("Mine_Cliff_Ledge-col", (6.5, 5.0, 4.0), (mn_cx - 4.5, 2.5, mn_cz + 0.5), material=mat_stone, seed_val=444)
    create_beveled_box("Mine_Entrance_Void", (2.8, 3.2, 1.2), (mn_cx, 1.6, mn_cz - 0.9), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Mine_Beam_L-col", (0.35, 3.4, 0.4), (mn_cx - 1.5, 1.7, mn_cz - 0.9), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Mine_Beam_R-col", (0.35, 3.4, 0.4), (mn_cx + 1.5, 1.7, mn_cz - 0.9), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Mine_Beam_Top-col", (3.6, 0.35, 0.4), (mn_cx, 3.2, mn_cz - 0.9), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_cylinder("Ore_Furnace-col", 1.3, 2.6, (mn_cx - 4.2, 1.3, mn_cz - 2.5), bevel_width=0.04, vertices=16, material=mat_cobble)
    create_beveled_box("Ore_Furnace_Fire", (0.8, 0.6, 0.5), (mn_cx - 4.2, 0.6, mn_cz - 1.8), bevel_width=0.02, material=mat_lava_fire)
    create_beveled_box("Rail_L-col", (0.08, 0.08, 4.5), (mn_cx + 2.0, 0.06, mn_cz - 1.0), bevel_width=0.01, material=mat_metal)
    create_beveled_box("Rail_R-col", (0.08, 0.08, 4.5), (mn_cx + 2.8, 0.06, mn_cz - 1.0), bevel_width=0.01, material=mat_metal)
    create_beveled_box("Minecart_Body-col", (1.2, 0.65, 1.6), (mn_cx + 2.4, 0.58, mn_cz - 1.5), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Minecart_Ore-col", (0.9, 0.3, 1.3), (mn_cx + 2.4, 0.88, mn_cz - 1.5), bevel_width=0.03, material=mat_stone)

    # Tinh thể quặng pha lê ma thuật phát quang cyan nhô ra từ vách đá
    build_chamfered_rock("Magic_Crystal_Ore_1", (0.6, 0.9, 0.6), (mn_cx - 2.5, 1.8, mn_cz + 1.2), material=mat_mystic_cyan, seed_val=1111)
    build_chamfered_rock("Magic_Crystal_Ore_2", (0.5, 0.7, 0.5), (mn_cx - 2.8, 2.4, mn_cz + 1.5), material=mat_mystic_cyan, seed_val=2222)
    build_chamfered_rock("Magic_Crystal_Ore_3", (0.7, 1.1, 0.7), (mn_cx + 4.8, 1.6, mn_cz + 1.8), material=mat_mystic_cyan, seed_val=3333)

    build_chamfered_rock("NPC_Brock_Ore_Cluster-col", (0.8, 0.5, 0.8), (12.5, 0.25, 37.5), material=mat_stone, seed_val=777)

    build_stylized_npc_at("NPC_Brock", mat_skin_tan, mat_miner_suit, mat_miner_suit, mat_npc_black,
                          pos=(12.5, 0.0, 36.5), rot_y=-0.8, has_beard=True, beard_m=mat_farmer_brown, hat_type="hard_hat", hat_m=mat_hard_hat_yellow, tool_type="miner")

    # =========================================================================
    # 15. CÂY CỐI TRANG TRÍ BAO QUANH LÀNG
    # =========================================================================
    build_stylized_tree("Tree_Gate_L", (-5.0, 0, 5.0), scale=1.1, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Gate_R", (5.5, 0, 4.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Smith_Back", (-18.5, 0, 14.0), scale=1.0, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Alchemist_Back", (16.5, 0, 16.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_House_South", (-17.0, 0, 32.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Elder_Back", (0.0, 0, 43.5), scale=1.4, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Mine_East", (18.5, 0, 35.0), scale=1.5, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # =========================================================================
    # 16. RENDER MẮT THẦN ĐA GÓC (VILLAGE OVERVIEW & 5 PHÒNG DIORAMA CẮT VÁCH)
    # =========================================================================
    temp_dir = os.path.join(workspace_dir, "Assets", "Models", "_temp_previews")
    os.makedirs(temp_dir, exist_ok=True)

    # 16.A Render Toàn Cảnh Làng
    p_village = os.path.join(temp_dir, "preview_village.png")
    setup_preview_render(p_village, resolution=(1280, 800), camera_pos=(-26, -36, 24), target_pos=(0, -22, 1), ortho_scale=50.0)

    # 16.B Render 5 Căn Phòng Nội Thất Cắt Vách (Ẩn tạm thời mái nhà để soi nội thất)
    roof_nodes = ["Roof_Smith", "Roof_Alchemist", "Roof_Chef", "Roof_House", "Roof_Elder"]
    wall_front_nodes = [
        "Wall_Front_Smith_L-col", "Wall_Front_Smith_R-col", "Wall_Front_Smith_Top-col", "Wall_South_Smith-col", "Wall_West_Smith-col",
        "Wall_Front_Alchemist_L-col", "Wall_Front_Alchemist_R-col", "Wall_Front_Alchemist_Top-col", "Wall_South_Alchemist-col",
        "Wall_Front_Chef_L-col", "Wall_Front_Chef_R-col", "Wall_Front_Chef_Top-col", "Wall_South_Chef-col",
        "Wall_Front_House_L-col", "Wall_Front_House_R-col", "Wall_Front_House_Top-col", "Wall_South_House-col", "Wall_West_House-col",
        "Wall_Front_Elder_L-col", "Wall_Front_Elder_R-col", "Wall_Front_Elder_Top-col", "Wall_West_Elder-col"
    ]

    tree_objs = [obj for obj in bpy.data.objects if 'Tree' in obj.name or 'Foliage' in obj.name]
    for obj in tree_objs:
        obj.hide_render = True
    for name in roof_nodes + wall_front_nodes:
        obj = bpy.data.objects.get(name)
        if obj:
            obj.hide_render = True

    # 1. Render Nội Thất Nhà Rèn
    p_smith = os.path.join(temp_dir, "preview_interior_smith.png")
    setup_preview_render(p_smith, resolution=(640, 480), camera_pos=(-11 - 5.5, -21 - 5.5, 7.2), target_pos=(-11.0, -21.0, 1.3), ortho_scale=7.2)

    # 2. Render Nội Thất Nhà Giả Kim
    p_alchemist = os.path.join(temp_dir, "preview_interior_alchemist.png")
    setup_preview_render(p_alchemist, resolution=(640, 480), camera_pos=(11 - 5.5, -21 - 5.5, 7.2), target_pos=(11.0, -21.0, 1.3), ortho_scale=7.2)

    # 3. Render Nội Thất Quán Ăn / Nhà Bếp
    p_chef = os.path.join(temp_dir, "preview_interior_chef.png")
    setup_preview_render(p_chef, resolution=(640, 480), camera_pos=(8 - 5.5, -7.5 - 5.5, 7.2), target_pos=(8.0, -7.5, 1.3), ortho_scale=7.2)

    # 4. Render Nội Thất Nhà Dân Cư
    p_house = os.path.join(temp_dir, "preview_interior_house.png")
    setup_preview_render(p_house, resolution=(640, 480), camera_pos=(-10 - 5.5, -28.5 - 5.5, 7.2), target_pos=(-10.5, -28.5, 1.3), ortho_scale=7.2)

    # 5. Render Nội Thất Nhà Trưởng Làng / Kho Dự Trữ Lương Thực (Nhìn từ Tây Nam vào)
    p_elder = os.path.join(temp_dir, "preview_interior_elder.png")
    setup_preview_render(p_elder, resolution=(640, 480), camera_pos=(el_cx - 5.5, -el_cz + 5.5, 7.5), target_pos=(el_cx, -el_cz, 1.3), ortho_scale=7.6)

    # Khôi phục hiển thị mái, vách và cây cối trước khi xuất GLB cho Godot
    for obj in tree_objs:
        obj.hide_render = False
    for name in roof_nodes + wall_front_nodes:
        obj = bpy.data.objects.get(name)
        if obj:
            obj.hide_render = False

    # Render trực tiếp ảnh toàn cảnh làng vào Assets/Models/_preview_render.png
    setup_preview_render(os.path.join(workspace_dir, "Assets", "Models", "_preview_render.png"), resolution=(1280, 800), camera_pos=(-26, -36, 24), target_pos=(0, -22, 1), ortho_scale=50.0)

    # =========================================================================
    # 17. XUẤT RA GLB & LƯU FILE BLEND AN TOÀN
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

    print("=== DỰNG BẢN ĐỒ LÀNG MỞ RỘNG CỰC HẠN HOÀN TẤT VỚI CHẤT LƯỢNG CAO ===")

if __name__ == '__main__':
    build_village()
