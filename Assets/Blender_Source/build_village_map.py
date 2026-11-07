"""
Script Blender 3D: Dựng Bản Đồ Làng Mở Rộng Liền Kề (Village Map District)
Kết nối trực tiếp với Đảo Đá WorldMap tại Z in [16, 50], Y = 0.0 trên cánh đồng cỏ.
Dựa trên ảnh concept 'modelyeucau/map2/1.jpg'.
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

def create_box(name, size, location, rotation=(0, 0, 0), material=None, add_collider=False):
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

def create_icosphere(name, radius, subdivisions, location, material=None):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=subdivisions,
        radius=radius,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def build_tree(name, location, scale=1.0, mat_wood=None, mat_foliage=None):
    x, y, z = location
    trunk_h = 2.4 * scale
    trunk_r = 0.25 * scale
    create_cylinder(f"{name}_Trunk", trunk_r, trunk_h, (x, y + trunk_h / 2, z), material=mat_wood, add_collider=True)
    f1_r = 1.3 * scale
    f1_y = y + trunk_h + 0.3 * scale
    create_icosphere(f"{name}_Foliage1", f1_r, 1, (x, f1_y, z), material=mat_foliage)
    f2_r = 0.9 * scale
    f2_y = f1_y + 0.8 * scale
    create_icosphere(f"{name}_Foliage2", f2_r, 1, (x + 0.1 * scale, f2_y, z - 0.1 * scale), material=mat_foliage)

def build_roof_gabled(name, width, length, height, center_pos, material=None):
    cx, cy, cz = center_pos
    hw = width / 2.0
    hl = length / 2.0
    
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    verts = [
        Vector((-hw, 0, -hl)),
        Vector((hw, 0, -hl)),
        Vector((hw, 0, hl)),
        Vector((-hw, 0, hl)),
        Vector((0, height, -hl)),
        Vector((0, height, hl))
    ]
    
    faces = [
        [0, 1, 4],
        [2, 3, 5],
        [0, 4, 5, 3],
        [1, 2, 5, 4],
        [3, 2, 1, 0]
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
    print("=== DỰNG BẢN ĐỒ LÀNG MỞ RỘNG LIỀN KỀ WORLDMAP ===")
    clean_scene()
    
    # 1. BẢNG VẬT LIỆU
    mat_dirt = create_material("Mat_Dirt", (0.54, 0.36, 0.21), roughness=0.90)
    mat_stone = create_material("Mat_Stone", (0.48, 0.50, 0.52), roughness=0.80)
    mat_wood = create_material("Mat_Wood", (0.55, 0.35, 0.21), roughness=0.75)
    mat_wood_fence = create_material("Mat_Wood_Fence", (0.40, 0.25, 0.15), roughness=0.80)
    mat_metal = create_material("Mat_Metal", (0.61, 0.64, 0.68), roughness=0.35, metallic=0.85)
    mat_darkiron = create_material("Mat_DarkIron", (0.18, 0.20, 0.22), roughness=0.40, metallic=0.90)
    mat_roof_red = create_material("Mat_Roof_Red", (0.78, 0.28, 0.22), roughness=0.80)
    mat_roof_teal = create_material("Mat_Roof_Teal", (0.18, 0.55, 0.52), roughness=0.80)
    mat_canopy_striped = create_material("Mat_Canopy_Striped", (0.85, 0.25, 0.20), roughness=0.85)
    mat_mystic_cyan = create_material("Mat_Mystic_Cyan", (0.20, 0.85, 0.80), roughness=0.20, emission_color=(0.20, 0.85, 0.80), emission_strength=2.0)
    mat_lava_fire = create_material("Mat_Lava_Fire", (1.00, 0.45, 0.05), roughness=0.40, emission_color=(1.00, 0.45, 0.05), emission_strength=2.5)
    mat_foliage = create_material("Mat_Foliage", (0.24, 0.56, 0.25), roughness=0.85)
    mat_vegetable = create_material("Mat_Vegetable", (0.37, 0.73, 0.29), roughness=0.80)
    mat_wall = create_material("Mat_Wall_Stone", (0.60, 0.58, 0.54), roughness=0.85)

    # 2. ĐƯỜNG MÒN ĐẤT NỐI LIỀN TỪ ĐẢO ĐÁ (Z=10) XUỐNG LÀNG
    # Đoạn nối từ Đảo Đá cũ xuống Cổng Làng
    create_box("Path_Connector_Island_To_Village", (3.0, 0.04, 8.0), (0.0, 0.02, 13.0), material=mat_dirt)
    # Đoạn từ Cổng Làng vào Chợ
    create_box("Path_Village_Main", (3.2, 0.04, 12.0), (0.0, 0.02, 23.0), material=mat_dirt)
    # Quảng trường Chợ Trung Tâm
    create_box("Path_Market_Square", (10.0, 0.04, 8.0), (0.0, 0.02, 31.0), material=mat_dirt)
    # Nhánh sang Nhà Rèn (Tây)
    create_box("Path_To_Smith", (6.0, 0.04, 2.4), (-6.0, 0.02, 35.0), material=mat_dirt)
    # Nhánh sang Nhà Giả Kim (Đông)
    create_box("Path_To_Alchemist", (6.0, 0.04, 2.4), (6.0, 0.02, 35.0), material=mat_dirt)
    # Nhánh lên Khu Lâm Nghiệp (Tây Bắc)
    create_box("Path_To_Lumber", (2.4, 0.04, 10.0), (-11.0, 0.02, 41.0), material=mat_dirt)
    # Nhánh lên Khu Mỏ Đá (Đông Bắc)
    create_box("Path_To_Mine", (2.4, 0.04, 10.0), (11.0, 0.02, 41.0), material=mat_dirt)
    # Nhánh vào Quán Ăn (Đông Nam)
    create_box("Path_To_Chef", (4.5, 0.04, 2.2), (5.5, 0.02, 24.0), material=mat_dirt)
    # Nhánh vào Nhà Dân (Tây Nam)
    create_box("Path_To_House", (4.5, 0.04, 2.2), (-5.5, 0.02, 24.0), material=mat_dirt)

    # 3. CỔNG LÀNG & VƯỜN RAU (Z in [17, 21])
    # Hai cột cổng làng
    gate_z = 17.5
    create_cylinder("Gate_Post_L", 0.22, 3.8, (-2.0, 1.9, gate_z), material=mat_wood, add_collider=True)
    create_cylinder("Gate_Post_R", 0.22, 3.8, (2.0, 1.9, gate_z), material=mat_wood, add_collider=True)
    create_box("Gate_Beam_Top", (4.6, 0.35, 0.35), (0.0, 3.6, gate_z), material=mat_wood, add_collider=True)
    create_box("Gate_Signboard", (2.2, 0.7, 0.1), (0.0, 3.0, gate_z), material=mat_wood)

    # Hàng rào gỗ rustic hai bên cổng làng
    for side in [-1, 1]:
        for i in range(4):
            fx = side * (2.8 + i * 1.6)
            create_cylinder(f"Fence_Post_{side}_{i}", 0.10, 1.2, (fx, 0.6, gate_z), material=mat_wood_fence, add_collider=True)
            create_box(f"Fence_Rail_Top_{side}_{i}", (1.7, 0.08, 0.08), (fx - side * 0.8, 0.9, gate_z), material=mat_wood_fence)
            create_box(f"Fence_Rail_Bot_{side}_{i}", (1.7, 0.08, 0.08), (fx - side * 0.8, 0.45, gate_z), material=mat_wood_fence)

    # Vườn rau cải bắp bên trái cổng làng (X in [-7, -2], Z in [18.5, 21.5])
    for row in range(3):
        rz = 19.0 + row * 1.0
        create_box(f"Crop_Soil_{row}", (4.5, 0.1, 0.7), (-4.5, 0.05, rz), material=mat_dirt)
        for col in range(4):
            cx = -6.0 + col * 1.0
            create_icosphere(f"Cabbage_{row}_{col}", 0.25, 1, (cx, 0.22, rz), material=mat_vegetable)

    # Cọc biển chỉ dẫn ngã ba (Nam)
    create_cylinder("Signpost_Crossroad_Post", 0.1, 1.8, (1.8, 0.9, 19.5), material=mat_wood, add_collider=True)
    create_box("Signpost_Board_Market", (0.8, 0.22, 0.06), (1.8, 1.5, 19.5), material=mat_wood)

    # 4. CHỢ TRUNG TÂM (Z in [28, 34], X in [-5, 5])
    # Giếng nước đá tròn mái che ròng rọc
    well_x, well_z = -1.5, 28.5
    create_cylinder("Well_Stone", 1.2, 0.9, (well_x, 0.45, well_z), vertices=14, material=mat_stone, add_collider=True)
    create_cylinder("Well_Water", 1.0, 0.1, (well_x, 0.6, well_z), material=mat_mystic_cyan)
    create_cylinder("Well_Post_1", 0.08, 2.2, (well_x - 1.0, 1.1, well_z), material=mat_wood)
    create_cylinder("Well_Post_2", 0.08, 2.2, (well_x + 1.0, 1.1, well_z), material=mat_wood)
    create_box("Well_Roof", (2.4, 0.15, 1.6), (well_x, 2.2, well_z), material=mat_roof_red)

    # Quầy sạp chợ 1 (Bạt sọc đỏ trắng)
    ms1_x, ms1_z = 2.5, 30.0
    create_box("Market_Stall_1_Table", (2.8, 0.85, 1.4), (ms1_x, 0.42, ms1_z), material=mat_wood, add_collider=True)
    create_cylinder("Market_Stall_1_P1", 0.06, 2.3, (ms1_x - 1.3, 1.15, ms1_z - 0.6), material=mat_wood)
    create_cylinder("Market_Stall_1_P2", 0.06, 2.3, (ms1_x + 1.3, 1.15, ms1_z - 0.6), material=mat_wood)
    create_cylinder("Market_Stall_1_P3", 0.06, 2.3, (ms1_x - 1.3, 1.15, ms1_z + 0.6), material=mat_wood)
    create_cylinder("Market_Stall_1_P4", 0.06, 2.3, (ms1_x + 1.3, 1.15, ms1_z + 0.6), material=mat_wood)
    create_box("Market_Stall_1_Canopy", (3.2, 0.15, 1.8), (ms1_x, 2.2, ms1_z), material=mat_canopy_striped)

    # Xe kéo hàng gỗ 2 bánh
    cart_x, cart_z = -2.5, 32.5
    create_box("Cart_Body", (1.8, 0.5, 1.2), (cart_x, 0.55, cart_z), material=mat_wood, add_collider=True)
    create_cylinder("Cart_Wheel_L", 0.4, 0.12, (cart_x - 0.95, 0.4, cart_z), rotation=(1.57, 0, 0), material=mat_wood_fence)
    create_cylinder("Cart_Wheel_R", 0.4, 0.12, (cart_x + 0.95, 0.4, cart_z), rotation=(1.57, 0, 0), material=mat_wood_fence)
    create_box("Cart_Crate", (0.7, 0.6, 0.7), (cart_x, 1.0, cart_z), material=mat_wood)

    # 5. NHÀ RÈN (TÂY: X = -11, Z = 36)
    sm_cx, sm_cz = -11.0, 36.0
    sm_w, sm_l, sm_h = 5.6, 4.8, 2.8

    # Sàn nhà rèn
    create_box("Floor_Smith", (sm_w, 0.15, sm_l), (sm_cx, 0.08, sm_cz), material=mat_stone, add_collider=True)
    # Tường Bắc, Nam, Tây
    create_box("Wall_North_Smith", (sm_w, sm_h, 0.3), (sm_cx, sm_h/2, sm_cz + sm_l/2 - 0.15), material=mat_wall, add_collider=True)
    create_box("Wall_South_Smith", (sm_w, sm_h, 0.3), (sm_cx, sm_h/2, sm_cz - sm_l/2 + 0.15), material=mat_wall, add_collider=True)
    create_box("Wall_West_Smith", (0.3, sm_h, sm_l - 0.6), (sm_cx - sm_w/2 + 0.15, sm_h/2, sm_cz), material=mat_wall, add_collider=True)
    # Tường trước phía Đông (cửa mở ra chợ): tách riêng để fade
    create_box("Wall_Front_Smith_L", (0.3, sm_h, 1.6), (sm_cx + sm_w/2 - 0.15, sm_h/2, sm_cz - 1.4), material=mat_wall, add_collider=True)
    create_box("Wall_Front_Smith_R", (0.3, sm_h, 1.6), (sm_cx + sm_w/2 - 0.15, sm_h/2, sm_cz + 1.4), material=mat_wall, add_collider=True)
    create_box("Wall_Front_Smith_Top", (0.3, 0.7, 1.6), (sm_cx + sm_w/2 - 0.15, sm_h - 0.35, sm_cz), material=mat_wall, add_collider=True)
    # Mái nhà rèn ngói đỏ (tách riêng)
    build_roof_gabled("Roof_Smith", sm_w + 0.6, sm_l + 0.6, 1.6, (sm_cx, sm_h, sm_cz), material=mat_roof_red)

    # Ống khói đá lớn
    create_box("Chimney_Smith_Base", (1.2, 4.8, 1.2), (sm_cx - sm_w/2 + 0.6, 2.4, sm_cz - sm_l/2 + 0.6), material=mat_stone, add_collider=True)
    # Lò rèn trong nhà (than hồng)
    create_box("Forge_Indoor_Base", (1.4, 0.9, 1.2), (sm_cx - 1.5, 0.45, sm_cz - 1.4), material=mat_stone, add_collider=True)
    create_box("Forge_Indoor_Fire", (1.0, 0.2, 0.8), (sm_cx - 1.5, 0.95, sm_cz - 1.4), material=mat_lava_fire)
    # Đe sắt trong nhà
    create_cylinder("Anvil_Indoor_Log", 0.4, 0.7, (sm_cx, 0.35, sm_cz), material=mat_wood, add_collider=True)
    create_box("Anvil_Indoor_Iron", (0.5, 0.3, 0.8), (sm_cx, 0.8, sm_cz), material=mat_darkiron, add_collider=True)
    # Rương quặng & than
    create_box("Chest_Coal", (1.0, 0.6, 0.7), (sm_cx - 1.8, 0.3, sm_cz + 1.4), material=mat_wood_fence)
    create_box("Chest_Scrap", (1.0, 0.6, 0.7), (sm_cx + 1.6, 0.3, sm_cz - 1.4), material=mat_wood_fence)

    # Sân rèn ngoài trời (Đe + Lò rèn ngoài sân)
    out_x, out_z = -6.5, 35.0
    create_cylinder("Anvil_Outdoor_Log", 0.45, 0.7, (out_x, 0.35, out_z), material=mat_wood, add_collider=True)
    create_box("Anvil_Outdoor_Iron", (0.6, 0.35, 0.9), (out_x, 0.82, out_z), material=mat_darkiron, add_collider=True)
    create_box("Forge_Outdoor_Base", (1.4, 0.9, 1.2), (out_x - 1.2, 0.45, out_z - 1.4), material=mat_stone, add_collider=True)
    create_box("Forge_Outdoor_Fire", (1.0, 0.2, 0.8), (out_x - 1.2, 0.95, out_z - 1.4), material=mat_lava_fire)

    # 6. NHÀ GIẢ KIM (ĐÔNG: X = 11, Z = 36)
    al_cx, al_cz = 11.0, 36.0
    al_w, al_l, al_h = 5.6, 4.8, 2.8

    # Sàn nhà giả kim
    create_box("Floor_Alchemist", (al_w, 0.15, al_l), (al_cx, 0.08, al_cz), material=mat_stone, add_collider=True)
    # Tường Bắc, Nam, Đông
    create_box("Wall_North_Alchemist", (al_w, al_h, 0.3), (al_cx, al_h/2, al_cz + al_l/2 - 0.15), material=mat_wall, add_collider=True)
    create_box("Wall_South_Alchemist", (al_w, al_h, 0.3), (al_cx, al_h/2, al_cz - al_l/2 + 0.15), material=mat_wall, add_collider=True)
    create_box("Wall_East_Alchemist", (0.3, al_h, al_l - 0.6), (al_cx + al_w/2 - 0.15, al_h/2, al_cz), material=mat_wall, add_collider=True)
    # Tường trước phía Tây (cửa mở ra chợ): tách riêng để fade
    create_box("Wall_Front_Alchemist_L", (0.3, al_h, 1.6), (al_cx - al_w/2 + 0.15, al_h/2, al_cz - 1.4), material=mat_wall, add_collider=True)
    create_box("Wall_Front_Alchemist_R", (0.3, al_h, 1.6), (al_cx - al_w/2 + 0.15, al_h/2, al_cz + 1.4), material=mat_wall, add_collider=True)
    create_box("Wall_Front_Alchemist_Top", (0.3, 0.7, 1.6), (al_cx - al_w/2 + 0.15, al_h - 0.35, al_cz), material=mat_wall, add_collider=True)
    # Mái ngói xanh ngọc teal (tách riêng)
    build_roof_gabled("Roof_Alchemist", al_w + 0.6, al_l + 0.6, 1.6, (al_cx, al_h, al_cz), material=mat_roof_teal)

    # Ống khói ma thuật cong
    create_cylinder("Chimney_Alchemist", 0.35, 4.5, (al_cx + al_w/2 - 0.8, 2.25, al_cz - al_l/2 + 0.8), material=mat_stone, add_collider=True)
    create_icosphere("Smoke_Alchemist_1", 0.45, 1, (al_cx + al_w/2 - 0.8, 4.8, al_cz - al_l/2 + 0.8), material=mat_mystic_cyan)
    create_icosphere("Smoke_Alchemist_2", 0.6, 1, (al_cx + al_w/2 - 0.6, 5.4, al_cz - al_l/2 + 0.6), material=mat_mystic_cyan)

    # Nội thất Nhà Giả Kim
    # Vạc ma thuật ở trung tâm
    create_cylinder("Cauldron_Base", 0.7, 0.7, (al_cx, 0.35, al_cz), material=mat_darkiron, add_collider=True)
    create_cylinder("Cauldron_Potion", 0.6, 0.1, (al_cx, 0.68, al_cz), material=mat_mystic_cyan)
    # Kệ sách cổ
    create_box("Bookshelf_Alchemist", (3.6, 2.4, 0.5), (al_cx, 1.2, al_cz + al_l/2 - 0.5), material=mat_wood_fence, add_collider=True)
    # Bàn pha chế potion
    create_box("Potion_Table", (0.8, 0.85, 2.4), (al_cx + al_w/2 - 0.6, 0.42, al_cz), material=mat_wood, add_collider=True)
    # Bồn thảo dược bên hông nhà
    create_box("Herb_Bed_1", (1.2, 0.35, 3.2), (al_cx + al_w/2 + 0.8, 0.18, al_cz), material=mat_wood_fence, add_collider=True)
    create_box("Herb_Soil_1", (1.0, 0.08, 3.0), (al_cx + al_w/2 + 0.8, 0.35, al_cz), material=mat_vegetable)

    # 7. QUÁN ĂN / NHÀ BẾP (ĐÔNG NAM: X = 10, Z = 24)
    cf_cx, cf_cz = 10.0, 24.0
    cf_w, cf_l, cf_h = 5.0, 4.4, 2.6
    create_box("Floor_Chef", (cf_w, 0.15, cf_l), (cf_cx, 0.08, cf_cz), material=mat_stone, add_collider=True)
    create_box("Wall_North_Chef", (cf_w, cf_h, 0.3), (cf_cx, cf_h/2, cf_cz + cf_l/2 - 0.15), material=mat_wall, add_collider=True)
    create_box("Wall_South_Chef", (cf_w, cf_h, 0.3), (cf_cx, cf_h/2, cf_cz - cf_l/2 + 0.15), material=mat_wall, add_collider=True)
    create_box("Wall_East_Chef", (0.3, cf_h, cf_l - 0.6), (cf_cx + cf_w/2 - 0.15, cf_h/2, cf_cz), material=mat_wall, add_collider=True)
    # Tường trước phía Tây
    create_box("Wall_Front_Chef_L", (0.3, cf_h, 1.4), (cf_cx - cf_w/2 + 0.15, cf_h/2, cf_cz - 1.2), material=mat_wall, add_collider=True)
    create_box("Wall_Front_Chef_R", (0.3, cf_h, 1.4), (cf_cx - cf_w/2 + 0.15, cf_h/2, cf_cz + 1.2), material=mat_wall, add_collider=True)
    create_box("Wall_Front_Chef_Top", (0.3, 0.6, 1.6), (cf_cx - cf_w/2 + 0.15, cf_h - 0.3, cf_cz), material=mat_wall, add_collider=True)
    build_roof_gabled("Roof_Chef", cf_w + 0.6, cf_l + 0.6, 1.5, (cf_cx, cf_h, cf_cz), material=mat_roof_red)

    # Nội thất Quán Ăn
    # Lò nướng bánh mì gạch đá
    create_box("Oven_Chef_Base", (1.4, 1.2, 1.2), (cf_cx + cf_w/2 - 0.9, 0.6, cf_cz - cf_l/2 + 0.9), material=mat_stone, add_collider=True)
    create_box("Oven_Chef_Fire", (0.8, 0.4, 0.4), (cf_cx + cf_w/2 - 0.9, 0.4, cf_cz - cf_l/2 + 0.4), material=mat_lava_fire)
    # Bàn ăn dài & ghế
    create_box("Dining_Table", (1.4, 0.8, 2.4), (cf_cx - 0.6, 0.4, cf_cz), material=mat_wood, add_collider=True)
    create_box("Dining_Bench_L", (0.4, 0.45, 2.4), (cf_cx - 1.6, 0.22, cf_cz), material=mat_wood)
    create_box("Dining_Bench_R", (0.4, 0.45, 2.4), (cf_cx + 0.4, 0.22, cf_cz), material=mat_wood)

    # 8. NHÀ DÂN (TÂY NAM: X = -10, Z = 24)
    hs_cx, hs_cz = -10.0, 24.0
    hs_w, hs_l, hs_h = 5.0, 4.4, 2.6
    create_box("Floor_House", (hs_w, 0.15, hs_l), (hs_cx, 0.08, hs_cz), material=mat_stone, add_collider=True)
    create_box("Wall_North_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz + hs_l/2 - 0.15), material=mat_wall, add_collider=True)
    create_box("Wall_South_House", (hs_w, hs_h, 0.3), (hs_cx, hs_h/2, hs_cz - hs_l/2 + 0.15), material=mat_wall, add_collider=True)
    create_box("Wall_West_House", (0.3, hs_h, hs_l - 0.6), (hs_cx - hs_w/2 + 0.15, hs_h/2, hs_cz), material=mat_wall, add_collider=True)
    # Tường trước phía Đông
    create_box("Wall_Front_House_L", (0.3, hs_h, 1.4), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz - 1.2), material=mat_wall, add_collider=True)
    create_box("Wall_Front_House_R", (0.3, hs_h, 1.4), (hs_cx + hs_w/2 - 0.15, hs_h/2, hs_cz + 1.2), material=mat_wall, add_collider=True)
    create_box("Wall_Front_House_Top", (0.3, 0.6, 1.6), (hs_cx + hs_w/2 - 0.15, hs_h - 0.3, hs_cz), material=mat_wall, add_collider=True)
    build_roof_gabled("Roof_House", hs_w + 0.6, hs_l + 0.6, 1.5, (hs_cx, hs_h, hs_cz), material=mat_roof_red)

    # Nội thất Nhà Dân: Giường ngủ, tủ áo, thảm
    create_box("Bed_Frame", (1.6, 0.4, 2.2), (hs_cx - hs_w/2 + 1.0, 0.2, hs_cz - hs_l/2 + 1.3), material=mat_wood, add_collider=True)
    create_box("Bed_Mattress", (1.4, 0.2, 2.0), (hs_cx - hs_w/2 + 1.0, 0.45, hs_cz - hs_l/2 + 1.3), material=mat_roof_red)
    create_box("Wardrobe", (1.2, 2.0, 0.6), (hs_cx - hs_w/2 + 0.8, 1.0, hs_cz + hs_l/2 - 0.5), material=mat_wood_fence, add_collider=True)
    create_box("House_Rug", (1.8, 0.02, 1.8), (hs_cx + 0.5, 0.09, hs_cz), material=mat_canopy_striped)

    # 9. KHU LÂM NGHIỆP (TÂY BẮC: X = -14, Z = 45)
    lm_cx, lm_cz = -14.0, 45.0
    # Lán cưa xẻ gỗ
    create_cylinder("Lumber_P1", 0.18, 3.0, (lm_cx - 2.5, 1.5, lm_cz - 2.0), material=mat_wood, add_collider=True)
    create_cylinder("Lumber_P2", 0.18, 3.0, (lm_cx + 2.5, 1.5, lm_cz - 2.0), material=mat_wood, add_collider=True)
    create_cylinder("Lumber_P3", 0.18, 3.0, (lm_cx - 2.5, 1.5, lm_cz + 2.0), material=mat_wood, add_collider=True)
    create_cylinder("Lumber_P4", 0.18, 3.0, (lm_cx + 2.5, 1.5, lm_cz + 2.0), material=mat_wood, add_collider=True)
    create_box("Lumber_Shed_Roof", (5.6, 0.15, 4.6), (lm_cx, 3.1, lm_cz), material=mat_wood_fence)
    # Bàn cưa gỗ
    create_box("Lumber_Saw_Table", (3.2, 0.8, 1.2), (lm_cx, 0.4, lm_cz), material=mat_wood, add_collider=True)
    create_cylinder("Lumber_Saw_Blade", 0.4, 0.04, (lm_cx, 0.9, lm_cz), rotation=(1.57, 0, 0), material=mat_metal)
    # Các đống thân cây gỗ tròn nằm ngang
    for i in range(3):
        create_cylinder(f"Log_Pile_Bot_{i}", 0.3, 3.8, (lm_cx + 3.8, 0.3, lm_cz - 1.2 + i * 0.7), rotation=(1.57, 0, 0), material=mat_wood, add_collider=True)
    for i in range(2):
        create_cylinder(f"Log_Pile_Top_{i}", 0.28, 3.8, (lm_cx + 3.8, 0.8, lm_cz - 0.85 + i * 0.7), rotation=(1.57, 0, 0), material=mat_wood)
    # Hàng cây rừng bao quanh
    build_tree("Tree_Lumber_1", (lm_cx - 4.5, 0, lm_cz - 3.0), scale=1.3, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_tree("Tree_Lumber_2", (lm_cx - 4.0, 0, lm_cz + 3.5), scale=1.2, mat_wood=mat_wood, mat_foliage=mat_foliage)
    build_tree("Tree_Lumber_3", (lm_cx, 0, lm_cz + 4.5), scale=1.4, mat_wood=mat_wood, mat_foliage=mat_foliage)

    # 10. KHU MỎ ĐÁ (ĐÔNG BẮC: X = 14, Z = 45)
    mn_cx, mn_cz = 14.0, 45.0
    # Vách núi đá cao sừng sững
    create_box("Mine_Cliff_Main", (12.0, 7.0, 8.0), (mn_cx, 3.5, mn_cz + 3.0), material=mat_stone, add_collider=True)
    create_box("Mine_Cliff_Ledge", (6.0, 5.0, 4.0), (mn_cx - 4.5, 2.5, mn_cz + 0.5), material=mat_stone, add_collider=True)
    # Cửa vòm hầm mỏ tối
    create_box("Mine_Entrance_Void", (2.8, 3.0, 1.2), (mn_cx, 1.5, mn_cz - 0.9), material=mat_darkiron, add_collider=True)
    create_box("Mine_Beam_L", (0.3, 3.2, 0.4), (mn_cx - 1.5, 1.6, mn_cz - 0.9), material=mat_wood_fence, add_collider=True)
    create_box("Mine_Beam_R", (0.3, 3.2, 0.4), (mn_cx + 1.5, 1.6, mn_cz - 0.9), material=mat_wood_fence, add_collider=True)
    create_box("Mine_Beam_Top", (3.4, 0.35, 0.4), (mn_cx, 3.1, mn_cz - 0.9), material=mat_wood_fence, add_collider=True)
    # Lò luyện quặng vòm rực lửa
    create_cylinder("Ore_Furnace", 1.2, 2.4, (mn_cx - 4.0, 1.2, mn_cz - 2.5), vertices=12, material=mat_stone, add_collider=True)
    create_box("Ore_Furnace_Fire", (0.8, 0.5, 0.4), (mn_cx - 4.0, 0.5, mn_cz - 1.8), material=mat_lava_fire)
    # Đường ray xe goòng ngắn
    create_box("Rail_L", (0.08, 0.08, 4.0), (mn_cx + 2.0, 0.06, mn_cz - 1.0), material=mat_metal)
    create_box("Rail_R", (0.08, 0.08, 4.0), (mn_cx + 2.8, 0.06, mn_cz - 1.0), material=mat_metal)
    # Xe goòng chở quặng
    create_box("Minecart_Body", (1.2, 0.6, 1.6), (mn_cx + 2.4, 0.55, mn_cz - 1.5), material=mat_darkiron, add_collider=True)
    create_box("Minecart_Ore", (0.9, 0.25, 1.3), (mn_cx + 2.4, 0.85, mn_cz - 1.5), material=mat_stone)

    # XUẤT RA GLB
    out_glb = "Assets/Models/village_map.glb"
    print(f"Xuất mô hình sang: {out_glb}")
    bpy.ops.export_scene.gltf(
        filepath=out_glb,
        export_format='GLB',
        export_yup=True,
        export_apply=True,
        export_materials='EXPORT'
    )
    # Lưu file blend an toàn
    blend_path = "Assets/Blender_Source/village_map.blend"
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("=== DỰNG BẢN ĐỒ LÀNG MỞ RỘNG HOÀN TẤT ===")

if __name__ == '__main__':
    build_village()
