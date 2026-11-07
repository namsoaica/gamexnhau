"""
Script Blender 3D: Dựng Bản Đồ Làng Mở Rộng Liền Kề WorldMap (Village District)
Bản quyền: Trò Chơi Mới - Antigravity Pipeline
Dựa trên ảnh phác họa concept 'modelyeucau/map2/1.jpg'.
Tất cả vật thể được định nghĩa bằng tọa độ Godot (X: Đông/Tây, Y: Độ cao, Z: Nam/Bắc).
Được chuyển đổi chính xác sang hệ trục Blender để khi xuất glTF (Y-Up),
mô hình nằm phẳng trên mặt cỏ, liền kề hoàn hảo với Đảo Đá (Z in [0, 48]).
"""

import bpy
import math
from mathutils import Vector

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def godot_to_blender_pos(gx, gy, gz):
    """
    Chuyển đổi tọa độ từ Godot (X phải, Y lên, Z tới/nam)
    sang Blender (X phải, Y bắc, Z lên).
    glTF Y-Up: glTF.X = b.X, glTF.Y = b.Z, glTF.Z = -b.Y.
    """
    return (gx, -gz, gy)

def godot_to_blender_size(sx, sy, sz):
    """
    Chuyển đổi kích thước: sx (chiều ngang X), sy (chiều cao Y), sz (chiều sâu Z).
    Blender: X = sx, Y = sz, Z = sy.
    """
    return (sx, sz, sy)

