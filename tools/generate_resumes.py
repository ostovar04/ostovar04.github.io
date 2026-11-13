"""Generate one-page Persian and English CV PDFs for Matin.

From the project root, run:
    python tools/generate_resumes.py
Dependencies: reportlab, arabic-reshaper, python-bidi, qrcode[pil].
"""
from io import BytesIO
from pathlib import Path

import arabic_reshaper
import qrcode
from bidi.algorithm import get_display
from PIL import Image, ImageDraw
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cv"
FONTS = ROOT / "assets" / "fonts"
AVATAR = ROOT / "assets" / "images" / "matin-avatar.jpg"
PAGE_W, PAGE_H = A4

INK = colors.HexColor("#17171B")
DARK = colors.HexColor("#111115")
RED = colors.HexColor("#C93440")
RED_BRIGHT = colors.HexColor("#E34A55")
PAPER = colors.HexColor("#FAF9F7")
CARD = colors.HexColor("#FFFFFF")
SOFT = colors.HexColor("#F3F0ED")
TEXT = colors.HexColor("#29282C")
MUTED = colors.HexColor("#6A676B")
LINE = colors.HexColor("#E6E0DC")
WHITE = colors.white

FONT_FA = "VazirResume"
FONT_FA_BOLD = "VazirResume-Bold"
FONT_LATIN = "SpaceResume"
FONT_LATIN_BOLD = "SpaceResume-Bold"


def register_fonts():
    pdfmetrics.registerFont(TTFont(FONT_FA, str(FONTS / "vazirmatn-pdf-regular.ttf")))
    pdfmetrics.registerFont(TTFont(FONT_FA_BOLD, str(FONTS / "vazirmatn-pdf-bold.ttf")))
    pdfmetrics.registerFont(TTFont(FONT_LATIN, str(FONTS / "space-grotesk-pdf-regular.ttf")))
    pdfmetrics.registerFont(TTFont(FONT_LATIN_BOLD, str(FONTS / "space-grotesk-pdf-bold.ttf")))


def shape_fa(text):
    return get_display(arabic_reshaper.reshape(text), base_dir="R")


def width_of(text, face, size, fa=False):
    return pdfmetrics.stringWidth(shape_fa(text) if fa else text, face, size)


def wrap_text(text, face, size, max_width, fa=False):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and width_of(candidate, face, size, fa) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_paragraph(c, text, x, top, width, face, size, leading, color=TEXT, fa=False, max_lines=None):
    lines = wrap_text(text, face, size, width, fa)
    if max_lines:
        lines = lines[:max_lines]
    c.setFillColor(color)
    y = top - size
    for line in lines:
        if fa:
            c.setFont(face, size)
            c.drawRightString(x + width, y, shape_fa(line))
        else:
            c.setFont(face, size)
            c.drawString(x, y, line)
        y -= leading
    return y


def draw_section(c, x, y, width, number, title, fa):
    c.setFillColor(RED)
    c.roundRect(x, y - 2, 18, 16, 4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_LATIN_BOLD, 7)
    c.drawCentredString(x + 9, y + 3, number)
    c.setFillColor(INK)
    if fa:
        c.setFont(FONT_FA_BOLD, 10)
        c.drawRightString(x + width, y + 1, shape_fa(title))
    else:
        c.setFont(FONT_LATIN_BOLD, 10)
        c.drawString(x + 26, y + 1, title.upper())
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(x, y - 8, x + width, y - 8)


def draw_fa(c, text, x_right, y, face, size, color=TEXT):
    c.setFont(face, size)
    c.setFillColor(color)
    c.drawRightString(x_right, y, shape_fa(text))


def draw_link(c, text, x, y, url, face=FONT_LATIN, size=7.1, color=RED, align="left"):
    c.setFont(face, size)
    c.setFillColor(color)
    if align == "right":
        c.drawRightString(x, y, text)
        width = pdfmetrics.stringWidth(text, face, size)
        rect = (x - width, y - 2, x, y + size + 2)
    else:
        c.drawString(x, y, text)
        width = pdfmetrics.stringWidth(text, face, size)
        rect = (x, y - 2, x + width, y + size + 2)
    c.linkURL(url, rect, relative=0, thickness=0)


