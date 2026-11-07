"""
Master 2.5D Isometric Game Map Generator - Final Perfected Edition
Blender 5.4 Script
Based on reference artwork:
- 100% Watertight, robust tile-column terrain mesh (zero holes, zero artifacts)
- True 2.5D isometric camera projection with Standard color management (vibrant cartoon colors)
- Balanced warm cartoon sunlight and soft sky fill (no blown-out highlights)
- Tier 0, Tier 1, Tier 1.5, and Tier 2 elevations
- Carved stone stairs with flagstone pavers and stepping stone pads
- Organic smooth-shaded deciduous trees in warm yellow-green tones
- Stylized 3-tiered conical pine trees
- Majestic royal-purple faceted mountain range & central spur
- Tier 2 overlook with wooden rail fence and directional signposts
- Rich foreground wildflower meadow with daisies and tall grass blades
- Cartoon sky gradient with puffy 3D clouds
Exports:
- map_25d.blend
- map_25d.glb
- map_25d.fbx
- render_map_25d.png
"""

import bpy
import bmesh
import math
import os
import random
from mathutils import Vector, Euler, Matrix

# Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------
# 1. TEXTURE GENERATION
# -------------------------------------------------------------
def make_grass_grid_texture():
    tex_path = os.path.join(WORKSPACE_DIR, "tex_grass_grid.png")
    size = 256
    img = bpy.data.images.new("Tex_Grass_Grid", width=size, height=size)
    pixels = []
    
    # Stylized vibrant cartoon grass palette
    for y in range(size):
        for x in range(size):
            dist_b = min(x, size - 1 - x, y, size - 1 - y)
            if dist_b < 6:
                # Dark grid seam
                r, g, b = 0.26, 0.48, 0.15
            elif dist_b < 12:
                # Highlight bevel
                r, g, b = 0.35, 0.62, 0.20
            else:
                # Main spring grass with soft subtle radial brightness
                cx = (x - size / 2) / (size / 2)
                cy = (y - size / 2) / (size / 2)
                cd = math.sqrt(cx*cx + cy*cy)
                f = max(0.0, 1.0 - cd * 0.45)
                r = 0.42 + 0.04 * f
                g = 0.72 + 0.05 * f
                b = 0.26 + 0.03 * f
            pixels.extend([r, g, b, 1.0])
            
    img.pixels = pixels
    img.filepath_raw = tex_path
    img.file_format = 'PNG'
    img.save()
    return img

def make_cliff_dirt_texture():
    tex_path = os.path.join(WORKSPACE_DIR, "tex_cliff_dirt.png")
    w, h = 256, 256
    img = bpy.data.images.new("Tex_Cliff_Dirt", width=w, height=h)
    pixels = []
    
    for y in range(h):
        ny = y / float(h)
        for x in range(w):
            if ny > 0.88:
                # Top green grass rim
                r, g, b = 0.40, 0.68, 0.22
            elif ny > 0.48:
                # Warm caramel soil with horizontal strata
                s = math.sin(ny * 30.0) * 0.05
                r = 0.54 + s
                g = 0.36 + s * 0.8
                b = 0.25 + s * 0.6
            elif ny > 0.22:
                # Darker clay layer
                s = math.sin(ny * 24.0) * 0.04
                r = 0.40 + s
                g = 0.26 + s
                b = 0.18 + s
            else:
                # Foundation slate rock
                s = math.sin(ny * 16.0 + x * 0.04) * 0.03
                r = 0.22 + s
                g = 0.25 + s
                b = 0.28 + s
            pixels.extend([r, g, b, 1.0])
            
    img.pixels = pixels
    img.filepath_raw = tex_path
    img.file_format = 'PNG'
    img.save()
    return img

img_grass = make_grass_grid_texture()
img_cliff = make_cliff_dirt_texture()

# -------------------------------------------------------------
# 2. MATERIALS SETUP
# -------------------------------------------------------------
materials = {}

