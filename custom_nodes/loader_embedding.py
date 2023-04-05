import folder_paths

class EmbeddingLoader:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "embedding_name": (folder_paths.get_filename_list("embeddings"), ),
                "strength": ("FLOAT", {"min": 0, "max": 64, "default": 1, "step": 0.1})
            }
        }

    RETURN_TYPES = ("RAW_TEXT",)
    FUNCTION = "load_embedding"

    CATEGORY = "loaders"

    def load_embedding(self, embedding_name,strength):

        return (f'(embedding:{embedding_name}):{strength}',)

NODE_CLASS_MAPPINGS = {
    "EmbeddingLoader": EmbeddingLoader,
}