def make_avatar_png():
    image = Image.open(AVATAR).convert("RGB")
    side = 360
    scale = max(side / image.width, side / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (image.width - side) // 2
    top = (image.height - side) // 2
    image = image.crop((left, top, left + side, top + side)).convert("RGBA")
    mask = Image.new("L", (side, side), 0)
    ImageDraw.Draw(mask).ellipse((1, 1, side - 2, side - 2), fill=255)
    image.putalpha(mask)
    buffer = BytesIO()
    image.save(buffer, "PNG")
    buffer.seek(0)
    return ImageReader(buffer)


def make_qr(url):
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="#17171B", back_color="#FFFFFF").convert("RGB")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return ImageReader(buffer)


def draw_header(c, fa, avatar):
    header_h = 158
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - header_h, PAGE_W, header_h, fill=1, stroke=0)
    c.setFillColor(RED)
    c.rect(0, PAGE_H - header_h, 6, header_h, fill=1, stroke=0)

    # A restrained chessboard strip along the bottom of the header.
    sq = 13
    strip_y = PAGE_H - header_h
    for col in range(int(PAGE_W / sq) + 1):
        c.setFillColor(RED if col % 2 == 0 else colors.HexColor("#29272C"))
        c.rect(col * sq, strip_y, sq, 5, fill=1, stroke=0)

    avatar_x, avatar_y, avatar_size = 39, PAGE_H - 139, 108
    c.setFillColor(RED)
    c.circle(avatar_x + avatar_size / 2, avatar_y + avatar_size / 2, avatar_size / 2 + 4, fill=1, stroke=0)
    c.drawImage(avatar, avatar_x, avatar_y, width=avatar_size, height=avatar_size, mask="auto")
    c.setStrokeColor(colors.HexColor("#F3DAD4"))
    c.setLineWidth(1)
    c.circle(avatar_x + avatar_size / 2, avatar_y + avatar_size / 2, avatar_size / 2 + 1, fill=0, stroke=1)

    c.setStrokeColor(colors.HexColor("#5C282E"))
    c.setLineWidth(1)
    c.line(163, PAGE_H - 145, 163, PAGE_H - 25)

    if fa:
        c.setFillColor(colors.HexColor("#D8C5C1"))
        c.setFont(FONT_LATIN_BOLD, 7)
        c.drawString(181, PAGE_H - 33, "SOFTWARE PORTFOLIO / 2026")
        draw_fa(c, "متین", 555, PAGE_H - 65, FONT_FA_BOLD, 27, WHITE)
        draw_fa(c, "توسعه‌دهندهٔ نرم‌افزار", 555, PAGE_H - 87, FONT_FA_BOLD, 10, RED_BRIGHT)
        draw_fa(c, "دانشجوی مهندسی کامپیوتر · دانشگاه آزاد اسلامی", 555, PAGE_H - 105, FONT_FA, 8.2, colors.HexColor("#E6E0DE"))
        c.setFont(FONT_LATIN_BOLD, 7.2)
        c.setFillColor(colors.HexColor("#E8DEDB"))
        c.drawString(181, PAGE_H - 124, "PYTHON  /  DJANGO  /  AI AGENTS  /  ANDROID  /  UNITY")
        draw_link(c, "ostovar04.github.io", 181, PAGE_H - 143, "https://ostovar04.github.io/", FONT_LATIN, 7.0, colors.HexColor("#F5B7B7"))
        draw_link(c, "github.com/ostovar04", 365, PAGE_H - 143, "https://github.com/ostovar04", FONT_LATIN, 7.0, colors.HexColor("#F5B7B7"))
    else:
        c.setFillColor(colors.HexColor("#D8C5C1"))
        c.setFont(FONT_LATIN_BOLD, 7)
        c.drawString(181, PAGE_H - 33, "SOFTWARE PORTFOLIO / 2026")
        c.setFillColor(WHITE)
        c.setFont(FONT_LATIN_BOLD, 27)
        c.drawString(181, PAGE_H - 65, "MATIN")
        c.setFillColor(RED_BRIGHT)
        c.setFont(FONT_LATIN_BOLD, 10)
        c.drawString(181, PAGE_H - 87, "SOFTWARE DEVELOPER")
        c.setFillColor(colors.HexColor("#E6E0DE"))
        c.setFont(FONT_LATIN, 8.2)
        c.drawString(181, PAGE_H - 105, "Computer Engineering Student · Islamic Azad University")
        c.setFillColor(colors.HexColor("#E8DEDB"))
        c.setFont(FONT_LATIN_BOLD, 7.2)
        c.drawString(181, PAGE_H - 124, "PYTHON  /  DJANGO  /  AI AGENTS  /  ANDROID  /  UNITY")
        draw_link(c, "ostovar04.github.io", 181, PAGE_H - 143, "https://ostovar04.github.io/", FONT_LATIN, 7.0, colors.HexColor("#F5B7B7"))
        draw_link(c, "github.com/ostovar04", 365, PAGE_H - 143, "https://github.com/ostovar04", FONT_LATIN, 7.0, colors.HexColor("#F5B7B7"))