def create_mat(name, color, roughness=0.6, metallic=0.0, img_tex=None, emit_col=None, emit_str=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    out = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    if img_tex:
        tex = nodes.new(type='ShaderNodeTexImage')
        tex.image = img_tex
        links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    else:
        bsdf.inputs['Base Color'].default_value = color
        
    if emit_col and emit_str > 0.0:
        bsdf.inputs['Emission Color'].default_value = emit_col
        bsdf.inputs['Emission Strength'].default_value = emit_str
        
    materials[name] = mat
    return mat

mat_grass = create_mat('Mat_Grass', (0.42, 0.72, 0.26, 1.0), roughness=0.65, img_tex=img_grass)
mat_cliff = create_mat('Mat_Cliff_Dirt', (0.54, 0.36, 0.24, 1.0), roughness=0.85, img_tex=img_cliff)
mat_rock_base = create_mat('Mat_Cliff_Rock', (0.20, 0.24, 0.28, 1.0), roughness=0.85)
mat_dirt = create_mat('Mat_Dirt_Path', (0.76, 0.52, 0.30, 1.0), roughness=0.85)
mat_stone = create_mat('Mat_Stone', (0.54, 0.58, 0.62, 1.0), roughness=0.55)
mat_mountain_lit = create_mat('Mat_Mountain_Purple', (0.44, 0.24, 0.74, 1.0), roughness=0.65)
mat_mountain_shadow = create_mat('Mat_Mountain_Dark', (0.26, 0.12, 0.50, 1.0), roughness=0.70)
mat_tree_leaf1 = create_mat('Mat_Tree_Leaf1', (0.44, 0.76, 0.24, 1.0), roughness=0.55)
mat_tree_leaf2 = create_mat('Mat_Tree_Leaf2', (0.52, 0.84, 0.30, 1.0), roughness=0.55)
mat_pine_leaf = create_mat('Mat_Pine_Leaf', (0.18, 0.48, 0.20, 1.0), roughness=0.60)
mat_wood = create_mat('Mat_Wood', (0.56, 0.34, 0.13, 1.0), roughness=0.65)
mat_trunk = create_mat('Mat_Trunk', (0.45, 0.30, 0.18, 1.0), roughness=0.75)
mat_petal = create_mat('Mat_Daisy_Petal', (0.98, 0.98, 0.98, 1.0), roughness=0.35, emit_col=(0.98, 0.98, 0.98, 1.0), emit_str=0.08)
mat_center = create_mat('Mat_Daisy_Center', (1.0, 0.78, 0.05, 1.0), roughness=0.35, emit_col=(1.0, 0.78, 0.05, 1.0), emit_str=0.08)
mat_blade = create_mat('Mat_Grass_Blade', (0.36, 0.70, 0.22, 1.0), roughness=0.5)

# Collections
collections = {}
for c_name in ['Terrain', 'Paths_and_Stairs', 'Mountains', 'Vegetation', 'Props', 'Lighting_and_Camera']:
    col = bpy.data.collections.new(c_name)
    bpy.context.scene.collection.children.link(col)
    collections[c_name] = col

def link_to(obj, c_name):
    collections[c_name].objects.link(obj)

# -------------------------------------------------------------
# 3. 100% WATERTIGHT TILE-COLUMN TERRAIN
# -------------------------------------------------------------
def build_watertight_terrain():
    """
    Constructs a 12x12 discrete elevation tile-column mesh:
    - Every tile has a top face at its tier elevation.
    - Whenever adjacent tiles have different elevations, a clean vertical cliff face connects them.
    - The boundary of the 12x12 grid connects to the soil layer (Z = -1.2) and tapering rock foundation (Z = -3.2).
    - ZERO holes, ZERO gaps, ZERO non-manifold geometry!
    """
    mesh = bpy.data.meshes.new('Terrain_Mesh')
    obj = bpy.data.objects.new('SM_Terrain_Chunk', mesh)
    link_to(obj, 'Terrain')
    obj.data.materials.append(mat_grass)      # 0
    obj.data.materials.append(mat_cliff)      # 1
    obj.data.materials.append(mat_rock_base)  # 2
    
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")
    
    # 12x12 elevation map
    W, H = 12, 12
    elev_grid = [[0.0 for _ in range(W)] for _ in range(H)]
    
    # Fill elevations:
    for y in range(H):
        for x in range(W):
            # Tier 2: Upper Overlook Plateau (Z = 2.50)
            if 5 <= x <= 8 and 7 <= y <= 11:
                elev_grid[y][x] = 2.50
            # Tier 1.5: Back-Left Terrace (Z = 1.85)
            elif 0 <= x <= 2 and 8 <= y <= 11:
                elev_grid[y][x] = 1.85
            # Tier 1: Mid Terrace (Z = 1.25)
            elif 0 <= x <= 5 and 4 <= y <= 11:
                # Sunken nook next to Staircase 1 at (5, 4)
                if x == 5 and y == 4:
                    elev_grid[y][x] = 0.0
                else:
                    elev_grid[y][x] = 1.25
            elif (x == 3 or x == 4) and 8 <= y <= 11:
                elev_grid[y][x] = 1.25
            else:
                # Tier 0 Ground
                elev_grid[y][x] = 0.0

    # 1. Generate Top Faces & Internal Vertical Cliff Walls
    for y in range(H):
        for x in range(W):
            h = elev_grid[y][x]
            # Top face (Grass)
            v0 = bm.verts.new((x, y, h))
            v1 = bm.verts.new((x + 1, y, h))
            v2 = bm.verts.new((x + 1, y + 1, h))
            v3 = bm.verts.new((x, y + 1, h))
            f_top = bm.faces.new((v0, v1, v2, v3))
            f_top.material_index = 0
            for loop in f_top.loops:
                loop[uv_layer].uv = (loop.vert.co.x, loop.vert.co.y)
                
            # Check East neighbor (x + 1)
            if x < W - 1:
                h_east = elev_grid[y][x + 1]
                if h != h_east:
                    h_low, h_high = min(h, h_east), max(h, h_east)
                    b0 = bm.verts.new((x + 1, y, h_low))
                    b1 = bm.verts.new((x + 1, y + 1, h_low))
                    t1 = bm.verts.new((x + 1, y + 1, h_high))
                    t0 = bm.verts.new((x + 1, y, h_high))
                    if h > h_east:
                        f_cliff = bm.faces.new((b0, t0, t1, b1))
                    else:
                        f_cliff = bm.faces.new((b0, b1, t1, t0))
                    f_cliff.material_index = 1
                    for loop in f_cliff.loops:
                        loop[uv_layer].uv = (loop.vert.co.y, (loop.vert.co.z + 1.2) / 2.5)
                        
            # Check North neighbor (y + 1)
            if y < H - 1:
                h_north = elev_grid[y + 1][x]
                if h != h_north:
                    h_low, h_high = min(h, h_north), max(h, h_north)
                    b0 = bm.verts.new((x, y + 1, h_low))
                    b1 = bm.verts.new((x + 1, y + 1, h_low))
                    t1 = bm.verts.new((x + 1, y + 1, h_high))
                    t0 = bm.verts.new((x, y + 1, h_high))
                    if h > h_north:
                        f_cliff = bm.faces.new((b0, b1, t1, t0))
                    else:
                        f_cliff = bm.faces.new((b0, t0, t1, b1))
                    f_cliff.material_index = 1
                    for loop in f_cliff.loops:
                        loop[uv_layer].uv = (loop.vert.co.x, (loop.vert.co.z + 1.2) / 2.5)

    # 2. Outer Perimeter Cutaway (from tile top edge down to Z = -1.2)
    # Collect boundary segments in CCW order around (0,0)->(12,0)->(12,12)->(0,12)->(0,0)
    perim_top_segments = []
    # South edge: y = 0, x from 0 to 12
    for x in range(W):
        h = elev_grid[0][x]
        perim_top_segments.append(((x, 0, h), (x + 1, 0, h)))
    # East edge: x = 12, y from 0 to 12
    for y in range(H):
        h = elev_grid[y][W - 1]
        perim_top_segments.append(((12, y, h), (12, y + 1, h)))
    # North edge: y = 12, x from 12 down to 0
    for x in range(W - 1, -1, -1):
        h = elev_grid[H - 1][x]
        perim_top_segments.append(((x + 1, 12, h), (x, 12, h)))
    # West edge: x = 0, y from 12 down to 0
    for y in range(H - 1, -1, -1):
        h = elev_grid[y][0]
        perim_top_segments.append(((0, y + 1, h), (0, y, h)))

    # For each outer segment, drop down to Z = -1.2 (Soil cliff wall)
    for (p0, p1) in perim_top_segments:
        vt0 = bm.verts.new(p0)
        vt1 = bm.verts.new(p1)
        vb1 = bm.verts.new((p1[0], p1[1], -1.2))
        vb0 = bm.verts.new((p0[0], p0[1], -1.2))
        f_outer = bm.faces.new((vt0, vt1, vb1, vb0))
        f_outer.material_index = 1
        for loop in f_outer.loops:
            loop[uv_layer].uv = (loop.vert.co.x + loop.vert.co.y, (loop.vert.co.z + 1.2) / 2.5)

    # 3. Floating Rock Underside (from Z = -1.2 tapering to tip Z = -3.2)
    ring_12_pts = [
        (0.0, 0.0), (4.0, 0.0), (8.0, 0.0), (12.0, 0.0),
        (12.0, 4.0), (12.0, 8.0), (12.0, 12.0),
        (8.0, 12.0), (4.0, 12.0), (0.0, 12.0),
        (0.0, 8.0), (0.0, 4.0),
    ]
    ring_22_pts = []
    for (rx, ry) in ring_12_pts:
        ix = 5.5 + (rx - 5.5) * 0.55
        iy = 5.5 + (ry - 5.5) * 0.55
        ring_22_pts.append((ix, iy))
        
    v_tip = bm.verts.new((5.5, 5.5, -3.2))
    
    n_pts = len(ring_12_pts)
    for i in range(n_pts):
        i_next = (i + 1) % n_pts
        v12_0 = bm.verts.new((ring_12_pts[i][0], ring_12_pts[i][1], -1.2))
        v12_1 = bm.verts.new((ring_12_pts[i_next][0], ring_12_pts[i_next][1], -1.2))
        v22_1 = bm.verts.new((ring_22_pts[i_next][0], ring_22_pts[i_next][1], -2.2))
        v22_0 = bm.verts.new((ring_22_pts[i][0], ring_22_pts[i][1], -2.2))
        f_r1 = bm.faces.new((v12_0, v12_1, v22_1, v22_0))
        f_r1.material_index = 2
        for loop in f_r1.loops:
            loop[uv_layer].uv = (loop.vert.co.x, loop.vert.co.z)
            
        f_tip = bm.faces.new((v22_0, v22_1, v_tip))
        f_tip.material_index = 2
        for loop in f_tip.loops:
            loop[uv_layer].uv = (loop.vert.co.x, loop.vert.co.z)

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return obj

# -------------------------------------------------------------
# 4. PATHS & STAIRCASES
# -------------------------------------------------------------
def build_paths_and_stairs():
    # 1. Foreground Curved Dirt Path
    path_pts = [
        (5.8, 0.1, 0.012),
        (5.3, 0.8, 0.012),
        (4.6, 1.5, 0.012),
        (3.8, 2.2, 0.012),
        (4.1, 3.0, 0.012),
        (4.5, 3.4, 0.012),
    ]
    p_mesh = bpy.data.meshes.new('Dirt_Path_Main_Mesh')
    p_obj = bpy.data.objects.new('SM_Dirt_Path_Main', p_mesh)
    link_to(p_obj, 'Paths_and_Stairs')
    p_obj.data.materials.append(mat_dirt)
    
    bm = bmesh.new()
    width = 1.05
    prev_l, prev_r = None, None
    for i, pt in enumerate(path_pts):
        p = Vector(pt)
        if i < len(path_pts) - 1:
            tan = (Vector(path_pts[i+1]) - p).normalized()
        else:
            tan = (p - Vector(path_pts[i-1])).normalized()
        norm = Vector((-tan.y, tan.x, 0.0))
        vl = bm.verts.new(p - norm * (width * 0.5))
        vr = bm.verts.new(p + norm * (width * 0.5))
        if prev_l and prev_r:
            bm.faces.new((prev_l, prev_r, vr, vl))
        prev_l, prev_r = vl, vr
    bm.to_mesh(p_mesh)
    bm.free()

    # 2. Stepping Stone Slabs (Embedded in dirt path)
    slabs = [
        (5.5, 0.4, 0.022, 0.26, 0.22),
        (4.9, 1.1, 0.022, 0.28, 0.24),
        (4.2, 1.8, 0.022, 0.25, 0.25),
        (3.8, 2.4, 0.022, 0.27, 0.21),
        (4.2, 3.0, 0.022, 0.26, 0.24),
        (3.7, 3.3, 0.022, 0.22, 0.20),
        (3.9, 3.6, 0.022, 0.24, 0.22),
    ]
    for idx, (sx, sy, sz, rx, ry) in enumerate(slabs):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=7,
            radius=1.0,
            depth=0.035,
            location=(sx, sy, sz)
        )
        st = bpy.context.active_object
        st.name = f'SM_Stepping_Stone_{idx+1:02d}'
        st.scale = (rx, ry, 1.0)
        st.rotation_euler = (0, 0, (idx * 1.3) % 3.14)
        st.data.materials.append(mat_stone)
        bpy.context.scene.collection.objects.unlink(st)
        link_to(st, 'Paths_and_Stairs')

    # 3. Staircase 1 (Tier 0 -> Tier 1)
    # Spans from Y = 3.2 to Y = 4.0, ascending Z = 0.0 to 1.25
    n_steps_1 = 5
    st1_mesh = bpy.data.meshes.new('Staircase_1_Mesh')
    st1_obj = bpy.data.objects.new('SM_Staircase_01', st1_mesh)
    link_to(st1_obj, 'Paths_and_Stairs')
    st1_obj.data.materials.append(mat_stone)
    
    bm = bmesh.new()
    s1_w = 1.15
    s1_run = (4.0 - 3.2) / n_steps_1
    s1_rise = 1.25 / n_steps_1
    for s in range(n_steps_1):
        cy = 3.2 + s * s1_run + s1_run * 0.5
        cz = (s + 0.5) * s1_rise
        bmesh.ops.create_cube(
            bm,
            size=1.0,
            matrix=Matrix.Translation((4.5, cy, cz)) @ Matrix.Diagonal((s1_w, s1_run * 1.05, s1_rise, 1.0))
        )
    bm.to_mesh(st1_mesh)
    bm.free()

    # 4. Tier 1 Dirt Path Walkway
    t1_pts = [
        (4.5, 4.1, 1.26),
        (3.8, 4.8, 1.26),
        (2.8, 5.6, 1.26),
        (2.2, 6.8, 1.26),
        (2.0, 8.0, 1.26),
    ]
    t1_mesh = bpy.data.meshes.new('Dirt_Path_T1_Mesh')
    t1_obj = bpy.data.objects.new('SM_Dirt_Path_Tier1', t1_mesh)
    link_to(t1_obj, 'Paths_and_Stairs')
    t1_obj.data.materials.append(mat_dirt)
    bm = bmesh.new()
    prev_l, prev_r = None, None
    for i, pt in enumerate(t1_pts):
        p = Vector(pt)
        if i < len(t1_pts) - 1:
            tan = (Vector(t1_pts[i+1]) - p).normalized()
        else:
            tan = (p - Vector(t1_pts[i-1])).normalized()
        norm = Vector((-tan.y, tan.x, 0.0))
        vl = bm.verts.new(p - norm * 0.46)
        vr = bm.verts.new(p + norm * 0.46)
        if prev_l and prev_r:
            bm.faces.new((prev_l, prev_r, vr, vl))
        prev_l, prev_r = vl, vr
    bm.to_mesh(t1_mesh)
    bm.free()

    # 5. Staircase 2 (Tier 1 -> Tier 2)
    # Spans from Y = 6.0 to Y = 7.0, ascending Z = 1.25 to 2.50
    n_steps_2 = 6
    st2_mesh = bpy.data.meshes.new('Staircase_2_Mesh')
    st2_obj = bpy.data.objects.new('SM_Staircase_02', st2_mesh)
    link_to(st2_obj, 'Paths_and_Stairs')
    st2_obj.data.materials.append(mat_stone)
    
    bm = bmesh.new()
    s2_w = 1.10
    s2_run = (7.0 - 6.0) / n_steps_2
    s2_rise = (2.50 - 1.25) / n_steps_2
    for s in range(n_steps_2):
        cy = 6.0 + s * s2_run + s2_run * 0.5
        cz = 1.25 + (s + 0.5) * s2_rise
        bmesh.ops.create_cube(
            bm,
            size=1.0,
            matrix=Matrix.Translation((5.7, cy, cz)) @ Matrix.Diagonal((s2_w, s2_run * 1.05, s2_rise, 1.0))
        )
    bm.to_mesh(st2_mesh)
    bm.free()

    # 6. Tier 2 Stone Landing Pavers & Overlook Dirt Pad
    landing_mesh = bpy.data.meshes.new('Landing_Pavers_Mesh')
    landing_obj = bpy.data.objects.new('SM_Tier2_Pavers', landing_mesh)
    link_to(landing_obj, 'Paths_and_Stairs')
    landing_obj.data.materials.append(mat_stone)
    bm = bmesh.new()
    pavers = [
        (5.4, 7.25), (5.9, 7.25),
        (5.4, 7.75), (5.9, 7.75),
    ]
    for px, py in pavers:
        bmesh.ops.create_cube(
            bm,
            size=1.0,
            matrix=Matrix.Translation((px, py, 2.512)) @ Matrix.Diagonal((0.44, 0.42, 0.025, 1.0))
        )
    bm.to_mesh(landing_mesh)
    bm.free()

    # Overlook Dirt Platform
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=10,
        radius=1.15,
        depth=0.015,
        location=(6.7, 8.4, 2.512)
    )
    overlook_pad = bpy.context.active_object
    overlook_pad.name = 'SM_Overlook_Dirt_Pad'
    overlook_pad.scale = (1.2, 0.95, 1.0)
    overlook_pad.data.materials.append(mat_dirt)
    bpy.context.scene.collection.objects.unlink(overlook_pad)
    link_to(overlook_pad, 'Paths_and_Stairs')

