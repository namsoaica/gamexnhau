"""
Thư Viện Procedural Chuẩn Cho Blender 3D (tools/blender_kit.py)
Dự án: Trò Chơi Mới - Antigravity Pipeline
Quy chuẩn:
- Cấm dùng primitive thô sơ (No Raw Primitives).
- Bắt buộc trải UV tự động (unwrap_mesh) cho TẤT CẢ các mesh tạo ra.
- Sử dụng bmesh, Blender Modifiers (Bevel 2-3 segments bo viền bắt sáng, Solidify, Displace).
- Gán vật liệu Principled BSDF liên kết Texture Seamless (thớ gỗ, thớ đá, bạt sọc, vân đất, ngói đỏ, ngói teal).
- Tự động căn chỉnh AABB (snap_to_ground, stack_on_top) chống bay lơ lửng / đâm xuyên.
- Hỗ trợ cơ chế Mắt Thần Tự Kiểm Tra (setup_preview_render xuất _preview_render.png, _char_preview.png, _texture_3d_check.png).
"""

import bpy
import bmesh
import math
import os
import random
from mathutils import Vector, Matrix

# ==============================================================================
# 1. HỆ TRỤC TỌA ĐỘ GODOT <-> BLENDER
# ==============================================================================

def godot_to_blender_pos(gx, gy, gz):
    """
    Chuyển đổi vị trí từ Godot (X phải, Y lên, Z tới/nam) sang Blender (X phải, Y bắc, Z lên).
    Xuất glTF Y-Up: glTF.X = b.X, glTF.Y = b.Z, glTF.Z = -b.Y.
    """
    return (gx, -gz, gy)

def godot_to_blender_size(sx, sy, sz):
    """
    Chuyển đổi kích thước: sx (ngang X), sy (cao Y), sz (sâu Z).
    Blender: X = sx, Y = sz, Z = sy.
    """
    return (sx, sz, sy)

def clean_scene():
    """Xóa sạch scene và mesh rác trước khi dựng mô hình mới."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

# ==============================================================================
# 2. TRẢI UV TỰ ĐỘNG BẮT BUỘC (AUTO UV UNWRAP PROTOCOL)
# ==============================================================================

def unwrap_mesh(obj, project_type='cube', cube_size=1.0):
    """
    Bắt buộc trải UV tự động (cube_project hoặc smart_project) cho Mesh.
    Xóa bỏ hoàn toàn tình trạng mất UV hoặc bệt màu.
    """
    if obj is None or obj.type != 'MESH':
        return
    try:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        if project_type == 'smart':
            bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=0.02)
        else:
            bpy.ops.uv.cube_project(cube_size=cube_size)
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception as e:
        print(f"[blender_kit] unwrap_mesh warning on {obj.name}: {e}")
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass

# ==============================================================================
# 3. VẬT LIỆU & SHADING CÓ TEXTURE SEAMLESS
# ==============================================================================

def create_material(name, color, roughness=0.7, metallic=0.0, emission_color=None, emission_strength=0.0, texture_path=None):
    """Tạo vật liệu Principled BSDF hỗ trợ màu sắc, độ nhám, kim loại, phát sáng và Texture Image."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = (color[0], color[1], color[2], 1.0)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = (450, 0)
    
    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.location = (0, 0)
    node_bsdf.inputs['Base Color'].default_value = (color[0], color[1], color[2], 1.0)
    node_bsdf.inputs['Roughness'].default_value = roughness
    node_bsdf.inputs['Metallic'].default_value = metallic
    
    if texture_path and os.path.exists(texture_path):
        try:
            img = bpy.data.images.load(os.path.abspath(texture_path), check_existing=True)
            node_tex = nodes.new(type='ShaderNodeTexImage')
            node_tex.location = (-400, 0)
            node_tex.image = img
            mat.node_tree.links.new(node_tex.outputs['Color'], node_bsdf.inputs['Base Color'])
        except Exception as e:
            print(f"[blender_kit] Lỗi tải texture {texture_path}: {e}")
            
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

