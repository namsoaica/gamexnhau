"""
Script Blender 3D: Dựng Cánh Cửa Gỗ Stylized (door_wooden.glb)
Dự án: Trò Chơi Mới - Antigravity Pipeline
Quy chuẩn:
- Kích thước: Rộng 1.2m, Cao 2.4m, Dày 0.12m.
- Tâm xoay (Pivot/Origin): Đặt chính xác tại mép bản lề xoay (X = 0.0, Y = 0.0, Z = 0.0).
- 4 tấm ván gỗ beveled bo cạnh bắt sáng, 2 nẹp sắt rèn ngang có đinh tán, tay nắm vòng sắt, bản lề trục xoay.
- Gán vật liệu liên kết Assets/Textures/Tileable/tex_door_wood.png và tex_metal_seamless.png.
- Trải UV khớp chuẩn tỉ lệ (U: 0->1.2m, V: 0->2.4m) để texture không bị lặp vạch thừa.
- Tích hợp collider '-col' cho Godot 4.
- Xuất GLB 'Assets/Models/door_wooden.glb', lưu 'Assets/Blender_Source/door_wooden.blend'.
- Render ảnh mắt thần 'Assets/Models/_door_preview.png' hiển thị cả mặt trước (Front) và mặt sau (Back).
"""

import sys
import os
import bpy
import bmesh
import math
from mathutils import Vector, Matrix, Euler

cur_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.abspath(os.path.join(cur_dir, ".."))
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from tools.blender_kit import (
    clean_scene,
    create_material,
    apply_auto_smooth
)

def make_trans_mat(pos, rot_euler=None):
    mat = Matrix.Translation(Vector(pos))
    if rot_euler:
        mat = mat @ Euler(rot_euler).to_matrix().to_4x4()
    return mat

def create_beveled_cube_mesh(bm, size, center, bevel_offset=0.015):
    """Tạo cube trong bmesh và bevel cạnh trực tiếp."""
    sx, sy, sz = size
    cx, cy, cz = center
    geom = bmesh.ops.create_cube(bm, size=1.0)
    verts = geom['verts']
    for v in verts:
        v.co.x = cx + v.co.x * sx
        v.co.y = cy + v.co.y * sy
        v.co.z = cz + v.co.z * sz
    if bevel_offset > 0:
        edges = [e for e in bm.edges if any(v in verts for v in e.verts)]
        bmesh.ops.bevel(bm, geom=edges, offset=bevel_offset, segments=2, profile=0.5)