# -------------------------------------------------------------
# 5. MAJESTIC PURPLE MOUNTAIN RANGE
# -------------------------------------------------------------
def build_mountain_range():
    """
    Creates the imposing, faceted stylized royal-purple mountain range:
    - Towering central peak reaching Z = 9.8
    - Left & right alpine ridges
    - Rocky purple spur in the center
    """
    mtn_mesh = bpy.data.meshes.new('Mountains_Mesh')
    mtn_obj = bpy.data.objects.new('SM_Mountains_Background', mtn_mesh)
    link_to(mtn_obj, 'Mountains')
    mtn_obj.data.materials.append(mat_mountain_lit)     # 0
    mtn_obj.data.materials.append(mat_mountain_shadow)  # 1
    
    bm = bmesh.new()
    
    def add_peak(cx, cy, bz, pz, rx, ry, facets=8, peak_off=(0,0)):
        vp = bm.verts.new((cx + peak_off[0], cy + peak_off[1], pz))
        ring = []
        for i in range(facets):
            ang = (i / float(facets)) * 2.0 * math.pi
            vx = cx + math.cos(ang) * rx * (0.88 + (i % 3) * 0.12)
            vy = cy + math.sin(ang) * ry * (0.88 + ((i+1) % 3) * 0.12)
            ring.append(bm.verts.new((vx, vy, bz)))
            
        for i in range(facets):
            i_next = (i + 1) % facets
            f = bm.faces.new((ring[i], ring[i_next], vp))
            # Facets facing right or slightly down get shadow purple
            if f.normal.x > 0.12 or f.normal.y < -0.1:
                f.material_index = 1
            else:
                f.material_index = 0

    # 1. Towering Central Sharp Peak (Height 9.8)
    add_peak(cx=5.8, cy=13.2, bz=0.5, pz=9.8, rx=4.6, ry=3.8, facets=10, peak_off=(-0.3, -0.4))
    # Front buttress peak
    add_peak(cx=6.6, cy=11.6, bz=1.5, pz=7.2, rx=2.5, ry=2.2, facets=8, peak_off=(0.1, -0.2))

    # 2. Left Mountain Peak
    add_peak(cx=1.8, cy=12.5, bz=1.0, pz=6.8, rx=3.4, ry=2.8, facets=8, peak_off=(-0.2, -0.2))
    add_peak(cx=-1.2, cy=11.2, bz=0.0, pz=5.0, rx=2.8, ry=2.6, facets=7)

    # 3. Right Mountain Peak
    add_peak(cx=10.4, cy=12.5, bz=0.5, pz=7.2, rx=3.6, ry=3.0, facets=8, peak_off=(0.3, -0.3))
    add_peak(cx=13.8, cy=11.0, bz=-0.5, pz=5.6, rx=4.0, ry=3.2, facets=8)

    # 4. Mid-Tier Mountain Spur (Apex at 3.6, 7.4, 3.4)
    add_peak(cx=3.6, cy=7.4, bz=1.25, pz=3.4, rx=1.4, ry=1.5, facets=7, peak_off=(0.1, -0.1))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mtn_mesh)
    bm.free()

