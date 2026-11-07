"""
Script Python: Tinh chỉnh cắt xén sạch sẽ 100% cho 8 Sprite NPC và Avatar Chân Dung.
"""

import os
import numpy as np
from PIL import Image

def clean_and_extract_perfect():
    src_path = os.path.abspath("modelyeucau/map2/1.jpg")
    out_dir = os.path.abspath("Assets/Textures/NPCs")
    os.makedirs(out_dir, exist_ok=True)

    img = Image.open(src_path).convert("RGB")

    # Tọa độ bounding box hoàn hảo từng nhân vật
    # [xmin, ymin, xmax, ymax]
    npc_configs = {
        "blacksmith": {
            "box": [35, 1065, 275, 1425],
            "avatar_box": [65, 1070, 245, 1260]
        },
        "alchemist": {
            "box": [290, 1065, 525, 1425],
            "avatar_box": [325, 1070, 485, 1260]
        },
        "chef": {
            "box": [540, 1030, 755, 1425],
            "avatar_box": [565, 1030, 730, 1220]
        },
        "farmer": {
            # Bắt đầu từ X=825 để loại bỏ hoàn toàn vạc thuốc bên trái
            "box": [825, 1045, 1015, 1425],
            "avatar_box": [825, 1050, 965, 1240]
        },
        "fisherman": {
            # Ymin=1030 để bỏ lá cây trên đỉnh
            "box": [1050, 1030, 1245, 1425],
            "avatar_box": [1075, 1060, 1235, 1250]
        },
        "miner": {
            # Bắt đầu từ X=1330 để loại bỏ mảng tường trắng bên trái
            "box": [1330, 1055, 1485, 1425],
            "avatar_box": [1330, 1055, 1470, 1240]
        },
        "lumberjack": {
            "box": [1520, 1040, 1725, 1425],
            "avatar_box": [1550, 1050, 1710, 1240]
        },
        "guard": {
            "box": [1785, 1020, 1980, 1425],
            "avatar_box": [1810, 1040, 1970, 1230]
        }
    }

    bg_r, bg_g, bg_b = 244, 243, 228

    def process_crop(crop_img, threshold=42, feather=18):
        arr = np.array(crop_img.convert("RGBA"))
        r = arr[:, :, 0].astype(float)
        g = arr[:, :, 1].astype(float)
        b = arr[:, :, 2].astype(float)

        dist = np.sqrt((r - bg_r)**2 + (g - bg_g)**2 + (b - bg_b)**2)

        alpha = np.zeros_like(dist)
        solid_mask = dist >= (threshold + feather)
        blend_mask = (dist >= threshold) & (dist < threshold + feather)

        alpha[solid_mask] = 255
        alpha[blend_mask] = ((dist[blend_mask] - threshold) / feather * 255.0).astype(np.uint8)

        arr[:, :, 3] = alpha.astype(np.uint8)
        res = Image.fromarray(arr, "RGBA")
        
        bbox = res.getbbox()
        if bbox:
            res = res.crop(bbox)
        return res

    preview_sprites = []

    for name, cfg in npc_configs.items():
        crop = img.crop(cfg["box"])
        sprite_rgba = process_crop(crop)

        # Lưu sprite
        sprite_out = os.path.join(out_dir, f"sprite_{name}.png")
        sprite_rgba.save(sprite_out, "PNG")
        print(f"-> Sprite: {sprite_out} ({sprite_rgba.size})")

        # Cắt avatar
        av_crop = img.crop(cfg["avatar_box"])
        av_rgba = process_crop(av_crop, threshold=38, feather=15)
        
        # Fit vào 160x160
        av_final = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        aw, ah = av_rgba.size
        scale = min(140.0 / aw, 140.0 / ah)
        nw, nh = int(aw * scale), int(ah * scale)
        av_resized = av_rgba.resize((nw, nh), Image.Resampling.LANCZOS)
        av_final.paste(av_resized, ((160 - nw) // 2, (160 - nh) // 2), av_resized)

        av_out = os.path.join(out_dir, f"avatar_{name}.png")
        av_final.save(av_out, "PNG")
        print(f"-> Avatar: {av_out}")

        preview_sprites.append((name, sprite_rgba))

    # Ghép ảnh Preview
    total_w = sum(s.size[0] + 25 for _, s in preview_sprites) + 25
    max_h = max(s.size[1] for _, s in preview_sprites) + 40
    comp = Image.new("RGBA", (total_w, max_h), (30, 32, 38, 255))
    cur_x = 25
    for name, s in preview_sprites:
        y_pos = max_h - s.size[1] - 20
        comp.paste(s, (cur_x, y_pos), s)
        cur_x += s.size[0] + 25

    preview_file = os.path.join(out_dir, "_npcs_extracted_preview.png")
    comp.save(preview_file, "PNG")
    print(f"=== ĐÃ XUẤT ẢNH PREVIEW HOÀN HẢO: {preview_file} ===")

if __name__ == "__main__":
    clean_and_extract_perfect()