def draw_sidebar(c, fa, x, width, qr):
    c.setFillColor(SOFT)
    c.roundRect(x, 53, width, 590, 10, fill=1, stroke=0)
    draw_section(c, x + 13, 623, width - 26, "01", "حوزه‌های کاری" if fa else "Core strengths", fa)

    groups = ([
        ("بک‌اند و رابط‌ها", "PYTHON · DJANGO · REST"),
        ("هوش مصنوعی و اتوماسیون", "AI AGENTS · WORKFLOWS"),
        ("موبایل و تعاملی", "ANDROID · UNITY · C#"),
        ("وب و همکاری", "FRONT-END · TEAMWORK"),
    ] if fa else [
        ("Back-end & APIs", "PYTHON · DJANGO · REST"),
        ("AI & automation", "AI AGENTS · WORKFLOWS"),
        ("Mobile & interactive", "ANDROID · UNITY · C#"),
        ("Web & collaboration", "FRONT-END · TEAMWORK"),
    ])
    y = 593
    for label, stack in groups:
        c.setFillColor(RED)
        c.circle(x + (20 if fa else width - 20), y + 3, 2.2, fill=1, stroke=0)
        if fa:
            draw_fa(c, label, x + width - 13, y, FONT_FA_BOLD, 7.7, TEXT)
        else:
            c.setFillColor(TEXT)
            c.setFont(FONT_LATIN_BOLD, 7.4)
            c.drawString(x + 13, y, label)
        c.setFillColor(MUTED)
        c.setFont(FONT_LATIN, 6.4)
        c.drawString(x + 13, y - 13, stack)
        y -= 42

    draw_section(c, x + 13, 414, width - 26, "02", "راه‌های ارتباطی" if fa else "Contact", fa)
    entries = [
        ("ایمیل" if fa else "EMAIL", "benjaminbigbang24@gmail.com", "mailto:benjaminbigbang24@gmail.com"),
        ("گیت‌هاب" if fa else "GITHUB", "github.com/ostovar04", "https://github.com/ostovar04"),
        ("وب‌سایت" if fa else "PORTFOLIO", "ostovar04.github.io", "https://ostovar04.github.io/"),
        ("تلگرام" if fa else "TELEGRAM", "t.me/Beagk", "https://t.me/Beagk"),
    ]
    y = 387
    for label, value, url in entries:
        if fa:
            draw_fa(c, label, x + width - 13, y, FONT_FA, 6.8, MUTED)
        else:
            c.setFillColor(MUTED)
            c.setFont(FONT_LATIN_BOLD, 6.2)
            c.drawString(x + 13, y, label)
        draw_link(c, value, x + 13, y - 12, url, FONT_LATIN, 6.4, RED)
        y -= 41

    c.setStrokeColor(colors.HexColor("#DAD2CE"))
    c.setLineWidth(0.65)
    c.line(x + 13, 216, x + width - 13, 216)
    c.drawImage(qr, x + 13, 105, width=76, height=76, mask="auto")
    if fa:
        draw_fa(c, "پروژه‌ها و نمونه‌کارها", x + width - 13, 193, FONT_FA_BOLD, 7.4, TEXT)
        c.setFillColor(MUTED)
        c.setFont(FONT_LATIN, 6.0)
        c.drawString(x + 13, 91, "SCAN / GITHUB")
    else:
        c.setFillColor(TEXT)
        c.setFont(FONT_LATIN_BOLD, 7.0)
        c.drawString(x + 13, 197, "PROJECTS & CODE")
        c.setFillColor(MUTED)
        c.setFont(FONT_LATIN, 6.0)
        c.drawString(x + 13, 91, "SCAN / GITHUB")
    c.linkURL("https://github.com/ostovar04", (x + 10, 98, x + 100, 190), relative=0, thickness=0)


