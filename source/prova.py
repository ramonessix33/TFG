from Inpainting import Inpainting
from diffusers.utils import load_image
from PIL import Image

# Create an instance of the Inpainting class
inpainting = Inpainting()

# Set the parameters for inpainting

image = load_image(r'C:\Users\USER\Desktop\inpainting\prova1.jpg').convert("RGB").resize((1024, 1024))
mask_image = load_image(r'C:\Users\USER\Desktop\TFG-main\a.png').resize((1024, 1024))
print(mask_image)
parameters = {
    "prompt": "Your inpainting prompt",
    "negative_prompt": "Your negative prompt",
    "image": image,  # Replace with your input image
    "mask_image": mask_image,  # Replace with your mask image
    "guidance_scale": 7.5,
    "inference_steps": 20,
    "strength": 0.99,
    "manual_seed": -1,
    "num_images": 1
}

# Run the inpainting process on the GPU
generated_images = inpainting.paint(parameters)

output_path = "prova.jpg"
generated_image = generated_images[0]  # Assuming you generated a single image
generated_image.save(output_path)
