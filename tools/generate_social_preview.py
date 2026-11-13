"""Build the Open Graph / social sharing card from local portfolio images.
Run from the project root with Pillow installed: python tools/generate_social_preview.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "social-preview.jpg"
W, H = 1200, 630
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def cover(image, size):
    scale = max(size[0] / image.width, size[1] / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (image.width - size[0]) // 2
    top = (image.height - size[1]) // 2
    return image.crop((left, top, left + size[0], top + size[1]))


def main():
    bg = Image.open(ROOT / "assets/images/anime-background.jpg").convert("RGB")
    bg = cover(bg, (W, H)).filter(ImageFilter.GaussianBlur(2.2))
    bg = ImageEnhance.Color(bg).enhance(0.58)
    bg = ImageEnhance.Contrast(bg).enhance(0.88)
    base = bg.convert("RGBA")

    # Dark red-black cinematic wash, keeping the anime frame recognizable.
    wash = Image.new("RGBA", (W, H), (4, 5, 9, 105))
    base.alpha_composite(wash)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = shade.load()
    for x in range(W):
        # Keep text legible at left; leave some light from the original scene on the right.
        a = int(226 - 94 * (x / W))
        for y in range(H):
            px[x, y] = (8, 7, 11, a)
    base.alpha_composite(shade)

    # A restrained crimson glow behind the portrait.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((745, 72, 1190, 535), fill=(180, 23, 39, 72))
    glow = glow.filter(ImageFilter.GaussianBlur(72))
    base.alpha_composite(glow)

    # Chess-board motif, subtly receding into the lower/right side.
    board = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(board)
    tile = 54
    x0, y0 = 700, 358
    for row in range(6):
        for col in range(10):
            if (row + col) % 2 == 0:
                x1, y1 = x0 + col * tile, y0 + row * tile
                alpha = max(7, 24 - row * 2)
                bd.rectangle((x1, y1, x1 + tile, y1 + tile), fill=(218, 205, 197, alpha))
    for i in range(11):
        x = x0 + i * tile
        bd.line((x, y0, x, y0 + 6 * tile), fill=(239, 226, 220, 24), width=1)
    for i in range(7):
        y = y0 + i * tile
        bd.line((x0, y, x0 + 10 * tile, y), fill=(239, 226, 220, 24), width=1)
    base.alpha_composite(board)

    # Fine grain adds a printed, cinematic finish without obscuring the type.
    random.seed(12)
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grain)
    for _ in range(4200):
        x, y = random.randrange(W), random.randrange(H)
        a = random.randrange(3, 12)
        c = 255 if random.random() > 0.52 else 0
        gdraw.point((x, y), fill=(c, c, c, a))
    base.alpha_composite(grain)

    # Portrait, with shadow, chess-red rim, and a clean inner keyline.
    portrait = Image.open(ROOT / "assets/images/matin-avatar.jpg").convert("RGB")
    portrait = cover(portrait, (316, 316))
    circle = Image.new("L", (316, 316), 0)
    ImageDraw.Draw(circle).ellipse((0, 0, 315, 315), fill=255)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((773, 127, 1123, 477), fill=(0, 0, 0, 185))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    base.alpha_composite(shadow)

    draw = ImageDraw.Draw(base)
    draw.ellipse((760, 114, 1136, 490), fill=(9, 8, 12, 255), outline=(224, 54, 66, 255), width=4)
    draw.ellipse((771, 125, 1125, 479), outline=(255, 222, 213, 170), width=1)
    portrait_layer = Image.new("RGBA", (316, 316), (0, 0, 0, 0))
    portrait_layer.paste(portrait, (0, 0), circle)
    base.alpha_composite(portrait_layer, (790, 144))
    draw = ImageDraw.Draw(base)
    draw.ellipse((790, 144, 1106, 460), outline=(246, 241, 236, 210), width=2)

    # Small chess markers on the portrait frame.
    draw.ellipse((1088, 176, 1158, 246), fill=(12, 11, 15, 245), outline=(226, 55, 67, 255), width=2)
    draw.text((1123, 211), "♟", font=font(FONT_BOLD, 35), fill=(246, 232, 224, 255), anchor="mm")
    draw.ellipse((752, 382, 810, 440), fill=(12, 11, 15, 245), outline=(226, 55, 67, 210), width=2)
    draw.text((781, 411), "♞", font=font(FONT_BOLD, 28), fill=(246, 232, 224, 245), anchor="mm")

    # Brand label and subtle rule.
    draw.rounded_rectangle((74, 66, 356, 105), radius=18, fill=(20, 17, 22, 218), outline=(218, 56, 68, 180), width=1)
    draw.text((93, 86), "♟  OSTOVAR04 / PORTFOLIO", font=font(FONT_MONO_BOLD, 14), fill=(244, 221, 214, 255), anchor="lm")
    draw.text((72, 135), "MATIN", font=font(FONT_BOLD, 92), fill=(250, 246, 241, 255), stroke_width=1, stroke_fill=(15, 10, 13, 100))
    draw.rounded_rectangle((77, 253, 318, 260), radius=3, fill=(226, 54, 67, 255))

    # Persian tagline, shaped right-to-left by Pillow's RAQM text engine.
    draw.text((690, 325), "هر حرکت، حساب‌شده", font=font(FONT_BOLD, 34), fill=(255, 243, 238, 255), direction="rtl", anchor="ra", language="fa")
    draw.text((75, 329), "SOFTWARE DEVELOPER", font=font(FONT_MONO_BOLD, 19), fill=(239, 94, 102, 255))
    draw.text((75, 363), "WEB DESIGNER  /  PYTHON · AI · DJANGO", font=font(FONT_MONO, 14), fill=(213, 204, 199, 245))

    # Contact-like handle badge and a short signature line.
    draw.rounded_rectangle((75, 456, 363, 506), radius=8, fill=(19, 17, 21, 205), outline=(245, 239, 232, 70), width=1)
    draw.rounded_rectangle((88, 467, 127, 495), radius=5, fill=(205, 42, 55, 255))
    draw.text((107, 481), "GH", font=font(FONT_MONO_BOLD, 13), fill=(255, 249, 244, 255), anchor="mm")
    draw.text((143, 481), "@OSTOVAR04", font=font(FONT_MONO_BOLD, 16), fill=(246, 239, 232, 255), anchor="lm")
    draw.text((75, 553), "OBSERVE  /  PLAN  /  BUILD", font=font(FONT_MONO_BOLD, 12), fill=(209, 193, 188, 215))
    draw.text((1122, 548), "E4 · MOVE WITH INTENT", font=font(FONT_MONO, 10), fill=(232, 198, 190, 205), anchor="ra")

    # Fine border and corner marks.
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((14, 14, W - 15, H - 15), radius=18, outline=(245, 237, 231, 70), width=1)
    for x, y, sx, sy in [(35, 35, 1, 1), (W-35, 35, -1, 1), (35, H-35, 1, -1), (W-35, H-35, -1, -1)]:
        draw.line((x, y, x + sx*25, y), fill=(227, 53, 66, 210), width=2)
        draw.line((x, y, x, y + sy*25), fill=(227, 53, 66, 210), width=2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT, "JPEG", quality=91, optimize=True, progressive=True)
    print(f"Created {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
