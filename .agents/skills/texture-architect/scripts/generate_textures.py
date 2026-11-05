"""
Script sinh Texture chuẩn lũy thừa 2 (512x512) Stylized và Seamless cho Godot 4.
Được thiết kế bởi @texture-architect.
"""

import math
import os
import numpy as np
from PIL import Image, ImageFilter

OUTPUT_TILEABLE = r"C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới\Assets\Textures\Tileable"
OUTPUT_MASKS = r"C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới\Assets\Textures\Grayscale_Masks"
OUTPUT_PALETTES = r"C:\xnhaugame\MyGodotGame\dự-án-trò-chơi-mới\Assets\Textures\Palettes"

os.makedirs(OUTPUT_TILEABLE, exist_ok=True)
os.makedirs(OUTPUT_MASKS, exist_ok=True)
os.makedirs(OUTPUT_PALETTES, exist_ok=True)

SIZE = 512

def periodic_noise(size, octaves=4, seed=42):
    """
    Sinh 2D seamless periodic noise dựa trên hàm điều hòa sin/cos đa tần số ngẫu nhiên.
    Đảm bảo 100% lặp tuần hoàn tại biên (f(0) == f(size)).
    """
    rng = np.random.RandomState(seed)
    grid_y, grid_x = np.indices((size, size), dtype=np.float32)
    noise = np.zeros((size, size), dtype=np.float32)
    
    total_amp = 0.0
    for o in range(1, octaves + 1):
        freq = 2 ** o
        amp = 1.0 / (o ** 1.2)
        total_amp += amp
        
        # Tạo tổ hợp sin/cos tuần hoàn hoàn hảo với chu kỳ size
        for _ in range(3):
            kx = rng.randint(1, freq + 1)
            ky = rng.randint(1, freq + 1)
            phase_x = rng.uniform(0, 2 * math.pi)
            phase_y = rng.uniform(0, 2 * math.pi)
            
            term = np.sin(2 * math.pi * kx * grid_x / size + phase_x) * \
                   np.cos(2 * math.pi * ky * grid_y / size + phase_y)
            noise += (term * (amp / 3.0))
            
    noise = (noise / total_amp)
    # Chuẩn hóa về [0, 1]
    noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-6)
    return noise

def periodic_worley(size, num_cells=8, seed=42):
    """
    Sinh Voronoi/Worley noise tuần hoàn (toroidal distance) phục vụ vân đá/sỏi nứt rạn Stylized.
    """
    rng = np.random.RandomState(seed)
    points = rng.rand(num_cells, 2) * size
    
    y, x = np.ogrid[:size, :size]
    min_dist1 = np.full((size, size), size * 2.0, dtype=np.float32)
    min_dist2 = np.full((size, size), size * 2.0, dtype=np.float32)
    
    for px, py in points:
        # Khoảng cách xuyến toroidal
        dx = np.abs(x - px)
        dx = np.minimum(dx, size - dx)
        dy = np.abs(y - py)
        dy = np.minimum(dy, size - dy)
        dist = np.sqrt(dx * dx + dy * dy)
        
        # Cập nhật khoảng cách gần nhất và nhì
        mask = dist < min_dist1
        min_dist2 = np.where(mask, min_dist1, np.minimum(min_dist2, dist))
        min_dist1 = np.where(mask, dist, min_dist1)
        
    f1 = min_dist1
    f2 = min_dist2
    edge = f2 - f1
    edge = (edge - edge.min()) / (edge.max() - edge.min() + 1e-6)
    cell = (f1 - f1.min()) / (f1.max() - f1.min() + 1e-6)
    return cell, edge

