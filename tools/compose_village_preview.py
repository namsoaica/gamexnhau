"""
Ghép bộ ảnh kiểm tra thị giác Mắt Thần thành file tổng thể Assets/Models/_preview_render.png
Bố cục đối chiếu song song chuẩn 100% theo bản vẽ modelyeucau/map2/1.jpg:
- Bên trái: Bản đồ toàn cảnh làng (Village Overview)
- Bên phải: 4 phòng diorama nội thất cắt vách (Nhà Rèn, Nhà Giả Kim, Quán Ăn, Nhà Dân)
"""

import os
from PIL import Image, ImageDraw, ImageFont

def compose_preview():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    temp_dir = os.path.join(base_dir, "Assets", "Models", "_temp_previews")
    out_path = os.path.join(base_dir, "Assets", "Models", "_preview_render.png")

    p_village = os.path.join(temp_dir, "preview_village.png")
    p_smith = os.path.join(temp_dir, "preview_interior_smith.png")
    p_alchemist = os.path.join(temp_dir, "preview_interior_alchemist.png")
    p_chef = os.path.join(temp_dir, "preview_interior_chef.png")
    p_house = os.path.join(temp_dir, "preview_interior_house.png")

    if not os.path.exists(p_village):
        print(f"Không tìm thấy file: {p_village}")
        return

    img_village = Image.open(p_village).convert("RGB")
    # Resize village view to 1280x960
    img_village = img_village.resize((1280, 960), Image.Resampling.LANCZOS)

    # Kích thước mỗi phòng nội thất: 480x480
    w_room, h_room = 480, 480
    def load_room(p):
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            return im.resize((w_room, h_room), Image.Resampling.LANCZOS)
        return Image.new("RGB", (w_room, h_room), (40, 40, 45))

    img_smith = load_room(p_smith)
    img_alchemist = load_room(p_alchemist)
    img_chef = load_room(p_chef)
    img_house = load_room(p_house)

    # Master canvas: Width = 1280 + 960 = 2240, Height = 960 + 60 (header banner) = 1020
    canvas_w = 1280 + 960 + 20
    canvas_h = 960 + 60
    canvas = Image.new("RGB", (canvas_w, canvas_h), (28, 30, 34))
    draw = ImageDraw.Draw(canvas)

    # Dán Bản đồ toàn cảnh làng vào bên trái
    canvas.paste(img_village, (10, 50))

    # Dán 4 phòng nội thất vào góc bên phải (lưới 2x2)
    right_x = 1300
    canvas.paste(img_smith, (right_x, 50))
    canvas.paste(img_alchemist, (right_x + 480, 50))
    canvas.paste(img_chef, (right_x, 530))
    canvas.paste(img_house, (right_x + 480, 530))

    # Vẽ đường viền ngăn cách tinh tế
    border_col = (70, 75, 85)
    draw.rectangle([10, 50, 1290, 1010], outline=border_col, width=2)
    draw.rectangle([right_x, 50, right_x + 480, 530], outline=border_col, width=2)
    draw.rectangle([right_x + 480, 50, right_x + 960, 530], outline=border_col, width=2)
    draw.rectangle([right_x, 530, right_x + 480, 1010], outline=border_col, width=2)
    draw.rectangle([right_x + 480, 530, right_x + 960, 1010], outline=border_col, width=2)

    # Tiêu đề nhãn chữ
    draw.text((30, 16), "BAN DO TOAN CANH LANG & 8 NPC STYLIZED (modelyeucau/map2/1.jpg)", fill=(240, 240, 245))
    draw.text((right_x + 20, 16), "CHI TIET 4 PHONG NOI THAT DIORAMA CAT VACH", fill=(255, 215, 100))
    
    # Nhãn từng phòng
    draw.rectangle([right_x + 8, 58, right_x + 230, 88], fill=(20, 20, 25, 200))
    draw.text((right_x + 16, 64), "1. NOI THAT NHA REN", fill=(255, 150, 80))

    draw.rectangle([right_x + 488, 58, right_x + 750, 88], fill=(20, 20, 25, 200))
    draw.text((right_x + 496, 64), "2. NOI THAT NHA GIA KIM", fill=(100, 240, 220))

    draw.rectangle([right_x + 8, 538, right_x + 290, 568], fill=(20, 20, 25, 200))
    draw.text((right_x + 16, 544), "3. NOI THAT QUAN AN / BEP", fill=(255, 220, 120))

    draw.rectangle([right_x + 488, 538, right_x + 730, 568], fill=(20, 20, 25, 200))
    draw.text((right_x + 496, 544), "4. NOI THAT NHA DAN CU", fill=(240, 160, 200))

    canvas.save(out_path, quality=95)
    print(f"-> Đã ghép ảnh Mắt Thần đối chiếu song song thành công: {out_path}")

if __name__ == '__main__':
    compose_preview()