def apply_auto_smooth(obj, angle_deg=35.0):
    """Bật Shade Smooth và áp dụng góc làm mịn tự động."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    if hasattr(obj.data, "use_auto_smooth"):
        obj.data.use_auto_smooth = True
        obj.data.auto_smooth_angle = math.radians(angle_deg)
    else:
        mod = obj.modifiers.new(name="SmoothByAngle", type='NODES')
        try:
            bpy.ops.object.modifier_set_active(modifier="SmoothByAngle")
        except Exception:
            pass

def add_bevel_modifier(obj, width=0.035, segments=2):
    """Gắn Bevel Modifier từ 2-3 segments để bo viền bắt sáng đẹp mắt."""
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = width
    mod.segments = segments
    mod.limit_method = 'ANGLE'
    mod.angle_limit = math.radians(30.0)
    mod.use_clamp_overlap = True
    return mod

def add_solidify_modifier(obj, thickness=0.15):
    """Gắn Solidify Modifier tạo độ dày thực tế cho tường/mái."""
    mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod.thickness = thickness
    return mod

# ==============================================================================
# 4. CĂN CHỈNH TỰ ĐỘNG AABB (BOUNDING BOX HELPERS)
# ==============================================================================

def get_world_bounds(obj):
    """Tính toán hộp bao thế giới (min_bound, max_bound) của một vật thể."""
    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    min_b = Vector((min(c.x for c in corners), min(c.y for c in corners), min(c.z for c in corners)))
    max_b = Vector((max(c.x for c in corners), max(c.y for c in corners), max(c.z for c in corners)))
    return min_b, max_b

def snap_to_ground(obj, ground_z=0.0):
    """Dịch chuyển vật thể để đáy của nó tiếp đất chính xác tại cao độ ground_z (Blender Z)."""
    min_b, _ = get_world_bounds(obj)
    diff = ground_z - min_b.z
    obj.location.z += diff
    bpy.context.view_layer.update()

def stack_on_top(child_obj, base_obj, offset_z=0.0):
    """Đặt vật thể child_obj nằm chính xác trên đỉnh mặt trên của base_obj."""
    _, base_max = get_world_bounds(base_obj)
    snap_to_ground(child_obj, ground_z=base_max.z + offset_z)

# ==============================================================================
# 5. CÁC HÀM DỰNG HÌNH PROCEDURAL NÂNG CAO (BMESH BUILDERS)
# ==============================================================================

def create_beveled_box(name, size, location, bevel_width=0.04, rotation=(0, 0, 0), material=None, unwrap=True):
    """Tạo khối hộp có vát cạnh bắt sáng (Bevel) chuẩn tỷ lệ và trải UV tự động."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = godot_to_blender_size(*size)
    obj.location = godot_to_blender_pos(*location)
    obj.rotation_euler = (rotation[0], -rotation[2], rotation[1])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    if unwrap:
        unwrap_mesh(obj, project_type='cube', cube_size=1.0)
        
    if bevel_width > 0:
        add_bevel_modifier(obj, width=bevel_width, segments=2)
    apply_auto_smooth(obj)
    
    if material:
        obj.data.materials.append(material)
    return obj

def create_beveled_cylinder(name, radius, depth, location, bevel_width=0.02, rotation=(0, 0, 0), vertices=16, material=None, unwrap=True):
    """Tạo hình trụ thẳng đứng có bo cạnh trên/dưới và trải UV tự động."""
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
    
    if unwrap:
        unwrap_mesh(obj, project_type='cube', cube_size=1.0)
        
    if bevel_width > 0:
        add_bevel_modifier(obj, width=bevel_width, segments=2)
    apply_auto_smooth(obj, angle_deg=45.0)
    
    if material:
        obj.data.materials.append(material)
    return obj

def build_chamfered_rock(name, size, location, material=None, seed_val=42):
    """Dựng tảng đá tự nhiên vát cạnh Low-Poly phong cách Isometric và trải UV tự động."""
    random.seed(seed_val)
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)
    
    # Biến dạng tự nhiên các đỉnh (Vertex Displace)
    for v in bm.verts:
        jitter = Vector((
            random.uniform(-0.15, 0.15),
            random.uniform(-0.15, 0.15),
            random.uniform(-0.12, 0.12)
        ))
        v.co += jitter
        
    bmesh.ops.bevel(bm, geom=bm.edges[:] + bm.verts[:], offset=0.12, segments=1, profile=0.5)
    bm.to_mesh(mesh)
    bm.free()
    
    obj.scale = godot_to_blender_size(*size)
    obj.location = godot_to_blender_pos(*location)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    unwrap_mesh(obj, project_type='smart')
    apply_auto_smooth(obj, angle_deg=40.0)
    
    if material:
        obj.data.materials.append(material)
    return obj

