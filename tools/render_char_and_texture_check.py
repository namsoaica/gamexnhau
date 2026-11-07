"""
Script Blender 3D: Render Mắt Thần Tự Kiểm Tra Nhân Vật (_char_preview.png)
và Bọc Thử Texture 3D (_texture_3d_check.png)
Tuân thủ Zero-Blindspot Protocol và yêu cầu từ modelyeucau/map2/1.jpg.
"""

import sys
import os
import bpy
import math
from mathutils import Vector

workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

from tools.blender_kit import (
    clean_scene,
    create_material,
    unwrap_mesh,
    create_beveled_box,
    create_beveled_cylinder,
    build_chamfered_rock,
    build_detailed_roof_gabled
)

def render_texture_3d_check(out_path):
    print("=== RENDER 3D TEXTURE CHECK (_texture_3d_check.png) ===")
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
    
    mat_wood = create_material("Mat_Wood", (0.55, 0.35, 0.20), roughness=0.75, texture_path=p_wood)
    mat_cobble = create_material("Mat_Cobble", (0.41, 0.42, 0.44), roughness=0.80, texture_path=p_cobble)
    mat_metal = create_material("Mat_Metal", (0.58, 0.60, 0.64), roughness=0.35, metallic=0.85, texture_path=p_metal)
    mat_roof_red = create_material("Mat_Roof_Red", (0.66, 0.22, 0.16), roughness=0.75, texture_path=p_roof_red)
    mat_roof_teal = create_material("Mat_Roof_Teal", (0.15, 0.55, 0.51), roughness=0.75, texture_path=p_roof_teal)
    mat_canopy = create_material("Mat_Canopy", (0.88, 0.23, 0.23), roughness=0.85, texture_path=p_canopy)
    mat_dirt = create_material("Mat_Dirt", (0.54, 0.36, 0.21), roughness=0.90, texture_path=p_dirt)
    mat_cyan = create_material("Mat_Cyan", (0.20, 0.88, 0.82), roughness=0.20, emission_color=(0.20, 0.88, 0.82), emission_strength=2.5)
    mat_fire = create_material("Mat_Fire", (1.00, 0.45, 0.05), roughness=0.40, emission_color=(1.00, 0.45, 0.05), emission_strength=3.0)

    # Nền đất
    create_beveled_box("Check_Floor", (18.0, 0.1, 12.0), (0, 0.05, 0), bevel_width=0.02, material=mat_dirt)

    # 1. Khối gỗ & thùng tròn
    create_beveled_box("Check_Wood_Box", (1.8, 1.8, 1.8), (-5.0, 1.0, 2.0), bevel_width=0.06, material=mat_wood)
    create_beveled_cylinder("Check_Wood_Barrel", 0.7, 1.8, (-5.0, 1.0, -2.0), bevel_width=0.04, vertices=16, material=mat_wood)

    # 2. Khối đá cobblestone & đe kim loại
    create_beveled_box("Check_Cobble_Pillar", (1.8, 2.6, 1.8), (-1.8, 1.4, 2.0), bevel_width=0.06, material=mat_cobble)
    create_beveled_box("Check_Metal_Anvil", (1.0, 0.7, 1.6), (-1.8, 0.45, -2.0), bevel_width=0.04, material=mat_metal)

    # 3. Mái ngói đỏ & mái ngói teal
    build_detailed_roof_gabled("Check_Roof_Red", 2.4, 2.4, 1.4, (1.8, 1.2, 2.0), overhang=0.2, ridge_along_x=True, material=mat_roof_red)
    build_detailed_roof_gabled("Check_Roof_Teal", 2.4, 2.4, 1.4, (1.8, 1.2, -2.0), overhang=0.2, ridge_along_x=True, material=mat_roof_teal)

    # 4. Bạt sọc đỏ trắng & Lửa/Thuốc ma thuật phát sáng
    create_beveled_box("Check_Canopy", (2.8, 0.2, 2.0), (5.5, 2.0, 2.0), bevel_width=0.04, material=mat_canopy)
    create_beveled_cylinder("Check_Cyan_Potion", 0.5, 1.0, (5.5, 0.6, 2.0), bevel_width=0.02, material=mat_cyan)
    create_beveled_box("Check_Lava_Fire", (1.4, 0.6, 1.4), (5.5, 0.4, -2.0), bevel_width=0.03, material=mat_fire)

    # Camera & Light
    setup_render_camera(out_path, camera_pos=(12, -14, 11), target_pos=(0, 0, 1), ortho_scale=16.0)

