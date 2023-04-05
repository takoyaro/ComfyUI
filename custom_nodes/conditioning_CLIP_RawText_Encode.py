class CLIPRawTextEncode:

    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"prompt": ("RAW_TEXT", {"multiline": True}),"neg_prompt": ("RAW_TEXT", {"multiline": True}), "clip": ("CLIP", )}}
    RETURN_TYPES = ("CONDITIONING","CONDITIONING",)
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "encode"

    CATEGORY = "conditioning"

    def encode(self, clip, prompt,neg_prompt):
        print(f'\nprompt: {prompt}\n\nneg_prompt: {neg_prompt}\n')
        return (
            [[clip.encode(str(prompt)), {}]],
            [[clip.encode(str(neg_prompt)), {}]]
        , )
    
NODE_CLASS_MAPPINGS = {
    "CLIP_RawTextEncode_ToPrompts": CLIPRawTextEncode,
}