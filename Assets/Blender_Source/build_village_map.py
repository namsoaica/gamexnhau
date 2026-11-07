"""
Script Blender 3D: Dựng Bản Đồ Làng Mở Rộng & Nội Thất (Village Map & Interiors)
Dựa trên ảnh concept 'modelyeucau/map2/1.jpg'.
Chuẩn hóa cho Godot 4 (.NET 8):
- Tách riêng mái (Roof_*) và tường mặt trước (Wall_Front_*) cho 4 căn nhà để hỗ trợ Seamless Interior Transition.
- Tạo mesh va chạm tự động với hậu tố '-col'.
- Tạo các Material Slot chuẩn hóa để Godot ánh xạ sang Assets/Materials_Shared/*.tres.
- Xuất sang Assets/Models/village_map.glb.
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

def clean_scene():
    """Xóa toàn bộ object cũ trong scene để dựng mới sạch sẽ."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def create_material(name, color, roughness=0.7, metallic=0.0, emission_color=None, emission_strength=0.0):
    """Tạo vật liệu Principled BSDF với các thuộc tính màu sắc và emission."""
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
    
    # Thiết lập thuộc tính cho Blender 4.x / 5.x
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

def create_box(name, size, location, rotation=(0, 0, 0), material=None, add_collider=False):
    """Tạo hộp chữ nhật (Box) với kích thước và vị trí xác định."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0], size[1], size[2])
    obj.rotation_euler = rotation
    obj.location = (location[0], location[1], location[2])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    if material:
        obj.data.materials.append(material)
        
    if add_collider:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
        col = bpy.context.active_object
        col.name = f"{name}-col"
        col.scale = (size[0], size[1], size[2])
        col.rotation_euler = rotation
        col.location = (location[0], location[1], location[2])
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        col.display_type = 'WIRE'
        
    return obj

def create_cylinder(name, radius, depth, location, rotation=(0, 0, 0), vertices=12, material=None, add_collider=False):
    """Tạo hình trụ tròn (Cylinder)."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation
    )
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    if material:
        obj.data.materials.append(material)
        
    if add_collider:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=max(6, vertices // 2),
            radius=radius,
            depth=depth,
            location=location,
            rotation=rotation
        )
        col = bpy.context.active_object
        col.name = f"{name}-col"
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        col.display_type = 'WIRE'
        
    return obj

def create_icosphere(name, radius, subdivisions, location, material=None, add_collider=False):
    """Tạo hình cầu đa giác IcoSphere Stylized."""
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=subdivisions,
        radius=radius,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    
    if material:
        obj.data.materials.append(material)
        
    if add_collider:
        bpy.ops.mesh.primitive_cube_add(
            size=radius * 1.6,
            location=location
        )
        col = bpy.context.active_object
        col.name = f"{name}-col"
        col.display_type = 'WIRE'
        
    return obj

def build_tree(name, location, scale=1.0, mat_wood=None, mat_foliage=None):
    """Tạo một cây rừng/làng gồm thân gỗ và 2 tầng tán lá cách điệu."""
    x, y, z = location
    # Thân cây
    trunk_h = 2.4 * scale
    trunk_r = 0.25 * scale
    create_cylinder(f"{name}_Trunk", trunk_r, trunk_h, (x, y + trunk_h / 2, z), material=mat_wood, add_collider=True)
    
    # Tán lá tầng 1
    f1_r = 1.3 * scale
    f1_y = y + trunk_h + 0.3 * scale
    create_icosphere(f"{name}_Foliage1", f1_r, 1, (x, f1_y, z), material=mat_foliage)
    
    # Tán lá tầng 2 (trên chóp)
    f2_r = 0.9 * scale
    f2_y = f1_y + 0.8 * scale
    create_icosphere(f"{name}_Foliage2", f2_r, 1, (x + 0.1 * scale, f2_y, z - 0.1 * scale), material=mat_foliage)

def build_roof_gabled(name, width, length, height, center_pos, material=None):
    """Tạo mái nhà 2 dốc nhọn (Gabled Roof) riêng biệt để fade out."""
    cx, cy, cz = center_pos
    hw = width / 2.0
    hl = length / 2.0
    
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    # 6 đỉnh của lăng trụ mái nhà
    verts = [
        Vector((-hw, 0, -hl)),   # 0: Đáy trước trái
        Vector((hw, 0, -hl)),    # 1: Đáy trước phải
        Vector((hw, 0, hl)),     # 2: Đáy sau phải
        Vector((-hw, 0, hl)),    # 3: Đáy sau trái
        Vector((0, height, -hl)), # 4: Chóp trước
        Vector((0, height, hl))   # 5: Chóp sau
    ]
    
    faces = [
        [0, 1, 4],       # Tam giác hồi trước
        [2, 3, 5],       # Tam giác hồi sau
        [0, 4, 5, 3],    # Mái dốc trái
        [1, 2, 5, 4],    # Mái dốc phải
        [3, 2, 1, 0]     # Đáy trần nhà
    ]
    
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    obj.location = (cx, cy, cz)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    if material:
        obj.data.materials.append(material)
        
    return obj

