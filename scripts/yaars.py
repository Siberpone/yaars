from modules import scripts, script_callbacks, shared
from modules.ui_components import ToolButton
from fractions import Fraction
import gradio as gr
import json

DEFAULT_RESOLUTIONS = \
"""{
    "512x512": "SD1",
    "768x768": "SD2",
    "786x512": "SD3",
    "1024x1024": "XL1",
    "1216x832": "XL2",
    "1344x768": "XL3",
    "1280x720": "HD",
    "1920x1080": "FHD"
}"""


def on_ui_settings():
    YAARS_SECTION = ("yaars", "Resolution Selector")
    shared.opts.add_option(
        "yaars_enable_t2i",
        shared.OptionInfo(
            True,
            "Enable for txt2img",
            section=YAARS_SECTION
        ).needs_reload_ui()
    )
    shared.opts.add_option(
        "yaars_enable_i2i",
        shared.OptionInfo(
            True,
            "Enable for img2img",
            section=YAARS_SECTION
        ).needs_reload_ui()
    )
    try:
        shared.opts.add_option(
            "yaars_resolutions",
            shared.OptionInfo(
                DEFAULT_RESOLUTIONS,
                "Resolutions",
                gr.Code,
                lambda: {
                    "language": "json",
                    "interactive": True
                },
                section=YAARS_SECTION
            )
        )
    except AttributeError:
        shared.opts.add_option(
            "yaars_resolutions",
            shared.OptionInfo(
                DEFAULT_RESOLUTIONS,
                "Resolutions",
                gr.Textbox,
                section=YAARS_SECTION
            )
        )


script_callbacks.on_ui_settings(on_ui_settings)


class Scripts(scripts.Script):
    a1111_controls = {}
    MAX_BUTTONS_IN_COLUMN = 3

    def __init__(self):
        try:
            resolutions_json = json.loads(
                getattr(shared.opts, "yaars_resolutions", DEFAULT_RESOLUTIONS)
            )
        except json.JSONDecodeError:
            print("[yaars] Failed to decode resolution definitions JSON. Check that resolutions are defined correctly in the settings.")
            resolutions_json = DEFAULT_RESOLUTIONS
        self.resolutions = [(k, v) for k, v in resolutions_json.items()]
        self.enable_t2i = getattr(shared.opts, "yaars_enable_t2i", True)
        self.enable_i2i = getattr(shared.opts, "yaars_enable_i2i", True)

    def title(self):
        return "Yet Another A1111 Aspect Ratio Selector"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def inject_yaars_section(self, tab_name, component, *args, **kwargs):
        if kwargs.get("elem_id") == f"{tab_name}_width":
            self.a1111_controls[f"{tab_name}_width"] = component
        if kwargs.get("elem_id") == f"{tab_name}_height":
            self.a1111_controls[f"{tab_name}_height"] = component
        if kwargs.get("elem_id") == f"{tab_name}_dimensions_row":
            def chunks(lst, n):
                """Yield successive n-sized chunks from lst."""
                for i in range(0, len(lst), n):
                    yield lst[i:i + n]

            columns = chunks(self.resolutions, self.MAX_BUTTONS_IN_COLUMN)
            for column in columns:
                with gr.Column(elem_classes=["dimensions-tools"], variant="compact"):
                    for res, label in column:
                        w, h = (int(x) for x in res.split("x"))
                        reduced = Fraction(w, h).as_integer_ratio()
                        btn_label = label or f"{reduced[0]}:{reduced[1]}"
                        res_button = ToolButton(btn_label)

                        # avoid closure trap
                        def click_func(w=w, h=h):
                            return (gr.update(value=w), gr.update(value=h))

                        res_button.click(
                            click_func,
                            None,
                            [
                                self.a1111_controls[f"{tab_name}_width"],
                                self.a1111_controls[f"{tab_name}_height"]
                            ],
                            show_progress="hidden"
                        )

    def after_component(self, component, *args, **kwargs):
        if self.enable_t2i:
            self.inject_yaars_section("txt2img", component, *args, **kwargs)
        if self.enable_i2i:
            self.inject_yaars_section("img2img", component, *args, **kwargs)
