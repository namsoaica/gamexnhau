"""
Loại bỏ triệt để các đốm lẻ tẻ còn lại trên Farmer, Fisherman, Miner.
"""

import os
from PIL import Image
import numpy as np

out_dir = os.path.abspath("Assets/Textures/NPCs")

def polish_clean():
    # 1. Farmer
    f_path = os.path.join(out_dir, "sprite_farmer.png")
    img = Image.open(f_path).convert("RGBA")
    arr = np.array(img)
    # Xóa đốm xanh lá ở đỉnh trên nón lá (Y < 50)
    for y in range(min(50, arr.shape[0])):
        for x in range(arr.shape[1]):
            r, g, b, a = arr[y, x]
            if g > 100 and g > r:
                arr[y, x, 3] = 0
    # Xóa mảnh kệ gỗ ở góc dưới-trái (Y > 180, X < 35)
    for y in range(180, arr.shape[0]):
        for x in range(min(35, arr.shape[1])):
            arr[y, x, 3] = 0
    img_clean = Image.fromarray(arr, "RGBA")
    bbox = img_clean.getbbox()
    if bbox:
        img_clean = img_clean.crop(bbox)
    img_clean.save(f_path, "PNG")

    # 2. Fisherman
    fish_path = os.path.join(out_dir, "sprite_fisherman.png")
    img = Image.open(fish_path).convert("RGBA")
    arr = np.array(img)
    # Xóa vệt mờ bên phải giỏ cá (X > arr.shape[1] - 25, Y > 200)
    for y in range(200, arr.shape[0]):
        for x in range(max(0, arr.shape[1] - 25), arr.shape[1]):
            r, g, b, a = arr[y, x]
            # Giỏ cá màu nâu đậm (R~120, G~80, B~40). Vết mờ là màu kem/xám nhạt (R > 180, G > 180)
            if r > 160 and g > 150:
                arr[y, x, 3] = 0
    img_clean = Image.fromarray(arr, "RGBA")
    bbox = img_clean.getbbox()
    if bbox:
        img_clean = img_clean.crop(bbox)
    img_clean.save(fish_path, "PNG")

    # 3. Miner
    m_path = os.path.join(out_dir, "sprite_miner.png")
    img = Image.open(m_path).convert("RGBA")
    arr = np.array(img)
    # Xóa chữ 'i mi' bên phải trên (X > arr.shape[1] - 45, Y < 100)
    for y in range(min(100, arr.shape[0])):
        for x in range(max(0, arr.shape[1] - 50), arr.shape[1]):
            # Nếu không phải lưỡi cuốc chim (màu xám xanh kim loại R~120, G~130, B~150)
            r, g, b, a = arr[y, x]
            if r < 80 and g < 80 and b < 80 and y < 80: # Chữ màu đen xám
                arr[y, x, 3] = 0
    img_clean = Image.fromarray(arr, "RGBA")
    bbox = img_clean.getbbox()
    if bbox:
        img_clean = img_clean.crop(bbox)
    img_clean.save(m_path, "PNG")

    # 4. Guard: Xóa thanh giáo kéo dài xuống đất bên trái nếu có
    g_path = os.path.join(out_dir, "sprite_guard.png")
    img = Image.open(g_path).convert("RGBA")
    arr = np.array(img)
    # Cắt gọn mép trên nếu có vệt đen
    for x in range(arr.shape[1]):
        for y in range(min(15, arr.shape[0])):
            r, g, b, a = arr[y, x]
            if x < arr.shape[1] // 2 and y < 10:
                # Chỉ giữ mũi giáo nhọn
                if not (x > 10 and x < 35):
                    arr[y, x, 3] = 0
    img_clean = Image.fromarray(arr, "RGBA")
    bbox = img_clean.getbbox()
    if bbox:
        img_clean = img_clean.crop(bbox)
    img_clean.save(g_path, "PNG")

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
    print(f"=== ĐÃ HOÀN TẤT CHẢI CHUỐT TỐI THƯỢNG: {preview_file} ===")

if __name__ == "__main__":
    polish_clean()
