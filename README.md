# 🔖 SD WebUI Watermark Extension (Enhanced Fork)

An enhanced Stable Diffusion WebUI Forge extension that adds **per-generation watermark control** with comprehensive **API support** and an intuitive **UI toggle** directly in the generation interface.

This fork improves upon the original by providing **case-by-case watermark processing** instead of global-only control, making it perfect for automated workflows and selective watermarking.

---

## ✨ Key Enhancements in This Fork

* 🎯 **Per-generation watermark control** - Toggle watermarks for individual generations
* 🚀 **Full API support** - Complete REST API for programmatic control
* 🎛️ **Inline UI toggle** - Watermark checkbox directly in txt2img/img2img interface
* 🔄 **Request-based processing** - Each generation can have different watermark settings
* 🌐 **Perfect for automation** - Ideal for batch processing and API workflows

---

## ✨ Features

* ✅ **Per-generation control**: Enable/disable watermarks on a case-by-case basis
* 🎛️ **Inline UI toggle**: Watermark checkbox visible directly in txt2img/img2img tabs
* 🚀 **Comprehensive API**: Full REST API for programmatic watermark control
* 🔋️ **Text watermark** mode:
  * Custom watermark string
  * Set font name (must match `.ttf` in `assets/fonts/`)
  * Adjustable font size
  * Choose text color: white or black
* 🖼️ **Image watermark** mode:
  * Upload your own transparent PNG
  * Resize with a max dimension limit
  * Adjustable opacity
* 📊 Watermark placement: bottom-right with customizable margins
* 📂 Watermark is burned into the final saved image
* ⚡ Fully compatible with **WebUI Forge**
* 🧠 Stable and lightweight, with intelligent per-request processing

---

## 📆 Installation

1. **Clone or download** this enhanced fork into your `extensions/` folder:

   ```bash
   cd stable-diffusion-webui-forge/extensions/
   git clone https://github.com/your-username/sd-webui-watermark.git
   ```

2. Restart WebUI Forge.

3. The watermark toggle will automatically appear in your txt2img and img2img tabs!

---

## 🎛️ Per-Generation Control (New!)

### UI Toggle
A **"Enable watermark for this generation"** checkbox now appears directly in the generation interface:
- Located in the **Watermark** accordion section
- Toggle ON/OFF for individual generations
- Overrides global settings when used
- Perfect for selective watermarking during interactive use

### How It Works
Unlike the original extension that applied watermarks globally to all saved images, this fork processes watermarks **per-request**:
- Each generation can have its own watermark setting
- Multiple concurrent API requests can have different watermark states
- UI and API controls work independently
- No interference between different generation sessions

---

## 🚀 API Usage (New!)

This fork provides comprehensive API support for programmatic watermark control.

### Method 1: Per-Request Control (Recommended)

Control watermarks for individual generation requests using the `alwayson_scripts` parameter:

```bash
curl -X POST http://localhost:7860/sdapi/v1/txt2img \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful landscape",
    "steps": 20,
    "width": 512,
    "height": 512,
    "alwayson_scripts": {
      "Watermark": {
        "args": [true]
      }
    }
  }'
```

**Arguments:**
- `args[0]` (boolean): Enable/disable watermark for this specific generation

**Benefits:**
- Watermarks are applied per-request, not globally
- Multiple concurrent requests can have different watermark settings
- No need to change global settings between requests
- Perfect for automated workflows with mixed watermark requirements

### Method 2: Global Settings API

Configure watermark settings globally (used as defaults when per-request control is not specified):

**GET** `/api/watermark/status` - Get current watermark status
```json
Response: {"enabled": true}
```

**POST** `/api/watermark/status` - Enable/disable watermark globally
```json
Request body: {"enabled": false}
Response: {"enabled": false}
```

**GET** `/api/watermark/settings` - Get all watermark settings
```json
Response: {
  "enabled": true,
  "use_image": false,
  "text": "My Watermark",
  "image_path": "extensions/sd-webui-watermark/assets/default_watermark.png",
  "opacity": 128,
  "max_size": 64,
  "text_black": false,
  "font": "UltimatePixelFont",
  "font_size": 16
}
```

**POST** `/api/watermark/settings` - Update watermark settings (all fields optional)
```json
Request body: {
  "enabled": true,
  "text": "© 2024",
  "opacity": 200,
  "font_size": 24
}
Response: (returns all current settings)
```

### Complete Automation Example

