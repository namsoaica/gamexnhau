import os
from PIL import Image
import numpy as np

img_path = "modelyeucau/map2/1.jpg"
img = Image.open(img_path).convert("RGB")
width, height = img.size
print(f"Image dimensions: {width}x{height}")

# Sample specific key areas based on coordinates in 1.jpg (normalized or pixel coordinates)
# We can define sample boxes or points
# In 1.jpg (width=2048, height=1536 approx):
# Let's inspect coordinates

samples = {
    "grass": (int(width * 0.25), int(height * 0.15)), # Green grass
    "dirt_road": (int(width * 0.40), int(height * 0.48)), # Dirt road
    "roof_red": (int(width * 0.32), int(height * 0.29)), # Red roof blacksmith
    "roof_teal": (int(width * 0.52), int(height * 0.35)), # Teal roof alchemist
    "rock_cliff": (int(width * 0.56), int(height * 0.12)), # Rock cliff at mine
    "wood_beam": (int(width * 0.28), int(height * 0.37)), # Wood beam / fence
    "smoke_cyan": (int(width * 0.55), int(height * 0.26)), # Magic cyan smoke
    "lava_fire": (int(width * 0.26), int(height * 0.37)), # Forge fire
    "canopy_red": (int(width * 0.41), int(height * 0.39)), # Market stall red stripe
    "canopy_white": (int(width * 0.42), int(height * 0.38)), # Market stall white stripe
    # NPCs along bottom row (approx y=85% to 92%)
    "npc_vulcan_apron": (int(width * 0.09), int(height * 0.83)),
    "npc_aria_cloak": (int(width * 0.21), int(height * 0.83)),
    "npc_gusteau_hat": (int(width * 0.33), int(height * 0.74)),
    "npc_george_hat": (int(width * 0.45), int(height * 0.75)),
    "npc_finn_hat": (int(width * 0.57), int(height * 0.76)),
    "npc_brock_suit": (int(width * 0.70), int(height * 0.83)),
    "npc_grover_shirt": (int(width * 0.82), int(height * 0.80)),
    "npc_aegis_armor": (int(width * 0.93), int(height * 0.83)),
}

print("\n--- EXTRACTED COLOR SAMPLES ---")
results = {}
for name, (x, y) in samples.items():
    # Take 5x5 average around pixel
    box = (max(0, x-2), max(0, y-2), min(width, x+3), min(height, y+3))
    crop = img.crop(box)
    arr = np.array(crop)
    avg_rgb = arr.mean(axis=(0, 1)).astype(int)
    hex_code = "#{:02X}{:02X}{:02X}".format(avg_rgb[0], avg_rgb[1], avg_rgb[2])
    norm_rgb = tuple(round(c / 255.0, 3) for c in avg_rgb)
    results[name] = {"hex": hex_code, "rgb255": tuple(avg_rgb), "rgb_norm": norm_rgb}
    print(f"{name:20s}: Hex={hex_code} | RGB={tuple(avg_rgb)} | Norm={norm_rgb}")

# Save palette summary to text
with open("Assets/Textures/extracted_map2_palette.py", "w", encoding="utf-8") as f:
    f.write("# Tự động trích xuất bảng màu từ modelyeucau/map2/1.jpg\n")
    f.write("PALETTE = {\n")
    for k, v in results.items():
        f.write(f'    "{k}": {v},\n')
    f.write("}\n")

print("\nPalette successfully saved to Assets/Textures/extracted_map2_palette.py")
