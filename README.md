## Yet Another A1111 Resolution Selector
This is a lean and mean [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) / [Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge) extension that adds convenient resolution selection buttons next to width and height sliders. It's simple and minimalistic: define desired resolutions in the settings = get buttons on the resolution panel, next to the "switch width and height" button, right where they belong; click button = instantly set predefined resolution. No huff, no puff, no taking up space on the extensions section, no "calculators", no bloat.

![YAARS Demo](https://github.com/user-attachments/assets/4ae0a325-1a41-44a4-aa8b-871a86b286bb)

## Installation
1. Open the "Extensions" tab
2. Open "Install from URL" tab
3. Paste this repository link into the "URL" field:
```
https://github.com/Siberpone/yaars
```
4. Click "Install" and wait for it to finish installation
5. Restart the server

## Configuration
YAARS can be configured through A1111's settings tab under the "Resolution Selector" section. From there you can enable/disable YAARS for t2i and i2i tabs with respective checkboxes and configure desired resolutions in the "Resolutions" textbox. Resolutions are defined as `"<width>x<height>": "<label>"`. \<label> can be left as an empty string, in which case aspect ratio of the resolution will be used. Must be a valid JSON.