```python
import requests
import json

# Generate image with watermark enabled for this request only
payload = {
    "prompt": "a serene mountain landscape at sunset",
    "negative_prompt": "blurry, low quality",
    "steps": 30,
    "sampler_name": "DPM++ 2M Karras",
    "cfg_scale": 7,
    "width": 768,
    "height": 512,
    "alwayson_scripts": {
        "Watermark": {
            "args": [True]  # Enable watermark for this generation
        }
    }
}

response = requests.post(
    "http://localhost:7860/sdapi/v1/txt2img",
    json=payload
)

# Generate another image without watermark - no global setting changes needed!
payload_no_watermark = {
    "prompt": "abstract digital art",
    "steps": 20,
    "alwayson_scripts": {
        "Watermark": {
            "args": [False]  # Disable watermark for this generation
        }
    }
}

response2 = requests.post(
    "http://localhost:7860/sdapi/v1/txt2img",
    json=payload_no_watermark
)
```

---

## ⚙️ Configuration

### 🔧 Settings Tab (Under "Watermark")

Configure global defaults and watermark appearance:

* **Enable watermark** (global toggle)
* **Watermark type**: `text` or `image`
* **Text string**
* **Text color**: toggle black or white
* **Font name**: must match a `.ttf` file in `assets/fonts/`
* **Font size**: in pixels
* **Image watermark path**: relative to your WebUI folder
* **Opacity**: from 0 (invisible) to 255 (fully visible)
* **Max image watermark size**: in pixels

### ⚡ Quicksettings Toggle (Optional)

To add a global toggle to the **top bar**, add this to your `config.json`:

```json
{
  "quicksettings": ["sd_model_checkpoint", "watermark_enabled"]
}
```

---

## 🌤️ Custom Fonts

To use your own fonts:

1. Place `.ttf` files into:
   ```
   extensions/sd-webui-watermark/assets/fonts/
   ```

2. In the settings, enter the font **filename without `.ttf`** in the "Font name" field.

For example:

| File in folder              | Set `watermark_font` to |
| --------------------------- | ----------------------- |
| `DejaVuSans.ttf`            | `DejaVuSans`            |
| `MyCustomSignatureFont.ttf` | `MyCustomSignatureFont` |

---

## 🧪 Usage Notes

* Only PNG and JPG images will be watermarked
* **Per-generation control** takes precedence over global settings
* UI checkbox controls individual generations regardless of global settings
* API `alwayson_scripts` parameter overrides both UI and global settings
* Settings changes apply immediately after clicking **Apply Settings**
* Multiple concurrent generations can have different watermark states

---

## 🆚 Original vs Fork Comparison

| Feature | Original Extension | This Enhanced Fork |
|---------|-------------------|-------------------|
| Watermark Control | Global only | Per-generation + Global |
| UI Integration | Settings page only | Inline toggle in generation tabs |
| API Support | None | Full REST API |
| Processing Method | All saved images | Request-based processing |
| Concurrent Usage | Single global state | Multiple independent states |
| Automation Support | Limited | Comprehensive |

---

## 🛠️ Troubleshooting

* If text watermark doesn't appear:
  * Ensure the per-generation checkbox is enabled OR global setting is on
  * Check that `watermark_type` is set to `text`
  * Make sure the font file exists and is valid
* If image watermark doesn't show:
  * Ensure path is correct (relative to WebUI folder)
  * Image should be a transparent `.png`
* For API issues:
  * Check that the `alwayson_scripts` format is correct
  * Verify boolean values are properly formatted (true/false, not strings)
  * Enable debug logging to see parameter processing

---

## 📁 Folder Structure

```
sd-webui-watermark/
├── scripts/
│   └── watermark.py          # Enhanced with API and per-request processing
├── assets/
│   ├── default_watermark.png
│   └── fonts/
│       └── UltimatePixelFont.ttf
├── README.md
└── CLAUDE.md                 # Development instructions
```

---

## 🔧 Development

This extension includes comprehensive debug logging for troubleshooting:
- Parameter processing logs
- Per-request state tracking
- API call debugging

See `CLAUDE.md` for development guidelines and architecture details.

---

## 📜 Font Credits

**Font Name**: Ultimate Pixel Font  
**Author**: Linus Suter – https://codewelt.com  
**License**: GNU General Public License (GPL)

This font is licensed under the GNU GPL, which allows for free use, modification, and distribution, provided the license terms are respected.

---

## 🤝 Contributing

This is an open-source fork with enhancements for better automation and per-request control. Contributions welcome!

**Original Extension**: Made for [Stable Diffusion WebUI Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge)  
**Enhanced Fork**: Improved with API support and per-generation control

---

## 📄 License

GNU General Public License (GPL) - Same as original extension