def make_grass_textures():
    """Tạo tex_grass_seamless.png và mask_grass_detail.png"""
    n1 = periodic_noise(SIZE, octaves=5, seed=101)
    n2 = periodic_noise(SIZE, octaves=3, seed=102)
    
    # Stylized Grass clumps
    grass_blend = n1 * 0.7 + n2 * 0.3
    grass_stylized = np.clip(np.sin(grass_blend * math.pi * 3.5) * 0.5 + 0.5, 0, 1)
    grass_mask = grass_blend * 0.6 + grass_stylized * 0.4
    grass_mask = np.clip(grass_mask * 0.7 + 0.3, 0.25, 1.0)
    
    # Màu cỏ xanh mát Stylized: Base #529934 -> R=82, G=153, B=52
    c_dark = np.array([48, 110, 32], dtype=np.float32)
    c_mid = np.array([82, 153, 52], dtype=np.float32)
    c_light = np.array([126, 194, 68], dtype=np.float32)
    c_warm = np.array([148, 206, 75], dtype=np.float32)
    
    t = grass_mask[..., np.newaxis]
    color = np.where(t < 0.5, 
                     c_dark + (c_mid - c_dark) * (t / 0.5),
                     c_mid + (c_light - c_mid) * ((t - 0.5) / 0.5))
    
    accent = (periodic_noise(SIZE, octaves=6, seed=103) > 0.78)
    color[accent] = color[accent] * 0.85 + c_warm * 0.15
    
    img_color = Image.fromarray(np.clip(color, 0, 255).astype(np.uint8))
    img_color = img_color.filter(ImageFilter.SMOOTH_MORE)
    img_color.save(os.path.join(OUTPUT_TILEABLE, "tex_grass_seamless.png"))
    
    img_mask = Image.fromarray((grass_mask * 255).astype(np.uint8))
    img_mask.save(os.path.join(OUTPUT_MASKS, "mask_grass_detail.png"))
    print("✓ Đã tạo tex_grass_seamless.png và mask_grass_detail.png")

def make_dirt_textures():
    """Tạo tex_dirt_seamless.png và mask_dirt_detail.png"""
    n1 = periodic_noise(SIZE, octaves=4, seed=201)
    n2 = periodic_noise(SIZE, octaves=6, seed=202)
    cells, edges = periodic_worley(SIZE, num_cells=18, seed=203)
    
    dirt_val = n1 * 0.5 + n2 * 0.3 + (1.0 - edges) * 0.2
    dirt_val = np.clip(dirt_val, 0, 1)
    dirt_mask = np.clip(dirt_val * 0.7 + 0.3, 0.25, 1.0)
    
    # Nâu đất tự nhiên #8A5C35
    c_deep = np.array([92, 58, 36], dtype=np.float32)
    c_base = np.array([138, 92, 53], dtype=np.float32)
    c_light = np.array([178, 128, 80], dtype=np.float32)
    c_pebble = np.array([150, 135, 120], dtype=np.float32)
    
    t = dirt_val[..., np.newaxis]
    color = np.where(t < 0.5,
                     c_deep + (c_base - c_deep) * (t / 0.5),
                     c_base + (c_light - c_base) * ((t - 0.5) / 0.5))
    
    pebble_mask = (cells < 0.12)
    color[pebble_mask] = color[pebble_mask] * 0.4 + c_pebble * 0.6
    
    img_color = Image.fromarray(np.clip(color, 0, 255).astype(np.uint8))
    img_color = img_color.filter(ImageFilter.SMOOTH)
    img_color.save(os.path.join(OUTPUT_TILEABLE, "tex_dirt_seamless.png"))
    
    img_mask = Image.fromarray((dirt_mask * 255).astype(np.uint8))
    img_mask.save(os.path.join(OUTPUT_MASKS, "mask_dirt_detail.png"))
    print("✓ Đã tạo tex_dirt_seamless.png và mask_dirt_detail.png")