def draw_main(c, fa, x, width):
    profile = (
        "دانشجوی مهندسی کامپیوتر و توسعه‌دهندهٔ نرم‌افزار با تمرکز بر توسعهٔ بک‌اند و رابط‌های برنامه‌نویسی، ساخت ایجنت‌های هوش مصنوعی، اپلیکیشن‌های اندروید و نمونه‌سازی تعاملی. علاقه‌مند به تبدیل ایده‌ها به ابزارهای کاربردی و همکاری تیمی در مسیر اجرا و تحویل پروژه."
        if fa else
        "Computer Engineering student focused on software development across Python and Django back ends, AI agents, Android apps, and Unity prototypes. Interested in building practical tools and collaborating on project delivery."
    )
    draw_section(c, x, 623, width, "01", "خلاصهٔ حرفه‌ای" if fa else "Profile", fa)
    draw_paragraph(c, profile, x, 603, width, FONT_FA if fa else FONT_LATIN, 8.15 if fa else 8.4, 12.3, TEXT, fa)

    card_x, card_y, card_w, card_h = x, 385, width, 171
    c.setFillColor(CARD)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.roundRect(card_x, card_y, card_w, card_h, 9, fill=1, stroke=1)
    c.setFillColor(RED)
    c.roundRect(card_x, card_y + card_h - 5, card_w, 5, 2, fill=1, stroke=0)
    draw_section(c, x + 12, 535, width - 24, "02", "پروژهٔ شاخص" if fa else "Featured project", fa)

    c.setFillColor(INK)
    c.setFont(FONT_LATIN_BOLD, 12)
    c.drawString(x + 15, 507, "Mazetoori")
    if fa:
        draw_fa(c, "مزه · منتشرشده", x + width - 16, 507, FONT_FA, 7.4, RED)
        description = "وب‌اپی برای جست‌وجوی غذای فارسی و رستوران‌های نزدیک روی نقشهٔ نشان؛ با محدودهٔ جست‌وجوی ۵ کیلومتر و مرتب‌سازی بر اساس فاصله."
    else:
        c.setFillColor(RED)
        c.setFont(FONT_LATIN_BOLD, 7.2)
        c.drawRightString(x + width - 16, 507, "PUBLISHED · WEB APP")
        description = "A web app for discovering Persian food and nearby restaurants on the Neshan map, within a 5 km radius and sorted by distance."
    draw_paragraph(c, description, x + 15, 490, width - 30, FONT_FA if fa else FONT_LATIN, 7.6 if fa else 7.8, 10.8, MUTED, fa)

    c.setFillColor(TEXT)
    c.setFont(FONT_LATIN_BOLD, 6.3)
    c.drawString(x + 15, 440, "STACK")
    c.setFillColor(MUTED)
    c.setFont(FONT_LATIN, 6.5)
    c.drawString(x + 53, 440, "VITE  ·  JAVASCRIPT  ·  THREE.JS  ·  NESHAN")

    # Project and GitHub links are clickable in the digital PDF and legible on paper.
    draw_link(c, "LIVE DEMO", x + 15, 408, "https://ostovar04.github.io/Mazetoori/", FONT_LATIN_BOLD, 7.0, RED)
    draw_link(c, "MAZETOORI REPOSITORY", x + 92, 408, "https://github.com/ostovar04/Mazetoori", FONT_LATIN_BOLD, 6.8, RED)
    if fa:
        draw_fa(c, "برای دیدن پروژه‌های بیشتر و نمونه‌کدها به گیت‌هاب سر بزنید.", x + width - 15, 393, FONT_FA, 6.6, MUTED)
    else:
        c.setFillColor(MUTED)
        c.setFont(FONT_LATIN, 6.6)
        c.drawRightString(x + width - 15, 393, "Explore more projects and code samples on GitHub.")
    c.linkURL("https://github.com/ostovar04?tab=repositories", (x + 13, 386, x + width - 12, 402), relative=0, thickness=0)

    draw_section(c, x, 357, width, "03", "تحصیلات" if fa else "Education", fa)
    if fa:
        draw_fa(c, "مهندسی کامپیوتر", x + width, 335, FONT_FA_BOLD, 8.4, TEXT)
        draw_fa(c, "دانشگاه آزاد اسلامی · در حال تحصیل", x + width, 319, FONT_FA, 7.6, MUTED)
    else:
        c.setFillColor(TEXT)
        c.setFont(FONT_LATIN_BOLD, 8.4)
        c.drawString(x, 335, "Computer Engineering")
        c.setFillColor(MUTED)
        c.setFont(FONT_LATIN, 7.6)
        c.drawString(x, 319, "Islamic Azad University · In progress")

    draw_section(c, x, 284, width, "04", "همکاری و اجرا" if fa else "Collaboration", fa)
    cooperation = (
        "همکاری تیمی در هماهنگی، بازاریابی و تحویل پروژه؛ با تأکید بر یادگیری پیوسته و ساخت راه‌حل‌های کاربردی."
        if fa else
        "Team collaboration across coordination, marketing, and project delivery, with an emphasis on continuous learning and practical solutions."
    )
    draw_paragraph(c, cooperation, x, 264, width, FONT_FA if fa else FONT_LATIN, 7.9 if fa else 8.1, 12.0, TEXT, fa)


