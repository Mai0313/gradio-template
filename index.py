import os

import gradio as gr
import pandas as pd

from src.download_result import provide_download_file
from src.finetune import finetune
from src.get_models import create_refresh_button, list_model_paths
from src.inference import inference

folder_symbol = "\U0001f4c2"  # 📂
refresh_symbol = "\U0001f504"  # 🔄


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

                with gr.Column():
                    gr.Markdown("Output Files")
                    download_button = gr.Button("Download ZIP")
                    download_link = gr.File(label="Download Link")
                    df_output1 = gr.Dataframe()
                    df_output2 = gr.Dataframe()
                    df_output3 = gr.Dataframe()
                    df_output4 = gr.Dataframe()

            download_button.click(fn=provide_download_file, inputs=[], outputs=[download_link])

            inference_button.click(
                fn=inference,
                inputs=[model_selector, data_path_input],
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
                fn=finetune,
                inputs=[model_selector, data_path_input],
                outputs=[df_output1, df_output2, df_output3, df_output4],
            )
    return service_interface


demo = gradio_interface()
if __name__ == "__main__":
    demo.launch(share=False)
