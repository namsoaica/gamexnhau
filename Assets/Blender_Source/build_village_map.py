"""
Script Blender 3D: Dựng Bản Đồ Làng Hoàn Thiện Theo Phác Họa 'modelyeucau/map2/1.jpg'
Sử dụng Thư Viện Procedural Chuẩn 'tools/blender_kit.py'.
Tuân thủ:
- Bắt buộc trải UV tự động (unwrap_mesh) cho MỌI mesh.
- Gán vật liệu liên kết Texture Seamless (thớ gỗ, thớ đá, bạt sọc, vân đất, ngói đỏ, ngói teal).
- Chi tiết nội thất 4 phòng diorama cắt vách theo đúng ảnh '1.jpg': Nhà Rèn, Nhà Giả Kim, Quán Ăn, Nhà Dân.
- Phụ kiện đạo cụ đặc trưng cho 8 NPC: Vulcan, Aria, Gusteau, George, Finn, Brock, Grover, Aegis.
- Xuất 'Assets/Models/village_map.glb' và lưu an toàn 'Assets/Blender_Source/village_map.blend'.
- Render ảnh mắt thần '_preview_render.png'.
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

    # 1. BẢNG VẬT LIỆU CÓ TEXTURE SEAMLESS THEO BẢNG MÀU THẬT 1.JPG
    mat_dirt = create_material("Mat_Dirt", (0.54, 0.36, 0.21), roughness=0.90, texture_path=p_dirt)
    mat_stone = create_material("Mat_Stone", (0.42, 0.44, 0.46), roughness=0.80, texture_path=p_rock)
    mat_cobble = create_material("Mat_Cobble", (0.41, 0.42, 0.44), roughness=0.80, texture_path=p_cobble)
    mat_wood = create_material("Mat_Wood", (0.55, 0.35, 0.20), roughness=0.75, texture_path=p_wood)
    mat_wood_fence = create_material("Mat_Wood_Fence", (0.36, 0.23, 0.13), roughness=0.80, texture_path=p_wood)
    mat_metal = create_material("Mat_Metal", (0.58, 0.60, 0.64), roughness=0.35, metallic=0.85, texture_path=p_metal)
    mat_roof_red = create_material("Mat_Roof_Red", (0.66, 0.22, 0.16), roughness=0.75, texture_path=p_roof_red)
    mat_roof_teal = create_material("Mat_Roof_Teal", (0.15, 0.55, 0.51), roughness=0.75, texture_path=p_roof_teal)
    mat_canopy_striped = create_material("Mat_Canopy_Striped", (0.88, 0.23, 0.23), roughness=0.85, texture_path=p_canopy)
    mat_mystic_cyan = create_material("Mat_Mystic_Cyan", (0.20, 0.88, 0.82), roughness=0.20, emission_color=(0.20, 0.88, 0.82), emission_strength=2.6)
    mat_mystic_purple = create_material("Mat_Mystic_Purple", (0.65, 0.22, 0.85), roughness=0.25, emission_color=(0.65, 0.22, 0.85), emission_strength=2.4)
    mat_lava_fire = create_material("Mat_Lava_Fire", (1.00, 0.45, 0.05), roughness=0.40, emission_color=(1.00, 0.45, 0.05), emission_strength=3.2)
    mat_foliage = create_material("Mat_Foliage", (0.22, 0.52, 0.20), roughness=0.85, texture_path=p_grass)
    mat_vegetable = create_material("Mat_Vegetable", (0.30, 0.69, 0.24), roughness=0.80)
    mat_wheat = create_material("Mat_Wheat", (0.90, 0.75, 0.29), roughness=0.85)
    mat_bread = create_material("Mat_Bread", (0.83, 0.58, 0.29), roughness=0.70)
    mat_wall = create_material("Mat_Wall_Stone", (0.82, 0.80, 0.76), roughness=0.85)
    mat_water = create_material("Mat_Water", (0.18, 0.65, 0.72), roughness=0.15, emission_color=(0.18, 0.65, 0.72), emission_strength=0.8)

    # 2. ĐƯỜNG MÒN ĐẤT NỐI LIỀN TRỰC TIẾP TỪ ĐẢO ĐÁ VÀO LÀNG
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

    # 3. CỔNG LÀNG & VƯỜN RAU CẢI (Z in [7, 10])
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

    # Đạo cụ Lính Canh 1 (Aegis) tại cổng làng bên trái (-0.8, 0, 8.5)
    create_beveled_cylinder("NPC_Aegis_Spear_Shaft", 0.04, 2.8, (-0.8, 1.4, gate_z - 0.4), bevel_width=0.01, material=mat_wood)
    create_beveled_box("NPC_Aegis_Spear_Blade", (0.10, 0.40, 0.04), (-0.8, 2.9, gate_z - 0.4), bevel_width=0.01, material=mat_metal)
    create_beveled_cylinder("NPC_Aegis_Shield", 0.45, 0.08, (-1.1, 0.55, gate_z - 0.3), bevel_width=0.02, rotation=(0.2, 0, 0.3), vertices=16, material=mat_metal)
    create_beveled_cylinder("NPC_Aegis_Iron_Helmet", 0.22, 0.30, (-0.8, 0.25, gate_z + 0.3), bevel_width=0.02, material=mat_metal)

    # Đạo cụ Lính Canh 2 (Guard 2) tại cổng làng bên phải (0.8, 0, 8.5)
    create_beveled_cylinder("NPC_Guard_2_Spear_Shaft", 0.04, 2.8, (0.8, 1.4, gate_z - 0.4), bevel_width=0.01, material=mat_wood)
    create_beveled_box("NPC_Guard_2_Spear_Blade", (0.10, 0.40, 0.04), (0.8, 2.9, gate_z - 0.4), bevel_width=0.01, material=mat_metal)
    create_beveled_cylinder("NPC_Guard_2_Shield", 0.45, 0.08, (1.1, 0.55, gate_z - 0.3), bevel_width=0.02, rotation=(-0.2, 0, -0.3), vertices=16, material=mat_metal)
    create_beveled_cylinder("NPC_Guard_2_Iron_Helmet", 0.22, 0.30, (0.8, 0.25, gate_z + 0.3), bevel_width=0.02, material=mat_metal)

    # Vườn rau cải 1 (Bên trái đường: -5.2, 0, 8.5)
    for row in range(3):
        rz = 7.5 + row * 1.1
        create_beveled_box(f"Crop_Soil_L_{row}", (4.2, 0.1, 0.8), (-5.2, 0.05, rz), bevel_width=0.02, material=mat_dirt)
        for col in range(4):
            cx = -6.5 + col * 0.9
            build_chamfered_rock(f"Cabbage_L_{row}_{col}", (0.52, 0.44, 0.52), (cx, 0.22, rz), material=mat_vegetable, seed_val=row*10+col)

    # Vườn rau cải 2 (Bên phải đường: 5.2, 0, 8.5)
    for row in range(3):
        rz = 7.5 + row * 1.1
        create_beveled_box(f"Crop_Soil_R_{row}", (3.6, 0.1, 0.8), (4.8, 0.05, rz), bevel_width=0.02, material=mat_dirt)
        for col in range(3):
            cx = 3.9 + col * 0.9
            build_chamfered_rock(f"Cabbage_R_{row}_{col}", (0.50, 0.42, 0.50), (cx, 0.22, rz), material=mat_vegetable, seed_val=100+row*10+col)

    create_beveled_cylinder("NPC_George_Straw_Hat", 0.38, 0.18, (-4.2, 0.70, 8.5), bevel_width=0.02, vertices=12, material=mat_wheat)
    create_beveled_cylinder("NPC_George_Garden_Hoe_Handle", 0.04, 1.8, (-4.4, 0.90, 8.8), bevel_width=0.01, rotation=(0.1, 0, 0.2), material=mat_wood)
    create_beveled_box("NPC_George_Garden_Hoe_Blade", (0.22, 0.06, 0.14), (-4.2, 0.10, 8.9), bevel_width=0.01, material=mat_metal)
    create_beveled_cylinder("NPC_George_Wheat_Bundle", 0.25, 0.80, (-4.8, 0.40, 8.0), bevel_width=0.03, vertices=8, material=mat_wheat)

    # 4. QUÁN ĂN / TAVERN CỦA ĐẦU BẾP GUSTEAU (ĐÔNG: X = 8.0, Z = 7.5)
    cf_cx, cf_cz = 8.0, 7.5
    cf_w, cf_l, cf_h = 5.8, 5.0, 3.0
    create_beveled_box("Floor_Chef", (cf_w, 0.15, cf_l), (cf_cx, 0.08, cf_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_Chef", (cf_w, cf_h, 0.3), (cf_cx, cf_h/2, cf_cz - cf_l/2 + 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_Chef", (cf_w, cf_h, 0.3), (cf_cx, cf_h/2, cf_cz + cf_l/2 - 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_East_Chef", (0.3, cf_h, cf_l - 0.6), (cf_cx + cf_w/2 - 0.15, cf_h/2, cf_cz), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Chef_L", (0.3, cf_h, 1.6), (cf_cx - cf_w/2 + 0.15, cf_h/2, cf_cz - 1.4), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Chef_R", (0.3, cf_h, 1.6), (cf_cx - cf_w/2 + 0.15, cf_h/2, cf_cz + 1.4), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Chef_Top", (0.3, 0.7, 1.8), (cf_cx - cf_w/2 + 0.15, cf_h - 0.35, cf_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Chef", cf_w, cf_l, 1.6, (cf_cx, cf_h, cf_cz), overhang=0.3, ridge_along_x=False, material=mat_roof_red)

    # 4.A NỘI THẤT QUÁN ĂN / NHÀ BẾP (DIORAMA CẮT VÁCH CHUẨN ẢNH 1.JPG)
    # Lò nướng bánh mì gạch vòm đỏ than hồng (Bakery_Brick_Oven-col)
    create_beveled_cylinder("Bakery_Brick_Oven-col", 0.90, 1.7, (cf_cx + cf_w/2 - 1.2, 0.85, cf_cz - cf_l/2 + 1.2), bevel_width=0.04, vertices=16, material=mat_cobble)
    build_chamfered_rock("Bakery_Brick_Oven_Fire", (0.75, 0.55, 0.65), (cf_cx + cf_w/2 - 1.2, 0.55, cf_cz - cf_l/2 + 1.2), material=mat_lava_fire, seed_val=666)
    create_beveled_cylinder("Bakery_Oven_Flue", 0.25, 1.4, (cf_cx + cf_w/2 - 1.2, 2.0, cf_cz - cf_l/2 + 1.2), bevel_width=0.02, material=mat_cobble)

    # Bàn nhào bột lớn có cây cán bột, bột mì trắng và các ổ bánh mì baguette (Bakery_Prep_Table-col)
    create_beveled_box("Bakery_Prep_Table-col", (1.2, 0.88, 2.2), (cf_cx - 1.3, 0.44, cf_cz - 0.9), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Bakery_Flour_Dust", (0.7, 0.02, 1.1), (cf_cx - 1.3, 0.89, cf_cz - 0.9), bevel_width=0.01, material=mat_wall)
    create_beveled_cylinder("Bakery_Rolling_Pin", 0.04, 0.55, (cf_cx - 1.3, 0.93, cf_cz - 0.6), bevel_width=0.01, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_cylinder("Bakery_Baguette_1", 0.08, 0.65, (cf_cx - 1.3, 0.95, cf_cz - 1.2), bevel_width=0.02, rotation=(0.3, 0, 0.4), material=mat_bread)
    create_beveled_cylinder("Bakery_Baguette_2", 0.08, 0.65, (cf_cx - 1.3, 0.95, cf_cz - 1.0), bevel_width=0.02, rotation=(-0.2, 0, 0.3), material=mat_bread)

    # Bàn ăn gỗ dài kèm 2 hàng ghế băng (Dining_Table_Long-col, Dining_Bench_L-col, Dining_Bench_R-col)
    create_beveled_box("Dining_Table_Long-col", (1.2, 0.85, 2.6), (cf_cx + 0.3, 0.42, cf_cz + 0.7), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Dining_Bench_L-col", (0.35, 0.45, 2.6), (cf_cx - 0.6, 0.22, cf_cz + 0.7), bevel_width=0.02, material=mat_wood)
    create_beveled_box("Dining_Bench_R-col", (0.35, 0.45, 2.6), (cf_cx + 1.2, 0.22, cf_cz + 0.7), bevel_width=0.02, material=mat_wood)

    # Kệ để bát đĩa gốm sứ (Dish_Shelf-col)
    create_beveled_box("Dish_Shelf-col", (2.2, 0.85, 0.30), (cf_cx - 0.4, 1.85, cf_cz - cf_l/2 + 0.35), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Dish_Plate_1", 0.18, 0.04, (cf_cx - 0.9, 1.88, cf_cz - cf_l/2 + 0.42), bevel_width=0.01, vertices=12, material=mat_wall)
    create_beveled_cylinder("Dish_Plate_2", 0.18, 0.04, (cf_cx - 0.4, 1.88, cf_cz - cf_l/2 + 0.42), bevel_width=0.01, vertices=12, material=mat_wall)
    create_beveled_cylinder("Dish_Cup_1", 0.09, 0.18, (cf_cx + 0.2, 1.88, cf_cz - cf_l/2 + 0.42), bevel_width=0.01, vertices=10, material=mat_cobble)

    # Xâu xúc xích, giò hun khói treo trần (Hanging_Sausages-col)
    create_beveled_box("Hanging_Sausages-col", (2.0, 0.12, 0.12), (cf_cx, 2.50, cf_cz + 0.6), bevel_width=0.015, material=mat_wood_fence)
    create_beveled_cylinder("Hanging_Sausage_Link_1", 0.06, 0.45, (cf_cx - 0.5, 2.15, cf_cz + 0.6), bevel_width=0.02, rotation=(0.1, 0, 0.1), material=mat_roof_red)
    create_beveled_cylinder("Hanging_Sausage_Link_2", 0.07, 0.50, (cf_cx + 0.4, 2.12, cf_cz + 0.6), bevel_width=0.02, rotation=(-0.1, 0, 0.2), material=mat_roof_red)

    # Thùng rượu gỗ (Wine_Barrel_Cask-col)
    create_beveled_cylinder("Wine_Barrel_Cask-col", 0.45, 1.05, (cf_cx + cf_w/2 - 0.8, 0.52, cf_cz + cf_l/2 - 0.8), bevel_width=0.03, vertices=14, material=mat_wood_fence)
    create_beveled_cylinder("Wine_Barrel_Cask_Small", 0.38, 0.85, (cf_cx + cf_w/2 - 1.6, 0.42, cf_cz + cf_l/2 - 0.8), bevel_width=0.03, vertices=12, material=mat_wood)

    # Đạo cụ Đầu Bếp Gusteau tại vị trí NPC (5.5, 0, 7.5)
    create_beveled_cylinder("NPC_Gusteau_Chef_Hat", 0.22, 0.35, (5.5, 1.2, 7.5), bevel_width=0.02, vertices=12, material=mat_wall)
    create_beveled_box("NPC_Gusteau_Baguette_Tray", (0.55, 0.10, 0.80), (5.1, 0.65, 7.5), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("NPC_Gusteau_Baguette_Prop", 0.08, 0.65, (5.1, 0.75, 7.5), bevel_width=0.02, rotation=(0, 0, 1.57), material=mat_bread)

    # 4.1 BẾN CẢNG NGƯ DÂN (FISHERMAN'S WHARF & PIER: X in [12, 18], Z in [5, 11])
    dock_x, dock_z = 13.5, 7.5
    # Mặt nước sông / bờ biển trong xanh
    create_beveled_box("Water_Fisher_Basin-col", (7.0, 0.10, 8.0), (16.2, 0.02, dock_z), bevel_width=0.02, material=mat_water)
    # Cầu cảng gỗ vươn ra mặt nước
    create_beveled_box("Pier_Dock_Deck-col", (2.8, 0.16, 5.0), (dock_x, 0.18, dock_z), bevel_width=0.03, material=mat_wood)
    for pi, (px, pz) in enumerate([(dock_x - 1.1, dock_z - 2.0), (dock_x + 1.1, dock_z - 2.0), (dock_x - 1.1, dock_z + 2.0), (dock_x + 1.1, dock_z + 2.0)]):
        create_beveled_cylinder(f"Pier_Piling_{pi+1}", 0.14, 0.8, (px, -0.15, pz), bevel_width=0.02, material=mat_wood_fence)
    # Cọc buộc dây thừng
    create_beveled_cylinder("Pier_Bollard_1", 0.12, 0.5, (dock_x + 1.2, 0.42, dock_z - 1.8), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Pier_Bollard_2", 0.12, 0.5, (dock_x + 1.2, 0.42, dock_z + 1.8), bevel_width=0.02, material=mat_wood_fence)
    # Thuyền gỗ nan đậu sát cầu cảng
    create_beveled_box("Fisher_Boat_Hull", (1.4, 0.40, 2.8), (16.0, 0.12, dock_z), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Fisher_Boat_Seat", (1.2, 0.08, 0.4), (16.0, 0.25, dock_z), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Fisher_Boat_Oar", 0.04, 2.2, (15.7, 0.35, dock_z), bevel_width=0.01, rotation=(0, 0.4, 0.6), material=mat_wood)
    # Giỏ cá tươi và giàn phơi cá
    create_beveled_cylinder("Fisher_Basket_OnDock", 0.32, 0.45, (dock_x + 0.8, 0.40, dock_z - 0.8), bevel_width=0.02, vertices=12, material=mat_wood)
    create_beveled_box("Fish_Drying_Rack", (0.3, 1.4, 1.8), (dock_x - 0.8, 0.70, dock_z + 1.6), bevel_width=0.02, material=mat_wood_fence)
    # Cần câu tre của Finn trên cầu cảng
    create_beveled_cylinder("NPC_Finn_Pier_Rod", 0.03, 3.2, (dock_x + 0.6, 1.6, dock_z), bevel_width=0.01, rotation=(0.4, 0, 0.3), material=mat_wood)
    create_beveled_cylinder("NPC_Finn_Bucket_Hat", 0.25, 0.15, (dock_x, 0.50, dock_z - 0.6), bevel_width=0.02, material=mat_wheat)

    # 5. CHỢ TRUNG TÂM (Z in [14, 20], X in [-4, 4])
    well_x, well_z = -1.6, 16.5
    create_beveled_cylinder("Well_Stone", 1.25, 0.95, (well_x, 0.48, well_z), bevel_width=0.04, vertices=16, material=mat_cobble)
    create_beveled_cylinder("Well_Water", 1.05, 0.12, (well_x, 0.70, well_z), bevel_width=0.01, material=mat_water)
    create_beveled_cylinder("Well_Post_1", 0.08, 2.4, (well_x - 1.0, 1.2, well_z), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Well_Post_2", 0.08, 2.4, (well_x + 1.0, 1.2, well_z), bevel_width=0.02, material=mat_wood)
    build_detailed_roof_gabled("Well_Roof", 2.2, 1.5, 0.7, (well_x, 2.2, well_z), overhang=0.2, ridge_along_x=True, material=mat_roof_red)

    # 2 Sạp chợ có bạt sọc đỏ trắng
    for i, sz in enumerate([15.0, 18.5]):
        ms_x = 2.8
        create_beveled_box(f"Market_Stall_{i+1}_Table", (2.8, 0.85, 1.4), (ms_x, 0.42, sz), bevel_width=0.03, material=mat_wood)
        for pi, (dx, dz) in enumerate([(-1.3, -0.6), (1.3, -0.6), (-1.3, 0.6), (1.3, 0.6)]):
            create_beveled_cylinder(f"Market_Stall_{i+1}_P{pi+1}", 0.06, 2.4, (ms_x + dx, 1.2, sz + dz), bevel_width=0.015, material=mat_wood)
        create_beveled_box(f"Market_Stall_{i+1}_Canopy", (3.2, 0.15, 1.8), (ms_x, 2.3, sz), bevel_width=0.04, material=mat_canopy_striped)
        create_beveled_box(f"Market_Produce_Box_{i+1}", (0.8, 0.3, 0.6), (ms_x - 0.6, 0.95, sz), bevel_width=0.02, material=mat_wood_fence)
        create_beveled_cylinder(f"Market_Barrel_{i+1}", 0.35, 0.75, (ms_x + 1.8, 0.38, sz), bevel_width=0.03, vertices=12, material=mat_wood_fence)

    cart_x, cart_z = -2.6, 18.8
    create_beveled_box("Cart_Body", (1.6, 0.5, 1.8), (cart_x, 0.55, cart_z), bevel_width=0.03, material=mat_wood)
    create_beveled_cylinder("Cart_Wheel_L", 0.42, 0.12, (cart_x - 0.9, 0.42, cart_z), bevel_width=0.03, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_cylinder("Cart_Wheel_R", 0.42, 0.12, (cart_x + 0.9, 0.42, cart_z), bevel_width=0.03, rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_beveled_box("Cart_Crate_1", (0.6, 0.5, 0.6), (cart_x - 0.3, 0.9, cart_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Cart_Crate_2", (0.5, 0.4, 0.5), (cart_x + 0.3, 0.85, cart_z), bevel_width=0.03, material=mat_wood)

    # 6. NHÀ RÈN CỦA VULCAN (TÂY: X = -11.0, Z = 21.0)
    sm_cx, sm_cz = -11.0, 21.0
    sm_w, sm_l, sm_h = 6.4, 5.6, 3.2
    create_beveled_box("Floor_Smith", (sm_w, 0.15, sm_l), (sm_cx, 0.08, sm_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_Smith", (sm_w, sm_h, 0.3), (sm_cx, sm_h/2, sm_cz - sm_l/2 + 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_Smith", (sm_w, sm_h, 0.3), (sm_cx, sm_h/2, sm_cz + sm_l/2 - 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_West_Smith", (0.3, sm_h, sm_l - 0.6), (sm_cx - sm_w/2 + 0.15, sm_h/2, sm_cz), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Smith_L", (0.3, sm_h, 1.9), (sm_cx + sm_w/2 - 0.15, sm_h/2, sm_cz - 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Smith_R", (0.3, sm_h, 1.9), (sm_cx + sm_w/2 - 0.15, sm_h/2, sm_cz + 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Smith_Top", (0.3, 0.8, 1.8), (sm_cx + sm_w/2 - 0.15, sm_h - 0.4, sm_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Smith", sm_w, sm_l, 1.8, (sm_cx, sm_h, sm_cz), overhang=0.3, ridge_along_x=False, material=mat_roof_red)

    # Ống khói đá lớn
    create_beveled_box("Chimney_Smith_Base", (1.2, 5.2, 1.2), (sm_cx - sm_w/2 + 0.7, 2.6, sm_cz - sm_l/2 + 0.7), bevel_width=0.04, material=mat_cobble)

    # 6.A NỘI THẤT NHÀ RÈN (DIORAMA CẮT VÁCH CHUẨN ẢNH 1.JPG)
    # Lò rèn vòm đá gạch cao bốc khói rực lửa cam đỏ (Blacksmith_Forge_Furnace-col, lửa phát quang)
    create_beveled_box("Blacksmith_Forge_Furnace-col", (1.7, 2.2, 1.5), (sm_cx - 1.6, 1.10, sm_cz - 1.5), bevel_width=0.04, material=mat_cobble)
    build_chamfered_rock("Blacksmith_Forge_Fire", (1.2, 0.55, 1.0), (sm_cx - 1.6, 0.90, sm_cz - 1.5), material=mat_lava_fire, seed_val=999)
    create_beveled_cylinder("Forge_Chimney_Flue", 0.35, 1.6, (sm_cx - 1.6, 2.4, sm_cz - 1.5), bevel_width=0.02, material=mat_cobble)

    # Đe sắt lớn (Anvil_Heavy-col) đặt trên bục gỗ/đá trung tâm
    create_beveled_cylinder("Anvil_Block_Center", 0.48, 0.72, (sm_cx, 0.36, sm_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Anvil_Heavy-col", (0.55, 0.35, 0.95), (sm_cx, 0.85, sm_cz), bevel_width=0.03, material=mat_metal)

    # Rương sắt chứa phôi thép vụn (Chest_Scrap_Metal-col)
    create_beveled_box("Chest_Scrap_Metal-col", (0.85, 0.55, 0.65), (sm_cx - 1.8, 0.28, sm_cz + 1.5), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Chest_Scrap_Lumps", (0.65, 0.22, 0.45), (sm_cx - 1.8, 0.60, sm_cz + 1.5), bevel_width=0.02, material=mat_metal)

    # Rương gỗ chứa than củi (Chest_Charcoal-col)
    create_beveled_box("Chest_Charcoal-col", (0.85, 0.55, 0.65), (sm_cx - 0.7, 0.28, sm_cz + 1.5), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Chest_Charcoal_Lumps", (0.65, 0.20, 0.45), (sm_cx - 0.7, 0.58, sm_cz + 1.5), bevel_width=0.02, material=mat_stone)

    # Bể nước làm nguội tôi kim loại (Quench_Tank-col)
    create_beveled_box("Quench_Tank-col", (1.5, 0.65, 0.80), (sm_cx + 1.3, 0.33, sm_cz - 1.5), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Quench_Tank_Water", (1.3, 0.12, 0.60), (sm_cx + 1.3, 0.58, sm_cz - 1.5), bevel_width=0.01, material=mat_water)

    # Giá vũ khí trên tường đá có kiếm, khiên tròn, áo giáp sắt treo (Weapon_Rack_Wall-col)
    create_beveled_box("Weapon_Rack_Wall-col", (2.6, 0.95, 0.16), (sm_cx + 0.4, 1.85, sm_cz - sm_l/2 + 0.35), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Weapon_Rack_Sword_1", 0.04, 1.4, (sm_cx - 0.2, 1.85, sm_cz - sm_l/2 + 0.45), bevel_width=0.01, rotation=(0, 0, 0.75), material=mat_metal)
    create_beveled_cylinder("Weapon_Rack_Sword_2", 0.04, 1.4, (sm_cx + 0.3, 1.85, sm_cz - sm_l/2 + 0.45), bevel_width=0.01, rotation=(0, 0, -0.75), material=mat_metal)
    create_beveled_cylinder("Weapon_Rack_Shield", 0.38, 0.06, (sm_cx + 1.1, 1.85, sm_cz - sm_l/2 + 0.45), bevel_width=0.02, rotation=(1.57, 0, 0), vertices=16, material=mat_metal)
    create_beveled_box("Weapon_Rack_Armor_Plate", (0.45, 0.60, 0.12), (sm_cx - 0.7, 1.85, sm_cz - sm_l/2 + 0.45), bevel_width=0.02, material=mat_metal)

    # Bàn thợ nguội và công cụ kìm búa đe (Blacksmith_Workbench-col)
    create_beveled_box("Blacksmith_Workbench-col", (0.8, 0.88, 2.0), (sm_cx + 1.8, 0.44, sm_cz + 0.5), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Smith_Vise_Tool", (0.22, 0.25, 0.25), (sm_cx + 1.8, 0.98, sm_cz - 0.2), bevel_width=0.01, material=mat_metal)
    create_beveled_cylinder("Smith_Bench_Hammer", 0.03, 0.45, (sm_cx + 1.8, 0.90, sm_cz + 0.3), bevel_width=0.01, rotation=(0, 0, 1.57), material=mat_metal)
    create_beveled_cylinder("Smith_Bench_Tongs", 0.025, 0.50, (sm_cx + 1.8, 0.90, sm_cz + 0.8), bevel_width=0.01, rotation=(0, 0, 1.2), material=mat_metal)

    # Đạo cụ Thợ Rèn Vulcan bên ngoài (-6.8, 0, 20.0)
    out_x, out_z = -6.8, 20.0
    create_beveled_cylinder("Anvil_Outdoor_Log", 0.45, 0.7, (out_x, 0.35, out_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Anvil_Outdoor_Iron", (0.55, 0.35, 0.9), (out_x, 0.82, out_z), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Forge_Outdoor_Base", (1.4, 0.9, 1.2), (out_x - 1.2, 0.45, out_z - 1.4), bevel_width=0.04, material=mat_cobble)
    build_chamfered_rock("Forge_Outdoor_Fire", (1.0, 0.35, 0.8), (out_x - 1.2, 0.95, out_z - 1.4), material=mat_lava_fire, seed_val=888)
    create_beveled_cylinder("NPC_Vulcan_Hammer_Shaft", 0.04, 0.8, (out_x + 0.1, 1.05, out_z), bevel_width=0.01, rotation=(0, 0, 1.2), material=mat_wood)
    create_beveled_box("NPC_Vulcan_Hammer_Head", (0.22, 0.14, 0.14), (out_x + 0.4, 1.2, out_z), bevel_width=0.02, material=mat_metal)

    # 7. NHÀ GIẢ KIM CỦA ARIA (ĐÔNG: X = 11.0, Z = 21.0)
    al_cx, al_cz = 11.0, 21.0
    al_w, al_l, al_h = 6.4, 5.6, 3.2
    create_beveled_box("Floor_Alchemist", (al_w, 0.15, al_l), (al_cx, 0.08, al_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_Alchemist", (al_w, al_h, 0.3), (al_cx, al_h/2, al_cz - al_l/2 + 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_Alchemist", (al_w, al_h, 0.3), (al_cx, al_h/2, al_cz + al_l/2 - 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_East_Alchemist", (0.3, al_h, al_l - 0.6), (al_cx + al_w/2 - 0.15, al_h/2, al_cz), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Alchemist_L", (0.3, al_h, 1.9), (al_cx - al_w/2 + 0.15, al_h/2, al_cz - 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Alchemist_R", (0.3, al_h, 1.9), (al_cx - al_w/2 + 0.15, al_h/2, al_cz + 1.8), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_Alchemist_Top", (0.3, 0.8, 1.8), (al_cx - al_w/2 + 0.15, al_h - 0.4, al_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_Alchemist", al_w, al_l, 1.8, (al_cx, al_h, al_cz), overhang=0.3, ridge_along_x=False, material=mat_roof_teal)

    # Ống khói & Khói ma thuật uốn lượn bay ra
    create_beveled_cylinder("Chimney_Alchemist", 0.38, 4.8, (al_cx + al_w/2 - 0.8, 2.4, al_cz - al_l/2 + 0.8), bevel_width=0.03, material=mat_cobble)
    build_chamfered_rock("Smoke_Alchemist_1", (1.1, 1.1, 1.1), (al_cx + al_w/2 - 0.8, 5.2, al_cz - al_l/2 + 0.8), material=mat_mystic_cyan, seed_val=111)
    build_chamfered_rock("Smoke_Alchemist_2", (1.4, 1.4, 1.4), (al_cx + al_w/2 - 0.5, 6.0, al_cz - al_l/2 + 0.6), material=mat_mystic_cyan, seed_val=222)
    build_chamfered_rock("Smoke_Alchemist_3", (1.8, 1.8, 1.8), (al_cx + al_w/2 - 0.2, 7.0, al_cz - al_l/2 + 0.4), material=mat_mystic_cyan, seed_val=333)

    # 7.A NỘI THẤT NHÀ GIẢ KIM (DIORAMA CẮT VÁCH CHUẨN ẢNH 1.JPG)
    # Vạc đồng ma thuật phát quang cyan/ngọc bích đang sôi sục khói bốc lên (Alchemist_Cauldron_Glowing-col)
    create_beveled_cylinder("Cauldron_Hearth_Stand", 0.62, 0.35, (al_cx, 0.18, al_cz), bevel_width=0.03, vertices=16, material=mat_cobble)
    create_beveled_cylinder("Cauldron_Magic_Fire", 0.55, 0.22, (al_cx, 0.12, al_cz), bevel_width=0.02, material=mat_mystic_purple)
    create_beveled_cylinder("Alchemist_Cauldron_Glowing-col", 0.85, 0.90, (al_cx, 0.55, al_cz), bevel_width=0.03, vertices=16, material=mat_metal)
    create_beveled_cylinder("Alchemist_Potion_Surface", 0.74, 0.12, (al_cx, 0.92, al_cz), bevel_width=0.01, material=mat_mystic_cyan)
    build_chamfered_rock("Alchemist_Cauldron_Vapor", (0.7, 0.45, 0.7), (al_cx, 1.18, al_cz), material=mat_mystic_cyan, seed_val=777)

    # Bàn thí nghiệm mở cuốn sách ma thuật cổ, đèn cầy và ống nghiệm (Alchemy_Lab_Table-col)
    create_beveled_box("Alchemy_Lab_Table-col", (0.9, 0.88, 2.8), (al_cx + al_w/2 - 0.7, 0.44, al_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Spellbook_Open", (0.42, 0.08, 0.55), (al_cx + al_w/2 - 0.7, 0.92, al_cz - 0.7), bevel_width=0.015, material=mat_wheat)
    create_beveled_box("Spellbook_Pages", (0.38, 0.06, 0.50), (al_cx + al_w/2 - 0.7, 0.96, al_cz - 0.7), bevel_width=0.01, material=mat_wall)
    create_beveled_cylinder("Candle_Wax", 0.05, 0.20, (al_cx + al_w/2 - 0.7, 0.98, al_cz - 1.2), bevel_width=0.01, material=mat_wall)
    create_beveled_cylinder("Candle_Flame", 0.025, 0.06, (al_cx + al_w/2 - 0.7, 1.11, al_cz - 1.2), bevel_width=0.005, material=mat_lava_fire)
    create_beveled_box("Test_Tube_Rack", (0.18, 0.22, 0.55), (al_cx + al_w/2 - 0.7, 0.99, al_cz + 0.6), bevel_width=0.01, material=mat_wood_fence)
    create_beveled_cylinder("Test_Tube_1", 0.03, 0.22, (al_cx + al_w/2 - 0.7, 1.05, al_cz + 0.45), bevel_width=0.005, material=mat_mystic_cyan)
    create_beveled_cylinder("Test_Tube_2", 0.03, 0.22, (al_cx + al_w/2 - 0.7, 1.05, al_cz + 0.60), bevel_width=0.005, material=mat_mystic_purple)
    create_beveled_cylinder("Test_Tube_3", 0.03, 0.22, (al_cx + al_w/2 - 0.7, 1.05, al_cz + 0.75), bevel_width=0.005, material=mat_lava_fire)

    # Tủ sách cổ ma thuật cao kịch trần đầy sách cổ (Alchemy_Tall_Bookshelf-col)
    create_beveled_box("Alchemy_Tall_Bookshelf-col", (4.2, 2.9, 0.55), (al_cx, 1.45, al_cz - al_l/2 + 0.45), bevel_width=0.03, material=mat_wood_fence)
    # Hàng sách cổ màu sắc trên kệ
    create_beveled_box("Bookshelf_Row_Teal", (3.6, 0.45, 0.40), (al_cx, 0.70, al_cz - al_l/2 + 0.50), bevel_width=0.02, material=mat_roof_teal)
    create_beveled_box("Bookshelf_Row_Red", (3.6, 0.45, 0.40), (al_cx, 1.50, al_cz - al_l/2 + 0.50), bevel_width=0.02, material=mat_roof_red)
    create_beveled_box("Bookshelf_Row_Gold", (3.6, 0.45, 0.40), (al_cx, 2.30, al_cz - al_l/2 + 0.50), bevel_width=0.02, material=mat_wheat)

    # Vô số kệ và chai lọ độc dược đủ sắc màu đỏ tím lục lam (Potion_Shelves-col)
    create_beveled_box("Potion_Shelves-col", (0.35, 1.6, 1.8), (al_cx + al_w/2 - 0.4, 1.80, al_cz + 1.2), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_cylinder("Potion_Bottle_Cyan", 0.10, 0.28, (al_cx + al_w/2 - 0.4, 1.35, al_cz + 0.7), bevel_width=0.01, material=mat_mystic_cyan)
    create_beveled_cylinder("Potion_Bottle_Purple", 0.10, 0.28, (al_cx + al_w/2 - 0.4, 1.35, al_cz + 1.2), bevel_width=0.01, material=mat_mystic_purple)
    create_beveled_cylinder("Potion_Bottle_Red", 0.10, 0.28, (al_cx + al_w/2 - 0.4, 1.35, al_cz + 1.7), bevel_width=0.01, material=mat_lava_fire)
    create_beveled_cylinder("Potion_Bottle_Green", 0.09, 0.25, (al_cx + al_w/2 - 0.4, 2.05, al_cz + 0.9), bevel_width=0.01, material=mat_vegetable)
    create_beveled_cylinder("Potion_Bottle_Teal", 0.09, 0.25, (al_cx + al_w/2 - 0.4, 2.05, al_cz + 1.5), bevel_width=0.01, material=mat_roof_teal)

    # Chùm thảo mộc khô treo lơ lửng từ xà nhà (Hanging_Herbs-col)
    create_beveled_box("Hanging_Herbs_Rafter", (al_w - 0.8, 0.16, 0.16), (al_cx, 2.85, al_cz), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Hanging_Herbs-col", 0.18, 0.55, (al_cx - 1.0, 2.35, al_cz), bevel_width=0.02, rotation=(0.1, 0, 0.1), material=mat_vegetable)
    create_beveled_cylinder("Hanging_Herbs_Bundle_2", 0.18, 0.55, (al_cx, 2.38, al_cz), bevel_width=0.02, rotation=(-0.1, 0, 0.1), material=mat_wheat)
    create_beveled_cylinder("Hanging_Herbs_Bundle_3", 0.18, 0.55, (al_cx + 1.0, 2.32, al_cz), bevel_width=0.02, rotation=(0.1, 0, -0.1), material=mat_vegetable)

    # Vườn thảo mộc ngoài hiên
    create_beveled_box("Herb_Bed_1", (1.2, 0.35, 3.2), (al_cx - al_w/2 - 0.8, 0.18, al_cz + 1.2), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("Herb_Soil_1", (1.0, 0.10, 3.0), (al_cx - al_w/2 - 0.8, 0.36, al_cz + 1.2), bevel_width=0.02, material=mat_vegetable)

    # Đạo cụ Nhà Giả Kim Aria tại vị trí NPC (7.5, 0, 21.0)
    create_beveled_cylinder("NPC_Aria_Potion_Flask_Cyan", 0.12, 0.35, (7.5, 0.70, 20.6), bevel_width=0.02, material=mat_mystic_cyan)
    create_beveled_cylinder("NPC_Aria_Potion_Flask_Purple", 0.12, 0.35, (7.5, 0.70, 21.4), bevel_width=0.02, material=mat_mystic_purple)
    create_beveled_box("NPC_Aria_Herb_Desk", (0.8, 0.6, 1.4), (7.5, 0.30, 21.0), bevel_width=0.02, material=mat_wood)

    # 8. NHÀ DÂN CƯ (TÂY: X = -10.0, Z = 28.5)
    hs_cx, hs_cz = -10.0, 28.5
    hs_w, hs_l, hs_h = 5.8, 5.0, 3.0
    create_beveled_box("Floor_House", (hs_w, 0.15, hs_l), (hs_cx, 0.08, hs_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Wall_North_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz - hs_l/2 + 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz + hs_l/2 - 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_West_House", (0.3, hs_h, hs_l - 0.6), (hs_cx - hs_w/2 + 0.15, hs_h/2, hs_cz), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_L", (0.3, hs_h, 1.6), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz - 1.4), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_R", (0.3, hs_h, 1.6), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz + 1.4), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_Top", (0.3, 0.7, 1.8), (hs_cx + hs_w/2 - 0.15, hs_h - 0.35, hs_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_House", hs_w, hs_l, 1.6, (hs_cx, hs_h, hs_cz), overhang=0.3, ridge_along_x=False, material=mat_roof_red)

    # 8.A NỘI THẤT NHÀ DÂN (DIORAMA CẮT VÁCH CHUẨN ẢNH 1.JPG)
    # Giường ngủ gỗ nệm đỏ gối trắng ấm cúng (House_Cozy_Bed-col)
    create_beveled_box("House_Cozy_Bed-col", (1.7, 0.50, 2.3), (hs_cx - hs_w/2 + 1.2, 0.25, hs_cz - hs_l/2 + 1.5), bevel_width=0.03, material=mat_wood)
    create_beveled_box("House_Bed_Mattress", (1.5, 0.25, 2.1), (hs_cx - hs_w/2 + 1.2, 0.55, hs_cz - hs_l/2 + 1.5), bevel_width=0.03, material=mat_roof_red)
    create_beveled_box("House_Bed_Pillow", (0.9, 0.16, 0.45), (hs_cx - hs_w/2 + 1.2, 0.72, hs_cz - hs_l/2 + 0.7), bevel_width=0.02, material=mat_wall)

    # Tủ quần áo 2 cánh cao lớn (House_Wardrobe_Tall-col)
    create_beveled_box("House_Wardrobe_Tall-col", (1.3, 2.4, 0.70), (hs_cx - hs_w/2 + 0.85, 1.20, hs_cz + hs_l/2 - 0.7), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("House_Wardrobe_Door_L", (0.58, 2.1, 0.04), (hs_cx - hs_w/2 + 0.55, 1.20, hs_cz + hs_l/2 - 0.33), bevel_width=0.015, material=mat_wood)
    create_beveled_box("House_Wardrobe_Door_R", (0.58, 2.1, 0.04), (hs_cx - hs_w/2 + 1.15, 1.20, hs_cz + hs_l/2 - 0.33), bevel_width=0.015, material=mat_wood)
    create_beveled_cylinder("House_Wardrobe_Handle_L", 0.02, 0.12, (hs_cx - hs_w/2 + 0.80, 1.20, hs_cz + hs_l/2 - 0.30), bevel_width=0.005, material=mat_metal)
    create_beveled_cylinder("House_Wardrobe_Handle_R", 0.02, 0.12, (hs_cx - hs_w/2 + 0.90, 1.20, hs_cz + hs_l/2 - 0.30), bevel_width=0.005, material=mat_metal)

    # Tấm thảm sàn dệt thổ cẩm sọc kẻ (House_Floor_Rug-col)
    create_beveled_box("House_Floor_Rug-col", (2.2, 0.02, 2.2), (hs_cx + 0.5, 0.09, hs_cz), bevel_width=0.01, material=mat_canopy_striped)

    # Bàn con bên cửa sổ có rèm vải xanh (House_Side_Table-col)
    create_beveled_cylinder("House_Side_Table-col", 0.52, 0.80, (hs_cx + 1.3, 0.40, hs_cz + 1.3), bevel_width=0.02, vertices=14, material=mat_wood)
    create_beveled_cylinder("House_Side_Stool", 0.25, 0.45, (hs_cx + 1.3, 0.22, hs_cz + 0.5), bevel_width=0.02, vertices=10, material=mat_wood)
    # Rèm cửa vải xanh trên tường South
    create_beveled_box("House_Window_Frame", (1.4, 1.2, 0.08), (hs_cx + 1.3, 1.80, hs_cz + hs_l/2 - 0.25), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("House_Window_Curtain_L", (0.4, 1.1, 0.06), (hs_cx + 0.8, 1.80, hs_cz + hs_l/2 - 0.22), bevel_width=0.02, material=mat_roof_teal)
    create_beveled_box("House_Window_Curtain_R", (0.4, 1.1, 0.06), (hs_cx + 1.8, 1.80, hs_cz + hs_l/2 - 0.22), bevel_width=0.02, material=mat_roof_teal)

    # 9. KHU LÂM NGHIỆP CỦA GROVER (TÂY BẮC: X = -14.0, Z = 38.0)
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

    # Đạo cụ Tiều Phu Grover (-13.5, 0, 36.5)
    create_beveled_cylinder("NPC_Grover_Chopping_Block", 0.40, 0.60, (-13.5, 0.30, 36.5), bevel_width=0.03, vertices=12, material=mat_wood)
    create_beveled_cylinder("NPC_Grover_Lumber_Axe_Handle", 0.04, 0.90, (-13.5, 0.85, 36.5), bevel_width=0.01, rotation=(0.2, 0, 0.3), material=mat_wood)
    create_beveled_box("NPC_Grover_Lumber_Axe_Blade", (0.26, 0.18, 0.06), (-13.4, 0.65, 36.5), bevel_width=0.01, material=mat_metal)
    create_beveled_cylinder("NPC_Grover_Beanie_Hat", 0.22, 0.20, (-13.5, 0.65, 35.8), bevel_width=0.02, material=mat_roof_red)

    build_stylized_tree("Tree_Lumber_1", (lm_cx - 4.5, 0, lm_cz - 3.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Lumber_2", (lm_cx - 4.0, 0, lm_cz + 3.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Lumber_3", (lm_cx, 0, lm_cz + 4.5), scale=1.4, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # 10. KHU MỎ ĐÁ CỦA BROCK (ĐÔNG BẮC: X = 14.0, Z = 38.0)
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

    # Đạo cụ Thợ Mỏ Brock (12.5, 0, 36.5)
    create_beveled_cylinder("NPC_Brock_Pickaxe_Handle", 0.04, 1.1, (12.5, 0.55, 36.5), bevel_width=0.01, rotation=(0, 0, 0.5), material=mat_wood)
    create_beveled_box("NPC_Brock_Pickaxe_Head", (0.45, 0.12, 0.08), (12.3, 0.95, 36.5), bevel_width=0.01, material=mat_metal)
    create_beveled_cylinder("NPC_Brock_Safety_Helmet", 0.22, 0.22, (12.5, 0.20, 35.8), bevel_width=0.02, material=mat_lava_fire)
    build_chamfered_rock("NPC_Brock_Ore_Cluster", (0.8, 0.5, 0.8), (12.5, 0.25, 37.3), material=mat_stone, seed_val=777)

    # 11. CÂY CỐI TRANG TRÍ BAO QUANH LÀNG
    build_stylized_tree("Tree_Gate_L", (-5.0, 0, 5.0), scale=1.1, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Gate_R", (5.5, 0, 4.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Smith_Back", (-18.5, 0, 14.0), scale=1.0, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Alchemist_Back", (16.5, 0, 16.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_House_South", (-17.0, 0, 32.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Mine_East", (18.5, 0, 35.0), scale=1.5, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # 12. XUẤT RA GLB & LƯU FILE BLEND AN TOÀN
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

    # 13. CƠ CHẾ MẮT THẦN TỰ KIỂM TRA (VISUAL PREVIEW RENDER)
    render_preview_path = os.path.join(workspace_dir, "Assets", "Models", "_preview_render.png")
    setup_preview_render(render_preview_path, resolution=(1280, 720), camera_pos=(-26, -34, 22), target_pos=(0, -18, 1))
    print("=== DỰNG BẢN ĐỒ LÀNG MỞ RỘNG HOÀN TẤT VỚI CHẤT LƯỢNG CAO ===")

if __name__ == '__main__':
    build_village()
