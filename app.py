import gradio as gr
import subprocess
import shutil
import os

def run_scripts(target, source, use_face_enhancer):
    if target is None or (not use_face_enhancer and source is None):
        return None
    target_extension = os.path.splitext(target.name)[-1]
    output_path1 = "output1" + target_extension
    output_path2 = "output2" + target_extension

    if not use_face_enhancer:
        # Run both scripts
        cmd1 = ["python3", "run.py", "-s", source.name, "-t", target.name, "-o", output_path1, "--frame-processor", "face_swapper"]
        subprocess.run(cmd1)

    # Run the second script
    cmd2 = ["python3", "run.py", "-t", target.name if use_face_enhancer else output_path1, "-o", output_path2, "--frame-processor", "face_enhancer"]
    subprocess.run(cmd2)

    if not use_face_enhancer:
        os.remove(source.name)
    os.remove(target.name)

    return output_path2

iface = gr.Interface(
    fn=run_scripts,
    inputs=[
        "file",
        "file",
        gr.inputs.Checkbox(default=False, label="Use only Face Enhancer")  # New checkbox input
    ],
    outputs="file",
    title="Face swapper",
    description="Upload a target image/video and a source image to swap faces.",
    live=True
)

iface.launch(server_name="0.0.0.0", server_port=8000)
