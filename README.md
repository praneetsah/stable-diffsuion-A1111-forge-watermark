# 🔖 SD WebUI Watermark Extension

This extension automatically adds a customizable **text or image watermark** to the bottom-right of saved generations in **Stable Diffusion WebUI Forge**.

---

## ✨ Features

* ✅ Enable/disable watermark globally or via Quicksettings checkbox
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
* 🧠 Stable and lightweight, triggered only at image save

---

## 📆 Installation

1. **Download & extract** this extension into your `extensions/` folder:

   ```
   stable-diffusion-webui-forge/extensions/sd-webui-watermark/
   ```

2. Restart WebUI Forge.

---

## ⚙️ Configuration

### 🔧 Settings Tab (Under “Watermark”)

* **Enable watermark** (toggle)
* **Watermark type**: `text` or `image`
* **Text string**
* **Text color**: toggle black or white
* **Font name**: must match a `.ttf` file in `assets/fonts/`
* **Font size**: in pixels
* **Image watermark path**: relative to your WebUI folder
* **Opacity**: from 0 (invisible) to 255 (fully visible)
* **Max image watermark size**: in pixels

### ⚡ Quicksettings Toggle (Optional)

To toggle watermarking from the **top bar**, add this to your `config.json`:

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

* Only PNG and JPG images will be watermarked.
* Watermark will only appear if **enabled** in settings **and/or** checked in the Quicksettings bar.
* Settings changes apply immediately after clicking **Apply Settings**.

---

## 🧼 Uninstall

Just delete the folder:

```
extensions/sd-webui-watermark/
```

And restart WebUI Forge.

---

## 🛠️ Troubleshooting

* If text watermark doesn’t appear:

  * Ensure `watermark_enabled` is checked
  * Check that `watermark_type` is set to `text`
  * Make sure the font file exists and is valid
* If image watermark doesn’t show:

  * Ensure path is correct (relative to WebUI folder)
  * Image should be a transparent `.png`

---

## 📁 Folder Structure

```
sd-webui-watermark/
├── scripts/
│   └── watermark.py
├── assets/
│   ├── default_watermark.png
│   └── fonts/
│       └── DejaVuSans.ttf
└── README.md
```

---

Font Credits
Font Name: Ultimate Pixel Font
Author(s):

Linus Suter – https://codewelt.com

Lionel Pailloncy (credited in project metadata)

License: GNU General Public License (GPL)
This font is licensed under the GNU GPL, which allows for free use, modification, and distribution, provided the license terms are respected. For projects embedding this font in software, ensure compliance with GPL font linking exceptions if applicable.

Source: https://codewelt.com

Made for [Stable Diffusion WebUI Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge)

