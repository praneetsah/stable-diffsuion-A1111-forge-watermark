
import os
from PIL import Image, ImageDraw, ImageFont
from modules import script_callbacks, shared

MARGIN = 10

def get_font_path(font_name):
    font_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
    font_file = f"{font_name}.ttf"
    return os.path.join(font_dir, font_file)

def apply_text_watermark(image: Image.Image, text: str, opacity: int, use_black: bool, font_name: str, font_size: int):
    draw = ImageDraw.Draw(image)
    try:
        font_path = get_font_path(font_name)
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()

    text_size = draw.textsize(text, font=font)
    position = (image.width - text_size[0] - MARGIN, image.height - text_size[1] - MARGIN)
    color = (0, 0, 0, opacity) if use_black else (255, 255, 255, opacity)
    draw.text(position, text, fill=color, font=font)
    return image

def apply_image_watermark(image: Image.Image, watermark_path: str, max_size: int, opacity: int):
    if not os.path.exists(watermark_path):
        return image

    watermark = Image.open(watermark_path).convert("RGBA")
    scale = min(max_size / watermark.width, max_size / watermark.height)
    size = (int(watermark.width * scale), int(watermark.height * scale))
    watermark = watermark.resize(size, Image.ANTIALIAS)

    alpha = watermark.split()[3].point(lambda p: p * (opacity / 255))
    watermark.putalpha(alpha)

    position = (image.width - watermark.width - MARGIN, image.height - watermark.height - MARGIN)
    image.paste(watermark, position, watermark)
    return image

def on_image_saved(params):
    try:
        if not getattr(shared.opts, "watermark_enabled", False):
            return

        path = params.filename
        if not path.lower().endswith((".png", ".jpg", ".jpeg")):
            return

        opacity = int(getattr(shared.opts, "watermark_opacity", 128))
        max_size = int(getattr(shared.opts, "watermark_max_size", 64))
        use_image = getattr(shared.opts, "watermark_use_image", False)

        img = Image.open(path).convert("RGBA")

        if use_image:
            image_path = getattr(shared.opts, "watermark_image_path", "")
            img = apply_image_watermark(img, image_path, max_size, opacity)
        else:
            text = getattr(shared.opts, "watermark_text", "My Watermark")
            use_black = getattr(shared.opts, "watermark_text_black", False)
            font_name = getattr(shared.opts, "watermark_font", "UltimatePixelFont")
            font_size = int(getattr(shared.opts, "watermark_font_size", 16))
            img = apply_text_watermark(img, text, opacity, use_black, font_name, font_size)

        img.convert("RGB").save(path)

    except Exception as e:
        print(f"[Watermark Extension] Failed to apply watermark: {e}")

def on_ui_settings():
    section = ("watermark", "Watermark")

    shared.opts.add_option("watermark_enabled", shared.OptionInfo(True, "Enable watermark", section=section))
    shared.opts.add_option("watermark_use_image", shared.OptionInfo(False, "Use image watermark (unchecked = use text)", section=section))
    shared.opts.add_option("watermark_text", shared.OptionInfo("My Watermark", "Watermark text", section=section))
    shared.opts.add_option("watermark_image_path", shared.OptionInfo("extensions/sd-webui-watermark/assets/default_watermark.png", "Path to PNG watermark", section=section))
    shared.opts.add_option("watermark_opacity", shared.OptionInfo(128, "Opacity (0-255)", section=section))
    shared.opts.add_option("watermark_max_size", shared.OptionInfo(64, "Max watermark size (px)", section=section))
    shared.opts.add_option("watermark_text_black", shared.OptionInfo(False, "Use black text instead of white", section=section))
    shared.opts.add_option("watermark_font", shared.OptionInfo("UltimatePixelFont", "Font name (must be placed in assets/fonts)", section=section))
    shared.opts.add_option("watermark_font_size", shared.OptionInfo(16, "Font size (px)", section=section))

script_callbacks.on_ui_settings(on_ui_settings)
script_callbacks.on_image_saved(on_image_saved)