def make_rock_textures():
    """Tạo tex_rock_seamless.png và mask_rock_detail.png"""
    cells, edges = periodic_worley(SIZE, num_cells=14, seed=301)
    n = periodic_noise(SIZE, octaves=5, seed=302)
    
    rock_facet = np.clip(cells * 0.6 + (1.0 - edges) * 0.4, 0, 1)
    rock_val = rock_facet * 0.7 + n * 0.3
    rock_mask = np.clip(rock_val * 0.75 + 0.25, 0.2, 1.0)
    
    # Đá xám đá phiến Stylized
    c_crack = np.array([65, 68, 75], dtype=np.float32)
    c_shade = np.array([95, 102, 112], dtype=np.float32)
    c_mid = np.array([135, 142, 150], dtype=np.float32)
    c_highlight = np.array([182, 190, 200], dtype=np.float32)
    
    t = rock_val[..., np.newaxis]
    color = np.where(t < 0.4,
                     c_crack + (c_shade - c_crack) * (t / 0.4),
                     np.where(t < 0.75,
                              c_shade + (c_mid - c_shade) * ((t - 0.4) / 0.35),
                              c_mid + (c_highlight - c_mid) * ((t - 0.75) / 0.25)))
                              
    crack_mask = (edges < 0.08)
    color[crack_mask] = color[crack_mask] * 0.45 + c_crack * 0.55
    
    img_color = Image.fromarray(np.clip(color, 0, 255).astype(np.uint8))
    img_color.save(os.path.join(OUTPUT_TILEABLE, "tex_rock_seamless.png"))
    
    img_mask = Image.fromarray((rock_mask * 255).astype(np.uint8))
    img_mask.save(os.path.join(OUTPUT_MASKS, "mask_rock_detail.png"))
    print("✓ Đã tạo tex_rock_seamless.png và mask_rock_detail.png")

def make_wood_textures():
    """Tạo tex_wood_seamless.png và mask_wood_grain.png"""
    grid_y, grid_x = np.indices((SIZE, SIZE), dtype=np.float32)
    n_warp = periodic_noise(SIZE, octaves=3, seed=401)
    
    u = grid_x / SIZE
    distorted_u = u + (n_warp - 0.5) * 0.15
    grain_waves = np.sin(distorted_u * 2 * math.pi * 14) * 0.5 + 0.5
    fine_grain = periodic_noise(SIZE, octaves=5, seed=402)
    
    wood_val = grain_waves * 0.65 + fine_grain * 0.35
    wood_mask = np.clip(wood_val * 0.7 + 0.3, 0.25, 1.0)
    
    c_dark = np.array([115, 74, 45], dtype=np.float32)
    c_base = np.array([168, 118, 74], dtype=np.float32)
    c_light = np.array([205, 155, 108], dtype=np.float32)
    
    t = wood_val[..., np.newaxis]
    color = np.where(t < 0.5,
                     c_dark + (c_base - c_dark) * (t / 0.5),
                     c_base + (c_light - c_base) * ((t - 0.5) / 0.5))
                     
    img_color = Image.fromarray(np.clip(color, 0, 255).astype(np.uint8))
    img_color.save(os.path.join(OUTPUT_TILEABLE, "tex_wood_seamless.png"))
    
    img_mask = Image.fromarray((wood_mask * 255).astype(np.uint8))
    img_mask.save(os.path.join(OUTPUT_MASKS, "mask_wood_grain.png"))
    print("✓ Đã tạo tex_wood_seamless.png và mask_wood_grain.png")