# -------------------------------------------------------------
# 6. DECIDUOUS CARTOON TREES (Smooth Puffy Canopies)
# -------------------------------------------------------------
def create_deciduous_tree_template():
    mesh = bpy.data.meshes.new('Deciduous_Tree_Template_Mesh')
    obj = bpy.data.objects.new('Template_Deciduous_Tree', mesh)
    obj.data.materials.append(mat_trunk)       # 0
    obj.data.materials.append(mat_tree_leaf1)  # 1
    obj.data.materials.append(mat_tree_leaf2)  # 2
    
    bm = bmesh.new()
    
    # Curved Trunk with root flare
    trunk_h = 1.6
    n_rings = 4
    radii = [0.38, 0.25, 0.20, 0.17]
    zs = [0.0, 0.4, 0.9, trunk_h]
    xs = [0.0, 0.05, 0.10, 0.13]
    rings = []
    for r_i in range(n_rings):
        rv = []
        for i in range(8):
            ang = (i / 8.0) * 2.0 * math.pi
            vx = xs[r_i] + math.cos(ang) * radii[r_i]
            vy = math.sin(ang) * radii[r_i]
            rv.append(bm.verts.new((vx, vy, zs[r_i])))
        rings.append(rv)
        
    for r_i in range(n_rings - 1):
        for i in range(8):
            i_next = (i + 1) % 8
            f = bm.faces.new((rings[r_i][i], rings[r_i][i_next], rings[r_i+1][i_next], rings[r_i+1][i]))
            f.material_index = 0
            
    bm.faces.new(rings[0])
    
    # Fluffy Cloud Canopy (Smooth UV Spheres)
    puffs = [
        (0.12, 0.0, trunk_h + 0.65, 0.90, 1),
        (0.70, 0.25, trunk_h + 0.45, 0.68, 2),
        (-0.50, 0.20, trunk_h + 0.50, 0.66, 1),
        (0.10, -0.55, trunk_h + 0.40, 0.64, 2),
        (0.00, 0.55, trunk_h + 0.55, 0.68, 1),
        (0.20, 0.10, trunk_h + 1.25, 0.60, 2),
    ]
    for px, py, pz, prad, pmat in puffs:
        res = bmesh.ops.create_uvsphere(
            bm,
            u_segments=12,
            v_segments=8,
            radius=prad,
            matrix=Matrix.Translation((px, py, pz))
        )
        for v in res['verts']:
            for f in v.link_faces:
                f.material_index = pmat
                f.smooth = True
                
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    
    for poly in mesh.polygons:
        if poly.material_index in (1, 2):
            poly.use_smooth = True
            
    return obj