def render_char_preview(out_path):
    print("=== RENDER NPC & CHARACTER PREVIEW (_char_preview.png) ===")
    clean_scene()
    
    tex_dir = os.path.join(workspace_dir, "Assets", "Textures", "Tileable")
    p_wood = os.path.join(tex_dir, "tex_wood_seamless.png")
    p_metal = os.path.join(tex_dir, "tex_metal_seamless.png")
    p_canopy = os.path.join(tex_dir, "tex_canopy_striped.png")

    mat_wood = create_material("Mat_Wood", (0.55, 0.35, 0.20), roughness=0.75, texture_path=p_wood)
    mat_metal = create_material("Mat_Metal", (0.58, 0.60, 0.64), roughness=0.35, metallic=0.85, texture_path=p_metal)
    mat_skin = create_material("Mat_Skin", (0.90, 0.74, 0.62), roughness=0.60)
    mat_apron = create_material("Mat_Apron", (0.35, 0.25, 0.22), roughness=0.70)
    mat_purple = create_material("Mat_Purple", (0.42, 0.23, 0.51), roughness=0.65)
    mat_white = create_material("Mat_White", (0.95, 0.95, 0.92), roughness=0.70)
    mat_bread = create_material("Mat_Bread", (0.83, 0.58, 0.29), roughness=0.70)
    mat_straw = create_material("Mat_Straw", (0.81, 0.63, 0.38), roughness=0.80)
    mat_flannel = create_material("Mat_Flannel", (0.65, 0.18, 0.18), roughness=0.80)
    mat_yellow_miner = create_material("Mat_Miner", (0.75, 0.56, 0.26), roughness=0.75)
    mat_cyan = create_material("Mat_Cyan", (0.20, 0.88, 0.82), roughness=0.20, emission_color=(0.20, 0.88, 0.82), emission_strength=2.6)
    mat_lamp = create_material("Mat_Lamp", (1.00, 0.85, 0.20), roughness=0.20, emission_color=(1.00, 0.85, 0.20), emission_strength=3.0)

    # Dựng bục trưng bày 8 NPC
    create_beveled_box("Stage_Floor", (24.0, 0.2, 5.0), (0, 0.1, 0), bevel_width=0.03, material=mat_wood)

    npc_configs = [
        (-8.5, "Vulcan", mat_apron, "Hammer"),
        (-6.0, "Aria", mat_purple, "Potion"),
        (-3.5, "Gusteau", mat_white, "Bread"),
        (-1.0, "George", mat_straw, "Hoe"),
        (1.5, "Finn", mat_straw, "Rod"),
        (4.0, "Brock", mat_yellow_miner, "Pickaxe"),
        (6.5, "Grover", mat_flannel, "Axe"),
        (9.0, "Aegis", mat_metal, "SpearShield")
    ]

    for x_pos, name, body_mat, prop_type in npc_configs:
        # Thân hình Stylized chuẩn chiều cao 1.80m
        # Chân
        create_beveled_cylinder(f"{name}_Leg_L", 0.12, 0.70, (x_pos - 0.18, 0.35, 0), bevel_width=0.02, material=mat_metal if prop_type == "SpearShield" else mat_wood)
        create_beveled_cylinder(f"{name}_Leg_R", 0.12, 0.70, (x_pos + 0.18, 0.35, 0), bevel_width=0.02, material=mat_metal if prop_type == "SpearShield" else mat_wood)
        # Thân mình Torso (chiều cao 0.70m)
        create_beveled_box(f"{name}_Torso", (0.58, 0.65, 0.35), (x_pos, 1.05, 0), bevel_width=0.04, material=body_mat)
        # Đầu Head (0.35m)
        create_beveled_box(f"{name}_Head", (0.36, 0.38, 0.34), (x_pos, 1.55, 0), bevel_width=0.04, material=mat_skin)

        # Phụ kiện đạo cụ đặc trưng
        if prop_type == "Hammer":
            # Vulcan: Búa rèn + Đe nhỏ
            create_beveled_cylinder(f"{name}_Hammer_Shaft", 0.04, 0.8, (x_pos + 0.5, 1.0, 0.2), bevel_width=0.01, rotation=(0, 0, 0.5), material=mat_wood)
            create_beveled_box(f"{name}_Hammer_Head", (0.24, 0.15, 0.15), (x_pos + 0.7, 1.25, 0.2), bevel_width=0.02, material=mat_metal)
            create_beveled_box(f"{name}_Anvil_Small", (0.4, 0.4, 0.6), (x_pos + 0.6, 0.2, -0.2), bevel_width=0.03, material=mat_metal)
        elif prop_type == "Potion":
            # Aria: Áo choàng mũ trùm + 2 bình thuốc
            create_beveled_cylinder(f"{name}_Hood", 0.24, 0.25, (x_pos, 1.75, 0), bevel_width=0.03, material=mat_purple)
            create_beveled_cylinder(f"{name}_Flask_L", 0.08, 0.25, (x_pos - 0.45, 0.95, 0.2), bevel_width=0.01, material=mat_cyan)
            create_beveled_cylinder(f"{name}_Flask_R", 0.08, 0.25, (x_pos + 0.45, 0.95, 0.2), bevel_width=0.01, material=mat_cyan)
        elif prop_type == "Bread":
            # Gusteau: Mũ bếp cao + 2 ổ bánh baguette
            create_beveled_cylinder(f"{name}_Chef_Hat", 0.22, 0.45, (x_pos, 1.85, 0), bevel_width=0.02, vertices=12, material=mat_white)
            create_beveled_cylinder(f"{name}_Baguette_1", 0.07, 0.65, (x_pos - 0.35, 1.15, 0.25), bevel_width=0.02, rotation=(0.4, 0, 0.4), material=mat_bread)
            create_beveled_cylinder(f"{name}_Baguette_2", 0.07, 0.65, (x_pos + 0.35, 1.15, 0.25), bevel_width=0.02, rotation=(-0.4, 0, 0.4), material=mat_bread)
        elif prop_type == "Hoe":
            # George: Nón lá chóp + Cuốc làm vườn + Bó lúa
            create_beveled_cylinder(f"{name}_Cone_Hat", 0.38, 0.18, (x_pos, 1.82, 0), bevel_width=0.02, vertices=12, material=mat_straw)
            create_beveled_cylinder(f"{name}_Hoe_Handle", 0.04, 1.8, (x_pos + 0.45, 1.0, 0.2), bevel_width=0.01, rotation=(0.1, 0, 0.2), material=mat_wood)
            create_beveled_box(f"{name}_Hoe_Blade", (0.20, 0.06, 0.12), (x_pos + 0.55, 0.15, 0.2), bevel_width=0.01, material=mat_metal)
            create_beveled_cylinder(f"{name}_Wheat", 0.22, 0.70, (x_pos - 0.45, 0.95, 0.2), bevel_width=0.02, material=mat_straw)
        elif prop_type == "Rod":
            # Finn: Nón bucket + Cần câu tre + Giỏ cá
            create_beveled_cylinder(f"{name}_Bucket_Hat", 0.26, 0.16, (x_pos, 1.80, 0), bevel_width=0.02, material=mat_straw)
            create_beveled_cylinder(f"{name}_Fishing_Rod", 0.03, 2.8, (x_pos + 0.45, 1.4, 0.2), bevel_width=0.01, rotation=(0.2, 0, -0.1), material=mat_wood)
            create_beveled_cylinder(f"{name}_Fish_Creel", 0.25, 0.40, (x_pos - 0.45, 0.25, 0.2), bevel_width=0.02, material=mat_straw)
        elif prop_type == "Pickaxe":
            # Brock: Mũ đèn bảo hộ + Cuốc chim
            create_beveled_cylinder(f"{name}_Helmet", 0.24, 0.20, (x_pos, 1.80, 0), bevel_width=0.02, material=mat_lamp)
            create_beveled_cylinder(f"{name}_Pickaxe_Handle", 0.04, 1.2, (x_pos + 0.45, 1.0, 0.2), bevel_width=0.01, rotation=(0, 0, 0.4), material=mat_wood)
            create_beveled_box(f"{name}_Pickaxe_Head", (0.42, 0.12, 0.08), (x_pos + 0.35, 1.45, 0.2), bevel_width=0.01, material=mat_metal)
        elif prop_type == "Axe":
            # Grover: Mũ len đỏ + Rìu đốn củi
            create_beveled_cylinder(f"{name}_Beanie", 0.22, 0.20, (x_pos, 1.80, 0), bevel_width=0.02, material=mat_flannel)
            create_beveled_cylinder(f"{name}_Axe_Handle", 0.04, 1.1, (x_pos + 0.45, 1.0, 0.2), bevel_width=0.01, rotation=(0.2, 0, 0.3), material=mat_wood)
            create_beveled_box(f"{name}_Axe_Blade", (0.28, 0.18, 0.06), (x_pos + 0.6, 1.35, 0.2), bevel_width=0.01, material=mat_metal)
        elif prop_type == "SpearShield":
            # Aegis: Mũ giáp sắt + Ngọn giáo dài + Khiên tròn
            create_beveled_cylinder(f"{name}_Iron_Helmet", 0.22, 0.28, (x_pos, 1.80, 0), bevel_width=0.02, material=mat_metal)
            create_beveled_cylinder(f"{name}_Spear_Shaft", 0.04, 2.6, (x_pos + 0.45, 1.3, 0.2), bevel_width=0.01, material=mat_wood)
            create_beveled_box(f"{name}_Spear_Blade", (0.10, 0.35, 0.04), (x_pos + 0.45, 2.7, 0.2), bevel_width=0.01, material=mat_metal)
            create_beveled_cylinder(f"{name}_Shield", 0.42, 0.08, (x_pos - 0.45, 1.0, 0.2), bevel_width=0.02, rotation=(1.57, 0, 0), material=mat_metal)

    setup_render_camera(out_path, camera_pos=(0, -11.0, 3.2), target_pos=(0, 0, 1.2), ortho_scale=22.0)

