import os
from pathlib import Path

materials_map = {
    'M_Door_Wood.tres': ('norm_door_wood.png', 0.15, 0.65, 1.0),
    'M_Roof_Tiles_Red.tres': ('norm_roof_tiles_red.png', 0.0, 0.70, 1.2),
    'M_Roof_Tiles_Teal.tres': ('norm_roof_tiles_teal.png', 0.0, 0.65, 1.2),
    'M_Stone_Cobble.tres': ('norm_stone_cobble.png', 0.0, 0.80, 1.0),
    'M_Forge_Brick.tres': ('norm_forge_brick.png', 0.05, 0.75, 1.0),
    'M_Wood.tres': ('norm_wood_seamless.png', 0.05, 0.60, 0.8),
    'M_Wood_Fence.tres': ('norm_wood_seamless.png', 0.05, 0.65, 0.8),
    'M_Rock.tres': ('norm_rock_seamless.png', 0.0, 0.85, 1.1),
    'M_Anvil_Iron.tres': ('norm_anvil_iron.png', 0.75, 0.40, 0.9),
    'M_Metal.tres': ('norm_metal_seamless.png', 0.85, 0.35, 0.7),
    'M_Dirt.tres': ('norm_dirt_seamless.png', 0.0, 0.90, 0.8),
}

mat_dir = Path('Assets/Materials_Shared')
for mat_name, (norm_file, met, rough, nscale) in materials_map.items():
    p = mat_dir / mat_name
    if not p.exists():
        print(f'Not found: {p}')
        continue
    content = p.read_text(encoding='utf-8')
    if 'norm_' in content:
        print(f'Already upgraded: {mat_name}')
        continue
    
    # Update load_steps
    content = content.replace('load_steps=2', 'load_steps=3')
    if 'load_steps=3' not in content and 'load_steps=' not in content:
        content = content.replace('[gd_resource type="StandardMaterial3D" format=3', '[gd_resource type="StandardMaterial3D" load_steps=3 format=3')
    
    norm_line = f'[ext_resource type="Texture2D" path="res://Assets/Textures/Tileable/{norm_file}" id="2_norm"]\n'
    parts = content.split('[resource]')
    new_header = parts[0].strip() + '\n' + norm_line + '\n[resource]\n'
    body = parts[1].strip()
    
    # Add normal_enabled and normal_texture
    normal_block = f'normal_enabled = true\nnormal_scale = {nscale}\nnormal_texture = ExtResource("2_norm")\n'
    if 'metallic = ' not in body:
        normal_block += f'metallic = {met}\n'
    if 'roughness = ' not in body:
        normal_block += f'roughness = {rough}\n'
        
    new_content = new_header + normal_block + body + '\n'
    p.write_text(new_content, encoding='utf-8')
    print(f'Upgraded PBR for: {mat_name}')
