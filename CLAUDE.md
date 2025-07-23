# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Stable Diffusion WebUI Extension for the WebUI Forge variant that adds automatic watermarking functionality to generated images. The extension supports both text and image watermarks with customizable positioning, opacity, and styling.

## Development Commands
This extension does not have standalone build, test, or lint commands. It operates as part of the Stable Diffusion WebUI environment:
- To test changes: Install the extension in a WebUI Forge instance and restart the WebUI
- No compilation or build step required (pure Python)
- No test suite available

## Architecture

### Extension Integration
The extension follows standard WebUI extension patterns:
- **Entry point**: `scripts/watermark.py`
- **Callbacks**: Uses `script_callbacks.on_image_saved` and `script_callbacks.on_ui_settings`
- **Settings**: Integrated with WebUI's shared settings system via `shared.opts`

### Core Components

**watermark.py** (scripts/watermark.py)
- `add_watermark()`: Main function that processes saved images
- `on_image_saved()`: Callback handler that intercepts image saves
- `on_ui_settings()`: Registers extension settings in WebUI

### Key Implementation Details

1. **Watermark Processing Flow**:
   - WebUI generates and saves an image
   - `on_image_saved` callback triggers
   - Extension checks if watermarking is enabled
   - Opens the saved image file
   - Applies text or image watermark based on settings
   - Overwrites the original file with watermarked version

2. **Font Handling**:
   - Custom fonts are loaded from `assets/fonts/` directory
   - Falls back to PIL default font if custom font fails
   - Font files must be TTF format

3. **Image Watermark Constraints**:
   - Only PNG format supported for watermark images
   - Auto-resizes based on `watermark_max_size` setting
   - Preserves aspect ratio during resize

4. **Error Handling**:
   - All operations wrapped in try-except blocks
   - Errors are printed but don't crash WebUI
   - Graceful fallbacks for missing fonts/images

## Important Notes

- This extension modifies saved files directly - there's no undo functionality
- Only processes PNG and JPG/JPEG output files
- Watermark positioning is fixed at bottom-right with 10px margin
- The extension requires WebUI Forge (may not work with original Automatic1111 WebUI)
- No external dependencies beyond what WebUI already provides (PIL/Pillow)