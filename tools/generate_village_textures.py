"""
Sinh các Texture Liền Mạch (Seamless Tileable Textures) cho Bản Đồ Làng
Theo quy chuẩn Zero-Bloat Texture Architect và bảng màu từ modelyeucau/map2/1.jpg
"""
import os
import math
from PIL import Image, ImageDraw

out_dir = "Assets/Textures/Tileable"
os.makedirs(out_dir, exist_ok=True)

def generate_roof_tiles(path, base_rgb, highlight_rgb, shadow_rgb, tile_w=32, tile_h=16, size=256):
    img = Image.new("RGB", (size, size), shadow_rgb)
    draw = ImageDraw.Draw(img)
    
    rows = size // tile_h
    cols = size // tile_w + 2
    
    for r in range(rows):
        y = r * tile_h
        offset = (tile_w // 2) if (r % 2 == 1) else 0
        for c in range(-1, cols):
            x = c * tile_w + offset
            # Draw individual rounded tile
            # Tile body
            draw.rectangle([x + 1, y + 1, x + tile_w - 2, y + tile_h - 1], fill=base_rgb)
            # Top highlight
            draw.line([x + 2, y + 2, x + tile_w - 3, y + 2], fill=highlight_rgb, width=1)
            # Left highlight
            draw.line([x + 2, y + 2, x + 2, y + tile_h - 2], fill=highlight_rgb, width=1)
            # Bottom shadow
            draw.line([x + 1, y + tile_h - 1, x + tile_w - 2, y + tile_h - 1], fill=shadow_rgb, width=1)
            # Right shadow
            draw.line([x + tile_w - 2, y + 2, x + tile_w - 2, y + tile_h - 1], fill=shadow_rgb, width=1)
            
    # Crop to exact size to maintain tileability
    img = img.crop((0, 0, size, size))
    img.save(path)
    print(f"Generated: {path}")

def generate_cobblestone(path, base_rgb=(104, 108, 112), mortar_rgb=(58, 60, 62), size=256):
    img = Image.new("RGB", (size, size), mortar_rgb)
    draw = ImageDraw.Draw(img)
    
    # 8 rows of stones
    rows = 8
    rh = size // rows
    
    for r in range(rows):
        y = r * rh
        offset = (rh // 2) if (r % 2 == 1) else 0
        cols = 8
        cw = size // cols
        for c in range(-1, cols + 1):
            x = c * cw + offset
            # draw stone with bevel
            draw.rounded_rectangle([x + 2, y + 2, x + cw - 2, y + rh - 2], radius=4, fill=base_rgb)
            # inner stone texture line
            draw.line([x + 4, y + 3, x + cw - 4, y + 3], fill=(130, 135, 140), width=1)
            draw.line([x + 3, y + 4, x + 3, y + rh - 4], fill=(130, 135, 140), width=1)
            draw.line([x + cw - 3, y + 3, x + cw - 3, y + rh - 3], fill=(70, 72, 75), width=1)
            draw.line([x + 3, y + rh - 3, x + cw - 3, y + rh - 3], fill=(70, 72, 75), width=1)
            
    img = img.crop((0, 0, size, size))
    img.save(path)
    print(f"Generated: {path}")

def generate_2x2_tile_preview(tex_path, out_preview):
    """Xuất ảnh lát thử 2x2 để tự soi mép nối Seamless 100% theo quy chuẩn."""
    tex = Image.open(tex_path)
    w, h = tex.size
    preview = Image.new(tex.mode, (w * 2, h * 2))
    preview.paste(tex, (0, 0))
    preview.paste(tex, (w, 0))
    preview.paste(tex, (0, h))
    preview.paste(tex, (w, h))
    preview.save(out_preview)
    print(f"Tile 2x2 preview saved: {out_preview}")

if __name__ == '__main__':
    # 1. Red roof tiles (Nhà rèn, quán ăn, nhà dân)
    p_red = os.path.join(out_dir, "tex_roof_tiles_red.png")
    generate_roof_tiles(p_red, (168, 56, 40), (200, 80, 60), (92, 29, 21))
    
    # 2. Teal roof tiles (Nhà giả kim)
    p_teal = os.path.join(out_dir, "tex_roof_tiles_teal.png")
    generate_roof_tiles(p_teal, (38, 140, 130), (60, 175, 162), (20, 75, 70))
    
    # 3. Cobblestone (Lò rèn, ống khói, giếng đá, vách đá)
    p_cobble = os.path.join(out_dir, "tex_stone_cobble.png")
    generate_cobblestone(p_cobble)
    
    # Preview 2x2
    generate_2x2_tile_preview(p_red, "Assets/Textures/_tile_preview_roof_red.png")
    generate_2x2_tile_preview(p_teal, "Assets/Textures/_tile_preview_roof_teal.png")
    generate_2x2_tile_preview(p_cobble, "Assets/Textures/_tile_preview.png")