def build_village():
    print("=== BẮT ĐẦU DỰNG BẢN ĐỒ LÀNG MỞ RỘNG (VILLAGE MAP & INTERIORS) ===")
    clean_scene()
    
    # 1. KHỞI TẠO BẢNG VẬT LIỆU DÙNG CHUNG
    mat_grass = create_material("Mat_Grass", (0.32, 0.60, 0.20), roughness=0.85)
    mat_dirt = create_material("Mat_Dirt", (0.54, 0.36, 0.21), roughness=0.90)
    mat_stone = create_material("Mat_Stone", (0.48, 0.50, 0.52), roughness=0.80)
    mat_wood = create_material("Mat_Wood", (0.55, 0.35, 0.21), roughness=0.75)
    mat_wood_dark = create_material("Mat_Wood_Dark", (0.34, 0.20, 0.12), roughness=0.80)
    mat_metal = create_material("Mat_Metal", (0.61, 0.64, 0.68), roughness=0.35, metallic=0.85)
    mat_darkiron = create_material("Mat_DarkIron", (0.18, 0.20, 0.22), roughness=0.40, metallic=0.90)
    mat_roof_red = create_material("Mat_Roof_Red", (0.78, 0.28, 0.22), roughness=0.80)
    mat_roof_teal = create_material("Mat_Roof_Teal", (0.18, 0.55, 0.52), roughness=0.80)
    mat_canopy_striped = create_material("Mat_Canopy_Striped", (0.85, 0.25, 0.20), roughness=0.85)
    mat_mystic_cyan = create_material("Mat_Mystic_Cyan", (0.20, 0.85, 0.80), roughness=0.20, emission_color=(0.20, 0.85, 0.80), emission_strength=2.0)
    mat_lava_fire = create_material("Mat_Lava_Fire", (1.00, 0.45, 0.05), roughness=0.40, emission_color=(1.00, 0.45, 0.05), emission_strength=2.5)
    mat_foliage = create_material("Mat_Foliage", (0.24, 0.56, 0.25), roughness=0.85)
    mat_vegetable = create_material("Mat_Vegetable", (0.37, 0.73, 0.29), roughness=0.80)
    mat_cloth = create_material("Mat_Cloth_White", (0.90, 0.87, 0.79), roughness=0.90)

    # 2. ĐỊA HÌNH NỀN LÀNG (TERRAIN: 48m x 48m)
    # Nền đất cỏ chính
    terrain = create_box("Terrain_Village", (48.0, 0.8, 48.0), (0.0, -0.4, 0.0), material=mat_grass, add_collider=True)
    
    # Mạng lưới đường mòn đất (Dirt Paths) nổi nhẹ 0.02m trên cỏ
    # Trục chính Nam -> Bắc (từ Cổng làng lên Chợ)
    create_box("Path_Main_South", (3.2, 0.04, 18.0), (0.0, 0.02, 10.0), material=mat_dirt)
    # Quảng trường Chợ trung tâm
    create_box("Path_Market_Square", (12.0, 0.04, 10.0), (0.0, 0.02, 0.0), material=mat_dirt)
    # Lối mòn sang Nhà Rèn (Tây)
    create_box("Path_To_Smith", (8.0, 0.04, 2.6), (-6.0, 0.02, -1.0), material=mat_dirt)
    # Lối mòn lên Khu Lâm Nghiệp (Tây Bắc)
    create_box("Path_To_Lumber", (2.6, 0.04, 10.0), (-10.5, 0.02, -8.0), material=mat_dirt)
    # Lối mòn sang Nhà Giả Kim (Đông)
    create_box("Path_To_Alchemist", (8.0, 0.04, 2.6), (6.0, 0.02, -2.0), material=mat_dirt)
    # Lối mòn lên Khu Mỏ Đá (Đông Bắc)
    create_box("Path_To_Mine", (2.8, 0.04, 12.0), (10.0, 0.02, -10.0), material=mat_dirt)
    # Lối rẽ vào Quán Ăn (Đông Nam)
    create_box("Path_To_Chef", (5.0, 0.04, 2.4), (7.0, 0.02, 10.5), material=mat_dirt)
    # Lối rẽ vào Nhà Dân (Tây Nam)
    create_box("Path_To_House", (5.0, 0.04, 2.4), (-4.5, 0.02, 11.5), material=mat_dirt)

    # 3. KHU LÂM NGHIỆP (TÂY BẮC: X: -16 đến -8, Z: -18 đến -10)
    # Lán cưa xẻ gỗ mộc (Lumber Shed)
    ls_x, ls_z = -12.0, -14.0
    # 4 cột gỗ
    col_h = 3.0
    create_cylinder("Lumber_Col1", 0.16, col_h, (ls_x - 2.5, col_h/2, ls_z - 2.0), material=mat_wood, add_collider=True)
    create_cylinder("Lumber_Col2", 0.16, col_h, (ls_x + 2.5, col_h/2, ls_z - 2.0), material=mat_wood, add_collider=True)
    create_cylinder("Lumber_Col3", 0.16, col_h, (ls_x - 2.5, col_h/2, ls_z + 2.0), material=mat_wood, add_collider=True)
    create_cylinder("Lumber_Col4", 0.16, col_h, (ls_x + 2.5, col_h/2, ls_z + 2.0), material=mat_wood, add_collider=True)
    # Mái lán gỗ dốc 1 chiều
    create_box("Lumber_Shed_Roof", (5.6, 0.15, 4.6), (ls_x, col_h + 0.1, ls_z), material=mat_wood_dark)
    # Bàn xẻ gỗ dài
    create_box("Lumber_Saw_Table", (3.2, 0.8, 1.2), (ls_x, 0.4, ls_z), material=mat_wood, add_collider=True)
    # Lưỡi cưa kim loại tròn lớn
    create_cylinder("Lumber_Saw_Blade", 0.6, 0.04, (ls_x, 0.95, ls_z), rotation=(1.57, 0, 0), material=mat_metal)
    # Đống thân gỗ tròn nằm ngang (Lumber Logs Pile)
    log_z_start = ls_z + 4.5
    for row in range(3):
        num_logs = 3 - row
        for i in range(num_logs):
            lx = ls_x - 1.2 + i * 0.9 + row * 0.45
            ly = 0.35 + row * 0.6
            create_cylinder(f"Lumber_Log_{row}_{i}", 0.32, 4.0, (lx, ly, log_z_start), rotation=(1.57, 0, 0), material=mat_wood, add_collider=(row==0))
    # Rừng cây bao quanh góc Tây Bắc
    tree_coords = [
        (-18.0, -12.0), (-20.0, -16.0), (-16.0, -20.0), (-21.0, -21.0),
        (-11.0, -21.0), (-7.0, -19.0), (-21.0, -7.0), (-18.0, -4.0)
    ]
    for idx, (tx, tz) in enumerate(tree_coords):
        build_tree(f"ForestTree_{idx}", (tx, 0.0, tz), scale=1.1, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # 4. NHÀ RÈN (TRUNG TÂY: X: -14 đến -6, Z: -5 đến 1)
    sm_cx, sm_cz = -10.0, -2.0
    sm_w, sm_l, sm_h = 7.0, 6.0, 3.2
    
    # Nền móng nhà rèn
    create_box("Floor_Smith", (sm_w, 0.2, sm_l), (sm_cx, 0.1, sm_cz), material=mat_stone, add_collider=True)
    
    # Tường cố định (Tường Bắc, Tường Tây, Tường Đông)
    # Tường Bắc (sau)
    create_box("Wall_North_Smith", (sm_w, sm_h, 0.4), (sm_cx, sm_h/2, sm_cz - sm_l/2 + 0.2), material=mat_stone, add_collider=True)
    # Tường Tây (trái)
    create_box("Wall_West_Smith", (0.4, sm_h, sm_l - 0.8), (sm_cx - sm_w/2 + 0.2, sm_h/2, sm_cz), material=mat_stone, add_collider=True)
    # Tường Đông (phải)
    create_box("Wall_East_Smith", (0.4, sm_h, sm_l - 0.8), (sm_cx + sm_w/2 - 0.2, sm_h/2, sm_cz), material=mat_stone, add_collider=True)
    
    # Tường mặt trước (Nam) CÓ THỂ ẨN ĐI: Wall_Front_Smith (chia làm 2 cánh chừa cửa giữa rộng 1.6m)
    # Cánh trái
    create_box("Wall_Front_Smith_L", (2.7, sm_h, 0.4), (sm_cx - 2.15, sm_h/2, sm_cz + sm_l/2 - 0.2), material=mat_stone, add_collider=True)
    # Cánh phải
    create_box("Wall_Front_Smith_R", (2.7, sm_h, 0.4), (sm_cx + 2.15, sm_h/2, sm_cz + sm_l/2 - 0.2), material=mat_stone, add_collider=True)
    # Đà ngang phía trên cửa
    create_box("Wall_Front_Smith_Top", (1.6, 0.8, 0.4), (sm_cx, sm_h - 0.4, sm_cz + sm_l/2 - 0.2), material=mat_stone, add_collider=True)
    
    # Mái nhà ngói đỏ CÓ THỂ ẨN ĐI: Roof_Smith
    build_roof_gabled("Roof_Smith", sm_w + 0.8, sm_l + 0.8, 2.0, (sm_cx, sm_h, sm_cz), material=mat_roof_red)
    
    # Ống khói đá lớn ngoài nhà vươn cao
    create_box("Chimney_Smith", (1.2, 5.6, 1.2), (sm_cx - sm_w/2 + 0.6, 2.8, sm_cz - sm_l/2 + 0.6), material=mat_stone, add_collider=True)
    
    # Ngoại thất Nhà Rèn (Sân rèn ngoài trời):
    # Lò rèn ngoài trời rực lửa
    create_box("Forge_Outdoor_Base", (1.8, 1.0, 1.8), (sm_cx + 4.5, 0.5, sm_cz + 2.0), material=mat_stone, add_collider=True)
    create_box("Forge_Outdoor_Fire", (1.2, 0.3, 1.2), (sm_cx + 4.5, 1.05, sm_cz + 2.0), material=mat_lava_fire)
    # Đe sắt ngoài trời
    create_cylinder("Anvil_Outdoor_Stump", 0.45, 0.7, (sm_cx + 3.0, 0.35, sm_cz + 3.2), material=mat_wood, add_collider=True)
    create_box("Anvil_Outdoor_Iron", (0.5, 0.35, 0.8), (sm_cx + 3.0, 0.85, sm_cz + 3.2), material=mat_darkiron)
    # Đống than đen vụn
    create_box("Coal_Pile_Outdoor", (1.4, 0.35, 1.4), (sm_cx + 1.2, 0.17, sm_cz + 4.0), material=mat_darkiron)
    # Giá búa đập sắt
    create_box("Hammer_Rack", (1.6, 1.2, 0.3), (sm_cx - 1.0, 0.6, sm_cz + 3.8), material=mat_wood, add_collider=True)
    
    # Nội thất bên trong Nhà Rèn:
    # Lò rèn trong nhà ăn vào tường Bắc
    create_box("Forge_Interior_Base", (2.2, 1.4, 1.2), (sm_cx, 0.7, sm_cz - 2.2), material=mat_stone, add_collider=True)
    create_box("Forge_Interior_Fire", (1.4, 0.5, 0.6), (sm_cx, 0.8, sm_cz - 2.0), material=mat_lava_fire)
    # Đe sắt trong nhà
    create_cylinder("Anvil_Interior_Stump", 0.4, 0.7, (sm_cx, 0.35, sm_cz), material=mat_wood, add_collider=True)
    create_box("Anvil_Interior_Iron", (0.45, 0.3, 0.7), (sm_cx, 0.82, sm_cz), material=mat_darkiron)
    # Rương sắt vụn góc Tây Bắc
    create_box("Chest_Scrap_Metal", (1.2, 0.6, 0.8), (sm_cx - 2.5, 0.3, sm_cz - 2.0), material=mat_wood_dark, add_collider=True)
    # Rương than củi góc Đông Bắc
    create_box("Chest_Coal", (1.2, 0.6, 0.8), (sm_cx + 2.5, 0.3, sm_cz - 2.0), material=mat_wood_dark, add_collider=True)
    # Bể nước tôi kim loại góc Tây Nam
    create_box("Quench_Tank", (1.2, 0.8, 1.0), (sm_cx - 2.5, 0.4, sm_cz + 1.8), material=mat_wood, add_collider=True)
    create_box("Quench_Water", (1.0, 0.1, 0.8), (sm_cx - 2.5, 0.75, sm_cz + 1.8), material=mat_mystic_cyan)
    # Giá treo vũ khí trên vách Tây
    create_box("Weapon_Rack_Wall", (0.2, 1.6, 2.0), (sm_cx - sm_w/2 + 0.3, 1.8, sm_cz), material=mat_wood)

    # 5. CHỢ TRUNG TÂM (GIỮA: X: -5 đến 5, Z: -4 đến 6)
    # Giếng nước đá tròn cổ kính ở giữa chợ
    well_x, well_z = -1.5, 3.5
    create_cylinder("Well_Stone", 1.2, 0.9, (well_x, 0.45, well_z), material=mat_stone, add_collider=True)
    create_cylinder("Well_Water", 0.95, 0.1, (well_x, 0.75, well_z), material=mat_mystic_cyan)
    # 2 cột đỡ mái giếng
    create_cylinder("Well_Post_L", 0.1, 2.2, (well_x - 1.0, 1.1, well_z), material=mat_wood)
    create_cylinder("Well_Post_R", 0.1, 2.2, (well_x + 1.0, 1.1, well_z), material=mat_wood)
    create_box("Well_Roof", (2.4, 0.15, 1.6), (well_x, 2.2, well_z), material=mat_roof_red)
    
    # Quầy sạp bạt sọc đỏ-trắng 1 (Phía Bắc chợ)
    ms1_x, ms1_z = -1.0, -1.8
    create_box("Market_Stall_1_Table", (3.0, 0.85, 1.4), (ms1_x, 0.42, ms1_z), material=mat_wood, add_collider=True)
    create_box("Market_Stall_1_Canopy", (3.4, 0.15, 1.8), (ms1_x, 2.2, ms1_z), material=mat_canopy_striped)
    # 4 cọc lều sạp
    create_cylinder("Stall1_Post1", 0.08, 2.2, (ms1_x - 1.5, 1.1, ms1_z - 0.7), material=mat_wood)
    create_cylinder("Stall1_Post2", 0.08, 2.2, (ms1_x + 1.5, 1.1, ms1_z - 0.7), material=mat_wood)
    create_cylinder("Stall1_Post3", 0.08, 2.2, (ms1_x - 1.5, 1.1, ms1_z + 0.7), material=mat_wood)
    create_cylinder("Stall1_Post4", 0.08, 2.2, (ms1_x + 1.5, 1.1, ms1_z + 0.7), material=mat_wood)
    
    # Quầy sạp hàng 2 (Phía Đông chợ)
    ms2_x, ms2_z = 3.5, 0.5
    create_box("Market_Stall_2_Table", (1.4, 0.85, 2.8), (ms2_x, 0.42, ms2_z), material=mat_wood, add_collider=True)
    create_box("Market_Stall_2_Canopy", (1.8, 0.15, 3.2), (ms2_x, 2.2, ms2_z), material=mat_canopy_striped)
    create_cylinder("Stall2_Post1", 0.08, 2.2, (ms2_x - 0.7, 1.1, ms2_z - 1.4), material=mat_wood)
    create_cylinder("Stall2_Post2", 0.08, 2.2, (ms2_x + 0.7, 1.1, ms2_z - 1.4), material=mat_wood)
    create_cylinder("Stall2_Post3", 0.08, 2.2, (ms2_x - 0.7, 1.1, ms2_z + 1.4), material=mat_wood)
    create_cylinder("Stall2_Post4", 0.08, 2.2, (ms2_x + 0.7, 1.1, ms2_z + 1.4), material=mat_wood)
    
    # Xe kéo hàng gỗ 2 bánh (Wooden Cart)
    cart_x, cart_z = 2.5, 4.0
    create_box("Cart_Body", (1.8, 0.6, 2.6), (cart_x, 0.7, cart_z), material=mat_wood, add_collider=True)
    create_cylinder("Cart_Wheel_L", 0.5, 0.12, (cart_x - 1.0, 0.5, cart_z), rotation=(0, 0, 1.57), material=mat_wood_dark)
    create_cylinder("Cart_Wheel_R", 0.5, 0.12, (cart_x + 1.0, 0.5, cart_z), rotation=(0, 0, 1.57), material=mat_wood_dark)
    # Hàng hóa trên xe: Thùng gỗ và bao tải
    create_cylinder("Cart_Barrel", 0.35, 0.7, (cart_x - 0.3, 1.25, cart_z - 0.5), material=mat_wood)
    create_box("Cart_Sack", (0.6, 0.4, 0.7), (cart_x + 0.3, 1.15, cart_z + 0.4), material=mat_cloth)
    
    # Các thùng và rương rải quanh chợ
    create_cylinder("Market_Barrel_1", 0.38, 0.8, (ms1_x + 2.2, 0.4, ms1_z), material=mat_wood, add_collider=True)
    create_box("Market_Crate_1", (0.8, 0.8, 0.8), (ms1_x + 2.2, 0.4, ms1_z + 1.0), material=mat_wood_dark, add_collider=True)

    # 6. NHÀ GIẢ KIM (TRUNG ĐÔNG: X: 8 đến 16, Z: -7 đến 0)
    al_cx, al_cz = 11.5, -3.5
    al_w, al_l, al_h = 7.0, 6.0, 3.4
    
    # Nền móng nhà giả kim
    create_box("Floor_Alchemist", (al_w, 0.2, al_l), (al_cx, 0.1, al_cz), material=mat_stone, add_collider=True)
    
    # Tường cố định (Bắc, Đông, Tây)
    create_box("Wall_North_Alchemist", (al_w, al_h, 0.4), (al_cx, al_h/2, al_cz - al_l/2 + 0.2), material=mat_cloth, add_collider=True)
    create_box("Wall_East_Alchemist", (0.4, al_h, al_l - 0.8), (al_cx + al_w/2 - 0.2, al_h/2, al_cz), material=mat_cloth, add_collider=True)
    create_box("Wall_West_Alchemist", (0.4, al_h, al_l - 0.8), (al_cx - al_w/2 + 0.2, al_h/2, al_cz), material=mat_cloth, add_collider=True)
    
    # Tường mặt trước (Nam) CÓ THỂ ẨN ĐI: Wall_Front_Alchemist
    create_box("Wall_Front_Alchemist_L", (2.7, al_h, 0.4), (al_cx - 2.15, al_h/2, al_cz + al_l/2 - 0.2), material=mat_cloth, add_collider=True)
    create_box("Wall_Front_Alchemist_R", (2.7, al_h, 0.4), (al_cx + 2.15, al_h/2, al_cz + al_l/2 - 0.2), material=mat_cloth, add_collider=True)
    create_box("Wall_Front_Alchemist_Top", (1.6, 0.8, 0.4), (al_cx, al_h - 0.4, al_cz + al_l/2 - 0.2), material=mat_cloth, add_collider=True)
    
    # Mái ngói xanh ngọc teal CÓ THỂ ẨN ĐI: Roof_Alchemist
    build_roof_gabled("Roof_Alchemist", al_w + 0.8, al_l + 0.8, 2.2, (al_cx, al_h, al_cz), material=mat_roof_teal)
    
    # Ống khói ma thuật cong & khói ma thuật cyan phát sáng
    create_cylinder("Chimney_Alchemist", 0.4, 5.0, (al_cx + al_w/2 - 0.8, 2.5, al_cz - al_l/2 + 0.8), material=mat_stone, add_collider=True)
    # Đám mây khói ma thuật cyan phát sáng
    create_icosphere("Smoke_Magic_Cyan_1", 0.6, 1, (al_cx + al_w/2 - 0.8, 5.3, al_cz - al_l/2 + 0.8), material=mat_mystic_cyan)
    create_icosphere("Smoke_Magic_Cyan_2", 0.8, 1, (al_cx + al_w/2 - 0.5, 6.0, al_cz - al_l/2 + 0.6), material=mat_mystic_cyan)
    
    # Bồn thảo mộc dược liệu bên hông Đông nhà giả kim
    create_box("Herb_Bed_1", (1.4, 0.4, 3.5), (al_cx + al_w/2 + 1.2, 0.2, al_cz), material=mat_wood, add_collider=True)
    create_box("Herb_Soil_1", (1.2, 0.1, 3.3), (al_cx + al_w/2 + 1.2, 0.4, al_cz), material=mat_dirt)
    # Các bụi thảo mộc
    for hi in range(4):
        create_icosphere(f"Herb_Plant_{hi}", 0.3, 1, (al_cx + al_w/2 + 1.2, 0.55, al_cz - 1.2 + hi * 0.8), material=mat_vegetable)
        
    # Nội thất bên trong Nhà Giả Kim:
    # Vạc ma thuật lớn ở trung tâm phòng
    create_cylinder("Cauldron_Pedestal", 1.0, 0.3, (al_cx, 0.15, al_cz), material=mat_stone, add_collider=True)
    create_cylinder("Cauldron_Magic", 0.8, 0.8, (al_cx, 0.7, al_cz), material=mat_darkiron, add_collider=True)
    # Dung dịch ma thuật cyan phát sáng bên trong vạc
    create_cylinder("Cauldron_Liquid_Cyan", 0.75, 0.05, (al_cx, 1.05, al_cz), material=mat_mystic_cyan)
    # Bong bóng ma thuật lơ lửng trên vạc
    create_icosphere("Magic_Bubble_1", 0.15, 1, (al_cx - 0.2, 1.35, al_cz + 0.1), material=mat_mystic_cyan)
    create_icosphere("Magic_Bubble_2", 0.12, 1, (al_cx + 0.25, 1.5, al_cz - 0.15), material=mat_mystic_cyan)
    
    # Kệ sách ma thuật kịch trần dọc tường Bắc
    create_box("Bookshelf_Magic", (4.5, 2.8, 0.6), (al_cx, 1.4, al_cz - al_l/2 + 0.6), material=mat_wood_dark, add_collider=True)
    
    # Bàn pha chế độc dược dọc tường Đông
    create_box("Potion_Table", (0.8, 0.9, 3.0), (al_cx + al_w/2 - 0.7, 0.45, al_cz), material=mat_wood, add_collider=True)
    # Các lọ potion trên bàn
    create_cylinder("Potion_Cyan", 0.1, 0.3, (al_cx + al_w/2 - 0.7, 1.05, al_cz - 0.8), material=mat_mystic_cyan)
    create_cylinder("Potion_Red", 0.1, 0.35, (al_cx + al_w/2 - 0.7, 1.08, al_cz - 0.3), material=mat_lava_fire)
    create_cylinder("Potion_Green", 0.12, 0.25, (al_cx + al_w/2 - 0.7, 1.03, al_cz + 0.5), material=mat_vegetable)

    # 7. KHU MỎ ĐÁ (ĐÔNG BẮC: X: 8 đến 23, Z: -23 đến -9)
    # Vách núi đá mỏ cao sừng sững
    cliff_x, cliff_z = 16.0, -17.0
    # Khối núi chính
    create_box("Mountain_Mine_Wall", (14.0, 8.0, 12.0), (cliff_x, 4.0, cliff_z), material=mat_stone, add_collider=True)
    # Các gờ đá phụ tạo độ gồ ghề Stylized
    create_box("Mountain_Ledge_1", (6.0, 5.0, 4.0), (cliff_x - 4.5, 2.5, cliff_z + 4.5), material=mat_stone, add_collider=True)
    create_box("Mountain_Ledge_2", (5.0, 6.5, 5.0), (cliff_x + 4.5, 3.25, cliff_z + 3.5), material=mat_stone, add_collider=True)
    
    # Cửa vòm hang hầm mỏ đào sâu vào núi
    cave_x, cave_z = 13.5, -11.0
    create_box("Mine_Cave_Entrance_Dark", (2.8, 3.2, 1.5), (cave_x, 1.6, cave_z), material=mat_darkiron, add_collider=True)
    # Khung xà gỗ chống hầm
    create_cylinder("Mine_Timber_Post_L", 0.18, 3.2, (cave_x - 1.4, 1.6, cave_z + 0.8), material=mat_wood, add_collider=True)
    create_cylinder("Mine_Timber_Post_R", 0.18, 3.2, (cave_x + 1.4, 1.6, cave_z + 0.8), material=mat_wood, add_collider=True)
    create_box("Mine_Timber_Beam", (3.2, 0.35, 0.4), (cave_x, 3.2, cave_z + 0.8), material=mat_wood)
    
    # Lò luyện quặng đá vòm lớn (Smelting Furnace)
    furn_x, furn_z = 8.5, -15.5
    create_box("Smelting_Furnace_Base", (3.6, 3.4, 3.2), (furn_x, 1.7, furn_z), material=mat_stone, add_collider=True)
    create_box("Smelting_Furnace_Fire", (1.6, 1.2, 0.4), (furn_x, 1.0, furn_z + 1.6), material=mat_lava_fire)
    # Ống khói lò nung
    create_cylinder("Smelting_Chimney", 0.6, 2.2, (furn_x, 4.0, furn_z), material=mat_stone)
    
    # Đường ray xe goòng và Xe goòng chở quặng
    track_z = cave_z + 2.5
    # Thanh tà vẹt gỗ
    for ti in range(6):
        create_box(f"Mine_Tie_{ti}", (1.6, 0.08, 0.25), (cave_x, 0.04, track_z + ti * 0.8), material=mat_wood)
    # Hai thanh ray sắt
    create_box("Mine_Rail_L", (0.08, 0.12, 4.8), (cave_x - 0.6, 0.1, track_z + 2.0), material=mat_metal)
    create_box("Mine_Rail_R", (0.08, 0.12, 4.8), (cave_x + 0.6, 0.1, track_z + 2.0), material=mat_metal)
    
    # Xe goòng khai khoáng (Mine Cart)
    mc_x, mc_z = cave_x, track_z + 2.4
    create_box("Mine_Cart_Body", (1.4, 0.8, 1.8), (mc_x, 0.65, mc_z), material=mat_darkiron, add_collider=True)
    create_box("Mine_Cart_Ore", (1.2, 0.3, 1.6), (mc_x, 1.05, mc_z), material=mat_stone)
    # 4 bánh xe sắt
    create_cylinder("MC_Wheel_1", 0.22, 0.08, (mc_x - 0.65, 0.25, mc_z - 0.5), rotation=(0, 0, 1.57), material=mat_metal)
    create_cylinder("MC_Wheel_2", 0.22, 0.08, (mc_x + 0.65, 0.25, mc_z - 0.5), rotation=(0, 0, 1.57), material=mat_metal)
    create_cylinder("MC_Wheel_3", 0.22, 0.08, (mc_x - 0.65, 0.25, mc_z + 0.5), rotation=(0, 0, 1.57), material=mat_metal)
    create_cylinder("MC_Wheel_4", 0.22, 0.08, (mc_x + 0.65, 0.25, mc_z + 0.5), rotation=(0, 0, 1.57), material=mat_metal)

    # 8. QUÁN ĂN / NHÀ BẾP (ĐÔNG NAM: X: 9 đến 17, Z: 7 đến 14)
    cf_cx, cf_cz = 13.0, 10.5
    cf_w, cf_l, cf_h = 7.0, 6.0, 3.2
    
    # Nền quán ăn
    create_box("Floor_Chef", (cf_w, 0.2, cf_l), (cf_cx, 0.1, cf_cz), material=mat_wood, add_collider=True)
    
    # Tường cố định (Bắc, Đông, Tây)
    create_box("Wall_North_Chef", (cf_w, cf_h, 0.4), (cf_cx, cf_h/2, cf_cz - cf_l/2 + 0.2), material=mat_wood, add_collider=True)
    create_box("Wall_East_Chef", (0.4, cf_h, cf_l - 0.8), (cf_cx + cf_w/2 - 0.2, cf_h/2, cf_cz), material=mat_wood, add_collider=True)
    create_box("Wall_West_Chef", (0.4, cf_h, cf_l - 0.8), (cf_cx - cf_w/2 + 0.2, cf_h/2, cf_cz), material=mat_wood, add_collider=True)
    
    # Tường mặt trước (Nam) CÓ THỂ ẨN ĐI: Wall_Front_Chef
    create_box("Wall_Front_Chef_L", (2.7, cf_h, 0.4), (cf_cx - 2.15, cf_h/2, cf_cz + cf_l/2 - 0.2), material=mat_wood, add_collider=True)
    create_box("Wall_Front_Chef_R", (2.7, cf_h, 0.4), (cf_cx + 2.15, cf_h/2, cf_cz + cf_l/2 - 0.2), material=mat_wood, add_collider=True)
    create_box("Wall_Front_Chef_Top", (1.6, 0.8, 0.4), (cf_cx, cf_h - 0.4, cf_cz + cf_l/2 - 0.2), material=mat_wood, add_collider=True)
    
    # Mái nhà ngói đỏ CÓ THỂ ẨN ĐI: Roof_Chef
    build_roof_gabled("Roof_Chef", cf_w + 0.8, cf_l + 0.8, 2.0, (cf_cx, cf_h, cf_cz), material=mat_roof_red)
    
    # Nội thất Quán Ăn / Bếp:
    # Lò nướng bánh mì gạch đá lớn sát tường Bắc
    create_box("Oven_Bakery", (2.4, 1.8, 1.2), (cf_cx - 1.8, 0.9, cf_cz - cf_l/2 + 0.8), material=mat_stone, add_collider=True)
    create_box("Oven_Fire", (1.2, 0.6, 0.2), (cf_cx - 1.8, 0.7, cf_cz - cf_l/2 + 1.35), material=mat_lava_fire)
    # Bàn sơ chế và bánh mì
    create_box("Kitchen_Prep_Table", (1.8, 0.85, 1.0), (cf_cx + 1.8, 0.42, cf_cz - cf_l/2 + 0.8), material=mat_wood, add_collider=True)
    create_icosphere("Bread_Loaf_1", 0.2, 1, (cf_cx + 1.5, 0.95, cf_cz - cf_l/2 + 0.8), material=mat_dirt)
    create_icosphere("Bread_Loaf_2", 0.22, 1, (cf_cx + 2.0, 0.95, cf_cz - cf_l/2 + 0.8), material=mat_dirt)
    # Bàn ăn dài và 2 dãy ghế
    create_box("Dining_Table", (1.4, 0.85, 3.2), (cf_cx, 0.42, cf_cz + 0.6), material=mat_wood, add_collider=True)
    create_box("Dining_Bench_L", (0.4, 0.45, 3.0), (cf_cx - 1.1, 0.22, cf_cz + 0.6), material=mat_wood, add_collider=True)
    create_box("Dining_Bench_R", (0.4, 0.45, 3.0), (cf_cx + 1.1, 0.22, cf_cz + 0.6), material=mat_wood, add_collider=True)
    # Thùng bia/rượu gỗ ở góc phòng
    create_cylinder("Beer_Keg_1", 0.4, 0.9, (cf_cx + cf_w/2 - 0.8, 0.45, cf_cz + cf_l/2 - 1.0), material=mat_wood_dark, add_collider=True)
    create_cylinder("Beer_Keg_2", 0.35, 0.8, (cf_cx + cf_w/2 - 1.5, 0.4, cf_cz + cf_l/2 - 0.8), material=mat_wood_dark, add_collider=True)

    # 9. NHÀ DÂN (NAM TRUNG TÂM / TÂY NAM: X: -10 đến -2, Z: 8 đến 15)
    hs_cx, hs_cz = -6.0, 11.5
    hs_w, hs_l, hs_h = 7.0, 6.0, 3.2
    
    # Nền nhà dân
    create_box("Floor_House", (hs_w, 0.2, hs_l), (hs_cx, 0.1, hs_cz), material=mat_wood, add_collider=True)
    
    # Tường cố định (Bắc, Tây, Đông)
    create_box("Wall_North_House", (hs_w, hs_h, 0.4), (hs_cx, hs_h/2, hs_cz - hs_l/2 + 0.2), material=mat_cloth, add_collider=True)
    create_box("Wall_West_House", (0.4, hs_h, hs_l - 0.8), (hs_cx - hs_w/2 + 0.2, hs_h/2, hs_cz), material=mat_cloth, add_collider=True)
    create_box("Wall_East_House", (0.4, hs_h, hs_l - 0.8), (hs_cx + hs_w/2 - 0.2, hs_h/2, hs_cz), material=mat_cloth, add_collider=True)
    
    # Tường mặt trước (Nam) CÓ THỂ ẨN ĐI: Wall_Front_House
    create_box("Wall_Front_House_L", (2.7, hs_h, 0.4), (hs_cx - 2.15, hs_h/2, hs_cz + hs_l/2 - 0.2), material=mat_cloth, add_collider=True)
    create_box("Wall_Front_House_R", (2.7, hs_h, 0.4), (hs_cx + 2.15, hs_h/2, hs_cz + hs_l/2 - 0.2), material=mat_cloth, add_collider=True)
    create_box("Wall_Front_House_Top", (1.6, 0.8, 0.4), (hs_cx, hs_h - 0.4, hs_cz + hs_l/2 - 0.2), material=mat_cloth, add_collider=True)
    
    # Mái nhà ngói đỏ CÓ THỂ ẨN ĐI: Roof_House
    build_roof_gabled("Roof_House", hs_w + 0.8, hs_l + 0.8, 2.0, (hs_cx, hs_h, hs_cz), material=mat_roof_red)
    
    # Bậc thềm đá trước cửa nhà dân
    create_box("House_Doorstep", (2.0, 0.15, 0.8), (hs_cx, 0.08, hs_cz + hs_l/2 + 0.3), material=mat_stone)
    
    # Nội thất Nhà Dân:
    # Giường ngủ bằng gỗ ấm cúng
    create_box("Bed_Frame", (1.8, 0.4, 2.4), (hs_cx - hs_w/2 + 1.4, 0.2, hs_cz - hs_l/2 + 1.6), material=mat_wood, add_collider=True)
    create_box("Bed_Mattress", (1.6, 0.25, 2.2), (hs_cx - hs_w/2 + 1.4, 0.45, hs_cz - hs_l/2 + 1.6), material=mat_cloth)
    create_box("Bed_Pillow", (1.2, 0.15, 0.6), (hs_cx - hs_w/2 + 1.4, 0.62, hs_cz - hs_l/2 + 0.8), material=mat_roof_red)
    # Thảm len trải sàn giữa phòng
    create_box("House_Rug", (2.4, 0.02, 3.0), (hs_cx, 0.21, hs_cz + 0.2), material=mat_foliage)
    # Tủ quần áo bằng gỗ cao góc Đông Bắc
    create_box("House_Wardrobe", (1.4, 2.4, 0.8), (hs_cx + hs_w/2 - 1.1, 1.2, hs_cz - hs_l/2 + 0.8), material=mat_wood_dark, add_collider=True)
    # Bàn đọc sách nhỏ và ghế
    create_box("House_Desk", (1.2, 0.8, 0.7), (hs_cx + hs_w/2 - 1.0, 0.4, hs_cz + 1.5), material=mat_wood, add_collider=True)
    create_box("House_Chair", (0.5, 0.5, 0.5), (hs_cx + hs_w/2 - 1.0, 0.25, hs_cz + 0.8), material=mat_wood)

    # 10. CỔNG LÀNG, HÀNG RÀO & VƯỜN RAU CẢI BẮP (PHÍA NAM: Z: 16 đến 22)
    # Cổng làng ở giữa: 2 cột trụ cổng gỗ cao kèm đèn lồng
    gate_w = 4.6
    create_cylinder("Gate_Post_L", 0.25, 3.8, (-gate_w/2, 1.9, 18.5), material=mat_wood, add_collider=True)
    create_cylinder("Gate_Post_R", 0.25, 3.8, (gate_w/2, 1.9, 18.5), material=mat_wood, add_collider=True)
    create_box("Gate_Crossbeam", (gate_w + 1.0, 0.35, 0.4), (0.0, 3.7, 18.5), material=mat_wood)
    # Biển chỉ dẫn làng
    create_box("Gate_Signboard", (2.2, 0.6, 0.08), (0.0, 3.0, 18.5), material=mat_wood_dark)
    
    # Hàng rào gỗ rustic chạy sang 2 bên
    # Nhánh Tây: X từ -2.5 đến -22.0
    for fi in range(10):
        fx = -3.2 - fi * 1.9
        create_cylinder(f"Fence_Post_W_{fi}", 0.12, 1.4, (fx, 0.7, 18.5), material=mat_wood, add_collider=True)
        if fi < 9:
            create_box(f"Fence_Rail_W_{fi}", (1.9, 0.1, 0.08), (fx - 0.95, 0.9, 18.5), material=mat_wood)
            create_box(f"Fence_Rail_W2_{fi}", (1.9, 0.1, 0.08), (fx - 0.95, 0.45, 18.5), material=mat_wood)
            
    # Nhánh Đông: X từ 2.5 đến 22.0
    for fi in range(10):
        fx = 3.2 + fi * 1.9
        create_cylinder(f"Fence_Post_E_{fi}", 0.12, 1.4, (fx, 0.7, 18.5), material=mat_wood, add_collider=True)
        if fi < 9:
            create_box(f"Fence_Rail_E_{fi}", (1.9, 0.1, 0.08), (fx + 0.95, 0.9, 18.5), material=mat_wood)
            create_box(f"Fence_Rail_E2_{fi}", (1.9, 0.1, 0.08), (fx + 0.95, 0.45, 18.5), material=mat_wood)
            
    # Vườn rau cải bắp (Vegetable Garden)
    # Cụm vườn Tây Nam: X: -8 đến -3, Z: 15.5 đến 18.0
    for bed_i in range(3):
        bz = 16.0 + bed_i * 0.9
        create_box(f"Veg_Bed_W_{bed_i}", (4.8, 0.18, 0.65), (-5.5, 0.09, bz), material=mat_dirt)
        # Các bắp cải tròn xanh tươi trên luống
        for ci in range(5):
            cx = -7.4 + ci * 0.95
            create_icosphere(f"Cabbage_W_{bed_i}_{ci}", 0.22, 1, (cx, 0.28, bz), material=mat_vegetable)
            
    # Cụm vườn Đông Nam: X: 3 đến 8, Z: 15.5 đến 18.0
    for bed_i in range(3):
        bz = 16.0 + bed_i * 0.9
        create_box(f"Veg_Bed_E_{bed_i}", (4.8, 0.18, 0.65), (5.5, 0.09, bz), material=mat_dirt)
        for ci in range(5):
            cx = 3.6 + ci * 0.95
            create_icosphere(f"Cabbage_E_{bed_i}_{ci}", 0.22, 1, (cx, 0.28, bz), material=mat_vegetable)
            
    # Cọc chỉ đường bằng gỗ ở ngã ba cổng làng
    create_cylinder("Signpost_Pole", 0.1, 2.0, (1.8, 1.0, 16.5), material=mat_wood, add_collider=True)
    create_box("Sign_Market", (0.8, 0.25, 0.06), (1.8, 1.7, 16.5), rotation=(0, 0.4, 0), material=mat_wood_dark)
    create_box("Sign_Smith", (0.8, 0.25, 0.06), (1.8, 1.4, 16.5), rotation=(0, -0.6, 0), material=mat_wood_dark)

    # 11. CÂY CỐI VÀ TẢNG ĐÁ RẢI RÁC TRONG LÀNG
    village_trees = [
        (-14.0, 4.0), (-16.0, 10.0), (-12.0, 15.0),
        (8.0, -8.0), (16.0, 2.0), (18.0, 14.0),
        (-2.0, 21.0), (3.0, 21.5), (-14.0, 20.0), (14.0, 20.5)
    ]
    for idx, (tx, tz) in enumerate(village_trees):
        build_tree(f"VillageTree_{idx}", (tx, 0.0, tz), scale=0.9, mat_wood=mat_wood, mat_foliage=mat_foliage)
        
    print("=== DỰNG XONG HÌNH HỌC BẢN ĐỒ LÀNG ===")

def export_glb(output_path):
    """Xuất toàn bộ Scene sang định dạng GLB chuẩn Godot 4."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"Đang xuất file GLB sang: {output_path}")
    
    # Chọn tất cả các object
    bpy.ops.object.select_all(action='SELECT')
    
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_yup=True,
        export_apply=True,
        export_materials='EXPORT',
        export_cameras=False,
        export_lights=False
    )
    print(f"=== XUẤT THÀNH CÔNG: {output_path} ===")

if __name__ == "__main__":
    build_village()
    out_blend = os.path.abspath("Assets/Blender_Source/village_map.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)
    print(f"=== ĐÃ LƯU FILE BLEND AN TOÀN: {out_blend} ===")
    out_file = os.path.abspath("Assets/Models/village_map.glb")
    export_glb(out_file)
