class MathFloatInput:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"_float": ("FLOAT", {"default": 0.0, "step": 0.01})},
        }

    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "exec"

    CATEGORY = "Math"

    def exec(self, _float=0.0):
        print(f"FloatInput: {_float}")
        return { _float }

class MathIntInput:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"_int": ("INT", {"default": 0, "step": 1})},
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "exec"

    CATEGORY = "Math"

    def exec(self, _int=0):
        print(f"IntInput: {_int}")
        return { _int }

NODE_CLASS_MAPPINGS = {
    "Single Float": MathFloatInput,
    "Single Integer": MathIntInput,
}