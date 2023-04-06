import random


class DescribeCharacter:

    def __init__(self):
        pass
    # @classmethod
    def INPUT_TYPES():
        return {
            "required": {
                "age": (["child","teenager","young adult","adult","middle-aged","elderly"], ),
                "gender": (["male","female"], ),
                "eye_color": (["blue","brown","green","hazel","amber","gray","black","red","violet","pink","purple","yellow"], ),
                "hair_color": (["blonde","brown","black","red","gray","white","blue","green","pink","purple","yellow","orange","violet"], ),
                "hair_length": (["short","medium","long"], ),
                "hair_style": (["bald","bun","ponytail","curly","straight","wavy","braided","mohawk","pixie","afro","bob","bangs","ponytail","braid","dreadlocks","mullet","side part","top knot","undercut","bowl cut","butterfly","cornrows","dutch braid","fishtail braid","french braid","half up","half down","high ponytail"], ),
                "body_type": (["slim","average","athletic","curvy","chubby","overweight","obese"], ),
                "ethnicity": (["white","black","japanese","korean","chinese","indonesian","hispanic","middle eastern","indian","native american","pacific islander"], ),
                "safety": (["sfw","nsfw"], ),
            }
        }
    RETURN_TYPES = ("RAW_TEXT","RAW_TEXT",)
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "gen_human"

    CATEGORY = "generation"

    def gen_human(self,age,gender,eye_color,hair_color,hair_length,hair_style,body_type,ethnicity,safety):
        positive_prompt = []
        negative_prompt = []
        ages = ["child","teenager","young adult","adult","middle-aged","elderly"]
        eye_colors = ["blue","brown","green","hazel","amber","gray","black","red","violet","pink","purple","yellow"]
        hair_lengths = ["short","medium","long"]
        hair_styles = ["bald","bun","ponytail","curly","straight","wavy","braided","mohawk","pixie","afro","bob","bangs","ponytail","braid","dreadlocks","mullet","side part","top knot","undercut","bowl cut","butterfly","cornrows","dutch braid","fishtail braid","french braid","half up","half down","high ponytail"]
        hair_colors = ["blonde","brown","black","red","gray","white","blue","green","pink","purple","yellow","orange","violet"]
        body_types = ["slim","average","athletic","curvy","chubby","overweight","obese"]
        ethnicities = ["white","black","japanese","korean","chinese","indonesian","hispanic","middle eastern","indian","native american","pacific islander"]

        #age
        positive_prompt.append(age)
        ages.remove(age)
        negative_prompt.append(" ".join(ages))

        #gender
        if gender == "random":
            gender = random.choice(["male","female"])
        positive_prompt.append(gender)
        if gender == "male":
            positive_prompt.append("1boy")
            negative_prompt.append("female, multiple people,multiple subjects")
        else:
            positive_prompt.append("1girl")
            negative_prompt.append("male, multiple people,multiple subjects")
        
        #eye color
        positive_prompt.append(f'with {eye_color} eyes')
        eye_colors.remove(eye_color)
        negative_prompt.append(" ".join(eye_colors))

        #hair length
        positive_prompt.append(f'and {hair_length}')
        hair_lengths.remove(hair_length)
        negative_prompt.append(" hair,".join(hair_lengths))

        #hair color
        positive_prompt.append(hair_color)
        hair_colors.remove(hair_color)
        negative_prompt.append("-colored hair,".join(hair_colors))

        #hair style
        positive_prompt.append(f'{hair_style} hair')
        hair_styles.remove(hair_style)
        negative_prompt.append("-styled hair, ".join(hair_styles))

        #body type
        positive_prompt.append(f'and a {body_type} body')
        body_types.remove(body_type)
        negative_prompt.append(" body,".join(body_types))

        #ethnicity
        positive_prompt.append(f'of {ethnicity} descent')
        ethnicities.remove(ethnicity)
        negative_prompt.append(",".join(ethnicities))

        #safety
        if safety == "nsfw":
            positive_prompt.append(",nsfw")
        if safety == "sfw":
            positive_prompt.append(",sfw")
        

        #reset lists
        ages = ["child","teenager","young adult","adult","middle-aged","elderly"]
        eye_colors = ["blue","brown","green","hazel","amber","gray","black","red","violet","pink","purple","yellow"]
        hair_lengths = ["short","medium","long"]
        hair_styles = ["bald","bun","ponytail","curly","straight","wavy","braided","mohawk","pixie","afro","bob","bangs","ponytail","braid","dreadlocks","mullet","side part","top knot","undercut","bowl cut","butterfly","cornrows","dutch braid","fishtail braid","french braid","half up","half down","high ponytail"]
        hair_colors = ["blonde","brown","black","red","gray","white","blue","green","pink","purple","yellow","orange","violet"]
        body_types = ["a slim","an average","an athletic","a curvy","a chubby","an overweight","an obese"]
        ethnicities = ["white","black","japanese","korean","chinese","indonesian","hispanic","middle eastern","indian","native american","pacific islander"]
        
        return (" ".join(positive_prompt)," ".join(negative_prompt), )

class DescribeStyle:

    def __init__(self):
        pass
    # @classmethod
    def INPUT_TYPES():
        return {
            "required": {
                "Style": (["anime","manga","realistic","sci-fi","3D Render"], ),
            }
        }
    RETURN_TYPES = ("RAW_TEXT",)
    RETURN_NAMES = ("Style",)

    FUNCTION = "gen_style"

    CATEGORY = "generation"

    def gen_style(self,Style):
        if Style == "anime":
            return ("anime,makoto shinkai,ghibli,anime screencap,screencap", )
        if Style == "manga":
            return ("(drawing), manga pen drawing, grayscale, manga character, style of toriyama akira, style of otomo katsuhiro, style of urasawa naoki, style of arakawa hiromu, style of murata yusuke, style of ito junji, style of inoue takehiko, style of oda eiichiro", )
        if Style == "realistic":
            return ("realistic,intricate details,sharp focus, film grain, high definition, insanely detailed, hdr, lightroom, 8k, 4k", )
        if Style == "sci-fi":
            return ("sci-fi,science fiction, cyberpunk, highly detailed, futuristic, cyborg, bionic, 8k, ghost in the shell, star wars, blade runner, tech, hyper-realistic, intricate details", )
        if Style == "3D Render":
            return ("3D Render, ArtStation, Octane, Blender, PBR, film grain, ray tracing, volumetric", )
        return (f'{Style}', )

class DescribeScene:

    def __init__(self):
        pass
    # @classmethod
    def INPUT_TYPES():
        return {
            "required": {
                "Style": ("RAW_TEXT", ),
            },
            "optional": {
                "Character": ("RAW_TEXT", ),
                "Location": ("RAW_TEXT", ),
                "Action": ("RAW_TEXT", ),
                "Emotion": ("RAW_TEXT", ),
                "Lighting": ("RAW_TEXT", ),
            },
        }
    RETURN_TYPES = ("RAW_TEXT",)
    RETURN_NAMES = ("Scene Prompt",)
    FUNCTION = "gen_scene"

    CATEGORY = "generation"

    def gen_scene(self,Style,Character="",Location="",Action="",Emotion="",Lighting=""):
        prompt = f'{Character}, {Location}, {Action}, {Emotion}, {Lighting}, {Style}'
        # if Style includes "manga" prepend the prompt with "drawing"
        if "manga" in Style:
            prompt = f'manga sketch of {prompt}'
        return (prompt, )
    
NODE_CLASS_MAPPINGS = {
    "Character": DescribeCharacter,
    "Style": DescribeStyle,
    "Scene": DescribeScene,
}