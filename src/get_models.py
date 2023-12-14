import os

import gradio as gr

folder_symbol = "\U0001f4c2"  # 📂
refresh_symbol = "\U0001f504"  # 🔄


def list_model_paths():
    model_paths = []
    for root, dirs, files in os.walk("./logs"):
        for dir in dirs:
            if "runs" in dir:
                log_folders = os.listdir(f"{root}/{dir}")
                for log_folder in log_folders:
                    abs_log_folder = f"{root}/{dir}/{log_folder}"
                    model_paths.append(abs_log_folder)
    return model_paths


class ToolButton(gr.components.Button):
    """Small button with single emoji as text, fits inside gradio forms"""

    def __init__(self, *args, **kwargs):
        classes = kwargs.pop("elem_classes", [])
        super().__init__(*args, elem_classes=["tool", *classes], **kwargs)

    def get_block_name(self):
        return "button"


def create_refresh_button(refresh_component, refresh_method, refreshed_args, elem_id):
    refresh_components = (
        refresh_component if isinstance(refresh_component, list) else [refresh_component]
    )

    def refresh():
        refresh_method()
        args = refreshed_args() if callable(refreshed_args) else refreshed_args

        for k, v in args.items():
            for comp in refresh_components:
                setattr(comp, k, v)

        return (
            [gr.update(**(args or {})) for _ in refresh_components]
            if len(refresh_components) > 1
            else gr.update(**(args or {}))
        )

    refresh_button = ToolButton(value=refresh_symbol, elem_id=elem_id)
    refresh_button.click(fn=refresh, inputs=[], outputs=refresh_components)
    return refresh_button