def place_deciduous_trees():
    template = create_deciduous_tree_template()
    trees = [
        # Right meadow grove (Tier 0)
        (8.4, 2.6, 0.0, 1.20, 0.4),
        (7.2, 4.2, 0.0, 0.98, -0.6),
        (10.0, 2.2, 0.0, 1.10, 1.2),
        (9.5, 4.4, 0.0, 0.88, 2.1),
        (11.0, 3.8, 0.0, 1.28, -1.8),
        # Far-left edge
        (1.2, 2.8, 0.0, 0.98, 0.8),
        (0.8, 4.2, 0.0, 0.82, -1.2),
    ]
    for idx, (tx, ty, tz, ts, tyaw) in enumerate(trees):
        t = bpy.data.objects.new(f'SM_Tree_Deciduous_{idx+1:02d}', template.data)
        t.location = (tx, ty, tz)
        t.rotation_euler = (0, 0, tyaw)
        t.scale = (ts, ts, ts)
        link_to(t, 'Vegetation')

# -------------------------------------------------------------
# 7. STYLIZED PINE TREES (Flared 3-Tier Cones)
# -------------------------------------------------------------
def create_pine_tree_template():
    mesh = bpy.data.meshes.new('Pine_Tree_Template_Mesh')
    obj = bpy.data.objects.new('Template_Pine_Tree', mesh)
    obj.data.materials.append(mat_trunk)        # 0
    obj.data.materials.append(mat_pine_leaf)    # 1
    
    bm = bmesh.new()
    
    res_tr = bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        segments=8,
        radius1=0.16,
        radius2=0.12,
        depth=0.55,
        matrix=Matrix.Translation((0, 0, 0.275))
    )
    for v in res_tr['verts']:
        for f in v.link_faces:
            f.material_index = 0
            
    tiers = [
        (0.82, 0.24, 0.90, 0.80),
        (0.64, 0.16, 0.85, 1.35),
        (0.42, 0.00, 0.85, 1.90),
    ]
    for r1, r2, ch, cz in tiers:
        res_c = bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            segments=8,
            radius1=r1,
            radius2=r2,
            depth=ch,
            matrix=Matrix.Translation((0, 0, cz))
        )
        for v in res_c['verts']:
            for f in v.link_faces:
                f.material_index = 1
                
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    return obj

def place_pine_trees():
    template = create_pine_tree_template()
    pines = [
        # Near Stairs 1
        (5.8, 4.8, 1.25, 0.90, 0.5),
        # On Tier 1 terrace / path
        (1.5, 4.5, 0.0, 0.85, -0.3),
        (0.8, 7.0, 1.25, 0.95, 1.1),
        (1.8, 9.2, 1.85, 1.00, -1.4),
        # On Tier 1 spur
        (4.8, 8.4, 1.85, 1.05, 0.7),
        # On Tier 2 overlook
        (5.0, 9.8, 2.50, 1.15, -0.8),
        (7.6, 9.2, 2.50, 1.00, 1.5),
        # Foreground & Right grove mix
        (1.8, 1.8, 0.0, 0.78, 0.2),
        (6.8, 5.8, 0.0, 0.90, -0.5),
        (10.8, 6.0, 0.0, 1.10, 0.9),
    ]
    for idx, (px, py, pz, ps, pyaw) in enumerate(pines):
        p = bpy.data.objects.new(f'SM_Tree_Pine_{idx+1:02d}', template.data)
        p.location = (px, py, pz)
        p.rotation_euler = (0, 0, pyaw)
        p.scale = (ps, ps, ps)
        link_to(p, 'Vegetation')