def create_material(name, color, roughness=0.7, metallic=0.0, emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (300, 0)
    
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.location = (0, 0)
    node_bsdf.inputs['Base Color'].default_value = (color[0], color[1], color[2], 1.0)
    node_bsdf.inputs['Roughness'].default_value = roughness
    node_bsdf.inputs['Metallic'].default_value = metallic
    
    if emission_color and emission_strength > 0:
        if 'Emission Color' in node_bsdf.inputs:
            node_bsdf.inputs['Emission Color'].default_value = (emission_color[0], emission_color[1], emission_color[2], 1.0)
            node_bsdf.inputs['Emission Strength'].default_value = emission_strength
        elif 'Emission' in node_bsdf.inputs:
            node_bsdf.inputs['Emission'].default_value = (emission_color[0], emission_color[1], emission_color[2], 1.0)
            if 'Emission Strength' in node_bsdf.inputs:
                node_bsdf.inputs['Emission Strength'].default_value = emission_strength
                
    mat.node_tree.links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
    return mat

def create_box(name, size, location, rotation=(0, 0, 0), material=None):
    """
    Tạo khối hộp với size (sx, sy, sz) và location (gx, gy, gz) theo hệ tọa độ Godot.
    """
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    
    obj.scale = godot_to_blender_size(*size)
    obj.location = godot_to_blender_pos(*location)
    
    # Góc quay theo Godot: ry là quay quanh trục thẳng đứng Y (trong Blender là trục Z)
    obj.rotation_euler = (rotation[0], -rotation[2], rotation[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    if material:
        obj.data.materials.append(material)
    return obj

def create_cylinder(name, radius, depth, location, rotation=(0, 0, 0), vertices=12, material=None):
    """
    Tạo hình trụ thẳng đứng theo hệ tọa độ Godot (depth là chiều cao thẳng đứng Y).
    """
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=(0, 0, 0)
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.location = godot_to_blender_pos(*location)
    obj.rotation_euler = (rotation[0], -rotation[2], rotation[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    if material:
        obj.data.materials.append(material)
    return obj

def create_icosphere(name, radius, subdivisions, location, material=None):
    """
    Tạo khối cầu tròn icosphere tại vị trí (gx, gy, gz) theo hệ Godot.
    """
    b_pos = godot_to_blender_pos(*location)
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=subdivisions,
        radius=radius,
        location=b_pos
    )
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def build_roof_gabled(name, width, length, height, center_pos, ridge_along_x=True, material=None):
    """
    Tạo mái nhà dốc 2 mái (gabled roof) trong hệ tọa độ Godot.
    center_pos: (cx, cy, cz) với cy là mép chân mái (đỉnh tường).
    """
    cx, cy, cz = center_pos
    hw = width / 2.0
    hl = length / 2.0
    
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    if ridge_along_x:
        # Đường nóc chạy dọc trục X (mái dốc về Bắc và Nam)
        g_verts = [
            (-hw, 0.0, -hl),    # 0: Tây Bắc
            (hw, 0.0, -hl),     # 1: Đông Bắc
            (hw, 0.0, hl),      # 2: Đông Nam
            (-hw, 0.0, hl),     # 3: Tây Nam
            (-hw, height, 0.0), # 4: Đỉnh nóc Tây
            (hw, height, 0.0)   # 5: Đỉnh nóc Đông
        ]
        faces = [
            [0, 3, 4],       # Hồi Tây (Tam giác)
            [1, 5, 2],       # Hồi Đông (Tam giác)
            [0, 4, 5, 1],    # Mái Bắc
            [3, 2, 5, 4],    # Mái Nam
            [0, 1, 2, 3]     # Trần đáy
        ]
    else:
        # Đường nóc chạy dọc trục Z (mái dốc về Tây và Đông)
        g_verts = [
            (-hw, 0.0, -hl),    # 0: Tây Bắc
            (hw, 0.0, -hl),     # 1: Đông Bắc
            (hw, 0.0, hl),      # 2: Đông Nam
            (-hw, 0.0, hl),     # 3: Tây Nam
            (0.0, height, -hl), # 4: Đỉnh nóc Bắc
            (0.0, height, hl)   # 5: Đỉnh nóc Nam
        ]
        faces = [
            [0, 4, 1],       # Hồi Bắc (Tam giác)
            [3, 2, 5],       # Hồi Nam (Tam giác)
            [0, 3, 5, 4],    # Mái Tây
            [1, 4, 5, 2],    # Mái Đông
            [0, 1, 2, 3]     # Trần đáy
        ]
        
    b_verts = [Vector(godot_to_blender_pos(cx + vx, cy + vy, cz + vz)) for (vx, vy, vz) in g_verts]
    mesh.from_pydata(b_verts, [], faces)
    mesh.update()
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    if material:
        obj.data.materials.append(material)
    return obj

def build_tree(name, location, scale=1.0, mat_wood=None, mat_foliage=None):
    """
    Dựng cây bóng mát tán lá cách điệu tại vị trí Godot (gx, gy, gz).
    """
    gx, gy, gz = location
    trunk_h = 2.8 * scale
    trunk_r = 0.28 * scale
    create_cylinder(f"{name}_Trunk", trunk_r, trunk_h, (gx, gy + trunk_h / 2, gz), material=mat_wood)
    
    f1_r = 1.4 * scale
    f1_y = gy + trunk_h + 0.3 * scale
    create_icosphere(f"{name}_Foliage1", f1_r, 1, (gx, f1_y, gz), material=mat_foliage)
    
    f2_r = 1.0 * scale
    f2_y = f1_y + 0.8 * scale
    create_icosphere(f"{name}_Foliage2", f2_r, 1, (gx + 0.15 * scale, f2_y, gz - 0.15 * scale), material=mat_foliage)

def build_village():
    print("=== BẮT ĐẦU DỰNG BẢN ĐỒ LÀNG MỞ RỘNG LIỀN KỀ WORLDMAP ===")
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
    # Đoạn rẽ nhẹ từ chân dốc Đảo Đá vào trục chính
    create_box("Path_Connector_Island", (3.2, 0.04, 4.5), (4.0, 0.02, 2.5), material=mat_dirt)
    create_box("Path_Connector_Bend", (3.4, 0.04, 4.5), (2.0, 0.02, 6.0), material=mat_dirt)
    # Trục đại lộ Làng qua Cổng Làng tới Chợ
    create_box("Path_Village_Main_Gate", (3.6, 0.04, 8.0), (0.0, 0.02, 11.5), material=mat_dirt)
    create_box("Path_Village_Main_Avenue", (4.0, 0.04, 12.0), (0.0, 0.02, 20.0), material=mat_dirt)
    # Quảng trường Chợ Trung Tâm
    create_box("Path_Market_Square", (11.0, 0.04, 9.0), (0.0, 0.02, 29.5), material=mat_dirt)
    # Các nhánh đường tới các phân khu
    create_box("Path_To_Farm", (4.5, 0.04, 2.4), (-4.5, 0.02, 8.5), material=mat_dirt)
    create_box("Path_To_Chef", (4.5, 0.04, 2.4), (4.5, 0.02, 8.5), material=mat_dirt)
    create_box("Path_To_Smith", (6.5, 0.04, 3.0), (-6.0, 0.02, 21.0), material=mat_dirt)
    create_box("Path_To_Alchemist", (6.5, 0.04, 3.0), (6.0, 0.02, 21.0), material=mat_dirt)
    create_box("Path_To_House", (5.0, 0.04, 2.6), (-5.5, 0.02, 28.0), material=mat_dirt)
    create_box("Path_To_Lumber", (2.8, 0.04, 11.0), (-12.0, 0.02, 36.0), material=mat_dirt)
    create_box("Path_To_Mine", (2.8, 0.04, 11.0), (12.0, 0.02, 36.0), material=mat_dirt)

    # 3. CỔNG LÀNG & VƯỜN RAU CẢI (Z in [7, 10])
    gate_z = 8.5
    create_cylinder("Gate_Post_L", 0.24, 4.0, (-2.0, 2.0, gate_z), material=mat_wood)
    create_cylinder("Gate_Post_R", 0.24, 4.0, (2.0, 2.0, gate_z), material=mat_wood)
    create_box("Gate_Beam_Top", (4.6, 0.35, 0.35), (0.0, 3.8, gate_z), material=mat_wood)
    create_box("Gate_Signboard", (2.4, 0.7, 0.12), (0.0, 3.1, gate_z), material=mat_wood)

    # Hàng rào gỗ mộc hai bên cổng
    for side in [-1, 1]:
        for i in range(4):
            fx = side * (2.8 + i * 1.5)
            create_cylinder(f"Fence_Gate_{side}_{i}", 0.11, 1.3, (fx, 0.65, gate_z), material=mat_wood_fence)
            create_box(f"Fence_Rail_Top_{side}_{i}", (1.6, 0.08, 0.08), (fx - side * 0.75, 1.0, gate_z), material=mat_wood_fence)
            create_box(f"Fence_Rail_Bot_{side}_{i}", (1.6, 0.08, 0.08), (fx - side * 0.75, 0.5, gate_z), material=mat_wood_fence)

    # Vườn rau cải bắp (Tây: X in [-7, -3], Z in [7, 10])
    for row in range(3):
        rz = 7.5 + row * 1.1
        create_box(f"Crop_Soil_{row}", (4.2, 0.1, 0.8), (-5.2, 0.05, rz), material=mat_dirt)
        for col in range(4):
            cx = -6.5 + col * 0.9
            create_icosphere(f"Cabbage_{row}_{col}", 0.26, 1, (cx, 0.22, rz), material=mat_vegetable)

    # 4. QUÁN ĂN / TAVERN CỦA ĐẦU BẾP (ĐÔNG: X = 8.0, Z = 7.5)
    cf_cx, cf_cz = 8.0, 7.5
    cf_w, cf_l, cf_h = 5.8, 5.0, 3.0
    create_box("Floor_Chef", (cf_w, 0.15, cf_l), (cf_cx, 0.08, cf_cz), material=mat_stone)
    create_box("Wall_North_Chef", (cf_w, cf_h, 0.3), (cf_cx, cf_h/2, cf_cz - cf_l/2 + 0.15), material=mat_wall)
    create_box("Wall_South_Chef", (cf_w, cf_h, 0.3), (cf_cx, cf_h/2, cf_cz + cf_l/2 - 0.15), material=mat_wall)
    create_box("Wall_East_Chef", (0.3, cf_h, cf_l - 0.6), (cf_cx + cf_w/2 - 0.15, cf_h/2, cf_cz), material=mat_wall)
    # Tường trước phía Tây (cửa rộng 1.8m nhìn ra đường chính)
    create_box("Wall_Front_Chef_L", (0.3, cf_h, 1.6), (cf_cx - cf_w/2 + 0.15, cf_h/2, cf_cz - 1.4), material=mat_wall)
    create_box("Wall_Front_Chef_R", (0.3, cf_h, 1.6), (cf_cx - cf_w/2 + 0.15, cf_h/2, cf_cz + 1.4), material=mat_wall)
    create_box("Wall_Front_Chef_Top", (0.3, 0.7, 1.8), (cf_cx - cf_w/2 + 0.15, cf_h - 0.35, cf_cz), material=mat_wall)
    build_roof_gabled("Roof_Chef", cf_w + 0.6, cf_l + 0.6, 1.6, (cf_cx, cf_h, cf_cz), ridge_along_x=False, material=mat_roof_red)

    # Nội thất Quán Ăn: Lò nướng bánh gạch đá rực lửa & Bàn ăn dài
    create_box("Oven_Chef_Base", (1.4, 1.3, 1.2), (cf_cx + cf_w/2 - 1.0, 0.65, cf_cz - cf_l/2 + 1.0), material=mat_stone)
    create_box("Oven_Chef_Fire", (0.8, 0.45, 0.5), (cf_cx - cf_w/2 + 1.0, 0.4, cf_cz - cf_l/2 + 1.0), material=mat_lava_fire)
    create_box("Dining_Table_Chef", (1.2, 0.85, 2.6), (cf_cx, 0.42, cf_cz), material=mat_wood)
    create_box("Dining_Bench_Chef_L", (0.35, 0.45, 2.6), (cf_cx - 0.9, 0.22, cf_cz), material=mat_wood)
    create_box("Dining_Bench_Chef_R", (0.35, 0.45, 2.6), (cf_cx + 0.9, 0.22, cf_cz), material=mat_wood)

    # 5. CHỢ TRUNG TÂM (Z in [14, 20], X in [-4, 4])
    # Giếng nước đá tròn mái che ròng rọc
    well_x, well_z = -1.6, 16.5
    create_cylinder("Well_Stone", 1.25, 0.95, (well_x, 0.48, well_z), vertices=14, material=mat_stone)
    create_cylinder("Well_Water", 1.05, 0.12, (well_x, 0.70, well_z), material=mat_mystic_cyan)
    create_cylinder("Well_Post_1", 0.08, 2.4, (well_x - 1.0, 1.2, well_z), material=mat_wood)
    create_cylinder("Well_Post_2", 0.08, 2.4, (well_x + 1.0, 1.2, well_z), material=mat_wood)
    build_roof_gabled("Well_Roof", 2.4, 1.6, 0.7, (well_x, 2.2, well_z), ridge_along_x=True, material=mat_roof_red)

    # Sạp chợ 1 (Bạt vải sọc đỏ trắng)
    ms1_x, ms1_z = 2.8, 15.0
    create_box("Market_Stall_1_Table", (2.8, 0.85, 1.4), (ms1_x, 0.42, ms1_z), material=mat_wood)
    create_cylinder("Market_Stall_1_P1", 0.06, 2.4, (ms1_x - 1.3, 1.2, ms1_z - 0.6), material=mat_wood)
    create_cylinder("Market_Stall_1_P2", 0.06, 2.4, (ms1_x + 1.3, 1.2, ms1_z - 0.6), material=mat_wood)
    create_cylinder("Market_Stall_1_P3", 0.06, 2.4, (ms1_x - 1.3, 1.2, ms1_z + 0.6), material=mat_wood)
    create_cylinder("Market_Stall_1_P4", 0.06, 2.4, (ms1_x + 1.3, 1.2, ms1_z + 0.6), material=mat_wood)
    create_box("Market_Stall_1_Canopy", (3.2, 0.15, 1.8), (ms1_x, 2.3, ms1_z), material=mat_canopy_striped)

    # Sạp chợ 2
    ms2_x, ms2_z = 2.8, 18.5
    create_box("Market_Stall_2_Table", (2.8, 0.85, 1.4), (ms2_x, 0.42, ms2_z), material=mat_wood)
    create_cylinder("Market_Stall_2_P1", 0.06, 2.4, (ms2_x - 1.3, 1.2, ms2_z - 0.6), material=mat_wood)
    create_cylinder("Market_Stall_2_P2", 0.06, 2.4, (ms2_x + 1.3, 1.2, ms2_z - 0.6), material=mat_wood)
    create_cylinder("Market_Stall_2_P3", 0.06, 2.4, (ms2_x - 1.3, 1.2, ms2_z + 0.6), material=mat_wood)
    create_cylinder("Market_Stall_2_P4", 0.06, 2.4, (ms2_x + 1.3, 1.2, ms2_z + 0.6), material=mat_wood)
    create_box("Market_Stall_2_Canopy", (3.2, 0.15, 1.8), (ms2_x, 2.3, ms2_z), material=mat_canopy_striped)

    # Xe kéo hàng gỗ 2 bánh
    cart_x, cart_z = -2.6, 18.8
    create_box("Cart_Body", (1.6, 0.5, 1.8), (cart_x, 0.55, cart_z), material=mat_wood)
    create_cylinder("Cart_Wheel_L", 0.42, 0.12, (cart_x - 0.9, 0.42, cart_z), rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_cylinder("Cart_Wheel_R", 0.42, 0.12, (cart_x + 0.9, 0.42, cart_z), rotation=(0, 0, 1.57), material=mat_wood_fence)
    create_box("Cart_Crate_1", (0.6, 0.5, 0.6), (cart_x - 0.3, 0.9, cart_z), material=mat_wood)
    create_box("Cart_Crate_2", (0.5, 0.4, 0.5), (cart_x + 0.3, 0.85, cart_z), material=mat_wood)

    # 6. NHÀ RÈN CỦA VULCAN (TÂY: X = -11.0, Z = 21.0)
    sm_cx, sm_cz = -11.0, 21.0
    sm_w, sm_l, sm_h = 6.4, 5.6, 3.2
    create_box("Floor_Smith", (sm_w, 0.15, sm_l), (sm_cx, 0.08, sm_cz), material=mat_stone)
    create_box("Wall_North_Smith", (sm_w, sm_h, 0.3), (sm_cx, sm_h/2, sm_cz - sm_l/2 + 0.15), material=mat_wall)
    create_box("Wall_South_Smith", (sm_w, sm_h, 0.3), (sm_cx, sm_h/2, sm_cz + sm_l/2 - 0.15), material=mat_wall)
    create_box("Wall_West_Smith", (0.3, sm_h, sm_l - 0.6), (sm_cx - sm_w/2 + 0.15, sm_h/2, sm_cz), material=mat_wall)
    # Tường trước phía Đông (cửa mở ra chợ, rộng 1.8m)
    create_box("Wall_Front_Smith_L", (0.3, sm_h, 1.9), (sm_cx + sm_w/2 - 0.15, sm_h/2, sm_cz - 1.8), material=mat_wall)
    create_box("Wall_Front_Smith_R", (0.3, sm_h, 1.9), (sm_cx + sm_w/2 - 0.15, sm_h/2, sm_cz + 1.8), material=mat_wall)
    create_box("Wall_Front_Smith_Top", (0.3, 0.8, 1.8), (sm_cx + sm_w/2 - 0.15, sm_h - 0.4, sm_cz), material=mat_wall)
    build_roof_gabled("Roof_Smith", sm_w + 0.6, sm_l + 0.6, 1.8, (sm_cx, sm_h, sm_cz), ridge_along_x=False, material=mat_roof_red)

    # Ống khói đá lớn
    create_box("Chimney_Smith_Base", (1.2, 5.2, 1.2), (sm_cx - sm_w/2 + 0.7, 2.6, sm_cz - sm_l/2 + 0.7), material=mat_stone)
    # Lò rèn than hồng trong nhà
    create_box("Forge_Indoor_Base", (1.5, 0.9, 1.3), (sm_cx - 1.6, 0.45, sm_cz - 1.4), material=mat_stone)
    create_box("Forge_Indoor_Fire", (1.1, 0.25, 0.9), (sm_cx - 1.6, 0.95, sm_cz - 1.4), material=mat_lava_fire)
    # Đe sắt trong nhà
    create_cylinder("Anvil_Indoor_Log", 0.45, 0.7, (sm_cx, 0.35, sm_cz), material=mat_wood)
    create_box("Anvil_Indoor_Iron", (0.5, 0.3, 0.8), (sm_cx, 0.8, sm_cz), material=mat_metal)

    # Sân rèn ngoài trời (Vulcan làm việc ngoài trời)
    out_x, out_z = -6.8, 20.0
    create_cylinder("Anvil_Outdoor_Log", 0.45, 0.7, (out_x, 0.35, out_z), material=mat_wood)
    create_box("Anvil_Outdoor_Iron", (0.55, 0.35, 0.9), (out_x, 0.82, out_z), material=mat_metal)
    create_box("Forge_Outdoor_Base", (1.4, 0.9, 1.2), (out_x - 1.2, 0.45, out_z - 1.4), material=mat_stone)
    create_box("Forge_Outdoor_Fire", (1.0, 0.2, 0.8), (out_x - 1.2, 0.95, out_z - 1.4), material=mat_lava_fire)

    # 7. NHÀ GIẢ KIM CỦA ARIA (ĐÔNG: X = 11.0, Z = 21.0)
    al_cx, al_cz = 11.0, 21.0
    al_w, al_l, al_h = 6.4, 5.6, 3.2
    create_box("Floor_Alchemist", (al_w, 0.15, al_l), (al_cx, 0.08, al_cz), material=mat_stone)
    create_box("Wall_North_Alchemist", (al_w, al_h, 0.3), (al_cx, al_h/2, al_cz - al_l/2 + 0.15), material=mat_wall)
    create_box("Wall_South_Alchemist", (al_w, al_h, 0.3), (al_cx, al_h/2, al_cz + al_l/2 - 0.15), material=mat_wall)
    create_box("Wall_East_Alchemist", (0.3, al_h, al_l - 0.6), (al_cx + al_w/2 - 0.15, al_h/2, al_cz), material=mat_wall)
    # Tường trước phía Tây (cửa mở ra chợ, rộng 1.8m)
    create_box("Wall_Front_Alchemist_L", (0.3, al_h, 1.9), (al_cx - al_w/2 + 0.15, al_h/2, al_cz - 1.8), material=mat_wall)
    create_box("Wall_Front_Alchemist_R", (0.3, al_h, 1.9), (al_cx - al_w/2 + 0.15, al_h/2, al_cz + 1.8), material=mat_wall)
    create_box("Wall_Front_Alchemist_Top", (0.3, 0.8, 1.8), (al_cx - al_w/2 + 0.15, al_h - 0.4, al_cz), material=mat_wall)
    build_roof_gabled("Roof_Alchemist", al_w + 0.6, al_l + 0.6, 1.8, (al_cx, al_h, al_cz), ridge_along_x=False, material=mat_roof_teal)

    # Ống khói ma thuật & làn khói xanh huyền ảo
    create_cylinder("Chimney_Alchemist", 0.38, 4.8, (al_cx + al_w/2 - 0.8, 2.4, al_cz - al_l/2 + 0.8), material=mat_stone)
    create_icosphere("Smoke_Alchemist_1", 0.5, 1, (al_cx + al_w/2 - 0.8, 5.1, al_cz - al_l/2 + 0.8), material=mat_mystic_cyan)
    create_icosphere("Smoke_Alchemist_2", 0.7, 1, (al_cx + al_w/2 - 0.6, 5.8, al_cz - al_l/2 + 0.6), material=mat_mystic_cyan)

    # Nội thất Nhà Giả Kim
    create_cylinder("Cauldron_Base", 0.75, 0.75, (al_cx, 0.38, al_cz), material=mat_metal)
    create_cylinder("Cauldron_Potion", 0.65, 0.1, (al_cx, 0.72, al_cz), material=mat_mystic_cyan)
    create_box("Bookshelf_Alchemist", (3.8, 2.4, 0.5), (al_cx, 1.2, al_cz - al_l/2 + 0.4), material=mat_wood_fence)
    create_box("Potion_Table", (0.8, 0.85, 2.6), (al_cx + al_w/2 - 0.6, 0.42, al_cz), material=mat_wood)

    # Bồn thảo dược bên hiên nhà
    create_box("Herb_Bed_1", (1.2, 0.35, 3.2), (al_cx - al_w/2 - 0.8, 0.18, al_cz + 1.2), material=mat_wood_fence)
    create_box("Herb_Soil_1", (1.0, 0.10, 3.0), (al_cx - al_w/2 - 0.8, 0.36, al_cz + 1.2), material=mat_vegetable)

    # 8. NHÀ DÂN (TÂY: X = -10.0, Z = 28.5)
    hs_cx, hs_cz = -10.0, 28.5
    hs_w, hs_l, hs_h = 5.8, 5.0, 3.0
    create_box("Floor_House", (hs_w, 0.15, hs_l), (hs_cx, 0.08, hs_cz), material=mat_stone)
    create_box("Wall_North_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz - hs_l/2 + 0.15), material=mat_wall)
    create_box("Wall_South_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz + hs_l/2 - 0.15), material=mat_wall)
    create_box("Wall_West_House", (0.3, hs_h, hs_l - 0.6), (hs_cx - hs_w/2 + 0.15, hs_h/2, hs_cz), material=mat_wall)
    # Tường trước phía Đông (cửa rộng 1.8m)
    create_box("Wall_Front_House_L", (0.3, hs_h, 1.6), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz - 1.4), material=mat_wall)
    create_box("Wall_Front_House_R", (0.3, hs_h, 1.6), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz + 1.4), material=mat_wall)
    create_box("Wall_Front_House_Top", (0.3, 0.7, 1.8), (hs_cx + hs_w/2 - 0.15, hs_h - 0.35, hs_cz), material=mat_wall)
    build_roof_gabled("Roof_House", hs_w + 0.6, hs_l + 0.6, 1.6, (hs_cx, hs_h, hs_cz), ridge_along_x=False, material=mat_roof_red)

    # Nội thất Nhà Dân: Giường ngủ, tủ áo, thảm trải sàn
    create_box("Bed_Frame", (1.6, 0.45, 2.2), (hs_cx - hs_w/2 + 1.1, 0.22, hs_cz - hs_l/2 + 1.4), material=mat_wood)
    create_box("Bed_Mattress", (1.4, 0.25, 2.0), (hs_cx - hs_w/2 + 1.1, 0.50, hs_cz - hs_l/2 + 1.4), material=mat_roof_red)
    create_box("Wardrobe", (1.2, 2.1, 0.6), (hs_cx - hs_w/2 + 0.8, 1.05, hs_cz + hs_l/2 - 0.6), material=mat_wood_fence)
    create_box("House_Rug", (1.8, 0.02, 1.8), (hs_cx + 0.5, 0.09, hs_cz), material=mat_canopy_striped)

    # 9. KHU LÂM NGHIỆP CỦA GROVER (TÂY BẮC: X = -14.0, Z = 38.0)
    lm_cx, lm_cz = -14.0, 38.0
    # Lán cưa xẻ gỗ
    create_cylinder("Lumber_P1", 0.18, 3.2, (lm_cx - 2.5, 1.6, lm_cz - 2.0), material=mat_wood)
    create_cylinder("Lumber_P2", 0.18, 3.2, (lm_cx + 2.5, 1.6, lm_cz - 2.0), material=mat_wood)
    create_cylinder("Lumber_P3", 0.18, 3.2, (lm_cx - 2.5, 1.6, lm_cz + 2.0), material=mat_wood)
    create_cylinder("Lumber_P4", 0.18, 3.2, (lm_cx + 2.5, 1.6, lm_cz + 2.0), material=mat_wood)
    build_roof_gabled("Lumber_Shed_Roof", 5.8, 4.8, 1.0, (lm_cx, 3.2, lm_cz), ridge_along_x=True, material=mat_wood_fence)
    # Bàn cưa gỗ & lưỡi cưa thép tròn
    create_box("Lumber_Saw_Table", (3.2, 0.85, 1.4), (lm_cx, 0.42, lm_cz), material=mat_wood)
    create_cylinder("Lumber_Saw_Blade", 0.45, 0.04, (lm_cx, 0.95, lm_cz), rotation=(1.57, 0, 0), material=mat_metal)
    # Các đống thân cây gỗ tròn nằm ngang
    for i in range(3):
        create_cylinder(f"Log_Pile_Bot_{i}", 0.32, 4.0, (lm_cx + 4.0, 0.32, lm_cz - 1.2 + i * 0.75), rotation=(1.57, 0, 0), material=mat_wood)
    for i in range(2):
        create_cylinder(f"Log_Pile_Top_{i}", 0.30, 4.0, (lm_cx + 4.0, 0.85, lm_cz - 0.85 + i * 0.75), rotation=(1.57, 0, 0), material=mat_wood)
    # Cây rừng bao quanh
    build_tree("Tree_Lumber_1", (lm_cx - 4.5, 0, lm_cz - 3.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_tree("Tree_Lumber_2", (lm_cx - 4.0, 0, lm_cz + 3.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_tree("Tree_Lumber_3", (lm_cx, 0, lm_cz + 4.5), scale=1.4, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # 10. KHU MỎ ĐÁ CỦA BROCK (ĐÔNG BẮC: X = 14.0, Z = 38.0)
    mn_cx, mn_cz = 14.0, 38.0
    # Vách núi đá hùng vĩ
    create_box("Mine_Cliff_Main", (13.0, 7.5, 8.0), (mn_cx, 3.75, mn_cz + 3.0), material=mat_stone)
    create_box("Mine_Cliff_Ledge", (6.5, 5.0, 4.0), (mn_cx - 4.5, 2.5, mn_cz + 0.5), material=mat_stone)
    # Cửa vòm hầm mỏ
    create_box("Mine_Entrance_Void", (2.8, 3.2, 1.2), (mn_cx, 1.6, mn_cz - 0.9), material=mat_stone)
    create_box("Mine_Beam_L", (0.35, 3.4, 0.4), (mn_cx - 1.5, 1.7, mn_cz - 0.9), material=mat_wood_fence)
    create_box("Mine_Beam_R", (0.35, 3.4, 0.4), (mn_cx + 1.5, 1.7, mn_cz - 0.9), material=mat_wood_fence)
    create_box("Mine_Beam_Top", (3.6, 0.35, 0.4), (mn_cx, 3.2, mn_cz - 0.9), material=mat_wood_fence)
    # Lò luyện quặng vòm rực lửa
    create_cylinder("Ore_Furnace", 1.3, 2.6, (mn_cx - 4.2, 1.3, mn_cz - 2.5), vertices=12, material=mat_stone)
    create_box("Ore_Furnace_Fire", (0.8, 0.6, 0.5), (mn_cx - 4.2, 0.6, mn_cz - 1.8), material=mat_lava_fire)
    # Đường ray xe goòng
    create_box("Rail_L", (0.08, 0.08, 4.5), (mn_cx + 2.0, 0.06, mn_cz - 1.0), material=mat_metal)
    create_box("Rail_R", (0.08, 0.08, 4.5), (mn_cx + 2.8, 0.06, mn_cz - 1.0), material=mat_metal)
    # Xe goòng chở quặng
    create_box("Minecart_Body", (1.2, 0.65, 1.6), (mn_cx + 2.4, 0.58, mn_cz - 1.5), material=mat_metal)
    create_box("Minecart_Ore", (0.9, 0.3, 1.3), (mn_cx + 2.4, 0.88, mn_cz - 1.5), material=mat_stone)

    # 11. CÂY CỐI TRANG TRÍ BAO QUANH LÀNG (TẠO KHÔNG GIAN SỐNG ĐỘNG)
    build_tree("Tree_Gate_L", (-5.0, 0, 5.0), scale=1.1, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_tree("Tree_Gate_R", (5.5, 0, 4.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_tree("Tree_Smith_Back", (-16.0, 0, 21.0), scale=1.4, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_tree("Tree_Alchemist_Back", (16.0, 0, 21.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_tree("Tree_House_South", (-12.0, 0, 32.0), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_tree("Tree_Mine_East", (18.5, 0, 35.0), scale=1.5, mat_wood=mat_wood, mat_foliage=mat_foliage)

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
    print("=== DỰNG BẢN ĐỒ LÀNG MỞ RỘNG LIỀN KỀ HOÀN TẤT ===")

if __name__ == '__main__':
    build_village()
