from PIL import Image
import inspect
from typing import List, Optional, Union

import numpy as np
import torch

import PIL
#PIL.ImageFile.LOAD_TRUNCATED_IMAGES = False
#import gradio as gr
from diffusers import AutoPipelineForInpainting

class Inpainting:
    def __init__(self, parent=None):
        self.parent = parent
        self.initialized = 0

    def initialize(self):
        device = "cuda"
        model_path = "diffusers/stable-diffusion-xl-1.0-inpainting-0.1"

        self.pipe = AutoPipelineForInpainting.from_pretrained("diffusers/stable-diffusion-xl-1.0-inpainting-0.1", torch_dtype=torch.float16, variant="fp16").to("cuda")
        print("inicialitzat pipeline")

    def paint(self, parameters):
        if self.initialized == 0:
            self.initialize()
            self.initialized = 1

        if parameters["manual_seed"] == -1:
            generator = torch.Generator(device="cuda")
        else:
            generator = torch.Generator(device="cuda").manual_seed(parameters["manual_seed"]) # change the seed to get different results

        images = self.pipe(
        #height=alcada,
        #width=amplada,
        prompt=parameters["prompt"],
        negative_prompt=parameters["negative_prompt"],
        image=parameters["image"],
        mask_image=parameters["mask_image"],
        guidance_scale=parameters["guidance_scale"],
        num_inference_steps=parameters["inference_steps"],  # steps between 15 and 30 work well for us
        strength=parameters["strength"],  # make sure to use `strength` below 1.0
        generator=generator,
        num_images_per_prompt=parameters["num_images"],
        ).images

        print('Images generated')

        return images

    def stub_paint(self,parameters):
        generated_images = []
        path_imatge = r'C:\Users\USER\Desktop\inpainting\prova1.jpg'
        imatge = Image.open(path_imatge)
        generated_images = [imatge.copy() for _ in range(parameters["num_images"])]
        return generated_images