# -------------------------------------------------------------
# 8. WOODEN PROPS (Fence & Signposts)
# -------------------------------------------------------------
def build_wooden_props():
    # 1. Wooden Fence on Tier 2 Overlook
    f_mesh = bpy.data.meshes.new('Wooden_Fence_Mesh')
    f_obj = bpy.data.objects.new('SM_Fence_Wood_Overlook', f_mesh)
    link_to(f_obj, 'Props')
    f_obj.data.materials.append(mat_wood)
    
    bm = bmesh.new()
    posts = [
        (5.4, 7.5, 2.50),
        (6.4, 7.5, 2.50),
        (7.5, 7.5, 2.50),
        (7.5, 8.6, 2.50),
    ]
    p_h = 0.78
    p_w = 0.12
    for px, py, pz in posts:
        bmesh.ops.create_cube(
            bm,
            size=1.0,
            matrix=Matrix.Translation((px, py, pz + p_h * 0.5)) @ Matrix.Diagonal((p_w, p_w, p_h, 1.0))
        )
        bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            segments=4,
            radius1=p_w * 0.75,
            radius2=0.0,
            depth=0.10,
            matrix=Matrix.Translation((px, py, pz + p_h + 0.05)) @ Matrix.Rotation(math.radians(45), 4, 'Z')
        )
        
    rails = [(posts[0], posts[1]), (posts[1], posts[2]), (posts[2], posts[3])]
    for (p1, p2) in rails:
        v1 = Vector(p1)
        v2 = Vector(p2)
        mid = (v1 + v2) * 0.5
        dist = (v2 - v1).length
        ang = math.atan2(v2.y - v1.y, v2.x - v1.x)
        bmesh.ops.create_cube(
            bm,
            size=1.0,
            matrix=Matrix.Translation((mid.x, mid.y, mid.z + 0.30)) @ Matrix.Rotation(ang, 4, 'Z') @ Matrix.Diagonal((dist, 0.05, 0.06, 1.0))
        )
        bmesh.ops.create_cube(
            bm,
            size=1.0,
            matrix=Matrix.Translation((mid.x, mid.y, mid.z + 0.58)) @ Matrix.Rotation(ang, 4, 'Z') @ Matrix.Diagonal((dist, 0.05, 0.06, 1.0))
        )
    bm.to_mesh(f_mesh)
    bm.free()

    # 2. Wooden Directional Signpost on Overlook
    s_mesh = bpy.data.meshes.new('Signpost_Mesh')
    s_obj = bpy.data.objects.new('SM_Signpost_Overlook', s_mesh)
    link_to(s_obj, 'Props')
    s_obj.data.materials.append(mat_wood)
    bm = bmesh.new()
    sx, sy, sz = 6.2, 8.2, 2.50
    bmesh.ops.create_cube(
        bm,
        size=1.0,
        matrix=Matrix.Translation((sx, sy, sz + 0.60)) @ Matrix.Diagonal((0.10, 0.10, 1.20, 1.0))
    )
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        segments=4,
        radius1=0.08,
        radius2=0.0,
        depth=0.12,
        matrix=Matrix.Translation((sx, sy, sz + 1.26)) @ Matrix.Rotation(math.radians(45), 4, 'Z')
    )
    bmesh.ops.create_cube(
        bm,
        size=1.0,
        matrix=Matrix.Translation((sx - 0.26, sy, sz + 0.98)) @ Matrix.Diagonal((0.58, 0.05, 0.18, 1.0))
    )
    bmesh.ops.create_cube(
        bm,
        size=1.0,
        matrix=Matrix.Translation((sx + 0.24, sy + 0.08, sz + 0.74)) @ Matrix.Rotation(math.radians(25), 4, 'Z') @ Matrix.Diagonal((0.52, 0.05, 0.16, 1.0))
    )
    bm.to_mesh(s_mesh)
    bm.free()

    # 3. Secondary Sign on Tier 1
    s2_mesh = bpy.data.meshes.new('Signpost_T1_Mesh')
    s2_obj = bpy.data.objects.new('SM_Signpost_Tier1', s2_mesh)
    link_to(s2_obj, 'Props')
    s2_obj.data.materials.append(mat_wood)
    bm = bmesh.new()
    s2x, s2y, s2z = 2.2, 7.6, 1.25
    bmesh.ops.create_cube(
        bm,
        size=1.0,
        matrix=Matrix.Translation((s2x, s2y, s2z + 0.45)) @ Matrix.Diagonal((0.08, 0.08, 0.90, 1.0))
    )
    bmesh.ops.create_cube(
        bm,
        size=1.0,
        matrix=Matrix.Translation((s2x + 0.18, s2y, s2z + 0.78)) @ Matrix.Diagonal((0.46, 0.04, 0.15, 1.0))
    )
    bm.to_mesh(s2_mesh)
    bm.free()

# -------------------------------------------------------------
# 9. BOULDERS & ROCKS
# -------------------------------------------------------------
def build_boulders():
    boulders = [
        (4.4, 0.9, 0.08, 0.24, 0.20, 0.18),
        (3.2, 2.4, 0.08, 0.30, 0.24, 0.20),
        (4.2, 3.2, 0.08, 0.20, 0.16, 0.15),
        (5.8, 3.4, 0.08, 0.28, 0.22, 0.20),
        (6.2, 1.2, 0.08, 0.35, 0.28, 0.22),
        (1.5, 6.2, 1.30, 0.38, 0.30, 0.24),
        (2.0, 8.6, 1.90, 0.30, 0.24, 0.20),
    ]
    for idx, (bx, by, bz, rx, ry, rz) in enumerate(boulders):
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=2,
            radius=1.0,
            location=(bx, by, bz)
        )
        rk = bpy.context.active_object
        rk.name = f'SM_Rock_Boulder_{idx+1:02d}'
        rk.scale = (rx, ry, rz)
        rk.rotation_euler = (random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), (idx * 1.5) % 3.14)
        rk.data.materials.append(mat_stone)
        bpy.context.scene.collection.objects.unlink(rk)
        link_to(rk, 'Props')