def build_stylized_tree(name, location, scale=1.0, mat_wood=None, mat_foliage=None):
    """Dựng cây cách điệu nhiều tầng tán lá không bị trùng lặp khối."""
    gx, gy, gz = location
    trunk_h = 2.8 * scale
    trunk_r = 0.28 * scale
    
    # Thân cây vát nhẹ ở ngọn
    create_beveled_cylinder(f"{name}_Trunk", trunk_r, trunk_h, (gx, gy + trunk_h / 2, gz), bevel_width=0.03, material=mat_wood)
    
    # Tán lá tầng 1
    f1_r = 1.45 * scale
    f1_y = gy + trunk_h + 0.3 * scale
    f1 = build_chamfered_rock(f"{name}_Foliage1", (f1_r * 2, f1_r * 1.5, f1_r * 2), (gx, f1_y, gz), material=mat_foliage, seed_val=int(abs(gx) * 10 + 1))
    
    # Tán lá tầng 2 lệch nhẹ tự nhiên
    f2_r = 1.05 * scale
    f2_y = f1_y + 0.85 * scale
    f2 = build_chamfered_rock(f"{name}_Foliage2", (f2_r * 2, f2_r * 1.4, f2_r * 2), (gx + 0.18 * scale, f2_y, gz - 0.15 * scale), material=mat_foliage, seed_val=int(abs(gz) * 10 + 2))
    return f1, f2

def build_detailed_roof_gabled(name, width, length, height, center_pos, overhang=0.25, ridge_along_x=True, material=None):
    """
    Dựng mái ngói dốc 2 mái có riềm mái chìa ra ngoài (Overhang) và độ dày chân thực.
    """
    cx, cy, cz = center_pos
    hw = (width + overhang * 2) / 2.0
    hl = (length + overhang * 2) / 2.0
    
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    if ridge_along_x:
        g_verts = [
            (-hw, 0.0, -hl),
            (hw, 0.0, -hl),
            (hw, 0.0, hl),
            (-hw, 0.0, hl),
            (-hw, height, 0.0),
            (hw, height, 0.0)
        ]
        faces = [
            [0, 3, 4],
            [1, 5, 2],
            [0, 4, 5, 1],
            [3, 2, 5, 4],
            [0, 1, 2, 3]
        ]
    else:
        g_verts = [
            (-hw, 0.0, -hl),
            (hw, 0.0, -hl),
            (hw, 0.0, hl),
            (-hw, 0.0, hl),
            (0.0, height, -hl),
            (0.0, height, hl)
        ]
        faces = [
            [0, 4, 1],
            [3, 2, 5],
            [0, 3, 5, 4],
            [1, 4, 5, 2],
            [0, 1, 2, 3]
        ]
        
    b_verts = [Vector(godot_to_blender_pos(cx + vx, cy + vy, cz + vz)) for (vx, vy, vz) in g_verts]
    mesh.from_pydata(b_verts, [], faces)
    mesh.update()
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    unwrap_mesh(obj, project_type='cube', cube_size=1.0)
    add_bevel_modifier(obj, width=0.04, segments=2)
    apply_auto_smooth(obj, angle_deg=35.0)
    
    if material:
        obj.data.materials.append(material)
    return obj

# ==============================================================================
# 6. CƠ CHẾ MẮT THẦN TỰ KIỂM TRA (VISUAL PREVIEW RENDER)
# ==============================================================================

def setup_preview_render(output_path, resolution=(1280, 720), camera_pos=(-24, -4, 24), target_pos=(0, -22, 1), ortho_scale=46.0):
    """
    Thiết lập Camera Isometric + Ánh sáng mặt trời và render ảnh kiểm tra trực quan.
    Góc nhìn khớp chuẩn với Isometric Camera của Godot và ảnh mẫu modelyeucau/map2/1.jpg.
    """
    light_data = bpy.data.lights.new(name="PreviewSun", type='SUN')
    light_data.energy = 2.8
    light_data.color = (1.0, 0.97, 0.92)
    light_obj = bpy.data.objects.new(name="PreviewSun", object_data=light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = (-15, -10, 35)
    light_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(45))
    
    cam_data = bpy.data.cameras.new(name="PreviewCamera")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = ortho_scale
    cam_obj = bpy.data.objects.new(name="PreviewCamera", object_data=cam_data)
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
    
    abs_out = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)
    bpy.context.scene.render.filepath = abs_out
    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]
    
    print(f"Render ảnh mắt thần kiểm tra: {abs_out}")
    bpy.ops.render.render(write_still=True)
    print(f"Render hoàn tất: {os.path.exists(abs_out)}")
    return abs_out