def build_door():
    print("=== BẮT ĐẦU DỰNG CÁNH CỬA GỖ STYLIZED (DOOR WOODEN) ===")
    clean_scene()

    tex_dir = os.path.join(workspace_dir, "Assets", "Textures", "Tileable")
    p_door_wood = os.path.join(tex_dir, "tex_door_wood.png")
    p_metal = os.path.join(tex_dir, "tex_metal_seamless.png")

    mat_wood = create_material("Mat_Door_Wood", (0.55, 0.35, 0.20), roughness=0.75, texture_path=p_door_wood)
    mat_metal = create_material("Mat_Door_Iron", (0.32, 0.34, 0.38), roughness=0.40, metallic=0.88, texture_path=p_metal)
    mat_rivet = create_material("Mat_Door_Rivet", (0.24, 0.25, 0.28), roughness=0.35, metallic=0.90)

    door_w = 1.20
    door_h = 2.40
    plank_count = 4
    plank_pitch = door_w / plank_count # 0.30m
    plank_w = 0.292
    plank_th = 0.075
    back_y = -plank_th / 2.0 - 0.014
    front_strap_y = plank_th / 2.0 + 0.008

    # Vị trí chuẩn của 2 nẹp sắt khớp hoàn hảo với texture tex_door_wood.png
    strap_bot_z = 0.43
    strap_top_z = 1.95

    # =========================================================================
    # 1. TẠO MESH GỖ (WOOD PARTS)
    # =========================================================================
    mesh_wood = bpy.data.meshes.new("Door_Wood_Mesh")
    bm_wood = bmesh.new()

    for i in range(plank_count):
        cx = i * plank_pitch + plank_pitch / 2.0
        create_beveled_cube_mesh(bm_wood, (plank_w, plank_th, door_h - 0.02), (cx, 0.0, door_h / 2.0), bevel_offset=0.014)

    for bz in [strap_bot_z, strap_top_z]:
        create_beveled_cube_mesh(bm_wood, (door_w - 0.06, 0.024, 0.13), (door_w / 2.0, back_y, bz), bevel_offset=0.010)

    diag_cx = door_w / 2.0
    diag_cz = (strap_bot_z + strap_top_z) / 2.0
    diag_len = math.sqrt((door_w - 0.1)**2 + (strap_top_z - strap_bot_z)**2)
    diag_angle = math.atan2(strap_top_z - strap_bot_z, door_w - 0.1)

    geom_diag = bmesh.ops.create_cube(bm_wood, size=1.0)
    for v in geom_diag['verts']:
        vx = v.co.x * diag_len
        vy = v.co.y * 0.022
        vz = v.co.z * 0.11
        cos_a = math.cos(-diag_angle)
        sin_a = math.sin(-diag_angle)
        rx = vx * cos_a + vz * sin_a
        rz = -vx * sin_a + vz * cos_a
        v.co.x = diag_cx + rx
        v.co.y = back_y + vy
        v.co.z = diag_cz + rz

    edges_diag = [e for e in bm_wood.edges if any(v in geom_diag['verts'] for v in e.verts)]
    bmesh.ops.bevel(bm_wood, geom=edges_diag, offset=0.010, segments=2, profile=0.5)

    bm_wood.to_mesh(mesh_wood)
    bm_wood.free()

    obj_wood = bpy.data.objects.new("Door_Wood_Part", mesh_wood)
    bpy.context.collection.objects.link(obj_wood)
    apply_auto_smooth(obj_wood, angle_deg=35.0)
    obj_wood.data.materials.append(mat_wood)

    # =========================================================================
    # 2. TẠO MESH KIM LOẠI (METAL PARTS: Straps, Hinges, Handle Plate)
    # =========================================================================
    mesh_metal = bpy.data.meshes.new("Door_Metal_Mesh")
    bm_metal = bmesh.new()

    for sz in [strap_bot_z, strap_top_z]:
        create_beveled_cube_mesh(bm_metal, (door_w - 0.04, 0.016, 0.11), (door_w / 2.0, front_strap_y, sz), bevel_offset=0.008)

    handle_x = door_w - 0.16
    handle_z = 1.10
    create_beveled_cube_mesh(bm_metal, (0.09, 0.014, 0.26), (handle_x, front_strap_y, handle_z), bevel_offset=0.006)

    for hz in [strap_bot_z, strap_top_z]:
        bmesh.ops.create_cone(
            bm_metal,
            cap_ends=True,
            cap_tris=False,
            segments=16,
            radius1=0.034,
            radius2=0.034,
            depth=0.18,
            matrix=make_trans_mat((0.015, 0.0, hz))
        )

    bmesh.ops.create_cone(
        bm_metal,
        cap_ends=True,
        cap_tris=False,
        segments=12,
        radius1=0.018,
        radius2=0.018,
        depth=0.035,
        matrix=make_trans_mat((handle_x, front_strap_y + 0.022, handle_z + 0.04), (math.radians(90), 0, 0))
    )

    ring_r = 0.055
    ring_tube = 0.012
    ring_segs = 18
    tube_segs = 8
    ring_cx = handle_x
    ring_cy = front_strap_y + 0.035
    ring_cz = handle_z - 0.02

    ring_verts = []
    for i in range(ring_segs):
        theta = 2.0 * math.pi * i / ring_segs
        for j in range(tube_segs):
            phi = 2.0 * math.pi * j / tube_segs
            tx = (ring_r + ring_tube * math.cos(phi)) * math.cos(theta)
            ty = ring_tube * math.sin(phi)
            tz = (ring_r + ring_tube * math.cos(phi)) * math.sin(theta)
            v = bm_metal.verts.new((ring_cx + tx, ring_cy + ty - tz * 0.15, ring_cz + tz))
            ring_verts.append(v)

    bm_metal.verts.ensure_lookup_table()
    for i in range(ring_segs):
        next_i = (i + 1) % ring_segs
        for j in range(tube_segs):
            next_j = (j + 1) % tube_segs
            v1 = ring_verts[i * tube_segs + j]
            v2 = ring_verts[next_i * tube_segs + j]
            v3 = ring_verts[next_i * tube_segs + next_j]
            v4 = ring_verts[i * tube_segs + next_j]
            bm_metal.faces.new((v1, v2, v3, v4))

    bmesh.ops.create_cone(
        bm_metal,
        cap_ends=True,
        cap_tris=False,
        segments=14,
        radius1=0.032,
        radius2=0.020,
        depth=0.04,
        matrix=make_trans_mat((handle_x, back_y - 0.020, handle_z), (math.radians(90), 0, 0))
    )

    bm_metal.to_mesh(mesh_metal)
    bm_metal.free()

    obj_metal = bpy.data.objects.new("Door_Metal_Part", mesh_metal)
    bpy.context.collection.objects.link(obj_metal)
    apply_auto_smooth(obj_metal, angle_deg=40.0)
    obj_metal.data.materials.append(mat_metal)

    # =========================================================================
    # 3. TẠO MESH ĐINH TÁN (RIVETS & PINS)
    # =========================================================================
    mesh_rivet = bpy.data.meshes.new("Door_Rivet_Mesh")
    bm_rivet = bmesh.new()

    for sz in [strap_bot_z, strap_top_z]:
        for p in range(plank_count):
            rx = p * plank_pitch + plank_pitch / 2.0
            bmesh.ops.create_cone(
                bm_rivet,
                cap_ends=True,
                segments=10,
                radius1=0.022,
                radius2=0.012,
                depth=0.018,
                matrix=make_trans_mat((rx, front_strap_y + 0.010, sz), (math.radians(90), 0, 0))
            )
            bmesh.ops.create_cone(
                bm_rivet,
                cap_ends=True,
                segments=10,
                radius1=0.020,
                radius2=0.010,
                depth=0.018,
                matrix=make_trans_mat((rx, back_y - 0.014, sz), (math.radians(90), 0, 0))
            )

    for hz in [strap_bot_z, strap_top_z]:
        bmesh.ops.create_cone(
            bm_rivet,
            cap_ends=True,
            segments=12,
            radius1=0.018,
            radius2=0.018,
            depth=0.22,
            matrix=make_trans_mat((0.015, 0.0, hz))
        )

    bmesh.ops.create_cone(
        bm_rivet,
        cap_ends=True,
        segments=8,
        radius1=0.010,
        radius2=0.006,
        depth=0.020,
        matrix=make_trans_mat((handle_x, front_strap_y + 0.012, handle_z - 0.06), (math.radians(90), 0, 0))
    )

    bm_rivet.to_mesh(mesh_rivet)
    bm_rivet.free()

    obj_rivet = bpy.data.objects.new("Door_Rivet_Part", mesh_rivet)
    bpy.context.collection.objects.link(obj_rivet)
    apply_auto_smooth(obj_rivet, angle_deg=45.0)
    obj_rivet.data.materials.append(mat_rivet)

    # =========================================================================
    # 4. HỢP NHẤT THÀNH 'door_wooden-col' VỚI ORIGIN TẠI (0,0,0)
    # =========================================================================
    bpy.ops.object.select_all(action='DESELECT')
    obj_wood.select_set(True)
    obj_metal.select_set(True)
    obj_rivet.select_set(True)
    bpy.context.view_layer.objects.active = obj_wood
    bpy.ops.object.join()

    main_door = bpy.context.active_object
    main_door.name = "door_wooden-col"

    # Trải UV chuẩn xác 100%: Cube project theo chiều cao cửa (2.4m)
    # để texture lặp đúng 1 lần từ chân lên đỉnh
    bpy.context.view_layer.objects.active = main_door
    main_door.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=door_h, correct_aspect=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    uvl = main_door.data.uv_layers[0]
    for d in uvl.data:
        # Scale U từ [0.25, 0.75] -> [0.0, 1.0] để khớp 4 tấm ván
        d.uv[0] = (d.uv[0] - 0.25) * 2.0

    # Đặt Tâm Xoay (Pivot / Origin) chính xác tại mép bản lề (0.0, 0.0, 0.0)
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    print(f"Cánh cửa gỗ hợp nhất thành công: '{main_door.name}', Origin = (0,0,0).")

    # =========================================================================
    # 5. XUẤT RA GLB & LƯU FILE BLEND AN TOÀN TRƯỚC KHI TẠO SCENE PREVIEW
    # =========================================================================
    out_glb = os.path.join(workspace_dir, "Assets", "Models", "door_wooden.glb")
    print(f"Xuất mô hình sang: {out_glb}")
    bpy.ops.export_scene.gltf(
        filepath=out_glb,
        export_format='GLB',
        export_yup=True,
        export_apply=True,
        export_materials='EXPORT'
    )

    blend_path = os.path.join(workspace_dir, "Assets", "Blender_Source", "door_wooden.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Lưu file blend: {blend_path}")

    # =========================================================================
    # 6. RENDER ẢNH MẮT THẦN TỰ KIỂM TRA (_door_preview.png)
    # Cửa 1 (Bên trái): X in [0.0, 1.2] - Mặt trước (Front)
    # Cửa 2 (Bên phải): X in [1.6, 2.8] - Mặt sau (Back) xoay 180 độ
    # =========================================================================
    bpy.ops.object.select_all(action='DESELECT')
    main_door.select_set(True)
    bpy.context.view_layer.objects.active = main_door
    bpy.ops.object.duplicate()
    back_door = bpy.context.active_object
    back_door.name = "door_preview_back_only"
    back_door.rotation_euler = (0, 0, math.radians(180))
    back_door.location = (2.8, 0.0, 0.0)

    light_data = bpy.data.lights.new(name="DoorSun", type='SUN')
    light_data.energy = 3.2
    light_data.color = (1.0, 0.96, 0.90)
    light_obj = bpy.data.objects.new(name="DoorSun", object_data=light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = (-2, 5, 5)
    light_obj.rotation_euler = (math.radians(55), math.radians(10), math.radians(25))

    fill_data = bpy.data.lights.new(name="DoorFill", type='SUN')
    fill_data.energy = 1.4
    fill_data.color = (0.80, 0.88, 1.0)
    fill_obj = bpy.data.objects.new(name="DoorFill", object_data=fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (4, -4, 3)
    fill_obj.rotation_euler = (math.radians(-35), math.radians(30), math.radians(-50))

    cam_data = bpy.data.cameras.new(name="DoorCam")
    cam_data.type = 'PERSP'
    cam_data.lens = 45
    cam_obj = bpy.data.objects.new(name="DoorCam", object_data=cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    cam_obj.location = (1.4, 5.8, 1.20)
    direction = Vector((1.4, 0.0, 1.20)) - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
    bpy.context.scene.display.shading.color_type = 'TEXTURE'
    bpy.context.scene.display.shading.show_cavity = True
    bpy.context.scene.display.shading.cavity_type = 'BOTH'
    bpy.context.scene.display.shading.cavity_ridge_factor = 2.5
    bpy.context.scene.display.shading.cavity_valley_factor = 1.5

    out_preview = os.path.join(workspace_dir, "Assets", "Models", "_door_preview.png")
    bpy.context.scene.render.filepath = os.path.abspath(out_preview)
    bpy.context.scene.render.resolution_x = 1280
    bpy.context.scene.render.resolution_y = 800

    print(f"Render ảnh mắt thần cánh cửa đôi: {out_preview}")
    bpy.ops.render.render(write_still=True)

    print("=== DỰNG CÁNH CỬA GỖ HOÀN TẤT ===")

if __name__ == '__main__':
    build_door()