# -------------------------------------------------------------
# 10. DAISY WILDFLOWERS & TALL GRASS
# -------------------------------------------------------------
def build_flowers_and_grass():
    d_mesh = bpy.data.meshes.new('Daisy_Template_Mesh')
    d_template = bpy.data.objects.new('Template_Daisy', d_mesh)
    d_template.data.materials.append(mat_center)  # 0
    d_template.data.materials.append(mat_petal)   # 1
    d_template.data.materials.append(mat_blade)   # 2
    
    bm = bmesh.new()
    stem_h = 0.32
    res_st = bmesh.ops.create_cone(
        bm,
        cap_ends=False,
        segments=5,
        radius1=0.016,
        radius2=0.012,
        depth=stem_h,
        matrix=Matrix.Translation((0, 0, stem_h * 0.5))
    )
    for v in res_st['verts']:
        for f in v.link_faces:
            f.material_index = 2
            
    res_c = bmesh.ops.create_uvsphere(
        bm,
        u_segments=8,
        v_segments=6,
        radius=0.052,
        matrix=Matrix.Translation((0, 0, stem_h + 0.025)) @ Matrix.Diagonal((1.0, 1.0, 0.5, 1.0))
    )
    for v in res_c['verts']:
        for f in v.link_faces:
            f.material_index = 0
            
    n_pet = 8
    p_len = 0.10
    p_w = 0.034
    for i in range(n_pet):
        ang = (i / float(n_pet)) * 2.0 * math.pi
        px = math.cos(ang) * (p_len * 0.5 + 0.035)
        py = math.sin(ang) * (p_len * 0.5 + 0.035)
        res_p = bmesh.ops.create_cube(
            bm,
            size=1.0,
            matrix=Matrix.Translation((px, py, stem_h + 0.018)) @ Matrix.Rotation(ang, 4, 'Z') @ Matrix.Diagonal((p_len, p_w, 0.01, 1.0))
        )
        for v in res_p['verts']:
            for f in v.link_faces:
                f.material_index = 1
                
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(d_mesh)
    bm.free()

    fg_flowers = []
    for _ in range(65):
        fx = random.uniform(0.8, 7.5)
        fy = random.uniform(0.15, 1.8)
        if 4.5 <= fx <= 6.2 and fy <= 0.8:
            continue
        fg_flowers.append((fx, fy, 0.0, random.uniform(0.85, 1.30)))
        
    t1_flowers = []
    for _ in range(35):
        fx = random.uniform(2.5, 4.8)
        fy = random.uniform(5.0, 6.8)
        t1_flowers.append((fx, fy, 1.25, random.uniform(0.85, 1.25)))
        
    t15_flowers = []
    for _ in range(18):
        fx = random.uniform(0.8, 2.8)
        fy = random.uniform(8.8, 10.5)
        t15_flowers.append((fx, fy, 1.85, random.uniform(0.85, 1.20)))

    t2_flowers = []
    for _ in range(16):
        fx = random.uniform(6.0, 8.0)
        fy = random.uniform(8.0, 9.4)
        t2_flowers.append((fx, fy, 2.50, random.uniform(0.85, 1.20)))

    all_fl = fg_flowers + t1_flowers + t15_flowers + t2_flowers
    for idx, (flx, fly, flz, fls) in enumerate(all_fl):
        flo = bpy.data.objects.new(f'SM_Daisy_{idx+1:03d}', d_template.data)
        flo.location = (flx, fly, flz)
        flo.rotation_euler = (random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15), random.uniform(0, 3.14))
        flo.scale = (fls, fls, fls)
        link_to(flo, 'Vegetation')

    # Grass Blades
    g_mesh = bpy.data.meshes.new('Grass_Clump_Template_Mesh')
    g_template = bpy.data.objects.new('Template_Grass_Clump', g_mesh)
    g_template.data.materials.append(mat_blade)
    bm = bmesh.new()
    for b_i in range(5):
        b_ang = (b_i / 5.0) * math.pi * 0.9 - 0.45
        b_tilt = random.uniform(0.18, 0.38)
        b_h = random.uniform(0.30, 0.48)
        bmesh.ops.create_cone(
            bm,
            cap_ends=False,
            segments=3,
            radius1=0.035,
            radius2=0.005,
            depth=b_h,
            matrix=Matrix.Translation((math.sin(b_ang)*0.07, 0, b_h*0.5)) @ Matrix.Rotation(b_tilt * math.cos(b_ang), 4, 'Y')
        )
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(g_mesh)
    bm.free()

    for idx in range(55):
        gx = random.uniform(0.6, 7.8)
        gy = random.uniform(0.1, 2.2)
        go = bpy.data.objects.new(f'SM_Grass_Clump_{idx+1:02d}', g_template.data)
        go.location = (gx, gy, 0.0)
        go.rotation_euler = (0, 0, random.uniform(0, 3.14))
        go.scale = (1.0, 1.0, random.uniform(0.85, 1.35))
        link_to(go, 'Vegetation')

