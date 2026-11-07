"""
Script Blender 3D: Dựng Bản Đồ Làng Mở Rộng Liền Kề WorldMap (Village District)
Sử dụng Thư Viện Procedural Chuẩn 'tools/blender_kit.py'.
Bảo đảm:
- Không dùng primitive thô sơ (No Raw Primitives).
- Toàn bộ chi tiết có Bevel Modifier 2-3 segments bo viền bắt sáng.
- Cây cối và đá tự nhiên vát cạnh Low-Poly cách điệu.
- Mái ngói có riềm chìa ra ngoài (overhang) và độ dày chân thực.
- Render ảnh mắt thần kiểm tra trực quan '_preview_render.png'.
"""

import sys
import os
import bpy
import math

# Thêm thư mục gốc vào sys.path để import tools.blender_kit
workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

from tools.blender_kit import (
    clean_scene,
    create_material,
    create_beveled_box,
    create_beveled_cylinder,
    build_chamfered_rock,
    build_stylized_tree,
    build_detailed_roof_gabled,
    setup_preview_render
)

def build_village():
    print("=== BẮT ĐẦU DỰNG BẢN ĐỒ LÀNG MỞ RỘNG (PROCEDURAL PIPELINE) ===")
    clean_scene()
    
    # 1. BẢNG VẬT LIỆU CHUẨN PALETTE
    mat_dirt = create_material("Mat_Dirt", (0.54, 0.36, 0.21), roughness=0.90)
    mat_stone = create_material("Mat_Stone", (0.52, 0.54, 0.56), roughness=0.80)
    mat_wood = create_material("Mat_Wood", (0.55, 0.36, 0.21), roughness=0.75)
    mat_wood_fence = create_material("Mat_Wood_Fence", (0.42, 0.26, 0.16), roughness=0.80)
    mat_metal = create_material("Mat_Metal", (0.62, 0.65, 0.70), roughness=0.35, metallic=0.85)
    mat_roof_red = create_material("Mat_Roof_Red", (0.80, 0.28, 0.22), roughness=0.80)
    mat_roof_teal = create_material("Mat_Roof_Teal", (0.16, 0.56, 0.54), roughness=0.80)
    mat_canopy_striped = create_material("Mat_Canopy_Striped", (0.86, 0.24, 0.20), roughness=0.85)
    mat_mystic_cyan = create_material("Mat_Mystic_Cyan", (0.20, 0.88, 0.82), roughness=0.20, emission_color=(0.20, 0.88, 0.82), emission_strength=2.2)
    mat_lava_fire = create_material("Mat_Lava_Fire", (1.00, 0.45, 0.05), roughness=0.40, emission_color=(1.00, 0.45, 0.05), emission_strength=2.6)
    mat_foliage = create_material("Mat_Foliage", (0.24, 0.56, 0.24), roughness=0.85)
    mat_vegetable = create_material("Mat_Vegetable", (0.36, 0.74, 0.28), roughness=0.80)
    mat_wall = create_material("Mat_Wall_Stone", (0.62, 0.60, 0.56), roughness=0.85)

    # 2. ĐƯỜNG MÒN ĐẤT NỐI LIỀN TRỰC TIẾP TỪ ĐẢO ĐÁ (Z=0.2, X=4.8) VÀO LÀNG
    create_beveled_box("Path_Connector_Island", (3.2, 0.04, 4.5), (4.0, 0.02, 2.5), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_Connector_Bend", (3.4, 0.04, 4.5), (2.0, 0.02, 6.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_Village_Main_Gate", (3.6, 0.04, 8.0), (0.0, 0.02, 11.5), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_Village_Main_Avenue", (4.0, 0.04, 12.0), (0.0, 0.02, 20.0), bevel_width=0.02, material=mat_dirt)
    create_beveled_box("Path_Market_Square", (11.0, 0.04, 9.0), (0.0, 0.02, 29.5), bevel_width=0.02, material=mat_dirt)
    
    # Các nhánh đường tới các phân khu
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

    for row in range(3):
        rz = 7.5 + row * 1.1
        create_beveled_box(f"Crop_Soil_{row}", (4.2, 0.1, 0.8), (-5.2, 0.05, rz), bevel_width=0.02, material=mat_dirt)
        for col in range(4):
            cx = -6.5 + col * 0.9
            build_chamfered_rock(f"Cabbage_{row}_{col}", (0.52, 0.44, 0.52), (cx, 0.22, rz), material=mat_vegetable, seed_val=row*10+col)

    # 4. QUÁN ĂN / TAVERN CỦA ĐẦU BẾP (ĐÔNG: X = 8.0, Z = 7.5)
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

    create_beveled_box("Oven_Chef_Base", (1.4, 1.3, 1.2), (cf_cx + cf_w/2 - 1.0, 0.65, cf_cz - cf_l/2 + 1.0), bevel_width=0.04, material=mat_stone)
    create_beveled_box("Oven_Chef_Fire", (0.8, 0.45, 0.5), (cf_cx - cf_w/2 + 1.0, 0.4, cf_cz - cf_l/2 + 1.0), bevel_width=0.02, material=mat_lava_fire)
    create_beveled_box("Dining_Table_Chef", (1.2, 0.85, 2.6), (cf_cx, 0.42, cf_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Dining_Bench_Chef_L", (0.35, 0.45, 2.6), (cf_cx - 0.9, 0.22, cf_cz), bevel_width=0.02, material=mat_wood)
    create_beveled_box("Dining_Bench_Chef_R", (0.35, 0.45, 2.6), (cf_cx + 0.9, 0.22, cf_cz), bevel_width=0.02, material=mat_wood)

    # 5. CHỢ TRUNG TÂM (Z in [14, 20], X in [-4, 4])
    well_x, well_z = -1.6, 16.5
    create_beveled_cylinder("Well_Stone", 1.25, 0.95, (well_x, 0.48, well_z), bevel_width=0.04, vertices=16, material=mat_stone)
    create_beveled_cylinder("Well_Water", 1.05, 0.12, (well_x, 0.70, well_z), bevel_width=0.01, material=mat_mystic_cyan)
    create_beveled_cylinder("Well_Post_1", 0.08, 2.4, (well_x - 1.0, 1.2, well_z), bevel_width=0.02, material=mat_wood)
    create_beveled_cylinder("Well_Post_2", 0.08, 2.4, (well_x + 1.0, 1.2, well_z), bevel_width=0.02, material=mat_wood)
    build_detailed_roof_gabled("Well_Roof", 2.2, 1.5, 0.7, (well_x, 2.2, well_z), overhang=0.2, ridge_along_x=True, material=mat_roof_red)

    # 2 Sạp chợ có bạt sọc
    for i, sz in enumerate([15.0, 18.5]):
        ms_x = 2.8
        create_beveled_box(f"Market_Stall_{i+1}_Table", (2.8, 0.85, 1.4), (ms_x, 0.42, sz), bevel_width=0.03, material=mat_wood)
        for pi, (dx, dz) in enumerate([(-1.3, -0.6), (1.3, -0.6), (-1.3, 0.6), (1.3, 0.6)]):
            create_beveled_cylinder(f"Market_Stall_{i+1}_P{pi+1}", 0.06, 2.4, (ms_x + dx, 1.2, sz + dz), bevel_width=0.015, material=mat_wood)
        create_beveled_box(f"Market_Stall_{i+1}_Canopy", (3.2, 0.15, 1.8), (ms_x, 2.3, sz), bevel_width=0.04, material=mat_canopy_striped)

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

    create_beveled_box("Chimney_Smith_Base", (1.2, 5.2, 1.2), (sm_cx - sm_w/2 + 0.7, 2.6, sm_cz - sm_l/2 + 0.7), bevel_width=0.04, material=mat_stone)
    create_beveled_box("Forge_Indoor_Base", (1.5, 0.9, 1.3), (sm_cx - 1.6, 0.45, sm_cz - 1.4), bevel_width=0.04, material=mat_stone)
    create_beveled_box("Forge_Indoor_Fire", (1.1, 0.25, 0.9), (sm_cx - 1.6, 0.95, sm_cz - 1.4), bevel_width=0.02, material=mat_lava_fire)
    create_beveled_cylinder("Anvil_Indoor_Log", 0.45, 0.7, (sm_cx, 0.35, sm_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Anvil_Indoor_Iron", (0.5, 0.3, 0.8), (sm_cx, 0.8, sm_cz), bevel_width=0.03, material=mat_metal)

    out_x, out_z = -6.8, 20.0
    create_beveled_cylinder("Anvil_Outdoor_Log", 0.45, 0.7, (out_x, 0.35, out_z), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Anvil_Outdoor_Iron", (0.55, 0.35, 0.9), (out_x, 0.82, out_z), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Forge_Outdoor_Base", (1.4, 0.9, 1.2), (out_x - 1.2, 0.45, out_z - 1.4), bevel_width=0.04, material=mat_stone)
    create_beveled_box("Forge_Outdoor_Fire", (1.0, 0.2, 0.8), (out_x - 1.2, 0.95, out_z - 1.4), bevel_width=0.02, material=mat_lava_fire)

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

    create_beveled_cylinder("Chimney_Alchemist", 0.38, 4.8, (al_cx + al_w/2 - 0.8, 2.4, al_cz - al_l/2 + 0.8), bevel_width=0.03, material=mat_stone)
    build_chamfered_rock("Smoke_Alchemist_1", (1.0, 1.0, 1.0), (al_cx + al_w/2 - 0.8, 5.1, al_cz - al_l/2 + 0.8), material=mat_mystic_cyan, seed_val=111)
    build_chamfered_rock("Smoke_Alchemist_2", (1.3, 1.3, 1.3), (al_cx + al_w/2 - 0.6, 5.8, al_cz - al_l/2 + 0.6), material=mat_mystic_cyan, seed_val=222)

    create_beveled_cylinder("Cauldron_Base", 0.75, 0.75, (al_cx, 0.38, al_cz), bevel_width=0.03, material=mat_metal)
    create_beveled_cylinder("Cauldron_Potion", 0.65, 0.1, (al_cx, 0.72, al_cz), bevel_width=0.01, material=mat_mystic_cyan)
    create_beveled_box("Bookshelf_Alchemist", (3.8, 2.4, 0.5), (al_cx, 1.2, al_cz - al_l/2 + 0.4), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("Potion_Table", (0.8, 0.85, 2.6), (al_cx + al_w/2 - 0.6, 0.42, al_cz), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Herb_Bed_1", (1.2, 0.35, 3.2), (al_cx - al_w/2 - 0.8, 0.18, al_cz + 1.2), bevel_width=0.02, material=mat_wood_fence)
    create_beveled_box("Herb_Soil_1", (1.0, 0.10, 3.0), (al_cx - al_w/2 - 0.8, 0.36, al_cz + 1.2), bevel_width=0.02, material=mat_vegetable)

    # 8. NHÀ DÂN CƯ (TÂY: X = -10.0, Z = 28.5)
    hs_cx, hs_cz = -10.0, 28.5
    hs_w, hs_l, hs_h = 5.8, 5.0, 3.0
    create_beveled_box("Floor_House", (hs_w, 0.15, hs_l), (hs_cx, 0.08, hs_cz), bevel_width=0.03, material=mat_stone)
    create_beveled_box("Wall_North_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz - hs_l/2 + 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_South_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz + hs_l/2 - 0.15), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_West_House", (0.3, hs_h, hs_l - 0.6), (hs_cx - hs_w/2 + 0.15, hs_h/2, hs_cz), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_L", (0.3, hs_h, 1.6), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz - 1.4), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_R", (0.3, hs_h, 1.6), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz + 1.4), bevel_width=0.03, material=mat_wall)
    create_beveled_box("Wall_Front_House_Top", (0.3, 0.7, 1.8), (hs_cx + hs_w/2 - 0.15, hs_h - 0.35, hs_cz), bevel_width=0.03, material=mat_wall)
    build_detailed_roof_gabled("Roof_House", hs_w, hs_l, 1.6, (hs_cx, hs_h, hs_cz), overhang=0.3, ridge_along_x=False, material=mat_roof_red)

    create_beveled_box("Bed_Frame", (1.6, 0.45, 2.2), (hs_cx - hs_w/2 + 1.1, 0.22, hs_cz - hs_l/2 + 1.4), bevel_width=0.03, material=mat_wood)
    create_beveled_box("Bed_Mattress", (1.4, 0.25, 2.0), (hs_cx - hs_w/2 + 1.1, 0.50, hs_cz - hs_l/2 + 1.4), bevel_width=0.03, material=mat_roof_red)
    create_beveled_box("Wardrobe", (1.2, 2.1, 0.6), (hs_cx - hs_w/2 + 0.8, 1.05, hs_cz + hs_l/2 - 0.6), bevel_width=0.03, material=mat_wood_fence)
    create_beveled_box("House_Rug", (1.8, 0.02, 1.8), (hs_cx + 0.5, 0.09, hs_cz), bevel_width=0.01, material=mat_canopy_striped)

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
    create_beveled_cylinder("Ore_Furnace", 1.3, 2.6, (mn_cx - 4.2, 1.3, mn_cz - 2.5), bevel_width=0.04, vertices=16, material=mat_stone)
    create_beveled_box("Ore_Furnace_Fire", (0.8, 0.6, 0.5), (mn_cx - 4.2, 0.6, mn_cz - 1.8), bevel_width=0.02, material=mat_lava_fire)
    create_beveled_box("Rail_L", (0.08, 0.08, 4.5), (mn_cx + 2.0, 0.06, mn_cz - 1.0), bevel_width=0.01, material=mat_metal)
    create_beveled_box("Rail_R", (0.08, 0.08, 4.5), (mn_cx + 2.8, 0.06, mn_cz - 1.0), bevel_width=0.01, material=mat_metal)
    create_beveled_box("Minecart_Body", (1.2, 0.65, 1.6), (mn_cx + 2.4, 0.58, mn_cz - 1.5), bevel_width=0.03, material=mat_metal)
    create_beveled_box("Minecart_Ore", (0.9, 0.3, 1.3), (mn_cx + 2.4, 0.88, mn_cz - 1.5), bevel_width=0.03, material=mat_stone)

    # 11. CÂY CỐI TRANG TRÍ BAO QUANH LÀNG (Bố trí khéo léo để không che khuất góc nhìn Camera Isometric vào các ngôi nhà)
    build_stylized_tree("Tree_Gate_L", (-5.0, 0, 5.0), scale=1.1, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Gate_R", (5.5, 0, 4.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Smith_Back", (-18.5, 0, 14.0), scale=1.0, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Alchemist_Back", (16.5, 0, 16.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_House_South", (-17.0, 0, 32.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_stylized_tree("Tree_Mine_East", (18.5, 0, 35.0), scale=1.5, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # 12. XUẤT RA GLB & LƯU FILE BLEND AN TOÀN
    out_glb = "Assets/Models/village_map.glb"
    print(f"Xuất mô hình sang: {out_glb}")
    bpy.ops.export_scene.gltf(
        filepath=out_glb,
        export_format='GLB',
        export_yup=True,
        export_apply=True,
        export_materials='EXPORT'
    )
    blend_path = "Assets/Blender_Source/village_map.blend"
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    # 13. CƠ CHẾ MẮT THẦN TỰ KIỂM TRA (VISUAL PREVIEW RENDER)
    render_preview_path = "Assets/Models/_preview_render.png"
    setup_preview_render(render_preview_path, resolution=(1280, 720), camera_pos=(28, -25, 24), target_pos=(0, -20, 2))
    print("=== DỰNG BẢN ĐỒ LÀNG MỞ RỘNG HOÀN TẤT VỚI CHẤT LƯỢNG CAO ===")

if __name__ == '__main__':
    build_village()
