
import os


class LoadImageWithAspectRatio:

    def __init__(self) -> None:
        pass
    input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")
    @classmethod
    def INPUT_TYPES(s):
        if not os.path.exists(s.input_dir):
            os.makedirs(s.input_dir)
        return {"required":
                    {"image":( "IMAGE",), },
                }

    CATEGORY = "image"

    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "get_aspect_ratio"
    def get_aspect_ratio(self, image):
        height2 = image.shape[1]
        width2 = image.shape[2]

        aspect_ratio2 = float(width2 / height2)

        return (aspect_ratio2,)


class AspectRatioToResolution:

    def __init__(self) -> None:
        pass
    # @classmethod
    def INPUT_TYPES():
        return {
            "required": {
                "Shortest_Side": ("INT", {"default": 512}),
                "Aspect_Ratio": ("FLOAT", {"default": 1.0}),
            },
        }
    RETURN_TYPES = ("INT","INT",)
    RETURN_NAMES = ("Width","Height",)
    FUNCTION = "get_resolution"

    CATEGORY = "utils"

    def get_resolution(self,Shortest_Side,Aspect_Ratio):
        Width = 512
        Height = 512
        pixel_multiplier = 64
        if Aspect_Ratio < 1.0:
            Width = Shortest_Side
            Height = int(Width / Aspect_Ratio)
        else:
            Height = Shortest_Side
            Width = int(Height * Aspect_Ratio)
        
        if Width/pixel_multiplier % 2 != 0:
            #Width is equal to next multiple of 64
            Width = int(Width/pixel_multiplier)*pixel_multiplier+pixel_multiplier
        if Height/pixel_multiplier % 2 != 0:
            #Height is equal to next multiple of 8
            Height = int(Height/pixel_multiplier)*pixel_multiplier+pixel_multiplier

        print(f'Width: {Width}, Height: {Height}, Aspect Ratio: {Aspect_Ratio}')
        return (Width,Height,)

NODE_CLASS_MAPPINGS = {
    "LoadImageWithAspectRatio": LoadImageWithAspectRatio,
    "AspectRatioToResolution": AspectRatioToResolution,
}