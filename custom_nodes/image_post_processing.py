import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np

class Mirror:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image1": ("IMAGE",),
                "blend_mode": (["horizontal", "vertical"],),
                "ratio": ("FLOAT", {"default": 0.5, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "mirror_images"

    CATEGORY = "image/postprocessing"

    def mirror_images(self, image1: torch.Tensor, blend_mode: str, ratio: float):

        mirrored_image = image1.clone()
        batch_size, height, width, channels = mirrored_image.shape
        if blend_mode == "horizontal":
            crop_width = int(width * ratio) if ratio <= 0.5 else int(width * (1 - ratio))
            cropped_tensor  = mirrored_image[:, :, -(width-crop_width):, :] if ratio <= 0.5 else mirrored_image[:, :, :width-crop_width, :]
            mirrored_part = cropped_tensor[:, :, :crop_width, :] if ratio <= 0.5 else cropped_tensor[:, :, -crop_width:, :]
            flipped_tensor = torch.flip(mirrored_part, dims=[2])
            merged_tensor = torch.cat([flipped_tensor, cropped_tensor], dim=2) if ratio <= 0.5 else torch.cat([cropped_tensor, flipped_tensor], dim=2)
            return (merged_tensor,)
        elif blend_mode == "vertical":
            crop_height = int(height * ratio) if ratio <= 0.5 else int(height * (1 - ratio))
            cropped_tensor  = mirrored_image[:, -(height-crop_height):, :, :] if ratio <= 0.5 else mirrored_image[:, :height-crop_height, :, :]
            mirrored_part = cropped_tensor[:, :crop_height, :, :] if ratio <= 0.5 else cropped_tensor[:, -crop_height:, :, :]
            flipped_tensor = torch.flip(mirrored_part, dims=[1])
            merged_tensor = torch.cat([flipped_tensor, cropped_tensor], dim=1) if ratio <= 0.5 else torch.cat([cropped_tensor, flipped_tensor], dim=1)
            return (merged_tensor,)
        else:
            raise ValueError(f"Unsupported blend mode: {blend_mode}")
        return (mirrored_image,)


NODE_CLASS_MAPPINGS = {
    "Symmetry Mirror": Mirror,
}