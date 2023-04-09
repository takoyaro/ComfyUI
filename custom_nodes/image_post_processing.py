import comfy.utils
import torch

class Mirror:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image1": ("IMAGE",),
                "blend_mode": (["horizontal", "vertical"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "mirror_images"

    CATEGORY = "image/postprocessing"

    def mirror_images(self, image1: torch.Tensor, blend_mode: str):

        print(f'Image shape: {image1.shape}') # torch.Size([1, 720, 1280, 3])
        print(f'Image resolution: {image1.shape[2]} x {image1.shape[1]}') # torch.Size([720, 1280])

        mirrored_image = image1.clone()
        batch_size, height, width, channels = mirrored_image.shape
        if blend_mode == "horizontal":
            # Crop the image tensor at half its width
            crop_width = width // 2
            cropped_tensor = mirrored_image[:, :, :crop_width, :]

            # Flip the cropped tensor horizontally
            flipped_tensor = torch.flip(cropped_tensor, dims=[2])

            # Concatenate the cropped and flipped tensors back together
            merged_tensor = torch.cat([cropped_tensor, flipped_tensor], dim=2)
            return (merged_tensor,)
        elif blend_mode == "vertical":
            # Crop the image tensor at half its height
            crop_height = height // 2
            cropped_tensor = mirrored_image[:, :crop_height, :, :]

            # Flip the cropped tensor vertically
            flipped_tensor = torch.flip(cropped_tensor, dims=[1])

            # Concatenate the cropped and flipped tensors back together
            merged_tensor = torch.cat([cropped_tensor, flipped_tensor], dim=1)
            return (merged_tensor,)
        else:
            raise ValueError(f"Unsupported blend mode: {blend_mode}")
        return (mirrored_image,)


NODE_CLASS_MAPPINGS = {
    "Symmetry Mirror": Mirror,
}