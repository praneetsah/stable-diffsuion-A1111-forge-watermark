
import os
from PIL import Image, ImageDraw, ImageFont
from modules import script_callbacks, shared, scripts
from modules.api import api
from fastapi import Body
import gradio as gr

MARGIN = 10

class WatermarkScript(scripts.Script):
    def __init__(self):
        super().__init__()
        self.request_watermark_settings = {}
    
    def title(self):
        return "Watermark"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("Watermark", open=False):
                enabled = gr.Checkbox(
                    label="Enable watermark for this generation", 
                    value=lambda: getattr(shared.opts, "watermark_enabled", False),
                    elem_id="watermark_enabled_checkbox"
                )
                
                def update_watermark_setting(value):
                    shared.opts.watermark_enabled = value
                    shared.opts.save(shared.config_filename)
                    return value
                
                enabled.change(
                    fn=update_watermark_setting,
                    inputs=[enabled],
                    outputs=[enabled]
                )
                
        return [enabled]

    def process(self, p, enabled):
        # Store per-request watermark settings
        request_id = id(p)  # Use processing object ID as unique identifier
        
        # Debug logging for API parameter handling
        print(f"[Watermark Debug] Received enabled parameter: {enabled}, type: {type(enabled)}, repr: {repr(enabled)}")
        print(f"[Watermark Debug] Global watermark_enabled: {getattr(shared.opts, 'watermark_enabled', False)}")
        
        # Proper boolean handling for API calls (handles both boolean and string inputs)
        if enabled is not None:
            if isinstance(enabled, str):
                # Handle string representations from API
                watermark_enabled = enabled.lower() in ('true', '1', 'yes', 'on')
                print(f"[Watermark Debug] String conversion: '{enabled}' -> {watermark_enabled}")
            elif isinstance(enabled, bool):
                # Handle proper boolean values
                watermark_enabled = enabled
                print(f"[Watermark Debug] Boolean value: {watermark_enabled}")
            else:
                # Handle other types (int, etc.) - use standard bool conversion
                watermark_enabled = bool(enabled)
                print(f"[Watermark Debug] Other type conversion: {enabled} -> {watermark_enabled}")
        else:
            watermark_enabled = getattr(shared.opts, "watermark_enabled", False)
            print(f"[Watermark Debug] Using global setting: {watermark_enabled}")
        
        print(f"[Watermark Debug] Final enabled state: {watermark_enabled}")
        
        # Get current global settings as base
        self.request_watermark_settings[request_id] = {
            'enabled': watermark_enabled,
            'use_image': getattr(shared.opts, "watermark_use_image", False),
            'text': getattr(shared.opts, "watermark_text", "My Watermark"),
            'image_path': getattr(shared.opts, "watermark_image_path", ""),
            'opacity': getattr(shared.opts, "watermark_opacity", 128),
            'max_size': getattr(shared.opts, "watermark_max_size", 64),
            'text_black': getattr(shared.opts, "watermark_text_black", False),
            'font': getattr(shared.opts, "watermark_font", "UltimatePixelFont"),
            'font_size': getattr(shared.opts, "watermark_font_size", 16)
        }
        
        # Add to generation params for tracking
        if self.request_watermark_settings[request_id]['enabled']:
            p.extra_generation_params["Watermark"] = "enabled"

    def postprocess_image(self, p, pp, enabled):
        request_id = id(p)
        settings = self.request_watermark_settings.get(request_id, {})
        
        print(f"[Watermark Debug] postprocess_image - enabled param: {enabled}, settings enabled: {settings.get('enabled', False)}")
        
        if not settings.get('enabled', False):
            print(f"[Watermark Debug] Watermark disabled, skipping")
            return
        
        print(f"[Watermark Debug] Applying watermark")
        
        try:
            img = pp.image.convert("RGBA")
            
            if settings.get('use_image', False):
                img = apply_image_watermark(
                    img, 
                    settings.get('image_path', ''), 
                    settings.get('max_size', 64), 
                    settings.get('opacity', 128)
                )
            else:
                img = apply_text_watermark(
                    img,
                    settings.get('text', 'My Watermark'),
                    settings.get('opacity', 128),
                    settings.get('text_black', False),
                    settings.get('font', 'UltimatePixelFont'),
                    settings.get('font_size', 16)
                )
            
            pp.image = img.convert("RGB")
            
        except Exception as e:
            print(f"[Watermark Extension] Failed to apply watermark: {e}")
    
    def postprocess(self, p, processed, enabled):
        # Clean up stored settings after processing is complete
        request_id = id(p)
        if request_id in self.request_watermark_settings:
            del self.request_watermark_settings[request_id]

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

def watermark_get_status():
    return {"enabled": getattr(shared.opts, "watermark_enabled", False)}

def watermark_set_status(enabled: bool = Body(..., description="Enable or disable watermark")):
    shared.opts.watermark_enabled = enabled
    shared.opts.save(shared.config_filename)
    return {"enabled": enabled}

def watermark_get_settings():
    return {
        "enabled": getattr(shared.opts, "watermark_enabled", False),
        "use_image": getattr(shared.opts, "watermark_use_image", False),
        "text": getattr(shared.opts, "watermark_text", "My Watermark"),
        "image_path": getattr(shared.opts, "watermark_image_path", ""),
        "opacity": getattr(shared.opts, "watermark_opacity", 128),
        "max_size": getattr(shared.opts, "watermark_max_size", 64),
        "text_black": getattr(shared.opts, "watermark_text_black", False),
        "font": getattr(shared.opts, "watermark_font", "UltimatePixelFont"),
        "font_size": getattr(shared.opts, "watermark_font_size", 16)
    }

def watermark_update_settings(
    enabled: bool = Body(None, description="Enable or disable watermark"),
    use_image: bool = Body(None, description="Use image watermark instead of text"),
    text: str = Body(None, description="Watermark text"),
    image_path: str = Body(None, description="Path to watermark image"),
    opacity: int = Body(None, description="Opacity (0-255)"),
    max_size: int = Body(None, description="Max watermark size in pixels"),
    text_black: bool = Body(None, description="Use black text instead of white"),
    font: str = Body(None, description="Font name"),
    font_size: int = Body(None, description="Font size in pixels")
):
    if enabled is not None:
        shared.opts.watermark_enabled = enabled
    if use_image is not None:
        shared.opts.watermark_use_image = use_image
    if text is not None:
        shared.opts.watermark_text = text
    if image_path is not None:
        shared.opts.watermark_image_path = image_path
    if opacity is not None:
        shared.opts.watermark_opacity = opacity
    if max_size is not None:
        shared.opts.watermark_max_size = max_size
    if text_black is not None:
        shared.opts.watermark_text_black = text_black
    if font is not None:
        shared.opts.watermark_font = font
    if font_size is not None:
        shared.opts.watermark_font_size = font_size
    
    shared.opts.save(shared.config_filename)
    return watermark_get_settings()

def watermark_api_process(enabled: bool = True):
    """API function for processing watermark via alwayson_scripts"""
    return {"enabled": enabled}

def on_app_started(_, app):
    app.add_api_route("/api/watermark/status", watermark_get_status, methods=["GET"])
    app.add_api_route("/api/watermark/status", watermark_set_status, methods=["POST"])
    app.add_api_route("/api/watermark/settings", watermark_get_settings, methods=["GET"])
    app.add_api_route("/api/watermark/settings", watermark_update_settings, methods=["POST"])

script_callbacks.on_ui_settings(on_ui_settings)
script_callbacks.on_app_started(on_app_started)