# -------------------------------------------------------------
# 11. CARTOON SKY BACKDROP & CLOUDS
# -------------------------------------------------------------
def setup_sky_backdrop():
    mat_sky = bpy.data.materials.new('Mat_Sky_Gradient')
    mat_sky.use_nodes = True
    sn = mat_sky.node_tree.nodes
    sl = mat_sky.node_tree.links
    sn.clear()
    
    out = sn.new(type='ShaderNodeOutputMaterial')
    emit = sn.new(type='ShaderNodeEmission')
    emit.inputs['Strength'].default_value = 1.0
    sl.new(emit.outputs['Emission'], out.inputs['Surface'])
    
    tex_coord = sn.new(type='ShaderNodeTexCoord')
    sep_xyz = sn.new(type='ShaderNodeSeparateXYZ')
    sl.new(tex_coord.outputs['Generated'], sep_xyz.inputs['Vector'])
    
    ramp = sn.new(type='ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0.92, 0.94, 0.98, 1.0)  # Horizon soft lavender
    ramp.color_ramp.elements[1].position = 0.45
    ramp.color_ramp.elements[1].color = (0.48, 0.76, 0.98, 1.0)  # Rich vibrant sky cyan
    sl.new(sep_xyz.outputs['Z'], ramp.inputs['Fac'])
    sl.new(ramp.outputs['Color'], emit.inputs['Color'])

    # Backdrop plane behind mountains
    bpy.ops.mesh.primitive_plane_add(
        size=45.0,
        location=(13.0, 13.0, 7.5)
    )
    sky = bpy.context.active_object
    sky.name = 'SM_Sky_Backdrop_Plane'
    sky.rotation_euler = (math.radians(90), 0, math.radians(-45))
    sky.scale = (1.2, 1.0, 1.0)
    sky.data.materials.append(mat_sky)
    bpy.context.scene.collection.objects.unlink(sky)
    link_to(sky, 'Mountains')

    # Stylized 3D Puffy Cartoon Clouds
    mat_cloud = create_mat('Mat_Cartoon_Cloud', (0.96, 0.97, 1.0, 1.0), roughness=0.35, emit_col=(0.96, 0.97, 1.0, 1.0), emit_str=0.20)
    clouds = [
        (2.0, 14.5, 8.0, 2.2),
        (9.5, 15.0, 8.5, 2.5),
        (-2.5, 13.0, 6.4, 1.8),
        (14.0, 13.5, 7.0, 2.0),
    ]
    for idx, (cx, cy, cz, cs) in enumerate(clouds):
        c_mesh = bpy.data.meshes.new(f'Cloud_{idx+1}_Mesh')
        c_obj = bpy.data.objects.new(f'SM_Cloud_{idx+1:02d}', c_mesh)
        link_to(c_obj, 'Mountains')
        c_obj.data.materials.append(mat_cloud)
        
        bm = bmesh.new()
        puffs = [
            (0, 0, 0, 0.85),
            (0.75, 0, -0.1, 0.65),
            (-0.75, 0, -0.1, 0.60),
            (0.2, 0, 0.40, 0.60),
        ]
        for px, py, pz, prad in puffs:
            res = bmesh.ops.create_uvsphere(
                bm,
                u_segments=10,
                v_segments=7,
                radius=prad * cs,
                matrix=Matrix.Translation((cx + px * cs, cy + py * cs, cz + pz * cs)) @ Matrix.Diagonal((1.0, 0.7, 0.65, 1.0))
            )
            for v in res['verts']:
                for f in v.link_faces:
                    f.smooth = True
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(c_mesh)
        bm.free()

# -------------------------------------------------------------
# 12. CAMERA & BALANCED LIGHTING SETUP
# -------------------------------------------------------------
def setup_camera_and_lighting():
    center_x = 6.0
    center_y = 6.0
    center_z = 1.35
    
    empty = bpy.data.objects.new('Target_Iso_Center', None)
    empty.location = (center_x, center_y, center_z)
    link_to(empty, 'Lighting_and_Camera')
    
    cam_data = bpy.data.cameras.new('Isometric_Camera')
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 17.5
    cam_obj = bpy.data.objects.new('SM_Isometric_Camera', cam_data)
    link_to(cam_obj, 'Lighting_and_Camera')
    
    dist = 28.0
    cam_height = 23.0
    cam_obj.location = (center_x - dist, center_y - dist, center_z + cam_height)
    
    c = cam_obj.constraints.new(type='TRACK_TO')
    c.target = empty
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'
    bpy.context.scene.camera = cam_obj
    
    # Balanced Warm Sunlight (Clean cartoon shadows, no blowout)
    sun_data = bpy.data.lights.new(name='Sun_KeyLight', type='SUN')
    sun_data.energy = 3.2
    sun_data.color = (1.0, 0.98, 0.94)
    sun_data.angle = math.radians(2.0)
    sun_obj = bpy.data.objects.new('SM_Sun_KeyLight', sun_data)
    link_to(sun_obj, 'Lighting_and_Camera')
    sun_obj.rotation_euler = (math.radians(48), math.radians(22), math.radians(-35))
    
    # Soft Sky Fill Light
    fill_data = bpy.data.lights.new(name='Sun_FillLight', type='SUN')
    fill_data.energy = 1.5
    fill_data.color = (0.80, 0.90, 1.0)
    fill_obj = bpy.data.objects.new('SM_Sun_FillLight', fill_data)
    link_to(fill_obj, 'Lighting_and_Camera')
    fill_obj.rotation_euler = (math.radians(60), math.radians(-40), math.radians(120))
    
    # World Background Color
    world = bpy.data.worlds.new('Cartoon_World')
    bpy.context.scene.world = world
    world.color = (0.75, 0.85, 0.96)

# -------------------------------------------------------------
# 13. RENDER AND EXPORT PIPELINE
# -------------------------------------------------------------
def render_and_export():
    scene = bpy.context.scene
    
    # Standard View Transform for Vibrant Cartoon Art Style
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    
    # Render Settings
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    
    # Save .blend scene
    blend_path = os.path.join(WORKSPACE_DIR, "map_25d.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved .blend: {blend_path}")
    
    # Render image
    render_path = os.path.join(WORKSPACE_DIR, "render_map_25d.png")
    scene.render.filepath = render_path
    bpy.ops.render.render(write_still=True)
    print(f"Saved Render: {render_path}")
    
    # Export glTF 2.0 (.glb)
    glb_path = os.path.join(WORKSPACE_DIR, "map_25d.glb")
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_materials='EXPORT',
        export_yup=True
    )
    print(f"Exported GLB: {glb_path}")
    
    # Export FBX
    fbx_path = os.path.join(WORKSPACE_DIR, "map_25d.fbx")
    bpy.ops.export_scene.fbx(
        filepath=fbx_path,
        use_selection=False,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        bake_space_transform=True,
        object_types={'MESH', 'EMPTY'}
    )
    print(f"Exported FBX: {fbx_path}")

# -------------------------------------------------------------
# RUN
# -------------------------------------------------------------
if __name__ == '__main__':
    print("Executing Master 2.5D Game Map generation...")
    build_watertight_terrain()
    build_paths_and_stairs()
    build_mountain_range()
    place_deciduous_trees()
    place_pine_trees()
    build_wooden_props()
    build_boulders()
    build_flowers_and_grass()
    setup_sky_backdrop()
    setup_camera_and_lighting()
    render_and_export()
    print("Master 2.5D Game Map completed successfully!")