def setup_render_camera(out_path, camera_pos, target_pos, ortho_scale=20.0, resolution=(1280, 720)):
    light_data = bpy.data.lights.new(name="Sun", type='SUN')
    light_data.energy = 2.8
    light_data.color = (1.0, 0.98, 0.94)
    light_obj = bpy.data.objects.new(name="Sun", object_data=light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = (10, -10, 20)
    light_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(45))

    cam_data = bpy.data.cameras.new(name="Camera")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = ortho_scale
    cam_obj = bpy.data.objects.new(name="Camera", object_data=cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = camera_pos

    direction = Vector(target_pos) - Vector(camera_pos)
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()
    bpy.context.scene.camera = cam_obj

    bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
    bpy.context.scene.display.shading.color_type = 'TEXTURE'
    bpy.context.scene.display.shading.show_cavity = True
    bpy.context.scene.display.shading.cavity_type = 'BOTH'
    bpy.context.scene.display.shading.cavity_ridge_factor = 2.5
    bpy.context.scene.display.shading.cavity_valley_factor = 1.5

    abs_out = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)
    bpy.context.scene.render.filepath = abs_out
    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]

    print(f"Bắt đầu render: {abs_out}")
    bpy.ops.render.render(write_still=True)
    print(f"Render hoàn tất: {os.path.exists(abs_out)}")

if __name__ == '__main__':
    render_texture_3d_check("docs/test_screenshots/_texture_3d_check.png")
    render_char_preview("Assets/Models/_char_preview.png")
