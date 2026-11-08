"""
Ghép bộ ảnh kiểm tra thị giác Mắt Thần thành file tổng thể Assets/Models/_preview_render.png
Bố cục đối chiếu song song chuẩn 100% theo bản vẽ modelyeucau/map2/1.jpg:
- Bên trái: Bản đồ toàn cảnh làng mở rộng cực hạn (Village Overview & 10 Street Lanterns & 8 NPCs)
- Bên phải (Lưới 3x2):
  1. Nội thất Nhà Rèn (Smithy Diorama)
  2. Nội thất Nhà Giả Kim (Alchemist Diorama)
  3. Nội thất Quán Ăn / Bếp (Chef Tavern Diorama)
  4. Nội thất Nhà Dân Cư (House Diorama)
  5. Nội thất Nhà Trưởng Làng / Kho Dự Trữ Lương Thực (Elder Hall & Storehouse Diorama)
  6. Mô hình Cánh Cửa Gỗ Stylized 2 Mặt (Wooden Door 3D Front & Back)
"""

import os
from PIL import Image, ImageDraw

def compose_preview():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    temp_dir = os.path.join(base_dir, "Assets", "Models", "_temp_previews")
    out_path = os.path.join(base_dir, "Assets", "Models", "_preview_render.png")

    p_village = os.path.join(temp_dir, "preview_village.png")
    p_smith = os.path.join(temp_dir, "preview_interior_smith.png")
    p_alchemist = os.path.join(temp_dir, "preview_interior_alchemist.png")
    p_chef = os.path.join(temp_dir, "preview_interior_chef.png")
    p_house = os.path.join(temp_dir, "preview_interior_house.png")
    p_elder = os.path.join(temp_dir, "preview_interior_elder.png")
    p_door = os.path.join(base_dir, "Assets", "Models", "_door_preview.png")

    if not os.path.exists(p_village):
        print(f"Không tìm thấy file: {p_village}")
        return

    img_village = Image.open(p_village).convert("RGB")
    img_village = img_village.resize((1280, 960), Image.Resampling.LANCZOS)

    # Kích thước mỗi ô lưới bên phải: 470x310
    w_box, h_box = 470, 310
    def load_tile(p):
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            return im.resize((w_box, h_box), Image.Resampling.LANCZOS)
        return Image.new("RGB", (w_box, h_box), (40, 40, 45))

    img_smith = load_tile(p_smith)
    img_alchemist = load_tile(p_alchemist)
    img_chef = load_tile(p_chef)
    img_house = load_tile(p_house)
    img_elder = load_tile(p_elder)
    img_door = load_tile(p_door)

    canvas_w = 1280 + 960 + 30
    canvas_h = 960 + 60
    canvas = Image.new("RGB", (canvas_w, canvas_h), (25, 27, 30))
    draw = ImageDraw.Draw(canvas)

    # Dán Toàn Cảnh Làng vào bên trái
    canvas.paste(img_village, (10, 50))

    # Dán 6 ô nội thất & model vào bên phải theo lưới 3 hàng x 2 cột
    rx = 1305
    col_w = w_box + 10
    row_h = h_box + 15

    # Hàng 1
    canvas.paste(img_smith, (rx, 50))
    canvas.paste(img_alchemist, (rx + col_w, 50))

    # Hàng 2
    canvas.paste(img_chef, (rx, 50 + row_h))
    canvas.paste(img_house, (rx + col_w, 50 + row_h))

    # Hàng 3
    canvas.paste(img_elder, (rx, 50 + row_h * 2))
    canvas.paste(img_door, (rx + col_w, 50 + row_h * 2))

    # Đường viền ngăn cách
    border_col = (70, 75, 85)
    draw.rectangle([10, 50, 1290, 1010], outline=border_col, width=2)
    for r in range(3):
        for c in range(2):
            bx = rx + c * col_w
            by = 50 + r * row_h
            draw.rectangle([bx, by, bx + w_box, by + h_box], outline=border_col, width=2)

    # Tiêu đề nhãn chữ
    draw.text((30, 16), "BAN DO TOAN CANH LANG MO RONG, 10 TRU DEN DUONG & 8 NPC (modelyeucau/map2/1.jpg)", fill=(240, 240, 245))
    draw.text((rx + 20, 16), "5 PHONG NOI THAT DIORAMA CAT VACH & MO HINH CANH CUA GO 3D", fill=(255, 215, 100))

    # Nhãn từng ô
    def draw_badge(x, y, text, color):
        draw.rectangle([x, y, x + 230, y + 26], fill=(20, 20, 25, 210))
        draw.text((x + 8, y + 5), text, fill=color)

    draw_badge(rx + 6, 56, "1. NOI THAT NHA REN", (255, 150, 80))
    draw_badge(rx + col_w + 6, 56, "2. NOI THAT NHA GIA KIM", (100, 240, 220))
    draw_badge(rx + 6, 56 + row_h, "3. NOI THAT QUAN AN / BEP", (255, 220, 120))
    draw_badge(rx + col_w + 6, 56 + row_h, "4. NOI THAT NHA DAN CU", (240, 160, 200))
    draw_badge(rx + 6, 56 + row_h * 2, "5. NHA TRUONG LANG / KHO", (140, 220, 140))
    draw_badge(rx + col_w + 6, 56 + row_h * 2, "6. CANH CUA GO STYLIZED", (255, 200, 90))

    canvas.save(out_path, quality=95)
    print(f"-> Đã ghép ảnh Mắt Thần đối chiếu song song thành công: {out_path}")

if __name__ == '__main__':
    compose_preview()
