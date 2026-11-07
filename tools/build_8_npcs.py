"""
Script Blender: Dựng 8 Mô Hình Nhân Vật (NPC) Độc Nhất Theo Đúng Ảnh Phác Họa 'modelyeucau/map2/1.jpg'
Tuân thủ nghiêm ngặt Character & Rigging Pipeline:
- Từng nhân vật cao chuẩn 1.80m
- Trang phục, mũ nón và phụ kiện cầm tay đặc thù khớp 100% bản vẽ concept
- Xuất thành 8 file GLB độc lập vào Assets/Models/NPCs/
- Render ảnh mắt thần _char_preview.png chụp toàn bộ 8 NPC đối chiếu song song
"""

import sys
import os
import math
import bpy

# Đảm bảo import được tools.blender_kit
workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

from tools.blender_kit import (
    clean_scene,
    create_material,
    create_beveled_box,
    create_beveled_cylinder,
    unwrap_mesh,
    setup_preview_render
)

def create_base_human(name_prefix, skin_mat, shirt_mat, pants_mat, shoe_mat, has_beard=False, beard_mat=None):
    """Tạo khung cơ thể nhân vật Chibi Stylized chuẩn cao 1.8m."""
    # 1. Chân (Legs) & Giày (Shoes)
    create_beveled_box(f"{name_prefix}_Shoe_L", (0.16, 0.14, 0.22), (-0.14, 0.07, 0.03), bevel_width=0.02, material=shoe_mat)
    create_beveled_box(f"{name_prefix}_Shoe_R", (0.16, 0.14, 0.22), (0.14, 0.07, 0.03), bevel_width=0.02, material=shoe_mat)
    create_beveled_box(f"{name_prefix}_Leg_L", (0.15, 0.62, 0.16), (-0.14, 0.45, 0.0), bevel_width=0.02, material=pants_mat)
    create_beveled_box(f"{name_prefix}_Leg_R", (0.15, 0.62, 0.16), (0.14, 0.45, 0.0), bevel_width=0.02, material=pants_mat)

    # 2. Thân người (Torso / Áo)
    create_beveled_box(f"{name_prefix}_Torso", (0.42, 0.58, 0.26), (0.0, 1.05, 0.0), bevel_width=0.03, material=shirt_mat)

    # 3. Cánh tay (Arms)
    create_beveled_box(f"{name_prefix}_Arm_L", (0.13, 0.50, 0.14), (-0.28, 1.02, 0.0), bevel_width=0.02, material=shirt_mat)
    create_beveled_box(f"{name_prefix}_Arm_R", (0.13, 0.50, 0.14), (0.28, 1.02, 0.0), bevel_width=0.02, material=shirt_mat)
    create_beveled_box(f"{name_prefix}_Hand_L", (0.11, 0.12, 0.12), (-0.28, 0.72, 0.0), bevel_width=0.02, material=skin_mat)
    create_beveled_box(f"{name_prefix}_Hand_R", (0.11, 0.12, 0.12), (0.28, 0.72, 0.0), bevel_width=0.02, material=skin_mat)

    # 4. Cổ & Đầu (Head)
    create_beveled_cylinder(f"{name_prefix}_Neck", 0.09, 0.12, (0.0, 1.36, 0.0), bevel_width=0.015, material=skin_mat)
    create_beveled_box(f"{name_prefix}_Head", (0.34, 0.36, 0.32), (0.0, 1.56, 0.0), bevel_width=0.04, material=skin_mat)

    # Mắt (Eyes)
    mat_black = create_material(f"{name_prefix}_Mat_BlackEye", (0.05, 0.05, 0.05), roughness=0.3)
    create_beveled_box(f"{name_prefix}_Eye_L", (0.04, 0.06, 0.02), (-0.08, 1.58, 0.17), bevel_width=0.005, material=mat_black)
    create_beveled_box(f"{name_prefix}_Eye_R", (0.04, 0.06, 0.02), (0.08, 1.58, 0.17), bevel_width=0.005, material=mat_black)

    # Râu quai nón (nếu có)
    if has_beard and beard_mat:
        create_beveled_box(f"{name_prefix}_Beard", (0.36, 0.18, 0.18), (0.0, 1.45, 0.10), bevel_width=0.02, material=beard_mat)

