"""
Chải chuốt tinh vi cho Farmer, Fisherman, Miner để triệt tiêu 100% vệt nền thừa.
"""

import os
from PIL import Image
import numpy as np

out_dir = os.path.abspath("Assets/Textures/NPCs")

def refine_sprites():
    # 1. Farmer: Xóa vệt bàn thuốc ở bên trái
    f_path = os.path.join(out_dir, "sprite_farmer.png")
    img = Image.open(f_path).convert("RGBA")
    arr = np.array(img)
    # Bàn thuốc nằm ở góc trên-trái (X < 55, Y < 300)
    for y in range(arr.shape[0]):
        for x in range(min(55, arr.shape[1])):
            # Nếu không phải là cánh tay áo hay đòn cuốc (màu nâu/gỗ)
            r, g, b, a = arr[y, x]
            if a > 0:
                # Vệt bàn thuốc có màu tím/xanh nhạt của vạc hoặc kệ gỗ nhạt
                if x < 40 or y < 140:
                    arr[y, x, 3] = 0
    img_clean = Image.fromarray(arr, "RGBA")
    bbox = img_clean.getbbox()
    if bbox:
        img_clean = img_clean.crop(bbox)
    img_clean.save(f_path, "PNG")

    # 2. Fisherman: Xóa miếng lá xanh trên đỉnh
    fish_path = os.path.join(out_dir, "sprite_fisherman.png")
    img = Image.open(fish_path).convert("RGBA")
    arr = np.array(img)
    # Lá cây xanh ở đỉnh (Y < 40, X < 100)
    for y in range(min(45, arr.shape[0])):
        for x in range(min(90, arr.shape[1])):
            r, g, b, a = arr[y, x]
            if g > r and g > b: # Màu xanh lá cây
                arr[y, x, 3] = 0
    img_clean = Image.fromarray(arr, "RGBA")
    bbox = img_clean.getbbox()
    if bbox:
        img_clean = img_clean.crop(bbox)
    img_clean.save(fish_path, "PNG")

    # 3. Miner: Xóa vệt tường trắng bên trái và chữ trên đỉnh
    m_path = os.path.join(out_dir, "sprite_miner.png")
    img = Image.open(m_path).convert("RGBA")
    arr = np.array(img)
    # Tường trắng bên trái (X < 25)
    for y in range(arr.shape[0]):
        for x in range(min(25, arr.shape[1])):
            arr[y, x, 3] = 0
    # Chữ trên đỉnh (Y < 35, X > 40)
    for y in range(min(40, arr.shape[0])):
        for x in range(arr.shape[1]):
            # Nếu không phải mũ bảo hộ vàng (vàng có R > 200, G > 180, B < 80)
            r, g, b, a = arr[y, x]
            if not (r > 190 and g > 160 and b < 80):
                arr[y, x, 3] = 0
    img_clean = Image.fromarray(arr, "RGBA")
    bbox = img_clean.getbbox()
    if bbox:
        img_clean = img_clean.crop(bbox)
    img_clean.save(m_path, "PNG")

    # Ghép lại Preview
    sprites = []
    names = ["blacksmith", "alchemist", "chef", "farmer", "fisherman", "miner", "lumberjack", "guard"]
    for n in names:
        sp = Image.open(os.path.join(out_dir, f"sprite_{n}.png"))
        sprites.append((n, sp))

    total_w = sum(s.size[0] + 25 for _, s in sprites) + 25
    max_h = max(s.size[1] for _, s in sprites) + 40
    comp = Image.new("RGBA", (total_w, max_h), (30, 32, 38, 255))
    cur_x = 25
    for name, s in sprites:
        y_pos = max_h - s.size[1] - 20
        comp.paste(s, (cur_x, y_pos), s)
        cur_x += s.size[0] + 25

    preview_file = os.path.join(out_dir, "_npcs_extracted_preview.png")
    comp.save(preview_file, "PNG")
    print(f"=== ĐÃ LÀM SẠCH VÀ LƯU PREVIEW MỚI: {preview_file} ===")

if __name__ == "__main__":
    refine_sprites()