def make_metal_textures():
    """Tạo tex_metal_seamless.png và mask_metal_surface.png"""
    grid_y, grid_x = np.indices((SIZE, SIZE), dtype=np.float32)
    n1 = periodic_noise(SIZE, octaves=3, seed=501)
    
    scratch = periodic_noise(SIZE, octaves=6, seed=502)
    scratch_aniso = np.sin((grid_y / SIZE) * 2 * math.pi * 24 + n1 * 2) * 0.5 + 0.5
    metal_val = scratch * 0.4 + scratch_aniso * 0.3 + n1 * 0.3
    metal_mask = np.clip(metal_val * 0.6 + 0.4, 0.35, 1.0)
    
    c_dark = np.array([140, 145, 155], dtype=np.float32)
    c_base = np.array([185, 192, 202], dtype=np.float32)
    c_shine = np.array([225, 230, 238], dtype=np.float32)
    
    t = metal_val[..., np.newaxis]
    color = np.where(t < 0.5,
                     c_dark + (c_base - c_dark) * (t / 0.5),
                     c_base + (c_shine - c_base) * ((t - 0.5) / 0.5))
                     
    img_color = Image.fromarray(np.clip(color, 0, 255).astype(np.uint8))
    img_color.save(os.path.join(OUTPUT_TILEABLE, "tex_metal_seamless.png"))
    
    img_mask = Image.fromarray((metal_mask * 255).astype(np.uint8))
    img_mask.save(os.path.join(OUTPUT_MASKS, "mask_metal_surface.png"))
    print("✓ Đã tạo tex_metal_seamless.png và mask_metal_surface.png")

def make_palette_texture():
    """Tạo palette_standard_stylized.png (256x64 px)"""
    WIDTH = 256
    HEIGHT = 64
    
    ramps = [
        [(34, 78, 24), (65, 130, 42), (98, 178, 62), (160, 220, 85)],
        [(18, 48, 22), (32, 92, 45), (55, 145, 75), (110, 195, 120)],
        [(68, 40, 22), (115, 72, 40), (165, 112, 65), (210, 160, 110)],
        [(80, 50, 45), (135, 85, 70), (180, 120, 100), (220, 170, 150)],
        [(45, 48, 55), (85, 92, 102), (135, 142, 152), (195, 202, 212)],
        [(60, 45, 75), (105, 80, 130), (155, 125, 185), (205, 180, 230)],
        [(75, 45, 25), (130, 82, 48), (180, 125, 78), (225, 175, 125)],
        [(110, 90, 65), (165, 140, 105), (205, 185, 150), (240, 225, 195)],
        [(65, 70, 80), (120, 130, 145), (180, 190, 205), (235, 240, 250)],
        [(110, 75, 20), (180, 130, 35), (235, 185, 55), (255, 230, 130)],
        [(140, 85, 65), (195, 130, 105), (235, 175, 145), (255, 215, 190)],
        [(100, 20, 30), (175, 35, 45), (230, 65, 70), (255, 135, 130)],
        [(20, 45, 95), (35, 85, 165), (65, 140, 230), (145, 195, 255)],
        [(15, 50, 85), (30, 105, 155), (65, 175, 215), (180, 240, 255)],
        [(70, 130, 200), (120, 175, 235), (180, 215, 250), (245, 250, 255)],
        [(110, 25, 80), (185, 45, 135), (235, 95, 185), (255, 175, 225)],
    ]
    
    palette_data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    row_height = HEIGHT // len(ramps)
    
    for row_idx, ramp in enumerate(ramps):
        y_start = row_idx * row_height
        y_end = (row_idx + 1) * row_height if row_idx < len(ramps) - 1 else HEIGHT
        
        num_stops = len(ramp)
        step_w = WIDTH / (num_stops - 1)
        for x in range(WIDTH):
            stop_idx = min(int(x / step_w), num_stops - 2)
            frac = (x - stop_idx * step_w) / step_w
            c0 = np.array(ramp[stop_idx], dtype=np.float32)
            c1 = np.array(ramp[stop_idx + 1], dtype=np.float32)
            c = c0 + (c1 - c0) * frac
            palette_data[y_start:y_end, x] = np.clip(c, 0, 255).astype(np.uint8)
            
    img_palette = Image.fromarray(palette_data)
    img_palette.save(os.path.join(OUTPUT_PALETTES, "palette_standard_stylized.png"))
    print("✓ Đã tạo palette_standard_stylized.png")

if __name__ == "__main__":
    print("Bắt đầu sinh bộ Texture nền tảng...")
    make_grass_textures()
    make_dirt_textures()
    make_rock_textures()
    make_wood_textures()
    make_metal_textures()
    make_palette_texture()
    print("Hoàn tất sinh Texture!")