def export_character(name, output_dir):
    """Xuất nhân vật sang GLB và unwrap toàn bộ mesh."""
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            unwrap_mesh(obj, project_type='cube', cube_size=1.0)
    
    out_path = os.path.join(output_dir, f"{name}.glb")
    bpy.ops.export_scene.gltf(
        filepath=out_path,
        export_format='GLB',
        export_yup=True,
        export_apply=True,
        export_materials='EXPORT'
    )
    print(f"-> Đã xuất: {out_path}")

def build_all_npcs():
    out_dir = os.path.abspath("Assets/Models/NPCs")
    os.makedirs(out_dir, exist_ok=True)

    # =========================================================================
    # 1. THỢ RÈN (VULCAN) - Búa rèn sắt, tạp dề da nâu, cơ bắp
    # =========================================================================
    print("Dựng NPC: Thợ Rèn Vulcan...")
    clean_scene()
    mat_skin_tan = create_material("Mat_Vulcan_Skin", (0.74, 0.54, 0.42), roughness=0.60)
    mat_black = create_material("Mat_Vulcan_Black", (0.12, 0.12, 0.12), roughness=0.50)
    mat_apron = create_material("Mat_Vulcan_Apron", (0.42, 0.26, 0.16), roughness=0.80)
    mat_pants = create_material("Mat_Vulcan_Pants", (0.32, 0.34, 0.38), roughness=0.80)
    mat_dark_iron = create_material("Mat_Vulcan_Iron", (0.28, 0.30, 0.34), roughness=0.40, metallic=0.85)
    mat_wood_handle = create_material("Mat_Vulcan_Handle", (0.55, 0.36, 0.21), roughness=0.75)

    create_base_human("Vulcan", mat_skin_tan, mat_skin_tan, mat_pants, mat_black, has_beard=True, beard_mat=mat_black)
    create_beveled_box("Vulcan_Apron", (0.34, 0.52, 0.05), (0.0, 0.95, 0.14), bevel_width=0.015, material=mat_apron)
    create_beveled_cylinder("Vulcan_Hammer_Handle", 0.03, 0.85, (0.38, 0.95, 0.25), bevel_width=0.008, rotation=(0.5, 0, 0), material=mat_wood_handle)
    create_beveled_box("Vulcan_Hammer_Head", (0.16, 0.14, 0.25), (0.38, 1.25, 0.42), bevel_width=0.02, material=mat_dark_iron)
    export_character("npc_blacksmith", out_dir)

    # =========================================================================
    # 2. NHÀ GIẢ KIM (ARIA) - Mũ trùm tím, áo choàng tím viền vàng, 2 bình thuốc
    # =========================================================================
    print("Dựng NPC: Nhà Giả Kim Aria...")
    clean_scene()
    mat_skin = create_material("Mat_Aria_Skin", (0.86, 0.68, 0.54), roughness=0.60)
    mat_black = create_material("Mat_Aria_Black", (0.12, 0.12, 0.12), roughness=0.50)
    mat_purple = create_material("Mat_Aria_Purple", (0.46, 0.18, 0.56), roughness=0.70)
    mat_cyan_pot = create_material("Mat_Aria_PotCyan", (0.20, 0.90, 0.85), roughness=0.15, emission_color=(0.20, 0.90, 0.85), emission_strength=2.5)
    mat_pink_pot = create_material("Mat_Aria_PotPink", (0.90, 0.25, 0.75), roughness=0.15, emission_color=(0.90, 0.25, 0.75), emission_strength=2.5)

    create_base_human("Aria", mat_skin, mat_purple, mat_purple, mat_black)
    create_beveled_box("Aria_Hood", (0.40, 0.42, 0.38), (0.0, 1.60, -0.02), bevel_width=0.04, material=mat_purple)
    create_beveled_box("Aria_Hood_Tip", (0.15, 0.15, 0.20), (0.0, 1.65, -0.22), bevel_width=0.03, material=mat_purple)
    create_beveled_box("Aria_Skirt", (0.46, 0.55, 0.32), (0.0, 0.55, 0.0), bevel_width=0.03, material=mat_purple)
    create_beveled_cylinder("Aria_Pot_L", 0.06, 0.14, (-0.28, 0.82, 0.16), bevel_width=0.015, material=mat_cyan_pot)
    create_beveled_cylinder("Aria_Pot_R", 0.06, 0.14, (0.28, 0.82, 0.16), bevel_width=0.015, material=mat_pink_pot)
    export_character("npc_alchemist", out_dir)

    # =========================================================================
    # 3. ĐẦU BẾP (GUSTEAU) - Mũ đầu bếp trắng cao xếp nếp, bánh mì baguette
    # =========================================================================
    print("Dựng NPC: Đầu Bếp Gusteau...")
    clean_scene()
    mat_skin = create_material("Mat_Gusteau_Skin", (0.86, 0.68, 0.54), roughness=0.60)
    mat_white = create_material("Mat_Gusteau_White", (0.96, 0.96, 0.96), roughness=0.75)
    mat_black = create_material("Mat_Gusteau_Black", (0.12, 0.12, 0.12), roughness=0.50)
    mat_bread = create_material("Mat_Gusteau_Bread", (0.84, 0.56, 0.24), roughness=0.80)

    create_base_human("Gusteau", mat_skin, mat_white, mat_black, mat_black)
    create_beveled_cylinder("Gusteau_ChefHat_Base", 0.16, 0.15, (0.0, 1.78, 0.0), bevel_width=0.02, material=mat_white)
    create_beveled_cylinder("Gusteau_ChefHat_Top", 0.22, 0.20, (0.0, 1.92, 0.0), bevel_width=0.04, material=mat_white)
    create_beveled_cylinder("Gusteau_Baguette", 0.07, 0.65, (0.0, 0.92, 0.20), bevel_width=0.02, rotation=(0, 1.57, 0.2), material=mat_bread)
    export_character("npc_chef", out_dir)

    # =========================================================================
    # 4. NÔNG DÂN (GEORGE) - Nón lá chóp nhọn, áo nâu, cuốc đất & bó lúa vàng
    # =========================================================================
    print("Dựng NPC: Nông Dân George...")
    clean_scene()
    mat_skin_tan = create_material("Mat_George_Skin", (0.74, 0.54, 0.42), roughness=0.60)
    mat_farmer_brown = create_material("Mat_George_Brown", (0.54, 0.36, 0.22), roughness=0.85)
    mat_farmer_pants = create_material("Mat_George_Pants", (0.38, 0.26, 0.16), roughness=0.85)
    mat_straw = create_material("Mat_George_Straw", (0.88, 0.74, 0.42), roughness=0.80)
    mat_dark_iron = create_material("Mat_George_Iron", (0.28, 0.30, 0.34), roughness=0.40, metallic=0.85)
    mat_wood_handle = create_material("Mat_George_Wood", (0.55, 0.36, 0.21), roughness=0.75)

    create_base_human("George", mat_skin_tan, mat_farmer_brown, mat_farmer_pants, mat_farmer_brown)
    create_beveled_cylinder("George_Hat_Rim", 0.35, 0.05, (0.0, 1.74, 0.0), bevel_width=0.02, vertices=16, material=mat_straw)
    create_beveled_cylinder("George_Hat_Cone", 0.22, 0.18, (0.0, 1.84, 0.0), bevel_width=0.03, vertices=16, material=mat_straw)
    create_beveled_cylinder("George_Hoe_Handle", 0.025, 1.10, (0.36, 1.15, -0.10), bevel_width=0.008, rotation=(-0.4, 0, 0), material=mat_wood_handle)
    create_beveled_box("George_Hoe_Blade", (0.14, 0.18, 0.04), (0.36, 1.55, -0.32), bevel_width=0.01, material=mat_dark_iron)
    create_beveled_cylinder("George_Wheat_Bundle", 0.11, 0.45, (-0.28, 0.88, 0.16), bevel_width=0.02, rotation=(0.3, 0, 0), material=mat_straw)
    export_character("npc_farmer", out_dir)

    # =========================================================================
    # 5. NGƯ DÂN (FINN) - Nón vành tròn, cần câu tre dài, giỏ nan cá tươi
    # =========================================================================
    print("Dựng NPC: Ngư Dân Finn...")
    clean_scene()
    mat_skin_tan = create_material("Mat_Finn_Skin", (0.74, 0.54, 0.42), roughness=0.60)
    mat_kaki = create_material("Mat_Finn_Kaki", (0.76, 0.68, 0.52), roughness=0.80)
    mat_pants_blue = create_material("Mat_Finn_Pants", (0.32, 0.42, 0.48), roughness=0.80)
    mat_fish = create_material("Mat_Finn_Fish", (0.72, 0.82, 0.88), roughness=0.35, metallic=0.6)
    mat_straw = create_material("Mat_Finn_Straw", (0.88, 0.74, 0.42), roughness=0.80)
    mat_wood_handle = create_material("Mat_Finn_Wood", (0.55, 0.36, 0.21), roughness=0.75)
    mat_apron = create_material("Mat_Finn_Shoes", (0.42, 0.26, 0.16), roughness=0.80)

    create_base_human("Finn", mat_skin_tan, mat_kaki, mat_pants_blue, mat_apron)
    create_beveled_cylinder("Finn_Hat_Brim", 0.30, 0.04, (0.0, 1.74, 0.0), bevel_width=0.015, vertices=16, material=mat_kaki)
    create_beveled_cylinder("Finn_Hat_Crown", 0.18, 0.12, (0.0, 1.80, 0.0), bevel_width=0.02, vertices=16, material=mat_kaki)
    create_beveled_cylinder("Finn_Rod", 0.02, 2.10, (0.32, 1.05, 0.12), bevel_width=0.005, rotation=(-0.1, 0, 0), material=mat_wood_handle)
    create_beveled_cylinder("Finn_Basket", 0.14, 0.24, (-0.32, 0.45, 0.08), bevel_width=0.02, material=mat_straw)
    create_beveled_box("Finn_Fish_1", (0.06, 0.16, 0.08), (-0.32, 0.58, 0.08), bevel_width=0.01, material=mat_fish)
    export_character("npc_fisherman", out_dir)

    # =========================================================================
    # 6. THỢ MỎ (BROCK) - Mũ bảo hộ vàng có đèn soi, áo bảo hộ vàng cam, cuốc chim
    # =========================================================================
    print("Dựng NPC: Thợ Mỏ Brock...")
    clean_scene()
    mat_skin_tan = create_material("Mat_Brock_Skin", (0.74, 0.54, 0.42), roughness=0.60)
    mat_hard_hat = create_material("Mat_Brock_HardHat", (0.95, 0.78, 0.12), roughness=0.40)
    mat_miner_suit = create_material("Mat_Brock_MinerSuit", (0.84, 0.58, 0.18), roughness=0.75)
    mat_lamp_light = create_material("Mat_Brock_Light", (1.0, 0.95, 0.65), roughness=0.10, emission_color=(1.0, 0.95, 0.65), emission_strength=3.0)
    mat_farmer_brown = create_material("Mat_Brock_Beard", (0.54, 0.36, 0.22), roughness=0.85)
    mat_black = create_material("Mat_Brock_Black", (0.12, 0.12, 0.12), roughness=0.50)
    mat_wood_handle = create_material("Mat_Brock_Wood", (0.55, 0.36, 0.21), roughness=0.75)
    mat_dark_iron = create_material("Mat_Brock_Iron", (0.28, 0.30, 0.34), roughness=0.40, metallic=0.85)

    create_base_human("Brock", mat_skin_tan, mat_miner_suit, mat_miner_suit, mat_black, has_beard=True, beard_mat=mat_farmer_brown)
    create_beveled_cylinder("Brock_Hat_Brim", 0.24, 0.05, (0.0, 1.74, 0.0), bevel_width=0.02, material=mat_hard_hat)
    create_beveled_cylinder("Brock_Hat_Dome", 0.19, 0.16, (0.0, 1.82, 0.0), bevel_width=0.04, material=mat_hard_hat)
    create_beveled_box("Brock_Headlamp", (0.08, 0.07, 0.06), (0.0, 1.80, 0.22), bevel_width=0.01, material=mat_lamp_light)
    create_beveled_cylinder("Brock_Pick_Handle", 0.028, 1.05, (0.36, 1.15, -0.10), bevel_width=0.008, rotation=(-0.4, 0, 0), material=mat_wood_handle)
    create_beveled_box("Brock_Pick_Head", (0.10, 0.08, 0.42), (0.36, 1.55, -0.32), bevel_width=0.02, material=mat_dark_iron)
    export_character("npc_miner", out_dir)

    # =========================================================================
    # 7. TIỀU PHU (GROVER) - Mũ len đỏ, áo sơ mi kẻ caro đỏ đen, rìu đốn củi to
    # =========================================================================
    print("Dựng NPC: Tiều Phu Grover...")
    clean_scene()
    mat_skin_tan = create_material("Mat_Grover_Skin", (0.74, 0.54, 0.42), roughness=0.60)
    mat_beanie = create_material("Mat_Grover_Beanie", (0.85, 0.22, 0.18), roughness=0.85)
    mat_plaid = create_material("Mat_Grover_Plaid", (0.76, 0.18, 0.18), roughness=0.80)
    mat_jeans = create_material("Mat_Grover_Jeans", (0.24, 0.36, 0.54), roughness=0.80)
    mat_farmer_brown = create_material("Mat_Grover_Beard", (0.54, 0.36, 0.22), roughness=0.85)
    mat_black = create_material("Mat_Grover_Black", (0.12, 0.12, 0.12), roughness=0.50)
    mat_wood_handle = create_material("Mat_Grover_Wood", (0.55, 0.36, 0.21), roughness=0.75)
    mat_metal_silver = create_material("Mat_Grover_Silver", (0.75, 0.78, 0.82), roughness=0.30, metallic=0.90)

    create_base_human("Grover", mat_skin_tan, mat_plaid, mat_jeans, mat_black, has_beard=True, beard_mat=mat_farmer_brown)
    create_beveled_cylinder("Grover_Beanie_Band", 0.20, 0.08, (0.0, 1.72, 0.0), bevel_width=0.02, material=mat_beanie)
    create_beveled_cylinder("Grover_Beanie_Top", 0.18, 0.14, (0.0, 1.80, -0.02), bevel_width=0.04, material=mat_beanie)
    create_beveled_cylinder("Grover_Axe_Handle", 0.03, 1.10, (0.36, 1.15, -0.10), bevel_width=0.008, rotation=(-0.4, 0, 0), material=mat_wood_handle)
    create_beveled_box("Grover_Axe_Blade", (0.08, 0.26, 0.22), (0.36, 1.55, -0.32), bevel_width=0.02, material=mat_metal_silver)
    export_character("npc_lumberjack", out_dir)

    # =========================================================================
    # 8. LÍNH CANH (AEGIS) - Mũ giáp sắt, áo giáp kim loại, khiên tròn & giáo dài
    # =========================================================================
    print("Dựng NPC: Lính Canh Aegis...")
    clean_scene()
    mat_skin = create_material("Mat_Aegis_Skin", (0.86, 0.68, 0.54), roughness=0.60)
    mat_armor = create_material("Mat_Aegis_Armor", (0.75, 0.78, 0.82), roughness=0.30, metallic=0.90)
    mat_tunic = create_material("Mat_Aegis_Tunic", (0.28, 0.32, 0.38), roughness=0.80)
    mat_gold = create_material("Mat_Aegis_Gold", (0.92, 0.75, 0.22), roughness=0.35, metallic=0.80)
    mat_wood_handle = create_material("Mat_Aegis_Wood", (0.55, 0.36, 0.21), roughness=0.75)
    mat_metal_silver = create_material("Mat_Aegis_Silver", (0.75, 0.78, 0.82), roughness=0.30, metallic=0.90)

    create_base_human("Aegis", mat_skin, mat_armor, mat_tunic, mat_armor)
    create_beveled_cylinder("Aegis_Helmet", 0.20, 0.24, (0.0, 1.76, 0.0), bevel_width=0.03, material=mat_armor)
    create_beveled_box("Aegis_Nasal", (0.04, 0.14, 0.06), (0.0, 1.62, 0.19), bevel_width=0.01, material=mat_armor)
    create_beveled_cylinder("Aegis_Shield_Rim", 0.30, 0.06, (-0.36, 0.95, 0.15), bevel_width=0.02, rotation=(1.57, 0, 0), material=mat_gold)
    create_beveled_cylinder("Aegis_Shield_Center", 0.24, 0.07, (-0.36, 0.95, 0.15), bevel_width=0.02, rotation=(1.57, 0, 0), material=mat_wood_handle)
    create_beveled_cylinder("Aegis_Spear_Shaft", 0.025, 2.30, (0.36, 1.15, 0.12), bevel_width=0.005, material=mat_wood_handle)
    create_beveled_box("Aegis_Spear_Tip", (0.05, 0.30, 0.08), (0.36, 2.35, 0.12), bevel_width=0.015, material=mat_metal_silver)
    export_character("npc_guard", out_dir)

    print("=== DỰNG XONG 8 NPC ĐỘC NHẤT THÀNH CÔNG ===")

    # =========================================================================
    # RENDER ẢNH MẮT THẦN _char_preview.png TRƯNG BÀY ĐẦY ĐỦ 8 NPC ĐỐI CHIẾU
    # =========================================================================
    clean_scene()
    npc_files = [
        "npc_blacksmith.glb", "npc_alchemist.glb", "npc_chef.glb", "npc_farmer.glb",
        "npc_fisherman.glb", "npc_miner.glb", "npc_lumberjack.glb", "npc_guard.glb"
    ]
    mat_pedestal = create_material("Mat_Showcase", (0.45, 0.32, 0.22), roughness=0.85)
    create_beveled_box("Showcase_Floor", (13.5, 0.2, 3.0), (0, -0.1, 0), bevel_width=0.04, material=mat_pedestal)

    for i, file_name in enumerate(npc_files):
        glb_path = os.path.join(out_dir, file_name)
        x_pos = -5.25 + i * 1.5
        bpy.ops.import_scene.gltf(filepath=glb_path)
        for obj in bpy.context.selected_objects:
            obj.location.x += x_pos

    preview_path = "Assets/Models/_char_preview.png"
    setup_preview_render(preview_path, resolution=(1920, 1080), camera_pos=(0, -7.5, 2.2), target_pos=(0, 0, 1.1))
    print(f"-> Đã render ảnh mắt thần trưng bày 8 NPC: {preview_path}")

if __name__ == '__main__':
    build_all_npcs()