def draw_footer(c, fa):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(38, 40, PAGE_W - 38, 40)
    c.setFillColor(RED)
    c.rect(38, 38, 54, 3, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont(FONT_LATIN, 6.5)
    c.drawString(38, 25, "MATIN  /  @OSTOVAR04")
    c.drawRightString(PAGE_W - 38, 25, "ONE-PAGE CV  ·  2026")


def build_one(lang, avatar, qr):
    fa = lang == "fa"
    path = OUT / ("matin-resume-fa.pdf" if fa else "matin-resume-en.pdf")
    c = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
    c.setTitle("رزومهٔ متین" if fa else "Matin — One-page Resume")
    c.setAuthor("Matin / @ostovar04")
    c.setSubject("رزومهٔ یک‌صفحه‌ای فارسی" if fa else "One-page English resume")

    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, fa, avatar)

    margin = 38
    side_w = 158
    gap = 26
    main_w = PAGE_W - 2 * margin - side_w - gap
    if fa:
        side_x = margin
        main_x = margin + side_w + gap
        divider_x = margin + side_w + gap / 2
    else:
        main_x = margin
        side_x = margin + main_w + gap
        divider_x = margin + main_w + gap / 2
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(divider_x, 63, divider_x, 651)

    draw_sidebar(c, fa, side_x, side_w, qr)
    draw_main(c, fa, main_x, main_w)
    draw_footer(c, fa)
    c.showPage()
    c.save()
    print(f"Created {path}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    register_fonts()
    avatar = make_avatar_png()
    qr = make_qr("https://github.com/ostovar04")
    build_one("fa", avatar, qr)
    build_one("en", avatar, qr)


if __name__ == "__main__":
    main()
