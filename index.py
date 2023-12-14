import os

import gradio as gr
import pandas as pd

folder_symbol = "\U0001f4c2"  # 📂
refresh_symbol = "\U0001f504"  # 🔄


# 虛擬的 finetune 和 inference 函數
def finetune(model_path, data_path):
    # 模擬 finetune 的過程
    return f"Finetuning model {model_path} with data {data_path}"


def inference(model_path):
    # 模擬推論的過程
    return f"Inference using model {model_path}"


def provide_download_file():
    file_path = "./tests.zip"  # 更改為您的 ZIP 文件路徑
    return file_path


# 生成用於顯示的 DataFrame
def generate_dataframes():
    # 使用虛擬數據創建四個 DataFrame
    df1 = pd.DataFrame({"A": range(5), "B": range(5, 10)})
    df2 = pd.DataFrame({"C": range(10, 15), "D": range(15, 20)})
    df3 = pd.DataFrame({"E": range(20, 25), "F": range(25, 30)})
    df4 = pd.DataFrame({"G": range(30, 35), "H": range(35, 40)})
    return df1, df2, df3, df4


# 列出 ./log 下的所有子資料夾
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


class FormComponent:
    def get_expected_parent(self):
        return gr.components.Form


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

    refresh_button = ToolButton(value="\U0001f504", elem_id=elem_id)
    refresh_button.click(fn=refresh, inputs=[], outputs=refresh_components)
    return refresh_button


# Gradio 介面
def gradio_interface():
    with gr.Blocks() as service_interface:
        gr.Markdown("# DV-Log Service")
        with gr.Tab("Inference / Prediction"):
            with gr.Row():
                with gr.Column():
                    model_selector = gr.Dropdown(
                        label="Select a model", choices=list_model_paths()
                    )
                    refresh_button = create_refresh_button(
                        model_selector,
                        list_model_paths,
                        lambda: {"choices": list_model_paths()},
                        "model_selector_refresh",
                    )
                    data_path_input = gr.Textbox(label="Enter Data Path")
                    inference_button = gr.Button("Inference")
                    download_button = gr.Button("Download ZIP")
                    download_link = gr.File(label="Download Link")

                with gr.Column():
                    gr.Markdown("Output DataFrames")
                    df_output1 = gr.Dataframe()
                    df_output2 = gr.Dataframe()
                    df_output3 = gr.Dataframe()
                    df_output4 = gr.Dataframe()
                    download_button.click(
                        fn=provide_download_file, inputs=[], outputs=[download_link]
                    )

            inference_button.click(
                fn=lambda x: generate_dataframes(),
                inputs=[model_selector],
                outputs=[df_output1, df_output2, df_output3, df_output4],
            )
        with gr.Tab("Finetune Models"):
            with gr.Row():
                with gr.Column():
                    model_selector = gr.Dropdown(
                        label="Select a model", choices=list_model_paths()
                    )
                    refresh_button = create_refresh_button(
                        model_selector,
                        list_model_paths,
                        lambda: {"choices": list_model_paths()},
                        "model_selector_refresh",
                    )
                    data_path_input = gr.Textbox(label="Enter Finetune Dataset Path")
                    finetune_button = gr.Button("Finetune")

                with gr.Column():
                    gr.Markdown("Output DataFrames")
                    df_output1 = gr.Dataframe()
                    df_output2 = gr.Dataframe()
                    df_output3 = gr.Dataframe()
                    df_output4 = gr.Dataframe()

            finetune_button.click(
                fn=lambda x, y: generate_dataframes(),
                inputs=[model_selector, data_path_input],
                outputs=[df_output1, df_output2, df_output3, df_output4],
            )
    return service_interface


demo = gradio_interface()
if __name__ == "__main__":
    demo.launch(share=False)
